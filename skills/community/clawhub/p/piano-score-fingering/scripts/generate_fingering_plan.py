#!/usr/bin/env python3
"""Generate piano fingering in a unified plan with the bundled solver."""

from __future__ import annotations

import argparse
import copy
import math
import sys
import time
from collections import defaultdict
from itertools import combinations
from pathlib import Path

from fingering_core import Hand, INote
from plan_io import load_plan, note_sort_key, save_plan
from validate_recognition import validate_recognition


CHORD_PATTERNS = {
    1: [1],
    3: [1, 3, 5],
    4: [1, 2, 4, 5],
    5: [1, 2, 3, 4, 5],
}

# One-octave major-scale templates.  These are intentionally limited to an
# unambiguous eight-note diatonic octave; they do not try to guess a key from
# a fragment.  The reference patterns are standard technical fingerings and
# prevent the local geometric search from placing the thumb on an unsuitable
# black-key crossing in beginner-scale passages.
MAJOR_SCALE_PATTERNS = {
    0: ("12312345", "54321321"),   # C
    1: ("23123412", "32143213"),   # Db / C#
    2: ("12312345", "54321321"),   # D
    3: ("31234123", "32143213"),   # Eb / D#
    4: ("12312345", "54321321"),   # E
    5: ("12341234", "54321321"),   # F
    6: ("23412312", "43213214"),   # Gb / F#
    7: ("12312345", "54321321"),   # G
    8: ("34123123", "32143213"),   # Ab / G#
    9: ("12312345", "54321321"),   # A
    10: ("41231234", "32143213"),  # Bb / A#
    11: ("12312345", "43214321"),  # B / Cb
}
MAJOR_STEPS = (0, 2, 4, 5, 7, 9, 11, 12)
DESCENDING_MAJOR_STEPS = tuple(12 - step for step in reversed(MAJOR_STEPS))


def parse_measure_range(value: str) -> tuple[int, int]:
    parts = value.split("-", 1)
    try:
        start = int(parts[0])
        end = int(parts[1]) if len(parts) == 2 else start
    except ValueError as exc:
        raise argparse.ArgumentTypeError("measure range must be N or START-END") from exc
    if start < 1 or end < start:
        raise argparse.ArgumentTypeError("measure range must satisfy 1 <= START <= END")
    return start, end


def chord_pattern(members: list[dict], hand_code: str) -> list[int]:
    """Choose an ordered chord shape whose finger span matches its pitch span."""
    if len(members) == 2:
        semitones = abs(int(members[1]["pitch_midi"]) - int(members[0]["pitch_midi"]))
        if semitones <= 2:
            pattern = [1, 2]
        elif semitones <= 4:
            pattern = [1, 3]
        elif semitones <= 5:
            pattern = [1, 4]
        else:
            pattern = [1, 5]
    else:
        pattern = CHORD_PATTERNS[len(members)]
        if len(members) == 3 and hand_code == "RH":
            pitches = [int(member["pitch_midi"]) for member in members]
            # A close lower third with a wide upper sixth is more balanced as
            # 1-2-5 than 1-3-5.  The second finger keeps the middle voice near
            # the thumb and leaves the full upper reach to finger 5.
            if (pitches[1] - pitches[0], pitches[2] - pitches[1]) == (3, 6):
                pattern = [1, 2, 5]
    return list(reversed(pattern)) if hand_code == "LH" else pattern


def _mark_reviewed(record: dict, finger: int, reason: str, transition: str = "lateral_shift") -> None:
    record["finger"] = finger
    record["source"] = "reviewed"
    record["transition_type"] = transition
    record["exception_reason"] = reason


def _single_event_runs(records: list[dict]) -> list[list[dict]]:
    """Return continuous monophonic event runs without crossing chord/rest boundaries."""
    events: dict[tuple, list[dict]] = defaultdict(list)
    for record in records:
        events[(record["measure_index"], record["onset"], record["event_index"], record["chord_id"])].append(record)
    ordered = [sorted(event, key=lambda item: int(item["pitch_midi"])) for _, event in sorted(events.items())]
    runs: list[list[dict]] = []
    current: list[dict] = []
    for event in ordered:
        note = event[0] if len(event) == 1 else None
        prior = current[-1] if current else None
        continuous = bool(note and prior)
        if continuous:
            if note.get("preceding_rest") or note.get("connection") == "detached":
                continuous = False
            else:
                end = float(prior["onset"]) + float(prior.get("duration", 0))
                continuous = float(note["onset"]) <= end + 1.0e-6
        if not continuous:
            if current:
                runs.append(current)
            current = []
        if note:
            current.append(note)
    if current:
        runs.append(current)
    return runs


def _phrase_transition_cost(previous: dict, current: dict, fa: int, fb: int, hand_code: str, frest: list[float | None]) -> float:
    """Physical pair cost used by the global single-line phrase solver."""
    pitch_delta = int(current["pitch_midi"]) - int(previous["pitch_midi"])
    if pitch_delta == 0:
        return 0.0 if fa == fb else 1000.0
    # Reuse the solver's mirrored LH geometry without mutating score records.
    direction = 1.0 if hand_code == "RH" else -1.0
    previous_x = direction * float(previous["keyboard_x_cm"])
    current_x = direction * float(current["keyboard_x_cm"])
    rest_a, rest_b = frest[fa], frest[fb]
    if rest_a is None or rest_b is None:
        return 1.0e6
    expected = previous_x + (rest_b - rest_a)
    elapsed = max(0.1, abs(float(current["onset"]) - float(previous["onset"])) + 0.1)
    movement = abs(current_x - expected) / elapsed
    if int(current["pitch_midi"]) % 12 in {1, 3, 6, 8, 10}:
        movement /= {1: 0.3, 2: 1.0, 3: 1.1, 4: 0.8, 5: 0.7}[fb]
    # Moving naturally through adjacent fingers is cheap; a crossing is allowed
    # but must be prepared.  This mirrors the local solver's rules while the DP
    # sees the entire connected phrase rather than a rolling window.
    natural = 1 if (pitch_delta > 0) == (hand_code == "RH") else -1
    finger_delta = fb - fa
    penalty = 0.0
    if finger_delta * natural > 0:
        penalty += max(0, abs(finger_delta) - 1) * 2.0
    elif fb != 1 and fa != 1:
        penalty += 2.5 + abs(finger_delta) * 0.4
    stepwise = abs(pitch_delta) <= 2
    thumb_under = fb == 1 and fa > 1 and finger_delta * natural < 0
    finger_over = fa == 1 and fb > 1 and finger_delta * natural < 0
    if stepwise and thumb_under:
        penalty += {2: 7.0, 3: 0.15, 4: 0.8, 5: 3.5}[fa]
    elif stepwise and finger_over:
        penalty += {2: 1.2, 3: 0.15, 4: 0.7, 5: 3.0}[fb]
    return movement + penalty


def optimize_connected_melody(records: list[dict], hand_code: str, hand_size: str) -> None:
    """Globally optimize generic connected single-note phrases.

    The historical solver commits one event at a time and carries only the next
    predicted finger.  That is fast, but it can choose a phrase entry that is
    locally cheap and awkward several notes later.  This pass only replaces a
    complete unanchored monophonic run when a whole-run dynamic programme has a
    strictly lower physical cost.  Chords, rests, ties and any reviewed/source
    anchors remain outside its scope.
    """
    size_factor = Hand.size_factor(hand_size)
    frest: list[float | None] = [None, -7.0 * size_factor, -2.8 * size_factor, 0.0,
                                  2.8 * size_factor, 5.6 * size_factor]
    for phrase in _single_event_runs(records):
        if len(phrase) < 4 or len(phrase) > 64:
            continue
        if any(note.get("locked") or note.get("tie_group") or note.get("review_decision") for note in phrase):
            continue
        costs: list[dict[int, tuple[float, list[int]]]] = []
        first: dict[int, tuple[float, list[int]]] = {}
        # A sustained stepwise phrase normally enters with the outer available
        # finger.  This is a soft start cost, not a scale-specific template.
        deltas = [int(phrase[index]["pitch_midi"]) - int(phrase[index - 1]["pitch_midi"])
                  for index in range(1, min(4, len(phrase)))]
        same_direction = bool(deltas) and (all(delta > 0 for delta in deltas) or all(delta < 0 for delta in deltas))
        stepwise = same_direction and all(abs(delta) <= 2 for delta in deltas)
        preferred = 0
        if stepwise:
            preferred = 1 if (deltas[0] > 0) == (hand_code == "RH") else 5
        for finger in range(1, 6):
            first[finger] = (0.0 if not preferred or finger == preferred else 6.0, [finger])
        costs.append(first)
        for index in range(1, len(phrase)):
            current: dict[int, tuple[float, list[int]]] = {}
            for finger in range(1, 6):
                candidates = []
                for previous_finger, (prior_cost, prior_path) in costs[-1].items():
                    value = prior_cost + _phrase_transition_cost(
                        phrase[index - 1], phrase[index], previous_finger, finger, hand_code, frest
                    )
                    candidates.append((value, prior_path + [finger]))
                current[finger] = min(candidates, key=lambda item: (item[0], item[1]))
            costs.append(current)
        global_cost, global_path = min(costs[-1].values(), key=lambda item: (item[0], item[1]))
        local_path = [int(note.get("finger", 0)) for note in phrase]
        if any(finger not in {1, 2, 3, 4, 5} for finger in local_path):
            continue
        local_cost = sum(
            _phrase_transition_cost(phrase[index - 1], phrase[index], local_path[index - 1], local_path[index], hand_code, frest)
            for index in range(1, len(phrase))
        ) + (0.0 if not preferred or local_path[0] == preferred else 6.0)
        # Require a material improvement so a tie-break cannot silently rewrite
        # one textbook-valid phrase into another equally plausible option.
        if global_path == local_path or not math.isfinite(global_cost) or global_cost + 0.75 >= local_cost:
            continue
        for note, finger in zip(phrase, global_path):
            if int(note.get("finger", 0)) == finger:
                continue
            transition = "thumb_under" if finger == 1 else (
                "finger_over" if int(note.get("finger", 0)) == 1 else "lateral_shift"
            )
            _mark_reviewed(note, finger, "global connected-phrase optimisation improved whole-phrase physical cost", transition)


