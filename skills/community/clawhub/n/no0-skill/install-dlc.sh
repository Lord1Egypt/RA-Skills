#!/usr/bin/env bash
# No.0-DLC-Internal Control installer.
#
# Can run standalone or on top of an existing No.0 Core install.
# When Core is present, auto-enables event linkage.
#
# Usage:  ./install-dlc.sh [target_dir]
# Default target: ~/.openclaw/workspace/skills/no0-skill

set -euo pipefail

SRC_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
TARGET="${1:-$HOME/.openclaw/workspace/skills/no0-skill}"
DLC_NAME="no0-dlc-internal-control"

echo "→ Installing No.0-DLC-Internal Control"
echo "  source: $SRC_DIR/$DLC_NAME"
echo "  target: $TARGET/$DLC_NAME"

mkdir -p "$TARGET"

# Detect Core for linkage.
if [ -d "$TARGET/no0-core" ] && [ -x "$TARGET/no0" ]; then
  LINKAGE="enabled"
  echo "✓ No.0 Core detected — event linkage will be enabled."
else
  LINKAGE="disabled"
  echo "! No.0 Core not found at $TARGET — DLC will install standalone."
fi

cp -R "$SRC_DIR/$DLC_NAME" "$TARGET/"

# When standalone, copy dispatcher + supply a no-op no0-core marker so DLC
# subcommands still route correctly via ./no0.
if [ "$LINKAGE" = "disabled" ]; then
  cp "$SRC_DIR/no0" "$TARGET/" 2>/dev/null || true
  cp "$SRC_DIR/no0.command" "$TARGET/" 2>/dev/null || true
  cp "$SRC_DIR/no0.ps1" "$TARGET/" 2>/dev/null || true
  cp "$SRC_DIR/no0.cmd" "$TARGET/" 2>/dev/null || true
  cp "$SRC_DIR/no0.bat" "$TARGET/" 2>/dev/null || true
  chmod +x "$TARGET/no0" "$TARGET/no0.command" 2>/dev/null || true
fi

# Install DLC runtime deps.
if command -v python3 >/dev/null 2>&1; then
  PY="python3"
elif command -v python >/dev/null 2>&1; then
  PY="python"
else
  echo "✗ Python 3 not found — install it, then re-run this script." >&2
  exit 127
fi

# Bootstrap DLC runtime state first — so a pip hiccup (PEP 668 etc.) still
# leaves a usable skeleton behind.
mkdir -p "$HOME/.openclaw/no0/dlc"

echo "→ Installing Python dependencies (PyYAML, cryptography, keyring)"
if ! "$PY" -m pip install --user -r "$TARGET/$DLC_NAME/requirements.txt" 2>/tmp/no0-dlc-pip.log; then
  echo "! pip install failed (see /tmp/no0-dlc-pip.log). Common fixes:"
  echo "    python3 -m pip install --user --break-system-packages -r \"$TARGET/$DLC_NAME/requirements.txt\""
  echo "    # or use a venv / pipx"
  echo "  Continuing — classify commands will error until deps are present."
fi

"$PY" "$TARGET/$DLC_NAME/cli/dlc_cli.py" init || true

# If Core is present, kick off a one-shot handler sweep to validate wiring.
# The long-running handler daemon is intentionally NOT auto-started here —
# leave process management to the user (launchd/systemd/cron) for now.
if [ "$LINKAGE" = "enabled" ]; then
  echo "→ Validating event handler wiring"
  "$PY" "$TARGET/$DLC_NAME/event_listener/cognitive_event_handler.py" --once || true
fi

echo "✓ No.0-DLC-Internal Control installed."
echo
echo "Verify:"
echo "  cd \"$TARGET\""
echo "  ./no0 classify get ~/.ssh/id_rsa   # any path"
echo "  ./no0 audit log"
echo
echo "Run the event handler in the background (recommended when Core is installed):"
echo "  nohup $PY \"$TARGET/$DLC_NAME/event_listener/cognitive_event_handler.py\" >/tmp/no0-dlc.log 2>&1 &"
