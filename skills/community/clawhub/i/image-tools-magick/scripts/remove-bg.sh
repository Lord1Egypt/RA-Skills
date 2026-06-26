#!/usr/bin/env bash
set -euo pipefail
# remove-bg.sh: Remove solid background color -> transparent PNG
# Usage: remove-bg.sh <input> <output> [tolerance] [color]

[ $# -lt 2 ] && echo "Usage: $(basename "$0") <input> <output> [tolerance%] [color]" && exit 2
input="$1"; output="$2"; tolerance="${3:-20}"; color="${4:-#FFFFFF}"
[ ! -f "$input" ] && echo "ERROR: file not found: $input" >&2 && exit 1
mkdir -p "$(dirname "$output")"
echo "Removing background: $color (tolerance: ${tolerance}%) | $input -> $output"
convert "$input" -fuzz "${tolerance}%" -transparent "$color" "$output"
echo "Done: $output"
