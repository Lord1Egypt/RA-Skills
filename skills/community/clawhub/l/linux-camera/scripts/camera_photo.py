#!/usr/bin/env python3
"""
Take a photo from any connected camera. Simplest possible interface.

Usage:
  python camera_photo.py                          # default camera, saves to /tmp/photo.jpg
  python camera_photo.py front                    # /dev/video0
  python camera_photo.py back                     # /dev/video2
  python camera_photo.py /dev/video4              # explicit device
  python camera_photo.py front photo_name.jpg     # custom filename
"""

import os
import subprocess
import sys
import time
from datetime import datetime

CAMERAS = {
    "front": "/dev/video0",
    "back": "/dev/video2",
    "0": "/dev/video0",
    "2": "/dev/video2",
}

DEFAULT_DEVICE = "/dev/video0"
DEFAULT_DIR = "/tmp"


def find_first_camera():
    """Find the first available video device."""
    for i in range(10):
        dev = f"/dev/video{i}"
        if os.path.exists(dev):
            return dev
    return None


def take_photo(device: str, output: str, width: int = 1280, height: int = 720):
    """Capture a single JPEG frame using ffmpeg."""
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "v4l2",
        "-video_size", f"{width}x{height}",
        "-i", device,
        "-frames:v", "6",
        "-q:v", "2",
        "-update", "1",
        output,
    ]

    print(f"Taking photo from {device}...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)

    if result.returncode != 0:
        print(f"Error: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)

    if os.path.exists(output):
        size_kb = os.path.getsize(output) / 1024
        print(f"Saved: {output} ({size_kb:.0f} KB)")
    else:
        print("Failed to capture photo", file=sys.stderr)
        sys.exit(1)


def main():
    args = sys.argv[1:]

    # Resolve device
    if not args:
        device = find_first_camera()
        if not device:
            print("No camera found. Connect a USB camera and try again.", file=sys.stderr)
            sys.exit(1)
    elif args[0] in CAMERAS:
        device = CAMERAS[args[0]]
    elif args[0].startswith("/dev/"):
        device = args[0]
    else:
        device = find_first_camera() or DEFAULT_DEVICE

    if not os.path.exists(device):
        print(f"Device {device} not found. Available cameras:", file=sys.stderr)
        for i in range(10):
            dev = f"/dev/video{i}"
            if os.path.exists(dev):
                print(f"  {dev}", file=sys.stderr)
        sys.exit(1)

    # Resolve output filename
    if len(args) >= 2:
        output = args[1]
        if not output.startswith("/"):
            output = os.path.join(DEFAULT_DIR, output)
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = os.path.join(DEFAULT_DIR, f"photo_{ts}.jpg")

    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
    take_photo(device, output)


if __name__ == "__main__":
    main()
