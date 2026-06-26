#!/usr/bin/env python3
"""
Music Composer — mmx music generation tool
Usage:
  python3 generate_music.py instrumental <prompt> [output_name]
  python3 generate_music.py song <prompt> <lyrics_file> <vocal_style> [output_name]
  python3 generate_music.py cover <audio_file> <style_prompt> [output_name]
"""

import subprocess
import sys
import os
import json
from pathlib import Path

DEFAULT_OUT_DIR = Path.home() / "video"

def run(cmd):
    print(f"\n🎵 Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        print(f"❌ Command failed with code {result.returncode}", file=sys.stderr)
    return result

def check_quota():
    print("📊 Checking mmx quota...")
    r = subprocess.run(["mmx", "quota"], capture_output=True, text=True)
    print(r.stdout or r.stderr)

def generate_instrumental(prompt, out_name=None):
    if not out_name:
        out_name = f"instrumental_{pd.ts()}.mp3"
    out_path = DEFAULT_OUT_DIR / out_name
    cmd = [
        "mmx", "music", "generate",
        "--model", "music-2.6",
        "--prompt", prompt,
        "--instrumental",
        "--out", str(out_path)
    ]
    r = run(cmd)
    if r.returncode == 0:
        print(f"✅ Saved: {out_path}")
    return r

def generate_song(prompt, lyrics_path, vocal_style, out_name=None):
    if not out_name:
        out_name = f"song_{pd.ts()}.mp3"
    out_path = DEFAULT_OUT_DIR / out_name
    lyrics = Path(lyrics_path).read_text(encoding="utf-8")
    full_prompt = f"{prompt} | vocal: {vocal_style}"
    cmd = [
        "mmx", "music", "generate",
        "--model", "music-2.6",
        "--prompt", full_prompt,
        "--lyrics", lyrics,
        "--out", str(out_path)
    ]
    r = run(cmd)
    if r.returncode == 0:
        print(f"✅ Saved: {out_path}")
    return r

def generate_cover(audio_file, style_prompt, out_name=None):
    if not out_name:
        fname = Path(audio_file).stem
        out_name = f"cover_{fname}.mp3"
    out_path = DEFAULT_OUT_DIR / out_name
    cmd = [
        "mmx", "music", "cover",
        "--prompt", style_prompt,
        "--audio-file", audio_file,
        "--out", str(out_path)
    ]
    r = run(cmd)
    if r.returncode == 0:
        print(f"✅ Saved: {out_path}")
    return r

class pd:
    import time
    @staticmethod
    def ts():
        return pd.time.strftime("%Y%m%d_%H%M%S")

if __name__ == "__main__":
    check_quota()
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    mode = sys.argv[1]
    if mode == "instrumental":
        if len(sys.argv) < 3:
            print("Usage: generate_music.py instrumental <prompt> [output_name]")
            sys.exit(1)
        generate_instrumental(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    elif mode == "song":
        if len(sys.argv) < 5:
            print("Usage: generate_music.py song <prompt> <lyrics_file> <vocal_style> [output_name]")
            sys.exit(1)
        generate_song(sys.argv[2], sys.argv[3], sys.argv[4],
                      sys.argv[5] if len(sys.argv) > 5 else None)
    elif mode == "cover":
        if len(sys.argv) < 4:
            print("Usage: generate_music.py cover <audio_file> <style_prompt> [output_name]")
            sys.exit(1)
        generate_cover(sys.argv[2], sys.argv[3],
                       sys.argv[4] if len(sys.argv) > 4 else None)
    else:
        print(f"Unknown mode: {mode}")
        print(__doc__)
        sys.exit(1)
