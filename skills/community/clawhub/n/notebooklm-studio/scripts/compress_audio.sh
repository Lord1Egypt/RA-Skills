#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   compress_audio.sh <input_audio> <output_mp3>
# Example:
#   compress_audio.sh input.wav output.mp3

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg not found" >&2
  exit 127
fi

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <input_audio> <output_mp3>" >&2
  exit 2
fi

INPUT="$1"
OUTPUT="$2"

# Pass 1: speech-optimized compression
ffmpeg -y -i "$INPUT" \
  -vn -ac 1 -ar 24000 -b:a 64k \
  -c:a libmp3lame \
  "$OUTPUT"

# Optional pass 2: if file still large, downscale further.
# Default threshold: 45MB (safe for most Telegram bot/file workflows)
MAX_BYTES=$((45 * 1024 * 1024))
SIZE=$(wc -c < "$OUTPUT" | tr -d ' ')

if [ "$SIZE" -gt "$MAX_BYTES" ]; then
  TMP="${OUTPUT%.mp3}.fallback.mp3"
  ffmpeg -y -i "$INPUT" \
    -vn -ac 1 -ar 22050 -b:a 48k \
    -c:a libmp3lame \
    "$TMP"
  mv "$TMP" "$OUTPUT"
fi

echo "$OUTPUT"
