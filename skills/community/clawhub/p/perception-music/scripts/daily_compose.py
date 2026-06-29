#!/usr/bin/env python3
"""Daily composition from perception data using Zig FM synth."""
import json, subprocess, sys, os
from datetime import datetime

def main():
    # Read latest perception data
    reports_path = os.path.expanduser("~/.qclaw/workspace/data/situation_reports.jsonl")
    if not os.path.exists(reports_path):
        print("No reports file", file=sys.stderr)
        return
    
    # Get latest report
    latest = None
    with open(reports_path) as f:
        for line in f:
            try:
                latest = json.loads(line)
            except:
                pass
    
    if not latest:
        print("No reports", file=sys.stderr)
        return
    
    brightness = latest.get("brightness", 100)
    rms = latest.get("rms", 10.0)
    
    # Determine phase from hour
    hour = datetime.now().hour
    if hour < 5: phase = "night"
    elif hour < 8: phase = "dawn"
    elif hour < 12: phase = "morning"
    elif hour < 17: phase = "afternoon"
    elif hour < 20: phase = "evening"
    elif hour < 22: phase = "dusk"
    else: phase = "night"
    
    # Output path
    date_str = datetime.now().strftime("%Y%m%d_%H%M")
    wav_path = f"/tmp/compose_{date_str}.wav"
    mp3_path = f"/tmp/compose_{date_str}.mp3"
    
    # Run Zig FM composer
    print(f"Composing: brightness={brightness} rms={rms:.1f} phase={phase}", file=sys.stderr)
    result = subprocess.run([
        os.path.expanduser("~/.local/bin/fm_compose"),
        "--brightness", str(brightness),
        "--rms", str(rms),
        "--phase", phase,
        "--duration", "90",
        "--output", wav_path,
    ], capture_output=True, text=True, timeout=30)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return
    
    print(result.stderr.strip(), file=sys.stderr)
    
    # Convert to MP3
    ffmpeg = os.path.expanduser("~/.local/bin/ffmpeg")
    subprocess.run([ffmpeg, "-y", "-i", wav_path, "-codec:a", "libmp3lame", "-b:a", "128k", mp3_path],
                   capture_output=True, timeout=30)
    
    # Save to soundscape directory
    sc_dir = os.path.expanduser("~/.qclaw/workspace/soundscape")
    os.makedirs(sc_dir, exist_ok=True)
    final_path = os.path.join(sc_dir, f"compose_{date_str}.mp3")
    os.rename(mp3_path, final_path)
    
    # Clean up WAV
    os.unlink(wav_path)
    
    print(f"Saved: {final_path}")
    return final_path

if __name__ == "__main__":
    main()
