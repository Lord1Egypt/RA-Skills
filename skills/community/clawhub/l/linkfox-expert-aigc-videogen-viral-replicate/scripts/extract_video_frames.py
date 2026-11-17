#!/usr/bin/env python3
"""
Extract ordered JPG frames for viral-replicate video-analysis fallback.

The script accepts a local path or http(s) URL, extracts evenly spaced frames,
and prints JSON with frame paths and approximate timestamps. It uses either a
system ffmpeg binary or imageio-ffmpeg's bundled ffmpeg binary.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path


def _is_url(value: str) -> bool:
    parsed = urllib.parse.urlparse(value)
    return parsed.scheme in {"http", "https"}


def _suffix_from_url(url: str) -> str:
    path = urllib.parse.urlparse(url).path
    suffix = Path(path).suffix.lower()
    return suffix if suffix in {".mp4", ".mov", ".m4v", ".webm"} else ".mp4"


def _download(url: str) -> str:
    fd, path = tempfile.mkstemp(prefix="viral_replicate_ref_", suffix=_suffix_from_url(url))
    os.close(fd)
    req = urllib.request.Request(url, headers={"User-Agent": "linkfox-skill/viral-replicate"})
    with urllib.request.urlopen(req, timeout=120) as response, open(path, "wb") as out:
        shutil.copyfileobj(response, out)
    return path


def _find_ffmpeg() -> str | None:
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg
    try:
        import imageio_ffmpeg  # type: ignore

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def _probe_duration(ffmpeg: str, video_path: str) -> float | None:
    ffprobe = shutil.which("ffprobe")
    if ffprobe:
        proc = subprocess.run(
            [
                ffprobe,
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                video_path,
            ],
            text=True,
            capture_output=True,
        )
        if proc.returncode == 0:
            try:
                value = float(proc.stdout.strip())
                if value > 0:
                    return value
            except ValueError:
                pass

    proc = subprocess.run(
        [ffmpeg, "-hide_banner", "-i", video_path],
        text=True,
        capture_output=True,
    )
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", proc.stderr)
    if not match:
        return None
    hours, minutes, seconds = match.groups()
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def _timestamps(duration: float | None, frame_count: int) -> list[float]:
    if frame_count <= 1:
        return [0.0]
    if not duration or duration <= 0:
        return [float(i) for i in range(frame_count)]
    margin = min(0.25, duration * 0.05)
    start = margin
    end = max(start, duration - margin)
    return [start + (end - start) * i / (frame_count - 1) for i in range(frame_count)]


def _extract_frame(ffmpeg: str, video_path: str, timestamp: float, out_path: Path) -> None:
    proc = subprocess.run(
        [
            ffmpeg,
            "-y",
            "-ss",
            f"{timestamp:.3f}",
            "-i",
            video_path,
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(out_path),
        ],
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0 or not out_path.exists() or out_path.stat().st_size == 0:
        raise RuntimeError(proc.stderr.strip() or f"failed to extract {out_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract ordered video frames for textgen fallback")
    parser.add_argument("--video", required=True, help="Reference video local path or http(s) URL")
    parser.add_argument("--out-dir", required=True, help="Output directory for JPG frames")
    parser.add_argument("--frames", type=int, default=9, help="Number of evenly spaced frames")
    args = parser.parse_args()

    if args.frames < 3 or args.frames > 10:
        print("ERROR: --frames must be between 3 and 10", file=sys.stderr)
        return 2

    ffmpeg = _find_ffmpeg()
    if not ffmpeg:
        print(
            "ERROR: ffmpeg not found. Install system ffmpeg or Python package imageio-ffmpeg.",
            file=sys.stderr,
        )
        return 3

    local_video = _download(args.video) if _is_url(args.video) else args.video
    if not os.path.isfile(local_video):
        print(f"ERROR: video file not found: {local_video}", file=sys.stderr)
        return 4

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    duration = _probe_duration(ffmpeg, local_video)
    frames = []
    for index, timestamp in enumerate(_timestamps(duration, args.frames)):
        name = f"frame_{index:03d}_t{int(timestamp * 1000):06d}.jpg"
        path = out_dir / name
        _extract_frame(ffmpeg, local_video, timestamp, path)
        frames.append(
            {
                "index": index,
                "timestamp_seconds": round(timestamp, 3),
                "path": str(path),
                "name": name,
            }
        )

    print(
        json.dumps(
            {
                "source_video": args.video,
                "local_video": local_video,
                "duration_seconds": round(duration, 3) if duration else None,
                "frame_count": len(frames),
                "frames": frames,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
