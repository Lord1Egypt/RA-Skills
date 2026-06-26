#!/usr/bin/env bash
# install.sh — One-shot setup for ocmesh
# Installs deps, registers LaunchAgent (macOS), starts the daemon.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# The actual ocmesh source lives one level up (skill root)
OCMESH_DIR="$(dirname "$SCRIPT_DIR")"
PLIST_SRC="$OCMESH_DIR/com.ocmesh.agent.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.ocmesh.agent.plist"
LOG_DIR="$HOME/.ocmesh"

echo "==> ocmesh installer"

mkdir -p "$LOG_DIR"
echo "    Log directory: $LOG_DIR"

echo "==> Installing Node dependencies..."
cd "$OCMESH_DIR"
npm install

NODE_PATH="$(which node)"
echo "    Node binary: $NODE_PATH"

sed "s|/usr/local/bin/node|$NODE_PATH|g; s|OCMESH_DIR|$OCMESH_DIR|g" \
  "$PLIST_SRC" > "$PLIST_DST"
echo "    LaunchAgent installed: $PLIST_DST"

launchctl unload "$PLIST_DST" 2>/dev/null || true
launchctl load -w "$PLIST_DST"
echo "    LaunchAgent loaded and enabled"

sleep 2
echo ""
echo "✅ ocmesh is running!"
echo ""
echo "  API:  http://127.0.0.1:7432"
echo "  Logs: $LOG_DIR/ocmesh.log"
echo ""
curl -s http://127.0.0.1:7432/status || echo "(daemon still starting up)"
