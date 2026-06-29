#!/usr/bin/env python3
"""extract_melody.py — Polyphonic audio → MIDI via Spotify's Basic Pitch.

Wraps basic-pitch (Spotify Research, Apache-2.0) for polyphonic automatic
music transcription. The output MIDI is the cleanest symbolic representation
of "what notes/keys" the song uses.

Usage:
    python3 extract_melody.py <input.wav> --output out.json
    python3 extract_melody.py <input.wav> --midi-out out.mid --output out.json

Output:
    {
      "duration_seconds": 228.6,
      "midi_notes": [{"pitch": 41, "start": 1.06, "end": 1.21, "velocity": 57}, ...],
      "num_notes": 1235,
      "key_estimate_from_midi": "E minor",
      "scale_modes": ["minor"],
      "interval_pattern": "mostly_steps",
      "pitch_range": "E2 to E5",
      "pitch_range_semitones": 36,
      "monophonic_fraction": 0.18,
      "model": "basic-pitch"
    }
"""
import sys
import os
import json
import argparse
import hashlib
from pathlib import Path
from collections import Counter

# Optional: basic_pitch
try:
    from basic_pitch.inference import predict as bp_predict
    HAS_BASIC_PITCH = True
except ImportError:
    HAS_BASIC_PITCH = False

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


def cache_key(audio_path):
    try:
        st = os.stat(audio_path)
        sig = f"{audio_path}|{st.st_mtime}|{st.st_size}|extract_melody"
        return hashlib.sha256(sig.encode()).hexdigest()[:16]
    except OSError:
        return hashlib.sha256(audio_path.encode()).hexdigest()[:16]


def _load_cached(audio_path, cache_dir):
    cache_file = Path(cache_dir) / f"{cache_key(audio_path)}.json"
    if cache_file.exists():
        try:
            with open(cache_file) as f:
                return json.load(f)
        except Exception:
            return None
    return None


def _save_cached(audio_path, cache_dir, result):
    Path(cache_dir).mkdir(parents=True, exist_ok=True)
    cache_file = Path(cache_dir) / f"{cache_key(audio_path)}.json"
    with open(cache_file, 'w') as f:
        json.dump(result, f, indent=2)


# Krumhansl-Schmuckler-style key profile matching on MIDI pitch class
MAJOR_PROFILE = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
MINOR_PROFILE = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
KEY_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Scale mode detection helpers
SCALE_INTERVALS = {
    'major': [0, 2, 4, 5, 7, 9, 11],
    'minor': [0, 2, 3, 5, 7, 8, 10],
    'dorian': [0, 2, 3, 5, 7, 9, 10],
    'phrygian': [0, 1, 3, 5, 7, 8, 10],
    'lydian': [0, 2, 4, 6, 7, 9, 11],
    'mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'locrian': [0, 1, 3, 5, 6, 8, 10],
    'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],
    'melodic_minor': [0, 2, 3, 5, 7, 9, 11],
    'pentatonic_major': [0, 2, 4, 7, 9],
    'pentatonic_minor': [0, 3, 5, 7, 10],
    'blues': [0, 3, 5, 6, 7, 10],
}


def detect_key_from_pitch_classes(pitch_classes):
    """Return (key_name, mode) using Krumhansl-Schmuckler correlation."""
    if not pitch_classes:
        return ('C', 'major')
    counts = Counter(pitch_classes)
    total = sum(counts.values())
    dist = [counts.get(i, 0) / total for i in range(12)]
    best_score = -2
    best_idx = 0
    best_mode = 'major'
    for shift in range(12):
        # Major
        rotated = [dist[(i - shift) % 12] for i in range(12)]
        if len(rotated) == 12:
            mean_r = sum(rotated) / 12
            mean_p = sum(MAJOR_PROFILE) / 12
            num = sum((rotated[i] - mean_r) * (MAJOR_PROFILE[i] - mean_p) for i in range(12))
            den = (
                (sum((rotated[i] - mean_r) ** 2 for i in range(12)) *
                 sum((MAJOR_PROFILE[i] - mean_p) ** 2 for i in range(12))) ** 0.5
            )
            score_major = num / den if den > 0 else 0
            # Minor
            mean_pm = sum(MINOR_PROFILE) / 12
            num = sum((rotated[i] - mean_r) * (MINOR_PROFILE[i] - mean_pm) for i in range(12))
            den = (
                (sum((rotated[i] - mean_r) ** 2 for i in range(12)) *
                 sum((MINOR_PROFILE[i] - mean_pm) ** 2 for i in range(12))) ** 0.5
            )
            score_minor = num / den if den > 0 else 0
            if score_major > best_score:
                best_score = score_major
                best_idx = shift
                best_mode = 'major'
            if score_minor > best_score:
                best_score = score_minor
                best_idx = shift
                best_mode = 'minor'
    return (KEY_NAMES[best_idx], best_mode)


