#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$BASE_DIR"

bash "$BASE_DIR/scripts/ensure_env.sh" >/dev/null

PYTHON_BIN="$BASE_DIR/.venv/bin/python"
"$PYTHON_BIN" scripts/crawl.py "$@"
