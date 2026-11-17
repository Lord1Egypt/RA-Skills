#!/usr/bin/env bash
# Export a presentation-md HTML deck to a vector PDF (one page per
# slide, selectable text) using headless Chromium's native print pipeline.
#
# Usage:
#   bash scripts/export-pdf.sh ./deck.html
#   bash scripts/export-pdf.sh ./deck.html ./output.pdf
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'EOF'
Usage: export-pdf.sh <deck.html> [output.pdf]

Renders a presentation-md HTML deck to PDF via headless Chromium's
native print pipeline (vector output, selectable text — not a screenshot).
Installs Playwright + Chromium on first run if not already available.
EOF
}

if [[ $# -lt 1 || "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ ! -f "$1" ]]; then
  echo "error: input file not found: $1" >&2
  exit 1
fi
INPUT="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"

if [[ $# -ge 2 ]]; then
  mkdir -p "$(dirname "$2")"
  OUTPUT="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"
else
  OUTPUT="${INPUT%.html}.pdf"
fi

command -v npm >/dev/null 2>&1 || {
  echo "error: npm not found — install Node.js first" >&2
  exit 1
}

if [[ ! -d "$SCRIPT_DIR/node_modules/playwright" ]]; then
  echo "installing playwright (first run only)..." >&2
  npm install --prefix "$SCRIPT_DIR" --silent >&2
fi
"$SCRIPT_DIR/node_modules/.bin/playwright" install chromium >&2

NODE_PATH="$SCRIPT_DIR/node_modules" node "$SCRIPT_DIR/export-pdf.mjs" "$INPUT" "$OUTPUT"

if [[ ! -s "$OUTPUT" ]]; then
  echo "error: export failed — no PDF written to $OUTPUT" >&2
  exit 1
fi

echo "PDF written to $OUTPUT"
