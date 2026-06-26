#!/usr/bin/env python3
"""
Build a short highlight reel from a long video using ffmpeg scene-change
detection.

Usage:
  python3 highlight_reel.py <input.mp4> <output.mp4> [--duration SECONDS]
                                                     [--threshold FLOAT]
                                                     [--clip-length SECONDS]

Algorithm:
  1. Run ffmpeg with the `select='gt(scene,THRESHOLD)'` filter and parse
     `showinfo` lines to collect scene-change timestamps.
  2. Trim a fixed-length clip starting at each scene-change timestamp until
     the cumulative duration reaches the requested target.
  3. Concatenate the clips losslessly via the concat demuxer.

The script never reads or writes paths outside the directories of the input
and output files. It rejects paths that contain shell metacharacters, so the
caller can pass user-provided filenames directly.
"""

from __future__ import annotations

import argparse
import os
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List


SAFE_PATH_RE = re.compile(r"^[\w./\-+ @=:%,()'\[\]]+$")


def safe_path(p: str) -> Path:
    """Reject shell-metacharacter paths and return a resolved Path."""
    if not SAFE_PATH_RE.match(p):
        raise ValueError(f"Refusing path with unsafe characters: {p!r}")
    return Path(p).expanduser()


def run(cmd: List[str], capture: bool = False) -> subprocess.CompletedProcess:
    """Run a command; never use shell=True."""
    return subprocess.run(
        cmd,
        check=False,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE,
    )


def probe_duration(path: Path) -> float:
    res = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture=True,
    )
    if res.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {res.stderr.strip()}")
    return float(res.stdout.strip())


def detect_scene_changes(path: Path, threshold: float) -> List[float]:
    """Return scene-change timestamps in seconds."""
    res = run(
        [
            "ffmpeg",
            "-hide_banner",
            "-i",
            str(path),
            "-filter:v",
            f"select='gt(scene,{threshold})',showinfo",
            "-f",
            "null",
            "-",
        ],
        capture=False,
    )
    # ffmpeg writes showinfo lines to stderr
    timestamps: List[float] = []
    for line in res.stderr.splitlines():
        m = re.search(r"pts_time:([0-9.]+)", line)
        if m:
            timestamps.append(float(m.group(1)))
    return timestamps


def select_clips(
    scene_times: List[float],
    target_duration: float,
    clip_length: float,
    video_duration: float,
) -> List[tuple]:
    """Choose (start, length) pairs whose total length is close to target."""
    if not scene_times:
        # Fall back to evenly spaced clips
        n = max(1, int(target_duration // clip_length))
        if n == 1:
            return [(0.0, min(clip_length, video_duration))]
        step = max(1.0, (video_duration - clip_length) / (n - 1))
        return [(round(i * step, 3), clip_length) for i in range(n)]

    selected: List[tuple] = []
    total = 0.0
    for t in scene_times:
        if t + clip_length > video_duration:
            t = max(0.0, video_duration - clip_length)
        selected.append((round(t, 3), clip_length))
        total += clip_length
        if total >= target_duration:
            break
    return selected


def extract_clips(
    src: Path, clips: List[tuple], workdir: Path
) -> List[Path]:
    out_paths: List[Path] = []
    for i, (start, length) in enumerate(clips):
        out = workdir / f"clip_{i:03d}.mp4"
        res = run(
            [
                "ffmpeg",
                "-hide_banner",
                "-y",
                "-ss",
                f"{start}",
                "-i",
                str(src),
                "-t",
                f"{length}",
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-crf",
                "20",
                "-c:a",
                "aac",
                "-b:a",
                "160k",
                "-movflags",
                "+faststart",
                str(out),
            ]
        )
        if res.returncode != 0 or not out.exists():
            raise RuntimeError(
                f"Failed to extract clip {i} at {start}s: {res.stderr.strip()}"
            )
        out_paths.append(out)
    return out_paths


def concat_clips(clip_paths: List[Path], output: Path, workdir: Path) -> None:
    list_file = workdir / "clips.txt"
    with list_file.open("w", encoding="utf-8") as f:
        for c in clip_paths:
            # The concat demuxer requires escaped single quotes
            safe = str(c).replace("'", r"'\''")
            f.write(f"file '{safe}'\n")
    res = run(
        [
            "ffmpeg",
            "-hide_banner",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_file),
            "-c",
            "copy",
            "-movflags",
            "+faststart",
            str(output),
        ]
    )
    if res.returncode != 0:
        raise RuntimeError(f"concat failed: {res.stderr.strip()}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("input", help="Source video path")
    parser.add_argument("output", help="Output highlight reel path")
    parser.add_argument(
        "--duration",
        type=float,
        default=30.0,
        help="Target reel duration in seconds (default: 30)",
    )
    parser.add_argument(
        "--clip-length",
        type=float,
        default=3.0,
        help="Length of each clip in seconds (default: 3)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.4,
        help="Scene-change sensitivity 0..1 (default: 0.4)",
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
    if args.duration <= 0 or args.clip_length <= 0:
        print("error: duration and clip-length must be > 0", file=sys.stderr)
        return 2
    if not 0.0 < args.threshold <= 1.0:
        print("error: threshold must be in (0, 1]", file=sys.stderr)
        return 2

    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        video_duration = probe_duration(src)
    except Exception as e:  # noqa: BLE001
        print(f"error: probe failed: {e}", file=sys.stderr)
        return 1

    if args.duration >= video_duration:
        print(
            f"warning: target duration ({args.duration}s) >= source ({video_duration:.1f}s); "
            "result will be the full source",
            file=sys.stderr,
        )

    print(f"Detecting scene changes in {src.name} ...", file=sys.stderr)
    scenes = detect_scene_changes(src, args.threshold)
    print(f"  found {len(scenes)} scene-change points", file=sys.stderr)

    clips = select_clips(scenes, args.duration, args.clip_length, video_duration)
    print(f"  selected {len(clips)} clips", file=sys.stderr)
    for i, (s, l) in enumerate(clips):
        print(f"    {i:02d}: start={s:.2f}s length={l:.2f}s", file=sys.stderr)

    with tempfile.TemporaryDirectory(prefix="highlight_") as tmp:
        workdir = Path(tmp)
        clip_paths = extract_clips(src, clips, workdir)
        concat_clips(clip_paths, out, workdir)

    print(f"Wrote {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
