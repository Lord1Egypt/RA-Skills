#!/usr/bin/env python3
"""Validate score facts before any piano fingering is generated."""

from __future__ import annotations

import argparse
import statistics
import sys
from collections import defaultdict
from pathlib import Path

from fingering_core import INote, keypos_midi
from plan_io import load_plan
from recognition_state import open_review_items, verify_fact_lock
from source_provenance import verify_source_assets


STEP_INDEX = {"C": 0, "D": 1, "E": 2, "F": 3, "G": 4, "A": 5, "B": 6}
STEP_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
TOP_LINE = {
    "treble": ("F", 5),
    "g": ("F", 5),
    "bass": ("A", 3),
    "f": ("A", 3),
}
VISUAL_GATES = (
    "scope_complete",
    "staff_geometry",
    "pitch_geometry",
    "key_signature",
    "accidentals",
    "rhythm",
    "ties",
    "chords",
    "anchors",
)
SEMANTIC_GATES = ("pitch_spelling", "rhythm", "ties", "chords")
INDEPENDENT_MEASURE_SOURCES = {"independent_visual_review", "source_semantic"}
# Visual plans are factual records, not a best-effort import format. Keep the
# policy contract here as well as in the visual-facts compiler: otherwise an
# older plan that simply lacks a newly added gate can silently bypass it.
MANDATORY_VISUAL_POLICY_FLAGS = (
    "require_measure_region_coverage",
    "require_measure_symbol_checks",
    "require_event_topology",
    "require_rest_inventory",
    "require_direct_notehead_anchors",
    "require_dense_event_checks",
    "require_notehead_shape_evidence",
    "require_sparse_rest_checks",
    "require_same_position_evidence",
    "require_tie_evidence",
)


def _scope_key(record: dict) -> tuple[int, int, str]:
    return (
        int(record.get("page", 0) or 0),
        int(record.get("measure_index", record.get("measure", 0)) or 0),
        str(record.get("hand", "")).upper(),
    )


def _inside_bbox(record: dict, bbox: list[float]) -> bool:
    try:
        x = float(record["page_x"])
        y = float(record["page_y"])
    except (KeyError, TypeError, ValueError):
        return False
    x0, y0, x1, y1 = bbox
    return min(x0, x1) <= x <= max(x0, x1) and min(y0, y1) <= y <= max(y0, y1)


