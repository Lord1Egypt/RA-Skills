#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"


def run(cmd):
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or f"command failed: {' '.join(cmd)}")
    return proc


def main():
    parser = argparse.ArgumentParser(description="Build a Feishu-compatible Ogg/Opus voice file from text.")
    parser.add_argument("--text", required=True, help="Text to synthesize")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help=f"Edge TTS voice (default: {DEFAULT_VOICE})")
    parser.add_argument("--out-dir", help="Output directory; defaults to a temp dir")
    parser.add_argument("--basename", default="voice-reply", help="Base filename without extension")
    args = parser.parse_args()

    text = (args.text or "").strip()
    if not text:
        raise SystemExit("--text is required")

    edge_tts = shutil.which("edge-tts")
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if not edge_tts:
        raise SystemExit("edge-tts not found in PATH")
    if not ffmpeg:
        raise SystemExit("ffmpeg not found in PATH")

    out_dir = Path(args.out_dir) if args.out_dir else Path(tempfile.mkdtemp(prefix="feishu-voice-"))
    out_dir.mkdir(parents=True, exist_ok=True)
    base = "".join(c if c.isalnum() or c in {"-", "_"} else "-" for c in args.basename).strip("-") or "voice-reply"
    mp3_path = out_dir / f"{base}.mp3"
    ogg_path = out_dir / f"{base}.ogg"

    run([edge_tts, "--voice", args.voice, "--text", text, "--write-media", str(mp3_path)])
    if not mp3_path.exists() or mp3_path.stat().st_size == 0:
        raise RuntimeError("edge-tts produced an empty mp3 file")

    run([
        ffmpeg,
        "-y",
        "-i", str(mp3_path),
        "-c:a", "libopus",
        "-ar", "48000",
        "-ac", "1",
        "-b:a", "32k",
        str(ogg_path),
    ])
    if not ogg_path.exists() or ogg_path.stat().st_size == 0:
        raise RuntimeError("ffmpeg produced an empty ogg file")

    duration_sec = None
    if ffprobe:
        try:
            probe = run([
                ffprobe,
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(ogg_path),
            ])
            duration_sec = round(float((probe.stdout or "").strip()), 2)
        except Exception:
            duration_sec = None

    result = {
        "text": text,
        "voice": args.voice,
        "output_dir": str(out_dir),
        "mp3_path": str(mp3_path),
        "ogg_path": str(ogg_path),
        "duration_sec": duration_sec,
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
