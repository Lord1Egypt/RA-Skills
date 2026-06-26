#!/bin/bash
set -euo pipefail

PROJECT_DIR="/Users/ShiXin/Documents/Workspace/github-project/opencli"
SOURCE_ENTRY="$PROJECT_DIR/dist/main.js"

if [[ -f "$SOURCE_ENTRY" ]]; then
  cd "$PROJECT_DIR"
  exec node "$SOURCE_ENTRY" "$@"
fi

if command -v opencli >/dev/null 2>&1; then
  exec "$(command -v opencli)" "$@"
fi

echo "opencli entrypoint not found. Expected source build at $SOURCE_ENTRY or a global opencli binary on PATH." >&2
exit 127
