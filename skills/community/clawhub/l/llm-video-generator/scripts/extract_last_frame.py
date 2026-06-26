#!/opt/anaconda3/bin/python3
"""
Extract the last frame from a video file using ffmpeg.

Usage:
    python extract_last_frame.py <video_path> [--output <output_path>]

Output: PNG image of the last frame.
"""

import argparse
import os
import subprocess
import sys


def extract_last_frame(video_path, output_path=None):
    if not os.path.isfile(video_path):
        print(f"ERROR: Video file not found: {video_path}", file=sys.stderr)
        sys.exit(1)

    if output_path is None:
        base = os.path.splitext(video_path)[0]
        output_path = f"{base}_last_frame.png"

    # Use ffmpeg: seek to near end, grab last frame
    cmd = [
        "ffmpeg", "-y",
        "-sseof", "-0.1",       # seek to 0.1s before end
        "-i", video_path,
        "-frames:v", "1",       # grab 1 frame
        "-q:v", "2",            # high quality
        output_path
    ]
    print(f"Extracting last frame from {video_path}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        # Fallback: try without sseof (some videos are very short)
        cmd2 = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", "select='eq(n,0)'",  # will be overridden below
            "-frames:v", "1",
            "-q:v", "2",
            output_path
        ]
        # Get frame count first
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
             "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", video_path],
            capture_output=True, text=True
        )
        try:
            total_frames = int(probe.stdout.strip())
            last_idx = max(0, total_frames - 1)
        except ValueError:
            last_idx = 0

        cmd_fallback = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", f"select='eq(n\\,{last_idx})'",
            "-vsync", "vfr",
            "-frames:v", "1",
            "-q:v", "2",
            output_path
        ]
        result2 = subprocess.run(cmd_fallback, capture_output=True, text=True)
        if result2.returncode != 0:
            print(f"ERROR: ffmpeg failed:\n{result2.stderr}", file=sys.stderr)
            sys.exit(1)

    if os.path.isfile(output_path):
        print(f"✅ Last frame saved: {output_path}")
        return output_path
    else:
        print(f"ERROR: Output file not created", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract last frame from video")
    parser.add_argument("video_path", help="Path to the video file")
    parser.add_argument("--output", default=None, help="Output image path (default: <video>_last_frame.png)")
    args = parser.parse_args()
    extract_last_frame(args.video_path, args.output)
