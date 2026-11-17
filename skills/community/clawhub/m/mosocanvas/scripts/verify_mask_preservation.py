#!/usr/bin/env python3
"""Verify that a repaired image changed no pixels outside a placed mask."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image


def parse_origin(value: str) -> tuple[int, int]:
    try:
        x_text, y_text = value.split(",", 1)
        return int(x_text), int(y_text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("origin must be x,y") from exc


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("mask", type=Path)
    parser.add_argument("--mask-origin", type=parse_origin, default=(0, 0))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    source = np.asarray(Image.open(args.source).convert("RGB"))
    candidate = np.asarray(Image.open(args.candidate).convert("RGB"))
    if source.shape != candidate.shape:
        raise SystemExit(f"dimension mismatch: {source.shape} != {candidate.shape}")

    local_mask = np.asarray(Image.open(args.mask).convert("L"))
    x, y = args.mask_origin
    height, width = local_mask.shape
    full_mask = np.zeros(source.shape[:2], dtype=np.uint8)
    if x < 0 or y < 0 or x + width > source.shape[1] or y + height > source.shape[0]:
        raise SystemExit("placed mask exceeds source bounds")
    full_mask[y : y + height, x : x + width] = local_mask

    changed = np.any(source != candidate, axis=2)
    outside_changed = changed & (full_mask == 0)
    changed_y, changed_x = np.where(changed)

    report = {
        "source_dimensions": [int(source.shape[1]), int(source.shape[0])],
        "candidate_dimensions": [int(candidate.shape[1]), int(candidate.shape[0])],
        "mask_origin": [x, y],
        "mask_dimensions": [width, height],
        "mask_nonzero_pixels": int(np.count_nonzero(full_mask)),
        "changed_pixels": int(np.count_nonzero(changed)),
        "outside_mask_changed_pixels": int(np.count_nonzero(outside_changed)),
        "outside_mask_preserved_exactly": not bool(np.any(outside_changed)),
        "changed_bbox": (
            None
            if changed_x.size == 0
            else [
                int(changed_x.min()),
                int(changed_y.min()),
                int(changed_x.max()) + 1,
                int(changed_y.max()) + 1,
            ]
        ),
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
