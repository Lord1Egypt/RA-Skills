#!/usr/bin/env python3
"""Check what this machine can do before making Instagram posts, and say how to fix what's missing.

    python3 scripts/check_setup.py

Required: Python 3.9+ and Pillow (slides, checks, previews). ffmpeg for Reels, Stories with video
and video carousel items. On Windows, tzdata for scheduling in your time zone.
"""
import importlib.util, os, platform, re, shutil, subprocess, sys

system = platform.system()
INSTALL_FFMPEG = {"Darwin": "brew install ffmpeg", "Windows": "winget install ffmpeg",
                  "Linux": "sudo apt install ffmpeg   (or your distro's package manager)"}.get(system, "install ffmpeg")
PIP = "py -m pip" if system == "Windows" else "python3 -m pip"
ok = True


def line(status, name, detail):
    print(f"[{status}] {name}: {detail}")


if sys.version_info < (3, 9):
    ok = False
    line("missing", "Python", f"{platform.python_version()}; needs 3.9 or newer")
else:
    line("ok", "Python", platform.python_version())

if importlib.util.find_spec("PIL"):
    import PIL
    ver = tuple(int(x) for x in re.findall(r"\d+", PIL.__version__)[:2])
    if ver < (9, 1):
        ok = False
        line("old", "Pillow", f"{PIL.__version__}; needs 9.1 or newer: {PIP} install --upgrade pillow")
    else:
        line("ok", "Pillow", f"{PIL.__version__}: slides, image checks, previews")
else:
    ok = False
    line("missing", "Pillow", f"{PIP} install pillow")

if shutil.which("ffmpeg") and shutil.which("ffprobe"):
    v = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True).stdout.split("\n")[0]
    line("ok", "ffmpeg", v.replace("ffmpeg version ", "")[:60])
else:
    line("needed for video", "ffmpeg", f"{INSTALL_FFMPEG}  (photos and carousels work without it)")

try:
    from zoneinfo import ZoneInfo
    ZoneInfo("Europe/Amsterdam")
    line("ok", "Time zones", "scheduling in local time works")
except Exception:
    ok = False
    line("missing", "Time zones", f"{PIP} install tzdata")

if importlib.util.find_spec("pillow_heif"):
    line("ok", "HEIC photos", "iPhone photos can be converted")
else:
    line("optional", "HEIC photos", f"{PIP} install pillow-heif  (only to convert iPhone .heic photos)")

if importlib.util.find_spec("cv2"):
    line("ok", "OpenCV", "warns when slide text sits on a face")
else:
    line("optional", "OpenCV", f"{PIP} install opencv-python-headless  (warns when slide text covers a face)")

fonts = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts")
if os.path.exists(os.path.join(fonts, "Inter.ttf")):
    line("ok", "Fonts", "bundled (Inter, Instrument Serif)")
else:
    line("note", "Fonts", "not bundled in this copy; downloaded once on first render")

py = "py" if system == "Windows" else "python3"
print(f"\nReady. Run the scripts with: {py} scripts/<name>.py ..." if ok else "\nInstall the missing items above, then run this again.")
sys.exit(0 if ok else 1)
