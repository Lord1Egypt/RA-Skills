#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$DIR/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  python3 -m venv "$DIR/.venv"
  "$DIR/.venv/bin/python" -m pip install -r "$DIR/requirements.txt"
fi
exec "$PY" "$DIR/scripts/gemini_google_search.py" "$@"
