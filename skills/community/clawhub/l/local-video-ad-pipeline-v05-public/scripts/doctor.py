"""
Environment checks for the local video ad pipeline.

This is intentionally read-only. It verifies the tools, ports, folders, and
ComfyUI object registry that the other scripts expect.
"""
import argparse
import json
import shutil
import sys
import urllib.request
from pathlib import Path


DEFAULT_INPUT = r"\\wsl.localhost\Ubuntu\home\choi_g16\comfy\ComfyUI\input"
DEFAULT_OUTPUT = r"\\wsl.localhost\Ubuntu\home\choi_g16\comfy\ComfyUI\output"
REQUIRED_NODES = {
    "UNETLoader",
    "LoraLoaderModelOnly",
    "ModelSamplingSD3",
    "VAELoader",
    "CLIPLoader",
    "CLIPTextEncode",
    "LoadImage",
    "WanImageToVideo",
    "KSamplerAdvanced",
    "VAEDecode",
    "VHS_VideoCombine",
}


def fetch_json(url, timeout=8):
    with urllib.request.urlopen(url, timeout=timeout) as res:
        return json.loads(res.read())


def check(name, ok, detail=""):
    status = "OK" if ok else "FAIL"
    print(f"[{status}] {name}{': ' + detail if detail else ''}")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--comfy", default="http://127.0.0.1:8192")
    ap.add_argument("--ace", default="http://127.0.0.1:7860")
    ap.add_argument("--input-dir", default=DEFAULT_INPUT)
    ap.add_argument("--output-dir", default=DEFAULT_OUTPUT)
    ap.add_argument("--project")
    ap.add_argument("--silent", "--no-bgm", action="store_true",
                    help="Skip ACE-Step as an expected condition for silent/no-BGM videos.")
    args = ap.parse_args()

    ok = True
    ok &= check("python", sys.version_info >= (3, 10), sys.version.split()[0])
    ok &= check("ffmpeg", shutil.which("ffmpeg") is not None, shutil.which("ffmpeg") or "not found")
    ok &= check("ffprobe", shutil.which("ffprobe") is not None, shutil.which("ffprobe") or "not found")

    for label, raw in [("ComfyUI input", args.input_dir), ("ComfyUI output", args.output_dir)]:
        p = Path(raw)
        ok &= check(label, p.exists(), str(p))

    try:
        stats = fetch_json(f"{args.comfy}/system_stats")
        ok &= check("ComfyUI server", True, args.comfy)
        devices = stats.get("devices") or []
        if devices:
            print(f"       device: {devices[0].get('name', 'unknown')}")
    except Exception as e:
        ok &= check("ComfyUI server", False, f"{args.comfy} ({e})")

    try:
        objects = fetch_json(f"{args.comfy}/object_info", timeout=15)
        missing = sorted(REQUIRED_NODES - set(objects))
        ok &= check("ComfyUI required nodes", not missing, ", ".join(missing) if missing else "all present")
    except Exception as e:
        ok &= check("ComfyUI object_info", False, str(e))

    if args.silent:
        check("ACE-Step server", True, "skipped for silent/no-BGM run")
    else:
        try:
            fetch_json(f"{args.ace}/config")
            check("ACE-Step server", True, args.ace)
        except Exception as e:
            check("ACE-Step server", False, f"{args.ace} ({e})")

    if args.project:
        project = Path(args.project)
        ok &= check("project dir", project.exists(), str(project))
        ok &= check("shotlist", (project / "shotlist" / "shotlist.json").exists())
        ok &= check("keyframes dir", (project / "keyframes").exists())

    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
