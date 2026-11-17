#!/usr/bin/env bash
# Standalone purpose-crop via POST /v1/crop (decode + face/head geometry + crop
# ONLY -- no human parse, no color grading; use grade.sh for grading + crop combined).
# Defaults to the full-resolution source (crop quality is bounded by source
# resolution, not a latency budget). Saves the cropped image.
# Usage: crop.sh <input> <output> [spec-id] [bg-color] [pad-color]
#   spec-id    — crop spec id (default: one_inch). List ids with crop-specs.sh.
#   bg-color   — optional background replacement: a palette name the spec allows
#                (e.g. white/blue/red), "default" for the spec's standard color, or
#                an explicit #RRGGBB. Omit to keep the original background.
#   pad-color  — optional #RRGGBB padding when the source lacks the spec's required
#                margin. Omit to edge-replicate padding (the API default).
set -euo pipefail

BASE="${MCE_API_BASE:-https://mce.motu.art}"
IN="${1:?usage: crop.sh <input> <output> [spec-id] [bg-color] [pad-color]}"
OUT="${2:?usage: crop.sh <input> <output> [spec-id] [bg-color] [pad-color]}"
SPEC="${3:-one_inch}"
BG_COLOR="${4:-}"
PAD_COLOR="${5:-}"

[ -f "$IN" ] || { echo "input not found: $IN" >&2; exit 1; }

HEADERS_FILE="$(mktemp)"
trap 'rm -f "$HEADERS_FILE"' EXIT

args=(-sS -A "motu-mce-skill/1.0" -X POST "$BASE/v1/crop"
  -F "file=@$IN"
  -F "spec=$SPEC"
  -F "output_format=png"
  -D "$HEADERS_FILE"
  -o "$OUT"
  -w "%{http_code}")
[ -n "$BG_COLOR" ] && args+=(-F "bg_color=$BG_COLOR")
[ -n "$PAD_COLOR" ] && args+=(-F "pad_color=$PAD_COLOR")
[ -n "${MCE_API_KEY:-}" ] && args+=(-H "X-API-Key: $MCE_API_KEY")

code="$(curl "${args[@]}")"
if [ "$code" != "200" ]; then
  echo "crop failed (HTTP $code): $(cat "$OUT" 2>/dev/null)" >&2
  rm -f "$OUT"
  exit 1
fi

info="$(grep -i '^x-mce-crop-info:' "$HEADERS_FILE" | sed -E 's/^[^:]+:[[:space:]]*//' | tr -d '\r')"
echo "saved $OUT  spec=$SPEC${BG_COLOR:+ bg=$BG_COLOR}"
[ -n "$info" ] && echo "crop info: $info"
