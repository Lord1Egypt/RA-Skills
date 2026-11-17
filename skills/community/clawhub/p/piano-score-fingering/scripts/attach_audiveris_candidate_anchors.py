#!/usr/bin/env python3
"""Attach review-only Audiveris coordinates to a candidate MusicXML plan.

The input plan remains ``omr_candidate`` and cannot pass recognition merely
because its noteheads have page coordinates.  This helper only pairs events
within page/measure/hand groups whose OMR and MXL counts already agree, then
marks every result ``anchor_candidate=true`` for raw-page review.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from plan_io import load_plan, save_plan


def page_offsets(data: dict) -> list[tuple[int, int, int]]:
    """Return page-to-global-measure ranges without guessing through rests.

    New extractor output declares every page's OMR measure count.  Older
    candidate JSON may omit it; its `measure_consistency` table is also an
    authoritative page span.  A multi-page legacy payload with neither
    record is unsafe because a silent trailing measure is invisible in a
    notehead list, so refuse it instead of shifting later-page anchors.
    """
    rows: list[tuple[int, int, int]] = []
    first = 1
    pages = sorted(data.get("pages", []), key=lambda row: int(row["page"]))
    audited_counts: dict[int, int] = {}
    for entry in data.get("measure_consistency", []):
        if not isinstance(entry, dict):
            continue
        try:
            page = int(entry["page"])
            audited_counts[page] = max(audited_counts.get(page, 0), int(entry["measure"]))
        except (KeyError, TypeError, ValueError):
            continue
    for index, page in enumerate(pages):
        try:
            declared = int(page.get("measure_count", 0))
        except (TypeError, ValueError):
            declared = 0
        count = declared or audited_counts.get(int(page["page"]), 0)
        if not count and len(pages) == 1:
            # A legacy one-page payload may still assist review of the
            # visible measures.  There is no subsequent page to misalign.
            count = max((int(head.get("local_measure", 0)) for head in page.get("candidate_noteheads", []) if isinstance(head, dict)), default=0)
        if not count and index < len(pages) - 1:
            raise ValueError(
                "multi-page candidate anchors lack per-page measure counts; "
                "regenerate them with extract_audiveris_anchor_candidates.py"
            )
        if count:
            rows.append((int(page["page"]), first, first + count - 1))
            first += count
    if not rows:
        raise ValueError("candidate anchors have no scoped measures")
    return rows


def scope_for_measure(measure: int, offsets: list[tuple[int, int, int]]) -> tuple[int, int]:
    for page, first, last in offsets:
        if first <= measure <= last:
            return page, measure - first + 1
    raise ValueError(f"candidate anchors have no page scope for MusicXML measure {measure}")


def x_clusters(heads: list[dict], tolerance: float) -> list[list[dict]]:
    """Group candidate heads into simultaneous visual events conservatively.

    Sorting and slicing by chord size lets one spurious/missing head shift all
    later labels in a measure.  Only a clear horizontal event topology may be
    used as a review aid; close-but-ambiguous heads deliberately block a
    whole page/measure/hand scope instead.
    """
    clusters: list[list[dict]] = []
    for head in sorted(heads, key=lambda item: (float(item["page_x"]), float(item["page_y"]))):
        if not clusters or float(head["page_x"]) - float(clusters[-1][-1]["page_x"]) > tolerance:
            clusters.append([head])
        else:
            clusters[-1].append(head)
    return clusters


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="omr_candidate plan from create_plan_from_musicxml.py")
    parser.add_argument("anchors", type=Path, help="candidate-anchor JSON from extract_audiveris_anchor_candidates.py")
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--max-chord-x-spread", type=float, default=18.0)
    parser.add_argument("--event-x-tolerance", type=float, default=6.0,
                        help="maximum x separation for heads to count as one visual event")
    parser.add_argument("--page", type=int, action="append",
                        help="attach only this rendered original page; repeat for several pages")
    args = parser.parse_args()
    if args.max_chord_x_spread <= 0 or args.event_x_tolerance <= 0:
        parser.error("--max-chord-x-spread and --event-x-tolerance must be positive")
    plan = load_plan(args.plan)
    if str(plan.get("source", {}).get("type", "")) != "omr_candidate":
        raise ValueError("plan must retain source.type=omr_candidate")
    data = json.loads(args.anchors.read_text(encoding="utf-8"))
    if data.get("candidate_only") is not True:
        raise ValueError("candidate anchors must be explicitly candidate-only")
    offsets = page_offsets(data)
    selected_pages = set(args.page or [int(row["page"]) for row in data.get("pages", []) if row.get("target_image")])
    if not selected_pages:
        raise ValueError("no rendered original target page was selected")
    declared_mismatches = {
        (int(row["page"]), int(row["measure"]), str(row["hand"]).upper())
        for row in data.get("mismatched_measure_scopes", []) if isinstance(row, dict)
    }
    by_scope_heads: dict[tuple[int, int, str], list[dict]] = defaultdict(list)
    pages = {int(page["page"]): page for page in data.get("pages", [])}
    for page in data.get("pages", []):
        for head in page.get("candidate_noteheads", []):
            if not isinstance(head, dict) or int(page["page"]) not in selected_pages or not {"page_x", "page_y", "local_measure", "hand"} <= set(head):
                continue
            by_scope_heads[(int(page["page"]), int(head["local_measure"]), str(head["hand"]).upper())].append(head)

    by_scope_events: dict[tuple[int, int, str], list[list[dict]]] = defaultdict(list)
    groups: dict[tuple[int, str, str], list[dict]] = defaultdict(list)
    for note in plan.get("notes", []):
        measure = int(note["measure_index"])
        page, local_measure = scope_for_measure(measure, offsets)
        if page not in selected_pages:
            continue
        hand = str(note["hand"]).upper()
        groups[(measure, hand, str(note["chord_id"]))].append(note)
        note["page"] = page
    for (measure, hand, _chord), members in groups.items():
        page, local_measure = scope_for_measure(measure, offsets)
        by_scope_events[(page, local_measure, hand)].append(members)

    attached = 0
    blocked: list[dict] = []
    for scope, events in by_scope_events.items():
        if scope in declared_mismatches:
            blocked.append({"page": scope[0], "measure": scope[1], "hand": scope[2], "reason": "OMR/MXL count mismatch"})
            continue
        heads = by_scope_heads.get(scope, [])
        event_notes = sum(len(event) for event in events)
        if len(heads) != event_notes:
            blocked.append({"page": scope[0], "measure": scope[1], "hand": scope[2], "reason": f"plan has {event_notes} notes; geometry has {len(heads)} heads"})
            continue
        events.sort(key=lambda members: (float(members[0]["onset"]), str(members[0]["chord_id"])))
        head_events = x_clusters(heads, args.event_x_tolerance)
        expected_shape = [len(members) for members in events]
        actual_shape = [len(members) for members in head_events]
        if expected_shape != actual_shape:
            blocked.append({
                "page": scope[0], "measure": scope[1], "hand": scope[2],
                "reason": f"event x-cluster topology differs (plan {expected_shape}; geometry {actual_shape})",
            })
            continue
        assignments: list[tuple[dict, dict]] = []
        scope_failed = False
        for members, chunk in zip(events, head_events):
            count = len(members)
            spread = max(float(head["page_x"]) for head in chunk) - min(float(head["page_x"]) for head in chunk)
            if count > 1 and spread > args.max_chord_x_spread:
                blocked.append({"page": scope[0], "measure": scope[1], "hand": scope[2], "reason": f"candidate chord x spread {spread:.1f}"})
                scope_failed = True
                break
            members.sort(key=lambda note: int(note["pitch_midi"]))
            chunk.sort(key=lambda head: float(head["page_y"]), reverse=True)  # lower pitch is lower on page
            for note, head in zip(members, chunk):
                assignments.append((note, head))
        if scope_failed:
            continue
        for note, head in assignments:
            note.update({
                "page_x": float(head["page_x"]), "page_y": float(head["page_y"]),
                "anchor_candidate": True, "anchor_verified": False,
                "pitch_geometry_verified": False, "anchor_method": "audiveris_candidate_geometry",
                "origin": "candidate_visual_notehead", "candidate_confidence": float(head.get("context_grade", head.get("grade", 0))),
            })
            attached += 1
    if not attached:
        raise ValueError("no selected page/measure-hand scope had attachable candidate geometry")
    for page, row in pages.items():
        target = row.get("target_image")
        if target and page in selected_pages:
            plan.setdefault("pages", []).append({"page": page, "width": row["target_width"], "height": row["target_height"], "image": target})
    recognition = plan.setdefault("recognition", {})
    recognition["status"] = "review"
    recognition["candidate_anchor_review"] = {
        "source": str(args.anchors.resolve()), "attached_notes": attached,
        "blocked_scopes": blocked,
        "warning": "Every attached coordinate is candidate-only and requires raw-page review.",
    }
    recognition.pop("fact_lock", None)
    save_plan(args.output, plan)
    print(json.dumps({"attached_notes": attached, "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: {exc}")
