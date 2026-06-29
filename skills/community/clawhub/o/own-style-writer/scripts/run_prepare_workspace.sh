#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: run_prepare_workspace.sh <style-dir> [content-dir] [extra prepare_writing_workspace.py args...]" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STYLE_DIR="$1"
shift

ARGS=(--style-dir "$STYLE_DIR")
if [[ $# -gt 0 && "${1:-}" != --* ]]; then
  ARGS+=(--content-dir "$1")
  shift
fi
ARGS+=("$@")

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$SCRIPT_DIR/prepare_writing_workspace.py" "${ARGS[@]}"
fi

if command -v python >/dev/null 2>&1; then
  exec python "$SCRIPT_DIR/prepare_writing_workspace.py" "${ARGS[@]}"
fi

echo "No Python runtime found. Install Python 3.10+." >&2
exit 127
