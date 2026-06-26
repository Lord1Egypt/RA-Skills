#!/usr/bin/env bash
set -euo pipefail
# resize.sh: Resize images using ImageMagick
# Usage: resize.sh <input> <geometry> [output]

usage() {
  cat <<EOF
Usage: $(basename "$0") <input> <geometry> [output]
Examples:
  resize.sh photo.jpg 800x                    # width 800, keep aspect
  resize.sh photo.jpg 800x600                 # exact 800x600
  resize.sh photo.jpg 50%                     # half size
  resize.sh photo.jpg 800x800\>               # shrink only if larger
  resize.sh photo.jpg 800x600! output.jpg     # force exact (ignore aspect)
EOF
  exit 2
}

[ $# -lt 2 ] && usage
input="$1"; geometry="$2"; output="${3:-}"
[ ! -f "$input" ] && echo "ERROR: file not found: $input" >&2 && exit 1

if [ -z "$output" ]; then
  dir="$(dirname "$input")"; base="$(basename "$input")"
  ext="${base##*.}"; name="${base%.*}"
  output="${dir}/${name}-resized.${ext}"
fi

mkdir -p "$(dirname "$output")"
echo "Resizing: $input -> $output (geometry: $geometry)"
convert "$input" -resize "$geometry" "$output"
echo "Done: $output ($(identify -format '%wx%h' "$output"))"
