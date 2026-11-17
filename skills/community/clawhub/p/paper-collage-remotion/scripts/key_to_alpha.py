#!/usr/bin/env python3
"""Convert a near-green background to alpha while preserving non-green pixels."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Input image with a green background")
    parser.add_argument("output", type=Path, help="Output transparent PNG")
    parser.add_argument("--tolerance", type=int, default=85, help="Green dominance threshold, 0-255")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not 0 <= args.tolerance <= 255:
        raise SystemExit("tolerance must be between 0 and 255")
    image = Image.open(args.source).convert("RGBA")
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            red, green, blue, alpha = pixels[x, y]
            dominance = green - max(red, blue)
            if green > 70 and dominance >= args.tolerance:
                pixels[x, y] = (red, green, blue, 0)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output)


if __name__ == "__main__":
    main()
