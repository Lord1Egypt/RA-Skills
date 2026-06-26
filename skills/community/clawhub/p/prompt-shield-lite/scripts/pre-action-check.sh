#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"
if [[ -z "$ACTION" ]]; then
  echo '{"ok":false,"error":"usage: pre-action-check.sh ""<action>"""}'
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
"$SCRIPT_DIR/psl-core.sh" --type action --action-text "$ACTION"
