#!/usr/bin/env bash
set -euo pipefail
# crop.sh: Crop images using ImageMagick
# Usage: crop.sh <input> <geometry> [output]

usage() {
  cat <<EOF
Usage: $(basename "$0") <input> <geometry> [output]
Geometry format: WxH+X+Y
Examples:
  crop.sh photo.jpg 500x500+100+50              # crop 500x500 at offset (100,50)
  crop.sh photo.jpg 1920x1080+0+0               # crop from top-left
  crop.sh photo.jpg 500x500+center              # center crop (special mode)
EOF
  exit 2
}

[ $# -lt 2 ] && usage
input="$1"; geometry="$2"; output="${3:-}"
[ ! -f "$input" ] && echo "ERROR: file not found: $input" >&2 && exit 1

if [ -z "$output" ]; then
  dir="$(dirname "$input")"; base="$(basename "$input")"
  ext="${base##*.}"; name="${base%.*}"
  output="${dir}/${name}-cropped.${ext}"
fi

mkdir -p "$(dirname "$output")"

if [[ "$geometry" == *"+center" ]]; then
  dims="${geometry%+center}"
  echo "Center-cropping: $input -> $output ($dims from center)"
  convert "$input" -gravity center -crop "$dims+0+0" +repage "$output"
else
  echo "Cropping: $input -> $output (geometry: $geometry)"
  convert "$input" -crop "$geometry" +repage "$output"
fi

echo "Done: $output ($(identify -format '%wx%h' "$output"))"
