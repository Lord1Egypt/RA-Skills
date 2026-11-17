#!/usr/bin/env python3
"""Subtract reviewed protection regions from an existing grayscale repair mask."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


def draw_regions(size: tuple[int, int], regions_path: Path) -> Image.Image:
    result = Image.new("L", size, 0)
    draw = ImageDraw.Draw(result)
    data = json.loads(regions_path.read_text(encoding="utf-8"))
    for region in data["regions"]:
        kind = region["kind"]
        if kind == "polygon":
            draw.polygon([tuple(point) for point in region["points"]], fill=255)
        elif kind == "ellipse":
            draw.ellipse(tuple(region["box"]), fill=255)
        elif kind == "rectangle":
            draw.rectangle(tuple(region["box"]), fill=255)
        else:
            raise ValueError(f"unsupported region kind: {kind}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("mask", type=Path)
    parser.add_argument("exclusions", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--preview", type=Path, required=True)
    parser.add_argument("--exclusion-grow", type=int, default=2)
    parser.add_argument("--exclusion-feather", type=float, default=1.5)
    args = parser.parse_args()

    source = Image.open(args.source).convert("RGB")
    mask = Image.open(args.mask).convert("L")
    if mask.size != source.size:
        raise SystemExit(f"mask {mask.size} does not match source {source.size}")
    exclusions = draw_regions(source.size, args.exclusions)
    if args.exclusion_grow:
        exclusions = exclusions.filter(ImageFilter.MaxFilter(args.exclusion_grow * 2 + 1))
    if args.exclusion_feather:
        exclusions = exclusions.filter(ImageFilter.GaussianBlur(args.exclusion_feather))
    refined = ImageChops.multiply(mask, ImageChops.invert(exclusions))

    for path in (args.output, args.preview):
        path.parent.mkdir(parents=True, exist_ok=True)
    refined.save(args.output)

    overlay = source.convert("RGBA")
    cyan = Image.new("RGBA", source.size, (0, 220, 255, 0))
    cyan.putalpha(refined.point(lambda value: round(value * 0.72)))
    magenta = Image.new("RGBA", source.size, (255, 40, 180, 0))
    magenta.putalpha(exclusions.point(lambda value: round(value * 0.22)))
    Image.alpha_composite(Image.alpha_composite(overlay, magenta), cyan).save(args.preview)


if __name__ == "__main__":
    main()
