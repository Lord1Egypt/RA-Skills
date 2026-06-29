#!/usr/bin/env python3
"""Compose music from perception data using Zig FM synth.
Reads the latest perception report and generates a WAV/MP3.
"""
import json, subprocess, sys, os
from datetime import datetime

def read_latest_perception():
    """Try multiple perception sources in order."""
    # Source 1: situation_reports.jsonl
    reports = os.path.expanduser("~/.qclaw/workspace/data/situation_reports.jsonl")
    if os.path.exists(reports):
        latest = None
        with open(reports) as f:
            for line in f:
                try: latest = json.loads(line)
                except: pass
        if latest:
            return {
                "brightness": latest.get("brightness", 100),
                "rms": latest.get("rms", 10.0),
                "phase": latest.get("phase", "day"),
            }
    
    # Source 2: sense_all
    sense = os.path.expanduser("~/.local/bin/sense_all")
    if os.path.exists(sense):
        try:
            r = subprocess.run([sense], capture_output=True, text=True, timeout=60)
            d = json.loads(r.stdout)
            p = d.get("perceive", {})
            brightness = p.get("brightness", 100)
            rms = p.get("audio", {}).get("rms", 10.0)
            phase = p.get("phase", "day")
            return {"brightness": brightness, "rms": rms, "phase": phase}
        except: pass
    
    # Fallback: defaults
    hour = datetime.now().hour
    if hour < 5: phase = "night"
    elif hour < 8: phase = "dawn"
    elif hour < 12: phase = "morning"
    elif hour < 17: phase = "afternoon"
    elif hour < 20: phase = "evening"
    elif hour < 22: phase = "dusk"
    else: phase = "night"
    return {"brightness": 100, "rms": 10.0, "phase": phase}

def main():
    p = read_latest_perception()
    date_str = datetime.now().strftime("%Y%m%d_%H%M")
    wav_path = f"/tmp/perception_music_{date_str}.wav"
    mp3_path = f"/tmp/perception_music_{date_str}.mp3"
    
    fm = os.path.expanduser("~/.local/bin/fm_compose")
    if not os.path.exists(fm):
        print("Error: fm_compose not found at ~/.local/bin/fm_compose", file=sys.stderr)
        print("Build from: https://github.com/citriac/perception-music", file=sys.stderr)
        sys.exit(1)
    
    print(f"Composing: brightness={p['brightness']} rms={p['rms']:.1f} phase={p['phase']}", file=sys.stderr)
    result = subprocess.run([
        fm,
        "--brightness", str(p["brightness"]),
        "--rms", str(p["rms"]),
        "--phase", p["phase"],
        "--duration", "90",
        "--output", wav_path,
    ], capture_output=True, text=True, timeout=30)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(result.stderr.strip(), file=sys.stderr)
    
    # Convert to MP3 if ffmpeg available
    ffmpeg = os.path.expanduser("~/.local/bin/ffmpeg")
    if not os.path.exists(ffmpeg):
        ffmpeg = "ffmpeg"
    
    subprocess.run([ffmpeg, "-y", "-i", wav_path, "-codec:a", "libmp3lame", "-b:a", "128k", mp3_path],
                   capture_output=True, timeout=30)
    
    # Save to soundscape directory
    sc_dir = os.path.expanduser("~/.qclaw/workspace/soundscape")
    os.makedirs(sc_dir, exist_ok=True)
    final_path = os.path.join(sc_dir, f"compose_{date_str}.mp3")
    
    # Read WAV back if MP3 failed
    if os.path.exists(mp3_path):
        os.rename(mp3_path, final_path)
    elif os.path.exists(wav_path):
        final_path = wav_path
    
    if os.path.exists(wav_path) and wav_path != final_path:
        os.unlink(wav_path)
    
    print(f"Saved: {final_path}")
    return final_path

if __name__ == "__main__":
    main()
