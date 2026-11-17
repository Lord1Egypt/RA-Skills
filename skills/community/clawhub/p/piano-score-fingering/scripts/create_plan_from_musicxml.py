#!/usr/bin/env python3
"""Create a unified fingering plan from MusicXML using only the standard library."""

from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from itertools import groupby
from pathlib import Path

from fingering_core.models import INote, keypos_midi
from plan_io import save_plan
from recognition_state import set_fact_lock
from source_provenance import structured_asset_record
from safe_xml import load_musicxml
from musicxml_parts import hand_for_part_staff, select_piano_parts


STEP_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
TIME_PRECISION = 8
SHARP_ORDER = ("F", "C", "G", "D", "A", "E", "B")
FLAT_ORDER = tuple(reversed(SHARP_ORDER))


def omr_candidate_context(source: Path) -> dict | None:
    """Identify an MXL emitted beside this Skill's OMR candidate receipt.

    A generated MusicXML looks structurally complete to the generic importer,
    but it is not an authoritative source: OMR can have already reported a
    missing rest, a rhythm conflict, or an unlinked symbol.  Match the exact
    candidate path recorded in the receipt so only that output is demoted;
    ordinary user-provided MusicXML keeps its normal structured-source path.
    """
    receipt = source.parent / "omr-candidate-report.json"
    if not receipt.is_file():
        return None
    try:
        payload = json.loads(receipt.read_text(encoding="utf-8"))
        candidates = payload.get("musicxml_candidates", [])
        source_path = source.resolve()
        matched = any(Path(str(item)).expanduser().resolve() == source_path for item in candidates)
    except (OSError, ValueError, TypeError):
        return None
    if not matched:
        return None
    return {
        "report": str(receipt.resolve()),
        "engine": str(payload.get("candidate", "local_omr")),
        "status": str(payload.get("status", "unknown")),
        "risk_count": len(payload.get("semantic_risk_signals", []) or []),
    }


def key_signature_alter(fifths: int, step: str) -> int:
    """Return the default alteration for a written step in a key signature."""
    if fifths > 0:
        return 1 if step in SHARP_ORDER[:fifths] else 0
    if fifths < 0:
        return -1 if step in FLAT_ORDER[:(-fifths)] else 0
    return 0


def read_key(element: ET.Element) -> tuple[int, str] | None:
    raw_fifths = text(element, "fifths", "")
    if not raw_fifths:
        return None
    fifths = int(raw_fifths)
    if not -7 <= fifths <= 7:
        raise ValueError(f"unsupported key signature fifths={fifths}")
    return fifths, text(element, "mode", "unspecified").lower() or "unspecified"


def parse_measure_range(value: str) -> tuple[int, int]:
    try:
        parts = [int(item) for item in value.split("-", 1)]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("measure range must be N or START-END") from exc
    if len(parts) == 1:
        parts.append(parts[0])
    if min(parts) < 1 or parts[0] > parts[1]:
        raise argparse.ArgumentTypeError("measure range must be positive and ascending")
    return parts[0], parts[1]


def canonical_time(value: float) -> float:
    """Normalize musical time before it becomes an event identity.

    MusicXML backup/forward arithmetic frequently produces values such as
    13.000000000000007 for one voice and 13.0 for another.  They are the same
    notated onset, but treating them as distinct events produces duplicate
    note IDs and labels that appear to drift by one chord member.
    """
    return round(float(value), TIME_PRECISION)


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def children(element: ET.Element, name: str) -> list[ET.Element]:
    return [child for child in element if local(child.tag) == name]


def child(element: ET.Element, name: str) -> ET.Element | None:
    return next((item for item in element if local(item.tag) == name), None)


def text(element: ET.Element, name: str, default: str = "") -> str:
    item = child(element, name)
    return (item.text or default).strip() if item is not None else default


