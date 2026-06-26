#!/usr/bin/env python3
"""
Assemble — Combine a sequence of JPG frames into an MP4 video via FFmpeg.

Takes a directory of sequentially-named JPG files and encodes them into
an H.264 MP4 video using FFmpeg. Frames are sorted by natural filename order.

Dependencies:
    System: ffmpeg (brew install ffmpeg / apt-get install ffmpeg)
    Python: (none beyond stdlib)

Usage:
    python assemble.py ~/Photos/graded --output timelapse.mp4
    python assemble.py ~/Photos/graded --output timelapse.mp4 --fps 30 --crf 15
    python assemble.py ~/Photos/graded --dry-run
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


# ── Configuration ───────────────────────────────────────────────

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

_SKILL_DIR = Path(__file__).resolve().parent.parent
_ROOT_DIR = _SKILL_DIR.parent
_DEFAULT_CONFIG_PATH = (
    _SKILL_DIR / "config.toml" if (_SKILL_DIR / "config.toml").exists() else _ROOT_DIR / "config.toml"
)


def load_config(config_path=None):
    """Load configuration from config.toml."""
    path = Path(config_path or _DEFAULT_CONFIG_PATH).expanduser().resolve()
    if not path.exists():
        return {}
    try:
        with open(path, "rb") as f:
            cfg = tomllib.load(f)
        if not isinstance(cfg, dict):
            return {}
        print(f"📄 Loaded config: {path}")
        return cfg
    except Exception:
        return {}


# ── Helpers ─────────────────────────────────────────────────────

JPG_EXTENSIONS = {".jpg", ".jpeg"}


def natural_sort_key(path):
    """Natural sort key: frame_0001 < frame_0002 < frame_0010."""
    parts = re.split(r"(\d+)", path.stem.lower())
    return [int(p) if p.isdigit() else p for p in parts]


def find_jpg_frames(input_dir):
    """Find all JPG files in directory, sorted by natural filename order."""
    input_dir = Path(input_dir)
    results = []
    for p in input_dir.iterdir():
        if p.is_file() and p.suffix.lower() in JPG_EXTENSIONS:
            results.append(p)
    results.sort(key=natural_sort_key)
    return results


# ── Main ────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Assemble JPG frames into an MP4 video via FFmpeg",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
System dependency: ffmpeg
  macOS:  brew install ffmpeg
  Debian: apt-get install ffmpeg
  RHEL:   dnf install ffmpeg

Examples:
  %(prog)s ~/Photos/graded --output timelapse.mp4
  %(prog)s ~/Photos/graded -o timelapse.mp4 --fps 30 --crf 15
  %(prog)s ~/Photos/graded --dry-run
        """,
    )
    parser.add_argument("input", help="Directory containing JPG frames")
    parser.add_argument(
        "--output", "-o", type=str, default=None, help="Output video path (default: <input>/../timelapse.mp4)"
    )
    parser.add_argument("--fps", type=int, default=None, help="Video frame rate (default: 25)")
    parser.add_argument(
        "--crf", type=int, default=None, help="H.264 CRF quality: 0=lossless, 18=high, 23=default (default: 18)"
    )
    parser.add_argument("--config", type=str, default=None, help="Path to config.toml")
    parser.add_argument("--dry-run", action="store_true", help="Preview without encoding")

    args = parser.parse_args()
    cfg = load_config(args.config)

    fps = args.fps if args.fps is not None else cfg.get("fps", 25)
    crf = args.crf if args.crf is not None else cfg.get("crf", 18)

    input_dir = Path(args.input).expanduser().resolve()
    if not input_dir.exists():
        print(f"❌ Directory not found: {input_dir}", file=sys.stderr)
        sys.exit(1)

    # Output path
    if args.output:
        output_path = Path(args.output).expanduser().resolve()
    else:
        output_path = input_dir.parent / "timelapse.mp4"

    # ── Check FFmpeg ─────────────────────────────────────────────
    if not shutil.which("ffmpeg"):
        print("❌ FFmpeg not found.", file=sys.stderr)
        print("   Install with: brew install ffmpeg (macOS) / apt-get install ffmpeg", file=sys.stderr)
        sys.exit(1)

    # ── Find frames ──────────────────────────────────────────────
    frames = find_jpg_frames(input_dir)
    if not frames:
        print("❌ No JPG frames found in input directory.")
        sys.exit(1)

    duration = len(frames) / fps
    duration_str = f"{duration:.1f}s" if duration < 60 else f"{int(duration)//60}m {int(duration)%60}s"
    print(f"📷 Found {len(frames)} JPG frame(s)")
    print(f"   Duration: {duration_str} ({len(frames)} frames @ {fps}fps)")
    print(f"   CRF: {crf}")
    print(f"   Output: {output_path}")

    if args.dry_run:
        print(f"\n🔍 Dry run — no video created")
        print(f"   First frame: {frames[0].name}")
        print(f"   Last frame:  {frames[-1].name}")
        sys.exit(0)

    # ── Create sequential symlinks for FFmpeg ────────────────────
    # FFmpeg needs sequentially numbered files (frame_000001.jpg, frame_000002.jpg, ...)
    # Create temp dir with symlinks to ensure correct ordering
    tmp_dir = tempfile.mkdtemp(prefix="assemble_frames_")
    try:
        for i, frame in enumerate(frames):
            link_name = f"frame_{i:06d}.jpg"
            os.symlink(str(frame), os.path.join(tmp_dir, link_name))

        input_pattern = os.path.join(tmp_dir, "frame_%06d.jpg")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            "ffmpeg",
            "-y",
            "-framerate",
            str(fps),
            "-i",
            input_pattern,
            "-c:v",
            "libx264",
            "-crf",
            str(crf),
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(output_path),
        ]

        print(f"\n🎬 Encoding video...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"\n❌ FFmpeg failed (exit code {result.returncode}):", file=sys.stderr)
            stderr_lines = result.stderr.strip().split("\n")
            for line in stderr_lines[-10:]:
                print(f"   {line}", file=sys.stderr)
            sys.exit(1)

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    # ── Summary ──────────────────────────────────────────────────
    if output_path.exists():
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"\n{'─' * 55}")
        print(f"✅ Video created: {output_path}")
        print(f"   Size: {size_mb:.1f} MB")
        print(f"   Duration: {duration_str} @ {fps}fps")
    else:
        print("❌ Video file was not created", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
