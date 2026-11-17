#!/usr/bin/env bash
# Export an upload-ready image via POST /v1/optimize.
# Usage: optimize.sh <input> <output> [format] [max-kb] [quality] [resize] [dpi]
set -euo pipefail

BASE="${MCE_API_BASE:-https://mce.motu.art}"
IN="${1:?usage: optimize.sh <input> <output> [format] [max-kb] [quality] [resize] [dpi]}"
OUT="${2:?usage: optimize.sh <input> <output> [format] [max-kb] [quality] [resize] [dpi]}"
FORMAT="${3:-jpg}"
MAX_KB="${4:-}"
QUALITY="${5:-92}"
RESIZE="${6:-}"
DPI="${7:-}"

[ -f "$IN" ] || { echo "input not found: $IN" >&2; exit 1; }
HEADERS_FILE="$(mktemp)"
trap 'rm -f "$HEADERS_FILE"' EXIT
args=(-sS -A "motu-mce-skill/1.0" -X POST "$BASE/v1/optimize"
  -F "file=@$IN"
  -F "output_format=$FORMAT"
  -F "quality=$QUALITY"
  -D "$HEADERS_FILE"
  -o "$OUT"
  -w "%{http_code}")
[ -n "$MAX_KB" ] && args+=(-F "max_kb=$MAX_KB")
[ -n "$RESIZE" ] && args+=(-F "resize=$RESIZE")
[ -n "$DPI" ] && args+=(-F "dpi=$DPI")
[ -n "${MCE_API_KEY:-}" ] && args+=(-H "X-API-Key: $MCE_API_KEY")
code="$(curl "${args[@]}")"
if [ "$code" != "200" ]; then
  echo "optimize failed (HTTP $code): $(cat "$OUT" 2>/dev/null)" >&2
  rm -f "$OUT"
  exit 1
fi
info="$(grep -i '^x-mce-export-info:' "$HEADERS_FILE" | sed -E 's/^[^:]+:[[:space:]]*//' | tr -d '\r')"
echo "saved $OUT"
[ -n "$info" ] && echo "export info: $info"
