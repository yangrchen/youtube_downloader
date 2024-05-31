#!/usr/bin/env python

from pytube import YouTube
from argparse import ArgumentParser
from tqdm import tqdm
from functools import partial
from pathlib import Path


def _progress_callback(stream, chunk, bytes_remaining, progress_bar, file_size):
    progress_bar.update(file_size - bytes_remaining - progress_bar.n)


def download(url: str, download_path: str):
    try:
        yt = YouTube(url)
        yt.check_availability()
        stream = yt.streams.filter(
            progressive=True,
            file_extension="mp4",
        ).get_highest_resolution()
        file_size = stream.filesize
        progress_bar = tqdm(
            total=file_size,
            unit="B",
            unit_scale=True,
            desc=stream.title,
        )
        yt.register_on_progress_callback(
            partial(
                _progress_callback,
                progress_bar=progress_bar,
                file_size=file_size,
            )
        )
        stream.download(output_path=download_path)
        progress_bar.close()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--url", type=str, required=True, help="URL of YouTube video to be downloaded."
    )
    parser.add_argument(
        "-o", default=None, type=str, help="Output path for downloaded YouTube video"
    )
    args, _ = parser.parse_known_args()

    if args.o is not None:
        if not Path(args.o).exists():
            print(
                "Specified download path cannot be found. Defaulting to current directory."
            )
            args.o = None

    download(url=args.url, download_path=args.o)
