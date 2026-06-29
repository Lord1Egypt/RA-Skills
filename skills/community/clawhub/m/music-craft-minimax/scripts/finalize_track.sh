#!/usr/bin/env bash
set -euo pipefail

overwrite=false
if [ "${1:-}" = "--overwrite" ]; then
  overwrite=true
  shift
fi

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 [--overwrite] input.mp3 output.mp3" >&2
  exit 2
fi

input="$1"
output="$2"

if [ -e "$output" ] && [ "$overwrite" != true ]; then
  echo "Refusing to overwrite existing output: $output (pass --overwrite to replace it)" >&2
  exit 1
fi

if [ "$overwrite" = true ]; then
  ffmpeg -y -i "$input" -af loudnorm=I=-16:TP=-1:LRA=11 -ar 48k "$output"
else
  ffmpeg -n -i "$input" -af loudnorm=I=-16:TP=-1:LRA=11 -ar 48k "$output"
fi
