#!/usr/bin/env python3
"""Measure reference-image properties without making aesthetic claims."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps, ImageStat


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def channel_stats(image: Image.Image) -> dict:
    stats = ImageStat.Stat(image)
    return {
        "mean": round(stats.mean[0], 3),
        "stddev": round(stats.stddev[0], 3),
        "minimum": image.getextrema()[0],
        "maximum": image.getextrema()[1],
    }


def palette(rgb: Image.Image, colors: int) -> list[dict]:
    quantized = rgb.quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
    raw_palette = quantized.getpalette()
    total = rgb.width * rgb.height
    entries = []
    for count, index in sorted(quantized.getcolors() or [], reverse=True):
        offset = index * 3
        red, green, blue = raw_palette[offset : offset + 3]
        luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
        entries.append(
            {
                "hex": f"#{red:02X}{green:02X}{blue:02X}",
                "rgb": [red, green, blue],
                "coverage": round(count / total, 4),
                "relative_luminance_8bit": round(luminance, 2),
            }
        )
    return entries


def high_chroma_candidates(rgb: Image.Image, limit: int = 8) -> list[dict]:
    """Surface small saturated accents that a coverage-sorted palette can hide."""
    quantized = rgb.quantize(colors=32, method=Image.Quantize.MEDIANCUT)
    raw_palette = quantized.getpalette()
    total = rgb.width * rgb.height
    candidates = []
    for count, index in quantized.getcolors() or []:
        offset = index * 3
        red, green, blue = raw_palette[offset : offset + 3]
        chroma = max(red, green, blue) - min(red, green, blue)
        coverage = count / total
        if coverage < 0.0005 or chroma < 24:
            continue
        candidates.append(
            {
                "hex": f"#{red:02X}{green:02X}{blue:02X}",
                "rgb": [red, green, blue],
                "coverage": round(coverage, 5),
                "chroma_8bit": chroma,
                "_rank": chroma * math.sqrt(coverage),
            }
        )
    candidates.sort(key=lambda entry: entry["_rank"], reverse=True)
    for entry in candidates:
        entry.pop("_rank")
    return candidates[:limit]


def edge_density(gray: Image.Image, threshold: int) -> float:
    edges = gray.filter(ImageFilter.FIND_EDGES)
    if edges.width > 2 and edges.height > 2:
        edges = edges.crop((1, 1, edges.width - 1, edges.height - 1))
    histogram = edges.histogram()
    active = sum(histogram[threshold:])
    return round(active / (edges.width * edges.height), 4)


def grid_measurements(rgb: Image.Image) -> list[dict]:
    hsv = rgb.convert("HSV")
    cells = []
    for row in range(3):
        for column in range(3):
            left = math.floor(column * rgb.width / 3)
            right = math.floor((column + 1) * rgb.width / 3)
            top = math.floor(row * rgb.height / 3)
            bottom = math.floor((row + 1) * rgb.height / 3)
            rgb_cell = rgb.crop((left, top, right, bottom))
            hsv_cell = hsv.crop((left, top, right, bottom))
            cells.append(
                {
                    "row": row,
                    "column": column,
                    "mean_luminance_8bit": round(ImageStat.Stat(rgb_cell.convert("L")).mean[0], 2),
                    "mean_saturation_8bit": round(ImageStat.Stat(hsv_cell.getchannel("S")).mean[0], 2),
                }
            )
    return cells


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument("--colors", type=int, default=8)
    parser.add_argument("--edge-threshold", type=int, default=32)
    parser.add_argument("--max-analysis-size", type=int, default=768)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if not 2 <= args.colors <= 32:
        parser.error("--colors must be between 2 and 32")
    if not 0 <= args.edge_threshold <= 255:
        parser.error("--edge-threshold must be between 0 and 255")

    with Image.open(args.image) as source:
        oriented = ImageOps.exif_transpose(source)
        original = {
            "width_px": oriented.width,
            "height_px": oriented.height,
            "aspect_ratio": round(oriented.width / oriented.height, 6),
            "mode": oriented.mode,
            "format": source.format,
        }
        rgb = oriented.convert("RGB")
    rgb.thumbnail((args.max_analysis_size, args.max_analysis_size), Image.Resampling.LANCZOS)
    gray = rgb.convert("L")
    saturation = rgb.convert("HSV").getchannel("S")

    result = {
        "schema": "moso.reference-measurement/0.2",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_ref": str(args.image.resolve()),
        "sha256": sha256(args.image),
        "original": original,
        "analysis_size": {"width_px": rgb.width, "height_px": rgb.height},
        "dominant_palette": palette(rgb, args.colors),
        "high_chroma_candidates": high_chroma_candidates(rgb),
        "luminance": channel_stats(gray),
        "saturation": channel_stats(saturation),
        "edge_density": {
            "threshold_8bit": args.edge_threshold,
            "ratio": edge_density(gray, args.edge_threshold),
        },
        "three_by_three_grid": grid_measurements(rgb),
        "limits": [
            "Measurements do not identify semantic subjects, visual hierarchy, cultural meaning, or quality.",
            "Palette values are quantized and can change with color profile conversion.",
            "Edge density is threshold-dependent and is not a texture or detail score."
        ],
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
