#!/usr/bin/env python3
"""
Cut a clip out of a video by start/end timestamps.

The fast path uses ffmpeg stream-copy (no re-encode): this trims at the
nearest keyframe before --start, which is fast (typically faster than
real-time) and lossless. If you need a frame-accurate cut, pass --accurate
to switch to a re-encode pipeline.

Common use: pull a 30s highlight out of a long recording, build a short
preview, or extract the exact range that contains a piece of dialogue.

Usage:
  python3 extract_clip.py <input> <output> --start <ts> [options]

Either --end or --duration is required (not both).

Timestamps:
  Plain seconds:   12.5
  HH:MM:SS:        00:02:13
  HH:MM:SS.mmm:    00:02:13.500
  MM:SS:           02:13
  MM:SS.mmm:       02:13.500

Options:
  --start <ts>          Start timestamp (required).
  --end <ts>            End timestamp.
  --duration <seconds>  Clip duration (use instead of --end).
  --accurate            Re-encode for frame-accurate cut (slower, slight
                        quality loss; default codec libx264 CRF 20, AAC 192k).
  --no-audio            Drop the audio track from the output.
  --crf <int>           Re-encode quality (lower = better, 18-28 typical).
                        Only used with --accurate. Default: 20.
  --preset <name>       x264 preset (ultrafast..veryslow). Only used with
                        --accurate. Default: medium.
  --quiet               Suppress non-error stdout.

Exit codes:
  0 = success
  1 = ffmpeg failure mid-extraction
  2 = bad arguments / missing input / unsafe path / bad timestamp /
      missing input video stream / unsupported output extension
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple

SAFE_PATH_RE = re.compile(r"^[\w./\-+ @=:%,()'\[\]]+$")

ALLOWED_VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi", ".ts"}


def safe_path(p: str) -> Path:
    if not SAFE_PATH_RE.match(p):
        raise ValueError(f"Refusing path with unsafe characters: {p!r}")
    return Path(p).expanduser()


_TS_RE = re.compile(r"^(\d+):(\d{1,2})(?::(\d{1,2}))?(?:\.(\d{1,6}))?$")


def parse_timestamp(s: str) -> float:
    """Accept '12.5', 'MM:SS', 'MM:SS.mmm', 'HH:MM:SS', 'HH:MM:SS.mmm'."""
    s = s.strip()
    if not s:
        raise ValueError("empty timestamp")
    # Plain seconds form
    try:
        v = float(s)
        if v < 0:
            raise ValueError(f"negative timestamp: {s!r}")
        return v
    except ValueError:
        pass
    m = _TS_RE.match(s)
    if not m:
        raise ValueError(f"bad timestamp format: {s!r}")
    a, b, c, ms = m.groups()
    if c is None:
        # MM:SS or MM:SS.mmm
        hh, mm, ss = 0, int(a), int(b)
    else:
        hh, mm, ss = int(a), int(b), int(c)
    if mm >= 60 or ss >= 60:
        raise ValueError(f"minutes/seconds must be < 60: {s!r}")
    total = hh * 3600 + mm * 60 + ss
    if ms:
        total += int(ms.ljust(6, "0")) / 1_000_000
    return float(total)


def probe_has_video(path: Path) -> bool:
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v",
         "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(path)],
        check=False, capture_output=True, text=True,
    )
    return res.returncode == 0 and bool(res.stdout.strip())


def probe_duration(path: Path) -> Optional[float]:
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        check=False, capture_output=True, text=True,
    )
    if res.returncode != 0:
        return None
    try:
        return float(res.stdout.strip())
    except (TypeError, ValueError):
        return None


def format_ts(t: float) -> str:
    return f"{t:.3f}"


def build_cmd(in_path: Path, out_path: Path, start: float, duration: float,
              accurate: bool, no_audio: bool, crf: int, preset: str,
              quiet: bool) -> List[str]:
    """Build the ffmpeg command line.

    Fast path: -ss BEFORE -i for input seek (keyframe-accurate, fast) +
    -c copy. Accurate path: -ss AFTER -i (decodes from start) + re-encode.
    """
    base = ["ffmpeg", "-hide_banner"]
    if quiet:
        base += ["-loglevel", "error"]
    else:
        base += ["-loglevel", "warning"]
    base += ["-y"]

    if not accurate:
        # Fast keyframe cut: seek on input
        cmd = base + ["-ss", format_ts(start), "-i", str(in_path),
                      "-t", format_ts(duration),
                      "-c", "copy",
                      "-avoid_negative_ts", "make_zero"]
    else:
        # Frame-accurate: decode then seek
        cmd = base + ["-i", str(in_path),
                      "-ss", format_ts(start), "-t", format_ts(duration),
                      "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
                      "-pix_fmt", "yuv420p"]
        if not no_audio:
            cmd += ["-c:a", "aac", "-b:a", "192k"]
    if no_audio:
        cmd += ["-an"]
    cmd += [str(out_path)]
    return cmd


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("input", nargs="?")
    p.add_argument("output", nargs="?")
    p.add_argument("--start")
    p.add_argument("--end")
    p.add_argument("--duration")
    p.add_argument("--accurate", action="store_true")
    p.add_argument("--no-audio", dest="no_audio", action="store_true")
    p.add_argument("--crf", type=int, default=20)
    p.add_argument("--preset", default="medium")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.input or not args.output:
        print(__doc__)
        return 0 if args.help else 2
    if args.start is None:
        print("Error: --start <timestamp> is required", file=sys.stderr)
        return 2
    if (args.end is None) == (args.duration is None):
        print("Error: provide exactly one of --end or --duration", file=sys.stderr)
        return 2

    try:
        in_path = safe_path(args.input)
        out_path = safe_path(args.output)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    if not in_path.is_file():
        print(f"Error: input not found: {in_path}", file=sys.stderr)
        return 2
    if out_path.suffix.lower() not in ALLOWED_VIDEO_EXTS:
        print(f"Error: unsupported output extension '{out_path.suffix}'. "
              f"Allowed: {', '.join(sorted(ALLOWED_VIDEO_EXTS))}.", file=sys.stderr)
        return 2

    try:
        start = parse_timestamp(args.start)
        if args.end is not None:
            end = parse_timestamp(args.end)
            if end <= start:
                print(f"Error: --end ({end:.3f}s) must be greater than "
                      f"--start ({start:.3f}s)", file=sys.stderr)
                return 2
            duration = end - start
        else:
            duration = parse_timestamp(args.duration)
            if duration <= 0:
                print(f"Error: --duration must be positive (got {duration})",
                      file=sys.stderr)
                return 2
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    if not probe_has_video(in_path):
        print(f"Error: input has no video stream: {in_path}", file=sys.stderr)
        return 2

    src_duration = probe_duration(in_path)
    if src_duration is not None:
        if start >= src_duration:
            print(f"Error: --start ({start:.3f}s) is at or beyond source "
                  f"duration ({src_duration:.3f}s)", file=sys.stderr)
            return 2
        if start + duration > src_duration + 0.01:
            # Clamp silently to avoid an ffmpeg-side error
            duration = max(0.0, src_duration - start)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = build_cmd(in_path, out_path, start, duration,
                    args.accurate, args.no_audio, args.crf, args.preset,
                    args.quiet)
    if not args.quiet:
        print(f"extract_clip: {in_path} [{start:.3f}s + {duration:.3f}s] "
              f"-> {out_path}  "
              f"({'accurate re-encode' if args.accurate else 'fast stream-copy'})")

    res = subprocess.run(cmd, check=False)
    if res.returncode != 0:
        print(f"Error: ffmpeg failed (exit {res.returncode})", file=sys.stderr)
        return 1

    if not out_path.exists() or out_path.stat().st_size == 0:
        print("Error: ffmpeg produced no output", file=sys.stderr)
        return 1

    if not args.quiet:
        size_mb = out_path.stat().st_size / (1024 * 1024)
        print(f"  wrote {out_path.name}  ({size_mb:.2f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
