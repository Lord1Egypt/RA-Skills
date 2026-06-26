#!/usr/bin/env bash
set -euo pipefail
# pad.sh: Add padding / extend canvas around image
# Usage: pad.sh <input> <WxH> [output] [--color COL] [--gravity POS]

usage() {
  cat <<EOF
Usage: $(basename "$0") <input> <WxH> [output] [options]
Options:
  --color COL     Padding color (default: white, "none" for transparent)
  --gravity POS   Image placement (default: center)
Examples:
  pad.sh photo.jpg 1920x1080                              # white padding
  pad.sh icon.png 512x512 padded.png --color none         # transparent
  pad.sh photo.jpg 1920x1080 out.jpg --gravity northwest  # pad right/bottom
EOF
  exit 2
}

[ $# -lt 2 ] && usage
input="$1"; geometry="$2"; shift 2
output=""; color="white"; gravity="center"
while [ $# -gt 0 ]; do
  case "$1" in
    --color) color="$2"; shift 2 ;; --gravity) gravity="$2"; shift 2 ;;
    *) if [ -z "$output" ]; then output="$1"; shift; else echo "Unknown: $1" >&2; exit 1; fi ;;
  esac
done
[ ! -f "$input" ] && echo "ERROR: file not found: $input" >&2 && exit 1
if [ -z "$output" ]; then
  dir="$(dirname "$input")"; base="$(basename "$input")"
  ext="${base##*.}"; name="${base%.*}"
  output="${dir}/${name}-padded.${ext}"
fi
mkdir -p "$(dirname "$output")"
echo "Padding: $input -> $output (canvas: $geometry, color: $color, gravity: $gravity)"
convert "$input" -gravity "$gravity" -background "$color" -extent "$geometry" "$output"
echo "Done: $output ($(identify -format '%wx%h' "$output"))"
