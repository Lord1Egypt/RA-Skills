#!/usr/bin/env python3
"""Run a reproducible low-to-intermediate piano fingering/placement regression.

The corpus contains public, standard major-scale fingerings plus elementary
left-hand accompaniment and tie cases.  It is a guardrail for level-5-and-
below building blocks, not a claim that every editorial fingering is unique.
"""

from __future__ import annotations

import argparse
import json
import sys
import struct
import zlib
from pathlib import Path

from fingering_core import Hand, INote
from fingering_core.models import keypos_midi
from generate_fingering_plan import chord_pattern, postprocess
from audit_phrase_risk import risk_for_run
from plan_io import save_plan
from create_plan_from_visual_facts import compile_notes
from validate_recognition import _validate_measure_evidence


MAJOR_ROOTS = {
    "C": 0, "Db": 1, "D": 2, "Eb": 3, "E": 4, "F": 5,
    "Gb": 6, "G": 7, "Ab": 8, "A": 9, "Bb": 10, "B": 11,
}
MAJOR_EXPECTED = {
    "C": ("12312345", "54321321"), "Db": ("23123412", "32143213"),
    "D": ("12312345", "54321321"), "Eb": ("31234123", "32143213"),
    "E": ("12312345", "54321321"), "F": ("12341234", "54321321"),
    "Gb": ("23412312", "43213214"), "G": ("12312345", "54321321"),
    "Ab": ("34123123", "32143213"), "A": ("12312345", "54321321"),
    "Bb": ("41231234", "32143213"), "B": ("12312345", "43214321"),
}
MAJOR_STEPS = (0, 2, 4, 5, 7, 9, 11, 12)
BLACK = {1, 3, 6, 8, 10}


def record(note: INote, hand: str, index: int) -> dict:
    return {
        "note_id": f"regression-{hand}-{index}", "measure_index": int(note.measure),
        "onset": float(note.time), "event_index": int(note.chordID),
        "chord_id": f"event-{note.chordID}", "chord_row": int(note.chordnr),
        "chord_size": int(note.NinChord), "pitch_midi": int(note.pitch),
        "finger": int(note.fingering), "locked": False,
        "placement": "above" if hand == "RH" else "below",
    }


def solve_and_postprocess(pitches: list[int], hand: str) -> list[dict]:
    notes = [INote(
        pitch=pitch, x=keypos_midi(INote(pitch=pitch)), time=float(index), duration=1.0,
        measure=1, chordnr=0, NinChord=1, chordID=index, isBlack=pitch % 12 in BLACK,
    ) for index, pitch in enumerate(pitches)]
    solver = Hand(notes, side="right" if hand == "RH" else "left", size="M")
    solver.verbose = False
    solver.max_auto_depth = 4
    solver.generate()
    rows = [record(note, hand, index) for index, note in enumerate(notes)]
    postprocess(rows, hand)
    return rows


def solve_melody_records(
    pitches: list[int],
    *,
    measures: list[int] | None = None,
    durations: list[float] | None = None,
) -> list[dict]:
    """Run the production RH solver before applying deterministic repairs.

    These cases are intentionally not post-processing-only fixtures: a user
    receives the result of both stages, and a regression must exercise both.
    """
    measures = measures or [1] * len(pitches)
    durations = durations or [1.0] * len(pitches)
    notes = [INote(
        pitch=pitch, x=keypos_midi(INote(pitch=pitch)), time=float(index), duration=durations[index],
        measure=measures[index], chordnr=0, NinChord=1, chordID=index, isBlack=pitch % 12 in BLACK,
    ) for index, pitch in enumerate(pitches)]
    solver = Hand(notes, side="right", size="M")
    solver.verbose = False
    solver.max_auto_depth = 4
    solver.generate()
    rows = [record(note, "RH", index) | {"duration": durations[index]} for index, note in enumerate(notes)]
    postprocess(rows, "RH")
    return rows


def scale_cases() -> tuple[int, int]:
    matches = total = 0
    for hand in ("RH", "LH"):
        for name, root in MAJOR_ROOTS.items():
            expected = MAJOR_EXPECTED[name][0 if hand == "RH" else 1]
            for pitches, target in (
                ([60 + root + step for step in MAJOR_STEPS], expected),
                ([60 + root + step for step in reversed(MAJOR_STEPS)], expected[::-1]),
            ):
                rows = solve_and_postprocess(pitches, hand)
                actual = "".join(str(row["finger"]) for row in rows)
                matches += sum(a == b for a, b in zip(actual, target))
                total += len(target)
    return matches, total


