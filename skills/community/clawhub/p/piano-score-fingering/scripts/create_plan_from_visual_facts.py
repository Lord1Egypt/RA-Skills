#!/usr/bin/env python3
"""Compile model-reviewed PDF/image score facts into a draft fingering plan.

The input is deliberately limited to semantic and page-anchor facts observed
from the source score.  Derived fields (MIDI, keyboard geometry, note IDs and
chord membership) are computed here, preventing those representations from
drifting apart.
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
from collections import defaultdict
from pathlib import Path

from fingering_core.models import INote, keypos_midi
from plan_io import save_plan
from source_provenance import visual_asset_records


STEP_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
SHARP_ORDER = ("F", "C", "G", "D", "A", "E", "B")
FLAT_ORDER = tuple(reversed(SHARP_ORDER))
VISUAL_GATES = (
    "scope_complete", "staff_geometry", "pitch_geometry", "key_signature",
    "accidentals", "rhythm", "ties", "chords", "anchors", "pitch_spelling",
)
DEFAULT_VISUAL_CONFIDENCE_POLICY = {
    "require_independent_passes": 2,
    "require_measure_region_coverage": True,
    "require_measure_symbol_checks": True,
    "require_event_topology": True,
    "require_rest_inventory": True,
    "require_direct_notehead_anchors": True,
    "require_dense_event_checks": True,
    "dense_notehead_threshold": 8,
    "require_notehead_shape_evidence": True,
    "require_sparse_rest_checks": True,
    "sparse_event_threshold": 1,
    "require_same_position_evidence": True,
    "require_tie_evidence": True,
}
MANDATORY_VISUAL_POLICY_FLAGS = tuple(
    key for key, value in DEFAULT_VISUAL_CONFIDENCE_POLICY.items() if value is True
)


def number(value: object, field: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be numeric") from exc


def integer(value: object, field: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be an integer") from exc


def token(value: float) -> str:
    return f"{value:.8f}".rstrip("0").rstrip(".") or "0"


def note_pitch(note: dict, index: int) -> tuple[str, int, int, int]:
    step = str(note.get("pitch_step", "")).upper()
    if step not in STEP_PC:
        raise ValueError(f"notes[{index}].pitch_step must be A-G")
    alter = integer(note.get("pitch_alter", 0), f"notes[{index}].pitch_alter")
    octave = integer(note.get("pitch_octave"), f"notes[{index}].pitch_octave")
    midi = (octave + 1) * 12 + STEP_PC[step] + alter
    supplied = note.get("pitch_midi")
    if supplied is not None and integer(supplied, f"notes[{index}].pitch_midi") != midi:
        raise ValueError(f"notes[{index}] spelling conflicts with pitch_midi")
    if not 0 <= midi <= 127:
        raise ValueError(f"notes[{index}] has MIDI pitch outside 0-127")
    return step, alter, octave, midi


def signature_alter(fifths: int, step: str) -> int:
    return (1 if step in SHARP_ORDER[:fifths] else 0) if fifths >= 0 else (-1 if step in FLAT_ORDER[:(-fifths)] else 0)


def normalized_key_signatures(raw: object) -> list[dict]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise ValueError("recognition.key_signatures must be a list")
    keys: list[dict] = []
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"recognition.key_signatures[{index}] must be an object")
        fifths = integer(item.get("fifths"), f"recognition.key_signatures[{index}].fifths")
        if not -7 <= fifths <= 7:
            raise ValueError(f"recognition.key_signatures[{index}].fifths must be between -7 and 7")
        keys.append({
            **item,
            "page": integer(item.get("page", 1), f"recognition.key_signatures[{index}].page"),
            "measure_index": integer(item.get("measure_index", 1), f"recognition.key_signatures[{index}].measure_index"),
            "staff": integer(item.get("staff", 0), f"recognition.key_signatures[{index}].staff"),
            "fifths": fifths,
            "mode": str(item.get("mode", "unspecified")),
        })
    return keys


def key_for_note(note: dict, keys: list[dict]) -> tuple[int, str]:
    candidates = [
        key for key in keys
        if key["page"] == note["page"]
        and key["measure_index"] <= note["measure_index"]
        and key["staff"] in {0, note["staff"]}
        and str(key.get("part", note["part"])) == note["part"]
    ]
    if not candidates:
        return 0, "unspecified"
    selected = max(candidates, key=lambda item: (item["measure_index"], 1 if item["staff"] == note["staff"] else 0))
    return int(selected["fifths"]), str(selected["mode"])


def visual_note(raw: dict, index: int, keys: list[dict]) -> dict:
    if not isinstance(raw, dict):
        raise ValueError(f"notes[{index}] must be an object")
    step, alter, octave, midi = note_pitch(raw, index)
    hand = str(raw.get("hand", "")).upper()
    if hand not in {"RH", "LH"}:
        raise ValueError(f"notes[{index}].hand must be RH or LH")
    page = integer(raw.get("page"), f"notes[{index}].page")
    measure = integer(raw.get("measure_index", raw.get("measure")), f"notes[{index}].measure_index")
    staff = integer(raw.get("staff"), f"notes[{index}].staff")
    onset = number(raw.get("onset"), f"notes[{index}].onset")
    duration = number(raw.get("duration"), f"notes[{index}].duration")
    if page < 1 or measure < 1 or staff < 1 or onset < 0 or duration <= 0:
        raise ValueError(f"notes[{index}] has an invalid page, measure, staff, onset or duration")
    for field in ("page_x", "page_y"):
        number(raw.get(field), f"notes[{index}].{field}")
    record = dict(raw)
    record.update({
        "part": str(raw.get("part", "P1")),
        "measure": str(raw.get("measure", measure)),
        "measure_index": measure,
        "staff": staff,
        "voice": str(raw.get("voice", "1")),
        "hand": hand,
        "onset": round(onset, 8),
        "duration": round(duration, 8),
        "pitch_step": step,
        "pitch_alter": alter,
        "pitch_octave": octave,
        "pitch_midi": midi,
        "page": page,
        "page_x": number(raw.get("page_x"), f"notes[{index}].page_x"),
        "page_y": number(raw.get("page_y"), f"notes[{index}].page_y"),
        "keyboard_x_cm": round(keypos_midi(INote(pitch=midi)), 6),
        "placement": "above" if hand == "RH" else "below",
        "anchor_method": str(raw.get("anchor_method", "visual_notehead")),
        "locked": bool(raw.get("locked", False)),
        "source": str(raw.get("source", "unassigned")),
    })
    fifths, mode = key_for_note(record, keys)
    actual_signature_alter = signature_alter(fifths, step)
    record["key_fifths"] = fifths
    record["key_mode"] = mode
    record["key_signature_alter"] = actual_signature_alter
    record["accidental_scope"] = str(
        raw.get("accidental_scope", "key_signature" if alter == actual_signature_alter else "explicit_or_courtesy")
    )
    return record


def compile_notes(raw_notes: list[object], keys: list[dict]) -> list[dict]:
    notes = [visual_note(raw, index, keys) for index, raw in enumerate(raw_notes)]
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for note in notes:
        # A physical piano event is defined by hand, staff and onset, not by
        # the voice encoding used by the engraving application.  MusicXML
        # imports already merge notes split by <backup>/<voice>; retaining a
        # voice key only on visual input created two incompatible event models
        # and could let simultaneous notes reuse a finger.
        groups[(note["part"], note["measure_index"], note["staff"], note["onset"], note["hand"])].append(note)
    event_index: dict[str, int] = defaultdict(int)
    seen: set[str] = set()
    for key in sorted(groups):
        members = sorted(groups[key], key=lambda item: (item["pitch_midi"], item["page_y"], item["page_x"]))
        part, measure, staff, onset, hand = key
        chord_id = f"{part}-M{measure}-S{staff}-T{token(onset)}"
        current_event = event_index[hand]
        event_index[hand] += 1
        for row, note in enumerate(members):
            note["event_index"] = current_event
            note["chord_id"] = chord_id
            note["chord_row"] = row
            note["chord_size"] = len(members)
            note.setdefault("note_id", f"{chord_id}-N{note['pitch_midi']}-C{row}")
            if note["note_id"] in seen:
                raise ValueError(f"duplicate note_id: {note['note_id']}")
            seen.add(note["note_id"])
    return sorted(notes, key=lambda item: (item["page"], item["measure_index"], item["onset"], item["hand"], item["chord_row"]))


def compile_rests(raw_rests: list[object]) -> list[dict]:
    rests: list[dict] = []
    for index, raw in enumerate(raw_rests):
        if not isinstance(raw, dict):
            raise ValueError(f"rests[{index}] must be an object")
        page = integer(raw.get("page"), f"rests[{index}].page")
        measure = integer(raw.get("measure_index", raw.get("measure")), f"rests[{index}].measure_index")
        hand = str(raw.get("hand", "")).upper()
        if page < 1 or measure < 1 or hand not in {"RH", "LH"}:
            raise ValueError(f"rests[{index}] has invalid page, measure or hand")
        record = dict(raw)
        record.update({"page": page, "measure_index": measure, "hand": hand, "symbol_class": "rest"})
        record.setdefault("rest_id", f"p{page}-m{measure}-{hand.lower()}-rest-{index}")
        rests.append(record)
    return rests


def normalized_pages(raw_pages: object) -> list[dict]:
    if not isinstance(raw_pages, list) or not raw_pages:
        raise ValueError("pages must list every rendered source page")
    pages: list[dict] = []
    seen: set[int] = set()
    for index, raw in enumerate(raw_pages):
        if not isinstance(raw, dict):
            raise ValueError("every pages[] item must be an object")
        page = integer(raw.get("page"), f"pages[{index}].page")
        width = number(raw.get("width"), f"pages[{index}].width")
        height = number(raw.get("height"), f"pages[{index}].height")
        if page < 1 or width <= 0 or height <= 0 or page in seen:
            raise ValueError(f"pages[{index}] has duplicate/invalid page dimensions")
        seen.add(page)
        pages.append({**raw, "page": page, "width": width, "height": height})
    return pages


def png_dimensions(path: Path) -> tuple[int, int]:
    """Read PNG dimensions without a third-party image dependency."""
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError(f"page image must be a valid PNG: {path}")
    width, height = struct.unpack(">II", header[16:24])
    if width <= 0 or height <= 0:
        raise ValueError(f"page image has invalid dimensions: {path}")
    return width, height


def validate_page_image_dimensions(pages: list[dict], facts_path: Path) -> None:
    """Reject silent coordinate scaling before it can drift every label."""
    for page in pages:
        image = str(page.get("image", "")).strip()
        if not image:
            raise ValueError(f"pages[{page['page']}].image is required for visual coordinate facts")
        image_path = Path(image)
        if not image_path.is_absolute():
            image_path = facts_path.parent / image_path
        if not image_path.is_file():
            raise ValueError(f"page image not found: {image_path}")
        actual_width, actual_height = png_dimensions(image_path)
        declared_width, declared_height = page["width"], page["height"]
        if actual_width != declared_width or actual_height != declared_height:
            raise ValueError(
                f"page {page['page']} dimensions ({declared_width:g}×{declared_height:g}) do not match "
                f"its PNG ({actual_width}×{actual_height}); re-read anchors in the source image coordinate system"
            )


def validate_page_bounds(notes: list[dict], rests: list[dict], pages: list[dict]) -> None:
    dimensions = {page["page"]: (page["width"], page["height"]) for page in pages}
    for kind, records in (("notes", notes), ("rests", rests)):
        for index, record in enumerate(records):
            if record["page"] not in dimensions:
                raise ValueError(f"{kind}[{index}] refers to undeclared page {record['page']}")
            if kind == "rests" and ("page_x" not in record or "page_y" not in record):
                raise ValueError(f"rests[{index}].page_x/page_y are required visual facts")
            x, y = number(record.get("page_x"), f"{kind}[{index}].page_x"), number(record.get("page_y"), f"{kind}[{index}].page_y")
            width, height = dimensions[record["page"]]
            if not 0 <= x <= width or not 0 <= y <= height:
                raise ValueError(f"{kind}[{index}] anchor lies outside page {record['page']} bounds")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("facts", type=Path, help="model-reviewed visual facts JSON")
    parser.add_argument("-o", "--output", required=True, type=Path)
    args = parser.parse_args()
    raw = json.loads(args.facts.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("facts root must be an object")
    source = raw.get("source", {})
    if not isinstance(source, dict) or source.get("type") not in {"pdf", "image"}:
        raise ValueError("source.type must be pdf or image")
    source = dict(source)
    render_dpi = number(source.get("render_dpi", 144), "source.render_dpi")
    if not 36 <= render_dpi <= 600:
        raise ValueError("source.render_dpi must be between 36 and 600")
    source["render_dpi"] = render_dpi
    pages = normalized_pages(raw.get("pages", []))
    validate_page_image_dimensions(pages, args.facts)
    # Store absolute rendered-page paths and hashes.  A label anchor cannot be
    # safely carried across a different page render, even at the same DPI.
    source_assets = visual_asset_records(pages, args.facts.parent)
    for page, asset in zip(sorted(pages, key=lambda item: item["page"]), source_assets):
        page["image"] = asset["path"]
    page_numbers = {page["page"] for page in pages}
    supplied_recognition = raw.get("recognition", {})
    if not isinstance(supplied_recognition, dict):
        raise ValueError("recognition must be an object")
    keys = normalized_key_signatures(supplied_recognition.get("key_signatures", []))
    notes = compile_notes(raw.get("notes", []), keys)
    rests = compile_rests(raw.get("rests", []))
    unknown_pages = {item["page"] for item in notes + rests} - page_numbers
    if unknown_pages:
        raise ValueError(f"facts refer to undeclared page(s): {sorted(unknown_pages)}")
    validate_page_bounds(notes, rests, pages)
    supplied_verification = supplied_recognition.get("verification", {})
    if not isinstance(supplied_verification, dict):
        raise ValueError("recognition.verification must be an object")
    verification = {gate: False for gate in VISUAL_GATES}
    verification.update({key: value for key, value in supplied_verification.items() if key in verification})
    recognition = dict(supplied_recognition)
    supplied_policy = supplied_recognition.get("confidence_policy", {})
    if not isinstance(supplied_policy, dict):
        raise ValueError("recognition.confidence_policy must be an object")
    weakened = [key for key in MANDATORY_VISUAL_POLICY_FLAGS if supplied_policy.get(key) is False]
    if weakened:
        raise ValueError(f"visual facts cannot disable required confidence policy flags: {weakened}")
    confidence_policy = dict(DEFAULT_VISUAL_CONFIDENCE_POLICY)
    confidence_policy.update(supplied_policy)
    recognition.update({
        "status": "draft",
        "expected_note_count": len(notes),
        "unresolved_note_count": int(supplied_recognition.get("unresolved_note_count", 0) or 0),
        "verification": verification,
        "review_queue": [],
        "key_signatures": keys,
        "confidence_policy": confidence_policy,
        "source_assets": source_assets,
    })
    plan = {
        "schema_version": "1.0",
        "source": dict(source),
        "settings": dict(raw.get("settings", {"hand_size": "M", "lookahead": 0})),
        "pages": pages,
        "recognition": recognition,
        "notes": notes,
        "rests": rests,
    }
    save_plan(args.output, plan)
    print(f"Wrote draft visual plan with {len(notes)} notes and {len(rests)} rests: {args.output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
