#!/usr/bin/env bash
set -euo pipefail
# annotate.sh: Add text overlay to image
# Usage: annotate.sh <input> <text> [output] [options]

usage() {
  cat <<EOF
Usage: $(basename "$0") <input> <text> [output] [options]
Options:
  --font FONT       Font name (default: Helvetica)
  --size N          Font size pts (default: 36)
  --color COL       Text color (default: white)
  --bg COL          Text background (default: none)
  --gravity POS     Position (default: south)
  --offset +X+Y     Offset (default: +0+20)
  --stroke COL      Outline color
  --stroke-width N  Outline width (default: 2)
Examples:
  annotate.sh photo.jpg "Hello World" labeled.jpg
  annotate.sh photo.jpg "© 2026" out.jpg --size 16 --gravity southeast --color gray
EOF
  exit 2
}

[ $# -lt 2 ] && usage
input="$1"; text="$2"; shift 2
output=""; font="Helvetica"; size="36"; color="white"; bg="none"
gravity="south"; offset="+0+20"; stroke="none"; stroke_width="2"
while [ $# -gt 0 ]; do
  case "$1" in
    --font) font="$2"; shift 2 ;; --size) size="$2"; shift 2 ;;
    --color) color="$2"; shift 2 ;; --bg) bg="$2"; shift 2 ;;
    --gravity) gravity="$2"; shift 2 ;; --offset) offset="$2"; shift 2 ;;
    --stroke) stroke="$2"; shift 2 ;; --stroke-width) stroke_width="$2"; shift 2 ;;
    *) if [ -z "$output" ]; then output="$1"; shift; else echo "Unknown: $1" >&2; exit 1; fi ;;
  esac
done
[ ! -f "$input" ] && echo "ERROR: file not found: $input" >&2 && exit 1
if [ -z "$output" ]; then
  dir="$(dirname "$input")"; base="$(basename "$input")"
  ext="${base##*.}"; name="${base%.*}"
  output="${dir}/${name}-annotated.${ext}"
fi
mkdir -p "$(dirname "$output")"

cmd="convert \"$input\" -gravity $gravity"
[ "$stroke" != "none" ] && cmd="$cmd -stroke \"$stroke\" -strokewidth $stroke_width"
cmd="$cmd -fill \"$color\" -font \"$font\" -pointsize $size"
[ "$bg" != "none" ] && cmd="$cmd -undercolor \"$bg\""
cmd="$cmd -annotate $offset \" $text \" \"$output\""

echo "Annotating: $input -> $output | \"$text\""
eval "$cmd"
echo "Done: $output"
