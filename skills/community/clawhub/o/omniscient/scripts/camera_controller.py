#!/usr/bin/env python3
"""
Camera Controller - Manage cameras and capture images on Windows.

Capabilities:
  - List all cameras/webcams
  - Capture photo from camera
  - Camera info and capabilities

Requirements: Windows 10/11, PowerShell 5.1+
Dependencies: opencv-python (auto-installed for capture); for listing uses WMI
"""

import subprocess
import sys
import os
import json
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import run_ps as _run_ps


def _validate_output_path(path):
    """Validate output file path to prevent arbitrary file writes.

    Only allows writing to user-writable locations: home dir, Desktop,
    Documents, Downloads, Temp, and current working directory.
    """
    if path is None:
        return None
    resolved = os.path.realpath(os.path.expanduser(path))
    if '..' in os.path.normpath(path).replace(os.sep, '/').split('/'):
        return None
    home = os.path.realpath(os.path.expanduser("~"))
    if resolved.startswith(home + os.sep) or resolved == home:
        return resolved
    temp = os.path.realpath(os.environ.get('TEMP', os.environ.get('TMP', '')))
    if temp and (resolved.startswith(temp + os.sep) or resolved == temp):
        return resolved
    cwd = os.path.realpath(os.getcwd())
    if resolved.startswith(cwd + os.sep) or resolved == cwd:
        return resolved
    return None


def _ensure_opencv():
    try:
        import cv2
        return cv2
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python-headless>=4.9.0.80,<5", "-q"])
        import cv2
        return cv2


# ========== List Cameras ==========

def list_cameras():
    """List all available cameras via WMI and OpenCV."""
    results = {"wmi": [], "opencv": []}

    # WMI method
    script = r"""
try {
    Get-CimInstance Win32_PnPEntity | Where-Object {
        ($_.PNPClass -eq 'Camera' -or $_.PNPClass -eq 'Image' -or 
         $_.Name -match 'camera|webcam|capture|video|cam') -and 
         $_.Status -eq 'OK'
    } | ForEach-Object {
        [PSCustomObject]@{
            Name = $_.Name
            DeviceID = $_.DeviceID
            Status = $_.Status
            Manufacturer = $_.Manufacturer
        }
    } | ConvertTo-Json -Compress
} catch {
    Write-Output '[]'
}
"""
    stdout, _, _ = _run_ps(script, timeout=10)
    if stdout and stdout != '[]':
        try:
            wmi_devices = json.loads(stdout)
            if isinstance(wmi_devices, list):
                results["wmi"] = wmi_devices
            else:
                results["wmi"] = [wmi_devices]
        except Exception:
            pass

    # OpenCV method (actual working cameras)
    try:
        cv2 = _ensure_opencv()
        index = 0
        while True:
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                backend = cap.getBackendName()
                results["opencv"].append({
                    "Index": index,
                    "Resolution": f"{w}x{h}",
                    "FPS": round(fps, 1) if fps > 0 else None,
                    "Backend": backend,
                })
                cap.release()
                index += 1
            else:
                cap.release()
                break
    except Exception as e:
        results["opencv_error"] = str(e)

    return json.dumps(results, indent=2, ensure_ascii=False)


# ========== Camera Info ==========

