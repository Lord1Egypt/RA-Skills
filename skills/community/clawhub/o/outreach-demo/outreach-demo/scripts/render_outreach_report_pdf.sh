#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<EOF
Usage: $0 --input <brief.html> --output <brief.pdf>
EOF
}

INPUT=""
OUTPUT=""
CHROME_BIN="${CHROME_BIN:-}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --input) INPUT="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    *) usage; exit 2 ;;
  esac
done

[[ -n "$INPUT" && -n "$OUTPUT" ]] || { usage; exit 2; }
[[ -f "$INPUT" ]] || { echo "missing input html" >&2; exit 2; }

if [[ -z "$CHROME_BIN" ]]; then
  if command -v chromium >/dev/null 2>&1; then CHROME_BIN="$(command -v chromium)";
  elif command -v chromium-browser >/dev/null 2>&1; then CHROME_BIN="$(command -v chromium-browser)";
  else echo "chromium not found" >&2; exit 2; fi
fi

INPUT_URL="file://$INPUT"
"$CHROME_BIN" \
  --headless=new \
  --disable-gpu \
  --no-sandbox \
  --print-to-pdf="$OUTPUT" \
  "$INPUT_URL" >/dev/null 2>&1

test -f "$OUTPUT" || { echo "pdf render failed" >&2; exit 1; }
