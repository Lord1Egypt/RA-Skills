#!/usr/bin/env bash
set -euo pipefail

echo "== Peekaboo doctor =="

if command -v brew >/dev/null 2>&1; then
  echo "BREW=installed"
  command -v brew
else
  echo "BREW=missing"
fi

if command -v peekaboo >/dev/null 2>&1; then
  echo "PEEKABOO=installed"
  command -v peekaboo
  peekaboo --version || true
  echo "PERMISSIONS_CHECK=running"
  peekaboo permissions status || true
else
  echo "PEEKABOO=missing"
  echo "PERMISSIONS_CHECK=skipped"
fi
