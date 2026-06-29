#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: run_prepare_corpus.sh <input-dir> [output-dir] [extra prepare_style_corpus.py args...]" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT_DIR="$1"
shift

ARGS=(--input-dir "$INPUT_DIR")
if [[ $# -gt 0 && "${1:-}" != --* ]]; then
  ARGS+=(--output-dir "$1")
  shift
fi
ARGS+=("$@")

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$SCRIPT_DIR/prepare_style_corpus.py" "${ARGS[@]}"
fi

if command -v python >/dev/null 2>&1; then
  exec python "$SCRIPT_DIR/prepare_style_corpus.py" "${ARGS[@]}"
fi

echo "No Python runtime found. Install Python 3.10+." >&2
exit 127
