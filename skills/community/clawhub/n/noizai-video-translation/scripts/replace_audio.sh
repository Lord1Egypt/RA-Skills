#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: replace_audio.sh --video <video_file> --audio <audio_file> --output <output_file> [--srt <srt_file>]

Options:
  --video    Original video file path
  --audio    New audio file path (WAV/MP3)
  --output   Final output video file path
  --srt      Original or translated SRT file (optional). If provided, keeps original audio where there are no subtitles.
EOF
  exit "${1:-0}"
}

VIDEO=""
AUDIO=""
OUTPUT=""
SRT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --video)  VIDEO="$2"; shift 2 ;;
    --audio)  AUDIO="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    --srt)    SRT="$2"; shift 2 ;;
    -h|--help) usage 0 ;;
    *) echo "Unknown option: $1"; usage 1 ;;
  esac
done

if [[ -z "$VIDEO" || -z "$AUDIO" || -z "$OUTPUT" ]]; then
  echo "Error: --video, --audio, and --output are all required." >&2
  usage 1
fi

if [[ ! -f "$VIDEO" ]]; then
  echo "Error: Video file not found: $VIDEO" >&2
  exit 1
fi

if [[ ! -f "$AUDIO" ]]; then
  echo "Error: Audio file not found: $AUDIO" >&2
  exit 1
fi

# Use ffmpeg to replace or mix the audio track
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -n "$SRT" && -f "$SRT" ]]; then
  echo "Mixing original audio with dubbed audio using SRT timestamps -> $OUTPUT"
  CMD_FILE="$(mktemp /tmp/duck_cmd.XXXXXX.txt)"
  
  # Generate asendcmd volume ducking file
  python3 "$SCRIPT_DIR/srt_to_duck.py" "$SRT" "$CMD_FILE"
  
  # [0:a] is original audio, [1:a] is dubbed audio
  # We duck the original audio where subtitles exist, then mix it with the dubbed audio.
  ffmpeg -y -i "$VIDEO" -i "$AUDIO" \
    -filter_complex "[0:a]asendcmd=f='${CMD_FILE}',volume=1.0[orig_ducked];[orig_ducked][1:a]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[aout]" \
    -map 0:v:0 -map "[aout]" \
    -c:v copy -c:a aac -b:a 192k \
    -shortest \
    "$OUTPUT"
    
  rm -f "$CMD_FILE"
else
  echo "Replacing audio in $VIDEO with $AUDIO -> $OUTPUT"
  ffmpeg -y -i "$VIDEO" -i "$AUDIO" \
    -map 0:v:0 -map 1:a:0 \
    -c:v copy -c:a aac -b:a 192k \
    -shortest \
    "$OUTPUT"
fi

echo "Done! Output saved to $OUTPUT"
