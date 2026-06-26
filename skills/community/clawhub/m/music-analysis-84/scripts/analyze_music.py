#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from music_analysis_v2 import analyze_track, to_native


def ffprobe_meta(path: Path):
    cmd = [
        "ffprobe", "-v", "error", "-show_streams", "-show_format",
        "-print_format", "json", str(path)
    ]
    out = subprocess.check_output(cmd, text=True)
    j = json.loads(out)
    astream = next((s for s in j.get("streams", []) if s.get("codec_type") == "audio"), {})
    return {
        "duration_sec": float(j.get("format", {}).get("duration", 0) or 0),
        "sample_rate": int(astream.get("sample_rate", 0) or 0),
        "channels": int(astream.get("channels", 0) or 0),
        "codec": astream.get("codec_name"),
    }


def analyze_with_librosa(path: Path):
    return analyze_track(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out")
    args = ap.parse_args()

    p = Path(args.audio).expanduser()
    if not p.exists():
        raise SystemExit(f"audio not found: {p}")

    report = {"file": str(p), "meta": ffprobe_meta(p)}

    try:
        report["music"] = analyze_with_librosa(p)
        report["engine"] = "librosa-v2"
    except Exception as e:
        report["engine"] = "ffprobe-only"
        report["music"] = {
            "error": f"librosa analysis unavailable: {e}",
            "hint": "Create local venv and install librosa+numpy for full analysis."
        }

    out_text = json.dumps(to_native(report), indent=2)
    if args.out:
        Path(args.out).write_text(out_text)
    if args.json or not args.out:
        print(out_text)


if __name__ == "__main__":
    main()
