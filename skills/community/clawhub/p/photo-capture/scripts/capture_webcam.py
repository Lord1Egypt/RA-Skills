#!/usr/bin/env python3
"""
capture_webcam.py - Cross‑platform webcam snapshot utility.

Supported platforms:
- macOS (avfoundation)
- Windows (dshow)
- Linux (v4l2)

Requirements:
- ffmpeg must be available in PATH
- A webcam device must be present
"""

import argparse
import glob
import os
import pathlib
import platform
import re
import shutil
import subprocess
import sys
from typing import Dict, List, Optional


def run(cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and capture its output."""
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


def require_ffmpeg() -> str:
    """Ensure ffmpeg is available in PATH."""
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError(
            "ffmpeg is required but was not found in PATH.\n"
            "Install it via:\n"
            "  macOS: brew install ffmpeg\n"
            "  Windows: winget install ffmpeg or download from https://ffmpeg.org\n"
            "  Linux: apt install ffmpeg / yum install ffmpeg / pacman -S ffmpeg\n"
        )
    return ffmpeg


def current_platform() -> str:
    """Detect the current platform."""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    if system == "windows":
        return "windows"
    if system == "linux":
        return "linux"
    raise RuntimeError(f"Unsupported platform: {platform.system()}")


def list_macos_devices(ffmpeg: str) -> List[Dict[str, str]]:
    """List video devices on macOS using AVFoundation."""
    proc = run([ffmpeg, "-f", "avfoundation", "-list_devices", "true", "-i", ""], check=False)
    text = (proc.stderr or "") + "\n" + (proc.stdout or "")
    devices: List[Dict[str, str]] = []
    in_video_section = False
    for line in text.splitlines():
        if "AVFoundation video devices" in line:
            in_video_section = True
            continue
        if in_video_section and "AVFoundation audio devices" in line:
            break
        match = re.search(r"\[(\d+)\]\s+(.+)$", line)
        if in_video_section and match:
            devices.append({"id": match.group(1).strip(), "label": match.group(2).strip()})
    return devices


def list_windows_devices(ffmpeg: str) -> List[Dict[str, str]]:
    """List video devices on Windows using DirectShow."""
    proc = run([ffmpeg, "-list_devices", "true", "-f", "dshow", "-i", "dummy"], check=False)
    text = (proc.stderr or "") + "\n" + (proc.stdout or "")
    devices: List[Dict[str, str]] = []
    in_video_section = False
    for line in text.splitlines():
        if "DirectShow video devices" in line:
            in_video_section = True
            continue
        if in_video_section and "DirectShow audio devices" in line:
            break
        match = re.search(r'"([^"]+)"', line)
        if in_video_section and match:
            label = match.group(1).strip()
            devices.append({"id": label, "label": label})
    return devices


def list_linux_devices() -> List[Dict[str, str]]:
    """List video devices on Linux using /dev/video* pattern."""
    return [
        {"id": path, "label": path}
        for path in sorted(glob.glob("/dev/video*"))
        if os.path.exists(path)
    ]


def list_devices(platform_name: str, ffmpeg: str) -> List[Dict[str, str]]:
    """Get the list of available camera devices for the current platform."""
    if platform_name == "macos":
        return list_macos_devices(ffmpeg)
    if platform_name == "windows":
        return list_windows_devices(ffmpeg)
    if platform_name == "linux":
        return list_linux_devices()
    return []


def format_device_list(devices: List[Dict[str, str]]) -> str:
    """Format device list for display."""
    return "\n".join(f"  [{device['id']}] {device['label']}" for device in devices)


def choose_device(platform_name: str, ffmpeg: str, requested: Optional[str]) -> str:
    """Select a camera device, either by user request or auto-detect."""
    devices = list_devices(platform_name, ffmpeg)
    if not devices:
        raise RuntimeError(
            "No camera device found.\n"
            "Make sure your webcam is connected and recognized by the system."
        )

    if not requested:
        return devices[0]["id"]

    # Allow matching by either id or label (case-insensitive)
    requested_lower = requested.strip().lower()
    for device in devices:
        if requested_lower in {device["id"].lower(), device["label"].lower()}:
            return device["id"]

    raise RuntimeError(
        f"Requested camera device '{requested}' was not found.\n"
        f"Available devices:\n{format_device_list(devices)}"
    )


def capture_args(platform_name: str, device: str, width: int, height: int, fps: int) -> List[str]:
    """Build ffmpeg input arguments for the given platform."""
    video_size = f"{width}x{height}"
    if platform_name == "macos":
        return [
            "-f", "avfoundation",
            "-framerate", str(fps),
            "-video_size", video_size,
            "-i", f"{device}:none",  # :none disables audio input
        ]
    if platform_name == "windows":
        return [
            "-f", "dshow",
            "-video_size", video_size,
            "-framerate", str(fps),
            "-i", f"video={device}",
        ]
    if platform_name == "linux":
        return [
            "-f", "v4l2",
            "-video_size", video_size,
            "-framerate", str(fps),
            "-i", device,
        ]
    raise RuntimeError(f"Unsupported platform: {platform_name}")


def explain_capture_error(stderr: str, stdout: str) -> str:
    """Translate common ffmpeg errors into user-friendly messages."""
    combined = (stderr or "") + "\n" + (stdout or "")
    lower = combined.lower()

    if "permission denied" in lower or "not authorized" in lower or "operation not permitted" in lower:
        return (
            "Camera permission was denied by the operating system.\n"
            "Grant camera access to your terminal or Python process in System Preferences / Settings."
        )
    if "cannot open video device" in lower or "no such file or directory" in lower:
        return "The selected camera device could not be opened. It may be in use by another application."
    if "input/output error" in lower or "ioctl" in lower:
        return "The camera exists but ffmpeg could not read from it. Try a different resolution or device."
    if "could not find video device" in lower or "no video device" in lower:
        return "No usable camera device was detected. Check that your webcam is connected."
    if "not found in path" in lower:
        return "ffmpeg is missing from PATH. Install ffmpeg and try again."

    return combined.strip() or "ffmpeg capture failed with an unknown error."


def capture_frame(
    ffmpeg: str,
    platform_name: str,
    device: str,
    output_path: pathlib.Path,
    width: int,
    height: int,
    fps: int,
    warmup: float,
) -> None:
    """Capture a single frame from the webcam and save to output_path."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        ffmpeg,
        "-hide_banner",
        "-loglevel", "error",
        "-y",  # overwrite output
        *capture_args(platform_name, device, width, height, fps),
    ]

    # Warmup: skip N seconds to allow camera auto-exposure to stabilize
    if warmup > 0:
        cmd += ["-ss", str(warmup)]

    cmd += [
        "-frames:v", "1",  # capture exactly 1 frame
        "-q:v", "2",       # high quality JPEG
        str(output_path),
    ]

    proc = run(cmd, check=False)

    if proc.returncode != 0 or not output_path.exists() or output_path.stat().st_size == 0:
        raise RuntimeError(explain_capture_error(proc.stderr, proc.stdout))


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="📷 Capture a single frame from your webcam on macOS, Windows, or Linux.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python3 capture_webcam.py --output photo.jpg\n"
            "  python3 capture_webcam.py --list-devices\n"
            "  python3 capture_webcam.py --device 1 --output cam2.jpg\n"
            "  python3 capture_webcam.py --width 1920 --height 1080 --output hd.jpg\n"
        ),
    )
    parser.add_argument(
        "--output",
        help="Path to save the captured image (required unless --list-devices)",
    )
    parser.add_argument(
        "--device",
        help="Camera device ID, name, or path (auto-select if omitted)",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1280,
        help="Video width in pixels (default: 1280)",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=720,
        help="Video height in pixels (default: 720)",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=30,
        help="Frames per second for capture (default: 30)",
    )
    parser.add_argument(
        "--warmup",
        type=float,
        default=1.0,
        help="Seconds to wait before capture for auto-exposure (default: 1.0)",
    )
    parser.add_argument(
        "--list-devices",
        action="store_true",
        help="List available camera devices and exit",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        ffmpeg = require_ffmpeg()
        platform_name = current_platform()

        if args.list_devices:
            devices = list_devices(platform_name, ffmpeg)
            if not devices:
                print("❌ No camera devices found.", file=sys.stderr)
                return 1
            print("📷 Available camera devices:")
            for device in devices:
                print(f"  [{device['id']}] {device['label']}")
            return 0

        if not args.output:
            print("❌ --output is required unless --list-devices is used.", file=sys.stderr)
            return 2

        device = choose_device(platform_name, ffmpeg, args.device)
        output_path = pathlib.Path(args.output).expanduser().resolve()

        print(f"📷 Capturing from device [{device}]...")
        capture_frame(
            ffmpeg=ffmpeg,
            platform_name=platform_name,
            device=device,
            output_path=output_path,
            width=args.width,
            height=args.height,
            fps=args.fps,
            warmup=args.warmup,
        )

        print(f"✅ Saved to: {output_path}")

    except Exception as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())