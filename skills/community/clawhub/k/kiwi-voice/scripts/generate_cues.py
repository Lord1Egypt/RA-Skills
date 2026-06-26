#!/usr/bin/env python3
"""Generate audio cue WAV files for Kiwi Voice.

Creates short notification sounds used by the voice assistant:
  - wake_detected.wav  — chime when wake word is recognized
  - processing.wav     — tone when query is sent to OpenClaw

Uses pure numpy (no external audio libraries needed for generation).

Usage:
    python scripts/generate_cues.py
    python scripts/generate_cues.py --output-dir sounds
"""

import argparse
import os
import sys

import numpy as np

try:
    import soundfile as sf
except ImportError:
    print("ERROR: soundfile is required. Install with: pip install soundfile")
    sys.exit(1)


SAMPLE_RATE = 24000


def _fade(audio: np.ndarray, fade_in_ms: int = 10, fade_out_ms: int = 50) -> np.ndarray:
    """Apply fade-in and fade-out to avoid clicks."""
    fade_in_samples = int(SAMPLE_RATE * fade_in_ms / 1000)
    fade_out_samples = int(SAMPLE_RATE * fade_out_ms / 1000)

    if fade_in_samples > 0 and fade_in_samples < len(audio):
        audio[:fade_in_samples] *= np.linspace(0, 1, fade_in_samples)
    if fade_out_samples > 0 and fade_out_samples < len(audio):
        audio[-fade_out_samples:] *= np.linspace(1, 0, fade_out_samples)

    return audio


def generate_wake_chime() -> np.ndarray:
    """Two-tone ascending chime (C5 + E5), 250ms total."""
    duration = 0.25
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)

    # C5 (523 Hz) first half, E5 (659 Hz) second half
    mid = len(t) // 2
    tone1 = 0.4 * np.sin(2 * np.pi * 523 * t[:mid])
    tone2 = 0.4 * np.sin(2 * np.pi * 659 * t[mid:])

    audio = np.concatenate([tone1, tone2]).astype(np.float32)
    return _fade(audio)


def generate_processing_tone() -> np.ndarray:
    """Single soft tone (A4, 440 Hz), 150ms."""
    duration = 0.15
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    audio = (0.3 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)
    return _fade(audio)


def main():
    parser = argparse.ArgumentParser(description="Generate audio cues for Kiwi Voice")
    parser.add_argument(
        "--output-dir",
        type=str,
        default="sounds",
        help="Output directory (default: sounds)",
    )
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    cues = {
        "wake_detected.wav": generate_wake_chime,
        "processing.wav": generate_processing_tone,
    }

    for filename, generator in cues.items():
        path = os.path.join(args.output_dir, filename)
        audio = generator()
        sf.write(path, audio, SAMPLE_RATE)
        duration_ms = len(audio) / SAMPLE_RATE * 1000
        print(f"  Created {path} ({duration_ms:.0f}ms, {len(audio)} samples)")

    print(f"\nDone! {len(cues)} audio cues generated in {args.output_dir}/")


if __name__ == "__main__":
    main()
