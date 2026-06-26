#!/bin/bash
# KittenTTS WhatsApp: Generate TTS and convert to WhatsApp-compatible OGG
# Usage: bash tts_walkie.sh "Your text here" [voice]
# Output: /tmp/walkie_reply.ogg

set -e

TEXT="${1:-}"
VOICE="${2:-Bella}"
VOICE_SPEED="${VOICE_SPEED:-1.0}"
TMP_DIR="/tmp/kittentts-walkie"
WAV_PATH="$TMP_DIR/tts_raw.wav"
OGG_PATH="$TMP_DIR/walkie_reply.ogg"

if [ -z "$TEXT" ]; then
    echo "Usage: tts_walkie.sh \"Your text\" [voice]"
    exit 1
fi

# Create private temp dir (mode 700)
mkdir -p "$TMP_DIR"
chmod 700 "$TMP_DIR"

echo "[TTS] Generating: $TEXT"
echo "[TTS] Voice: $VOICE, Speed: $VOICE_SPEED"

python3 << PYEOF
from kittentts import KittenTTS
import numpy as np, soundfile as sf, subprocess, sys, os

text = """$TEXT"""
voice = "$VOICE"
speed = float("$VOICE_SPEED")

tts = KittenTTS("KittenML/kitten-tts-mini-0.8")
audio = tts.generate(text, voice=voice, speed=speed)  # speed now actually used

wav_path = "$WAV_PATH"
ogg_path = "$OGG_PATH"

sf.write(wav_path, audio, 24000)
print(f"[TTS] WAV saved: {os.path.getsize(wav_path)} bytes")

result = subprocess.run([
    "ffmpeg", "-y", "-i", wav_path,
    "-ar", "16000", "-ac", "1",
    "-c:a", "libopus", "-b:a", "128k",
    ogg_path
], capture_output=True, text=True)

if result.returncode != 0:
    print(f"[TTS] FFmpeg error: {result.stderr[-500:]}", file=sys.stderr)
    sys.exit(1)

print(f"[TTS] OGG saved: {os.path.getsize(ogg_path)} bytes -> {ogg_path}")
PYEOF

# Clean up WAV (keep OGG for sending)
rm -f "$WAV_PATH"

echo "[TTS] Done: $OGG_PATH"
