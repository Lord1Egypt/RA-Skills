#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PY="${PYTHON:-python3}"

$PY "$SCRIPT_DIR/scripts/md_img_r2.py" "$@"
