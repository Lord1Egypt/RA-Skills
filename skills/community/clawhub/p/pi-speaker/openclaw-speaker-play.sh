#!/usr/bin/env bash
# Play an audio file on the default output (e.g. Pi Bluetooth speaker).
# Usage: openclaw-speaker-play.sh <path-to-audio-file>
# Use with PulseAudio (paplay) or PipeWire (pw-play). Copy to the Pi, e.g. ~/bin/.

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <path-to-audio-file>" >&2
  exit 1
fi

path="$1"
if [[ ! -f "$path" ]]; then
  echo "Not a file: $path" >&2
  exit 1
fi

if command -v paplay >/dev/null 2>&1; then
  nohup paplay "$path" >/dev/null 2>&1 &
elif command -v pw-play >/dev/null 2>&1; then
  nohup pw-play "$path" >/dev/null 2>&1 &
else
  echo "No paplay or pw-play found. Install pulseaudio or pipewire." >&2
  exit 1
fi
exit 0
