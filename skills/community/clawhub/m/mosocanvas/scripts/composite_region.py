#!/usr/bin/env python3
"""Composite a generated crop into an immutable source through a supplied mask."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("generated_crop", type=Path)
    parser.add_argument("mask", type=Path)
    parser.add_argument("--crop-origin", required=True, help="x,y in source coordinates")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    x, y = [int(part) for part in args.crop_origin.split(",")]
    source = Image.open(args.source).convert("RGB")
    generated = Image.open(args.generated_crop).convert("RGB")
    mask = Image.open(args.mask).convert("L")
    if generated.size != mask.size:
        raise ValueError(f"generated crop {generated.size} != mask {mask.size}")

    destination = source.crop((x, y, x + generated.width, y + generated.height))
    composited_crop = Image.composite(generated, destination, mask)
    output = source.copy()
    output.paste(composited_crop, (x, y))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    output.save(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
