#!/usr/bin/env python3
"""
Audio Capture 模块 — 跨平台音频捕获
支持 PulseAudio (Linux), WASAPI loopback (Windows via PowerShell), PipeWire
"""

import json
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_DIR / "config.json"


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def list_audio_sources():
    """List all available audio sources."""
    sources = []

    # PulseAudio
    try:
        result = subprocess.run(
            ["pactl", "list", "short", "sources"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                if line.strip():
                    parts = line.split("\t")
                    sources.append({
                        "backend": "pulseaudio",
                        "id": parts[1] if len(parts) > 1 else parts[0],
                        "is_monitor": ".monitor" in line,
                        "raw": line.strip()
                    })
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # PipeWire
    try:
        result = subprocess.run(
            ["pw-record", "--list-targets"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                if line.strip() and not line.startswith("Available"):
                    sources.append({
                        "backend": "pipewire",
                        "id": line.strip(),
                        "is_monitor": "monitor" in line.lower() or "output" in line.lower(),
                        "raw": line.strip()
                    })
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    return sources


def find_best_loopback():
    """Find the best audio source for capturing system output (meeting audio)."""
    sources = list_audio_sources()

    # Prefer monitor sources (they capture what comes out of speakers)
    monitors = [s for s in sources if s["is_monitor"]]
    if monitors:
        return monitors[0]["id"], monitors[0]["backend"]

    if sources:
        return sources[0]["id"], sources[0]["backend"]

    return "default", "pulse"


def record_audio(output_path, duration=None, device=None):
    """
    Record audio to file.

    Args:
        output_path: Path to save WAV file
        duration: Recording duration in seconds (None = until killed)
        device: Audio device/source name (None = auto-detect)
    """
    config = load_config()

    if not device:
        device, backend = find_best_loopback()
    else:
        backend = "pulse"

    sample_rate = config.get("audio", {}).get("sample_rate", 16000)
    channels = config.get("audio", {}).get("channels", 1)

    cmd = [
        "ffmpeg", "-y",
        "-f", "pulse",
        "-i", device,
        "-ac", str(channels),
        "-ar", str(sample_rate),
        "-acodec", "pcm_s16le",
    ]

    if duration:
        cmd.extend(["-t", str(duration)])

    cmd.append(str(output_path))

    print(f"Recording from: {device} ({backend})")
    print(f"Output: {output_path}")
    if duration:
        print(f"Duration: {duration}s")
    else:
        print("Recording until stopped (Ctrl+C)")

    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return proc


def record_window_audio_windows(output_path, duration=None):
    """
    Record audio on Windows using WASAPI loopback via PowerShell.
    This captures the actual system audio output (what you hear in speakers).
    """
    powershell = "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
    config = load_config()
    sample_rate = config.get("audio", {}).get("sample_rate", 16000)

    # Convert WSL path to Windows path
    win_path = subprocess.run(
        ["wslpath", "-w", str(output_path)],
        capture_output=True, text=True
    ).stdout.strip()

    duration_flag = f"-t {duration}" if duration else ""

    cmd = [
        "ffmpeg", "-y",
        "-f", "dshow",
        "-i", "audio=virtual-audio-capturer",  # Requires Virtual Audio Cable or similar
        "-ac", "1",
        "-ar", str(sample_rate),
        "-acodec", "pcm_s16le",
    ]

    if duration:
        cmd.extend(["-t", str(duration)])

    cmd.append(str(output_path))

    print(f"Recording Windows audio via WASAPI")
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return proc


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Audio capture utility")
    parser.add_argument("command", choices=["list", "record", "test"])
    parser.add_argument("--output", "-o", default="test_recording.wav")
    parser.add_argument("--duration", "-d", type=int, help="Duration in seconds")
    parser.add_argument("--device", help="Audio device name")
    args = parser.parse_args()

    if args.command == "list":
        sources = list_audio_sources()
        if not sources:
            print("No audio sources found. Install pulseaudio or pipewire.")
        else:
            print("Available audio sources:")
            for s in sources:
                marker = " ★" if s["is_monitor"] else ""
                print(f"  [{s['backend']}] {s['id']}{marker}")
            print("\n★ = monitor source (captures system output)")

    elif args.command == "record":
        proc = record_audio(args.output, args.duration, args.device)
        try:
            proc.wait()
        except KeyboardInterrupt:
            proc.terminate()
            proc.wait()
        print(f"\nSaved: {args.output}")

    elif args.command == "test":
        print("Recording 5-second test clip...")
        proc = record_audio(args.output, duration=5, device=args.device)
        proc.wait()
        if Path(args.output).exists():
            size = Path(args.output).stat().st_size
            print(f"Test recording saved: {args.output} ({size} bytes)")
            if size < 1000:
                print("WARNING: File is very small, audio capture may not be working")
        else:
            print("ERROR: Test recording failed")
