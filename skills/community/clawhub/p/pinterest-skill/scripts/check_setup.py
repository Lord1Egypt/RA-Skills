#!/usr/bin/env python3
"""Check what this machine can do before making Pinterest pins, and say how to fix what's missing.

    python3 scripts/check_setup.py

Required: Python 3.9+ and Pillow (pins, checks, previews). ffmpeg only for video pins. On Windows, tzdata for scheduling in your time zone.
"""
import importlib.util, os, platform, re, shutil, subprocess, sys

system = platform.system()
INSTALL_FFMPEG = {"Darwin": "brew install ffmpeg", "Windows": "winget install ffmpeg",
                  "Linux": "sudo apt install ffmpeg   (or your distro's package manager)"}.get(system, "install ffmpeg")
PIP = "py -m pip" if system == "Windows" else "python3 -m pip"
try:   # Homebrew Python and recent Debian/Ubuntu refuse plain pip installs (PEP 668)
    import sysconfig
    if os.path.exists(os.path.join(sysconfig.get_paths()["stdlib"], "EXTERNALLY-MANAGED")):
        PIP = ("python3 -m venv ~/.pinterest-skill-venv && ~/.pinterest-skill-venv/bin/python3 -m pip"
               "  (then run the scripts with ~/.pinterest-skill-venv/bin/python3)")
except Exception:
    pass
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
        line("ok", "Pillow", f"{PIL.__version__}: pins, checks, previews")
else:
    ok = False
    line("missing", "Pillow", f"{PIP} install pillow")

if shutil.which("ffmpeg") and shutil.which("ffprobe"):
    v = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.split("\n")[0]
    enc = subprocess.run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    filt = subprocess.run(["ffmpeg", "-hide_banner", "-filters"], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    if "libx264" not in enc:
        line("limited", "ffmpeg", "this build has no libx264 (H.264): install a full ffmpeg for video pins: " + INSTALL_FFMPEG)
    elif " xfade " not in filt:
        line("old", "ffmpeg", "older than 4.3: video.py stills needs --fade 0; update for crossfades: " + INSTALL_FFMPEG)
    else:
        line("ok", "ffmpeg", v.replace("ffmpeg version ", "")[:60])
else:
    line("needed for video", "ffmpeg", f"{INSTALL_FFMPEG}  (image pins work without it)")

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

fonts = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts")
if os.path.exists(os.path.join(fonts, "Inter.ttf")):
    line("ok", "Fonts", "bundled (Inter, Instrument Serif)")
else:
    line("note", "Fonts", "not bundled in this copy; downloaded once on first render")

py = "py" if system == "Windows" else "python3"
here = os.path.dirname(os.path.abspath(__file__))
print(f"\nReady. From your own project folder (not this skill's), run: {py} {os.path.join(here, '<name>.py')} ..."
      if ok else "\nInstall the missing items above, then run this again.")
sys.exit(0 if ok else 1)
