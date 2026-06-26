#!/bin/bash
# Whisper transcription for incoming WhatsApp audio
# Usage: bash transcribe.sh /path/to/audio.ogg [model]
# Model options: tiny, base, small, medium, large (default: base)

set -e

AUDIO_PATH="${1:-}"
MODEL="${2:-base}"

if [ -z "$AUDIO_PATH" ]; then
    echo "Usage: transcribe.sh /path/to/audio.ogg [model]"
    exit 1
fi

if [ ! -f "$AUDIO_PATH" ]; then
    echo "[Transcribe] File not found: $AUDIO_PATH"
    exit 1
fi

echo "[Transcribe] Using model: $MODEL"
echo "[Transcribe] File: $AUDIO_PATH"

python3 << 'PYEOF'
import subprocess, sys, os

audio_path = """$AUDIO_PATH"""
model = """$MODEL"""

# Convert to WAV if needed (WhatsApp sends .ogg opus)
wav_path = "/tmp/whisper_input.wav"
result = subprocess.run([
    "ffmpeg", "-y", "-i", audio_path,
    "-ar", "16000", "-ac", "1",
    wav_path
], capture_output=True, text=True)

if result.returncode != 0:
    print(f"[Transcribe] Audio conversion failed: {result.stderr[-300:]}", file=sys.stderr)
    sys.exit(1)

print(f"[Transcribe] Converted to WAV: {os.path.getsize(wav_path)} bytes")

# Run whisper
result = subprocess.run([
    "whisper", wav_path,
    "--model", model,
    "--language", "en",
    "--fp16", "False",
    "--no-timestamps", "True"
], capture_output=True, text=True)

if result.returncode != 0:
    print(f"[Transcribe] Whisper failed: {result.stderr[-300:]}", file=sys.stderr)
    sys.exit(1)

transcript = result.stdout.strip()
print(transcript)
PYEOF
