#!/usr/bin/env python3

import argparse
import urllib.parse
import urllib.request
from pathlib import Path

DOWNLOAD_DIR = Path("/")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()

    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    filename = Path(urllib.parse.urlparse(args.url).path).name or "download"
    destination = DOWNLOAD_DIR / filename

    with urllib.request.urlopen(args.url) as response:
        destination.write_bytes(response.read())

    print(destination)


if __name__ == "__main__":
    main()