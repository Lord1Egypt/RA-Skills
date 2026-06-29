#!/usr/bin/env python3
"""track_beats.py — ISMIR 2024 SOTA beat + downbeat tracking.

Wraps beat_this (CPJKU, MIT-licensed) to extract precise beat and downbeat
positions from audio. The output is far more accurate than librosa.beat.beat_track
for syncopated or fast music, especially for downbeat detection.

Usage:
    python3 track_beats.py <input.wav> [--output out.json]

Output:
    {
      "duration_seconds": 228.6,
      "beat_positions": [0.06, 0.48, 0.86, ...],
      "downbeat_positions": [0.06, 1.62, 3.28, ...],
      "num_beats": 560,
      "num_downbeats": 153,
      "bpm_estimated": 152.0,
      "bpm_confidence": 0.92,
      "time_signature_estimate": 4,
      "downbeat_density_per_minute": 40.2
    }
"""
import sys
import os
import json
import argparse
import hashlib
import warnings
from pathlib import Path

# Optional: beat_this is the dependency
try:
    from beat_this.inference import File2Beats
    HAS_BEAT_THIS = True
except ImportError:
    HAS_BEAT_THIS = False

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


def cache_key(audio_path):
    try:
        st = os.stat(audio_path)
        sig = f"{audio_path}|{st.st_mtime}|{st.st_size}|track_beats"
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


def track_beats(audio_path, device='cpu', use_dbn=False, cache_dir=None):
    """Track beats and downbeats with beat_this.

    Args:
        audio_path: input audio file
        device: 'cpu' or 'cuda'
        use_dbn: whether to use the DBN (Dynamic Bayesian Network) post-processor
                (slower, more accurate). Default False (transformer-only).
        cache_dir: optional directory for result cache. Default: ~/.cache/openclaw/beats/

    Returns:
        dict with beat_positions, downbeat_positions, BPM, etc.
    """
    if not HAS_BEAT_THIS:
        return {
            'error': 'beat_this not installed',
            'install': 'pip install beat-this',
        }

    if cache_dir is None:
        cache_dir = os.path.expanduser("~/.cache/openclaw/beats")

    # Try cache first
    cached = _load_cached(audio_path, cache_dir)
    if cached is not None:
        cached['_cache'] = 'hit'
        return cached

    print(f"Tracking beats: {audio_path} (device={device})", file=sys.stderr)
    model = File2Beats(device=device, dbn=use_dbn)
    beat_times, downbeat_times = model(audio_path)

    # Ensure plain python lists (numpy arrays → list for JSON)
    if HAS_NUMPY and isinstance(beat_times, np.ndarray):
        beat_positions = beat_times.tolist()
        downbeat_positions = downbeat_times.tolist()
    else:
        beat_positions = list(beat_times)
        downbeat_positions = list(downbeat_times)

    # Compute BPM estimate from beat intervals
    if len(beat_positions) > 1:
        intervals = [beat_positions[i+1] - beat_positions[i]
                     for i in range(len(beat_positions) - 1)]
        if intervals:
            median_interval = sorted(intervals)[len(intervals) // 2]
            bpm = 60.0 / median_interval
            # Confidence: 1 - normalized std of intervals
            mean_interval = sum(intervals) / len(intervals)
            variance = sum((x - mean_interval) ** 2 for x in intervals) / len(intervals)
            std_interval = variance ** 0.5
            bpm_confidence = max(0.0, min(1.0, 1.0 - std_interval / (mean_interval + 1e-9)))
        else:
            bpm = 0
            bpm_confidence = 0
    else:
        bpm = 0
        bpm_confidence = 0

    # Time signature estimate: from median downbeats-per-beat ratio
    if len(beat_positions) > 5 and len(downbeat_positions) > 1:
        # Average downbeats per minute
        if beat_positions[-1] > beat_positions[0]:
            duration_min = (beat_positions[-1] - beat_positions[0]) / 60.0
            downbeat_density_per_minute = len(downbeat_positions) / max(duration_min, 1e-9)
            # Estimate time signature from the downbeat:beat ratio
            # 4/4 = 4 downbeats per ~4 beats (one downbeat per bar)
            # 3/4 = 3 downbeats per ~3 beats
            # We can't be exact without ground truth, but typical is 4
            # Heuristic: if downbeat density is ~30-50/min and BPM is 60-180, it's likely 4/4
            if 30 < downbeat_density_per_minute < 70:
                time_sig_estimate = 4
            elif 40 < downbeat_density_per_minute < 90:
                time_sig_estimate = 3
            elif 50 < downbeat_density_per_minute < 120:
                time_sig_estimate = 6
            else:
                time_sig_estimate = 4  # default
        else:
            time_sig_estimate = 4
            downbeat_density_per_minute = 0
    else:
        time_sig_estimate = 4
        downbeat_density_per_minute = 0

    result = {
        'duration_seconds': round(beat_positions[-1] if beat_positions else 0, 2),
        'beat_positions': [round(t, 3) for t in beat_positions],
        'downbeat_positions': [round(t, 3) for t in downbeat_positions],
        'num_beats': len(beat_positions),
        'num_downbeats': len(downbeat_positions),
        'bpm_estimated': round(bpm, 2),
        'bpm_confidence': round(bpm_confidence, 3),
        'time_signature_estimate': time_sig_estimate,
        'downbeat_density_per_minute': round(downbeat_density_per_minute, 2),
        'model': 'beat_this' + ('_dbn' if use_dbn else ''),
        '_cache': 'miss',
    }

    # Cache it
    try:
        _save_cached(audio_path, cache_dir, result)
    except Exception as e:
        print(f"Cache write failed: {e}", file=sys.stderr)

    return result


def main():
    parser = argparse.ArgumentParser(description='Track beats + downbeats with beat_this (ISMIR 2024 SOTA)')
    parser.add_argument('audio', help='Input audio file (WAV/MP3/FLAC)')
    parser.add_argument('--output', help='Output JSON file path')
    parser.add_argument('--device', default='cpu', choices=['cpu', 'cuda'], help='Inference device')
    parser.add_argument('--dbn', action='store_true', help='Use DBN postprocessor (slower, more accurate)')
    args = parser.parse_args()

    if not os.path.exists(args.audio):
        print(f"ERROR: audio file not found: {args.audio}", file=sys.stderr)
        sys.exit(1)

    result = track_beats(args.audio, device=args.device, use_dbn=args.dbn)

    json_out = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(json_out)
        print(f"Written: {args.output}", file=sys.stderr)
    else:
        print(json_out)


if __name__ == '__main__':
    main()
