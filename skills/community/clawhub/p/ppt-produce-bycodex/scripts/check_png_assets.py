#!/usr/bin/env python3
"""Inspect PPT PNG assets for dimensions and color mode."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def main() -> int:
    parser = argparse.ArgumentParser(description="Check PNG dimensions and image modes.")
    parser.add_argument("png_dir", type=Path, help="Directory containing PNG slides")
    parser.add_argument("--min-width", type=int, default=2048)
    parser.add_argument("--min-height", type=int, default=1152)
    args = parser.parse_args()

    if not args.png_dir.exists():
        raise SystemExit(f"Directory does not exist: {args.png_dir}")

    pngs = sorted(args.png_dir.glob("*.png"))
    if not pngs:
        raise SystemExit(f"No PNG files found in: {args.png_dir}")

    failed = False
    for path in pngs:
        with Image.open(path) as image:
            width, height = image.size
            mode = image.mode
            has_alpha = mode in {"RGBA", "LA"} or ("transparency" in image.info)
            too_small = width < args.min_width or height < args.min_height
            status = "OK"
            notes = []
            if too_small:
                status = "WARN"
                failed = True
                notes.append(f"below {args.min_width}x{args.min_height}")
            if has_alpha:
                status = "WARN"
                failed = True
                notes.append("has alpha/transparency")
            detail = f" ({', '.join(notes)})" if notes else ""
            print(f"{status}\t{path.name}\t{width}x{height}\t{mode}{detail}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
