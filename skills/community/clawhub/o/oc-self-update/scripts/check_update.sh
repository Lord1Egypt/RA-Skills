#!/usr/bin/env bash
# Check installed OpenClaw version vs latest on npm

set -euo pipefail

INSTALLED=$(npm list -g openclaw --depth=0 2>/dev/null | grep openclaw | sed 's/.*openclaw@//')
LATEST=$(npm show openclaw dist-tags.latest 2>/dev/null)

echo "Installed : $INSTALLED"
echo "Latest    : $LATEST"

if [ "$INSTALLED" = "$LATEST" ]; then
  echo "Status    : up to date"
  exit 0
else
  echo "Status    : update available"
  exit 1
fi