def accompaniment_cases() -> tuple[int, int]:
    matches = total = 0
    # Low bass + two identical dyads is the common elementary broken-chord
    # cell.  It tests the error that previously widened thirds to 4-1.
    for root in range(12):
        for span in (2, 3, 4, 5, 7):
            bass = 36 + root
            dyad = [bass + 7, bass + 7 + span]
            events = [[bass], dyad, dyad, [bass], dyad, dyad]
            rows = []
            for event_index, pitches in enumerate(events):
                for chord_row, pitch in enumerate(pitches):
                    rows.append({
                        "note_id": f"acc-{root}-{span}-{event_index}-{chord_row}", "measure_index": 1,
                        "onset": float(event_index), "event_index": event_index,
                        "chord_id": f"acc-{root}-{span}-{event_index}", "chord_row": chord_row,
                        "chord_size": len(pitches), "pitch_midi": pitch, "finger": 1,
                        "locked": False, "placement": "below",
                    })
            postprocess(rows, "LH")
            expected_dyad = chord_pattern([
                {"pitch_midi": dyad[0]}, {"pitch_midi": dyad[1]}
            ], "LH")
            expected = [5, *expected_dyad, *expected_dyad, 5, *expected_dyad, *expected_dyad]
            actual = [int(row["finger"]) for row in rows]
            matches += sum(a == b for a, b in zip(actual, expected))
            total += len(expected)
    return matches, total


def outer_bass_wide_dyad_cases() -> tuple[int, int]:
    """A close LH bass into a sixth/seventh dyad must not reuse finger 5."""
    matches = total = 0
    for root in range(12):
        bass = 36 + root
        dyad = [bass + 3, bass + 9]
        rows = []
        for event_index, pitches in enumerate(([bass], dyad, dyad)):
            for chord_row, pitch in enumerate(pitches):
                rows.append({
                    "note_id": f"outer-wide-{root}-{event_index}-{chord_row}", "measure_index": 1,
                    "onset": float(event_index), "event_index": event_index,
                    "chord_id": f"outer-wide-{root}-{event_index}", "chord_row": chord_row,
                    "chord_size": len(pitches), "pitch_midi": pitch, "finger": 1,
                    "locked": False, "placement": "below",
                })
        postprocess(rows, "LH")
        expected = [5, 4, 1, 4, 1]
        actual = [int(row["finger"]) for row in rows]
        matches += sum(a == b for a, b in zip(actual, expected))
        total += len(expected)
    return matches, total


def compact_triad_cases() -> tuple[int, int]:
    """Close LH major, minor, and diminished broken triads stay 5-3-2."""
    matches = total = 0
    for root in range(12):
        for gaps in ((3, 3), (3, 4), (4, 3)):
            pitches = [36 + root, 36 + root + gaps[0], 36 + root + sum(gaps)]
            rows = []
            for event_index, pitch in enumerate(pitches):
                rows.append({
                    "note_id": f"triad-{root}-{gaps}-{event_index}", "measure_index": 1,
                    "onset": float(event_index), "event_index": event_index,
                    "chord_id": f"triad-{root}-{gaps}-{event_index}", "chord_row": 0,
                    "chord_size": 1, "pitch_midi": pitch, "finger": 1,
                    "locked": False, "placement": "below",
                })
            postprocess(rows, "LH")
            actual = [int(row["finger"]) for row in rows]
            expected = [5, 3, 2]
            matches += sum(a == b for a, b in zip(actual, expected))
            total += len(expected)
    return matches, total


def diminished_reset_cases() -> tuple[int, int]:
    """A diminished 3-3 arpeggio resets as 5-3-1 before a new bass."""
    matches = total = 0
    for root in range(12):
        pitches = [36 + root, 39 + root, 42 + root, 35 + root]
        rows = []
        for event_index, pitch in enumerate(pitches):
            rows.append({
                "note_id": f"diminished-reset-{root}-{event_index}", "measure_index": 1,
                "onset": float(event_index), "event_index": event_index,
                "chord_id": f"diminished-reset-{root}-{event_index}", "chord_row": 0,
                "chord_size": 1, "pitch_midi": pitch, "finger": 1,
                "locked": False, "placement": "below",
            })
        postprocess(rows, "LH")
        actual = [int(row["finger"]) for row in rows[:3]]
        expected = [5, 3, 1]
        matches += sum(a == b for a, b in zip(actual, expected))
        total += len(expected)
    return matches, total


