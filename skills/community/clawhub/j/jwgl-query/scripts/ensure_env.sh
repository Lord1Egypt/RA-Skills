#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$BASE_DIR"

VENV_PYTHON="$BASE_DIR/.venv/bin/python"
CHECK_SCRIPT="$BASE_DIR/scripts/check_env.py"
SETUP_SCRIPT="$BASE_DIR/scripts/setup.sh"

needs_setup=0

if [ ! -x "$VENV_PYTHON" ]; then
  needs_setup=1
elif ! "$VENV_PYTHON" "$CHECK_SCRIPT" | tail -n 1 | grep -qx 'ready'; then
  needs_setup=1
fi

if [ ! -f "$BASE_DIR/config.json" ]; then
  needs_setup=1
fi

if [ "$needs_setup" -eq 1 ]; then
  bash "$SETUP_SCRIPT"
fi

echo "env_ready"