def repair_repeated_triplets(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Use the stable outer-middle-thumb shape for repeated wide descending triplets."""
    singles = [event[0] for event in ordered_events if len(event) == 1]
    by_measure: dict[int, list[dict]] = defaultdict(list)
    for note in singles:
        by_measure[int(note["measure_index"])].append(note)
    for notes in by_measure.values():
        notes.sort(key=note_sort_key)
        if len(notes) < 6:
            continue
        pattern = [5, 3, 1] if hand_code == "RH" else [1, 3, 5]
        # Scan repeated six-note windows instead of requiring the entire
        # measure length to be divisible by three. A pickup or resolution note
        # after two triplets must not disable recognition of the repeated cell.
        for start in range(len(notes) - 5):
            first = notes[start:start + 3]
            second = notes[start + 3:start + 6]

            def intervals(group: list[dict]) -> tuple[int, int] | None:
                pitches = [int(note["pitch_midi"]) for note in group]
                if not pitches[0] > pitches[1] > pitches[2]:
                    return None
                gaps = (pitches[0] - pitches[1], pitches[1] - pitches[2])
                if min(gaps) < 3 or sum(gaps) < 7:
                    return None
                return gaps

            first_intervals = intervals(first)
            second_intervals = intervals(second)
            if first_intervals is None or first_intervals != second_intervals:
                continue
            transpositions = {
                int(b["pitch_midi"]) - int(a["pitch_midi"])
                for a, b in zip(first, second)
            }
            if len(transpositions) != 1 or any(note.get("locked") for note in first + second):
                continue
            for group in (first, second):
                for note, finger in zip(group, pattern):
                    if int(note.get("finger", 0)) != finger:
                        _mark_reviewed(
                            note,
                            finger,
                            "wide repeated triplet uses outer-middle-thumb shape",
                        )


def repair_identical_measure_motifs(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Keep an exactly repeated notated measure in one fingering pattern.

    This is deliberately narrower than generic contour matching: only measures
    with identical pitches, event grouping and durations qualify.  A literal
    repeat is normally a request for one reusable hand shape; allowing a fresh
    local search to change it creates needlessly confusing beginner fingerings.
    Locked or explicitly substituted notes remain editorial exceptions.
    """
    by_measure: dict[int, list[list[dict]]] = defaultdict(list)
    for event in ordered_events:
        by_measure[int(event[0]["measure_index"])].append(event)
    canonical: dict[tuple, tuple[int, list[list[dict]]]] = {}
    for measure, events in sorted(by_measure.items()):
        signature = tuple(
            tuple(
                (int(note["pitch_midi"]), round(float(note.get("duration", 0)), 6))
                for note in event
            )
            for event in events
        )
        prior = canonical.get(signature)
        if prior is None:
            canonical[signature] = (measure, events)
            continue
        prior_measure, reference_events = prior
        notes = [note for event in events for note in event]
        reference_notes = [note for event in reference_events for note in event]
        if len(notes) != len(reference_notes):
            continue
        if any(note.get("locked") for note in notes + reference_notes):
            continue
        if any(
            note.get("exception_verified") is True
            or note.get("transition_type") == "substitution"
            for note in notes + reference_notes
        ):
            continue
        for current, reference in zip(notes, reference_notes):
            finger = int(reference.get("finger", 0))
            if finger not in {1, 2, 3, 4, 5}:
                break
        else:
            for current, reference in zip(notes, reference_notes):
                finger = int(reference["finger"])
                if int(current.get("finger", 0)) != finger:
                    _mark_reviewed(
                        current,
                        finger,
                        f"identical measure motif preserves the fingering of measure {prior_measure}",
                        "same_position",
                    )


def repair_repeated_accompaniment_pitch(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Keep the same finger for the repeated bass slot of an accompaniment cell."""
    if hand_code != "LH":
        return
    by_measure: dict[int, list[list[dict]]] = defaultdict(list)
    for event in ordered_events:
        by_measure[int(event[0]["measure_index"])].append(event)
    for events in by_measure.values():
        measure_floor = min(int(note["pitch_midi"]) for event in events for note in event)
        event_sizes = {int(event[0]["event_index"]): len(event) for event in events}
        singles = [event[0] for event in events if len(event) == 1]
        by_pitch: dict[int, list[dict]] = defaultdict(list)
        for note in singles:
            by_pitch[int(note["pitch_midi"])].append(note)
        for pitch, notes in by_pitch.items():
            if pitch != measure_floor:
                continue
            by_event = {int(note["event_index"]): note for note in notes}
            for event_index, first in list(by_event.items()):
                second = by_event.get(event_index + 3)
                if second is None:
                    continue
                if not any(event_sizes.get(middle, 1) > 1 for middle in (event_index + 1, event_index + 2)):
                    continue
                if any(note.get("transition_type") in {"substitution", "repeated_note"} for note in (first, second)):
                    continue
                locked = [note for note in (first, second) if note.get("locked")]
                if len(locked) == 2 and int(first.get("finger", 0)) != int(second.get("finger", 0)):
                    # Preserve source anchors; the validator will require review.
                    continue
                target = int(locked[0].get("finger", 0)) if locked else 5
                for note in (first, second):
                    if not note.get("locked") and int(note.get("finger", 0)) != target:
                        _mark_reviewed(
                            note,
                            target,
                            "same-pitch repeated bass slot keeps one stable finger",
                            "same_position",
                        )


def repair_tied_notes(ordered_events: list[list[dict]], hand_code: str) -> None:
    """A notated tie keeps one finger unless a verified substitution says otherwise."""
    groups: dict[str, list[dict]] = defaultdict(list)
    for event in ordered_events:
        for note in event:
            if note.get("tie_group"):
                groups[str(note["tie_group"])].append(note)
    for group_id, notes in groups.items():
        notes.sort(key=note_sort_key)
        locked = [note for note in notes if note.get("locked") and int(note.get("finger", 0))]
        if len({int(note["finger"]) for note in locked}) > 1:
            # Preserve source markings; the validator will reject the conflict.
            continue
        target = int(locked[0]["finger"]) if locked else int(notes[0].get("finger", 0) or 0)
        if not target:
            continue
        for note in notes:
            verified_substitution = (
                note.get("transition_type") == "substitution"
                and note.get("exception_verified") is True
            )
            if note.get("locked") or verified_substitution:
                continue
            if int(note.get("finger", 0)) != target:
                _mark_reviewed(
                    note,
                    target,
                    f"tie group {group_id} preserves one finger",
                    "same_position",
                )


def repair_connected_repeated_notes(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Keep a finger on a directly repeated connected single note.

    Repeated pitches separated by a rest or explicitly detached can legitimately
    alternate fingers.  By contrast, two touching/overlapping single-note
    events on the same key are a continuation unless the source explicitly
    requests a substitution.  Solver look-ahead must not silently change the
    digit in that situation.
    """
    del hand_code
    for previous_event, current_event in zip(ordered_events, ordered_events[1:]):
        if len(previous_event) != 1 or len(current_event) != 1:
            continue
        previous, current = previous_event[0], current_event[0]
        if current.get("preceding_rest"):
            continue
        if int(previous["pitch_midi"]) != int(current["pitch_midi"]):
            continue
        if current.get("connection") == "detached" or current.get("transition_type") in {"leap", "substitution"}:
            continue
        previous_end = float(previous["onset"]) + float(previous.get("duration", 0))
        if float(current["onset"]) > previous_end + 1.0e-6:
            continue
        prior_finger = int(previous.get("finger", 0) or 0)
        current_finger = int(current.get("finger", 0) or 0)
        if not prior_finger or prior_finger == current_finger:
            continue
        if current.get("locked"):
            # Do not overwrite an editorial instruction; validation reports a
            # conflict so the caller can decide whether it is an intentional
            # substitution.
            continue
        _mark_reviewed(
            current,
            prior_finger,
            "directly repeated connected pitch keeps the preceding finger",
            "repeated_note",
        )


def repair_complete_major_scales(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Apply a canonical pattern only to a complete, unambiguous octave scale.

    A local search is deliberately free to choose alternatives in normal music.
    An exact eight-note major octave is different: at beginner level it is a
    technical figure with established black-key-aware fingerings.  Treating it
    as eight unrelated intervals was the reason flat-key scales regressed.
    """
    singles = [(position, event[0]) for position, event in enumerate(ordered_events) if len(event) == 1]
    for window in zip(*[singles[offset:] for offset in range(8)]):
        positions = [position for position, _ in window]
        notes = [note for _, note in window]
        if positions != list(range(positions[0], positions[0] + 8)):
            continue
        pitches = [int(note["pitch_midi"]) for note in notes]
        direction = 1 if pitches[-1] > pitches[0] else -1
        intervals = tuple(direction * (pitch - pitches[0]) for pitch in pitches)
        expected_intervals = MAJOR_STEPS if direction > 0 else DESCENDING_MAJOR_STEPS
        if intervals != expected_intervals:
            continue
        root = pitches[0] % 12 if direction > 0 else pitches[-1] % 12
        tonal_fifths = {note.get("key_fifths") for note in notes if note.get("key_fifths") is not None}
        tonal_modes = {str(note.get("key_mode", "")).lower() for note in notes if note.get("key_mode")}
        # Do not promote a coincidental eight-note major fragment to a
        # technical scale when a confirmed key context says otherwise.  Older
        # plans without key facts retain the conservative interval-only path.
        if tonal_fifths and len(tonal_fifths) == 1 and tonal_modes == {"major"}:
            tonic = (7 * int(next(iter(tonal_fifths)))) % 12
            if root != tonic:
                continue
        patterns = MAJOR_SCALE_PATTERNS.get(root)
        if patterns is None or any(note.get("locked") for note in notes):
            continue
        # Ascending patterns are listed in pitch order.  Descending runs use
        # the current hand's own physical pattern backwards: e.g. RH C-major
        # descends 5-4-3-2-1-3-2-1, while LH descends 1-2-3-1-2-3-4-5.
        # Using the opposite hand here silently shifts every post-thumb
        # descent by one finger.
        hand_index = 0 if hand_code == "RH" else 1
        digits = patterns[hand_index] if direction > 0 else patterns[hand_index][::-1]
        for note, digit in zip(notes, digits):
            finger = int(digit)
            if int(note.get("finger", 0)) != finger:
                _mark_reviewed(
                    note,
                    finger,
                    "complete key-confirmed major scale uses standard black-key-aware fingering",
                    "thumb_under" if finger == 1 else "finger_over" if note.get("finger") == 1 else "lateral_shift",
                )
            note["rule_id"] = "B5-B6"


def repair_elementary_broken_arpeggios(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Normalize common LH three-note broken-chord cells as one hand action."""
    if hand_code != "LH":
        return
    singles = [(position, event[0]) for position, event in enumerate(ordered_events) if len(event) == 1]
    for start in range(len(singles) - 2):
        window = singles[start:start + 3]
        positions = [position for position, _ in window]
        notes = [note for _, note in window]
        if positions != list(range(positions[0], positions[0] + 3)):
            continue
        if len({int(note["measure_index"]) for note in notes}) != 1 or any(note.get("locked") for note in notes):
            continue
        first, second, third = [int(note["pitch_midi"]) for note in notes]
        # Root--third--fifth normally stays in a compact 5-3-2 shape.  When
        # the next event immediately resets downward to a new bass, landing
        # the fifth on 1 gives the stable 5-3-1 / 5-3-1 accompaniment shape
        # seen in short broken-chord cells. Root--fifth--octave is 5-2-1 and
        # root--octave--third is 5-1-2. These are explicit cells, so the rule
        # cannot reinterpret an arbitrary melodic fragment.
        pattern = None
        intervals = (second - first, third - second)
        # Include the diminished 3-3 shape.  It is common in elementary
        # accompaniment (for example leading-tone harmony) and still needs
        # the same prepared 5-3-1 reset as other close third-based cells.
        if intervals in {(3, 3), (3, 4), (4, 3)}:
            following = singles[start + 3][1] if start + 3 < len(singles) and singles[start + 3][0] == positions[-1] + 1 else None
            if following is not None and int(following["pitch_midi"]) <= third - 5:
                pattern = (5, 3, 1)
            else:
                pattern = (5, 3, 2)
        elif intervals == (6, 3):
            # A wide lower skip into a compact third is not a normal root
            # triad.  The 5-3-1 shape keeps the middle black-key reach open
            # and prepares the immediate bass reset without a 2-to-1 squeeze.
            pattern = (5, 3, 1)
        elif intervals == (7, 5):
            pattern = (5, 2, 1)
        elif intervals == (12, 4):
            pattern = (5, 1, 2)
        if pattern is None:
            continue
        for note, finger in zip(notes, pattern):
            if int(note.get("finger", 0)) != finger:
                _mark_reviewed(
                    note, finger,
                    "elementary broken-chord cell keeps a prepared LH arpeggio shape",
                    "thumb_under" if finger == 1 else "finger_over" if note.get("finger") == 1 else "lateral_shift",
                )
            note["rule_id"] = "B1-B3"


def repair_right_hand_compact_arpeggios(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Prepare a three-note RH broken triad/inversion as 1-2-4.

    A compact ascending third-based arpeggio is a single hand shape, not three
    unrelated leaps.  This covers root position and ordinary inversions while
    deliberately excluding wide octave jumps and scalar fragments.
    """
    if hand_code != "RH":
        return
    singles = [(position, event[0]) for position, event in enumerate(ordered_events) if len(event) == 1]
    for window in zip(singles, singles[1:], singles[2:]):
        positions = [position for position, _ in window]
        notes = [note for _, note in window]
        if positions != list(range(positions[0], positions[0] + 3)):
            continue
        if (
            len({int(note["measure_index"]) for note in notes}) != 1
            or any(note.get("locked") for note in notes)
            or any(float(note.get("duration", 1)) > 0.5 for note in notes)
        ):
            continue
        first, second, third = [int(note["pitch_midi"]) for note in notes]
        steps = (second - first, third - second)
        if not (3 <= steps[0] <= 4 and 3 <= steps[1] <= 5 and 7 <= third - first <= 9):
            continue
        for index, (note, finger) in enumerate(zip(notes, (1, 2, 4))):
            if int(note.get("finger", 0)) != finger:
                _mark_reviewed(
                    note, finger,
                    "compact right-hand broken triad/inversion keeps a prepared 1-2-4 shape",
                    "leap" if index == 0 else "finger_over" if note.get("finger") == 1 else "lateral_shift",
                )
            note["rule_id"] = "B1-B3"


def repair_right_hand_returning_thumb_fan(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Reserve upper fingers in a short low--middle--low--high fan figure.

    The repeated low note fixes a thumb position while the later reach needs
    fingers 4 and 5.  Judging the first upward interval alone tends to spend
    finger 3 or 4 too early.  This remains a generic contour rule: it requires
    five consecutive short single attacks in one measure and never crosses a
    chord, rest, long value, or locked editorial anchor.
    """
    if hand_code != "RH":
        return
    singles = [(position, event[0]) for position, event in enumerate(ordered_events) if len(event) == 1]
    for window in zip(singles, singles[1:], singles[2:], singles[3:], singles[4:]):
        positions = [position for position, _ in window]
        notes = [note for _, note in window]
        if positions != list(range(positions[0], positions[0] + 5)):
            continue
        if (
            len({int(note["measure_index"]) for note in notes}) != 1
            or any(note.get("locked") or float(note.get("duration", 1)) > 0.5 for note in notes)
        ):
            continue
        low, middle, repeated_low, upper_a, upper_b = [int(note["pitch_midi"]) for note in notes]
        if low != repeated_low or not (3 <= middle - low <= 5):
            continue
        if not (6 <= upper_a - low <= 12 and 6 <= upper_b - low <= 12 and abs(upper_b - upper_a) <= 2):
            continue
        upper_fingers = (5, 4) if upper_a >= upper_b else (4, 5)
        for note, finger in zip(notes, (1, 2, 1, *upper_fingers)):
            if int(note.get("finger", 0)) != finger:
                _mark_reviewed(
                    note,
                    finger,
                    "thumb-return fan reserves upper fingers for the later reach",
                    "thumb_under" if finger == 1 else "lateral_shift",
                )
            note["rule_id"] = "B2-B5"


def repair_compact_five_key_position_run(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Map a short post-rest five-key run to one stable hand position.

    When a phrase exposes exactly five pitch levels within a compact seventh
    or sixth, the hand should normally keep one pitch-to-finger map instead of
    entering in the middle of the hand and shifting two notes later.  The run
    must start after a real rest, contain only short single attacks, and stop
    before the next long value/chord.  This makes the decision from the whole
    local range rather than any particular melody or key.
    """
    for start, event in enumerate(ordered_events):
        if len(event) != 1 or not event[0].get("preceding_rest"):
            continue
        run: list[dict] = []
        for candidate in ordered_events[start:start + 12]:
            if len(candidate) != 1:
                break
            note = candidate[0]
            if run and note.get("preceding_rest"):
                break
            if float(note.get("duration", 1)) > 0.5 or note.get("locked"):
                break
            run.append(note)
        if len(run) < 5:
            continue
        pitches = sorted({int(note["pitch_midi"]) for note in run})
        if len(pitches) != 5 or not 6 <= pitches[-1] - pitches[0] <= 9:
            continue
        if any(abs(int(right["pitch_midi"]) - int(left["pitch_midi"])) > 7 for left, right in zip(run, run[1:])):
            continue
        mapping = {pitch: index + 1 for index, pitch in enumerate(pitches)}
        if hand_code == "LH":
            mapping = {pitch: 5 - index for index, pitch in enumerate(pitches)}
        for note in run:
            finger = mapping[int(note["pitch_midi"])]
            if int(note.get("finger", 0)) != finger:
                _mark_reviewed(
                    note,
                    finger,
                    "compact post-rest phrase keeps one five-key hand-position map",
                    "same_position",
                )
            note["rule_id"] = "B1-B5"
        if start > 0 and len(ordered_events[start - 1]) == 1:
            prior = ordered_events[start - 1][0]
            first = run[0]
            if (
                not prior.get("locked")
                and int(prior["measure_index"]) == int(first["measure_index"])
                and int(prior["pitch_midi"]) == int(first["pitch_midi"])
                and float(prior.get("duration", 0)) >= 1.0
            ):
                _mark_reviewed(
                    prior,
                    mapping[int(first["pitch_midi"])],
                    "isolated phrase announcement keeps the following stable hand-position finger",
                    "same_position",
                )
                prior["rule_id"] = "B1-B5"


def repair_elementary_measure_position_cells(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Keep short elementary measure cells in one prepared hand position.

    The geometric solver can spend finger 3/5 on the first wide-looking
    interval even when the whole bar only occupies four adjacent hand slots.
    This routine reads the complete measure cell before deciding.  It is
    deliberately narrow: monophonic, unlocked, one-measure cells only, with
    exact contour/range guards and no arbitrary pitch or key names.
    """
    by_measure: dict[int, list[tuple[int, dict]]] = defaultdict(list)
    for position, event in enumerate(ordered_events):
        if len(event) == 1:
            by_measure[int(event[0]["measure_index"])].append((position, event[0]))

    for items in by_measure.values():
        if not items:
            continue
        positions = [position for position, _ in items]
        notes = [note for _, note in items]
        if positions != list(range(positions[0], positions[0] + len(positions))):
            continue
        if any(note.get("locked") for note in notes):
            continue
        pitches = [int(note["pitch_midi"]) for note in notes]

        if hand_code == "RH" and len(notes) == 3:
            deltas = (pitches[1] - pitches[0], pitches[2] - pitches[1])
            pattern: tuple[int, ...] | None = None
            if all(-2 <= delta <= -1 for delta in deltas):
                pattern = (4, 3, 2)
                reason = "three-note descending phrase keeps a centred 4-3-2 position"
            elif pitches[0] % 12 in {1, 3, 6, 8, 10} and deltas[0] == 1 and -4 <= deltas[1] <= -2:
                pattern = (1, 3, 1)
                reason = "chromatic upper-neighbour cell returns to a prepared thumb"
            if pattern is not None:
                for note, finger in zip(notes, pattern):
                    if int(note.get("finger", 0)) != finger:
                        _mark_reviewed(note, finger, reason, "same_position")
                    note["rule_id"] = "B3-B5"
                continue

        if hand_code == "LH" and len(notes) == 3:
            deltas = (pitches[1] - pitches[0], pitches[2] - pitches[1])
            if -2 <= deltas[0] <= -1 and -5 <= deltas[1] <= -3 and 5 <= pitches[0] - pitches[2] <= 7:
                for note, finger in zip(notes, (1, 2, 5)):
                    if int(note.get("finger", 0)) != finger:
                        _mark_reviewed(
                            note, finger,
                            "descending left-hand three-note cell opens from thumb to little finger",
                            "same_position",
                        )
                    note["rule_id"] = "B3-B5"
                continue

        if hand_code != "RH" or not 5 <= len(notes) <= 8:
            continue
        levels = sorted(set(pitches))
        if len(levels) != 4 or pitches[0] != levels[0]:
            continue
        gaps = tuple(right - left for left, right in zip(levels, levels[1:]))
        if not (3 <= gaps[0] <= 5 and gaps[1:] == (2, 2) and 7 <= levels[-1] - levels[0] <= 9):
            continue
        if any(abs(right - left) > 5 for left, right in zip(pitches, pitches[1:])):
            continue
        mapping = {pitch: index + 1 for index, pitch in enumerate(levels)}
        for note in notes:
            finger = mapping[int(note["pitch_midi"])]
            if int(note.get("finger", 0)) != finger:
                _mark_reviewed(
                    note, finger,
                    "whole-measure four-level cell keeps one 1-2-3-4 hand-position map",
                    "same_position",
                )
            note["rule_id"] = "B1-B5"


def repair_right_hand_compact_octave_arpeggio(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Use 1-2-3-5 for a compact RH broken chord that closes at the octave."""
    if hand_code != "RH":
        return
    singles = [(position, event[0]) for position, event in enumerate(ordered_events) if len(event) == 1]
    for window in zip(singles, singles[1:], singles[2:], singles[3:]):
        positions = [position for position, _ in window]
        notes = [note for _, note in window]
        if positions != list(range(positions[0], positions[0] + 4)):
            continue
        if len({int(note["measure_index"]) for note in notes}) != 1 or any(note.get("locked") for note in notes):
            continue
        pitches = [int(note["pitch_midi"]) for note in notes]
        steps = tuple(right - left for left, right in zip(pitches, pitches[1:]))
        if not (steps[0] in {3, 4} and steps[1] in {3, 4} and steps[2] == 5 and pitches[-1] - pitches[0] == 12):
            continue
        for index, (note, finger) in enumerate(zip(notes, (1, 2, 3, 5))):
            if int(note.get("finger", 0)) != finger:
                _mark_reviewed(
                    note,
                    finger,
                    "compact broken chord closing at an octave uses the prepared 1-2-3-5 shape",
                    "leap" if index == 0 else "lateral_shift",
                )
            note["rule_id"] = "B1-B3"


def repair_right_hand_symmetric_compact_arch(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Keep a seven-note symmetric RH arch in a 1-2-3-5-3-2-1 shape."""
    if hand_code != "RH":
        return
    singles = [(position, event[0]) for position, event in enumerate(ordered_events) if len(event) == 1]
    for window in zip(*[singles[offset:] for offset in range(7)]):
        positions = [position for position, _ in window]
        notes = [note for _, note in window]
        if positions != list(range(positions[0], positions[0] + 7)):
            continue
        if len({int(note["measure_index"]) for note in notes}) != 1 or any(note.get("locked") for note in notes):
            continue
        pitches = [int(note["pitch_midi"]) for note in notes]
        deltas = tuple(right - left for left, right in zip(pitches, pitches[1:]))
        if not (
            all(2 <= delta <= 4 for delta in deltas[:3])
            and deltas[3:] == tuple(-delta for delta in reversed(deltas[:3]))
            and 7 <= pitches[3] - pitches[0] <= 10
        ):
            continue
        for index, (note, finger) in enumerate(zip(notes, (1, 2, 3, 5, 3, 2, 1))):
            if int(note.get("finger", 0)) != finger:
                _mark_reviewed(
                    note,
                    finger,
                    "symmetric compact arch keeps the stable 1-2-3-5-3-2-1 hand map",
                    "leap" if index == 0 else "lateral_shift",
                )
            note["rule_id"] = "B3-B5"


def repair_right_hand_octave_neighbour(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Use 1-5-3 for a low note, its octave, then upper neighbour below it."""
    if hand_code != "RH":
        return
    singles = [(position, event[0]) for position, event in enumerate(ordered_events) if len(event) == 1]
    for window in zip(singles, singles[1:], singles[2:]):
        positions = [position for position, _ in window]
        notes = [note for _, note in window]
        if positions != list(range(positions[0], positions[0] + 3)):
            continue
        if (
            len({int(note["measure_index"]) for note in notes}) != 1
            or any(note.get("locked") for note in notes)
            or any(float(note.get("duration", 1)) > 0.5 for note in notes)
        ):
            continue
        pitches = [int(note["pitch_midi"]) for note in notes]
        if (pitches[1] - pitches[0], pitches[2] - pitches[1]) != (12, -1):
            continue
        for index, (note, finger) in enumerate(zip(notes, (1, 5, 3))):
            if int(note.get("finger", 0)) != finger:
                _mark_reviewed(
                    note, finger,
                    "octave reach followed by upper neighbour uses prepared 1-5-3 shape",
                    "leap" if index == 0 else "lateral_shift",
                )
            note["rule_id"] = "B3"


def repair_right_hand_neighbour_drop(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Finger a compact neighbour-return plus fourth-drop gesture as one phrase."""
    if hand_code != "RH":
        return
    singles = [(position, event[0]) for position, event in enumerate(ordered_events) if len(event) == 1]
    for window in zip(*[singles[offset:] for offset in range(6)]):
        positions = [position for position, _ in window]
        notes = [note for _, note in window]
        if positions != list(range(positions[0], positions[0] + 6)) or any(note.get("locked") for note in notes):
            continue
        pitches = [int(note["pitch_midi"]) for note in notes]
        # A chromatic/diatonic upper-neighbour return followed by a fourth
        # down, then a small recovery.  Landing the fourth-drop on thumb
        # avoids an unnecessary shift and prepares the final 4-2 pair.
        deltas = tuple(b - a for a, b in zip(pitches, pitches[1:]))
        if not (-2 <= deltas[0] <= -1 and -deltas[0] == deltas[1] and deltas[2] == -5 and deltas[3] == 3 and deltas[4] == -2):
            continue
        for note, finger in zip(notes, (4, 3, 4, 1, 4, 2)):
            if int(note.get("finger", 0)) != finger:
                _mark_reviewed(
                    note, finger,
                    "neighbour-return plus fourth-drop gesture uses a prepared thumb landing",
                    "thumb_under" if finger == 1 else "finger_over" if note.get("finger") == 1 else "lateral_shift",
                )
            note["rule_id"] = "B3-B5"


def repair_extreme_turning_points(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Land isolated octave-scale turning points on the appropriate outer finger."""
    singles = [(position, event[0]) for position, event in enumerate(ordered_events) if len(event) == 1]
    for (left_position, previous), (middle_position, current), (right_position, following) in zip(
        singles, singles[1:], singles[2:]
    ):
        if middle_position - left_position != 1 or right_position - middle_position != 1:
            continue
        if len({int(previous["measure_index"]), int(current["measure_index"]), int(following["measure_index"])}) != 1:
            continue
        before = int(previous["pitch_midi"])
        pitch = int(current["pitch_midi"])
        after = int(following["pitch_midi"])
        upper_apex = min(pitch - before, pitch - after) >= 7
        lower_apex = min(before - pitch, after - pitch) >= 7
        if not upper_apex and not lower_apex:
            continue
        if hand_code == "RH":
            target = 5 if upper_apex else 1
        else:
            target = 1 if upper_apex else 5
        if current.get("locked") or int(current.get("finger", 0)) == target:
            continue
        _mark_reviewed(
            current,
            target,
            "isolated octave-scale turning point lands on the outer finger",
            "leap",
        )
        current["rule_id"] = "B3"


def repair_stepwise_neighbor_turns(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Keep a four-note upper-neighbour turn in one adjacent-finger hand shape."""
    singles = [(position, event[0]) for position, event in enumerate(ordered_events) if len(event) == 1]
    for window in zip(singles, singles[1:], singles[2:], singles[3:]):
        positions = [item[0] for item in window]
        notes = [item[1] for item in window]
        if positions != list(range(positions[0], positions[0] + 4)):
            continue
        if len({int(note["measure_index"]) for note in notes}) != 1:
            continue
        pitches = [int(note["pitch_midi"]) for note in notes]
        if not (
            pitches[0] < pitches[1] < pitches[2]
            and pitches[3] == pitches[1]
            and pitches[1] - pitches[0] <= 2
            and pitches[2] - pitches[1] <= 2
        ):
            continue
        pattern = [1, 2, 3, 2] if hand_code == "RH" else [5, 4, 3, 4]
        if any(note.get("locked") for note in notes):
            continue
        for index, (note, finger) in enumerate(zip(notes, pattern)):
            note["finger"] = finger
            note["source"] = "reviewed"
            note["exception_reason"] = "stepwise upper-neighbour turn keeps one adjacent-finger hand shape"
            note["rule_id"] = "B5"
            if index == 0:
                note["transition_type"] = "lateral_shift"


def repair_right_hand_sustained_reentry_descent(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Keep a central 4-3-2 shape after a sustained lower-note re-entry.

    A held lower note followed by an upward fourth-or-larger leap into three
    descending stepwise notes is a small phrase, not an isolated leap.  On the
    right hand, landing with 5-4-3 strands the hand at its edge; 4-3-2 keeps
    the run centred and prepares the continuation.  The duration and leap
    guards deliberately keep this from rewriting ordinary descending scales.
    """
    if hand_code != "RH":
        return
    singles = [(position, event[0]) for position, event in enumerate(ordered_events) if len(event) == 1]
    for window in zip(singles, singles[1:], singles[2:], singles[3:]):
        positions = [position for position, _ in window]
        notes = [note for _, note in window]
        if positions != list(range(positions[0], positions[0] + 4)):
            continue
        prior, first, second, third = notes
        if (
            int(first["measure_index"]) == int(prior["measure_index"])
            or len({int(note["measure_index"]) for note in (first, second, third)}) != 1
            or any(note.get("locked") for note in (first, second, third))
            or float(prior.get("duration", 0)) < 1.0
        ):
            continue
        leap = int(first["pitch_midi"]) - int(prior["pitch_midi"])
        steps = (int(second["pitch_midi"]) - int(first["pitch_midi"]), int(third["pitch_midi"]) - int(second["pitch_midi"]))
        if not (5 <= leap <= 12 and all(-2 <= step <= -1 for step in steps)):
            continue
        for index, (note, finger) in enumerate(zip((first, second, third), (4, 3, 2))):
            if int(note.get("finger", 0)) != finger:
                _mark_reviewed(
                    note,
                    finger,
                    "sustained lower-note re-entry uses a centred 4-3-2 descending hand shape",
                    "leap" if index == 0 else "lateral_shift",
                )
            note["rule_id"] = "B3-B5"


def repair_right_hand_held_descending_tetrachord(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Centre a held-start, compact four-note RH descent as 4-3-2-1.

    This applies only when a dotted-or-longer first note begins a compact
    descent within one measure.  It captures a phrase-led hand position while
    leaving ordinary quarter-note scale fragments to the main search.
    """
    if hand_code != "RH":
        return
    singles = [(position, event[0]) for position, event in enumerate(ordered_events) if len(event) == 1]
    for window in zip(singles, singles[1:], singles[2:], singles[3:]):
        positions = [position for position, _ in window]
        notes = [note for _, note in window]
        if positions != list(range(positions[0], positions[0] + 4)):
            continue
        if (
            len({int(note["measure_index"]) for note in notes}) != 1
            or any(note.get("locked") for note in notes)
            or float(notes[0].get("duration", 0)) < 1.5
        ):
            continue
        pitches = [int(note["pitch_midi"]) for note in notes]
        deltas = [right - left for left, right in zip(pitches, pitches[1:])]
        if not (all(-3 <= delta <= -1 for delta in deltas) and 6 <= pitches[0] - pitches[-1] <= 8):
            continue
        for index, (note, finger) in enumerate(zip(notes, (4, 3, 2, 1))):
            if int(note.get("finger", 0)) != finger:
                _mark_reviewed(
                    note,
                    finger,
                    "held-start compact descent keeps a centred 4-3-2-1 hand shape",
                    "lateral_shift" if index == 0 else "finger_over" if finger == 1 else "lateral_shift",
                )
            note["rule_id"] = "B3-B5"


def repair_right_hand_slow_phrase_entry(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Shape a slow cross-barline RH entry before local search strands it.

    A melody that begins after a genuine RH gap may need a thumb crossing even
    though every adjacent interval is stepwise.  The old repair only handled
    a four-note descent within one bar, so a slow two-plus-two entry across a
    barline was left as an edge-of-hand 5-4-3-2.  Restrict this to a stream
    entry, long values, and exactly two notes in each of two consecutive bars;
    ordinary running scales and mid-phrase fragments stay with the solver.
    """
    if hand_code != "RH":
        return
    singles = [(position, event[0]) for position, event in enumerate(ordered_events) if len(event) == 1]
    for window in zip(singles, singles[1:], singles[2:], singles[3:]):
        positions = [position for position, _ in window]
        notes = [note for _, note in window]
        if positions != list(range(positions[0], positions[0] + 4)) or positions[0] != 0:
            continue
        measures = [int(note["measure_index"]) for note in notes]
        if measures != [measures[0], measures[0], measures[0] + 1, measures[0] + 1]:
            continue
        if any(note.get("locked") or float(note.get("duration", 0)) < 1.5 for note in notes):
            continue
        pitches = [int(note["pitch_midi"]) for note in notes]
        deltas = [right - left for left, right in zip(pitches, pitches[1:])]
        if not (all(-2 <= delta <= -1 for delta in deltas) and 4 <= pitches[0] - pitches[-1] <= 7):
            continue
        for index, (note, finger) in enumerate(zip(notes, (4, 3, 1, 3))):
            if int(note.get("finger", 0)) != finger:
                _mark_reviewed(
                    note,
                    finger,
                    "slow cross-barline descent starts with a centred thumb crossing",
                    "lateral_shift" if index in {0, 1, 3} else "finger_over",
                )
            note["rule_id"] = "B3-B5"


def repair_right_hand_slow_lower_neighbour(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Keep a slow cross-barline lower-neighbour reply as 1-2-1-2."""
    if hand_code != "RH":
        return
    singles = [(position, event[0]) for position, event in enumerate(ordered_events) if len(event) == 1]
    for window in zip(singles, singles[1:], singles[2:], singles[3:]):
        positions = [position for position, _ in window]
        notes = [note for _, note in window]
        if positions != list(range(positions[0], positions[0] + 4)) or positions[0] < 1:
            continue
        prior_event = ordered_events[positions[0] - 1]
        if len(prior_event) != 1 or prior_event[0].get("rule_id") != "B3-B5":
            continue
        measures = [int(note["measure_index"]) for note in notes]
        if measures != [measures[0], measures[0], measures[0] + 1, measures[0] + 1]:
            continue
        if any(note.get("locked") or float(note.get("duration", 0)) < 1.5 for note in notes):
            continue
        pitches = [int(note["pitch_midi"]) for note in notes]
        if not (
            pitches[0] == pitches[2]
            and 1 <= pitches[0] - pitches[1] <= 2
            and 1 <= pitches[3] - pitches[2] <= 2
        ):
            continue
        for index, (note, finger) in enumerate(zip(notes, (1, 2, 1, 2))):
            if int(note.get("finger", 0)) != finger:
                _mark_reviewed(
                    note,
                    finger,
                    "slow lower-neighbour reply keeps a compact thumb-led hand shape",
                    "lateral_shift" if index in {0, 1, 3} else "finger_over",
                )
            note["rule_id"] = "B5"


def repair_final_melodic_invariants(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Recheck hard melodic constraints after every structural repair.

    Chord and accompaniment repairs intentionally run after the first melodic
    pass.  They can therefore reintroduce a same-finger move between different
    pitches.  This final pass either chooses a neighbouring finger or records a
    genuine reposition across intervening events/rests.  Stable repeated
    figures (for example 5-3-1 triplets) are preserved by moving the preceding
    note when possible rather than corrupting the repeated shape.
    """
    melodic = [(position, event[0]) for position, event in enumerate(ordered_events) if len(event) == 1]
    for (previous_position, previous), (current_position, current) in zip(melodic, melodic[1:]):
        if current.get("preceding_rest"):
            continue
        previous_finger = int(previous.get("finger", 0))
        current_finger = int(current.get("finger", 0))
        pitch_delta = int(current["pitch_midi"]) - int(previous["pitch_midi"])
        if not pitch_delta or not previous_finger or previous_finger != current_finger:
            continue
        if current.get("connection") == "detached" or current.get("transition_type") == "leap":
            continue

        # Chords or other events between the two single notes break literal
        # finger continuity.  Keep the stable outer finger and make the reset
        # explicit so the validator does not mistake it for legato motion.
        if (
            current_position - previous_position > 1
            or int(current["measure_index"]) - int(previous["measure_index"]) > 1
            or (
                int(current["measure_index"]) != int(previous["measure_index"])
                and abs(pitch_delta) >= 7
            )
        ):
            current["transition_type"] = "leap"
            current["exception_reason"] = "hand position resets after intervening events or rests"
            current["source"] = "reviewed"
            continue

        natural_sign = 1 if (pitch_delta > 0) == (hand_code == "RH") else -1
        reason = str(current.get("exception_reason", ""))
        preserve_current = any(token in reason for token in ("repeated triplet", "stable hand", "tie group"))

        if preserve_current and not previous.get("locked"):
            candidate = current_finger - natural_sign
            if not 1 <= candidate <= 5:
                candidate = current_finger + natural_sign
            if 1 <= candidate <= 5:
                _mark_reviewed(
                    previous,
                    candidate,
                    "prepare the following stable repeated figure without reusing one finger on a new pitch",
                )
                current["transition_type"] = "lateral_shift"
                current["exception_reason"] = "phrase boundary resets into the stable repeated figure"
                current["source"] = "reviewed"
                continue

        if not current.get("locked"):
            candidate = previous_finger + natural_sign
            if not 1 <= candidate <= 5:
                candidate = previous_finger - natural_sign
            if 1 <= candidate <= 5:
                transition = "lateral_shift"
                if candidate == 1:
                    transition = "thumb_under"
                elif previous_finger == 1:
                    transition = "finger_over"
                _mark_reviewed(
                    current,
                    candidate,
                    "final invariant: connected different pitches must not reuse one finger",
                    transition,
                )


def annotate_directional_repositions(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Record every remaining non-linear melodic move after structural repairs.

    A repair may deliberately choose a useful non-adjacent hand shape after the
    initial solver pass.  Leaving that move untyped makes downstream validation
    treat it as an unexplained mistake.  This pass never changes a finger: it
    only names the necessary physical action so it can be audited or rejected
    by a stricter caller policy.
    """
    melodic = [(position, event[0]) for position, event in enumerate(ordered_events) if len(event) == 1]
    for (previous_position, previous), (current_position, current) in zip(melodic, melodic[1:]):
        if current.get("preceding_rest"):
            continue
        if current.get("transition_type") or current.get("locked"):
            continue
        if current_position - previous_position > 1:
            continue
        pitch_delta = int(current["pitch_midi"]) - int(previous["pitch_midi"])
        finger_delta = int(current.get("finger", 0)) - int(previous.get("finger", 0))
        if not pitch_delta or not finger_delta:
            continue
        reversal = pitch_delta * finger_delta * (1 if hand_code == "RH" else -1) < 0
        if not reversal:
            continue
        transition = "thumb_under" if int(current["finger"]) == 1 else (
            "finger_over" if int(previous["finger"]) == 1 else "lateral_shift"
        )
        current["transition_type"] = transition
        current["source"] = "reviewed"
        current["exception_reason"] = "directional reversal retained after structural fingering repair"


def prepare_tied_chord_shapes(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Carry the *next* complete chord shape back to its tied members.

    A tied triad can become a four-note chord while it is held.  Sealing the
    first triad as 1-3-5 and the later four-note chord as 1-2-3-5 forces the
    tied pitches to change fingers.  The later chord is the more constrained
    physical event, so its assigned slots are propagated back to the starting
    tied members before either chord is sealed.
    """
    preferred: dict[str, int] = {}
    for event in ordered_events:
        if not event:
            continue
        pattern = chord_pattern(event, hand_code)
        for note, finger in zip(event, pattern):
            tie_group = str(note.get("tie_group", ""))
            if tie_group and note.get("tie_stop"):
                preferred[tie_group] = finger
    if not preferred:
        return
    for event in ordered_events:
        for note in event:
            tie_group = str(note.get("tie_group", ""))
            if tie_group in preferred:
                note["tie_preferred_finger"] = preferred[tie_group]


def chord_pattern_with_tie_slots(members: list[dict], hand_code: str) -> list[int] | None:
    """Return an ordered, unique chord pattern that retains tied finger slots."""
    preferred = {
        index: int(note["tie_preferred_finger"])
        for index, note in enumerate(members)
        if int(note.get("tie_preferred_finger", 0)) in {1, 2, 3, 4, 5}
    }
    if not preferred:
        return chord_pattern(members, hand_code)
    baseline = chord_pattern(members, hand_code)
    candidates: list[list[int]] = []
    for digits in combinations(range(1, 6), len(members)):
        proposal = list(digits if hand_code == "RH" else reversed(digits))
        if any(proposal[index] != finger for index, finger in preferred.items()):
            continue
        candidates.append(proposal)
    if not candidates:
        return None
    return min(candidates, key=lambda proposal: (sum((left - right) ** 2 for left, right in zip(proposal, baseline)), proposal))


def seal_chord_shapes(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Make chord order/uniqueness the final, non-overridable postcondition."""
    for event in ordered_events:
        if len(event) <= 1 or any(note.get("locked") for note in event):
            continue
        # A preceding close outer bass can require the explicit compact shape
        # 4-1 for a wider dyad.  It remains ordered and unique, so it is a
        # valid connection-aware exception to the generic span template.
        if any(note.get("chord_shape_override") == "reserve_outer_bass" for note in event):
            continue
        pattern = chord_pattern_with_tie_slots(event, hand_code)
        if pattern is None:
            # A tied slot is incompatible with a unique, ordered one-hand
            # chord. Preserve the current digits for the validator/review
            # instead of inventing a finger substitution.
            continue
        if [int(note.get("finger", 0)) for note in event] == pattern:
            continue
        for note, finger in zip(event, pattern):
            _mark_reviewed(note, finger, "final chord seal restores one finger per simultaneous pitch", "chord_change")
            note["rule_id"] = "B1"


def repair_single_chord_connections(ordered_events: list[list[dict]], hand_code: str) -> None:
    """Prevent a single bass/melody note from stealing a finger used by the next chord."""
    for previous, current in zip(ordered_events, ordered_events[1:]):
        if len(previous) == len(current) or {len(previous), len(current)} != {1, 2}:
            continue
        single_event, chord_event = (previous, current) if len(previous) == 1 else (current, previous)
        single = single_event[0]
        if single.get("connection") == "detached" or single.get("transition_type") == "leap":
            continue
        single_pitch = int(single["pitch_midi"])
        chord_pitches = [int(item["pitch_midi"]) for item in chord_event]
        single_finger = int(single.get("finger", 0))
        outside_below = single_pitch < min(chord_pitches)
        outside_above = single_pitch > max(chord_pitches)
        outer_side = (hand_code == "LH" and outside_below) or (hand_code == "RH" and outside_above)
        if not outer_side:
            continue
        outer_finger = 5 if (hand_code == "LH") == outside_below else 1
        verified_exception = single.get("exception_verified") is True
        # Broken-chord accompaniment needs a stable outer finger even when no
        # literal finger-number conflict exists. This evaluates the horizontal
        # single-to-dyad connection, not just each event in isolation.
        if not single.get("locked") and not verified_exception and single_finger != outer_finger:
            _mark_reviewed(
                single,
                outer_finger,
                "outer accompaniment note prepares the adjacent dyad with a stable hand position",
                "same_position",
            )
            single_finger = outer_finger
        if not single.get("locked"):
            single_finger = int(single.get("finger", 0))

        conflicts = [item for item in chord_event if int(item.get("finger", 0)) == single_finger and int(item["pitch_midi"]) != single_pitch]
        if not conflicts:
            continue
        if conflicts and not any(item.get("locked") for item in chord_event):
            # Keep the dyad's vertical shape tied to its *actual* interval.
            # The older repair used 4-1 for every LH dyad up to a fifth.  That
            # silently widened ordinary thirds (C--E) from 3-1 to 4-1 and was
            # the source of many unstable "bass--dyad" accompaniments.
            replacement = chord_pattern(chord_event, hand_code)
            # A nearby LH bass can legitimately hold 5 while the following
            # sixth/seventh dyad needs a compact 4-1 shape.  Reapplying 5-1
            # here would force the same finger through a 2nd/3rd and is the
            # exact local conflict this repair is meant to remove.  This is
            # deliberately narrow: thirds/fourths keep their normal 3-1/4-1
            # patterns and a real leap is left to the solver.
            if (
                hand_code == "LH"
                and len(chord_event) == 2
                and replacement[0] == single_finger
                and abs(int(chord_event[0]["pitch_midi"]) - single_pitch) <= 4
                and int(chord_event[1]["pitch_midi"]) - int(chord_event[0]["pitch_midi"]) >= 6
            ):
                replacement = [4, 1]
                for item in chord_event:
                    item["chord_shape_override"] = "reserve_outer_bass"
            for item, finger in zip(chord_event, replacement):
                _mark_reviewed(
                    item,
                    finger,
                    "reserve the outer finger for the adjacent single note",
                    "chord_change",
                )

    # Once a repeated accompaniment dyad has been narrowed to reserve finger 5,
    # keep the identical hand shape for every occurrence in that measure.
    shapes: dict[tuple[int, tuple[int, ...]], list[list[dict]]] = defaultdict(list)
    for event in ordered_events:
        if len(event) == 2:
            key = (
                int(event[0]["measure_index"]),
                tuple(int(item["pitch_midi"]) for item in event),
            )
            shapes[key].append(event)
    for (_, pitches), events in shapes.items():
        target = chord_pattern(events[0], hand_code)
        # Preserve a deliberately reviewed compact shape that reserved the
        # outer bass finger.  Do not let repeated-figure normalization undo
        # the immediately preceding connection repair.
        reserved = [
            [int(item.get("finger", 0)) for item in event]
            for event in events
            if any(
                "reserve the outer finger" in str(item.get("exception_reason", ""))
                for item in event
            )
        ]
        if reserved and all(finger in {1, 2, 3, 4, 5} for finger in reserved[0]):
            target = reserved[0]
            for event in events:
                for item in event:
                    item["chord_shape_override"] = "reserve_outer_bass"
        if len(events) < 2 or not any([int(item.get("finger", 0)) for item in event] == target for event in events):
            continue
        for event in events:
            if any(item.get("locked") for item in event):
                continue
            for item, finger in zip(event, target):
                if int(item.get("finger", 0)) != finger:
                    _mark_reviewed(
                        item,
                        finger,
                        "keep the repeated accompaniment dyad in one stable hand shape",
                        "chord_change",
                    )

    # Normalizing the last dyad of one measure can expose a new conflict with the
    # first bass note of the next measure, so close that boundary once more.
    for previous, current in zip(ordered_events, ordered_events[1:]):
        if {len(previous), len(current)} != {1, 2}:
            continue
        single_event, chord_event = (previous, current) if len(previous) == 1 else (current, previous)
        single = single_event[0]
        single_pitch = int(single["pitch_midi"])
        chord_pitches = [int(item["pitch_midi"]) for item in chord_event]
        outer_side = (hand_code == "LH" and single_pitch < min(chord_pitches)) or (
            hand_code == "RH" and single_pitch > max(chord_pitches)
        )
        nearest = min(chord_event, key=lambda item: abs(int(item["pitch_midi"]) - single_pitch))
        if (
            outer_side
            and int(single.get("finger", 0)) == int(nearest.get("finger", 0))
            and int(single.get("finger", 0)) != 0
            and abs(int(nearest["pitch_midi"]) - single_pitch) <= 4
            and not single.get("locked")
        ):
            _mark_reviewed(
                single,
                5,
                "reserve finger 5 across the measure boundary before the adjacent dyad",
            )


def postprocess(records: list[dict], hand_code: str) -> None:
    """Repair deterministic structural problems before musical review."""
    events: dict[tuple, list[dict]] = defaultdict(list)
    for record in records:
        events[(record["measure_index"], record["onset"], record["event_index"], record["chord_id"])].append(record)
    ordered_events: list[list[dict]] = []
    for key in sorted(events):
        members = sorted(events[key], key=lambda item: int(item["pitch_midi"]))
        if 1 < len(members) <= 5 and not any(item.get("locked") for item in members):
            pattern = chord_pattern(members, hand_code)
            old = [int(item.get("finger", 0)) for item in members]
            if old != pattern:
                for item, finger in zip(members, pattern):
                    item["finger"] = finger
                    item["source"] = "reviewed"
                    item["transition_type"] = "chord_change"
                    item["exception_reason"] = "normalize chord to an ordered hand shape matched to its pitch span"
        ordered_events.append(members)

    melodic = [event[0] for event in ordered_events if len(event) == 1]
    for previous, current in zip(melodic, melodic[1:]):
        previous_finger = int(previous.get("finger", 0))
        current_finger = int(current.get("finger", 0))
        pitch_delta = int(current["pitch_midi"]) - int(previous["pitch_midi"])
        if not pitch_delta or not previous_finger or not current_finger:
            continue
        if previous_finger == current_finger and not current.get("locked"):
            natural_sign = 1 if (pitch_delta > 0) == (hand_code == "RH") else -1
            candidate = previous_finger + natural_sign
            if not 1 <= candidate <= 5:
                candidate = previous_finger - natural_sign
            current["finger"] = candidate
            current["source"] = "reviewed"
            current["transition_type"] = "lateral_shift"
            current["exception_reason"] = "avoid same finger on connected different pitches"
            current_finger = candidate
        finger_delta = current_finger - previous_finger
        reversal = pitch_delta * finger_delta * (1 if hand_code == "RH" else -1) < 0
        if reversal and not current.get("transition_type"):
            if current_finger == 1:
                current["transition_type"] = "thumb_under"
                current["exception_reason"] = "thumb-under transition selected by the solver"
            elif previous_finger == 1:
                current["transition_type"] = "finger_over"
                current["exception_reason"] = "finger-over transition selected by the solver"
            else:
                current["transition_type"] = "lateral_shift"
                current["exception_reason"] = "phrase-level hand reposition selected by the solver"

    # These phrase/event repairs must run last: the melodic pass above may otherwise
    # overwrite a bass finger that was deliberately reserved for an adjacent chord.
    repair_repeated_triplets(ordered_events, hand_code)
    repair_single_chord_connections(ordered_events, hand_code)
    repair_repeated_accompaniment_pitch(ordered_events, hand_code)
    repair_tied_notes(ordered_events, hand_code)
    repair_complete_major_scales(ordered_events, hand_code)
    repair_elementary_broken_arpeggios(ordered_events, hand_code)
    repair_compact_five_key_position_run(ordered_events, hand_code)
    # The five-key map is broad; a returning-thumb fan has stronger contour
    # evidence and must be allowed to reserve 4/5 afterwards.
    repair_right_hand_returning_thumb_fan(ordered_events, hand_code)
    repair_elementary_measure_position_cells(ordered_events, hand_code)
    # These guarded melodic shapes describe slow, explicitly delimited phrase
    # entries.  Unlike a broad contour rewrite, each repair requires duration,
    # interval and barline evidence, so it improves a real class of elementary
    # phrases without touching ordinary scales or accompaniment figures.
    repair_right_hand_sustained_reentry_descent(ordered_events, hand_code)
    repair_right_hand_held_descending_tetrachord(ordered_events, hand_code)
    repair_right_hand_slow_phrase_entry(ordered_events, hand_code)
    repair_right_hand_slow_lower_neighbour(ordered_events, hand_code)
    repair_connected_repeated_notes(ordered_events, hand_code)
    repair_final_melodic_invariants(ordered_events, hand_code)
    # The final different-pitch invariant can change the first note of a
    # repeated-pitch run (for example when it fixes the preceding interval).
    # Reapply the hard same-pitch rule afterwards so that a later repair never
    # reintroduces an unrequested substitution.
    repair_connected_repeated_notes(ordered_events, hand_code)
    # Reapplying the same-pitch invariant can itself expose a same-finger move
    # from the repeated note into the next *different* pitch. Run the final
    # different-pitch seal once more: it does not alter equal pitches, and
    # closes the otherwise cyclic pair of hard constraints.
    repair_final_melodic_invariants(ordered_events, hand_code)
    annotate_directional_repositions(ordered_events, hand_code)
    # Chord sealing runs late to protect vertical order, but it can touch a
    # later chord member that is still tied from an earlier event.  Reapply
    # the non-negotiable tie invariant afterwards; otherwise a valid chord
    # repair silently becomes an illegal mid-note finger change.
    prepare_tied_chord_shapes(ordered_events, hand_code)
    seal_chord_shapes(ordered_events, hand_code)
    repair_tied_notes(ordered_events, hand_code)
    # Keep literal repetitions stable after every local repair has finished.
    repair_identical_measure_motifs(ordered_events, hand_code)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--ignore-existing", action="store_true")
    parser.add_argument(
        "--provisional-omr",
        action="store_true",
        help=(
            "generate a diagnostic-only candidate from a local OMR plan after semantic checks; "
            "it never bypasses the normal delivery gate or marks score facts as verified"
        ),
    )
    parser.add_argument(
        "--hand-size",
        choices=("XXS", "XS", "S", "M", "L", "XL", "XXL"),
        help="temporarily override the plan's hand-size preset for this generation",
    )
    parser.add_argument("--preserve-posture-memory", action="store_true")
    parser.add_argument(
        "--global-phrase-candidate", action="store_true",
        help="generate an experimental whole-phrase candidate; never enabled by the default delivery path",
    )
    parser.add_argument(
        "--max-auto-depth",
        type=int,
        default=4,
        choices=range(4, 8),
        metavar="4-7",
        help="cap automatic look-ahead depth (default: 4; increase only when a measured local review demonstrates a benefit)",
    )
    parser.add_argument("--changed-only", action="store_true", help="infer the latest recognition patch scope and recompute only affected measures")
    parser.add_argument("--quiet", action="store_true", help="suppress periodic progress and timing messages")
    parser.add_argument(
        "--measure-range",
        type=parse_measure_range,
        help="recompute only N or START-END while retaining nearby phrase context",
    )
    parser.add_argument(
        "--context-measures",
        type=int,
        default=1,
        help="neighbouring measures used as read-only context with --measure-range (default: 1)",
    )
    args = parser.parse_args()
    if args.context_measures < 0:
        parser.error("--context-measures must be non-negative")
    if args.changed_only and args.measure_range:
        parser.error("--changed-only and --measure-range cannot be used together")
    started_at = time.perf_counter()
    plan = load_plan(args.input)
    provisional_omr = args.provisional_omr
    source_type = str(plan.get("source", {}).get("type", "")).lower()
    if provisional_omr and source_type != "omr_candidate":
        parser.error("--provisional-omr is only valid for source.type=omr_candidate")
    # A candidate is useful for benchmark comparison and focused human review,
    # but must never become an ordinary deliverable just because the solver can
    # operate on it.  Keep the strict, locked recognition gate as the default;
    # the explicit diagnostic route only checks internally coherent score facts.
    recognition_errors, recognition_warnings = validate_recognition(
        plan,
        strict=not provisional_omr,
        require_locked=not provisional_omr,
    )
    for warning in recognition_warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    if recognition_errors:
        for error in recognition_errors:
            print(f"ERROR: recognition gate: {error}", file=sys.stderr)
        print("ERROR: fingering generation blocked until score facts pass recognition validation", file=sys.stderr)
        return 1
    if provisional_omr:
        recognition = plan.setdefault("recognition", {})
        recognition["provisional_omr"] = {
            "status": "diagnostic_only",
            "reason": "local OMR candidate has not passed raw-page recognition verification",
        }
    settings = plan["settings"]
    hand_size = args.hand_size or str(settings.get("hand_size", "M")).upper()
    # The plan is the source of truth for the delivery report.  Do not leave
    # its default (usually M) behind when a caller explicitly generated this
    # result with a different preset, otherwise the report can misrepresent
    # the physical assumption used by the solver.
    settings["hand_size"] = hand_size
    lookahead = int(settings.get("lookahead", 0))
    by_hand: dict[str, list[dict]] = defaultdict(list)
    # A benchmark must not let editorial digits influence postprocessing.  It
    # is insufficient to pass zero fingering to the search core: structural
    # repairs also honour ``locked`` and would otherwise silently skip every
    # source-marked note.  Keep the original input untouched on disk, but make
    # the in-memory generation copy fully unanchored.
    if args.ignore_existing:
        for record in plan["notes"]:
            record["finger"] = 0
            record["locked"] = False
            record["source"] = "unassigned"
    # Preserve a same-hand rest boundary for postprocessing. A new note at a
    # rest ending begins a fresh hand position rather than a legato successor.
    rest_endings: dict[str, set[float]] = defaultdict(set)
    for rest in plan.get("rests", []):
        try:
            hand = str(rest["hand"]).upper()
            ending = round(float(rest["onset"]) + float(rest["duration"]), 8)
        except (KeyError, TypeError, ValueError):
            continue
        if hand in {"RH", "LH"}:
            rest_endings[hand].add(ending)
    for record in plan["notes"]:
        onset = round(float(record.get("onset", 0)), 8)
        hand = str(record.get("hand", "")).upper()
        record["preceding_rest"] = onset in rest_endings.get(hand, set())
    target_range = args.measure_range
    if args.changed_only:
        history = plan.get("recognition", {}).get("patch_history", [])
        if not history:
            parser.error("--changed-only requires recognition.patch_history")
        scope = history[-1].get("scope", {})
        explicit = {int(value) for value in scope.get("measures", [])}
        if explicit:
            affected = explicit
        else:
            pages = {int(value) for value in scope.get("pages", [])}
            hands = {str(value).upper() for value in scope.get("hands", [])}
            affected = {
                int(note["measure_index"])
                for note in plan.get("notes", [])
                if (not pages or int(note.get("page", 0)) in pages)
                and (not hands or str(note.get("hand", "")).upper() in hands)
            }
        if not affected:
            parser.error("latest recognition patch scope does not resolve to any measures")
        target_range = (min(affected), max(affected))
        if not args.quiet:
            print(f"Incremental regeneration: measures {target_range[0]}-{target_range[1]}", file=sys.stderr, flush=True)
    if target_range and plan.get("generation", {}).get("complete") is not True:
        parser.error(
            "--measure-range/--changed-only requires a previously validated full generated plan; "
            "run a complete generation once before applying a local patch"
        )
    if target_range:
        context_start = max(1, target_range[0] - args.context_measures)
        context_end = target_range[1] + args.context_measures
    else:
        context_start = context_end = 0
    read_only_context: dict[str, dict] = {}
    hand_timings: dict[str, dict[str, float | int]] = {}
    for record in plan["notes"]:
        measure = int(record["measure_index"])
        if target_range and not context_start <= measure <= context_end:
            continue
        if target_range and not target_range[0] <= measure <= target_range[1]:
            read_only_context[str(record["note_id"])] = copy.deepcopy(record)
        by_hand[record["hand"]].append(record)

    for hand_code, records in by_hand.items():
        records.sort(key=note_sort_key)
        sequence: list[INote] = []
        for record in records:
            finger = 0 if args.ignore_existing else int(record.get("finger", 0) or 0)
            note = INote(
                name=record.get("pitch_step"),
                pitch=int(record["pitch_midi"]),
                octave=int(record.get("pitch_octave", 0)),
                x=float(record["keyboard_x_cm"]),
                time=float(record["onset"]),
                duration=float(record["duration"]),
                fingering=finger,
                is_anchor=bool(finger and record.get("locked", False)),
                measure=int(record["measure_index"]),
                staff=int(record["staff"]),
                chordnr=int(record["chord_row"]),
                NinChord=int(record["chord_size"]),
                chordID=hash(str(record["chord_id"])) & 0x7FFFFFFF,
                noteID=len(sequence),
                isChord=int(record["chord_size"]) > 1,
                isBlack=int(record["pitch_midi"]) % 12 in {1, 3, 6, 8, 10},
            )
            sequence.append(note)
        if not sequence:
            continue
        solver = Hand(sequence, side="right" if hand_code == "RH" else "left", size=hand_size)
        solver.verbose = False
        solver.preserve_posture_memory = args.preserve_posture_memory
        solver.max_auto_depth = args.max_auto_depth
        if lookahead:
            solver.autodepth = False
            solver.depth = lookahead
        first_measure = min(int(item["measure_index"]) for item in records)
        last_measure = max(int(item["measure_index"]) for item in records)
        hand_started = time.perf_counter()
        last_bucket = -1

        def show_progress(done: int, total: int, measure: int) -> None:
            nonlocal last_bucket
            bucket = min(10, (done * 10) // max(1, total))
            if bucket <= last_bucket:
                return
            last_bucket = bucket
            print(
                f"{hand_code} {bucket * 10:3d}% ({done}/{total}, measure {measure})",
                file=sys.stderr,
                flush=True,
            )

        solver.generate(
            first_measure,
            last_measure - first_measure + 1,
            show_progress=None if args.quiet else show_progress,
        )
        hand_elapsed = time.perf_counter() - hand_started
        hand_timings[hand_code] = {
            "notes": len(records),
            "seconds": round(hand_elapsed, 4),
            "cache_hits": int(solver.cache_hits),
            "cache_misses": int(solver.cache_misses),
        }
        if not args.quiet:
            print(
                f"{hand_code} solved in {hand_elapsed:.2f}s "
                f"(cache {solver.cache_hits} hit/{solver.cache_misses} miss)",
                file=sys.stderr,
                flush=True,
            )
        for record, note in zip(records, sequence):
            existing = int(record.get("finger", 0) or 0)
            if existing and record.get("locked") and not args.ignore_existing:
                record["source"] = "existing"
            else:
                record["finger"] = int(note.fingering)
                record["source"] = "generated"
                record["locked"] = False
            record["cost"] = round(float(note.cost), 6)
            record["placement"] = "above" if hand_code == "RH" else "below"
        if args.global_phrase_candidate:
            optimize_connected_melody(records, hand_code, hand_size)
        postprocess(records, hand_code)
    for record in plan["notes"]:
        original = read_only_context.get(str(record.get("note_id")))
        if original is not None:
            record.clear()
            record.update(original)
    total_elapsed = time.perf_counter() - started_at
    plan["generation"] = {
        "complete": True,
        "mode": "incremental" if target_range else "full",
        "last_measure_range": list(target_range) if target_range else None,
        "hand_size": hand_size,
        "timing_seconds": round(total_elapsed, 4),
        "hands": hand_timings,
    }
    save_plan(args.output, plan)
    if target_range:
        changed = sum(
            1 for note in plan["notes"]
            if target_range[0] <= int(note["measure_index"]) <= target_range[1]
        )
        print(
            f"Wrote {args.output}; recomputed {changed} note(s) in measures "
            f"{target_range[0]}-{target_range[1]} with read-only context."
        )
    else:
        print(f"Wrote {args.output} with fingering for {len(plan['notes'])} notes.")
    if not args.quiet:
        print(f"Total generation time: {total_elapsed:.2f}s", file=sys.stderr, flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
