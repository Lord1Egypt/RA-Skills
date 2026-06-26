#!/usr/bin/env python3
"""
Convert a horizontal video into a 9:16 vertical (1080x1920 by default) for
shorts, reels, and TikTok-style platforms.

Modes:
  letterbox  Original aspect inside a black 9:16 frame (no content lost).
  crop       Center-crop to 9:16 (fastest, content lost on left/right edges).
  blur-fill  Original centered with a blurred copy of itself filling the
             top/bottom bars (no content lost; popular look for repurposing
             horizontal clips as shorts).

Usage:
  python3 make_vertical.py <input> <output> [--mode letterbox|crop|blur-fill]
                                            [--width 1080] [--height 1920]
                                            [--blur-radius 30]
                                            [--crf 20]

The script never invokes a shell. Inputs are validated for safe characters
to avoid filter-graph injection.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

SAFE_PATH_RE = re.compile(r"^[\w./\-+ @=:%,()'\[\]]+$")
MODES = ("letterbox", "crop", "blur-fill")


def safe_path(p: str) -> Path:
    if not SAFE_PATH_RE.match(p):
        raise ValueError(f"Refusing path with unsafe characters: {p!r}")
    return Path(p).expanduser()


def run(cmd):
    return subprocess.run(cmd, check=False, text=True, stderr=subprocess.PIPE)


def build_filter(mode: str, width: int, height: int, blur_radius: int) -> str:
    if mode == "letterbox":
        # Scale to fit inside WxH, then pad with black bars.
        return (
            f"scale=w={width}:h={height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,"
            f"setsar=1"
        )
    if mode == "crop":
        # Cover WxH (may crop horizontally), then center-crop to exact size.
        return (
            f"scale=w={width}:h={height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height},"
            f"setsar=1"
        )
    if mode == "blur-fill":
        # Two branches:
        #   - bg: scale to cover WxH, blur, crop to WxH
        #   - fg: scale to fit inside WxH, preserve aspect
        # Then overlay fg on bg, centered.
        return (
            f"split=2[bg_in][fg_in];"
            f"[bg_in]scale=w={width}:h={height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height},"
            f"boxblur={blur_radius}:1[bg];"
            f"[fg_in]scale=w={width}:h={height}:force_original_aspect_ratio=decrease[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1"
        )
    raise ValueError(f"Unknown mode: {mode}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("input", help="Source video path")
    parser.add_argument("output", help="Output video path")
    parser.add_argument(
        "--mode",
        choices=MODES,
        default="blur-fill",
        help="Vertical conversion strategy (default: blur-fill).",
    )
    parser.add_argument("--width", type=int, default=1080, help="Output width (default 1080).")
    parser.add_argument("--height", type=int, default=1920, help="Output height (default 1920).")
    parser.add_argument(
        "--blur-radius",
        type=int,
        default=30,
        help="Boxblur radius for blur-fill mode (default 30).",
    )
    parser.add_argument(
        "--crf",
        type=int,
        default=20,
        help="x264 CRF value (default 20; lower = higher quality).",
    )
    parser.add_argument(
        "--preset",
        default="medium",
        help="x264 preset (default: medium). Use veryfast for quick previews.",
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

    if args.width <= 0 or args.height <= 0:
        print("error: --width and --height must be positive", file=sys.stderr)
        return 2
    if args.blur_radius < 0:
        print("error: --blur-radius must be non-negative", file=sys.stderr)
        return 2
    if args.height <= args.width:
        print(
            f"warning: output {args.width}x{args.height} is not a vertical aspect "
            "(height should exceed width). Continuing anyway.",
            file=sys.stderr,
        )

    out.parent.mkdir(parents=True, exist_ok=True)

    vfilter = build_filter(args.mode, args.width, args.height, args.blur_radius)
    cmd = [
        "ffmpeg", "-hide_banner", "-y",
        "-i", str(src),
        "-vf", vfilter,
        "-c:v", "libx264",
        "-preset", args.preset,
        "-crf", str(args.crf),
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-movflags", "+faststart",
        str(out),
    ]
    print(f"Mode: {args.mode}, output: {args.width}x{args.height}", file=sys.stderr)
    res = run(cmd)
    if res.returncode != 0:
        print(f"error: ffmpeg failed: {res.stderr.strip()}", file=sys.stderr)
        return 1

    print(f"Wrote {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
