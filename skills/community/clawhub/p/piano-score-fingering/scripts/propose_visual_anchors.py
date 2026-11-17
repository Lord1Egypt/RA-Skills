#!/usr/bin/env python3
"""Propose, but never verify, visual notehead anchors from semantic score facts.

This is a benchmark/review accelerator for a clean public score image that has
an independently supplied MusicXML version.  It projects events into reviewed
measure boxes, snaps each projection to nearby notehead-shaped source ink, and
writes *candidate* coordinates.  The output is intentionally a draft: every
candidate has ``anchor_verified=false`` and cannot pass visual generation
gates until an independent visual review confirms pitch, symbol class, rest
inventory, and notehead ownership.
"""

from __future__ import annotations

import argparse
import json
import math
import shutil
import sys
from collections import defaultdict
from pathlib import Path

from audit_source_noteheads import ink_signature
from plan_io import load_plan, save_plan
from render_fingering_pdf import png_pixels


STEP_INDEX = {"C": 0, "D": 1, "E": 2, "F": 3, "G": 4, "A": 5, "B": 6}
TOP_LINE = {"treble": ("F", 5), "g": ("F", 5), "bass": ("A", 3), "f": ("A", 3)}


def diatonic(step: str, octave: int) -> int:
    return octave * 7 + STEP_INDEX[step]