def extract_finger(note: ET.Element) -> int:
    for item in note.iter():
        if local(item.tag) == "fingering":
            raw = (item.text or "").strip()
            circled = {"①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5}
            if raw in circled:
                return circled[raw]
            if raw.isdigit() and 1 <= int(raw) <= 5:
                return int(raw)
    return 0


def tie_types(note: ET.Element) -> set[str]:
    """Read both MusicXML <tie> and notational <tied> declarations."""
    result = set()
    for item in note.iter():
        if local(item.tag) in {"tie", "tied"}:
            tie_type = item.attrib.get("type", "")
            if tie_type in {"start", "stop"}:
                result.add(tie_type)
    return result


def pitch_data(note: ET.Element) -> tuple[str, int, int, int] | None:
    pitch = child(note, "pitch")
    if pitch is None:
        return None
    step = text(pitch, "step")
    octave = int(text(pitch, "octave", "0"))
    alter = int(float(text(pitch, "alter", "0")))
    return step, alter, octave, (octave + 1) * 12 + STEP_PC[step] + alter


def spelled_name(step: str, alter: int) -> str:
    if alter > 0:
        return step + "#" * alter
    if alter < 0:
        return step + "-" * (-alter)
    return step


def normalized_clef(element: ET.Element) -> str | None:
    """Return the supported visual-pitch clef name, if the declaration is known."""
    sign, line = text(element, "sign").upper(), text(element, "line")
    if sign == "G" and line in {"", "2"}:
        return "treble"
    if sign == "F" and line in {"", "4"}:
        return "bass"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--hand-size", default="M")
    routing = parser.add_mutually_exclusive_group()
    routing.add_argument("--part-id", help="for an ambiguous multi-part score, select one grand-staff keyboard part explicitly")
    routing.add_argument("--rh-part-id", help="explicit right-hand one-staff part; requires --lh-part-id")
    parser.add_argument("--lh-part-id", help="explicit left-hand one-staff part; requires --rh-part-id")
    parser.add_argument("--measure-range", type=parse_measure_range, help="extract only N or START-END for a bounded semantic task")
    args = parser.parse_args()
    if args.output.resolve() == args.input.resolve():
        raise ValueError("output must not overwrite the input score")
    tree, source_name = load_musicxml(args.input)
    omr_context = omr_candidate_context(args.input)
    root = tree.getroot()
    parts, part_modes = select_piano_parts(root, args.part_id, args.rh_part_id, args.lh_part_id)
    notes: list[dict] = []
    rests: list[dict] = []
    event_counter = {"RH": 0, "LH": 0}
    open_ties: dict[tuple, str] = {}
    key_signatures: list[dict] = []
    for part_index, part in enumerate(parts):
        part_id = part.attrib.get("id", f"P{part_index + 1}")
        divisions = 1.0
        absolute_time = 0.0
        # A hand and a clef are independent facts.  A left-hand part can be
        # printed in treble clef, and a grand staff can change clef mid-score.
        clefs_by_staff: dict[int, str] = {1: "treble", 2: "bass"}
        keys_by_staff: dict[int, tuple[int, str]] = {1: (0, "unspecified"), 2: (0, "unspecified")}
        for measure_index, measure in enumerate(children(part, "measure"), 1):
            attributes = child(measure, "attributes")
            if attributes is not None and text(attributes, "divisions"):
                proposed_divisions = float(text(attributes, "divisions"))
                if proposed_divisions <= 0:
                    raise ValueError(
                        f"part {part_id} measure {measure_index}: MusicXML divisions must be positive; "
                        "the recognition result has no usable rhythmic timebase"
                    )
                divisions = proposed_divisions
            if attributes is not None:
                for key_element in children(attributes, "key"):
                    key = read_key(key_element)
                    if key is None:
                        continue
                    try:
                        key_staff = int(key_element.attrib.get("number", "0"))
                    except ValueError:
                        key_staff = 0
                    targets = [key_staff] if key_staff else list(keys_by_staff)
                    for target in targets:
                        keys_by_staff[target] = key
                        key_signatures.append({
                            "part": part_id, "measure_index": measure_index, "staff": target,
                            "fifths": key[0], "mode": key[1], "source": "musicxml_attributes",
                        })
                for clef_element in children(attributes, "clef"):
                    try:
                        clef_staff = int(clef_element.attrib.get("number", "1"))
                    except ValueError:
                        clef_staff = 1
                    clef = normalized_clef(clef_element)
                    if clef is not None:
                        clefs_by_staff[clef_staff] = clef
            cursor = canonical_time(absolute_time)
            furthest = cursor
            last_onset = cursor
            raw_notes: list[dict] = []
            raw_rests: list[dict] = []
            voice_chord_rows: dict[tuple, int] = defaultdict(int)
            for element in measure:
                kind = local(element.tag)
                if kind == "backup":
                    cursor = canonical_time(cursor - float(text(element, "duration", "0")) / divisions)
                    continue
                if kind == "forward":
                    cursor = canonical_time(cursor + float(text(element, "duration", "0")) / divisions)
                    furthest = max(furthest, cursor)
                    continue
                if kind != "note":
                    continue
                duration = float(text(element, "duration", "0")) / divisions
                is_chord = child(element, "chord") is not None
                onset = canonical_time(last_onset if is_chord else cursor)
                if not is_chord:
                    last_onset = onset
                pitch = pitch_data(element)
                grace = child(element, "grace") is not None
                staff = int(text(element, "staff", "1"))
                voice = text(element, "voice", "1")
                hand = hand_for_part_staff(part_id, staff, part_modes)
                clef = clefs_by_staff.get(staff, "treble" if staff == 1 else "bass")
                key_fifths, key_mode = keys_by_staff.get(staff, keys_by_staff.get(1, (0, "unspecified")))
                if pitch is not None:
                    step, alter, octave, midi = pitch
                    signature_alter = key_signature_alter(key_fifths, step)
                    # Simultaneous pitches on one staff form one physical hand event,
                    # even when MusicXML encodes them in separate voices via backup.
                    chord_key = (part_id, measure_index, staff, onset)
                    chord_row = voice_chord_rows[chord_key]
                    voice_chord_rows[chord_key] += 1
                    finger = extract_finger(element)
                    ties = tie_types(element)
                    tie_key = (part_id, staff, voice, midi)
                    tie_group = open_ties.get(tie_key)
                    if "start" in ties and tie_group is None:
                        tie_group = f"{part_id}-S{staff}-V{voice}-N{midi}-T{measure_index}-{onset:g}"
                    if "start" in ties and tie_group:
                        open_ties[tie_key] = tie_group
                    raw_notes.append({
                        "_element": element,
                        "_chord_key": chord_key,
                        "note_id": element.attrib.get("id", ""),
                        "part": part_id,
                        "measure": measure.attrib.get("number", str(measure_index)),
                        "measure_index": measure_index,
                        "staff": staff,
                        "voice": voice,
                        "clef": clef,
                        "onset": onset,
                        "duration": duration,
                        "pitch_midi": midi,
                        "pitch_step": step,
                        "pitch_alter": alter,
                        "key_fifths": key_fifths,
                        "key_mode": key_mode,
                        "key_signature_alter": signature_alter,
                        "accidental_scope": "key_signature" if alter == signature_alter else "explicit_or_courtesy",
                        "pitch_octave": octave,
                        "hand": hand,
                        "chord_row": chord_row,
                        "finger": finger,
                        "locked": bool(finger),
                        "source": "existing" if finger else "unassigned",
                        "placement": "above" if hand == "RH" else "below",
                        "grace": grace,
                        "tie_group": tie_group,
                        "tie_start": "start" in ties,
                        "tie_stop": "stop" in ties,
                    })
                    if "stop" in ties and "start" not in ties:
                        open_ties.pop(tie_key, None)
                elif child(element, "rest") is not None:
                    raw_rests.append({
                        "part": part_id,
                        "measure": measure.attrib.get("number", str(measure_index)),
                        "measure_index": measure_index,
                        "staff": staff,
                        "voice": voice,
                        "clef": clef,
                        "onset": onset,
                        "duration": duration,
                        "hand": hand,
                        "rest_type": text(element, "type", "unspecified") or "unspecified",
                        "symbol_class": "rest",
                        "rest_shape_verified": False,
                    })
                if not is_chord and not grace:
                    cursor = canonical_time(cursor + duration)
                    furthest = max(furthest, cursor)
            absolute_time = canonical_time(furthest)
            chord_groups: dict[tuple, list[dict]] = defaultdict(list)
            for record in raw_notes:
                chord_groups[record["_chord_key"]].append(record)
            for group in chord_groups.values():
                group.sort(key=lambda n: n["pitch_midi"])
                # Different MusicXML voices can notate the same physical key
                # at the same onset (for example when a melody is doubled by
                # an inner voice).  It must be one fingering event, not a
                # two-member unison chord.  Preserve the longest sounding
                # value and reject genuinely contradictory source fingers.
                physical_members: list[dict] = []
                for pitch, duplicates in groupby(group, key=lambda n: n["pitch_midi"]):
                    members = list(duplicates)
                    if len(members) == 1:
                        physical_members.append(members[0])
                        continue
                    explicit = {int(member["finger"]) for member in members if int(member["finger"])}
                    if len(explicit) > 1:
                        raise ValueError(
                            f"{part_id} measure {measure_index} onset {members[0]['onset']:g} "
                            f"has conflicting duplicate-voice fingers for MIDI {pitch}"
                        )
                    merged = max(members, key=lambda n: float(n["duration"]))
                    merged["duration"] = max(float(member["duration"]) for member in members)
                    merged["tie_start"] = any(bool(member["tie_start"]) for member in members)
                    merged["tie_stop"] = any(bool(member["tie_stop"]) for member in members)
                    if explicit:
                        merged["finger"] = explicit.pop()
                        merged["locked"] = True
                        merged["source"] = "existing"
                    merged["voice"] = "+".join(sorted({str(member["voice"]) for member in members}))
                    merged["merged_duplicate_voices"] = len(members)
                    physical_members.append(merged)
                group = physical_members
                event_index = event_counter[group[0]["hand"]]
                event_counter[group[0]["hand"]] += 1
                onset_token = f"{float(group[0]['onset']):.{TIME_PRECISION}f}".rstrip("0").rstrip(".") or "0"
                chord_id = f"{part_id}-M{measure_index}-S{group[0]['staff']}-T{onset_token}"
                for row, record in enumerate(group):
                    record["event_index"] = event_index
                    record["chord_id"] = chord_id
                    record["chord_row"] = row
                    record["chord_size"] = len(group)
                    if not record["note_id"]:
                        record["note_id"] = f"{chord_id}-N{record['pitch_midi']}-C{row}"
                    probe = INote(pitch=record["pitch_midi"])
                    record["keyboard_x_cm"] = round(keypos_midi(probe), 6)
                    record.pop("_element", None)
                    record.pop("_chord_key", None)
                    if args.measure_range is None or args.measure_range[0] <= measure_index <= args.measure_range[1]:
                        notes.append(record)
            for serial, record in enumerate(raw_rests):
                onset_token = f"{float(record['onset']):.{TIME_PRECISION}f}".rstrip("0").rstrip(".") or "0"
                record["rest_id"] = (
                    f"{part_id}-M{measure_index}-S{record['staff']}-T{onset_token}"
                    f"-V{record['voice']}-R{serial}"
                )
                if args.measure_range is None or args.measure_range[0] <= measure_index <= args.measure_range[1]:
                    rests.append(record)
    candidate_only = omr_context is not None
    verification = {
        "pitch_spelling": not candidate_only,
        "key_signature": not candidate_only,
        "rhythm": not candidate_only,
        "ties": not candidate_only,
        "chords": not candidate_only,
    }
    source = {
        "type": "omr_candidate" if candidate_only else "musicxml",
        "path": str(args.input.resolve()), "member": source_name,
        "selected_piano_parts": [str(part.attrib.get("id", f"P{index + 1}")) for index, part in enumerate(parts)],
        "piano_part_routing": dict(part_modes),
    }
    if omr_context is not None:
        source["omr_candidate"] = omr_context
    plan = {
        "schema_version": "1.0",
        "source": source,
        "settings": {"hand_size": args.hand_size.upper(), "lookahead": 0},
        "pages": [],
        "recognition": {
            "status": "candidate" if candidate_only else "verified",
            "scope": (
                "local OMR candidate; raw-page verification required" if candidate_only else
                ("complete MusicXML semantic source" if args.measure_range is None
                 else f"MusicXML measures {args.measure_range[0]}-{args.measure_range[1]}")
            ),
            "expected_note_count": len(notes),
            "unresolved_note_count": 0,
            "delivery_level": "review_required" if candidate_only else "complete",
            "verification": verification,
            "key_signatures": key_signatures,
            "source_assets": [structured_asset_record(args.input)],
        },
        "notes": notes,
        "rests": rests,
    }
    # A user-provided MusicXML is structured semantic source; an OMR receipt
    # next to its exact candidate is deliberately kept below the recognition
    # gate until independent raw-page facts are locked.
    set_fact_lock(plan)
    save_plan(args.output, plan)
    print(f"Wrote {args.output} with {len(notes)} notes and {len(rests)} rests.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, ET.ParseError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