def sustained_reentry_descent_cases() -> tuple[int, int]:
    """RH held low note then upward re-entry/downward steps stays 1-4-3-2."""
    matches = total = 0
    for root in range(12):
        pitches = [60 + root, 67 + root, 65 + root, 63 + root]
        rows = solve_melody_records(pitches, measures=[1, 2, 2, 2], durations=[3.0, 1.0, 1.0, 1.0])
        actual = [int(row["finger"]) for row in rows]
        expected = [1, 4, 3, 2]
        matches += sum(a == b for a, b in zip(actual, expected))
        total += len(expected)
    return matches, total


def held_descending_tetrachord_cases() -> tuple[int, int]:
    """A RH held-start compact descent uses 4-3-2-1."""
    matches = total = 0
    for root in range(12):
        pitches = [67 + root, 65 + root, 62 + root, 60 + root]
        rows = solve_melody_records(pitches, durations=[1.5, 0.5, 0.5, 0.5])
        actual = [int(row["finger"]) for row in rows]
        expected = [4, 3, 2, 1]
        matches += sum(a == b for a, b in zip(actual, expected))
        total += len(expected)
    return matches, total


def slow_cross_barline_phrase_cases() -> tuple[int, int]:
    """A slow two-plus-two RH entry and lower-neighbour reply stay centred."""
    matches = total = 0
    for root in range(12):
        # The first four are a new phrase spanning two bars; the following
        # four are the compact lower-neighbour response.
        pitches = [65 + root, 64 + root, 62 + root, 61 + root, 59 + root, 57 + root, 59 + root, 61 + root]
        rows = solve_melody_records(pitches, measures=[1 + event_index // 2 for event_index in range(8)], durations=[2.0] * 8)
        actual = [int(row["finger"]) for row in rows]
        expected = [4, 3, 1, 3, 1, 2, 1, 2]
        matches += sum(a == b for a, b in zip(actual, expected))
        total += len(expected)
    return matches, total


def right_hand_compact_octave_arpeggio_cases() -> tuple[int, int]:
    """A compact RH 3rd-3rd-4th arpeggio reaching an octave stays 1-2-3-5."""
    matches = total = 0
    for root in range(12):
        pitches = [60 + root, 64 + root, 67 + root, 72 + root]
        rows = solve_melody_records(pitches, durations=[0.5] * 4)
        actual = [int(row["finger"]) for row in rows]
        expected = [1, 2, 3, 5]
        matches += sum(a == b for a, b in zip(actual, expected))
        total += len(expected)
    return matches, total


def right_hand_symmetric_arch_cases() -> tuple[int, int]:
    """A compact symmetric RH arch stays 1-2-3-5-3-2-1."""
    matches = total = 0
    for root in range(12):
        pitches = [60 + root, 63 + root, 65 + root, 69 + root, 65 + root, 63 + root, 60 + root]
        rows = solve_melody_records(pitches, durations=[0.5] * 7)
        actual = [int(row["finger"]) for row in rows]
        expected = [1, 2, 3, 5, 3, 2, 1]
        matches += sum(a == b for a, b in zip(actual, expected))
        total += len(expected)
    return matches, total


def right_hand_returning_thumb_fan_cases() -> tuple[int, int]:
    matches = total = 0
    for root, offsets, expected in (
        (72, (0, 5, 0, 10, 8), (1, 2, 1, 5, 4)),
        (72, (0, 3, 0, 6, 7), (1, 2, 1, 4, 5)),
    ):
        for transpose in range(12):
            rows = solve_melody_records(
                [root + transpose + offset for offset in offsets],
                durations=[0.5] * 5,
            )
            actual = [int(row["finger"]) for row in rows]
            matches += sum(left == right for left, right in zip(actual, expected))
            total += len(expected)
    return matches, total


def compact_five_key_position_cases() -> tuple[int, int]:
    matches = total = 0
    for transpose in range(12):
        pitches = [76, 76, 77, 76, 74, 76, 81, 79, 76]
        rows = solve_melody_records(
            [pitch + transpose for pitch in pitches],
            measures=[1, 1, 1, 2, 2, 2, 2, 2, 2],
            durations=[2.0, 0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        )
        rows[1]["preceding_rest"] = True
        postprocess(rows, "RH")
        expected = (2, 2, 3, 2, 1, 2, 5, 4, 2)
        actual = [int(row["finger"]) for row in rows]
        matches += sum(left == right for left, right in zip(actual, expected))
        total += len(expected)
    return matches, total


def elementary_measure_position_cases() -> tuple[int, int]:
    """Whole-bar cells reserve fingers from their complete local range."""
    matches = total = 0
    for transpose in range(12):
        for offsets, expected in (
            ((4, 2, 0), (4, 3, 2)),
            ((6, 7, 4), (1, 3, 1)),
            ((0, 5, 7, 9, 7, 5), (1, 2, 3, 4, 3, 2)),
            ((0, 3, 5, 7, 5, 7), (1, 2, 3, 4, 3, 4)),
        ):
            rows = solve_melody_records([60 + transpose + offset for offset in offsets])
            actual = [int(row["finger"]) for row in rows]
            matches += sum(left == right for left, right in zip(actual, expected))
            total += len(expected)

        lh_pitches = [60 + transpose, 58 + transpose, 54 + transpose]
        lh_rows = [
            {
                "note_id": f"lh-desc-{transpose}-{index}", "measure_index": 1,
                "onset": float(index), "event_index": index,
                "chord_id": f"lh-desc-{transpose}-{index}", "chord_row": 0,
                "chord_size": 1, "pitch_midi": pitch, "finger": 1,
                "locked": False, "placement": "below", "duration": 1.0,
            }
            for index, pitch in enumerate(lh_pitches)
        ]
        postprocess(lh_rows, "LH")
        actual = [int(row["finger"]) for row in lh_rows]
        expected = (1, 2, 5)
        matches += sum(left == right for left, right in zip(actual, expected))
        total += len(expected)

        chord = [{"pitch_midi": 60 + transpose + offset} for offset in (0, 3, 9)]
        actual = chord_pattern(chord, "RH")
        expected = (1, 2, 5)
        matches += sum(left == right for left, right in zip(actual, expected))
        total += len(expected)
    return matches, total


def wide_skip_reset_cases() -> tuple[int, int]:
    """A wide LH skip plus a third uses 5-3-1 before the bass resets.

    This is deliberately separate from ordinary major/minor broken triads:
    its lower-sixth plus upper-third shape has a different physical reach.
    """
    matches = total = 0
    for root in range(12):
        pitches = [36 + root, 42 + root, 45 + root, 36 + root]
        rows = []
        for event_index, pitch in enumerate(pitches):
            rows.append({
                "note_id": f"wide-reset-{root}-{event_index}", "measure_index": 1,
                "onset": float(event_index), "event_index": event_index,
                "chord_id": f"wide-reset-{root}-{event_index}", "chord_row": 0,
                "chord_size": 1, "pitch_midi": pitch, "finger": 1,
                "locked": False, "placement": "below",
            })
        postprocess(rows, "LH")
        # The fourth note supplies the reset context; its fingering is not
        # prescribed by this narrowly scoped triad-shape assertion.
        actual = [int(row["finger"]) for row in rows[:3]]
        expected = [5, 3, 1]
        matches += sum(a == b for a, b in zip(actual, expected))
        total += len(expected)
    return matches, total


def tie_cases() -> tuple[int, int]:
    matches = total = 0
    for hand in ("RH", "LH"):
        rows = []
        for index, pitch in enumerate((60, 60, 62, 62, 64, 64)):
            rows.append({
                "note_id": f"tie-{hand}-{index}", "measure_index": 1, "onset": float(index),
                "event_index": index, "chord_id": f"tie-event-{index}", "chord_row": 0,
                "chord_size": 1, "pitch_midi": pitch, "finger": 1 + (index % 5),
                "locked": False, "placement": "above" if hand == "RH" else "below",
                "tie_group": f"tie-{hand}-{index // 2}",
            })
        before = [int(row["finger"]) for row in rows]
        postprocess(rows, hand)
        expected = [before[0], before[0], before[2], before[2], before[4], before[4]]
        actual = [int(row["finger"]) for row in rows]
        matches += sum(a == b for a, b in zip(actual, expected))
        total += len(expected)
    return matches, total


def postprocess_repeated_pitch_invariant_cases() -> tuple[int, int]:
    """A final different-pitch repair must not create an unrequested substitution.

    The first repeated note follows a changed phrase-entry finger.  This is the
    ordering edge case that used to leave the repeated attacks on a different
    digit after the earlier repeated-note pass had already run.
    """
    matches = total = 0
    for root in range(12):
        pitches = [60 + root, 67 + root, 67 + root, 69 + root, 67 + root, 65 + root, 64 + root, 64 + root, 64 + root]
        rows = []
        for event_index, pitch in enumerate(pitches):
            rows.append({
                "note_id": f"repeat-final-{root}-{event_index}", "measure_index": 1,
                "onset": float(event_index), "event_index": event_index,
                "chord_id": f"repeat-final-{root}-{event_index}", "chord_row": 0,
                "chord_size": 1, "pitch_midi": pitch, "duration": 1.0, "finger": 2,
                "locked": False, "placement": "above",
            })
        postprocess(rows, "RH")
        for previous, current in zip(rows, rows[1:]):
            if int(previous["pitch_midi"]) != int(current["pitch_midi"]):
                continue
            total += 1
            matches += int(previous["finger"]) == int(current["finger"])
    return matches, total


def identical_measure_fingering_cases() -> tuple[int, int]:
    """Literal repeated measures retain one complete fingering pattern.

    This guards a whole-phrase usability invariant rather than one interval:
    a locally valid search must not give the same written bar two unexplained
    hand shapes merely because it appears later in the piece.
    """
    rows = []
    pitches = (60, 62, 64, 65)
    seeds = ((1, 2, 3, 4), (2, 3, 4, 5))
    for measure, fingers in enumerate(seeds, start=1):
        for position, (pitch, finger) in enumerate(zip(pitches, fingers)):
            event_index = (measure - 1) * len(pitches) + position
            rows.append({
                "note_id": f"literal-repeat-{measure}-{position}",
                "measure_index": measure, "onset": float(event_index),
                "event_index": event_index, "chord_id": f"literal-repeat-event-{event_index}",
                "chord_row": 0, "chord_size": 1, "pitch_midi": pitch,
                "duration": 1.0, "finger": finger, "locked": False,
                "placement": "above",
            })
    postprocess(rows, "RH")
    first = [int(row["finger"]) for row in rows[:4]]
    second = [int(row["finger"]) for row in rows[4:]]
    return sum(left == right for left, right in zip(first, second)), len(first)


def cross_voice_visual_event_cases() -> tuple[int, int]:
    """Same-onset visual voices must form one physical chord event.

    A recurring source of impossible finger reuse was treating a notation
    voice as a piano hand event.  Keep this small schema-level check beside
    the musical regressions: it uses two distinct voices at the same visual
    onset and asserts that the compiler produces one low-to-high chord.
    """
    raw = [
        {
            "page": 1, "measure_index": 1, "staff": 1, "voice": "1", "hand": "RH",
            "onset": 0, "duration": 1, "pitch_step": "C", "pitch_alter": 0, "pitch_octave": 4,
            "page_x": 100, "page_y": 200,
        },
        {
            "page": 1, "measure_index": 1, "staff": 1, "voice": "2", "hand": "RH",
            "onset": 0, "duration": 1, "pitch_step": "E", "pitch_alter": 0, "pitch_octave": 4,
            "page_x": 100, "page_y": 180,
        },
    ]
    rows = compile_notes(raw, [])
    checks = (
        len({row["chord_id"] for row in rows}) == 1,
        [row["chord_size"] for row in rows] == [2, 2],
        [row["chord_row"] for row in rows] == [0, 1],
        len({row["event_index"] for row in rows}) == 1,
    )
    return sum(checks), len(checks)


def visual_event_topology_gate_cases() -> tuple[int, int]:
    """The independent event topology must reject a split chord."""
    scope = (1, 1, "RH")
    region = {
        "region_id": "p1-m001-rh", "page": 1, "measure": 1, "hand": "RH",
        "bbox": [0, 0, 200, 200], "evidence_crop": "fixture.png",
    }
    check = {
        "region_id": "p1-m001-rh", "page": 1, "measure": 1, "hand": "RH",
        "verified": True, "duration_verified": True, "source": "independent_visual_review",
        "evidence_crop": "fixture.png", "expected_noteheads": 2, "expected_rests": 0,
        "expected_attack_events": 1, "expected_chord_sizes": [2],
    }
    notes = [
        {"page": 1, "measure_index": 1, "hand": "RH", "staff": 1, "onset": 0, "page_x": 100, "page_y": y}
        for y in (100, 120)
    ]
    plan = {
        "notes": notes, "rests": [],
        "recognition": {
            "measure_scope": [{"page": 1, "measure_start": 1, "measure_end": 1, "hands": ["RH"]}],
            "measure_regions": [region], "measure_symbol_checks": [check],
        },
    }
    policy = {
        "require_measure_region_coverage": True, "require_measure_symbol_checks": True,
        "require_rest_inventory": False, "require_event_topology": True,
    }
    correct = not _validate_measure_evidence(plan, policy)
    plan["recognition"]["measure_symbol_checks"][0]["expected_attack_events"] = 2
    plan["recognition"]["measure_symbol_checks"][0]["expected_chord_sizes"] = [1, 1]
    split_rejected = bool(_validate_measure_evidence(plan, policy))
    return int(correct) + int(split_rejected), 2


def phrase_risk_gate_cases() -> tuple[int, int]:
    """Long connected melody must not silently pass an unexplained hand reset."""
    events = []
    for index, pitch in enumerate((60, 62, 64, 65)):
        events.append([{
            "note_id": f"phrase-risk-{index}", "page": 1, "measure_index": 1,
            "hand": "RH", "pitch_midi": pitch, "finger": index + 1,
            "onset": float(index), "duration": 1.0,
            "transition_type": "lateral_shift" if index == 2 else "",
        }])
    flagged = len(risk_for_run(events, 4)) == 1
    events[2][0]["review_decision"] = "verified local phrase entry"
    cleared_after_review = not risk_for_run(events, 4)
    return int(flagged) + int(cleared_after_review), 2


def slow_phrase_shape_risk_cases() -> tuple[int, int]:
    """Known ambiguous slow RH contours must be delivered for local review."""
    fixtures = (
        ([60, 67, 65, 63], [1, 2, 2, 2], [3.0, 1.0, 1.0, 1.0]),
        ([67, 65, 62, 60], [1, 1, 1, 1], [1.5, 0.5, 0.5, 0.5]),
        ([65, 64, 62, 61], [1, 1, 2, 2], [2.0, 2.0, 2.0, 2.0]),
    )
    matches = total = 0
    for pitches, measures, durations in fixtures:
        rows = solve_melody_records(pitches, measures=measures, durations=durations)
        for row in rows:
            row["hand"] = "RH"
        flagged = len(risk_for_run([[row] for row in rows], 4)) == 1
        matches += int(flagged)
        total += 1
    # The risky contour may begin in the middle of one longer legato run;
    # it still needs a page/measure/hand review scope rather than being hidden
    # behind the run's harmless opening notes.
    rows = solve_melody_records(
        [72, 74, 76, 60, 67, 65, 63],
        measures=[1, 1, 1, 1, 2, 2, 2],
        durations=[1.0, 1.0, 1.0, 3.0, 1.0, 1.0, 1.0],
    )
    for row in rows:
        row["hand"] = "RH"
    later_risks = risk_for_run([[row] for row in rows], 4)
    matches += int(len(later_risks) == 1 and later_risks[0]["note_id"] == rows[4]["note_id"])
    total += 1
    return matches, total


def placement_plan() -> dict:
    notes = []
    for index in range(120):
        x = 30 + index * 16
        notes.append({
            "note_id": f"placement-{index}", "part": "P1", "measure": str(index + 1),
            "measure_index": index + 1, "staff": 1, "voice": "1", "onset": 0,
            "duration": 1, "pitch_midi": 60 + (index % 12), "pitch_step": "C",
            "pitch_alter": 0, "pitch_octave": 4, "event_index": index,
            "chord_id": f"placement-event-{index}", "chord_row": 0, "chord_size": 1,
            "hand": "RH", "keyboard_x_cm": 0, "finger": 1 + (index % 5),
            "placement": "above", "page": 1, "page_x": x, "page_y": 220,
            "label_offset": 20, "font_size": 10, "anchor_verified": True,
            "staff_geometry_id": "system-1",
        })
    # The placement audit deliberately uses only page geometry; it does not
    # need semantic pitch validation, so fixed pitch fields are sufficient.
    return {
        "schema_version": "1.0", "source": {"type": "image", "coordinate_unit": "pixel_top_left"},
        "pages": [{"page": 1, "width": 2000, "height": 500}],
        "recognition": {"systems": [{"system_id": "system-1", "staff_line_y": [200, 210, 220, 230, 240]}]},
        "notes": notes,
    }


def write_white_png(path: Path, width: int = 2000, height: int = 500) -> None:
    """Create a deterministic RGB source page for the post-render label test."""
    rows = b"".join(b"\x00" + b"\xff\xff\xff" * width for _ in range(height))
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    payload = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    payload += chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b"")
    path.write_bytes(payload)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--minimum", type=float, default=0.80)
    parser.add_argument(
        "--group-minimum", type=float, default=0.80,
        help="minimum accuracy for every named musical pattern group (default: 0.80)",
    )
    args = parser.parse_args()
    if not 0 < args.minimum <= 1 or not 0 < args.group_minimum <= 1:
        parser.error("--minimum and --group-minimum must be in (0, 1]")
    groups = {
        "standard_major_scales": scale_cases(),
        "elementary_lh_broken_chords": accompaniment_cases(),
        "lh_outer_bass_wide_dyads": outer_bass_wide_dyad_cases(),
        "elementary_lh_broken_triads": compact_triad_cases(),
        "elementary_lh_diminished_resets": diminished_reset_cases(),
        "rh_sustained_reentry_descents": sustained_reentry_descent_cases(),
        "rh_held_descending_tetrachords": held_descending_tetrachord_cases(),
        "rh_slow_cross_barline_phrases": slow_cross_barline_phrase_cases(),
        "rh_compact_octave_arpeggios": right_hand_compact_octave_arpeggio_cases(),
        "rh_symmetric_compact_arches": right_hand_symmetric_arch_cases(),
        "rh_returning_thumb_fans": right_hand_returning_thumb_fan_cases(),
        "compact_five_key_positions": compact_five_key_position_cases(),
        "elementary_measure_position_cells": elementary_measure_position_cases(),
        "elementary_lh_wide_skip_resets": wide_skip_reset_cases(),
        "tied_note_invariants": tie_cases(),
        "postprocess_repeated_pitch_invariants": postprocess_repeated_pitch_invariant_cases(),
        "identical_measure_fingering_invariants": identical_measure_fingering_cases(),
        "cross_voice_visual_event_normalization": cross_voice_visual_event_cases(),
        "visual_event_topology_gate": visual_event_topology_gate_cases(),
        "phrase_reposition_review_gate": phrase_risk_gate_cases(),
        "slow_phrase_shape_review_gate": slow_phrase_shape_risk_cases(),
    }
    matches = sum(pair[0] for pair in groups.values())
    total = sum(pair[1] for pair in groups.values())
    group_rows = {
        name: {"matches": matched, "notes": count, "accuracy": matched / count}
        for name, (matched, count) in groups.items()
    }
    failing_groups = [
        {"id": name, **row}
        for name, row in group_rows.items()
        if row["accuracy"] < args.group_minimum
    ]
    aggregate_accuracy = matches / total
    report = {
        "scope": "level-5-and-below foundational technical patterns",
        "metric": "exact reference-finger agreement",
        "quality_policy": (
            "The aggregate is a coverage summary only. A passing aggregate cannot hide a failed "
            "named musical pattern group."
        ),
        "sources": [
            "https://piano.org/theory/piano-fingering/ (public standard major-scale patterns)",
            "references/professional-fingering-rules.md (dyad, tie, and accompaniment invariants)",
        ],
        "groups": group_rows,
        "matches": matches, "notes": total, "fingering_accuracy": aggregate_accuracy,
        "minimums": {"aggregate": args.minimum, "each_group": args.group_minimum},
        "aggregate_passed": aggregate_accuracy >= args.minimum,
        "failing_groups": failing_groups,
        "passed": aggregate_accuracy >= args.minimum and not failing_groups,
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    placement = placement_plan()
    write_white_png(args.out_dir / "placement-source.png")
    placement["pages"][0]["image"] = "placement-source.png"
    save_plan(args.out_dir / "placement-regression-plan.json", placement)
    (args.out_dir / "level5-fingering-regression.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
