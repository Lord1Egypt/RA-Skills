#!/usr/bin/env python3
"""Validate unified piano fingering data and flag musical review points."""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

from plan_io import (
    COORDINATE_UNITS,
    HAND_SIZES,
    finite_number,
    load_plan,
    note_sort_key,
    page_map,
)
from validate_recognition import validate_recognition


REQUIRED = {
    "note_id", "part", "measure", "measure_index", "staff", "voice",
    "onset", "duration", "pitch_midi", "event_index", "chord_id",
    "chord_row", "chord_size", "hand", "keyboard_x_cm",
}
TRANSITIONS = {
    "same_position", "thumb_under", "finger_over", "lateral_shift",
    "substitution", "repeated_note", "chord_change", "leap",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--require-coordinates", action="store_true")
    parser.add_argument("--require-verified-anchors", action="store_true")
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="reject any score note that does not have a final finger 1..5",
    )
    args = parser.parse_args()
    plan = load_plan(args.plan)
    errors: list[str] = []
    warnings: list[str] = []
    recognition_errors, recognition_warnings = validate_recognition(plan, strict=True)
    errors.extend(f"recognition gate: {message}" for message in recognition_errors)
    warnings.extend(f"recognition gate: {message}" for message in recognition_warnings)
    pages = page_map(plan)
    source = plan.get("source", {})
    source_type = source.get("type")
    unit = source.get("coordinate_unit")
    require_coordinates = args.require_coordinates or args.require_verified_anchors or source_type in {"pdf", "image"}
    if require_coordinates and unit not in COORDINATE_UNITS:
        errors.append("source.coordinate_unit must be pdf_point or pixel_top_left")

    settings = plan.get("settings", {})
    if str(settings.get("hand_size", "M")).upper() not in HAND_SIZES:
        errors.append("settings.hand_size must be XXS..XXL")
    lookahead = int(settings.get("lookahead", 0))
    if lookahead not in {0, 3, 4, 5, 6, 7, 8, 9}:
        errors.append("settings.lookahead must be 0 or 3..9")

    notes = plan.get("notes", [])
    if not notes:
        errors.append("notes must be a non-empty array")
    seen_ids: set[str] = set()
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    label_boxes: dict[int, list[tuple[float, float, float, float, str, tuple]]] = defaultdict(list)
    for index, note in enumerate(notes):
        if not isinstance(note, dict):
            errors.append(f"notes[{index}] must be an object")
            continue
        missing = sorted(REQUIRED - set(note))
        if missing:
            errors.append(f"notes[{index}] missing {missing}")
            continue
        note_id = str(note["note_id"])
        if not note_id or note_id in seen_ids:
            errors.append(f"notes[{index}] duplicate/empty note_id {note_id!r}")
        seen_ids.add(note_id)
        hand = str(note["hand"]).upper()
        if hand not in {"RH", "LH"}:
            errors.append(f"{note_id}: hand must be RH or LH")
            continue
        grouped[(str(note["part"]), hand)].append(note)
        try:
            pitch = int(note["pitch_midi"])
            finger = int(note.get("finger", 0))
            chord_row = int(note["chord_row"])
            chord_size = int(note["chord_size"])
            duration = finite_number(note["duration"], f"{note_id}.duration")
            finite_number(note["keyboard_x_cm"], f"{note_id}.keyboard_x_cm")
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not 0 <= pitch <= 127 or duration < 0:
            errors.append(f"{note_id}: invalid pitch or duration")
        if finger not in {0, 1, 2, 3, 4, 5}:
            errors.append(f"{note_id}: finger must be 0..5")
        if finger == 0:
            message = f"{note_id}: score note has no final finger"
            if args.require_complete:
                errors.append(message)
            elif note.get("source") in {"generated", "reviewed", "existing"}:
                warnings.append(message)
        if not 0 <= chord_row < chord_size:
            errors.append(f"{note_id}: chord_row must be within chord_size")
        placement = note.get("placement")
        if placement not in {"above", "below"}:
            errors.append(f"{note_id}: placement must be above or below")
        if hand == "RH" and placement != "above":
            warnings.append(f"{note_id}: review non-default RH placement")
        if hand == "LH" and placement != "below":
            warnings.append(f"{note_id}: review non-default LH placement")
        transition = note.get("transition_type")
        if transition is not None and transition not in TRANSITIONS:
            errors.append(f"{note_id}: invalid transition_type {transition!r}")
        if require_coordinates:
            try:
                pageno = int(note["page"])
                x = finite_number(note["page_x"], f"{note_id}.page_x")
                y = finite_number(note["page_y"], f"{note_id}.page_y")
                page = pages[pageno]
                width = finite_number(page["width"], f"page {pageno}.width")
                height = finite_number(page["height"], f"page {pageno}.height")
                if not (0 <= x <= width and 0 <= y <= height):
                    errors.append(f"{note_id}: page anchor outside page bounds")
                label_x = finite_number(note.get("label_x", x), f"{note_id}.label_x")
                offset = finite_number(note.get("label_offset", 20), f"{note_id}.label_offset")
                size = finite_number(note.get("font_size", 10), f"{note_id}.font_size")
                if size <= 0 or offset < 0:
                    errors.append(f"{note_id}: invalid label size/offset")
                if unit == "pixel_top_left":
                    label_y = y - offset if placement == "above" else y + offset
                else:
                    label_y = y + offset if placement == "above" else y - offset
                half_width = size * 0.35
                box = (label_x - half_width, label_y - size * 0.4, label_x + half_width, label_y + size * 0.7, note_id)
                if not (0 <= box[0] and box[2] <= width and 0 <= box[1] and box[3] <= height):
                    errors.append(f"{note_id}: label falls outside page bounds")
                event_key = (str(note["part"]), int(note["measure_index"]), float(note["onset"]), int(note["event_index"]), str(note["chord_id"]), hand)
                label_boxes[pageno].append((*box, event_key))
                if args.require_verified_anchors:
                    if note.get("anchor_verified") is not True:
                        errors.append(f"{note_id}: page anchor has not passed visual notehead verification")
                    if note.get("anchor_method") not in {"visual_notehead", "detected_notehead", "layout_source", "manual_visual_anchor_review"}:
                        errors.append(f"{note_id}: missing valid anchor_method")
            except (KeyError, TypeError, ValueError) as exc:
                errors.append(f"{note_id}: invalid/missing page coordinate ({exc})")

    for pageno, boxes in label_boxes.items():
        for index, first in enumerate(boxes):
            for second in boxes[index + 1:]:
                if first[5] == second[5]:
                    continue
                overlaps = first[0] < second[2] and first[2] > second[0] and first[1] < second[3] and first[3] > second[1]
                if overlaps:
                    errors.append(f"page {pageno}: label collision between {first[4]} and {second[4]}")

    for (_, hand), sequence in grouped.items():
        sequence.sort(key=note_sort_key)
        events: dict[tuple, list[dict]] = defaultdict(list)
        for note in sequence:
            key = (note["measure_index"], float(note["onset"]), note["event_index"], note["chord_id"])
            events[key].append(note)
        ordered_events = []
        for key in sorted(events):
            members = sorted(events[key], key=lambda n: int(n["pitch_midi"]))
            pitches = [int(n["pitch_midi"]) for n in members]
            fingers = [int(n.get("finger", 0)) for n in members]
            if any(int(n["chord_size"]) != len(members) for n in members):
                errors.append(f"{hand} event {key}: inconsistent chord_size")
            if [int(n["chord_row"]) for n in members] != list(range(len(members))):
                errors.append(f"{hand} event {key}: chord_row must be low-to-high from 0")
            if len(pitches) != len(set(pitches)):
                errors.append(
                    f"{hand} event {key}: duplicate simultaneous pitch must be merged or manually resolved "
                    "before fingering"
                )
            assigned = [f for f in fingers if f]
            if len(assigned) != len(set(assigned)):
                errors.append(f"{hand} event {key}: chord reuses a finger")
            if len(assigned) == len(members) and len(members) > 1:
                expected = sorted(assigned, reverse=hand == "LH")
                if assigned != expected:
                    errors.append(f"{hand} event {key}: fingers conflict with pitch order")
            ordered_events.append(members)

        for pair_index, (previous_event, current_event) in enumerate(zip(ordered_events, ordered_events[1:])):
            detached = any(note.get("connection") == "detached" for note in current_event)
            detached = detached or any(note.get("transition_type") == "leap" for note in current_event)
            if detached or {len(previous_event), len(current_event)} != {1, 2}:
                continue
            single_event, chord_event = (
                (previous_event, current_event) if len(previous_event) == 1 else (current_event, previous_event)
            )
            single = single_event[0]
            single_pitch = int(single["pitch_midi"])
            chord_pitches = [int(note["pitch_midi"]) for note in chord_event]
            nearest = min(chord_event, key=lambda note: abs(int(note["pitch_midi"]) - single_pitch))
            outside = single_pitch < min(chord_pitches) or single_pitch > max(chord_pitches)
            outer_side = (hand == "LH" and single_pitch < min(chord_pitches)) or (
                hand == "RH" and single_pitch > max(chord_pitches)
            )
            # The 5 -> 3-1 guard applies to an actual outer-bass/top-note
            # landing, not to the middle note of a scalar/arpeggiated run
            # which happens to precede a dyad.  Require a local extreme on the
            # open side before declaring the finger mechanically reserved.
            context_event = ordered_events[pair_index - 1] if pair_index else None
            if context_event and outer_side:
                context_pitches = [int(note["pitch_midi"]) for note in context_event]
                if hand == "LH" and single_pitch > min(context_pitches):
                    outer_side = False
                elif hand == "RH" and single_pitch < max(context_pitches):
                    outer_side = False
            same_finger = int(single.get("finger", 0)) == int(nearest.get("finger", 0)) != 0
            close_shift = abs(int(nearest["pitch_midi"]) - single_pitch) <= 4
            verified_exception = single.get("exception_verified") is True
            if outer_side and int(single.get("finger", 0)) not in {0, 5} and not verified_exception:
                errors.append(
                    f"{single['note_id']}: outer accompaniment note must use finger 5 before/after "
                    "the adjacent dyad, or carry an exception_verified justification"
                )
            chord_span = max(chord_pitches) - min(chord_pitches)
            wide_dyad_reset = (
                len(chord_event) == 2
                and chord_span >= 7
                and nearest.get("transition_type") == "chord_change"
            )
            # In an accompaniment cell such as C -> D-A, the LH may release
            # finger 5 from the bass and reset it on the low member of a
            # fifth (5-1).  This is a chord-position reset, not an attempted
            # legato reuse on a melodic single-note line.  Keep the narrow
            # dyad guard intact: thirds and fourths still require the normal
            # 3-1 / 4-1 checks below.
            if outside and outer_side and same_finger and close_shift and not wide_dyad_reset:
                errors.append(
                    f"{nearest['note_id']}: finger {nearest['finger']} is reused for a nearby "
                    "single note and the adjacent dyad"
                )

        # In a beginner-style LH broken-chord cell, a nearby outer bass plus a
        # minor/major-third dyad is not a free-standing chord.  It is one hand
        # position.  Rejecting 4-1 here prevents a later repair from widening
        # the standard 5 -> 3-1 motion just to satisfy a local transition.
        if hand == "LH":
            for index, event in enumerate(ordered_events):
                if len(event) != 2:
                    continue
                low, high = event
                span = int(high["pitch_midi"]) - int(low["pitch_midi"])
                if span not in {3, 4}:
                    continue
                neighbours = ordered_events[max(0, index - 1):index] + ordered_events[index + 1:index + 2]
                has_outer_bass = any(
                    len(candidate) == 1 and int(candidate[0]["pitch_midi"]) < int(low["pitch_midi"])
                    for candidate in neighbours
                )
                verified_exception = any(note.get("exception_verified") is True for note in event)
                fingers = [int(low.get("finger", 0)), int(high.get("finger", 0))]
                if not all(finger in {1, 2, 3, 4, 5} for finger in fingers):
                    continue
                if has_outer_bass and fingers != [3, 1] and not verified_exception:
                    errors.append(
                        f"{low['note_id']}, {high['note_id']}: LH third in an outer-bass broken-chord "
                        "cell must use 3-1, or carry an exception_verified justification"
                    )

        adjacent_singles = [
            (previous_event[0], current_event[0])
            for previous_event, current_event in zip(ordered_events, ordered_events[1:])
            if len(previous_event) == 1 and len(current_event) == 1
        ]
        for previous, current in adjacent_singles:
            pf, cf = int(previous.get("finger", 0)), int(current.get("finger", 0))
            if not pf or not cf:
                continue
            pd = int(current["pitch_midi"]) - int(previous["pitch_midi"])
            detached = current.get("connection") == "detached" or current.get("transition_type") == "leap"
            # Replaying the same connected key normally keeps the same finger.
            # A change is possible, but it is a deliberate substitution or a
            # repeated-note technique and must be declared instead of silently
            # appearing as a solver artefact.
            same_pitch_exception = current.get("transition_type") in {"repeated_note", "substitution"}
            previous_end = float(previous["onset"]) + float(previous.get("duration", 0))
            directly_connected = float(current["onset"]) <= previous_end + 1.0e-6
            if not pd and directly_connected and pf != cf and not detached and not same_pitch_exception:
                errors.append(
                    f"{current['note_id']}: connected repeated pitch changes finger without an explicit "
                    "repeated_note/substitution reason"
                )
            if pd and pf == cf and not detached:
                errors.append(f"{current['note_id']}: same finger moves to connected different pitch")
            fd = cf - pf
            reversal = pd * fd * (1 if hand == "RH" else -1) < 0
            exceptional = current.get("transition_type") in {"thumb_under", "finger_over", "lateral_shift", "substitution", "leap"}
            if pd and fd and reversal and not exceptional:
                warnings.append(f"{current['note_id']}: directional reversal needs review")
            if cf == 1 and int(current["pitch_midi"]) % 12 in {1, 3, 6, 8, 10}:
                warnings.append(f"{current['note_id']}: review thumb on black key")

        # Repeated accompaniment positions should not silently change fingers.
        # Alternation and substitution remain valid when they are explicitly
        # identified, but an unexplained change is a phrase-level review point.
        repeated_singles: dict[tuple[int, int], list[dict]] = defaultdict(list)
        event_sizes = {
            (int(event[0]["measure_index"]), int(event[0]["event_index"])): len(event)
            for event in ordered_events
        }
        for event in ordered_events:
            if hand == "LH" and len(event) == 1:
                note = event[0]
                repeated_singles[(int(note["measure_index"]), int(note["pitch_midi"]))].append(note)
        for same_pitch_notes in repeated_singles.values():
            fingers = {int(note.get("finger", 0)) for note in same_pitch_notes if int(note.get("finger", 0))}
            intentional = any(
                note.get("transition_type") in {"repeated_note", "substitution"}
                for note in same_pitch_notes
            )
            event_indices = sorted(int(note["event_index"]) for note in same_pitch_notes)
            measure = int(same_pitch_notes[0]["measure_index"])
            same_accompaniment_slot = any(
                b - a == 3
                and any(event_sizes.get((measure, middle), 1) > 1 for middle in (a + 1, a + 2))
                for a, b in zip(event_indices, event_indices[1:])
            )
            if len(fingers) > 1 and same_accompaniment_slot and not intentional:
                ids = ", ".join(str(note["note_id"]) for note in same_pitch_notes)
                errors.append(f"{ids}: repeated accompaniment pitch changes finger without an explicit reason")

        # A complete repeated LH accompaniment cell must preserve its whole
        # hand shape across measures.  The older guard above only sees copies
        # inside one measure; that missed the common case where the same
        # bass--dyad--dyad figure reappears several bars later with one finger
        # silently changed.  Limit this to identical multi-event measures with
        # both a single bass and a chord, so scalar passages and deliberate
        # phrase changes are not treated as accompaniment repetitions.
        if hand == "LH":
            measures: dict[int, list[list[dict]]] = defaultdict(list)
            for event in ordered_events:
                measures[int(event[0]["measure_index"])].append(event)
            prior_patterns: dict[tuple, tuple[int, tuple, list[list[dict]]]] = {}
            for measure, measure_events in sorted(measures.items()):
                if len(measure_events) < 3 or not any(len(event) == 1 for event in measure_events) or not any(len(event) > 1 for event in measure_events):
                    continue
                pitch_pattern = tuple(
                    tuple(int(note["pitch_midi"]) for note in event)
                    for event in measure_events
                )
                finger_pattern = tuple(
                    tuple(int(note.get("finger", 0)) for note in event)
                    for event in measure_events
                )
                if any(not finger for event in finger_pattern for finger in event):
                    continue
                intentional = any(
                    note.get("exception_verified") is True
                    or note.get("transition_type") in {"repeated_note", "substitution"}
                    for event in measure_events for note in event
                )
                previous = prior_patterns.get(pitch_pattern)
                if previous is not None:
                    prior_measure, prior_fingers, prior_events = previous
                    prior_intentional = any(
                        note.get("exception_verified") is True
                        or note.get("transition_type") in {"repeated_note", "substitution"}
                        for event in prior_events for note in event
                    )
                    if finger_pattern != prior_fingers and not intentional and not prior_intentional:
                        ids = ", ".join(str(note["note_id"]) for event in measure_events for note in event)
                        # Repeated notation can still require a different
                        # hand position because of the preceding/following
                        # phrase.  Flag it prominently, but do not reject an
                        # otherwise playable plan merely for differing from a
                        # repeated visual pattern.
                        warnings.append(
                            f"{ids}: LH accompaniment pattern repeats measure {prior_measure} in measure {measure} "
                            "but changes fingers without an explicit reason; review phrase-level hand position"
                        )
                else:
                    prior_patterns[pitch_pattern] = (measure, finger_pattern, measure_events)

        # Literal repetitions are a higher-level usability invariant for both
        # hands.  The event grouping, pitches and durations must all match;
        # transposed sequences and merely similar contours are intentionally
        # outside this check.  A solver may choose another valid local hand
        # position, but it must record an explicit editorial exception rather
        # than silently changing a repeated exercise or melody cell.
        measures: dict[int, list[list[dict]]] = defaultdict(list)
        for event in ordered_events:
            measures[int(event[0]["measure_index"])].append(event)
        prior_motifs: dict[tuple, tuple[int, tuple, list[list[dict]]]] = {}
        for measure, measure_events in sorted(measures.items()):
            motif = tuple(
                tuple(
                    (int(note["pitch_midi"]), round(float(note.get("duration", 0)), 6))
                    for note in event
                )
                for event in measure_events
            )
            finger_pattern = tuple(
                tuple(int(note.get("finger", 0)) for note in event)
                for event in measure_events
            )
            prior = prior_motifs.get(motif)
            if prior is None:
                prior_motifs[motif] = (measure, finger_pattern, measure_events)
                continue
            prior_measure, prior_fingers, prior_events = prior
            if finger_pattern == prior_fingers:
                continue
            notes = [note for event in measure_events for note in event] + [note for event in prior_events for note in event]
            exception = any(
                note.get("exception_verified") is True
                or note.get("transition_type") == "substitution"
                for note in notes
            )
            if not exception:
                ids = ", ".join(str(note["note_id"]) for event in measure_events for note in event)
                errors.append(
                    f"{ids}: identical measure motif repeats measure {prior_measure} with different fingers "
                    "without an explicit verified exception"
                )

        tied: dict[str, list[dict]] = defaultdict(list)
        for note in sequence:
            if note.get("tie_group"):
                tied[str(note["tie_group"])].append(note)
        for group_id, members in tied.items():
            members.sort(key=note_sort_key)
            fingers = {int(note.get("finger", 0)) for note in members if int(note.get("finger", 0))}
            substitutions = [
                note for note in members
                if note.get("transition_type") == "substitution" and note.get("exception_verified") is True
            ]
            if len(fingers) > 1 and not substitutions:
                ids = ", ".join(str(note["note_id"]) for note in members)
                errors.append(f"{ids}: tie group {group_id} changes finger without a verified substitution")

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"Validated {len(notes)} notes; {len(warnings)} review warning(s).")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
