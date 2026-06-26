#!/usr/bin/env python3
"""
Extract candidate frames from a video and rank them by a composite score
combining sharpness, brightness, contrast, and ffmpeg scene-change scores.

Outputs the top-N frames as PNG files plus a JSON report with per-frame
scores and timestamps.

Usage:
  python3 pick_frames.py <input.mp4> <output_dir> [--top N] [--interval S]
                                                  [--min-brightness 0-255]
                                                  [--max-brightness 0-255]
                                                  [--min-sharpness FLOAT]

Exit codes:
  0 = success, at least one frame written
  1 = no frames passed the filters (video may be too short, too dark, or static)
  2 = error (bad arguments, missing input, ffmpeg/ffprobe failure)
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Dict

try:
    from PIL import Image, ImageFilter, ImageStat
except ImportError:
    print("error: Pillow not installed. Run: pip install Pillow", file=sys.stderr)
    sys.exit(2)

SAFE_PATH_RE = re.compile(r"^[\w./\-+ @=:%,()'\[\]]+$")


def safe_path(p: str) -> Path:
    if not SAFE_PATH_RE.match(p):
        raise ValueError(f"Refusing path with unsafe characters: {p!r}")
    return Path(p).expanduser()


def probe_duration(path: Path) -> float:
    """Return media duration in seconds. Raises RuntimeError on ffprobe failure."""
    res = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=False, capture_output=True, text=True,
    )
    if res.returncode != 0:
        # Surface only the last meaningful line so the user gets a clean message.
        msg = (res.stderr or "").strip().splitlines()
        last = msg[-1] if msg else "ffprobe failed"
        raise RuntimeError(f"ffprobe failed: {last}")
    try:
        return float(res.stdout.strip())
    except ValueError:
        raise RuntimeError("ffprobe returned no duration")


def detect_scene_changes(path: Path, threshold: float = 0.3) -> List[float]:
    res = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-i", str(path),
            "-filter:v", f"select='gt(scene,{threshold})',showinfo",
            "-f", "null", "-",
        ],
        check=False, capture_output=True, text=True,
    )
    timestamps: List[float] = []
    for line in res.stderr.splitlines():
        m = re.search(r"pts_time:([0-9.]+)", line)
        if m:
            timestamps.append(float(m.group(1)))
    return timestamps


def extract_frame_at(src: Path, timestamp: float, out_path: Path) -> bool:
    res = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-y",
            "-ss", f"{timestamp}",
            "-i", str(src),
            "-frames:v", "1",
            "-q:v", "2",
            str(out_path),
        ],
        check=False, capture_output=True, text=True,
    )
    return res.returncode == 0 and out_path.exists()


def score_frame(frame_path: Path) -> Dict:
    """Compute brightness, contrast, and sharpness scores for a frame."""
    with Image.open(frame_path) as img:
        gray = img.convert("L")
        stat = ImageStat.Stat(gray)
        brightness = stat.mean[0]
        contrast = stat.stddev[0]
        # Sharpness via Laplacian-like edge filter variance
        edges = gray.filter(ImageFilter.FIND_EDGES)
        edge_stat = ImageStat.Stat(edges)
        sharpness = edge_stat.stddev[0]
        width, height = img.size
    return {
        "brightness": round(brightness, 2),
        "contrast": round(contrast, 2),
        "sharpness": round(sharpness, 2),
        "width": width,
        "height": height,
    }


def composite_score(metrics: Dict, scene_bonus: float = 0.0) -> float:
    """Combine raw metrics into a single rank score."""
    brightness = metrics["brightness"]
    contrast = metrics["contrast"]
    sharpness = metrics["sharpness"]

    # Penalise extreme brightness (too dark or blown out)
    ideal = 128.0
    brightness_penalty = abs(brightness - ideal) / ideal  # 0 = ideal, 1 = worst
    brightness_score = max(0.0, 1.0 - brightness_penalty)

    # Higher contrast/sharpness is better (cap to avoid runaway dominance)
    contrast_score = min(1.0, contrast / 80.0)
    sharpness_score = min(1.0, sharpness / 60.0)

    # Weighted composite
    return round(
        0.35 * sharpness_score
        + 0.30 * contrast_score
        + 0.25 * brightness_score
        + 0.10 * scene_bonus,
        4,
    )


def build_sample_times(duration: float, interval: float, scene_times: set) -> List[float]:
    """Build the list of timestamps to sample.

    For very short videos (< 2 * interval), fall back to a fixed minimum of
    3 evenly-spaced samples so we don't return zero candidates from a 1-2s clip.
    """
    sample_times: List[float] = []

    if duration <= 0:
        return sample_times

    if duration < interval * 2:
        # Short clip: take 3 evenly-spaced samples (or fewer for very short).
        n = max(1, min(3, int(duration * 4)))  # up to 3 samples per quarter-second resolution
        step = duration / (n + 1)
        sample_times = [round((i + 1) * step, 2) for i in range(n)]
    else:
        t = interval / 2.0
        while t < duration:
            sample_times.append(round(t, 2))
            t += interval

    # Add scene change times too (deduplicated by 0.5s buckets)
    bucket = {round(s, 1) for s in sample_times}
    for st in scene_times:
        st_r = round(st, 1)
        if st_r not in bucket and 0 < st < duration:
            sample_times.append(st)
            bucket.add(st_r)
    sample_times.sort()
    return sample_times


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("input", help="Source video path")
    parser.add_argument("output_dir", help="Output directory for top frames")
    parser.add_argument("--top", type=int, default=10, help="Number of top frames to keep (default 10)")
    parser.add_argument("--interval", type=float, default=2.0, help="Sampling interval in seconds (default 2.0)")
    parser.add_argument("--min-brightness", type=float, default=20.0, help="Reject frames darker than this (0-255)")
    parser.add_argument("--max-brightness", type=float, default=235.0, help="Reject frames brighter than this (0-255)")
    parser.add_argument("--min-sharpness", type=float, default=5.0, help="Reject frames with sharpness below this")
    parser.add_argument(
        "--scene-threshold", type=float, default=0.3,
        help="ffmpeg scene-change threshold for the bonus signal (default 0.3)",
    )
    parser.add_argument(
        "--relax-on-empty", action="store_true",
        help="If no frame passes the filters, retry once with min-sharpness=1 "
             "and min-brightness=5 so very short or static clips still produce "
             "at least one candidate.",
    )
    args = parser.parse_args()

    try:
        src = safe_path(args.input).resolve()
        out_dir = safe_path(args.output_dir).resolve()
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if not src.exists():
        print(f"error: input not found: {src}", file=sys.stderr)
        return 2
    if args.top <= 0 or args.interval <= 0:
        print("error: --top and --interval must be positive", file=sys.stderr)
        return 2

    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Probing {src.name} ...", file=sys.stderr)
    try:
        duration = probe_duration(src)
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    print(f"  duration: {duration:.2f}s", file=sys.stderr)

    if duration <= 0.05:
        print("error: video duration is zero or unreadable", file=sys.stderr)
        return 2

    scene_times = set()
    print("Detecting scene changes ...", file=sys.stderr)
    for t in detect_scene_changes(src, args.scene_threshold):
        scene_times.add(round(t, 1))
    print(f"  found {len(scene_times)} scene-change points", file=sys.stderr)

    sample_times = build_sample_times(duration, args.interval, scene_times)
    print(f"  sampling {len(sample_times)} candidate frames", file=sys.stderr)

    if not sample_times:
        print("error: could not build any sample timestamps", file=sys.stderr)
        return 2

    def collect(min_brightness: float, max_brightness: float, min_sharpness: float) -> List[Dict]:
        out = []
        with tempfile.TemporaryDirectory(prefix="thumbforge_") as tmpdir:
            tmp = Path(tmpdir)
            for i, ts in enumerate(sample_times):
                tmp_frame = tmp / f"cand_{i:04d}.png"
                if not extract_frame_at(src, ts, tmp_frame):
                    continue
                try:
                    metrics = score_frame(tmp_frame)
                except Exception as e:
                    print(f"  skip {ts:.2f}s: scoring failed ({e})", file=sys.stderr)
                    continue

                if metrics["brightness"] < min_brightness:
                    continue
                if metrics["brightness"] > max_brightness:
                    continue
                if metrics["sharpness"] < min_sharpness:
                    continue

                scene_bonus = 1.0 if round(ts, 1) in scene_times else 0.0
                score = composite_score(metrics, scene_bonus)
                out.append({
                    "timestamp": ts,
                    "metrics": metrics,
                    "scene_change": scene_bonus > 0,
                    "score": score,
                })
        return out

    candidates = collect(args.min_brightness, args.max_brightness, args.min_sharpness)
    if not candidates and args.relax_on_empty:
        print("  no frames passed; retrying with relaxed filters", file=sys.stderr)
        candidates = collect(5.0, 250.0, 1.0)

    candidates.sort(key=lambda c: c["score"], reverse=True)
    top = candidates[: args.top]

    report = []
    for rank, cand in enumerate(top, start=1):
        out_name = f"frame_{rank:03d}.png"
        out_path = out_dir / out_name
        # Re-extract at full quality to the final path
        extract_frame_at(src, cand["timestamp"], out_path)
        entry = {
            "rank": rank,
            "file": out_name,
            "timestamp": cand["timestamp"],
            "score": cand["score"],
            "metrics": cand["metrics"],
            "scene_change": cand["scene_change"],
        }
        report.append(entry)
        print(
            f"  #{rank:2d} {out_name} t={cand['timestamp']:6.2f}s "
            f"score={cand['score']:.3f} "
            f"sharp={cand['metrics']['sharpness']:.1f} "
            f"bright={cand['metrics']['brightness']:.1f}",
            file=sys.stderr,
        )

    (out_dir / "report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )

    if not report:
        print(
            "warning: no frames passed the filters. "
            "Try --relax-on-empty, lower --min-sharpness, or shorter --interval.",
            file=sys.stderr,
        )
        return 1
    print(f"Wrote {len(report)} top frames to {out_dir}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
