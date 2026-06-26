"""
Queue Wan2.2 shots one at a time and collect each output before moving on.

This avoids overlapping renders on UMA/VRAM-constrained hosts and avoids
ComfyUI HTTP polling during generation. It watches the output filesystem only.
"""
import argparse
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path


DEFAULT_OUTPUT = r"\\wsl.localhost\Ubuntu\home\choi_g16\comfy\ComfyUI\output"


def newest_output(output_dir, prefix, after_ts):
    root = Path(output_dir)
    candidates = []
    for current, _, files in os.walk(root):
        cur = Path(current)
        for name in files:
            if not name.startswith(prefix) or not name.lower().endswith(".mp4"):
                continue
            p = cur / name
            try:
                mtime = p.stat().st_mtime
            except OSError:
                continue
            if mtime >= after_ts:
                candidates.append((mtime, p))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][1]


def run(cmd):
    result = subprocess.run(cmd, text=True)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def load_duration_frames(path, fps, min_frames, frame_pad):
    if not path:
        return {}
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if "items" in data:
        data = data["items"]
    out = {}
    for sid, value in data.items():
        if isinstance(value, dict):
            dur = float(value.get("duration_s", 0))
            frames = int(value.get("frames_16fps") or 0)
        else:
            dur = float(value)
            frames = 0
        if frames <= 0:
            frames = int(math.ceil(dur * fps))
        out[sid] = max(min_frames, frames + frame_pad)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--shots", nargs="+", required=True)
    ap.add_argument("--comfy", default="http://127.0.0.1:8192")
    ap.add_argument("--output-dir", default=DEFAULT_OUTPUT)
    ap.add_argument("--fire-script", default=str(Path(__file__).with_name("fire_videos.py")))
    ap.add_argument("--frames", type=int, default=80)
    ap.add_argument("--durations", help="durations.json from plan_subtitle_durations.py; overrides --frames per shot")
    ap.add_argument("--duration-fps", type=float, default=16.0, help="FPS used to convert subtitle duration to Wan frames")
    ap.add_argument("--min-frames", type=int, default=33)
    ap.add_argument("--frame-pad", type=int, default=8, help="Extra native frames so compose can trim cleanly")
    ap.add_argument("--width", type=int, default=832)
    ap.add_argument("--height", type=int, default=480)
    ap.add_argument("--prefix", default="film_video")
    ap.add_argument("--sleep", type=int, default=20)
    ap.add_argument("--timeout-min", type=int, default=60)
    args = ap.parse_args()
    duration_frames = load_duration_frames(args.durations, args.duration_fps, args.min_frames, args.frame_pad)

    for sid in args.shots:
        since = time.time()
        frames = duration_frames.get(sid, args.frames)
        print(f"\n[{sid}] queue")
        run([
            sys.executable, args.fire_script,
            "--project", args.project,
            "--comfy", args.comfy,
            "--shots", sid,
            "--frames", str(frames),
            "--width", str(args.width),
            "--height", str(args.height),
            "--prefix", args.prefix,
        ])

        deadline = time.time() + args.timeout_min * 60
        found = None
        while time.time() < deadline:
            time.sleep(args.sleep)
            found = newest_output(args.output_dir, f"{args.prefix}_{sid}", since)
            if found:
                print(f"[{sid}] found {found}")
                break
        if not found:
            raise TimeoutError(f"{sid}: timed out after {args.timeout_min} min")

        print(f"[{sid}] collect")
        run([
            sys.executable, args.fire_script,
            "--project", args.project,
            "--shots", sid,
            "--collect",
            "--since", f"{since:.0f}",
            "--prefix", args.prefix,
        ])


if __name__ == "__main__":
    main()