def camera_info(camera_index=0):
    """Get detailed camera info."""
    try:
        cv2 = _ensure_opencv()
    except Exception as e:
        return f'ERROR: Could not install opencv: {e}'

    try:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            return f"ERROR: Could not open camera {camera_index}"

        props = {
            "Index": camera_index,
            "Backend": cap.getBackendName(),
            "Width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "Height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "FPS": cap.get(cv2.CAP_PROP_FPS),
            "Brightness": cap.get(cv2.CAP_PROP_BRIGHTNESS),
            "Contrast": cap.get(cv2.CAP_PROP_CONTRAST),
            "Saturation": cap.get(cv2.CAP_PROP_SATURATION),
            "Hue": cap.get(cv2.CAP_PROP_HUE),
            "Gain": cap.get(cv2.CAP_PROP_GAIN),
            "Exposure": cap.get(cv2.CAP_PROP_EXPOSURE),
            "AutoExposure": cap.get(cv2.CAP_PROP_AUTO_EXPOSURE),
            "Focus": cap.get(cv2.CAP_PROP_FOCUS),
            "AutoFocus": cap.get(cv2.CAP_PROP_AUTOFOCUS),
            "Zoom": cap.get(cv2.CAP_PROP_ZOOM),
            "Codec": int(cap.get(cv2.CAP_PROP_FOURCC)),
            "BufferCount": int(cap.get(cv2.CAP_PROP_BUFFERSIZE)),
        }

        # Get available resolutions (try common ones)
        resolutions = []
        common_resolutions = [
            (640, 480), (800, 600), (1024, 768),
            (1280, 720), (1920, 1080), (2560, 1440), (3840, 2160)
        ]
        for w, h in common_resolutions:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
            actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            if actual_w == w and actual_h == h:
                resolutions.append(f"{w}x{h}")

        # Restore original resolution
        cap.release()

        # Re-open to check supported
        cap2 = cv2.VideoCapture(camera_index)
        cap2.release()

        props["SupportedResolutions"] = resolutions if resolutions else ["Try capture to check actual resolution"]
        return json.dumps(props, indent=2, ensure_ascii=False)
    except Exception as e:
        return f'ERROR: {e}'


# ========== Capture Photo ==========

def capture_photo(output_file=None, camera_index=0, resolution=None):
    """Capture a photo from the specified camera."""
    try:
        cv2 = _ensure_opencv()
    except Exception as e:
        return f'ERROR: Could not install opencv: {e}'

    if output_file is None:
        output_file = os.path.join(os.path.expanduser("~"), "camera_capture.jpg")
    else:
        safe_path = _validate_output_path(output_file)
        if safe_path is None:
            return 'ERROR: Output path is not allowed. Files can only be saved to user directories (Home, Desktop, Documents, Downloads, Temp, CWD).'
        output_file = safe_path

    try:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            # Try to list available cameras
            available = []
            idx = 0
            while True:
                test = cv2.VideoCapture(idx)
                if test.isOpened():
                    available.append(str(idx))
                    test.release()
                    idx += 1
                else:
                    test.release()
                    break
            avail_str = ", ".join(available) if available else "None"
            return f"ERROR: Could not open camera {camera_index}. Available indices: {avail_str}"

        # Set resolution if specified
        if resolution:
            parts = resolution.lower().split("x")
            if len(parts) == 2:
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(parts[0]))
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(parts[1]))

        # Read a few frames to let camera warm up
        for _ in range(3):
            cap.read()

        ret, frame = cap.read()
        cap.release()

        if not ret:
            return "ERROR: Could not read frame from camera"

        # Save image
        cv2.imwrite(output_file, frame)
        h, w = frame.shape[:2]
        size_kb = os.path.getsize(output_file) / 1024
        return f"OK: Photo saved to '{output_file}' ({w}x{h}, {size_kb:.0f} KB)"
    except Exception as e:
        return f'ERROR: {e}'


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Camera Controller")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List all cameras")

    p_info = sub.add_parser("info", help="Camera details")
    p_info.add_argument("--index", type=int, default=0, help="Camera index")

    p_cap = sub.add_parser("capture", help="Capture photo")
    p_cap.add_argument("--output", type=str, help="Output file path")
    p_cap.add_argument("--index", type=int, default=0, help="Camera index")
    p_cap.add_argument("--resolution", type=str, help="Resolution (e.g. 1920x1080)")

    args = parser.parse_args()

    if args.command == "list":
        print(list_cameras())
    elif args.command == "info":
        print(camera_info(args.index))
    elif args.command == "capture":
        print(capture_photo(args.output, args.index, args.resolution))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
