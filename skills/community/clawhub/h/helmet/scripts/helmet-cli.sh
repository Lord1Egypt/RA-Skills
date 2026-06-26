#!/usr/bin/env bash
set -euo pipefail

if command -v helmet >/dev/null 2>&1; then
  helmet "$@"
else
  # Fallback: run from local build
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
  node "$REPO_ROOT/dist/cli.js" "$@"
fi