def load_regions(path: Path) -> tuple[dict, dict[int, tuple[dict, dict]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("review_required") is not True:
        raise ValueError("region proposal must explicitly be marked review_required")
    mapping: dict[int, tuple[dict, dict]] = {}
    for system in data.get("systems", []):
        for measure in system.get("measures", []):
            index = int(measure["measure_index"])
            if index in mapping:
                raise ValueError(f"duplicate proposed measure index {index}")
            mapping[index] = (system, measure)
    if not mapping:
        raise ValueError("no proposed measures found")
    return data, mapping


def source_rgb(path: Path) -> tuple[int, int, bytes]:
    width, height, pixels, colorspace = png_pixels(path.read_bytes())
    if colorspace != "/DeviceRGB":
        raise ValueError("source image must be RGB/RGBA PNG")
    return width, height, pixels


def expected_y(system: dict, note: dict) -> float:
    hand = str(note["hand"]).upper()
    lines = system["treble_staff_line_y"] if hand == "RH" else system["bass_staff_line_y"]
    lines = [float(value) for value in lines]
    half_space = sum(abs(right - left) for left, right in zip(lines, lines[1:])) / 8.0
    clef = str(note.get("clef", "treble" if hand == "RH" else "bass")).lower()
    top = TOP_LINE.get(clef)
    if top is None:
        raise ValueError(f"unsupported visual clef {clef!r} for {note.get('note_id', 'note')}")
    top_step, top_octave = top
    return lines[0] + (diatonic(top_step, top_octave) - diatonic(str(note["pitch_step"]), int(note["pitch_octave"]))) * half_space


def candidate_for_note(
    pixels: bytes, width: int, height: int, predicted_x: float, predicted_y: float, x_radius: int,
    y_radius: int = 1, x_bounds: tuple[float, float] | None = None,
) -> tuple[float, float, float, int, int, int]:
    """Find notehead-like source ink close to a time/pitch projection."""
    best: tuple[float, float, float, int, int, int] | None = None
    # A staff step at the supported render density is about four pixels.  A
    # ±3px scan can therefore jump to the adjacent diatonic position and
    # mistake a stem/beam for its neighbour's notehead.  Keep the pitch row
    # strict; x remains the only broad search axis.
    x_floor, x_ceiling = 0, width - 1
    if x_bounds is not None:
        x_floor = max(x_floor, math.ceil(min(x_bounds)))
        x_ceiling = min(x_ceiling, math.floor(max(x_bounds)))
    for y in range(max(0, round(predicted_y) - y_radius), min(height, round(predicted_y) + y_radius + 1)):
        for x in range(max(x_floor, round(predicted_x) - x_radius), min(x_ceiling + 1, round(predicted_x) + x_radius + 1)):
            total, widest, thick = ink_signature(pixels, width, height, x, y)
            dx, dy = abs(x - predicted_x), abs(y - predicted_y)
            # Noteheads contain several thick horizontal rows.  Projection
            # proximity breaks ties between repeated pitches in one measure.
            score = thick * 20 + total + widest * 2 - dx * 0.7 - dy * 2.0
            candidate = (score, float(x), float(y), total, widest, thick)
            if best is None or candidate[0] > best[0]:
                best = candidate
    if best is None:
        raise ValueError("empty candidate search")
    return best


def confidence(score: float, total: int, widest: int, thick: int, dx: float) -> float:
    if total < 11 or widest < 4 or thick < 2:
        return 0.0
    # Deliberately conservative: it is review priority, not verification.
    return round(max(0.0, min(0.95, 0.45 + total / 80 + thick / 20 - dx / 80)), 3)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("semantic_plan", type=Path, help="plan from create_plan_from_musicxml.py")
    parser.add_argument("regions", type=Path, help="proposed-regions.json from extract_score_regions.py")
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--max-x-search", type=int, default=28)
    parser.add_argument("--render-dpi", type=float, default=144.0, help="actual DPI used to render the supplied source PNG")
    parser.add_argument("--stage-source", action="store_true", help="copy the caller-supplied source PNG into the output directory for safe later rendering")
    args = parser.parse_args()
    if args.max_x_search < 4 or args.max_x_search > 160:
        parser.error("--max-x-search must be 4..160 pixels")
    if args.render_dpi < 36 or args.render_dpi > 600:
        parser.error("--render-dpi must be between 36 and 600")
    plan = load_plan(args.semantic_plan)
    # Key signatures were extracted from the structured semantic source.
    # Candidate coordinate staging must retain them: they remain score facts
    # to be visually checked, not expendable metadata that later makes a
    # visual plan lose its accidental context.
    semantic_key_signatures = list(plan.get("recognition", {}).get("key_signatures", []))
    region_data, region_map = load_regions(args.regions)
    source_path = Path(region_data["source_image"])
    width, height, pixels = source_rgb(source_path)
    page_image = str(source_path)
    if args.stage_source:
        staged = args.output.parent / f"source-page-{int(region_data['page'])}.png"
        if staged.exists() and staged.resolve() != source_path.resolve():
            raise ValueError(f"refusing to overwrite existing staged source {staged}")
        if not staged.exists():
            staged.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, staged)
        page_image = staged.name

    grouped: dict[tuple[int, str, str], list[dict]] = defaultdict(list)
    for note in plan["notes"]:
        measure = int(note["measure_index"])
        if measure not in region_map:
            continue
        key = (measure, str(note["hand"]).upper(), str(note["chord_id"]))
        grouped[key].append(note)
    missing_measures = sorted({int(note["measure_index"]) for note in plan["notes"]} - set(region_map))
    if missing_measures:
        raise ValueError(f"region proposal lacks semantic measures {missing_measures[:12]}")

    event_candidates: dict[str, tuple[float, float, float, int, int, int]] = {}
    geometry_ids: dict[tuple[str, str, str], str] = {}
    for (measure_index, hand, chord_id), members in grouped.items():
        if hand not in {"RH", "LH"}:
            raise ValueError(f"{chord_id}: unknown hand {hand}")
        system, measure = region_map[measure_index]
        # ``bbox`` includes review padding; use the actual barline span for
        # time projection so the extra context cannot shift event positions.
        bbox = measure.get("barline_bbox", measure["bbox"])
        measure_notes = [
            item for (candidate_measure, candidate_hand, _), notes in grouped.items()
            if candidate_measure == measure_index and candidate_hand == hand for item in notes
        ]
        # Rests occupy musical time even though they have no notehead to snap.
        # Omitting them makes every later note in a rest-containing measure
        # project too early, which can cascade into a visually plausible but
        # wrong anchor assignment.
        measure_rests = [
            rest for rest in plan.get("rests", [])
            if int(rest.get("measure_index", -1)) == measure_index
            and str(rest.get("hand", "")).upper() == hand
        ]
        timing_items = measure_notes + measure_rests
        if not timing_items:
            raise ValueError(f"measure {measure_index} {hand}: no timing facts")
        onset = float(members[0]["onset"])
        start = min(float(item["onset"]) for item in timing_items)
        final = max(
            float(item["onset"]) + max(float(item.get("duration", 0)), 0.05)
            for item in timing_items
        )
        fraction = (onset - start) / max(0.1, final - start)
        left, right = float(bbox[0]), float(bbox[2])
        # The first printed measure of *every system* normally includes a
        # repeated clef/key signature (and sometimes a time signature) before
        # its first sounding event.  Its left barline is a staff boundary, not
        # musical time-zero.  Reserving this lane only for measure 1 shifts
        # every later system's first measure onto its prefix glyphs.
        first_in_system = int(system["measures"][0]["measure_index"])
        if measure_index == first_in_system:
            lead = min((right - left) * 0.42, 112.0)
            left += lead
        else:
            left += min((right - left) * 0.06, 16.0)
        right -= min((right - left) * 0.06, 16.0)
        predicted_x = left + (right - left) * fraction
        # A chord has one horizontal event.  Use its middle pitch only for
        # choosing x; each individual member is snapped vertically below.
        centre_member = sorted(members, key=lambda item: int(item["pitch_midi"]))[len(members) // 2]
        y = expected_y(system, centre_member)
        event_candidates[chord_id] = candidate_for_note(
            pixels, width, height, predicted_x, y, args.max_x_search,
            x_bounds=(float(bbox[0]), float(bbox[2])),
        )

    for note in plan["notes"]:
        chord_id = str(note["chord_id"])
        score, candidate_x, _, total, widest, thick = event_candidates[chord_id]
        system, measure = region_map[int(note["measure_index"])]
        system_id = str(system["system_id"])
        hand = str(note["hand"]).upper()
        clef = str(note.get("clef", "treble" if hand == "RH" else "bass")).lower()
        geometry_ids[(system_id, hand, clef)] = f"{system_id}-{hand}-{clef}"
        y = expected_y(system, note)
        lines = system["treble_staff_line_y"] if hand == "RH" else system["bass_staff_line_y"]
        spacing = sum(abs(float(b) - float(a)) for a, b in zip(lines, lines[1:])) / 4.0
        # Ledger-line notes are visibly displaced by stroke thickness and must
        # receive a bounded extra vertical search.  Ordinary staff notes stay
        # on the strict ±1px pitch row to prevent neighbour-note swaps.
        ledger = y < min(lines) - spacing or y > max(lines) + spacing
        _, snapped_x, snapped_y, note_total, note_widest, note_thick = candidate_for_note(
            pixels, width, height, candidate_x, y, max(5, args.max_x_search // 5),
            y_radius=8 if ledger else 1,
            x_bounds=(
                float(measure.get("barline_bbox", measure["bbox"])[0]),
                float(measure.get("barline_bbox", measure["bbox"])[2]),
            ),
        )
        level = confidence(score, note_total, note_widest, note_thick, abs(snapped_x - candidate_x))
        note["page"] = int(region_data["page"])
        note["page_x"] = round(snapped_x, 2)
        note["page_y"] = round(snapped_y, 2)
        note["anchor_candidate"] = True
        note["anchor_verified"] = False
        note["anchor_method"] = "candidate_visual_ink"
        note["origin"] = "candidate_visual_notehead"
        note["staff_geometry_id"] = geometry_ids[(system_id, hand, clef)]
        note["pitch_geometry_verified"] = False
        note["candidate_confidence"] = level

    # Rests have no pitch row and are intentionally not snapped by the
    # notehead finder.  Keep their page/measure identity so a later manual
    # review must supply an actual glyph centre instead of silently dropping
    # them from a visual task.
    for rest in plan.get("rests", []):
        measure_index = int(rest["measure_index"])
        if measure_index not in region_map:
            raise ValueError(f"rest {rest.get('rest_id', 'unknown')}: region proposal lacks measure {measure_index}")
        system, _ = region_map[measure_index]
        hand = str(rest.get("hand", "")).upper()
        if hand not in {"RH", "LH"}:
            raise ValueError(f"rest {rest.get('rest_id', 'unknown')}: unknown hand {hand!r}")
        rest["page"] = int(region_data["page"])
        clef = str(rest.get("clef", "treble" if hand == "RH" else "bass")).lower()
        rest["staff_geometry_id"] = f"{system['system_id']}-{hand}-{clef}"
        rest["rest_candidate"] = True
        rest["rest_shape_verified"] = False

    # A time projection must not snap two distinct sequential events in the
    # same hand/measure onto one x-coordinate.  Such candidates often arise
    # from a stem or a nearby repeated pitch.  Keep them visible for review,
    # but mark both as low confidence rather than silently advancing.
    event_groups: dict[tuple[int, str, str], list[dict]] = defaultdict(list)
    for note in plan["notes"]:
        event_groups[(int(note["measure_index"]), str(note["hand"]).upper(), str(note["chord_id"]))].append(note)
    streams: dict[tuple[int, str], list[list[dict]]] = defaultdict(list)
    for (measure, hand, _), members in event_groups.items():
        streams[(measure, hand)].append(members)
    for (_, _), events in streams.items():
        events.sort(key=lambda members: float(members[0]["onset"]))
        for previous, current in zip(events, events[1:]):
            if float(current[0]["page_x"]) > float(previous[0]["page_x"]) + 2.0:
                continue
            # A repeated pitch can make both projections snap to the first
            # notehead.  Before declaring the pair ambiguous, retry the later
            # event to the right of the earlier *verified candidate*.  The
            # search remains bounded by the current measure's barlines, so it
            # cannot drift into a neighbouring bar or hand.
            measure_index = int(current[0]["measure_index"])
            _, measure = region_map[measure_index]
            right_bound = float(measure.get("barline_bbox", measure["bbox"])[2])
            # A printed notehead is roughly 8–10 px wide at the canonical
            # 144-dpi benchmark scale.  Move past that footprint rather than
            # merely to a different dark pixel in the same oval.
            floor = float(previous[0]["page_x"]) + 11.0
            if floor < right_bound - 2.0:
                for note in current:
                    system, _ = region_map[int(note["measure_index"])]
                    y = expected_y(system, note)
                    _, snapped_x, snapped_y, total, widest, thick = candidate_for_note(
                        pixels, width, height, float(note["page_x"]), y,
                        max(24, args.max_x_search),
                        y_radius=8 if (y < min((system["treble_staff_line_y"] if str(note["hand"]).upper() == "RH" else system["bass_staff_line_y"])) - 10 or y > max((system["treble_staff_line_y"] if str(note["hand"]).upper() == "RH" else system["bass_staff_line_y"])) + 10) else 1,
                        x_bounds=(floor, right_bound),
                    )
                    note["page_x"] = round(snapped_x, 2)
                    note["page_y"] = round(snapped_y, 2)
                    note["candidate_confidence"] = confidence(0.0, total, widest, thick, abs(snapped_x - float(note["page_x"])))
            if float(current[0]["page_x"]) > float(previous[0]["page_x"]) + 2.0:
                continue
            for note in previous + current:
                note["candidate_confidence"] = 0.0
                note["candidate_warning"] = "sequential events snapped to one/non-monotonic source x; verify crop manually"
    low_confidence = [str(note["note_id"]) for note in plan["notes"] if float(note["candidate_confidence"]) < 0.75]

    plan["source"] = {
        "type": "image", "coordinate_unit": "pixel_top_left", "path": str(source_path),
        "semantic_reference": str(args.semantic_plan), "render_dpi": args.render_dpi,
    }
    plan["pages"] = [{"page": int(region_data["page"]), "width": width, "height": height, "image": page_image}]
    systems: list[dict] = []
    systems_by_id = {str(system["system_id"]): system for system in region_data["systems"]}
    for (system_id, hand, clef), geometry_id in sorted(geometry_ids.items()):
        system = systems_by_id[system_id]
        lines = system["treble_staff_line_y"] if hand == "RH" else system["bass_staff_line_y"]
        systems.append({
            "system_id": geometry_id, "staff_line_y": lines, "clef": clef,
            "candidate_geometry": True,
        })
    measure_regions: list[dict] = []
    # A bounded MusicXML task (for example --measure-range 49-52) must not
    # inherit unreviewable empty regions from the full-page crop proposal.
    # Only score facts actually present in this semantic plan define the
    # recognition scope that later needs evidence and a fact lock.
    measure_indexes = sorted({
        int(item["measure_index"])
        for item in plan["notes"] + plan.get("rests", [])
    })
    for measure_index in measure_indexes:
        _, measure = region_map[measure_index]
        for hand in ("RH", "LH"):
            region = measure.get(hand)
            if not isinstance(region, dict):
                raise ValueError(f"measure {measure_index}: missing {hand} evidence crop")
            # A notehead centre can sit one or two pixels outside a tight
            # staff-band crop while its visible ink is still in that crop.
            # Preserve a small, bounded guard so a valid boundary note is not
            # reported as belonging to the adjacent hand/measure.
            x0, y0, x1, y1 = [float(value) for value in region["bbox"]]
            mx0, my0, mx1, my1 = [float(value) for value in measure["bbox"]]
            guard = 3.0
            measure_regions.append({
                "region_id": f"p{int(region_data['page'])}-m{measure_index:03d}-{hand.lower()}",
                "page": int(region_data["page"]),
                "measure": measure_index,
                "hand": hand,
                "bbox": [max(mx0, x0 - guard), max(my0, y0 - guard), min(mx1, x1 + guard), min(my1, y1 + guard)],
                "evidence_crop": str(region["evidence_crop"]),
            })
    plan["recognition"] = {
        "status": "draft",
        "scope": "candidate anchors require independent visual verification before fingering",
        "expected_note_count": len(plan["notes"]), "unresolved_note_count": 0,
        "delivery_level": "partial", "candidate_anchor_count": len(plan["notes"]),
        "low_confidence_candidates": low_confidence,
        "key_signatures": semantic_key_signatures,
        "systems": systems,
        "measure_scope": [{
            "page": int(region_data["page"]), "measure_start": measure_indexes[0],
            "measure_end": measure_indexes[-1], "hands": ["RH", "LH"],
        }],
        "measure_regions": measure_regions,
    }
    # Candidate coordinates are deliberately not fact-locked.
    plan.pop("fact_lock", None)
    save_plan(args.output, plan)
    report = {
        "notes": len(plan["notes"]),
        "rests": len(plan.get("rests", [])),
        "low_confidence": len(low_confidence),
        "vertical_search_px": 1,
        "output": str(args.output),
        "review_required": True,
    }
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
