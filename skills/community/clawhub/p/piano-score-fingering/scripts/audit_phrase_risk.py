#!/usr/bin/env python3
"""Flag long connected melodic phrases that contain an unexplained hand reset.

This is deliberately a confidence gate, not a second fingering engine.  Two
bounded searches can agree on the same locally cheap solution while still
making a debatable phrase-entry or cross-bar hand-position choice.  The audit
therefore makes that specific situation visible in the delivery report instead
of presenting it as an unqualified final result.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from plan_io import load_plan, note_sort_key


def event_key(note: dict) -> tuple:
    """Return a physical event identity without confusing staff voices for notes."""
    return (
        str(note.get("part", "")),
        int(note["measure_index"]),
        float(note["onset"]),
        int(note.get("event_index", 0)),
        str(note.get("chord_id", "")),
    )


def connected(previous: list[dict], current: list[dict]) -> bool:
    """Whether two singleton events are a continuous melodic phrase."""
    if len(previous) != 1 or len(current) != 1:
        return False
    earlier, later = previous[0], current[0]
    if later.get("preceding_rest") or later.get("connection") == "detached":
        return False
    if later.get("tie_group") and later.get("tie_group") == earlier.get("tie_group"):
        return True
    end = float(earlier["onset"]) + float(earlier.get("duration", 0))
    return float(later["onset"]) <= end + 1.0e-6


def stable_broken_chord_accompaniment(events: list[list[dict]]) -> bool:
    """Recognise a repeated LH 5-3-2-1 arpeggio accompaniment, not a melody.

    A four-note broken-chord pattern can be notated as nothing but singleton
    events.  Treating an entire ostinato as one 100-note melodic phrase made
    an ordinary, already stable left hand produce a meaningless risk warning.
    Require two full cells and a high proportion of matching cells so an
    irregular left-hand melody does not evade review.
    """
    if len(events) < 8 or any(len(event) != 1 for event in events):
        return False
    notes = [event[0] for event in events]
    if any(str(note.get("hand", "")).upper() != "LH" for note in notes):
        return False
    cells = [notes[index:index + 4] for index in range(0, len(notes) - 3, 4)]
    if len(cells) < 2:
        return False
    matched = 0
    for cell in cells:
        fingers = [int(note.get("finger", 0)) for note in cell]
        pitches = [int(note["pitch_midi"]) for note in cell]
        if fingers == [5, 3, 2, 1] and all(right > left for left, right in zip(pitches, pitches[1:])):
            matched += 1
    return matched / len(cells) >= 0.75


def within_stable_broken_chord_cell(events: list[list[dict]], index: int) -> bool:
    """Whether one event sits in two neighbouring LH 5-3-2-1 arpeggio cells."""
    for start in range(max(0, index - 6), min(index + 1, len(events) - 7)):
        first = [event[0] for event in events[start:start + 4]]
        second = [event[0] for event in events[start + 4:start + 8]]
        if len(first) != 4 or len(second) != 4:
            continue
        if any(str(note.get("hand", "")).upper() != "LH" for note in first + second):
            continue
        def stable(cell: list[dict]) -> bool:
            return (
                [int(note.get("finger", 0)) for note in cell] == [5, 3, 2, 1]
                and all(int(right["pitch_midi"]) > int(left["pitch_midi"])
                        for left, right in zip(cell, cell[1:]))
            )
        if stable(first) and stable(second) and start <= index < start + 8:
            return True
    return False


def slow_phrase_shape_risk(events: list[list[dict]]) -> dict | None:
    """Recognise slow RH contours with more than one credible hand position.

    These are deliberately *confidence* patterns rather than replacement
    templates.  A local search commonly returns an edge-of-hand descent such
    as 5-4-3-2, while a centred 4-3-2(-1) or a thumb-crossing alternative can
    be preferable depending on the phrase that follows.  Applying one of
    those choices globally made unrelated music regress; silently accepting
    the local answer is worse.  Report one concrete entry note so a host can
    compare the cropped source and adjacent measures before delivery.
    """
    if len(events) < 4 or any(len(event) != 1 for event in events):
        return None
    notes = [event[0] for event in events]
    if any(str(note.get("hand", "")).upper() != "RH" for note in notes):
        return None
    if any(note.get("locked") or note.get("review_decision") for note in notes[:4]):
        return None

    def row(note: dict, reason: str) -> dict:
        return {
            "note_id": str(note["note_id"]),
            "page": int(note.get("page", 0) or 0),
            "measure": int(note["measure_index"]),
            "hand": "RH",
            "pitch_midi": int(note["pitch_midi"]),
            "finger": int(note.get("finger", 0)),
            "phrase_events": len(events),
            "reason": reason,
        }

    first = notes[:4]
    pitches = [int(note["pitch_midi"]) for note in first]
    deltas = [right - left for left, right in zip(pitches, pitches[1:])]
    measures = [int(note["measure_index"]) for note in first]
    durations = [float(note.get("duration", 0)) for note in first]

    # A held entry with a compact descent: both an edge fingering and a
    # centred 4-3-2-1 solution can be valid, so use its continuation to decide.
    if (
        len(set(measures)) == 1
        and durations[0] >= 1.5
        and all(-3 <= delta <= -1 for delta in deltas)
        and 6 <= pitches[0] - pitches[-1] <= 8
    ):
        return row(first[0], "slow held RH descent has competing centred and edge-of-hand fingerings")

    # A phrase that starts with two long notes on each side of a barline should
    # not be treated as four unrelated local transitions.
    if (
        measures == [measures[0], measures[0], measures[0] + 1, measures[0] + 1]
        and all(duration >= 1.5 for duration in durations)
        and all(-2 <= delta <= -1 for delta in deltas)
        and 4 <= pitches[0] - pitches[-1] <= 7
    ):
        return row(first[0], "slow cross-barline RH descent requires phrase-level hand-position review")

    # The sustained note belongs to the previous bar; the leap and following
    # three notes are a new small phrase with two plausible landing positions.
    if len(notes) >= 4:
        prior, entry, second, third = notes[:4]
        entry_steps = (
            int(second["pitch_midi"]) - int(entry["pitch_midi"]),
            int(third["pitch_midi"]) - int(second["pitch_midi"]),
        )
        if (
            int(entry["measure_index"]) != int(prior["measure_index"])
            and len({int(note["measure_index"]) for note in (entry, second, third)}) == 1
            and float(prior.get("duration", 0)) >= 1.0
            and 5 <= int(entry["pitch_midi"]) - int(prior["pitch_midi"]) <= 12
            and all(-2 <= step <= -1 for step in entry_steps)
        ):
            return row(entry, "sustained re-entry RH descent requires centred landing-position review")
    return None


def risk_for_run(events: list[list[dict]], minimum_events: int) -> list[dict]:
    """Return one concrete review row for an unreviewed phrase transition.

    The generator does not always spell a lateral reset as ``transition_type``.
    Inferring it from the pitch/finger directions catches an important class of
    silent errors: a connected line reverses the finger order without either
    side of the move using the thumb.  This is not declared impossible -- a
    pianist may deliberately reposition -- but it is precisely the kind of
    long-phrase choice the caller should see rather than receive as certain.
    """
    if len(events) < minimum_events:
        return []
    if stable_broken_chord_accompaniment(events):
        return []
    # A long legato run can contain several independently ambiguous entries.
    # Looking only at its first four notes used to let a later held descent or
    # re-entry pass as an ordinary local transition.  Scan four-note windows,
    # but deduplicate their entry notes so overlapping windows do not flood the
    # review queue.
    phrase_shapes: list[dict] = []
    seen_entries: set[str] = set()
    for start in range(len(events) - 3):
        phrase_shape = slow_phrase_shape_risk(events[start:start + 4])
        if phrase_shape is None:
            continue
        note_id = str(phrase_shape["note_id"])
        if note_id in seen_entries:
            continue
        seen_entries.add(note_id)
        phrase_shapes.append(phrase_shape)
    if phrase_shapes:
        return phrase_shapes
    # The remaining generic heuristic infers an unannounced lateral reset
    # from pitch/finger direction alone. It is meaningful for a RH melodic
    # line, but creates many false warnings in LH accompaniment patterns that
    # are neither a 5-3-2-1 ostinato nor a literal repeated cell. LH has its
    # own hard accompaniment/chord checks; do not bury the few actionable RH
    # phrase reviews under generic LH noise.
    if str(events[0][0].get("hand", "")).upper() != "RH":
        return []
    rows: list[dict] = []
    for index, event in enumerate(events):
        note = event[0]
        if within_stable_broken_chord_cell(events, index):
            continue
        if note.get("locked") or note.get("review_decision"):
            continue
        transition = str(note.get("transition_type", ""))
        reason = str(note.get("exception_reason", ""))
        explicit_lateral = transition == "lateral_shift" or "phrase-level hand reposition" in reason
        inferred_nonthumb_reverse = False
        if index:
            prior = events[index - 1][0]
            if not prior.get("locked") and not prior.get("review_decision"):
                pitch_delta = int(note["pitch_midi"]) - int(prior["pitch_midi"])
                finger_delta = int(note.get("finger", 0)) - int(prior.get("finger", 0))
                hand = str(note["hand"]).upper()
                natural_sign = 1 if (pitch_delta > 0) == (hand == "RH") else -1
                has_thumb = int(prior.get("finger", 0)) == 1 or int(note.get("finger", 0)) == 1
                inferred_nonthumb_reverse = (
                    pitch_delta != 0
                    and finger_delta != 0
                    and finger_delta * natural_sign < 0
                    and not has_thumb
                    and transition not in {"leap", "substitution"}
                )
        if not explicit_lateral and not inferred_nonthumb_reverse:
            continue
        trigger = (
            "connected melodic phrase contains an unreviewed non-thumb reverse finger move"
            if inferred_nonthumb_reverse else
            "connected melodic phrase contains an unreviewed lateral hand reposition"
        )
        rows.append({
            "note_id": str(note["note_id"]),
            "page": int(note.get("page", 0) or 0),
            "measure": int(note["measure_index"]),
            "hand": str(note["hand"]).upper(),
            "pitch_midi": int(note["pitch_midi"]),
            "finger": int(note.get("finger", 0)),
            "phrase_events": len(events),
            "reason": trigger,
        })
        # One decision point is enough to review a phrase entry. Emitting every
        # later lateral move made ordinary long scores look wholly unusable and
        # did not give the reviewer any additional musical information.
        break
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--minimum-events", type=int, default=4,
                        help="minimum continuous singleton events for a phrase-risk check (default: 4)")
    args = parser.parse_args()
    if not 3 <= args.minimum_events <= 16:
        parser.error("--minimum-events must be 3..16")

    plan = load_plan(args.plan)
    by_hand: dict[str, list[dict]] = defaultdict(list)
    for note in plan.get("notes", []):
        by_hand[str(note["hand"]).upper()].append(note)

    risks: list[dict] = []
    for notes in by_hand.values():
        grouped: dict[tuple, list[dict]] = defaultdict(list)
        for note in notes:
            grouped[event_key(note)].append(note)
        events = [sorted(event, key=note_sort_key) for _, event in sorted(grouped.items())]
        run: list[list[dict]] = []
        for event in events:
            if run and not connected(run[-1], event):
                risks.extend(risk_for_run(run, args.minimum_events))
                run = []
            run.append(event)
        risks.extend(risk_for_run(run, args.minimum_events))

    by_scope: dict[tuple[int, int, str], list[str]] = defaultdict(list)
    for row in risks:
        by_scope[(row["page"], row["measure"], row["hand"])].append(row["note_id"])
    report = {
        "metric": "unreviewed lateral reposition inside a connected melodic phrase (confidence gate, not editorial ground truth)",
        "minimum_events": args.minimum_events,
        "passed": not risks,
        "risk_notes": risks,
        "review_scopes": [
            {"page": page, "measure": measure, "hand": hand,
             "risk_notes": len(note_ids), "note_ids": note_ids}
            for (page, measure, hand), note_ids in sorted(by_scope.items())
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
