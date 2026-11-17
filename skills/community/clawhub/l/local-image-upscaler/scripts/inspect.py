#!/usr/bin/env python3
"""Inspect image dimensions, megapixels, aspect ratios, and file sizes."""

from __future__ import annotations

import argparse
import json
import sys
from math import gcd
from pathlib import Path

from upscale import read_dimensions


SUPPORTED_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


def describe(path: Path) -> dict:
    width, height = read_dimensions(path)
    divisor = gcd(width, height)
    return {
        "path": str(path),
        "width": width,
        "height": height,
        "aspect_ratio": f"{width // divisor}:{height // divisor}",
        "megapixels": round(width * height / 1_000_000, 2),
        "size_bytes": path.stat().st_size,
        "size_kib": round(path.stat().st_size / 1024, 1),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--recursive", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.input.expanduser().resolve()
    if not source.exists():
        raise RuntimeError(f"Input does not exist: {source}")
    if source.is_file():
        paths = [source]
    else:
        pattern = "**/*" if args.recursive else "*"
        paths = sorted(path for path in source.glob(pattern) if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES)
    results = [describe(path) for path in paths]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(
                f"{item['path']}\n"
                f"  {item['width']}x{item['height']} | {item['aspect_ratio']} | "
                f"{item['megapixels']:.2f} MP | {item['size_kib']:.1f} KiB"
            )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
