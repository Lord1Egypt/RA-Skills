#!/usr/bin/env python3
"""
Apply a 3D LUT (.cube file) to a video using ffmpeg's lut3d filter.

Usage:
  python3 apply_lut.py <input.mp4> <lut.cube> <output.mp4> [--strength 0..1]
                                                            [--preset NAME]

If --preset is given instead of a .cube file, a deterministic ffmpeg filter
preset is applied. Available presets:
  - warm
  - cool
  - bw           (black and white)
  - high-contrast
  - faded

The script never invokes a shell. Inputs are validated for safe characters
to avoid filter-graph injection.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

SAFE_PATH_RE = re.compile(r"^[\w./\-+ @=:%,()'\[\]]+$")

PRESETS = {
    "warm": "eq=contrast=1.05:saturation=1.15,colorbalance=rs=0.10:gs=0.0:bs=-0.05",
    "cool": "eq=contrast=1.05:saturation=1.05,colorbalance=rs=-0.05:gs=0.0:bs=0.10",
    "bw": "hue=s=0,eq=contrast=1.15:brightness=-0.02",
    "high-contrast": "eq=contrast=1.30:brightness=0.0:saturation=1.05",
    "faded": "eq=contrast=0.92:saturation=0.85,curves=preset=lighter",
}


def safe_path(p: str) -> Path:
    if not SAFE_PATH_RE.match(p):
        raise ValueError(f"Refusing path with unsafe characters: {p!r}")
    return Path(p).expanduser()


def run(cmd):
    return subprocess.run(cmd, check=False, text=True, stderr=subprocess.PIPE)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("input", help="Source video path")
    parser.add_argument(
        "lut_or_dash",
        help="Path to a .cube LUT file, or '-' if using --preset",
    )
    parser.add_argument("output", help="Output video path")
    parser.add_argument(
        "--strength",
        type=float,
        default=1.0,
        help="LUT mix amount, 0..1 (default 1.0). Only effective with .cube LUTs.",
    )
    parser.add_argument(
        "--preset",
        choices=sorted(PRESETS.keys()),
        help="Use a named preset instead of a .cube file",
    )
    parser.add_argument(
        "--crf",
        type=int,
        default=20,
        help="x264 CRF value (default 20)",
    )
    args = parser.parse_args()

    try:
        src = safe_path(args.input).resolve()
        out = safe_path(args.output).resolve()
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if not src.exists():
        print(f"error: input not found: {src}", file=sys.stderr)
        return 2
    if not 0.0 <= args.strength <= 1.0:
        print("error: --strength must be in [0, 1]", file=sys.stderr)
        return 2

    if args.preset:
        vfilter = PRESETS[args.preset]
    else:
        if args.lut_or_dash == "-":
            print("error: pass a .cube path or use --preset", file=sys.stderr)
            return 2
        try:
            lut = safe_path(args.lut_or_dash).resolve()
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        if not lut.exists() or lut.suffix.lower() != ".cube":
            print(f"error: not a .cube file: {lut}", file=sys.stderr)
            return 2
        if args.strength >= 0.999:
            vfilter = f"lut3d='{lut}'"
        else:
            # Blend: split video, apply LUT to one branch, mix
            vfilter = (
                f"split[a][b];[a]lut3d='{lut}'[a2];"
                f"[a2][b]blend=all_mode=normal:all_opacity={args.strength}"
            )

    out.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-y",
        "-i",
        str(src),
        "-vf",
        vfilter,
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        str(args.crf),
        "-c:a",
        "copy",
        "-movflags",
        "+faststart",
        str(out),
    ]
    print("running:", " ".join(cmd), file=sys.stderr)
    res = run(cmd)
    if res.returncode != 0:
        print(f"error: ffmpeg failed: {res.stderr.strip()}", file=sys.stderr)
        return 1
    print(f"Wrote {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