def _validate_measure_evidence(
    plan: dict,
    confidence_policy: dict,
) -> list[str]:
    """Validate raw-image evidence for every declared measure/hand region."""
    errors: list[str] = []
    recognition = plan.get("recognition", {})
    regions = recognition.get("measure_regions", [])
    checks = recognition.get("measure_symbol_checks", [])
    rests = plan.get("rests", [])

    expected_scopes: set[tuple[int, int, str]] = set()
    measure_scope = recognition.get("measure_scope", [])
    if confidence_policy.get("require_measure_region_coverage") and not measure_scope:
        errors.append(
            "recognition.measure_scope must declare every target page and measure range before coverage can be proved"
        )
    for index, scope in enumerate(measure_scope):
        if not isinstance(scope, dict):
            errors.append(f"recognition.measure_scope[{index}] must be an object")
            continue
        try:
            page = int(scope["page"])
            measure_start = int(scope["measure_start"])
            measure_end = int(scope["measure_end"])
            hands = [str(hand).upper() for hand in scope["hands"]]
        except (KeyError, TypeError, ValueError):
            errors.append(f"recognition.measure_scope[{index}] is incomplete")
            continue
        if page < 1 or measure_start < 1 or measure_end < measure_start or not hands:
            errors.append(f"recognition.measure_scope[{index}] has an invalid page/range/hands")
            continue
        if any(hand not in {"RH", "LH"} for hand in hands):
            errors.append(f"recognition.measure_scope[{index}].hands must contain only RH/LH")
            continue
        for measure in range(measure_start, measure_end + 1):
            for hand in hands:
                expected_scopes.add((page, measure, hand))

    region_by_id: dict[str, dict] = {}
    region_by_scope: dict[tuple[int, int, str], str] = {}
    region_bbox: dict[str, list[float]] = {}
    for index, region in enumerate(regions):
        if not isinstance(region, dict):
            errors.append(f"recognition.measure_regions[{index}] must be an object")
            continue
        region_id = str(region.get("region_id", "")).strip()
        try:
            key = _scope_key(region)
        except (TypeError, ValueError):
            errors.append(f"recognition.measure_regions[{index}] has invalid page/measure/hand")
            continue
        if not region_id or region_id in region_by_id:
            errors.append(f"recognition.measure_regions[{index}] has duplicate/empty region_id")
            continue
        if key[0] < 1 or key[1] < 1 or key[2] not in {"RH", "LH"}:
            errors.append(f"{region_id}: page, measure and hand must identify one visual measure region")
        if key in region_by_scope:
            errors.append(f"{region_id}: duplicates measure region {region_by_scope[key]}")
        bbox = region.get("bbox")
        if not isinstance(bbox, list) or len(bbox) != 4:
            errors.append(f"{region_id}: bbox must contain [x0, y0, x1, y1]")
        else:
            try:
                numeric_bbox = [float(value) for value in bbox]
                if numeric_bbox[0] == numeric_bbox[2] or numeric_bbox[1] == numeric_bbox[3]:
                    raise ValueError
                region_bbox[region_id] = numeric_bbox
            except (TypeError, ValueError):
                errors.append(f"{region_id}: bbox must describe a non-empty numeric rectangle")
        evidence_crop = str(region.get("evidence_crop", "")).strip()
        if not evidence_crop:
            errors.append(f"{region_id}: evidence_crop is required; full-page memory is not source evidence")
        region_by_id[region_id] = region
        region_by_scope[key] = region_id

    if expected_scopes:
        missing_scopes = expected_scopes - set(region_by_scope)
        extra_scopes = set(region_by_scope) - expected_scopes
        for page, measure, hand in sorted(missing_scopes):
            errors.append(f"page {page} measure {measure} {hand}: target scope has no measure_region")
        for page, measure, hand in sorted(extra_scopes):
            errors.append(f"page {page} measure {measure} {hand}: measure_region lies outside declared measure_scope")

    check_by_region: dict[str, list[dict]] = defaultdict(list)
    for index, check in enumerate(checks):
        if not isinstance(check, dict):
            errors.append(f"recognition.measure_symbol_checks[{index}] must be an object")
            continue
        region_id = str(check.get("region_id", "")).strip()
        check_by_region[region_id].append(check)

    note_counts: dict[tuple[int, int, str], int] = defaultdict(int)
    rest_counts: dict[tuple[int, int, str], int] = defaultdict(int)
    for note in plan.get("notes", []):
        try:
            key = _scope_key(note)
        except (TypeError, ValueError):
            continue
        note_counts[key] += 1
        region_id = region_by_scope.get(key)
        if region_id is None:
            errors.append(f"{note.get('note_id', 'unknown')}: no declared measure_region covers this note")
        elif region_id in region_bbox and not _inside_bbox(note, region_bbox[region_id]):
            errors.append(f"{note.get('note_id', 'unknown')}: notehead anchor lies outside {region_id}.bbox")
    for rest in rests:
        try:
            key = _scope_key(rest)
        except (TypeError, ValueError):
            errors.append(f"{rest.get('rest_id', 'unknown')}: invalid page/measure/hand")
            continue
        rest_counts[key] += 1
        region_id = region_by_scope.get(key)
        if region_id is None:
            errors.append(f"{rest.get('rest_id', 'unknown')}: no declared measure_region covers this rest")
        elif region_id in region_bbox and not _inside_bbox(rest, region_bbox[region_id]):
            errors.append(f"{rest.get('rest_id', 'unknown')}: rest anchor lies outside {region_id}.bbox")

    for region_id, region in region_by_id.items():
        matching = check_by_region.get(region_id, [])
        if len(matching) != 1:
            errors.append(f"{region_id}: requires exactly one independent measure_symbol_check, found {len(matching)}")
            continue
        check = matching[0]
        key = _scope_key(region)
        if _scope_key(check) != key:
            errors.append(f"{region_id}: measure_symbol_check page/measure/hand does not match its region")
        if check.get("verified") is not True:
            errors.append(f"{region_id}: measure_symbol_check must be verified")
        if check.get("duration_verified") is not True:
            errors.append(f"{region_id}: note/rest durations must be verified from the raw crop")
        if str(check.get("source", "")) not in INDEPENDENT_MEASURE_SOURCES:
            errors.append(f"{region_id}: check source must be independent_visual_review or source_semantic")
        evidence_crop = str(check.get("evidence_crop", "")).strip()
        if not evidence_crop or evidence_crop != str(region.get("evidence_crop", "")).strip():
            errors.append(f"{region_id}: check must cite the exact region evidence_crop")
        try:
            expected_notes = int(check["expected_noteheads"])
            expected_rests = int(check["expected_rests"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"{region_id}: expected_noteheads and expected_rests must be independently entered integers")
            continue
        if expected_notes < 0 or expected_rests < 0:
            errors.append(f"{region_id}: expected counts cannot be negative")
            continue
        if note_counts[key] != expected_notes:
            errors.append(
                f"{region_id}: raw crop has {expected_notes} notehead(s), but plan contains {note_counts[key]}"
            )
        if rest_counts[key] != expected_rests:
            errors.append(
                f"{region_id}: raw crop has {expected_rests} rest(s), but plan contains {rest_counts[key]}"
            )
        if confidence_policy.get("require_event_topology"):
            try:
                expected_events = int(check["expected_attack_events"])
                expected_sizes = [int(value) for value in check["expected_chord_sizes"]]
            except (KeyError, TypeError, ValueError):
                errors.append(
                    f"{region_id}: expected_attack_events and ordered expected_chord_sizes "
                    "must be independently entered"
                )
                continue
            if expected_events < 0 or any(size < 1 for size in expected_sizes):
                errors.append(f"{region_id}: attack-event counts and chord sizes must be positive")
                continue
            if expected_events != len(expected_sizes) or sum(expected_sizes) != expected_notes:
                errors.append(
                    f"{region_id}: attack-event topology does not reconcile with expected_noteheads"
                )
                continue
            # Voice labels are engraving metadata.  At one staff/onset the
            # pianist has one physical attack, so merge cross-voice notes here
            # exactly as the MusicXML importer does.
            # Collapse all voice encodings into one (staff, onset) attack
            # before comparing the independently entered topology.
            event_sizes: dict[tuple[int, float], int] = {}
            for candidate in plan.get("notes", []):
                if _scope_key(candidate) != key:
                    continue
                event_key = (int(candidate.get("staff", 0)), float(candidate.get("onset", 0)))
                event_sizes[event_key] = event_sizes.get(event_key, 0) + 1
            actual_sizes = [size for _, size in sorted(event_sizes.items())]
            if actual_sizes != expected_sizes:
                errors.append(
                    f"{region_id}: raw crop attack topology {expected_sizes}, but plan contains {actual_sizes}"
                )

    for region_id in check_by_region.keys() - region_by_id.keys():
        errors.append(f"{region_id or '<empty>'}: measure_symbol_check has no declared measure_region")

    if confidence_policy.get("require_rest_inventory"):
        for rest in rests:
            rest_id = str(rest.get("rest_id", "unknown"))
            if rest.get("symbol_class") != "rest" or rest.get("rest_shape_verified") is not True:
                errors.append(f"{rest_id}: rest must have symbol_class=rest and rest_shape_verified=true")
            if not str(rest.get("rest_type", "")).strip() or rest.get("duration") is None:
                errors.append(f"{rest_id}: rest_type and duration are required")
    return errors


def diatonic_index(step: str, octave: int) -> int:
    return int(octave) * 7 + STEP_INDEX[step]


def _systems(plan: dict) -> tuple[dict[str, dict], list[str]]:
    result: dict[str, dict] = {}
    errors: list[str] = []
    for index, system in enumerate(plan.get("recognition", {}).get("systems", [])):
        if not isinstance(system, dict):
            errors.append(f"recognition.systems[{index}] must be an object")
            continue
        system_id = str(system.get("system_id", ""))
        if not system_id or system_id in result:
            errors.append(f"recognition.systems[{index}] has duplicate/empty system_id")
            continue
        lines = system.get("staff_line_y")
        if not isinstance(lines, list) or len(lines) != 5:
            errors.append(f"{system_id}: staff_line_y must contain five top-to-bottom line coordinates")
            continue
        try:
            line_y = [float(value) for value in lines]
        except (TypeError, ValueError):
            errors.append(f"{system_id}: staff_line_y must be numeric")
            continue
        gaps = [abs(b - a) for a, b in zip(line_y, line_y[1:])]
        if min(gaps) <= 0 or max(gaps) / min(gaps) > 1.25:
            errors.append(f"{system_id}: staff lines are not a stable five-line geometry")
            continue
        copy = dict(system)
        copy["staff_line_y"] = line_y
        result[system_id] = copy
    return result, errors


def _top_line_pitch(system: dict) -> tuple[str, int] | None:
    if system.get("top_line_step") is not None and system.get("top_line_octave") is not None:
        step = str(system["top_line_step"]).upper()
        if step in STEP_INDEX:
            return step, int(system["top_line_octave"])
        return None
    return TOP_LINE.get(str(system.get("clef", "")).lower())


def validate_recognition(
    plan: dict,
    *,
    strict: bool = True,
    require_locked: bool = True,
) -> tuple[list[str], list[str]]:
    """Return semantic score-fact errors and non-blocking review warnings."""
    errors: list[str] = []
    warnings: list[str] = []
    source_type = str(plan.get("source", {}).get("type", "musicxml")).lower()
    visual = source_type in {"pdf", "image"}
    omr_candidate = source_type == "omr_candidate"
    recognition = plan.get("recognition", {})
    verification = recognition.get("verification", {})
    confidence_policy = recognition.get("confidence_policy", {})
    required_gates = VISUAL_GATES if visual else SEMANTIC_GATES
    if strict:
        if omr_candidate:
            errors.append(
                "source is a local OMR candidate, not an authoritative MusicXML source; "
                "compile verified raw-page facts before fingering generation"
            )
        for gate in required_gates:
            if verification.get(gate) is not True:
                errors.append(f"recognition.verification.{gate} must be true before fingering generation")
        open_items = open_review_items(plan)
        if open_items:
            errors.append(f"recognition.review_queue contains {len(open_items)} unresolved item(s)")
        if require_locked:
            errors.extend(verify_fact_lock(plan))
        # Verify the content, not merely the pathname.  This stops stale
        # plans from being used after a PDF was replaced or rerendered.
        errors.extend(verify_source_assets(plan))
        if visual:
            # Do not treat omitted booleans as an intentional opt-out. A
            # visual plan made with an older template must be recompiled from
            # its visual facts so all current factual gates are applied.
            for flag in MANDATORY_VISUAL_POLICY_FLAGS:
                if confidence_policy.get(flag) is not True:
                    errors.append(
                        f"recognition.confidence_policy.{flag} must be true for visual plans; "
                        "recompile this legacy plan from visual facts"
                    )
            if int(confidence_policy.get("require_independent_passes", 0) or 0) < 2:
                errors.append(
                    "recognition.confidence_policy.require_independent_passes must be at least 2 "
                    "for visual plans; recompile this legacy plan from visual facts"
                )
            if int(confidence_policy.get("dense_notehead_threshold", 0) or 0) < 1:
                errors.append(
                    "recognition.confidence_policy.dense_notehead_threshold must be positive "
                    "for visual plans; recompile this legacy plan from visual facts"
                )
            if int(confidence_policy.get("sparse_event_threshold", 0) or 0) < 1:
                errors.append(
                    "recognition.confidence_policy.sparse_event_threshold must be positive "
                    "for visual plans; recompile this legacy plan from visual facts"
                )

    systems, system_errors = _systems(plan)
    errors.extend(system_errors)
    if visual and strict and not systems:
        errors.append("recognition.systems must define verified five-line geometry for every visual staff")

    tie_groups: dict[str, list[dict]] = defaultdict(list)
    simultaneous_keys: dict[tuple, list[str]] = defaultdict(list)
    for note in plan.get("notes", []):
        note_id = str(note.get("note_id", "unknown"))
        step = str(note.get("pitch_step", "")).upper()
        try:
            octave = int(note["pitch_octave"])
            alter = int(note.get("pitch_alter", 0) or 0)
            midi = int(note["pitch_midi"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"{note_id}: pitch_step/pitch_alter/pitch_octave/pitch_midi are required score facts")
            continue
        if step not in STEP_INDEX:
            errors.append(f"{note_id}: invalid pitch_step {step!r}")
            continue
        spelled_midi = (octave + 1) * 12 + STEP_PC[step] + alter
        if spelled_midi != midi:
            errors.append(
                f"{note_id}: pitch spelling {step}{alter:+d}/{octave} gives MIDI {spelled_midi}, not {midi}"
            )
        # A confirmed key signature is score fact, not a fingering hint.  It
        # makes explicit whether a written F in G major is the default F# or
        # an accidental/courtesy exception before keyboard geometry is used.
        if verification.get("key_signature") is True:
            try:
                fifths = int(note["key_fifths"])
                signature_alter = int(note["key_signature_alter"])
            except (KeyError, TypeError, ValueError):
                errors.append(f"{note_id}: key_fifths/key_signature_alter are required when key signature is verified")
            else:
                if not -7 <= fifths <= 7:
                    errors.append(f"{note_id}: key_fifths must be between -7 and 7")
                expected_signature_alter = (1 if step in ("F", "C", "G", "D", "A", "E", "B")[:fifths] else 0) if fifths >= 0 else (-1 if step in ("B", "E", "A", "D", "G", "C", "F")[:(-fifths)] else 0)
                if signature_alter != expected_signature_alter:
                    errors.append(f"{note_id}: key_signature_alter conflicts with key_fifths and written step")
        simultaneous_keys[(
            str(note.get("part", "")), str(note.get("hand", "")).upper(),
            int(note.get("measure_index", 0) or 0), float(note.get("onset", 0) or 0), midi,
        )].append(note_id)
        try:
            keyboard_x = float(note["keyboard_x_cm"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"{note_id}: keyboard_x_cm is required and must be derived from pitch_midi")
        else:
            expected_keyboard_x = keypos_midi(INote(pitch=midi))
            if abs(keyboard_x - expected_keyboard_x) > 0.02:
                errors.append(
                    f"{note_id}: keyboard_x_cm {keyboard_x:.4f} conflicts with MIDI {midi}; "
                    f"expected physical key centre {expected_keyboard_x:.4f}"
                )

        tie_group = note.get("tie_group")
        if note.get("tie_start") or note.get("tie_stop"):
            if not tie_group:
                errors.append(f"{note_id}: tie_start/tie_stop requires tie_group")
            else:
                tie_groups[str(tie_group)].append(note)
        elif tie_group:
            tie_groups[str(tie_group)].append(note)

        if not visual:
            continue
        if note.get("anchor_verified") is not True:
            errors.append(f"{note_id}: anchor_verified must be true before visual-score fingering")
        system_id = str(note.get("staff_geometry_id", ""))
        system = systems.get(system_id)
        if system is None:
            errors.append(f"{note_id}: missing/unknown staff_geometry_id {system_id!r}")
            continue
        try:
            page_y = float(note["page_y"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"{note_id}: page_y is required for pitch-geometry verification")
            continue
        lines = system["staff_line_y"]
        direction = 1 if lines[-1] > lines[0] else -1
        half_step_y = statistics.median(abs(b - a) for a, b in zip(lines, lines[1:])) / 2.0
        raw_position = (page_y - lines[0]) / (direction * half_step_y)
        position = round(raw_position)
        residual = abs(raw_position - position)
        if residual > float(system.get("position_tolerance", 0.48)):
            errors.append(f"{note_id}: page_y is not centered on a line/space position (residual {residual:.2f})")
            continue
        top = _top_line_pitch(system)
        if top is None:
            errors.append(f"{system_id}: clef or explicit top-line pitch is required")
            continue
        expected = diatonic_index(*top) - position
        actual = diatonic_index(step, octave)
        if expected != actual:
            errors.append(
                f"{note_id}: page_y implies diatonic index {expected}, but extracted {step}{octave} is {actual}"
            )
        elif note.get("pitch_geometry_verified") is not True:
            errors.append(f"{note_id}: pitch_geometry_verified must be true after visual comparison")

    # A single hand cannot press one physical key twice at the same instant.
    # This commonly signals a malformed multi-voice MusicXML import or a
    # duplicated visual detection.  Stopping here prevents impossible chord
    # fingerings from being mistaken for a solver failure downstream.
    for (part, hand, measure, onset, midi), note_ids in simultaneous_keys.items():
        if len(note_ids) > 1:
            errors.append(
                f"{part or 'unknown'} {hand or 'unknown'} measure {measure} onset {onset:g}: "
                f"duplicate simultaneous MIDI {midi} in {', '.join(note_ids)}; merge or review score facts"
            )

    if visual and strict:
        if (
            confidence_policy.get("require_measure_region_coverage")
            or confidence_policy.get("require_measure_symbol_checks")
            or confidence_policy.get("require_rest_inventory")
        ):
            errors.extend(_validate_measure_evidence(plan, confidence_policy))

        if confidence_policy.get("require_direct_notehead_anchors"):
            chord_groups: dict[str, list[dict]] = defaultdict(list)
            for note in plan.get("notes", []):
                note_id = str(note.get("note_id", "unknown"))
                if note.get("origin") != "direct_visual_notehead":
                    errors.append(
                        f"{note_id}: visual note origin must be direct_visual_notehead; inferred chord members are forbidden"
                    )
                if note.get("symbol_class") != "notehead" or note.get("notehead_shape_verified") is not True:
                    errors.append(f"{note_id}: direct visual note requires verified notehead shape")
                chord_size = int(note.get("chord_size", 1) or 1)
                if chord_size > 1:
                    if note.get("chord_member_verified") is not True:
                        errors.append(f"{note_id}: every merged/visible chord member needs its own verified center")
                    chord_id = str(note.get("chord_id", "")).strip()
                    if not chord_id:
                        errors.append(f"{note_id}: multi-note chord member requires chord_id")
                    else:
                        chord_groups[chord_id].append(note)
            for chord_id, members in chord_groups.items():
                declared = {int(note.get("chord_size", 1) or 1) for note in members}
                if len(declared) != 1 or declared != {len(members)}:
                    errors.append(
                        f"chord {chord_id}: declared chord_size {sorted(declared)} does not match "
                        f"{len(members)} directly verified member(s)"
                    )

        if confidence_policy.get("require_notehead_shape_evidence"):
            missing_by_scope: dict[tuple, list[str]] = defaultdict(list)
            for note in plan.get("notes", []):
                if (
                    note.get("symbol_class") == "notehead"
                    and note.get("notehead_shape_verified") is True
                ):
                    continue
                key = (note.get("page"), note.get("measure_index"), note.get("hand"))
                missing_by_scope[key].append(str(note.get("note_id", "unknown")))
            for (page, measure, hand), note_ids in sorted(missing_by_scope.items(), key=lambda item: str(item[0])):
                errors.append(
                    f"page {page} measure {measure} {hand}: {len(note_ids)} candidate(s) lack "
                    "verified notehead-shape evidence; exclude rests, beams, stems and barlines"
                )

        if confidence_policy.get("require_sparse_rest_checks"):
            sparse_threshold = int(confidence_policy.get("sparse_event_threshold", 1) or 1)
            sparse_groups: dict[tuple, list[dict]] = defaultdict(list)
            for note in plan.get("notes", []):
                key = (note.get("page"), note.get("measure_index"), note.get("hand"))
                sparse_groups[key].append(note)
            for (page, measure, hand), members in sorted(sparse_groups.items(), key=lambda item: str(item[0])):
                event_count = len({
                    (member.get("event_index"), member.get("chord_id"))
                    for member in members
                })
                if event_count > sparse_threshold:
                    continue
                if all(member.get("sparse_symbol_verified") is True for member in members):
                    continue
                errors.append(
                    f"page {page} measure {measure} {hand}: sparse region has {event_count} candidate event(s) "
                    "without explicit note-vs-rest visual verification"
                )

        required_passes = int(confidence_policy.get("require_independent_passes", 0) or 0)
        if required_passes:
            missing_by_scope: dict[tuple, list[str]] = defaultdict(list)
            for note in plan.get("notes", []):
                if int(note.get("recognition_passes", 0) or 0) < required_passes:
                    key = (note.get("page"), note.get("measure_index"), note.get("hand"))
                    missing_by_scope[key].append(str(note.get("note_id", "unknown")))
            for (page, measure, hand), note_ids in sorted(missing_by_scope.items(), key=lambda item: str(item[0])):
                errors.append(
                    f"page {page} measure {measure} {hand}: {len(note_ids)} note(s) have fewer than "
                    f"{required_passes} independent recognition passes"
                )

        if confidence_policy.get("require_same_position_evidence"):
            by_stream: dict[tuple, list[dict]] = defaultdict(list)
            for note in plan.get("notes", []):
                if int(note.get("chord_size", 1) or 1) != 1:
                    continue
                key = (
                    note.get("page"), note.get("measure_index"), note.get("hand"),
                    note.get("staff"), note.get("voice"),
                )
                by_stream[key].append(note)
            for key, stream in by_stream.items():
                stream.sort(key=lambda item: (float(item.get("onset", 0)), float(item.get("page_x", 0))))
                for previous, current in zip(stream, stream[1:]):
                    if abs(float(current.get("page_y", 0)) - float(previous.get("page_y", 0))) > 1.5:
                        continue
                    if not 0 < float(current.get("page_x", 0)) - float(previous.get("page_x", 0)) <= 45:
                        continue
                    if previous.get("same_position_verified") and current.get("same_position_verified"):
                        continue
                    relation = "same-pitch repetition/tie" if previous.get("pitch_midi") == current.get("pitch_midi") else "local-accidental pair"
                    errors.append(
                        f"page {key[0]} measure {key[1]} {key[2]}: {previous.get('note_id')} -> "
                        f"{current.get('note_id')} is a close same-position {relation} without explicit visual evidence"
                    )

        dense_threshold = int(confidence_policy.get("dense_notehead_threshold", 0) or 0)
        if confidence_policy.get("require_dense_event_checks") and dense_threshold > 0:
            verified_checks = {
                (int(check.get("page", 0)), int(check.get("measure", 0)), str(check.get("hand", "")))
                for check in recognition.get("event_count_checks", [])
                if check.get("verified") is True
            }
            dense_counts: dict[tuple, int] = defaultdict(int)
            for note in plan.get("notes", []):
                key = (int(note.get("page", 0)), int(note.get("measure_index", 0)), str(note.get("hand", "")))
                dense_counts[key] += 1
            for key, count in sorted(dense_counts.items()):
                if count >= dense_threshold and key not in verified_checks:
                    errors.append(
                        f"page {key[0]} measure {key[1]} {key[2]}: dense region has {count} noteheads "
                        "but no independently verified event_count_check"
                    )

    for group_id, members in tie_groups.items():
        members.sort(key=lambda item: (int(item.get("measure_index", 0)), float(item.get("onset", 0))))
        if len(members) < 2:
            errors.append(f"tie_group {group_id}: must contain at least two notes")
            continue
        pitches = {int(note["pitch_midi"]) for note in members}
        hands = {str(note.get("hand")) for note in members}
        if len(pitches) != 1 or len(hands) != 1:
            errors.append(f"tie_group {group_id}: tied notes must preserve pitch and hand")
        if not members[0].get("tie_start") or not members[-1].get("tie_stop"):
            errors.append(f"tie_group {group_id}: first note needs tie_start and last note needs tie_stop")
        if visual and strict and confidence_policy.get("require_tie_evidence"):
            if not all(note.get("tie_evidence") in {"visual_slur", "visual_tie", "source_semantic"} for note in members):
                errors.append(f"tie_group {group_id}: visual tie needs explicit tie_evidence on every member")

    # A global total can still pass when a visual system contains one invented
    # notehead and another system contains one omission.  Optional manually
    # verified local counts therefore act as hard gates for dense or disputed
    # regions.
    for index, check in enumerate(recognition.get("event_count_checks", [])):
        try:
            page = int(check["page"])
            measure = int(check["measure"])
            hand = str(check["hand"])
            expected_noteheads = int(check["expected_noteheads"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"recognition.event_count_checks[{index}] is incomplete")
            continue
        actual = sum(
            1 for note in plan.get("notes", [])
            if int(note.get("page", 0)) == page
            and int(note.get("measure_index", 0)) == measure
            and str(note.get("hand")) == hand
        )
        if actual != expected_noteheads:
            errors.append(
                f"page {page} measure {measure} {hand}: visually verified {expected_noteheads} "
                f"noteheads, but plan contains {actual}"
            )

    expected = recognition.get("expected_note_count")
    unresolved = int(recognition.get("unresolved_note_count", 0) or 0)
    if strict and expected is not None and int(expected) != len(plan.get("notes", [])) + unresolved:
        errors.append("recognition note count does not reconcile with expected_note_count")
    if unresolved:
        warnings.append(f"{unresolved} score facts remain unresolved")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--allow-review", action="store_true", help="report missing gates as warnings instead of generation blockers")
    parser.add_argument(
        "--max-errors", type=int, default=30,
        help="print at most this many errors, then print an omitted-count summary (default: 30)",
    )
    args = parser.parse_args()
    if args.max_errors < 1:
        raise ValueError("--max-errors must be at least 1")
    plan = load_plan(args.plan)
    errors, warnings = validate_recognition(plan, strict=not args.allow_review)
    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    for error in errors[:args.max_errors]:
        print(f"ERROR: {error}", file=sys.stderr)
    if len(errors) > args.max_errors:
        print(
            f"ERROR: {len(errors) - args.max_errors} additional issue(s) omitted; "
            "inspect the review queue and repair the listed page/measure/hand scopes first.",
            file=sys.stderr,
        )
    if errors:
        return 1
    print(f"Recognition gate passed for {len(plan.get('notes', []))} notes.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
