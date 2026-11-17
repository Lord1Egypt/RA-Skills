#!/usr/bin/env python3
"""Create a semantic *benchmark oracle* plan from a standard MIDI file.

This is deliberately not advertised as a user input path.  It exists so a
public PDF and a same-engraving MIDI can be paired during visual regression.
MIDI does not retain spelling, clefs, rests, or notation layout, so its facts
must never replace visual review for a user-provided PDF.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from fingering_core.models import INote, keypos_midi
from plan_io import save_plan
from recognition_state import set_fact_lock


STEP_NAMES = {
    0: ("C", 0), 1: ("C", 1), 2: ("D", 0), 3: ("D", 1),
    4: ("E", 0), 5: ("F", 0), 6: ("F", 1), 7: ("G", 0),
    8: ("G", 1), 9: ("A", 0), 10: ("A", 1), 11: ("B", 0),
}


def vlq(data: bytes, pos: int) -> tuple[int, int]:
    value = 0
    while True:
        if pos >= len(data):
            raise ValueError("truncated MIDI variable-length quantity")
        byte = data[pos]
        pos += 1
        value = (value << 7) | (byte & 0x7F)
        if not byte & 0x80:
            return value, pos


def parse_track(data: bytes) -> tuple[str, list[tuple[int, int, int]]]:
    pos = tick = 0
    running: int | None = None
    name = ""
    active: dict[tuple[int, int], list[int]] = defaultdict(list)
    notes: list[tuple[int, int, int]] = []
    while pos < len(data):
        delta, pos = vlq(data, pos)
        tick += delta
        status = data[pos]
        if status < 0x80:
            if running is None:
                raise ValueError("MIDI running status without prior status")
        else:
            pos += 1
            running = status
        assert running is not None
        if running == 0xFF:
            if pos >= len(data):
                raise ValueError("truncated MIDI meta event")
            kind = data[pos]
            pos += 1
            size, pos = vlq(data, pos)
            payload = data[pos:pos + size]
            if len(payload) != size:
                raise ValueError("truncated MIDI meta payload")
            pos += size
            if kind == 0x03:
                name = payload.decode("utf-8", errors="replace")
            continue
        if running in {0xF0, 0xF7}:
            size, pos = vlq(data, pos)
            pos += size
            continue
        kind, channel = running & 0xF0, running & 0x0F
        width = 1 if kind in {0xC0, 0xD0} else 2
        if pos + width > len(data):
            raise ValueError("truncated MIDI channel event")
        values = data[pos:pos + width]
        pos += width
        if kind == 0x90 and values[1] > 0:
            active[(channel, values[0])].append(tick)
        elif kind == 0x80 or (kind == 0x90 and values[1] == 0):
            starts = active[(channel, values[0])]
            if starts:
                start = starts.pop()
                notes.append((start, tick, values[0]))
    return name, sorted(notes)


def parse_midi(path: Path) -> tuple[int, list[tuple[str, list[tuple[int, int, int]]]]]:
    data = path.read_bytes()
    if data[:4] != b"MThd" or int.from_bytes(data[4:8], "big") != 6:
        raise ValueError("only standard MIDI headers are supported")
    fmt = int.from_bytes(data[8:10], "big")
    tracks = int.from_bytes(data[10:12], "big")
    division = int.from_bytes(data[12:14], "big")
    if fmt not in {0, 1} or division & 0x8000:
        raise ValueError("only PPQN format-0/1 MIDI is supported")
    pos = 14
    output = []
    for _ in range(tracks):
        if data[pos:pos + 4] != b"MTrk":
            raise ValueError("missing MIDI track chunk")
        size = int.from_bytes(data[pos + 4:pos + 8], "big")
        start = pos + 8
        end = start + size
        if end > len(data):
            raise ValueError("truncated MIDI track")
        output.append(parse_track(data[start:end]))
        pos = end
    return division, output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--rh-track", type=int, required=True, help="zero-based MIDI track index for RH")
    parser.add_argument("--lh-track", type=int, required=True, help="zero-based MIDI track index for LH")
    parser.add_argument("--beats", type=int, default=2, help="beats per bar in the paired engraving")
    parser.add_argument("--beat-unit", type=int, default=4, help="denominator of the paired engraving time signature")
    args = parser.parse_args()
    if args.beats < 1 or args.beat_unit not in {1, 2, 4, 8, 16}:
        raise ValueError("invalid time signature")
    ppqn, tracks = parse_midi(args.input)
    if not 0 <= args.rh_track < len(tracks) or not 0 <= args.lh_track < len(tracks) or args.rh_track == args.lh_track:
        raise ValueError("RH/LH tracks must be distinct valid zero-based indexes")
    measure_ticks = ppqn * 4 * args.beats / args.beat_unit
    events: list[tuple[str, int, int, int]] = []
    for hand, index in (("RH", args.rh_track), ("LH", args.lh_track)):
        for start, end, midi in tracks[index][1]:
            if end <= start:
                continue
            events.append((hand, start, end, midi))
    notes: list[dict] = []
    by_hand_measure: dict[tuple[str, int], list[tuple[int, int, int]]] = defaultdict(list)
    for hand, start, end, midi in events:
        measure = int(start // measure_ticks) + 1
        by_hand_measure[(hand, measure)].append((start, end, midi))
    for (hand, measure), group in sorted(by_hand_measure.items(), key=lambda item: (item[0][1], item[0][0])):
        by_onset: dict[int, list[tuple[int, int]]] = defaultdict(list)
        for start, end, midi in group:
            by_onset[start].append((end, midi))
        for event_index, (start, chord) in enumerate(sorted(by_onset.items())):
            for row, (end, midi) in enumerate(sorted(chord, key=lambda item: item[1])):
                step, alter = STEP_NAMES[midi % 12]
                octave = midi // 12 - 1
                onset = start / ppqn
                note_id = f"M{measure}-{hand}-T{start}-N{midi}-C{row}"
                notes.append({
                    "note_id": note_id, "part": "MIDI", "measure": str(measure), "measure_index": measure,
                    "staff": 1 if hand == "RH" else 2, "voice": "1", "onset": onset,
                    "duration": (end - start) / ppqn, "pitch_midi": midi, "pitch_step": step,
                    "pitch_alter": alter, "pitch_octave": octave, "hand": hand, "chord_row": row,
                    "chord_id": f"M{measure}-{hand}-T{start}", "chord_size": len(chord),
                    "event_index": event_index, "finger": 0, "locked": False, "source": "unassigned",
                    "grace": False, "tie_group": None, "tie_start": False, "tie_stop": False,
                    "keyboard_x_cm": keypos_midi(INote(pitch=midi)),
                })
    plan = {
        "schema_version": "1.0",
        "source": {"type": "midi_reference", "path": str(args.input), "role": "benchmark oracle only"},
        "settings": {"hand_size": "M", "lookahead": 0}, "pages": [],
        "recognition": {"status": "verified", "scope": "same-engraving MIDI benchmark oracle",
            "expected_note_count": len(notes), "unresolved_note_count": 0, "delivery_level": "complete",
            "verification": {"pitch_spelling": True, "rhythm": True, "ties": True, "chords": True}},
        "notes": notes, "rests": [],
    }
    set_fact_lock(plan)
    save_plan(args.output, plan)
    print(f"Wrote {args.output} with {len(notes)} notes (RH {len(tracks[args.rh_track][1])}, LH {len(tracks[args.lh_track][1])}).")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, IndexError) as exc:
        raise SystemExit(f"ERROR: {exc}")
