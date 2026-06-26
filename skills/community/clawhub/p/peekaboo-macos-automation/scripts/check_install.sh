#!/usr/bin/env bash
set -euo pipefail

if command -v peekaboo >/dev/null 2>&1; then
  echo "STATUS=installed"
  command -v peekaboo
  peekaboo --version || true
  exit 0
fi

echo "STATUS=missing"
exit 0
