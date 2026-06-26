#!/usr/bin/env bash
# No.0 Core installer — cognitive file guardian, zero external deps.
#
# Usage:  ./install.sh [target_dir]
# Default target: ~/.openclaw/workspace/skills/no0-skill

set -euo pipefail

SRC_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
TARGET="${1:-$HOME/.openclaw/workspace/skills/no0-skill}"

echo "→ Installing No.0 Core"
echo "  source: $SRC_DIR"
echo "  target: $TARGET"

mkdir -p "$TARGET"

# Dispatcher (all platforms) + Core package.
cp    "$SRC_DIR/no0"         "$TARGET/"
cp    "$SRC_DIR/no0.command" "$TARGET/"
cp    "$SRC_DIR/no0.ps1"     "$TARGET/"
cp    "$SRC_DIR/no0.cmd"     "$TARGET/"
cp    "$SRC_DIR/no0.bat"     "$TARGET/"
cp -R "$SRC_DIR/no0-core"    "$TARGET/"

chmod +x "$TARGET/no0" "$TARGET/no0.command" 2>/dev/null || true

# Runtime data dirs under ~/.openclaw/no0/ (shared with DLC).
mkdir -p "$HOME/.openclaw/no0/events/pending"
mkdir -p "$HOME/.openclaw/no0/events/processed"
mkdir -p "$HOME/.openclaw/no0/backups"

echo "✓ No.0 Core installed."
echo
echo "Next:"
echo "  cd \"$TARGET\""
echo "  ./no0 start"
echo "  ./no0 status"
echo
echo "Optional — add the Internal Control DLC:"
echo "  $SRC_DIR/install-dlc.sh [$TARGET]"
