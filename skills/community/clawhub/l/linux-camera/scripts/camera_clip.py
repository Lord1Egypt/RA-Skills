#!/usr/bin/env python3
"""Record a video clip from a V4L2 webcam or RTSP camera using ffmpeg."""

import argparse
import os
import subprocess
import sys


def clip_v4l2(device: str, output: str, duration: float, width: int, height: int, fps: int):
    """Record a clip from a V4L2 device."""
    cmd = [
        "ffmpeg", "-y",
        "-f", "v4l2",
        "-video_size", f"{width}x{height}",
        "-framerate", str(fps),
        "-i", device,
        "-t", str(duration),
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-pix_fmt", "yuv420p",
        output,
    ]

    print(f"Recording {duration}s from {device} ({width}x{height} @ {fps}fps)...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=duration + 30)

    if result.returncode != 0:
        print(f"ffmpeg error:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    if os.path.exists(output):
        size_mb = os.path.getsize(output) / (1024 * 1024)
        print(f"Saved: {output} ({size_mb:.1f} MB)")
    else:
        print(f"Failed to create {output}", file=sys.stderr)
        sys.exit(1)


def clip_rtsp(url: str, output: str, duration: float, fps: int):
    """Record a clip from an RTSP stream."""
    cmd = [
        "ffmpeg", "-y",
        "-rtsp_transport", "tcp",
        "-i", url,
        "-t", str(duration),
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-r", str(fps),
        "-pix_fmt", "yuv420p",
        output,
    ]

    print(f"Recording {duration}s from RTSP stream...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=duration + 30)

    if result.returncode != 0:
        print(f"ffmpeg error:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    if os.path.exists(output):
        size_mb = os.path.getsize(output) / (1024 * 1024)
        print(f"Saved: {output} ({size_mb:.1f} MB)")
    else:
        print(f"Failed to create {output}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Record a video clip from a camera")
    parser.add_argument("--device", type=str, default="/dev/video0",
                        help="V4L2 device path (default: /dev/video0)")
    parser.add_argument("--rtsp", type=str, default=None,
                        help="RTSP URL (use instead of --device for IP cameras)")
    parser.add_argument("--output", type=str, default="/tmp/camera_clip.mp4",
                        help="Output file path (default: /tmp/camera_clip.mp4)")
    parser.add_argument("--duration", type=float, default=5.0,
                        help="Recording duration in seconds (default: 5)")
    parser.add_argument("--width", type=int, default=1280, help="Capture width (default: 1280)")
    parser.add_argument("--height", type=int, default=720, help="Capture height (default: 720)")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second (default: 30)")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

    if args.rtsp:
        clip_rtsp(args.rtsp, args.output, args.duration, args.fps)
    else:
        if not os.path.exists(args.device):
            print(f"Device {args.device} not found. Run camera_list.py to see available cameras.",
                  file=sys.stderr)
            sys.exit(1)
        clip_v4l2(args.device, args.output, args.duration, args.width, args.height, args.fps)


if __name__ == "__main__":
    main()
