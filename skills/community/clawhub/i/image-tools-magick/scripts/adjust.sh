#!/usr/bin/env bash
set -euo pipefail
# adjust.sh: Adjust brightness, contrast, saturation, rotation, flip, blur, etc.
# Usage: adjust.sh <input> [output] [options]

usage() {
  cat <<EOF
Usage: $(basename "$0") <input> [output] [options]
Options:
  --brightness N    (-100 to 100)      --contrast N      (-100 to 100)
  --saturation N    (100=unchanged)    --rotate N        (degrees)
  --flip            (vertical)         --flop            (horizontal mirror)
  --grayscale                          --blur RADIUS     (e.g. 0x3)
  --sharpen RADIUS  (e.g. 0x1)        --negate          (invert colors)
  --border WxH                         --border-color COL
EOF
  exit 2
}

[ $# -lt 1 ] && usage
input="$1"; shift; output=""
brightness="0"; contrast="0"; saturation=""; rotate=""
flip=""; flop=""; grayscale=""; blur=""; sharpen=""
negate=""; border=""; border_color="black"

while [ $# -gt 0 ]; do
  case "$1" in
    --brightness) brightness="$2"; shift 2 ;; --contrast) contrast="$2"; shift 2 ;;
    --saturation) saturation="$2"; shift 2 ;; --rotate) rotate="$2"; shift 2 ;;
    --flip) flip=1; shift ;; --flop) flop=1; shift ;; --grayscale) grayscale=1; shift ;;
    --blur) blur="$2"; shift 2 ;; --sharpen) sharpen="$2"; shift 2 ;; --negate) negate=1; shift ;;
    --border) border="$2"; shift 2 ;; --border-color) border_color="$2"; shift 2 ;;
    *) if [ -z "$output" ]; then output="$1"; shift; else echo "Unknown: $1" >&2; exit 1; fi ;;
  esac
done

[ ! -f "$input" ] && echo "ERROR: file not found: $input" >&2 && exit 1
if [ -z "$output" ]; then
  dir="$(dirname "$input")"; base="$(basename "$input")"
  ext="${base##*.}"; name="${base%.*}"
  output="${dir}/${name}-adjusted.${ext}"
fi
mkdir -p "$(dirname "$output")"

cmd="convert \"$input\""
[ "$brightness" != "0" ] || [ "$contrast" != "0" ] && cmd="$cmd -brightness-contrast ${brightness}x${contrast}"
[ -n "$saturation" ] && cmd="$cmd -modulate 100,${saturation},100"
[ -n "$rotate" ] && cmd="$cmd -rotate $rotate"
[ -n "$flip" ] && cmd="$cmd -flip"
[ -n "$flop" ] && cmd="$cmd -flop"
[ -n "$grayscale" ] && cmd="$cmd -colorspace Gray"
[ -n "$blur" ] && cmd="$cmd -blur $blur"
[ -n "$sharpen" ] && cmd="$cmd -sharpen $sharpen"
[ -n "$negate" ] && cmd="$cmd -negate"
[ -n "$border" ] && cmd="$cmd -bordercolor \"$border_color\" -border $border"
cmd="$cmd \"$output\""

echo "Adjusting: $input -> $output"
eval "$cmd"
echo "Done: $output ($(identify -format '%wx%h' "$output"))"
