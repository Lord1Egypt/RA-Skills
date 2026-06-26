#!/usr/bin/env python3
import pathlib
import subprocess
import sys


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: download_pinterest_video.py <m3u8-url> <output.mp4>", file=sys.stderr)
        return 1

    m3u8_url = sys.argv[1]
    output = pathlib.Path(sys.argv[2]).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        m3u8_url,
        "-c",
        "copy",
        str(output),
    ]
    return subprocess.run(cmd, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
