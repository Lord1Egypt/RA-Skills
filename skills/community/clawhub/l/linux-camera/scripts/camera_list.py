#!/usr/bin/env python3
"""List available V4L2 video capture devices on Linux."""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def get_v4l2_devices():
    """Return a list of V4L2 video devices with metadata."""
    devices = []
    dev_path = Path("/dev")
    video_devs = sorted(dev_path.glob("video*"))

    for dev in video_devs:
        info = {"path": str(dev), "name": "", "driver": "", "formats": []}

        try:
            result = subprocess.run(
                ["v4l2-ctl", "--device", str(dev), "--info"],
                capture_output=True, text=True, timeout=5,
            )
            for line in result.stdout.splitlines():
                line = line.strip()
                if line.startswith("Card type"):
                    info["name"] = line.split(":", 1)[1].strip()
                elif line.startswith("Driver name"):
                    info["driver"] = line.split(":", 1)[1].strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        try:
            result = subprocess.run(
                ["v4l2-ctl", "--device", str(dev), "--list-formats-ext"],
                capture_output=True, text=True, timeout=5,
            )
            capture_capable = False
            for line in result.stdout.splitlines():
                stripped = line.strip()
                if "Video Capture" in stripped:
                    capture_capable = True
                if stripped.startswith("Size:"):
                    info["formats"].append(stripped)
            if not capture_capable:
                continue
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        devices.append(info)

    return devices


def main():
    parser = argparse.ArgumentParser(description="List available cameras on Linux")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    devices = get_v4l2_devices()

    if not devices:
        print("No video capture devices found.", file=sys.stderr)
        print("Make sure a camera is connected and v4l-utils is installed:")
        print("  sudo apt-get install -y v4l-utils")
        sys.exit(1)

    if args.json:
        print(json.dumps(devices, indent=2))
        return

    print(f"Found {len(devices)} camera(s):\n")
    for i, dev in enumerate(devices):
        name = dev["name"] or "Unknown"
        print(f"  [{i}] {dev['path']}  —  {name}")
        if dev["driver"]:
            print(f"      Driver: {dev['driver']}")
        if dev["formats"]:
            print(f"      Resolutions: {', '.join(dev['formats'][:5])}")
        print()


if __name__ == "__main__":
    main()
