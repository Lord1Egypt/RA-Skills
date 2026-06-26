#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: bash scripts/postprocess_audio.sh <input-audio> [output-audio]"
  echo "Example: bash scripts/postprocess_audio.sh test-output/a.m4a test-output/a-enhanced.m4a"
  exit 1
fi

IN="$1"
OUT="${2:-$1}"

if [[ ! -f "$IN" ]]; then
  echo "Error: input file not found: $IN" >&2
  exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "Error: ffmpeg not found." >&2
  echo "Install hint: brew install ffmpeg (macOS) / sudo apt-get install -y ffmpeg (Linux)" >&2
  exit 2
fi

EXT="${OUT##*.}"
EXT="$(echo "$EXT" | tr '[:upper:]' '[:lower:]')"
FILTER="highpass=f=70,lowpass=f=13500,compand=attacks=0.02:decays=0.20:points=-80/-80|-35/-22|-20/-12|0/-6,loudnorm=I=-16:TP=-1.5:LRA=11"

encode_args=()
case "$EXT" in
  m4a|mp4|aac)
    encode_args=(-c:a aac -b:a 128k)
    ;;
  mp3)
    encode_args=(-c:a libmp3lame -b:a 128k)
    ;;
  wav)
    encode_args=(-c:a pcm_s16le)
    ;;
  *)
    encode_args=(-c:a aac -b:a 128k)
    ;;
esac

if [[ "$IN" == "$OUT" ]]; then
  TMP="$(dirname "$OUT")/.$(basename "${OUT%.*}")-tmp.$EXT"
  ffmpeg -y -i "$IN" -af "$FILTER" "${encode_args[@]}" "$TMP" >/dev/null 2>&1
  mv "$TMP" "$OUT"
else
  ffmpeg -y -i "$IN" -af "$FILTER" "${encode_args[@]}" "$OUT" >/dev/null 2>&1
fi

echo "postprocessed=$OUT"
