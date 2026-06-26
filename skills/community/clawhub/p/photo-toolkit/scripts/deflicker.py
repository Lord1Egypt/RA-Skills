#!/usr/bin/env python3
"""
Deflicker — Smooth luminance fluctuations in a sequence of JPG frames.

Timelapse sequences often exhibit frame-to-frame brightness flicker due to
aperture/shutter micro-variations. This script applies a sliding-window
luminance smoothing to produce flicker-free results.

Algorithm:
  1. Compute mean luminance for each frame (sorted by filename)
  2. Apply a sliding-window average to create a smooth luminance curve
  3. Adjust each frame's brightness by the ratio: smoothed / actual
  4. Clamp correction ratios to 0.5–2.0× to prevent extreme adjustments

Dependencies:
    Python: pip install pillow numpy

Usage:
    python deflicker.py ~/Photos/graded
    python deflicker.py ~/Photos/graded --window 15
    python deflicker.py ~/Photos/graded --dry-run
"""

import argparse
import os
import re
import sys
import time
from pathlib import Path

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("❌ Missing dependencies: pillow, numpy", file=sys.stderr)
    print("   Install with: pip3 install pillow numpy", file=sys.stderr)
    sys.exit(1)


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


def compute_mean_luminance(img_path):
    """Compute mean luminance of a JPG image."""
    img = Image.open(img_path).convert("RGB")
    arr = np.array(img).astype(np.float64) / 255.0
    luminance = 0.2126 * arr[..., 0] + 0.7152 * arr[..., 1] + 0.0722 * arr[..., 2]
    return float(np.mean(luminance))


def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds) // 60
    secs = seconds - minutes * 60
    return f"{minutes}m {secs:.0f}s"


# ── Main ────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Smooth luminance fluctuations in a sequence of JPG frames (deflicker)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Algorithm:
  1. Compute mean luminance for each frame
  2. Sliding-window average → smooth luminance curve
  3. Adjust each frame: brightness *= smoothed / actual
  4. Clamp ratios to 0.5–2.0× for safety

Examples:
  %(prog)s ~/Photos/graded
  %(prog)s ~/Photos/graded --window 15
  %(prog)s ~/Photos/graded --dry-run
        """,
    )
    parser.add_argument("input", help="Directory containing JPG frames")
    parser.add_argument("--window", type=int, default=None, help="Sliding window size, odd number (default: 11)")
    parser.add_argument("--quality", type=int, default=None, help="Output JPEG quality (default: 95)")
    parser.add_argument("--config", type=str, default=None, help="Path to config.toml")
    parser.add_argument("--dry-run", action="store_true", help="Analyze without modifying files")
    parser.add_argument("--backup", action="store_true", help="Create backup copies before modifying (saved as .bak)")

    args = parser.parse_args()
    cfg = load_config(args.config)

    window = args.window if args.window is not None else cfg.get("deflicker_window", 11)
    quality = args.quality if args.quality is not None else cfg.get("jpeg_quality", 95)

    # Ensure odd window
    if window % 2 == 0:
        window += 1

    input_dir = Path(args.input).expanduser().resolve()
    if not input_dir.exists():
        print(f"❌ Directory not found: {input_dir}", file=sys.stderr)
        sys.exit(1)

    # ── Find frames ──────────────────────────────────────────────
    frames = find_jpg_frames(input_dir)
    if len(frames) < 3:
        print(f"❌ Need at least 3 JPG frames for deflicker, found {len(frames)}")
        sys.exit(1)

    print(f"📷 Found {len(frames)} JPG frame(s)")
    print(f"   Window: {window}")

    # ── Step 1: Compute luminances ───────────────────────────────
    print(f"\n━━━ Step 1/2: Analyzing luminance ━━━\n")
    start = time.monotonic()
    luminances = []
    for i, f in enumerate(frames):
        lum = compute_mean_luminance(f)
        luminances.append(lum)
        if (i + 1) % 50 == 0 or i == len(frames) - 1:
            print(f"  [{i+1}/{len(frames)}] analyzed")

    lum_array = np.array(luminances)
    analyze_elapsed = time.monotonic() - start
    print(
        f"\n  Luminance range: {lum_array.min():.4f} → {lum_array.max():.4f} (Δ{lum_array.max() - lum_array.min():.4f})"
    )
    print(f"  Analyzed in {format_time(analyze_elapsed)}")

    # ── Compute smoothed luminance ───────────────────────────────
    n = len(luminances)
    half_w = window // 2
    smoothed = np.zeros(n)
    for i in range(n):
        lo = max(0, i - half_w)
        hi = min(n, i + half_w + 1)
        smoothed[i] = np.mean(lum_array[lo:hi])

    ratios = np.where(lum_array > 1e-6, smoothed / lum_array, 1.0)
    ratios = np.clip(ratios, 0.5, 2.0)

    need_adjust = np.sum(np.abs(ratios - 1.0) >= 0.005)
    max_correction = np.max(np.abs(ratios - 1.0))
    print(f"  Frames needing adjustment: {need_adjust}/{n}")
    print(f"  Max correction: {max_correction:.4f} ({max_correction*100:.1f}%)")

    if args.dry_run:
        print(f"\n🔍 Dry run — no files modified")
        # Show top corrections
        corrections = [(i, ratios[i]) for i in range(n) if abs(ratios[i] - 1.0) >= 0.005]
        corrections.sort(key=lambda x: abs(x[1] - 1.0), reverse=True)
        if corrections:
            print(f"   Top corrections:")
            for idx, ratio in corrections[:10]:
                direction = "↑" if ratio > 1.0 else "↓"
                print(f"     {frames[idx].name}: {direction} {abs(ratio-1.0)*100:.1f}%")
        sys.exit(0)

    # ── Step 2: Apply corrections ────────────────────────────────
    print(f"\n━━━ Step 2/2: Applying corrections ━━━\n")
    adjust_start = time.monotonic()
    adjusted = 0

    # Create backups if requested
    if args.backup:
        print("  Creating backups...")
        import shutil

        for i, frame_path in enumerate(frames):
            if abs(ratios[i] - 1.0) >= 0.005:
                backup_path = frame_path.with_suffix(".jpg.bak")
                if not backup_path.exists():
                    shutil.copy2(frame_path, backup_path)
        print(f"  ✓ Backups created (.jpg.bak)\n")

    for i in range(n):
        if abs(ratios[i] - 1.0) < 0.005:
            continue

        frame_path = frames[i]
        img = Image.open(frame_path)
        arr = np.array(img).astype(np.float64)
        arr *= ratios[i]
        arr = np.clip(arr, 0, 255).astype(np.uint8)
        Image.fromarray(arr).save(frame_path, format="JPEG", quality=quality, optimize=True, subsampling=0)
        adjusted += 1

        if adjusted % 50 == 0:
            print(f"  [{adjusted}] frames adjusted...")

    adjust_elapsed = time.monotonic() - adjust_start
    total_elapsed = time.monotonic() - start

    print(f"\n{'─' * 55}")
    print(f"✅ Done in {format_time(total_elapsed)}")
    print(f"   Adjusted: {adjusted}  |  Unchanged: {n - adjusted}")
    print(f"   Directory: {input_dir}")


if __name__ == "__main__":
    main()
