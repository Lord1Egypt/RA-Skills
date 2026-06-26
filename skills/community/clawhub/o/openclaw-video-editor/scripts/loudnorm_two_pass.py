#!/usr/bin/env python3
"""
Two-pass loudnorm runner for ffmpeg.

Runs the EBU R128 loudnorm filter in measurement mode first, parses the JSON
block ffmpeg writes to stderr, then runs the second pass with the measured
values applied. Audio is normalized; video is copied without re-encoding.

Usage:
  python3 loudnorm_two_pass.py <input> <output> [--target-lufs -23]
                                                [--lra 7] [--tp -2]
                                                [--audio-codec aac] [--audio-bitrate 192k]

Defaults target broadcast (-23 LUFS, LRA 7, true-peak -2). For streaming
platforms pass --target-lufs -14.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import List

SAFE_PATH_RE = re.compile(r"^[\w./\-+ @=:%,()'\[\]]+$")
JSON_BLOCK_RE = re.compile(r"\{[^{}]*\"input_i\"[^{}]*\}", re.DOTALL)


def safe_path(p: str) -> Path:
    if not SAFE_PATH_RE.match(p):
        raise ValueError(f"Refusing path with unsafe characters: {p!r}")
    return Path(p).expanduser()


def run(cmd: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=False, text=True, stderr=subprocess.PIPE)


def has_audio_stream(path: Path) -> bool:
    """Return True if the media file contains at least one audio stream.

    Uses ffprobe to enumerate streams. Returns False on any ffprobe failure
    so the caller can surface a clean error message rather than letting
    pass 1 of loudnorm fail with an opaque "measurement JSON not found".
    """
    res = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-select_streams", "a",
            "-show_entries", "stream=codec_type",
            "-of", "csv=p=0",
            str(path),
        ],
        check=False, capture_output=True, text=True,
    )
    if res.returncode != 0:
        return False
    return bool(res.stdout.strip())


def parse_measurement(stderr_text: str) -> dict:
    """Extract the JSON measurement block ffmpeg's loudnorm filter prints."""
    matches = JSON_BLOCK_RE.findall(stderr_text)
    if not matches:
        raise RuntimeError(
            "Could not find loudnorm measurement JSON in ffmpeg stderr. "
            "The input may not contain an audio stream, or ffmpeg failed."
        )
    # Use the last block; loudnorm prints exactly one but we are defensive.
    raw = matches[-1]
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Failed to parse loudnorm JSON: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("input", help="Source media path")
    parser.add_argument("output", help="Output path")
    parser.add_argument(
        "--target-lufs",
        type=float,
        default=-23.0,
        help="Integrated loudness target in LUFS. -23 for broadcast (default), "
             "-14 for streaming (Spotify, YouTube, Apple Music).",
    )
    parser.add_argument(
        "--lra",
        type=float,
        default=7.0,
        help="Loudness range target (default 7).",
    )
    parser.add_argument(
        "--tp",
        type=float,
        default=-2.0,
        help="True-peak ceiling in dBTP (default -2).",
    )
    parser.add_argument(
        "--audio-codec",
        default="aac",
        help="Output audio codec (default: aac).",
    )
    parser.add_argument(
        "--audio-bitrate",
        default="192k",
        help="Output audio bitrate (default: 192k).",
    )
    parser.add_argument(
        "--show-measurement",
        action="store_true",
        help="Print the loudnorm measurement JSON before running pass 2.",
    )
    args = parser.parse_args()

    try:
        src = safe_path(args.input).resolve()
        out = safe_path(args.output).resolve()
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if not src.exists():
        print(f"error: input not found: {src}", file=sys.stderr)
        return 2

    # Preflight: refuse cleanly when the input has no audio stream, instead
    # of failing inside pass 1 of loudnorm with an opaque "could not find
    # measurement JSON" error.
    if not has_audio_stream(src):
        print(
            f"error: input has no audio stream: {src}. "
            f"loudnorm requires audio; use extract_audio.py or check the source file.",
            file=sys.stderr,
        )
        return 2

    out.parent.mkdir(parents=True, exist_ok=True)

    target_i = f"{args.target_lufs}"
    target_lra = f"{args.lra}"
    target_tp = f"{args.tp}"

    # ---- Pass 1: measure ----
    print(f"Pass 1: measuring loudness on {src.name} ...", file=sys.stderr)
    pass1_cmd = [
        "ffmpeg", "-hide_banner", "-nostats", "-y",
        "-i", str(src),
        "-af",
        f"loudnorm=I={target_i}:LRA={target_lra}:tp={target_tp}:print_format=json",
        "-f", "null", "-",
    ]
    res1 = run(pass1_cmd)
    if res1.returncode != 0:
        print(f"error: pass 1 failed: {res1.stderr.strip()}", file=sys.stderr)
        return 1

    try:
        measurement = parse_measurement(res1.stderr)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.show_measurement:
        print("Measurement:", file=sys.stderr)
        print(json.dumps(measurement, indent=2), file=sys.stderr)

    # Required keys for pass 2
    required = ("input_i", "input_tp", "input_lra", "input_thresh", "target_offset")
    for key in required:
        if key not in measurement:
            print(f"error: measurement missing key '{key}'", file=sys.stderr)
            return 1

    # ---- Pass 2: apply ----
    print(f"Pass 2: applying normalization to {out.name} ...", file=sys.stderr)
    af = (
        f"loudnorm=I={target_i}:LRA={target_lra}:tp={target_tp}"
        f":measured_I={measurement['input_i']}"
        f":measured_TP={measurement['input_tp']}"
        f":measured_LRA={measurement['input_lra']}"
        f":measured_thresh={measurement['input_thresh']}"
        f":offset={measurement['target_offset']}"
        f":linear=true:print_format=summary"
    )
    pass2_cmd = [
        "ffmpeg", "-hide_banner", "-y",
        "-i", str(src),
        "-af", af,
        "-c:v", "copy",
        "-c:a", args.audio_codec,
        "-b:a", args.audio_bitrate,
        "-movflags", "+faststart",
        str(out),
    ]
    res2 = run(pass2_cmd)
    if res2.returncode != 0:
        print(f"error: pass 2 failed: {res2.stderr.strip()}", file=sys.stderr)
        return 1

    print(f"Wrote {out}", file=sys.stderr)
    print(
        f"Target: I={target_i} LUFS, LRA={target_lra}, TP={target_tp} dBTP",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
