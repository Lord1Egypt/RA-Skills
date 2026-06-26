#!/usr/bin/env bash
set -euo pipefail

if command -v peekaboo >/dev/null 2>&1; then
  echo "STATUS=already-installed"
  peekaboo --version || true
  exit 0
fi

if ! command -v brew >/dev/null 2>&1; then
  echo "STATUS=brew-missing"
  exit 2
fi

brew install steipete/tap/peekaboo

echo "STATUS=installed-now"
command -v peekaboo
peekaboo --version || true
