#!/usr/bin/env python3
"""Clip highlight audio segments with ffmpeg.

Input: highlights.json (same schema produced by the workflow)
- expects: highlights[].id, highlights[].start, highlights[].end
Output: writes mp3 clips into out_dir/audio/{id}.mp3
Also updates highlights[].clip.file to relative path audio/{id}.mp3

Usage:
  python scripts/clip_audio.py --audio episode.mp3 --highlights highlights.json --out-dir site_assets
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def run(cmd: list[str]) -> None:
    subprocess.check_call(cmd)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True, help="Path to full episode audio file (mp3)")
    ap.add_argument("--highlights", required=True, help="Path to highlights.json")
    ap.add_argument("--out-dir", required=True, help="Output directory")
    ap.add_argument("--pad-before", type=float, default=2.0)
    ap.add_argument("--pad-after", type=float, default=2.0)
    ap.add_argument("--q", type=int, default=4, help="libmp3lame VBR quality (0 best, 9 worst)")
    args = ap.parse_args()

    audio = Path(args.audio)
    highlights_path = Path(args.highlights)
    out_dir = Path(args.out_dir)
    out_audio_dir = out_dir / "audio"
    out_audio_dir.mkdir(parents=True, exist_ok=True)

    data = json.loads(highlights_path.read_text("utf-8"))

    for h in data.get("highlights", []):
        hid = h["id"]
        start = max(0.0, float(h["start"]) - args.pad_before)
        end = float(h["end"]) + args.pad_after
        dur = max(0.1, end - start)
        out = out_audio_dir / f"{hid}.mp3"

        cmd = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            f"{start:.3f}",
            "-i",
            str(audio),
            "-t",
            f"{dur:.3f}",
            "-c:a",
            "libmp3lame",
            "-q:a",
            str(args.q),
            str(out),
        ]
        run(cmd)

        h.setdefault("clip", {})
        h["clip"]["file"] = f"audio/{hid}.mp3"
        h["clip"]["start"] = start
        h["clip"]["end"] = end

    highlights_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")


if __name__ == "__main__":
    main()
