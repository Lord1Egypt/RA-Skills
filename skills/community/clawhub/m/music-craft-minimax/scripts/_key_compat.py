#!/usr/bin/env python3
"""_key_compat.py — Shared utilities for key compatibility and mashup scoring.

Key distance is computed on the circle of fifths. Two keys are compatible
if they are within 2 fifths (a perfect fourth) of each other. Larger
distances require the LLM to decide whether to transpose one song.

BPM compatibility is computed as a ratio. Mashups work best when the
two songs are within +/-15% BPM. Larger differences require time-stretching
or a tempo bridge in the prompt.
"""
CIRCLE_OF_FIFTHS = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'F']

KEY_TO_OFFSET = {}
for i, note in enumerate(CIRCLE_OF_FIFTHS):
    semitones = (i * 7) % 12
    KEY_TO_OFFSET[f"{note.lower()} major"] = (semitones, False)
    KEY_TO_OFFSET[f"{note.lower()} minor"] = (semitones, True)

SEMITONE_TO_KEY_MAJOR = {}
SEMITONE_TO_KEY_MINOR = {}
for note in CIRCLE_OF_FIFTHS:
    sem_maj, _ = KEY_TO_OFFSET[f"{note.lower()} major"]
    SEMITONE_TO_KEY_MAJOR[sem_maj] = f"{note} major"
    sem_min, _ = KEY_TO_OFFSET[f"{note.lower()} minor"]
    SEMITONE_TO_KEY_MINOR[sem_min] = f"{note} minor"


def parse_key(key_string):
    """Parse 'X major' or 'X minor' into (semitone_offset, is_minor).

    Returns (None, None) if unparseable.
    """
    if not key_string or not isinstance(key_string, str):
        return None, None
    key_string = key_string.strip().lower()
    key_string = key_string.replace('sharp', '#').replace('flat', 'b')
    key_string = key_string.replace('\u266f', '#').replace('\u266d', 'b')
    return KEY_TO_OFFSET.get(key_string, (None, None))


def key_distance(key_a, key_b):
    """Compute distance between two keys on the circle of fifths.

    Returns:
      - distance_fifths: 0-6 (shorter is closer, 6 = tritone substitution)
      - distance_semitones: 0-6
      - is_relative_minor: True if A is the relative minor of B or vice versa
    """
    a_off, a_min = parse_key(key_a)
    b_off, b_min = parse_key(key_b)
    if a_off is None or b_off is None:
        return None

    raw_semitones = abs(a_off - b_off)
    distance_semitones = min(raw_semitones, 12 - raw_semitones)

    a_circle_idx = CIRCLE_OF_FIFTHS.index([n for n in CIRCLE_OF_FIFTHS if parse_key(f"{n.lower()} major")[0] == a_off][0])
    b_circle_idx = CIRCLE_OF_FIFTHS.index([n for n in CIRCLE_OF_FIFTHS if parse_key(f"{n.lower()} major")[0] == b_off][0])
    raw_fifths = abs(a_circle_idx - b_circle_idx)
    distance_fifths = min(raw_fifths, 12 - raw_fifths)

    is_relative_minor = False
    # The relative minor of major key X is at offset (X - 3) mod 12. Equivalently,
    # relative_minor_offset == (major_offset + 9) mod 12, because +9 ≡ -3 (mod 12).
    # So when exactly one of the keys is minor, we check whether the minor key's
    # offset equals (the major key's offset + 9) mod 12.
    if a_min != b_min:
        if a_min and not b_min:
            is_relative_minor = (a_off == (b_off + 9) % 12)
        else:
            is_relative_minor = (b_off == (a_off + 9) % 12)

    return {
        'distance_semitones': distance_semitones,
        'distance_fifths': distance_fifths,
        'is_relative_minor': is_relative_minor,
    }


def key_compatibility_score(key_a, key_b):
    """Score the key compatibility for a mashup from 0.0 (clashing) to 1.0 (perfect).

    Scoring:
      - Same key: 1.0
      - Relative minor/major: 0.95
      - 1 semitone apart (parallel): 0.9
      - 2 semitones apart: 0.8
      - 3 semitones apart (relative via fifth): 0.7
      - 4-5 semitones: 0.5
      - 6 semitones (tritone): 0.3
    """
    d = key_distance(key_a, key_b)
    if d is None:
        return None

    if d['is_relative_minor']:
        return 0.95
    if d['distance_semitones'] == 0:
        return 1.0
    if d['distance_semitones'] == 1:
        return 0.9
    if d['distance_semitones'] == 2:
        return 0.8
    if d['distance_semitones'] == 3:
        return 0.7
    if d['distance_semitones'] == 4:
        return 0.5
    if d['distance_semitones'] == 5:
        return 0.4
    return 0.3


def suggest_transposition(key_target, key_source):
    """Suggest a transposition of key_source to get closer to key_target.

    Returns: (transposed_key, semitones_to_shift)
    """
    target_off, target_min = parse_key(key_target)
    source_off, source_min = parse_key(key_source)
    if target_off is None or source_off is None:
        return None, None

    raw_shift = (target_off - source_off) % 12
    if raw_shift > 6:
        raw_shift -= 12

    if raw_shift == 0:
        return key_target, 0

    new_note_idx = (CIRCLE_OF_FIFTHS.index([n for n in CIRCLE_OF_FIFTHS if parse_key(f"{n.lower()} major")[0] == source_off][0]) + raw_shift) % 12
    new_note = CIRCLE_OF_FIFTHS[new_note_idx]
    new_key = f"{new_note} minor" if source_min else f"{new_note} major"

    return new_key, raw_shift


