#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORKSPACE_ROOT="${OPENCLAW_WORKSPACE:-$(cd "$ROOT/../.." && pwd)}"
SKILLS_DIR="$WORKSPACE_ROOT/skills"
TARGET="$SKILLS_DIR/openclaw-consensus"
MARKER="$TARGET/.openclaw-consensus-dev-install"

mkdir -p "$SKILLS_DIR"

if [ -e "$TARGET" ] && [ ! -f "$MARKER" ]; then
  echo "Refusing to overwrite target without repo install marker: $TARGET" >&2
  exit 1
fi

rm -rf "$TARGET"
mkdir -p "$TARGET"
rsync -a --delete \
  --exclude '.git/' \
  --exclude 'node_modules/' \
  --exclude 'runs/' \
  --exclude '.DS_Store' \
  "$ROOT/" "$TARGET/"

echo "repo=$ROOT" > "$MARKER"
echo "Installed openclaw-consensus skill copy: $TARGET"
