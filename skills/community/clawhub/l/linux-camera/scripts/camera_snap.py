#!/usr/bin/env python3
"""Capture a single photo from a V4L2 webcam or RTSP camera using ffmpeg."""

import argparse
import os
import subprocess
import sys
import time


def snap_v4l2(device: str, output: str, width: int, height: int, warmup: int, quality: int):
    """Capture a frame from a V4L2 device."""
    warmup_frames = max(0, warmup)
    total_frames = warmup_frames + 1

    cmd = [
        "ffmpeg", "-y",
        "-f", "v4l2",
        "-video_size", f"{width}x{height}",
        "-i", device,
        "-frames:v", str(total_frames),
        "-q:v", str(max(1, min(31, (100 - quality) * 31 // 100 + 1))),
        "-update", "1",
        output,
    ]

    print(f"Capturing from {device} ({width}x{height}, warmup={warmup_frames} frames)...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

    if result.returncode != 0:
        print(f"ffmpeg error:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    if os.path.exists(output):
        size_kb = os.path.getsize(output) / 1024
        print(f"Saved: {output} ({size_kb:.1f} KB)")
    else:
        print(f"Failed to create {output}", file=sys.stderr)
        sys.exit(1)


def snap_rtsp(url: str, output: str, quality: int):
    """Capture a frame from an RTSP stream."""
    cmd = [
        "ffmpeg", "-y",
        "-rtsp_transport", "tcp",
        "-i", url,
        "-frames:v", "1",
        "-q:v", str(max(1, min(31, (100 - quality) * 31 // 100 + 1))),
        output,
    ]

    print(f"Capturing from RTSP stream...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

    if result.returncode != 0:
        print(f"ffmpeg error:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    if os.path.exists(output):
        size_kb = os.path.getsize(output) / 1024
        print(f"Saved: {output} ({size_kb:.1f} KB)")
    else:
        print(f"Failed to create {output}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Capture a photo from a camera")
    parser.add_argument("--device", type=str, default="/dev/video0",
                        help="V4L2 device path (default: /dev/video0)")
    parser.add_argument("--rtsp", type=str, default=None,
                        help="RTSP URL (use instead of --device for IP cameras)")
    parser.add_argument("--output", type=str, default="/tmp/camera_snap.jpg",
                        help="Output file path (default: /tmp/camera_snap.jpg)")
    parser.add_argument("--width", type=int, default=1280, help="Capture width (default: 1280)")
    parser.add_argument("--height", type=int, default=720, help="Capture height (default: 720)")
    parser.add_argument("--warmup", type=int, default=5,
                        help="Warmup frames to skip for exposure adjustment (default: 5)")
    parser.add_argument("--quality", type=int, default=90,
                        help="JPEG quality 1-100 (default: 90)")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

    if args.rtsp:
        snap_rtsp(args.rtsp, args.output, args.quality)
    else:
        if not os.path.exists(args.device):
            print(f"Device {args.device} not found. Run camera_list.py to see available cameras.",
                  file=sys.stderr)
            sys.exit(1)
        snap_v4l2(args.device, args.output, args.width, args.height, args.warmup, args.quality)


if __name__ == "__main__":
    main()
