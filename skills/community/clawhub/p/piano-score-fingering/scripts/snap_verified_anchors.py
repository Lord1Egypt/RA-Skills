#!/usr/bin/env python3
"""Snap already verified source anchors to nearby notehead-shaped ink.

This is a coordinate-only repair: it never creates notes, changes pitches, or
promotes candidates.  It is safe only after visual recognition has already
verified the event inventory and pitch geometry.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from audit_source_clearance import source_image
from audit_source_noteheads import best_nearby_ink
from plan_io import load_plan, page_map, save_plan
from render_fingering_pdf import png_pixels


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", required=True, type=Path)
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--radius", type=int, default=7)
    args = parser.parse_args()
    if not 3 <= args.radius <= 16:
        raise ValueError("--radius must be 3..16")
    plan = load_plan(args.input)
    page = page_map(plan).get(args.page)
    if page is None:
        raise ValueError(f"page {args.page} is not declared")
    width, height, pixels, colorspace = png_pixels(source_image(args.input, page).read_bytes())
    if colorspace != "/DeviceRGB":
        raise ValueError("source PNG must be RGB/RGBA")
    sx, sy = width / float(page["width"]), height / float(page["height"])
    snapped = 0
    for note in plan["notes"]:
        if int(note.get("page", 0)) != args.page or note.get("anchor_verified") is not True:
            continue
        x, y = float(note["page_x"]) * sx, float(note["page_y"]) * sy
        thick, density, widest, best_x, best_y = best_nearby_ink(pixels, width, height, x, y, args.radius)
        if density >= 11 and widest >= 4 and thick >= 2:
            note["page_x"] = round(best_x / sx, 3)
            note["page_y"] = round(best_y / sy, 3)
            note["anchor_method"] = "verified_notehead_ink_snap"
            snapped += 1
    save_plan(args.output, plan)
    print(f"Snapped {snapped} verified anchors on page {args.page}: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
