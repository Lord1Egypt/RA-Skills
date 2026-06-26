#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$BASE_DIR"

SYSTEM_PYTHON="${PYTHON_BIN:-python3}"
VENV_DIR="$BASE_DIR/.venv"
VENV_PYTHON="$VENV_DIR/bin/python"

create_venv() {
  rm -rf "$VENV_DIR"
  "$SYSTEM_PYTHON" -m venv "$VENV_DIR"
}

if [ ! -x "$VENV_PYTHON" ]; then
  create_venv
fi

if ! "$VENV_PYTHON" -c 'import sys; print(sys.executable)' >/dev/null 2>&1; then
  create_venv
fi

"$VENV_PYTHON" -m pip install --upgrade pip >/dev/null
"$VENV_PYTHON" -m pip install -r requirements.txt

if [ ! -f config.json ]; then
  cp config.example.json config.json
fi

"$VENV_PYTHON" scripts/check_env.py || true

echo "setup_complete"
