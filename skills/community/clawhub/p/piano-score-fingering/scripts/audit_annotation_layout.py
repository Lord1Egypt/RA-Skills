#!/usr/bin/env python3
"""Quantify whether rendered fingering labels still belong to their note events.

This is a geometry audit for PDF/image plans.  It does not perform OMR: source
notehead anchors must already have passed the independent recognition gate.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from plan_io import finite_number, load_plan, page_map


def staff_space(plan: dict, note: dict) -> float:
    system_id = str(note.get("staff_geometry_id", ""))
    for system in plan.get("recognition", {}).get("systems", []):
        if str(system.get("system_id", "")) != system_id:
            continue
        lines = system.get("staff_line_y", [])
        if isinstance(lines, list) and len(lines) == 5:
            gaps = [abs(float(b) - float(a)) for a, b in zip(lines, lines[1:])]
            if min(gaps) > 0:
                return sum(gaps) / len(gaps)
    return max(6.0, finite_number(note.get("font_size", 10), "font_size") * 0.7)


def event_key(note: dict) -> tuple:
    return (
        int(note["page"]), str(note["part"]), int(note["measure_index"]),
        int(note["staff"]), float(note["onset"]), int(note["event_index"]),
        str(note["chord_id"]), str(note["hand"]),
    )


def label_position(note: dict, members: list[dict]) -> tuple[float, float]:
    x = finite_number(note.get("label_x", note["page_x"]), "label_x")
    offset = finite_number(note.get("label_offset", 20), "label_offset")
    stacked = len(members) > 1 and note.get("chord_label_layout", "stacked") == "stacked"
    if stacked:
        x = finite_number(note.get("chord_label_x", sum(float(item["page_x"]) for item in members) / len(members)), "chord_label_x")
        offset = finite_number(note.get("chord_label_offset", offset), "chord_label_offset")
        anchors = [finite_number(item["page_y"], "page_y") for item in members]
        row = int(note["chord_row"])
        size = finite_number(note.get("font_size", 10), "font_size")
        y = min(anchors) - offset - row * size * 1.15 if note["placement"] == "above" else max(anchors) + offset - row * size * 1.15
    else:
        y = finite_number(note["page_y"], "page_y")
        y += -offset if note["placement"] == "above" else offset
    return x, y


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("-o", "--output", type=Path, help="optional JSON audit")
    parser.add_argument("--minimum", type=float, default=0.90, help="minimum ownership accuracy (default: 0.90)")
    parser.add_argument(
        "--allow-provisional-omr", action="store_true",
        help="audit transactionally attached OMR candidate anchors without promoting them to verified score facts",
    )
    args = parser.parse_args()
    if not 0 < args.minimum <= 1:
        parser.error("--minimum must be in (0, 1]")
    plan = load_plan(args.plan)
    source_type = str(plan.get("source", {}).get("type", "")).lower()
    provisional = plan.get("recognition", {}).get("provisional_omr", {})
    provisional_ok = (
        args.allow_provisional_omr
        and source_type == "omr_candidate"
        and provisional.get("status") == "review_required"
    )
    if source_type not in {"pdf", "image"} and not provisional_ok:
        raise ValueError("layout audit is only meaningful for pdf/image plans")
    pages = page_map(plan)
    assigned = [note for note in plan["notes"] if int(note.get("finger", 0)) in {1, 2, 3, 4, 5}]
    events: dict[tuple, list[dict]] = defaultdict(list)
    for note in assigned:
        events[event_key(note)].append(note)
    event_centres: dict[tuple, float] = {
        key: sum(float(note["page_x"]) for note in members) / len(members)
        for key, members in events.items()
    }
    event_systems: dict[tuple, str] = {
        key: str(members[0].get("staff_geometry_id", ""))
        for key, members in events.items()
    }
    labels: list[tuple[dict, float, float, list[dict]]] = []
    failures: list[str] = []
    safe = 0
    for note in assigned:
        key = event_key(note)
        members = events[key]
        page = int(note["page"])
        anchor_ok = note.get("anchor_verified") is True or (
            provisional_ok and note.get("anchor_candidate") is True
        )
        if page not in pages or not anchor_ok:
            failures.append(f"{note['note_id']}: missing verified source anchor")
            continue
        x, y = label_position(note, members)
        space = staff_space(plan, note)
        own_centre = event_centres[key]
        alternatives = [
            (abs(x - centre), other)
            for other, centre in event_centres.items()
            if other[0] == page
            and other[3] == int(note["staff"])
            and event_systems.get(other, "") == str(note.get("staff_geometry_id", ""))
        ]
        nearest = min(alternatives, default=(0.0, key))[1]
        x_limit = max(space * 0.75, finite_number(note.get("font_size", 10), "font_size") * 0.55)
        is_chord = len(members) > 1 and note.get("chord_label_layout", "stacked") == "stacked"
        within_owner = abs(x - own_centre) <= x_limit if not is_chord else min(float(item["page_x"]) for item in members) - x_limit <= x <= max(float(item["page_x"]) for item in members) + x_limit
        vertical_clearance = abs(y - float(note["page_y"])) >= max(space * 0.9, finite_number(note.get("font_size", 10), "font_size") * 0.75)
        if nearest == key and within_owner and vertical_clearance:
            safe += 1
        else:
            failures.append(f"{note['note_id']}: label no longer has an unambiguous owner")
        labels.append((note, x, y, members))

    # A second label must never occupy the same printable box.  This catches
    # accidental duplicate labels even if each was initially attached to a note.
    for index, (note, x, y, _) in enumerate(labels):
        size = finite_number(note.get("font_size", 10), "font_size")
        for other, ox, oy, _ in labels[index + 1:]:
            if int(note["page"]) != int(other["page"]):
                continue
            if event_key(note) == event_key(other):
                continue
            other_size = finite_number(other.get("font_size", 10), "font_size")
            if abs(x - ox) < (size + other_size) * 0.36 and abs(y - oy) < (size + other_size) * 0.58:
                failures.append(f"{note['note_id']} and {other['note_id']}: label boxes overlap")

    accuracy = safe / len(assigned) if assigned else 0.0
    report = {
        "metric": "label-to-verified-note-event ownership",
        "labels": len(assigned),
        "unambiguous_labels": safe,
        "placement_accuracy": accuracy,
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
