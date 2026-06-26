#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  cat >&2 <<'USAGE'
Usage:
  bash scripts/md2pdf-browser.sh <input.md> <output.pdf> [cdp-url]

Examples:
  bash scripts/md2pdf-browser.sh doc.md doc.pdf
  bash scripts/md2pdf-browser.sh doc.md doc.pdf http://127.0.0.1:9222
  BROWSER_CDP_URL=http://192.168.1.30:9222 bash scripts/md2pdf-browser.sh doc.md doc.pdf
USAGE
  exit 1
fi

INPUT="$1"
OUTPUT="$2"
CDP_URL="${3:-${BROWSER_CDP_URL:-http://127.0.0.1:9222}}"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"

if [[ ! -f "$INPUT" ]]; then
  echo "[ERROR] Input file not found: $INPUT" >&2
  exit 1
fi
if ! command -v node >/dev/null 2>&1; then
  echo "[ERROR] node not found." >&2
  exit 1
fi
if ! command -v npm >/dev/null 2>&1; then
  echo "[ERROR] npm not found." >&2
  exit 1
fi

if [[ ! -d "$ROOT_DIR/node_modules/puppeteer-core" ]] || [[ ! -d "$ROOT_DIR/node_modules/marked" ]] || [[ ! -d "$ROOT_DIR/node_modules/twemoji" ]]; then
  (cd "$ROOT_DIR" && npm install)
fi

node "$SCRIPT_DIR/md2pdf_browser.js" "$INPUT" "$OUTPUT" "$CDP_URL"
