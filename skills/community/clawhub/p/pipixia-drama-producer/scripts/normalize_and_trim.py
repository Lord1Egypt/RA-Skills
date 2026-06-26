#!/usr/bin/env python3
"""
normalize_and_trim.py - Normalize video clips to 1280x720 24fps and trim N seconds from the start
Usage: python3 normalize_and_trim.py input.mp4 output.mp4 [--trim 1] [--width 1280] [--height 720]
"""

import argparse
import subprocess
import sys
import os

FFMPEG = os.environ.get("FFMPEG", "ffmpeg")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--trim", type=float, default=1.0, help="Seconds to trim from start")
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument("--fps", type=int, default=24)
    args = parser.parse_args()

    # Step 1: Normalize
    norm_out = args.output + ".norm.mp4"
    vf = (f"scale={args.width}:{args.height}:force_original_aspect_ratio=decrease,"
          f"pad={args.width}:{args.height}:(ow-iw)/2:(oh-ih)/2:black,fps={args.fps}")
    
    cmd1 = [FFMPEG, "-y", "-hide_banner", "-i", args.input,
            "-vf", vf,
            "-c:v", "libx264", "-crf", "22", "-preset", "fast",
            "-c:a", "aac", "-ar", "44100", "-ac", "2",
            norm_out]
    r1 = subprocess.run(cmd1, capture_output=True, text=True)
    if r1.returncode != 0:
        print("✗ Normalize failed:", r1.stderr[-300:])
        sys.exit(1)

    # Step 2: Trim
    cmd2 = [FFMPEG, "-y", "-hide_banner", "-i", norm_out,
            "-ss", str(args.trim),
            "-c:v", "libx264", "-crf", "22", "-preset", "fast",
            "-c:a", "aac", "-ar", "44100", "-ac", "2",
            args.output]
    r2 = subprocess.run(cmd2, capture_output=True, text=True)
    if r2.returncode != 0:
        print("✗ Trim failed:", r2.stderr[-300:])
        sys.exit(1)

    os.remove(norm_out)
    print(f"✓ {args.input} → {args.output} (trim {args.trim}s)")

if __name__ == "__main__":
    main()
