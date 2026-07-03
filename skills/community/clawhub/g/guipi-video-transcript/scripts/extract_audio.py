#!/usr/bin/env python3
"""Extract audio from video file as 16kHz mono WAV for whisper transcription."""

import subprocess
import sys
from pathlib import Path


def extract_audio(video_path: str, output_path: str) -> str:
    """Extract audio from video, return the WAV file path."""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        str(out)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{result.stderr[-500:]}")
    return str(out)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <video_path> <output_wav_path>")
        sys.exit(1)
    extract_audio(sys.argv[1], sys.argv[2])
