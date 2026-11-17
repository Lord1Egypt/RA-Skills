#!/usr/bin/env python3
"""Split an evenly gridded character sheet into trimmed transparent PNG layers."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Source PNG or image sheet")
    parser.add_argument("output_dir", type=Path, help="Directory for output PNG layers")
    parser.add_argument("prefix", help="Output prefix, e.g. close")
    parser.add_argument("count", type=int, help="Number of cells to export")
    parser.add_argument("--columns", type=int, help="Grid column count (default: count)")
    parser.add_argument("--rows", type=int, help="Grid row count (derived by default)")
    parser.add_argument("--padding", type=int, default=0, help="Shared gutter in source pixels")
    parser.add_argument("--no-trim", action="store_true", help="Keep complete cell bounds")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.count < 1 or args.padding < 0:
        raise SystemExit("count must be positive and padding cannot be negative")

    image = Image.open(args.source).convert("RGBA")
    columns = args.columns or args.count
    rows = args.rows or -(-args.count // columns)
    if columns < 1 or rows < 1 or args.count > columns * rows:
        raise SystemExit("grid dimensions cannot contain the requested count")

    usable_width = image.width - args.padding * (columns + 1)
    usable_height = image.height - args.padding * (rows + 1)
    if usable_width < columns or usable_height < rows:
        raise SystemExit("padding leaves no usable image area")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for index in range(args.count):
        row, column = divmod(index, columns)
        left = args.padding + round(column * usable_width / columns)
        right = args.padding + round((column + 1) * usable_width / columns)
        top = args.padding + round(row * usable_height / rows)
        bottom = args.padding + round((row + 1) * usable_height / rows)
        tile = image.crop((left, top, right, bottom))
        if not args.no_trim:
            alpha = tile.getchannel("A")
            bbox = alpha.getbbox()
            if bbox is None:
                print(f"Skipping empty cell {index + 1}")
                continue
            tile = tile.crop(bbox)
        output = args.output_dir / f"{args.prefix}-{index + 1}.png"
        tile.save(output)
        print(output)


if __name__ == "__main__":
    main()
