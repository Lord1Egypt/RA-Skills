#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORKSPACE_ROOT="${OPENCLAW_WORKSPACE:-$(cd "$ROOT/../.." && pwd)}"
TARGET="$WORKSPACE_ROOT/skills/openclaw-consensus"
MARKER="$TARGET/.openclaw-consensus-dev-install"

if [ ! -e "$TARGET" ]; then
  echo "No installed openclaw-consensus directory found at $TARGET"
  exit 0
fi

if [ ! -f "$MARKER" ]; then
  echo "Refusing to remove target without repo install marker: $TARGET" >&2
  exit 1
fi

rm -rf "$TARGET"
echo "Removed openclaw-consensus skill copy: $TARGET"
