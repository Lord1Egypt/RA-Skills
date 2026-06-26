#!/usr/bin/env bash
set -euo pipefail
# convert-format.sh: Convert image format (PNG<->JPG<->WebP<->GIF etc.)
# Usage: convert-format.sh <input> <output> [--quality N] [--strip]

[ $# -lt 2 ] && echo "Usage: $(basename "$0") <input> <output> [--quality N] [--strip]" && exit 2
input="$1"; output="$2"; shift 2; quality="85"; strip_flag=""
while [ $# -gt 0 ]; do
  case "$1" in
    --quality) quality="$2"; shift 2 ;; --strip) strip_flag="-strip"; shift ;;
    *) echo "Unknown: $1" >&2; exit 1 ;;
  esac
done
[ ! -f "$input" ] && echo "ERROR: file not found: $input" >&2 && exit 1
mkdir -p "$(dirname "$output")"
echo "Converting: $input -> $output"
ext="${output##*.}"; ext_lower="$(echo "$ext" | tr '[:upper:]' '[:lower:]')"
case "$ext_lower" in
  jpg|jpeg|webp) convert "$input" -quality "$quality" $strip_flag "$output" ;;
  *) convert "$input" $strip_flag "$output" ;;
esac
echo "Done: $output"
