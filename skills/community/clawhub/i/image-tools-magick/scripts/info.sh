#!/usr/bin/env bash
set -euo pipefail
# info.sh: Get image metadata and properties
[ $# -lt 1 ] && echo "Usage: $(basename "$0") <image>" && exit 2
input="$1"
[ ! -f "$input" ] && echo "ERROR: file not found: $input" >&2 && exit 1
echo "=== Image Info: $input ==="
identify -verbose "$input" 2>/dev/null | grep -E '(Filename|Format|Geometry|Resolution|Colorspace|Depth|Filesize|Type|Units)' | head -15
echo ""
echo "Quick: $(identify -format 'Format: %m | Size: %wx%h | Depth: %z-bit | Filesize: %b' "$input")"
