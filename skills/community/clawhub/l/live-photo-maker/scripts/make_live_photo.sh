#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <input-video> <base-output-path-without-extension>" >&2
  exit 1
fi

IN="$1"
BASE="$2"
DIR="$(dirname "$BASE")"
NAME="$(basename "$BASE")"
mkdir -p "$DIR"

UP_MP4="${BASE}.mp4"
JPG="${BASE}.jpg"
PVT="${BASE}.pvt"
ZIP="${BASE}.zip"

ffmpeg -y -i "$IN" -vf "scale=1180:2082:flags=lanczos" -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p "$UP_MP4"
ffmpeg -y -i "$UP_MP4" -frames:v 1 -q:v 1 -update 1 "$JPG"
rm -rf "$PVT"
makelive -p -m "$JPG" "$UP_MP4"
ditto -c -k --sequesterRsrc --keepParent "$PVT" "$ZIP"

echo "PVT: $PVT"
echo "ZIP: $ZIP"
