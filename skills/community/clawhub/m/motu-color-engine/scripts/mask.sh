#!/usr/bin/env bash
# Export a segmentation mask via POST /v1/mask (skips grading). Saves a grayscale PNG.
# Usage: mask.sh <input> <output.png> [mask-kind]
#   mask-kind: skin (default) | valid_skin | face | person
set -euo pipefail

BASE="${MCE_API_BASE:-https://mce.motu.art}"
IN="${1:?usage: mask.sh <input> <output.png> [mask-kind]}"
OUT="${2:?usage: mask.sh <input> <output.png> [mask-kind]}"
KIND="${3:-skin}"

[ -f "$IN" ] || { echo "input not found: $IN" >&2; exit 1; }

args=(-sS -A "motu-mce-skill/1.0" -X POST "$BASE/v1/mask"
  -F "file=@$IN"
  -F "mask_kind=$KIND"
  -o "$OUT"
  -w "%{http_code}")
[ -n "${MCE_API_KEY:-}" ] && args+=(-H "X-API-Key: $MCE_API_KEY")

code="$(curl "${args[@]}")"
if [ "$code" != "200" ]; then
  echo "mask failed (HTTP $code): $(cat "$OUT" 2>/dev/null)" >&2
  rm -f "$OUT"
  exit 1
fi
echo "saved $OUT  ($KIND mask)"
