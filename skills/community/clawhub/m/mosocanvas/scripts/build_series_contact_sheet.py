#!/usr/bin/env python3
"""Build a labeled carrier-ratio contact sheet for series review."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("images", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--columns", type=int, default=4)
    parser.add_argument("--cell-width", type=int, default=300)
    parser.add_argument("--background", default="#171717")
    args = parser.parse_args()

    if args.columns < 1 or args.cell_width < 64:
        parser.error("columns must be >=1 and cell-width must be >=64")
    missing = [str(path) for path in args.images if not path.exists()]
    if missing:
        parser.error("missing images: " + ", ".join(missing))

    opened = [Image.open(path).convert("RGB") for path in args.images]
    ratios = [image.height / image.width for image in opened]
    cell_height = round(args.cell_width * max(ratios))
    label_height = 34
    gap = 16
    rows = math.ceil(len(opened) / args.columns)
    width = gap + args.columns * (args.cell_width + gap)
    height = gap + rows * (cell_height + label_height + gap)
    sheet = Image.new("RGB", (width, height), args.background)
    draw = ImageDraw.Draw(sheet)

    for index, (path, image) in enumerate(zip(args.images, opened), start=1):
        column = (index - 1) % args.columns
        row = (index - 1) // args.columns
        x = gap + column * (args.cell_width + gap)
        y = gap + row * (cell_height + label_height + gap)
        fitted = ImageOps.contain(image, (args.cell_width, cell_height))
        px = x + (args.cell_width - fitted.width) // 2
        py = y + (cell_height - fitted.height) // 2
        sheet.paste(fitted, (px, py))
        draw.text((x, y + cell_height + 8), f"{index:02d}  {path.name}", fill="#f0f0f0")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output)
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
