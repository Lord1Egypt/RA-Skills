#!/usr/bin/env bash
# Deterministic, identity-preserving portrait light sculpting.
# Usage: portrait-lighting.sh <input> <output.png> [style] [strength]
#   style     — natural_dimension | soft_luminous | studio_definition
#   strength  — 0-1; omitted uses the selected style's calibrated default.
set -euo pipefail

BASE="${MCE_API_BASE:-https://mce.motu.art}"
IN="${1:?usage: portrait-lighting.sh <input> <output.png> [style] [strength]}"
OUT="${2:?usage: portrait-lighting.sh <input> <output.png> [style] [strength]}"
STYLE="${3:-natural_dimension}"
STRENGTH="${4:-}"

[ -f "$IN" ] || { echo "input not found: $IN" >&2; exit 1; }

args=(-sS -A "motu-mce-skill/1.0" -X POST "$BASE/v1/portrait-lighting"
  -F "file=@$IN"
  -F "style=$STYLE"
  -F "output_format=png"
  -o "$OUT"
  -w "%{http_code}")
[ -n "$STRENGTH" ] && args+=(-F "strength=$STRENGTH")
[ -n "${MCE_API_KEY:-}" ] && args+=(-H "X-API-Key: $MCE_API_KEY")

code="$(curl "${args[@]}")"
if [ "$code" != "200" ]; then
  echo "portrait lighting failed (HTTP $code): $(cat "$OUT" 2>/dev/null)" >&2
  rm -f "$OUT"
  exit 1
fi
echo "saved $OUT  (style=$STYLE${STRENGTH:+ strength=$STRENGTH}, identity and geometry preserved)"