def bpm_compatibility_score(bpm_a, bpm_b, tolerance_pct=15):
    """Score the BPM compatibility for a mashup from 0.0 (clashing) to 1.0 (perfect).

    Two songs are BPM-compatible if their tempos are within tolerance_pct.
    The score is 1.0 at 0% difference, dropping linearly to 0.5 at the tolerance,
    and 0.0 at >50% difference.
    """
    if bpm_a <= 0 or bpm_b <= 0:
        return None

    diff_pct = abs(bpm_a - bpm_b) / max(bpm_a, bpm_b) * 100

    if diff_pct == 0:
        return 1.0
    if diff_pct <= tolerance_pct:
        return round(1.0 - (diff_pct / tolerance_pct) * 0.3, 3)
    if diff_pct <= 30:
        return round(0.7 - ((diff_pct - tolerance_pct) / (30 - tolerance_pct)) * 0.3, 3)
    if diff_pct <= 50:
        return round(0.4 - ((diff_pct - 30) / 20) * 0.3, 3)
    return 0.1


def mashup_compatibility(song_a, song_b):
    """Compute an overall mashup compatibility score and notes.

    Args:
      song_a: dict with 'bpm', 'estimated_key' fields (from analyze_two_songs.py)
      song_b: dict with 'bpm', 'estimated_key' fields

    Returns dict with:
      - overall_score: 0.0-1.0
      - bpm_score, key_score: individual scores
      - notes: list of human-readable strings
      - suggested_target_bpm: int (BPM the mashup should use)
      - suggested_target_key: str (key the mashup should use)
    """
    bpm_a = song_a.get('bpm', 0)
    bpm_b = song_b.get('bpm', 0)
    key_a = song_a.get('estimated_key', '')
    key_b = song_b.get('estimated_key', '')

    bpm_score = bpm_compatibility_score(bpm_a, bpm_b) if bpm_a and bpm_b else None
    key_score = key_compatibility_score(key_a, key_b) if key_a and key_b else None

    notes = []

    if bpm_score is not None:
        diff = abs(bpm_a - bpm_b)
        if bpm_score >= 0.8:
            notes.append(f"BPMs ({bpm_a} / {bpm_b}) are within 15% — natural blend")
        elif bpm_score >= 0.5:
            notes.append(f"BPMs ({bpm_a} / {bpm_b}) are within 30% — moderate blend, may need tempo bridge")
        else:
            notes.append(f"BPMs ({bpm_a} / {bpm_b}) differ by >30% — requires time-stretching or tempo bridge")
        if bpm_score < 0.5:
            target = min(bpm_a, bpm_b)
        else:
            target = round((bpm_a + bpm_b) / 2, 1)
    else:
        target = bpm_a or bpm_b or 120
        notes.append("BPM not available for one or both songs — using default")

    if key_score is not None:
        d = key_distance(key_a, key_b)
        if key_score >= 0.9:
            notes.append(f"Keys ({key_a} / {key_b}) are harmonically compatible — direct blend works")
        elif key_score >= 0.7:
            notes.append(f"Keys ({key_a} / {key_b}) are within 3 semitones — minor transposition may help")
            transposed, shift = suggest_transposition(key_a, key_b)
            notes.append(f"Suggested transposition: {key_a} → {transposed} (shift {shift} semitones)")
        else:
            notes.append(f"Keys ({key_a} / {key_b}) are clashing — strong transposition recommended")
            transposed, shift = suggest_transposition(key_a, key_b)
            notes.append(f"Suggested transposition: {key_a} → {transposed} (shift {shift} semitones)")
        target_key = key_a
    else:
        target_key = key_a or key_b or 'C major'
        notes.append("Key not available for one or both songs — using default")

    scores = [s for s in [bpm_score, key_score] if s is not None]
    overall = round(sum(scores) / len(scores), 3) if scores else 0.5

    return {
        'overall_score': overall,
        'bpm_score': bpm_score,
        'key_score': key_score,
        'key_distance_semitones': (key_distance(key_a, key_b) or {}).get('distance_semitones') if key_a and key_b else None,
        'suggested_target_bpm': target,
        'suggested_target_key': target_key,
        'notes': notes,
    }


if __name__ == '__main__':
    test_cases = [
        (('A minor', 'A minor'), 1.0),
        (('A minor', 'C major'), 0.95),
        (('A minor', 'G major'), 0.8),
        (('A minor', 'F# minor'), 0.7),
        (('A minor', 'A major'), 0.95),
        (('C major', 'F# major'), 0.3),
    ]
    for (a, b), expected_min in test_cases:
        score = key_compatibility_score(a, b)
        ok = '\u2713' if (score or 0) >= expected_min - 0.05 else '\u2717'
        print(f"{ok} {a} + {b} -> score {score} (expected >= {expected_min})")

    print("\nBPM:")
    for (a, b), expected in [
        ((120, 120), 1.0),
        ((120, 130), 0.85),
        ((120, 160), 0.55),
        ((80, 160), 0.1),
    ]:
        score = bpm_compatibility_score(a, b)
        ok = '\u2713' if abs((score or 0) - expected) < 0.1 else '\u2717'
        print(f"{ok} {a} + {b} -> score {score} (expected ~{expected})")
