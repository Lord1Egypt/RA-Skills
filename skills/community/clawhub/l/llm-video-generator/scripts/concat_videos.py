#!/opt/anaconda3/bin/python3
"""
Concatenate multiple video files into one using ffmpeg.

Usage:
    python concat_videos.py --inputs v1.mp4 v2.mp4 v3.mp4 --output final.mp4

All input videos should have the same resolution and fps for best results.
"""

import argparse
import os
import subprocess
import sys
import tempfile


def concat_videos(input_files, output_path):
    for f in input_files:
        if not os.path.isfile(f):
            print(f"ERROR: File not found: {f}", file=sys.stderr)
            sys.exit(1)

    # Create concat list file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp:
        for f in input_files:
            tmp.write(f"file '{os.path.abspath(f)}'\n")
        list_path = tmp.name

    try:
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", list_path,
            "-c", "copy",
            output_path
        ]
        print(f"Concatenating {len(input_files)} videos...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            # Fallback: re-encode if copy fails (different codecs)
            print("Direct copy failed, trying re-encode...")
            cmd_reencode = [
                "ffmpeg", "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", list_path,
                "-c:v", "libx264",
                "-c:a", "aac",
                "-movflags", "+faststart",
                output_path
            ]
            result2 = subprocess.run(cmd_reencode, capture_output=True, text=True)
            if result2.returncode != 0:
                print(f"ERROR: ffmpeg concat failed:\n{result2.stderr}", file=sys.stderr)
                sys.exit(1)

        size_mb = os.path.getsize(output_path) / 1024 / 1024
        print(f"✅ Concatenated video saved: {output_path} ({size_mb:.1f} MB)")
        return output_path
    finally:
        os.unlink(list_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Concatenate video files")
    parser.add_argument("--inputs", nargs="+", required=True, help="Input video files")
    parser.add_argument("--output", required=True, help="Output video path")
    args = parser.parse_args()
    concat_videos(args.inputs, args.output)
