#!/usr/bin/env bash
# Layout ID photos onto a print sheet via POST /v1/print-sheet.
# Usage: print-sheet.sh <output> <paper> <input1> [input2 ...]
set -euo pipefail

BASE="${MCE_API_BASE:-https://mce.motu.art}"
OUT="${1:?usage: print-sheet.sh <output> <paper> <input1> [input2 ...]}"
PAPER="${2:?usage: print-sheet.sh <output> <paper> <input1> [input2 ...]}"
shift 2
[ "$#" -gt 0 ] || { echo "at least one input image is required" >&2; exit 1; }
HEADERS_FILE="$(mktemp)"
trap 'rm -f "$HEADERS_FILE"' EXIT
args=(-sS -A "motu-mce-skill/1.0" -X POST "$BASE/v1/print-sheet" -F "paper=$PAPER" -D "$HEADERS_FILE" -o "$OUT" -w "%{http_code}")
for img in "$@"; do
  [ -f "$img" ] || { echo "input not found: $img" >&2; exit 1; }
  args+=(-F "files=@$img")
done
[ -n "${MCE_API_KEY:-}" ] && args+=(-H "X-API-Key: $MCE_API_KEY")
code="$(curl "${args[@]}")"
if [ "$code" != "200" ]; then
  echo "print-sheet failed (HTTP $code): $(cat "$OUT" 2>/dev/null)" >&2
  rm -f "$OUT"
  exit 1
fi
info="$(grep -i '^x-mce-print-sheet-info:' "$HEADERS_FILE" | sed -E 's/^[^:]+:[[:space:]]*//' | tr -d '\r')"
echo "saved $OUT  paper=$PAPER"
[ -n "$info" ] && echo "print info: $info"
