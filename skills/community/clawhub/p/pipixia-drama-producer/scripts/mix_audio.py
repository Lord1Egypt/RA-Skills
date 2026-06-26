#!/usr/bin/env python3
"""
mix_audio.py - Mix TTS dialogue lines + BGM into a dubbed audio track
Usage: python3 mix_audio.py --video video.mp4 --bgm bgm.mp3 --output dubbed.mp4
       --lines "0.5:line1.mp3" "5.0:line2.mp3" ...

Each line is formatted as "start_seconds:audio_file_path"
"""

import argparse
import subprocess
import sys
import os

FFMPEG = os.environ.get("FFMPEG", "ffmpeg")
FFPROBE = os.environ.get("FFPROBE", "ffprobe")

def get_duration(f):
    r = subprocess.run([FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
                        "-of", "csv=p=0", f], capture_output=True, text=True)
    return float(r.stdout.strip())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--bgm", default=None)
    parser.add_argument("--bgm-volume", type=float, default=0.25)
    parser.add_argument("--voice-volume", type=float, default=1.5)
    parser.add_argument("--output", required=True)
    parser.add_argument("--lines", nargs="*", default=[])
    args = parser.parse_args()

    total = get_duration(args.video)
    print(f"Video duration: {total:.2f}s")

    # Parse lines
    parsed = []
    for l in args.lines:
        t, path = l.split(":", 1)
        parsed.append((float(t), path))
        print(f"  Line @{t}s: {path} ({get_duration(path):.2f}s)")

    # Build inputs
    inputs = ["-i", args.video,
              "-f", "lavfi", "-i", f"anullsrc=channel_layout=stereo:sample_rate=44100"]
    idx = 2
    for t, path in parsed:
        inputs += ["-i", path]
    
    if args.bgm:
        bgm_idx = idx + len(parsed)
        inputs += ["-i", args.bgm]

    # Build filter
    filters = [f"[1:a]atrim=duration={total}[base]"]
    for i, (t, path) in enumerate(parsed):
        ms = int(t * 1000)
        filters.append(f"[{i+2}:a]adelay={ms}|{ms}[d{i}]")

    n_mix = len(parsed) + 1
    mix_in = "[base]" + "".join(f"[d{i}]" for i in range(len(parsed)))

    if args.bgm:
        filters.append(f"[{bgm_idx}:a]aloop=loop=-1:size=2000000000,atrim=duration={total},"
                       f"asetpts=PTS-STARTPTS,volume={args.bgm_volume}[bgm]")
        mix_in += "[bgm]"
        n_mix += 1

    filters.append(f"{mix_in}amix=inputs={n_mix}:normalize=0,volume={args.voice_volume}[audio_out]")

    cmd = [FFMPEG, "-y", "-hide_banner"] + inputs + [
        "-filter_complex", ";".join(filters),
        "-map", "0:v", "-map", "[audio_out]",
        "-c:v", "copy", "-c:a", "aac", "-ar", "44100", "-ac", "2",
        "-shortest", args.output
    ]

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0:
        print(f"✓ Output: {args.output}")
    else:
        print("✗ Error:", r.stderr[-500:])
        sys.exit(1)

if __name__ == "__main__":
    main()
