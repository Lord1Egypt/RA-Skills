#!/usr/bin/env python3
"""Check that every verified visual anchor still lands on source notation ink.

The check is deliberately modest: it is not an OMR replacement and cannot
infer pitch or distinguish a rest by itself.  It catches a costly failure mode
before PDF rendering: a claimed notehead coordinate that has drifted onto a
staff line, a stem, or blank space.  Use it together with
``validate_recognition.py`` (semantic/visual facts) and
``audit_source_clearance.py`` (label-to-source clearance).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from audit_source_clearance import source_image
from plan_io import finite_number, load_plan, page_map
from render_fingering_pdf import png_pixels


def dark(red: int, green: int, blue: int) -> bool:
    return max(red, green, blue) < 150 and max(red, green, blue) - min(red, green, blue) < 22


def ink_signature(pixels: bytes, width: int, height: int, x: int, y: int) -> tuple[int, int, int]:
    """Return total ink, widest row, and number of thick rows near an anchor.

    A vertical stem can be dark but is one pixel wide.  A notehead normally
    has several horizontally thick rows.  This tiny shape test therefore
    catches more coordinate drift than a black-pixel total alone.
    """
    total = 0
    widest_row = 0
    thick_rows = 0
    for yy in range(max(0, y - 3), min(height, y + 4)):
        row_total = 0
        for xx in range(max(0, x - 4), min(width, x + 5)):
            start = (yy * width + xx) * 3
            if dark(*pixels[start:start + 3]):
                total += 1
                row_total += 1
        widest_row = max(widest_row, row_total)
        if row_total >= 3:
            thick_rows += 1
    return total, widest_row, thick_rows


def best_nearby_ink(
    pixels: bytes, width: int, height: int, anchor_x: float, anchor_y: float, radius: int,
) -> tuple[int, int, int, int, int]:
    """Return the strongest local notehead-shaped ink and its centre."""
    x0, y0 = round(anchor_x), round(anchor_y)
    best = (-1, -1, -1, x0, y0)
    for y in range(y0 - radius, y0 + radius + 1):
        for x in range(x0 - radius, x0 + radius + 1):
            density, widest_row, thick_rows = ink_signature(pixels, width, height, x, y)
            if (thick_rows, density, widest_row) > best[:3]:
                best = (thick_rows, density, widest_row, x, y)
    return best


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--minimum", type=float, default=0.90)
    parser.add_argument("--maximum-drift", type=float, default=4.0, help="maximum drift in 144-DPI-equivalent pixels")
    parser.add_argument("--minimum-ink", type=int, default=11, help="minimum dark pixels in a 9x7 notehead window")
    parser.add_argument(
        "--candidate-diagnostic", action="store_true",
        help="measure draft-anchor geometry without treating candidates as verified evidence",
    )
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    if not 0 < args.minimum <= 1 or args.maximum_drift < 0 or args.minimum_ink < 1:
        raise ValueError("invalid minimum, maximum-drift, or minimum-ink")
    plan = load_plan(args.plan)
    source_type = str(plan.get("source", {}).get("type", "")).lower()
    if source_type not in {"pdf", "image"} and not (
        args.candidate_diagnostic and source_type == "omr_candidate"
    ):
        raise ValueError("source-notehead audit is only meaningful for pdf/image plans")
    page = page_map(plan).get(args.page)
    if page is None:
        raise ValueError(f"page {args.page} is not declared by the plan")
    width, height, pixels, colorspace = png_pixels(source_image(args.plan, page).read_bytes())
    if colorspace != "/DeviceRGB":
        raise ValueError("source PNG must be RGB/RGBA")
    sx = width / finite_number(page["width"], "page.width")
    sy = height / finite_number(page["height"], "page.height")
    if abs(sx - sy) > 0.03 * max(sx, sy):
        raise ValueError("source image aspect ratio conflicts with plan page")
    source_dpi = finite_number(plan.get("source", {}).get("render_dpi", 144), "source.render_dpi")
    if not 36 <= source_dpi <= 600:
        raise ValueError("source.render_dpi must be between 36 and 600")
    drift_scale = source_dpi / 144.0
    maximum_drift_px = args.maximum_drift * drift_scale

    notes = [note for note in plan["notes"] if int(note.get("page", 0)) == args.page]
    if args.candidate_diagnostic:
        # The provisional PDF prints only assigned, transactionally attached
        # labels.  Hidden/unattached OMR notes belong in coverage, not in the
        # placement denominator for labels the user can actually see.
        notes = [note for note in notes if int(note.get("finger", 0) or 0) in {1, 2, 3, 4, 5}]
    checked = passed = 0
    failures: list[str] = []
    for note in notes:
        note_id = str(note.get("note_id", "unknown"))
        candidate = note.get("anchor_candidate") is True
        if note.get("anchor_verified") is not True and not (args.candidate_diagnostic and candidate):
            failures.append(f"{note_id}: source anchor is not verified")
            continue
        try:
            x = finite_number(note["page_x"], f"{note_id}.page_x") * sx
            y = finite_number(note["page_y"], f"{note_id}.page_y") * sy
        except (KeyError, ValueError) as exc:
            failures.append(f"{note_id}: invalid anchor ({exc})")
            continue
        thick_rows, density, widest_row, best_x, best_y = best_nearby_ink(pixels, width, height, x, y, radius=3)
        drift = ((best_x - x) ** 2 + (best_y - y) ** 2) ** 0.5
        checked += 1
        manual_review = note.get("anchor_method") == "manual_visual_anchor_review"
        # A manually reviewed chord member may be visibly compressed against a
        # stem/ledger line at low DPI.  Its separate review already proves the
        # symbol class; retain a source-ink proximity check without forcing it
        # through the stricter automatic notehead-shape discriminator.
        min_widest = 3 if manual_review else 4
        max_drift = maximum_drift_px + drift_scale if manual_review else maximum_drift_px
        if density >= args.minimum_ink and widest_row >= min_widest and thick_rows >= 2 and drift <= max_drift:
            passed += 1
        else:
            failures.append(
                f"{note_id}: best local ink {density} (widest row {widest_row}, thick rows {thick_rows}) "
                f"at ({best_x}, {best_y}), drift {drift:.2f}px "
                f"(need ink ≥{args.minimum_ink}, widest row ≥{min_widest}, thick rows ≥2, drift ≤{max_drift:g}px)"
            )
    accuracy = passed / checked if checked else 0.0
    report = {
        "metric": "candidate-anchor geometry diagnostic" if args.candidate_diagnostic else "verified-anchor source-ink proximity",
        "verification_status": "diagnostic_only" if args.candidate_diagnostic else "verified_only",
        "page": args.page,
        "anchors": len(notes),
        "valid_anchors": passed,
        "placement_accuracy": accuracy,
        "minimum_ink": args.minimum_ink,
        "maximum_drift_144dpi": args.maximum_drift,
        "source_render_dpi": source_dpi,
        "maximum_drift_pixels": maximum_drift_px,
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
    except (OSError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
