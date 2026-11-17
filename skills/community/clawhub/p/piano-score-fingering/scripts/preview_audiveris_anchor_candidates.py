#!/usr/bin/env python3
"""Render a review-only overlay for Audiveris candidate notehead anchors.

This accepts the JSON made by ``extract_audiveris_anchor_candidates.py`` and
never touches a fingering plan.  It exists so a person or multimodal model can
compare candidate geometry with the *original* rendered page before deciding
whether to use it as a review aid.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from preview_anchor_candidates import mark, write_png
from render_fingering_pdf import png_pixels


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("anchors", type=Path, help="candidate-anchor JSON from extract_audiveris_anchor_candidates.py")
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--minimum-grade", type=float, default=0.75,
                        help="orange below this Audiveris context grade; blue otherwise")
    args = parser.parse_args()
    if not 0 <= args.minimum_grade <= 1:
        parser.error("--minimum-grade must be 0..1")
    data = json.loads(args.anchors.read_text(encoding="utf-8"))
    if data.get("candidate_only") is not True:
        raise ValueError("anchor input must be explicitly candidate-only")
    page = next((item for item in data.get("pages", []) if int(item.get("page", 0)) == args.page), None)
    if not isinstance(page, dict):
        raise ValueError(f"page {args.page} was not found in the anchor file")
    source = Path(str(page.get("target_image") or ""))
    if not source.is_file():
        raise ValueError("candidate anchor page has no usable original target_image")
    width, height, raw, colorspace = png_pixels(source.read_bytes())
    if colorspace != "/DeviceRGB":
        raise ValueError("target image must be RGB/RGBA PNG")
    pixels = bytearray(raw)
    total = low = 0
    for head in page.get("candidate_noteheads", []):
        if not isinstance(head, dict) or "page_x" not in head or "page_y" not in head:
            continue
        try:
            x, y = round(float(head["page_x"])), round(float(head["page_y"]))
            grade = float(head.get("context_grade", head.get("grade", 0)))
        except (TypeError, ValueError):
            continue
        is_low = grade < args.minimum_grade
        mark(pixels, width, height, x, y, (231, 111, 0) if is_low else (22, 87, 170))
        total += 1
        low += int(is_low)
    write_png(args.output, width, height, bytes(pixels))
    print(f"Rendered {total} candidate anchor crosses ({low} low-grade): {args.output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: {exc}")
