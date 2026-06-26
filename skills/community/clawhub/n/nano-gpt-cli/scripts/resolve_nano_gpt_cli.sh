#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOCAL_BIN="$ROOT_DIR/cli/dist/src/bin.js"

if [[ -f "$LOCAL_BIN" ]]; then
  exec node "$LOCAL_BIN" "$@"
fi

if command -v nano-gpt >/dev/null 2>&1; then
  exec nano-gpt "$@"
fi

cat >&2 <<'EOF'
nano-gpt is not available.

Build the local CLI:
  npm install
  npm run build

Or install the published package globally:
  npm install -g nano-gpt-cli
EOF
exit 1
