#!/usr/bin/env bash
set -euo pipefail
# composite.sh: Place a smaller image onto a bigger image
# Usage: composite.sh <background> <overlay> [output] [options]

usage() {
  cat <<EOF
Usage: $(basename "$0") <background> <overlay> [output] [options]
Options:
  --gravity POS     Position: center, northwest, northeast, southeast, southwest, etc. (default: southeast)
  --offset +X+Y     Pixel offset from gravity point (default: +10+10)
  --resize GEO      Resize overlay before compositing (e.g., 200x200, 50%)
  --opacity PCT     Overlay opacity 0-100 (default: 100)
Examples:
  composite.sh bg.jpg logo.png output.jpg
  composite.sh bg.jpg logo.png output.jpg --gravity center
  composite.sh bg.jpg watermark.png out.jpg --resize 100x100 --opacity 50
EOF
  exit 2
}

[ $# -lt 2 ] && usage
background="$1"; shift; overlay="$1"; shift
output=""; gravity="southeast"; offset="+10+10"; resize_geo=""; opacity="100"

while [ $# -gt 0 ]; do
  case "$1" in
    --gravity) gravity="$2"; shift 2 ;; --offset) offset="$2"; shift 2 ;;
    --resize) resize_geo="$2"; shift 2 ;; --opacity) opacity="$2"; shift 2 ;;
    *) if [ -z "$output" ]; then output="$1"; shift; else echo "Unknown: $1" >&2; exit 1; fi ;;
  esac
done

[ ! -f "$background" ] && echo "ERROR: background not found: $background" >&2 && exit 1
[ ! -f "$overlay" ] && echo "ERROR: overlay not found: $overlay" >&2 && exit 1

if [ -z "$output" ]; then
  dir="$(dirname "$background")"; base="$(basename "$background")"
  ext="${base##*.}"; name="${base%.*}"
  output="${dir}/${name}-composite.${ext}"
fi

mkdir -p "$(dirname "$output")"
overlay_cmd="$overlay"; tmp_files=""

if [ -n "$resize_geo" ]; then
  tmp="/tmp/comp_resize_$$.png"
  convert "$overlay" -resize "$resize_geo" "$tmp"
  overlay_cmd="$tmp"; tmp_files="$tmp"
fi

if [ "$opacity" != "100" ]; then
  tmp2="/tmp/comp_opacity_$$.png"
  pct=$(echo "scale=2; $opacity/100" | bc)
  convert "$overlay_cmd" -alpha set -channel A -evaluate multiply "$pct" +channel "$tmp2"
  overlay_cmd="$tmp2"; tmp_files="$tmp_files $tmp2"
fi

echo "Compositing: $overlay onto $background -> $output (gravity: $gravity, offset: $offset)"
composite -gravity "$gravity" -geometry "$offset" "$overlay_cmd" "$background" "$output"
[ -n "$tmp_files" ] && rm -f $tmp_files
echo "Done: $output ($(identify -format '%wx%h' "$output"))"
