#!/usr/bin/env python3
"""Reject planned fingering labels that would cover black ink in the source PNG.

This complements geometric ownership checks.  It inspects the original rendered
score page—not a reconstructed staff—and catches labels placed onto noteheads,
stems, beams, accidentals, slurs, or staff lines.  The plan must use a local
PNG page image whose coordinate system matches ``pages[].width/height``.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from audit_annotation_layout import event_key, label_position
from plan_io import finite_number, load_plan, page_map
from render_fingering_pdf import png_pixels


def source_image(plan_path: Path, page: dict) -> Path:
    raw = str(page.get("image", "")).strip()
    if not raw:
        raise ValueError("source-clearance audit requires pages[].image")
    candidate = Path(raw)
    if not candidate.is_absolute():
        candidate = plan_path.parent / candidate
    if candidate.suffix.lower() != ".png":
        raise ValueError("source-clearance audit requires a PNG page image")
    if not candidate.is_file():
        raise ValueError(f"page image not found: {candidate}")
    return candidate


def dark_pixels(
    pixels: bytes, width: int, height: int, x0: int, y0: int, x1: int, y1: int,
) -> int:
    count = 0
    for y in range(max(0, y0), min(height, y1)):
        row = y * width * 3
        for x in range(max(0, x0), min(width, x1)):
            red, green, blue = pixels[row + x * 3:row + x * 3 + 3]
            # Music notation is near-neutral and dark.  Restricting the hue
            # avoids counting a coloured page watermark as musical ink.
            if max(red, green, blue) < 150 and max(red, green, blue) - min(red, green, blue) < 22:
                count += 1
    return count


def label_box(note: dict, members: list[dict], sx: float, sy: float, dpi: float) -> tuple[int, int, int, int]:
    """Return the conservative source-pixel box occupied by one printed digit."""
    x, baseline_y = label_position(note, members)
    x, baseline_y = x * sx, baseline_y * sy
    font_px = finite_number(note.get("font_size", 10), "font_size") * dpi / 72.0
    return (
        round(x - font_px * 0.62), round(baseline_y - font_px * 0.78),
        round(x + font_px * 0.58), round(baseline_y + font_px * 0.48),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--dpi", type=float, default=144.0, help="DPI used to render pages[].image")
    parser.add_argument("--minimum", type=float, default=0.90)
    parser.add_argument("--max-dark-pixels", type=int, default=4, help="allowed black source pixels in a label box")
    parser.add_argument(
        "--candidate-diagnostic", action="store_true",
        help="measure an OMR candidate layout without promoting its score semantics",
    )
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    if args.dpi < 36 or args.dpi > 600:
        raise ValueError("dpi must be between 36 and 600")
    if not 0 < args.minimum <= 1 or args.max_dark_pixels < 0:
        raise ValueError("minimum must be 0..1 and max-dark-pixels must be non-negative")

    plan = load_plan(args.plan)
    source_type = str(plan.get("source", {}).get("type", "")).lower()
    candidate_mode = args.candidate_diagnostic and source_type == "omr_candidate"
    if source_type not in {"pdf", "image"} and not candidate_mode:
        raise ValueError("source-clearance audit is only meaningful for pdf/image plans")
    page = page_map(plan).get(args.page)
    if page is None:
        raise ValueError(f"page {args.page} is not declared by the plan")
    width, height, pixels, colorspace = png_pixels(source_image(args.plan, page).read_bytes())
    if colorspace != "/DeviceRGB":
        raise ValueError("source PNG must be RGB/RGBA")
    plan_width = finite_number(page["width"], "page.width")
    plan_height = finite_number(page["height"], "page.height")
    sx, sy = width / plan_width, height / plan_height
    if abs(sx - sy) > 0.03 * max(sx, sy):
        raise ValueError("source image aspect ratio conflicts with plan page")

    notes = [note for note in plan["notes"] if int(note.get("page", 0)) == args.page and int(note.get("finger", 0)) in {1, 2, 3, 4, 5}]
    events: dict[tuple, list[dict]] = defaultdict(list)
    for note in notes:
        events[event_key(note)].append(note)
    checked = clear = 0
    failures: list[str] = []
    for note in notes:
        if note.get("anchor_verified") is not True and not (
            candidate_mode and note.get("anchor_candidate") is True
        ):
            failures.append(f"{note['note_id']}: source anchor is not verified")
            continue
        x0, y0, x1, y1 = label_box(note, events[event_key(note)], sx, sy, args.dpi)
        ink = dark_pixels(pixels, width, height, x0, y0, x1 + 1, y1 + 1)
        checked += 1
        if ink <= args.max_dark_pixels:
            clear += 1
        else:
            failures.append(f"{note['note_id']}: {ink} dark source pixels inside label box")
    accuracy = clear / checked if checked else 0.0
    report = {
        "metric": (
            "candidate source-notation clearance diagnostic"
            if candidate_mode else "source-notation clearance for planned fingering labels"
        ),
        "verification_status": "diagnostic_only" if candidate_mode else "verified_only",
        "page": args.page,
        "labels": len(notes),
        "clear_labels": clear,
        "placement_accuracy": accuracy,
        "max_dark_pixels": args.max_dark_pixels,
        "failures": failures,
    }
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    return 0 if accuracy >= args.minimum and not failures else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
