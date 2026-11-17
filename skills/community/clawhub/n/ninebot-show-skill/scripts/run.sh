#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
VENV="$SKILL_DIR/.venv"

if [[ ! -x "$VENV/bin/python" ]]; then
  echo "ninebot-show-skill 尚未初始化。先运行: bash $SKILL_DIR/scripts/setup.sh" >&2
  exit 2
fi

exec "$VENV/bin/python" "$SCRIPT_DIR/ninebot_report.py" "$@"
