#!/usr/bin/env python3
"""Move fingering labels vertically until they clear source-score ink.

This is intentionally conservative: it never changes note anchors, fingers,
or chord ordering.  It first tries a tiny horizontal label nudge (still subject
to the normal ownership audit), then increases the existing vertical offset.
Run the normal layout, source-clearance, and rendered-output audits after it.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from collections import defaultdict
from pathlib import Path

from audit_annotation_layout import event_key, label_position, staff_space
from audit_source_clearance import dark_pixels, label_box, source_image
from plan_io import finite_number, load_plan, page_map, save_plan
from render_fingering_pdf import png_pixels


def event_ink(note: dict, members: list[dict], pixels: bytes, width: int, height: int, sx: float, sy: float, dpi: float) -> int | None:
    total = 0
    for member in members:
        x0, y0, x1, y1 = label_box(member, members, sx, sy, dpi)
        # Labels which would leave the page are never viable candidates.
        if x0 < 0 or y0 < 0 or x1 >= width or y1 >= height:
            return None
        total += dark_pixels(pixels, width, height, x0, y0, x1 + 1, y1 + 1)
    return total


def apply_offset(members: list[dict], offset: float) -> None:
    stacked = len(members) > 1 and members[0].get("chord_label_layout", "stacked") == "stacked"
    for note in members:
        if stacked:
            note["chord_label_offset"] = offset
        else:
            note["label_offset"] = offset


def current_offset(members: list[dict]) -> float:
    stacked = len(members) > 1 and members[0].get("chord_label_layout", "stacked") == "stacked"
    field = "chord_label_offset" if stacked else "label_offset"
    return finite_number(members[0].get(field, members[0].get("label_offset", 20)), field)


def current_x(members: list[dict]) -> float:
    stacked = len(members) > 1 and members[0].get("chord_label_layout", "stacked") == "stacked"
    field = "chord_label_x" if stacked else "label_x"
    fallback = sum(float(note["page_x"]) for note in members) / len(members) if stacked else float(members[0]["page_x"])
    return finite_number(members[0].get(field, fallback), field)


def apply_x(members: list[dict], x: float) -> None:
    stacked = len(members) > 1 and members[0].get("chord_label_layout", "stacked") == "stacked"
    field = "chord_label_x" if stacked else "label_x"
    for note in members:
        note[field] = x


def labels_overlap(members: list[dict], occupied: list[tuple[dict, float, float, float, tuple]]) -> bool:
    """Return true when a candidate label would cover an earlier event label."""
    key = event_key(members[0])
    for note in members:
        x, y = label_position(note, members)
        size = finite_number(note.get("font_size", 10), "font_size")
        for other, ox, oy, other_size, other_key in occupied:
            if other_key == key or int(other["page"]) != int(note["page"]):
                continue
            if abs(x - ox) < (size + other_size) * 0.36 and abs(y - oy) < (size + other_size) * 0.58:
                return True
    return False


def occupy(members: list[dict], occupied: list[tuple[dict, float, float, float, tuple]]) -> None:
    key = event_key(members[0])
    for note in members:
        x, y = label_position(note, members)
        occupied.append((note, x, y, finite_number(note.get("font_size", 10), "font_size"), key))


def ownership_safe(
    plan: dict,
    members: list[dict],
    x: float,
    event_centres: dict[tuple, float],
    event_systems: dict[tuple, str],
) -> bool:
    """Keep every horizontal nudge inside the event's ownership cell."""
    note = members[0]
    key = event_key(note)
    page = int(note["page"])
    staff = int(note["staff"])
    system = str(note.get("staff_geometry_id", ""))
    alternatives = [
        (abs(x - centre), other)
        for other, centre in event_centres.items()
        if other[0] == page and other[3] == staff and event_systems.get(other, "") == system
    ]
    if min(alternatives, default=(0.0, key))[1] != key:
        return False
    size = finite_number(note.get("font_size", 10), "font_size")
    x_limit = max(staff_space(plan, note) * 0.75, size * 0.55)
    if len(members) > 1 and note.get("chord_label_layout", "stacked") == "stacked":
        left = min(float(item["page_x"]) for item in members) - x_limit
        right = max(float(item["page_x"]) for item in members) + x_limit
        return left <= x <= right
    return abs(x - event_centres[key]) <= x_limit


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--dpi", type=float, required=True, help="DPI used to render pages[].image")
    parser.add_argument("--step", type=float, default=6.0)
    parser.add_argument("--max-extra-offset", type=float, default=48.0)
    parser.add_argument("--max-horizontal-shift", type=float, default=5.0, help="small label-only x nudge; ownership audit remains mandatory")
    parser.add_argument("--max-dark-pixels", type=int, default=4)
    parser.add_argument("--report", type=Path)
    parser.add_argument(
        "--allow-provisional-omr",
        action="store_true",
        help="permit a diagnostic-only OMR candidate; it remains review-required",
    )
    parser.add_argument(
        "--hide-unresolved",
        action="store_true",
        help="remove labels that cannot be moved clear of source ink instead of rendering them overlapped",
    )
    args = parser.parse_args()
    if (
        args.dpi < 36 or args.dpi > 600 or args.step <= 0 or args.max_extra_offset < 0
        or args.max_horizontal_shift < 0 or args.max_dark_pixels < 0
    ):
        raise ValueError("invalid dpi, step, offset, horizontal shift, or max-dark-pixels")

    plan = load_plan(args.input)
    source_type = str(plan.get("source", {}).get("type", "")).lower()
    provisional = plan.get("recognition", {}).get("provisional_omr", {})
    if source_type not in {"pdf", "image"} and not (
        args.allow_provisional_omr
        and source_type == "omr_candidate"
        and provisional.get("status") == "review_required"
    ):
        raise ValueError("label clearance repair is only meaningful for pdf/image plans or explicit provisional OMR output")
    pages = page_map(plan)
    page_pixels: dict[int, tuple[int, int, bytes, float, float]] = {}
    for page_number, page in pages.items():
        width, height, pixels, colorspace = png_pixels(source_image(args.input, page).read_bytes())
        if colorspace != "/DeviceRGB":
            raise ValueError(f"page {page_number}: source PNG must be RGB/RGBA")
        sx = width / finite_number(page["width"], "page.width")
        sy = height / finite_number(page["height"], "page.height")
        if abs(sx - sy) > 0.03 * max(sx, sy):
            raise ValueError(f"page {page_number}: source image aspect ratio conflicts with plan")
        page_pixels[page_number] = (width, height, pixels, sx, sy)

    events: dict[tuple, list[dict]] = defaultdict(list)
    for note in plan["notes"]:
        if int(note.get("finger", 0)) in {1, 2, 3, 4, 5}:
            events[event_key(note)].append(note)
    event_centres = {
        key: sum(float(note["page_x"]) for note in members) / len(members)
        for key, members in events.items()
    }
    event_systems = {
        key: str(members[0].get("staff_geometry_id", ""))
        for key, members in events.items()
    }
    repaired: list[dict] = []
    unresolved: list[str] = []
    steps = int(args.max_extra_offset // args.step)
    occupied: list[tuple[dict, float, float, float, tuple]] = []
    for key, members in events.items():
        anchors_ok = all(note.get("anchor_verified") is True for note in members)
        provisional_ok = args.allow_provisional_omr and all(note.get("anchor_candidate") is True for note in members)
        if not anchors_ok and not provisional_ok:
            unresolved.append(f"{members[0]['note_id']}: unverified anchor")
            continue
        page_number = int(members[0]["page"])
        width, height, pixels, sx, sy = page_pixels[page_number]
        before = current_offset(members)
        before_x = current_x(members)
        baseline = event_ink(members[0], members, pixels, width, height, sx, sy, args.dpi)
        if (
            baseline is not None and baseline <= args.max_dark_pixels
            and ownership_safe(plan, members, before_x, event_centres, event_systems)
            and not labels_overlap(members, occupied)
        ):
            occupy(members, occupied)
            continue
        snapshot = copy.deepcopy(members)
        chosen = None
        horizontal = [0.0]
        if args.max_horizontal_shift:
            horizontal.extend((-args.max_horizontal_shift, args.max_horizontal_shift))
        for offset_index in range(0, steps + 1):
            candidate = before + offset_index * args.step
            for dx in horizontal:
                apply_offset(members, candidate)
                apply_x(members, before_x + dx)
                if not ownership_safe(plan, members, before_x + dx, event_centres, event_systems):
                    continue
                ink = event_ink(members[0], members, pixels, width, height, sx, sy, args.dpi)
                if ink is not None and ink <= args.max_dark_pixels and not labels_overlap(members, occupied):
                    chosen = (candidate, before_x + dx, ink)
                    break
            if chosen is not None:
                break
        if chosen is None:
            for original, note in zip(snapshot, members):
                note.clear(); note.update(original)
            if args.hide_unresolved:
                for note in members:
                    note["finger"] = 0
                    note["provisional_label"] = False
                unresolved.append(f"{members[0]['note_id']}: withheld after no clear vertical offset within +{args.max_extra_offset:g}")
                continue
            unresolved.append(f"{members[0]['note_id']}: no clear vertical offset within +{args.max_extra_offset:g}")
        else:
            repaired.append({
                "event": str(key), "offset_from": before, "offset_to": chosen[0],
                "label_x_from": before_x, "label_x_to": chosen[1], "dark_pixels": chosen[2],
            })
            occupy(members, occupied)
    if args.allow_provisional_omr and isinstance(provisional, dict):
        provisional["labelled_noteheads"] = sum(
            1 for note in plan.get("notes", []) if int(note.get("finger", 0) or 0) in {1, 2, 3, 4, 5}
        )
        provisional["unlabelled_notes"] = sum(
            1 for note in plan.get("notes", []) if int(note.get("finger", 0) or 0) not in {1, 2, 3, 4, 5}
        )
    save_plan(args.output, plan)
    report = {"repaired_events": repaired, "unresolved_events": unresolved}
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(payload + "\n", encoding="utf-8")
    return 0 if not unresolved else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