def detect_scale_mode(pitch_classes):
    """Detect modal/extended-scale characteristics from pitch class distribution."""
    if not pitch_classes:
        return []
    counts = Counter(pitch_classes)
    total = sum(counts.values())
    dist = [counts.get(i, 0) / total for i in range(12)]

    # Find the most likely tonic from the top 3 pitch classes
    top_pcs = [pc for pc, _ in counts.most_common(3)]

    # For each candidate tonic, score each mode by how well the distribution matches
    mode_scores = []
    for tonic in top_pcs:
        for mode_name, intervals in SCALE_INTERVALS.items():
            score = sum(dist[(tonic + i) % 12] for i in intervals)
            mode_scores.append((tonic, mode_name, score))

    mode_scores.sort(key=lambda x: -x[2])
    # Return top 2 modes that are actually different (filter trivial matches)
    top_modes = []
    for tonic, mode_name, score in mode_scores:
        if score > 0.5:  # Reasonable match
            top_modes.append(mode_name)
        if len(top_modes) >= 3:
            break
    # De-duplicate while preserving order
    seen = set()
    unique_modes = []
    for m in top_modes:
        if m not in seen:
            unique_modes.append(m)
            seen.add(m)
    return unique_modes if unique_modes else ['major']


def detect_interval_pattern(midi_notes):
    """Classify melody motion as mostly steps / mostly leaps / mixed."""
    if len(midi_notes) < 2:
        return "unknown"
    intervals = []
    sorted_notes = sorted(midi_notes, key=lambda n: n['start'])
    for i in range(len(sorted_notes) - 1):
        diff = abs(sorted_notes[i+1]['pitch'] - sorted_notes[i]['pitch'])
        if 0 < diff < 12:
            intervals.append(diff)
    if not intervals:
        return "unknown"
    steps = sum(1 for x in intervals if x <= 2)
    ratio = steps / len(intervals)
    if ratio > 0.7:
        return "mostly_steps"
    elif ratio < 0.4:
        return "mostly_leaps"
    return "mixed"


def detect_melody_track(midi_notes):
    """Extract the highest sustained voice as the 'melody line'."""
    if not midi_notes:
        return []
    # For now, return top 30% of notes by pitch (the lead voice)
    sorted_by_pitch = sorted(midi_notes, key=lambda n: -n['pitch'])
    n_top = max(1, int(len(sorted_by_pitch) * 0.3))
    return sorted_by_pitch[:n_top]


