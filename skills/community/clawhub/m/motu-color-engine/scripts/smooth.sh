#!/usr/bin/env bash
# Standalone M15 professional skin smoothing via POST /v1/smooth (no color grading).
# Usage: smooth.sh <input> <output.png> [strength] [texture-retain]
#   strength        — smoothing amount, 0-1 (default 0.6).
#   texture-retain  — how much pore/texture detail to keep, 0-1 (default 0.35).
set -euo pipefail

BASE="${MCE_API_BASE:-https://mce.motu.art}"
IN="${1:?usage: smooth.sh <input> <output.png> [strength] [texture-retain]}"
OUT="${2:?usage: smooth.sh <input> <output.png> [strength] [texture-retain]}"
STRENGTH="${3:-0.6}"
TEXTURE_RETAIN="${4:-0.35}"

[ -f "$IN" ] || { echo "input not found: $IN" >&2; exit 1; }

args=(-sS -A "motu-mce-skill/1.0" -X POST "$BASE/v1/smooth"
  -F "file=@$IN"
  -F "strength=$STRENGTH"
  -F "texture_retain=$TEXTURE_RETAIN"
  -F "output_format=png"
  -o "$OUT"
  -w "%{http_code}")
[ -n "${MCE_API_KEY:-}" ] && args+=(-H "X-API-Key: $MCE_API_KEY")

code="$(curl "${args[@]}")"
if [ "$code" != "200" ]; then
  echo "smooth failed (HTTP $code): $(cat "$OUT" 2>/dev/null)" >&2
  rm -f "$OUT"
  exit 1
fi
echo "saved $OUT  (strength=$STRENGTH texture_retain=$TEXTURE_RETAIN, color unchanged)"