def extract_melody(audio_path, midi_out_path=None, cache_dir=None):
    """Run Basic Pitch transcription. Returns dict with notes + analysis."""
    if not HAS_BASIC_PITCH:
        return {
            'error': 'basic-pitch not installed',
            'install': 'pip install basic-pitch',
        }

    if cache_dir is None:
        cache_dir = os.path.expanduser("~/.cache/openclaw/melody")

    cached = _load_cached(audio_path, cache_dir)
    if cached is not None:
        cached['_cache'] = 'hit'
        return cached

    print(f"Transcribing: {audio_path}", file=sys.stderr)
    model_output, midi_data, note_events = bp_predict(audio_path)

    # Save MIDI file if requested
    if midi_out_path:
        midi_data.write(midi_out_path)

    # Convert to JSON-serializable list
    inst = midi_data.instruments[0] if midi_data.instruments else None
    if inst is None:
        return {'error': 'basic-pitch produced no notes', 'midi': midi_data}

    midi_notes = []
    pitch_classes = []
    for n in inst.notes:
        midi_notes.append({
            'pitch': int(n.pitch),
            'start': round(float(n.start), 3),
            'end': round(float(n.end), 3),
            'velocity': int(n.velocity),
            'duration': round(float(n.end - n.start), 3),
        })
        pitch_classes.append(int(n.pitch) % 12)

    # Key estimate from MIDI pitch classes
    key_name, key_mode = detect_key_from_pitch_classes(pitch_classes)
    key_estimate = f"{key_name} {key_mode}"

    # Scale modes
    scale_modes = detect_scale_mode(pitch_classes)

    # Interval pattern
    interval_pattern = detect_interval_pattern(midi_notes)

    # Pitch range
    pitches = [n['pitch'] for n in midi_notes]
    if pitches:
        min_pitch, max_pitch = min(pitches), max(pitches)
        # Convert MIDI pitch to note name
        def midi_to_name(midi_p):
            return f"{KEY_NAMES[midi_p % 12]}{midi_p // 12 - 1}"
        pitch_range = f"{midi_to_name(min_pitch)} to {midi_to_name(max_pitch)}"
        pitch_range_semitones = max_pitch - min_pitch
    else:
        pitch_range = "unknown"
        pitch_range_semitones = 0

    # Monophonic fraction: at each time step, how many notes are playing?
    # Simpler: rough estimate by mean notes/second
    if midi_notes and HAS_NUMPY:
        duration = max(n['end'] for n in midi_notes)
        # Average concurrent notes per second
        timeline = []
        for n in midi_notes:
            timeline.append((n['start'], 1))
            timeline.append((n['end'], -1))
        timeline.sort()
        concurrent = 0
        total_concurrent = 0
        steps = 0
        for _, change in timeline:
            concurrent += change
            total_concurrent += concurrent
            steps += 1
        avg_concurrent = total_concurrent / max(steps, 1)
        # Monophonic fraction: 1.0 = single note at a time, 0.0 = heavy polyphony
        # Heuristic: <1.5 concurrent notes → mostly monophonic
        monophonic_fraction = max(0.0, min(1.0, 1.0 - (avg_concurrent - 1.0) / 4.0))
    else:
        monophonic_fraction = 0.5

    result = {
        'duration_seconds': round(midi_notes[-1]['end'] if midi_notes else 0, 2),
        'midi_notes': midi_notes[:500],  # cap to keep JSON small
        'num_notes': len(midi_notes),
        'num_notes_truncated': len(midi_notes) > 500,
        'key_estimate_from_midi': key_estimate,
        'key_confidence_from_midi': 0.7,  # K-S correlation is approximate
        'scale_modes': scale_modes,
        'interval_pattern': interval_pattern,
        'pitch_range': pitch_range,
        'pitch_range_semitones': pitch_range_semitones,
        'monophonic_fraction': round(monophonic_fraction, 3),
        'model': 'basic-pitch (Spotify ICASSP 2022)',
        '_cache': 'miss',
    }

    try:
        _save_cached(audio_path, cache_dir, result)
    except Exception as e:
        print(f"Cache write failed: {e}", file=sys.stderr)

    return result


def main():
    parser = argparse.ArgumentParser(description='Polyphonic audio → MIDI + analysis (Basic Pitch)')
    parser.add_argument('audio', help='Input audio file (WAV/MP3/FLAC)')
    parser.add_argument('--output', help='Output JSON file path')
    parser.add_argument('--midi-out', help='Also write MIDI file to this path')
    args = parser.parse_args()

    if not os.path.exists(args.audio):
        print(f"ERROR: audio file not found: {args.audio}", file=sys.stderr)
        sys.exit(1)

    result = extract_melody(args.audio, midi_out_path=args.midi_out)

    json_out = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(json_out)
        print(f"Written: {args.output}", file=sys.stderr)
    else:
        print(json_out)


if __name__ == '__main__':
    main()
