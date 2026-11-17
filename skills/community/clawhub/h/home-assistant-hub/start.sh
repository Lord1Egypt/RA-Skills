#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
# Kill any existing instance
pkill -f "ha-hub.js start" 2>/dev/null || true
sleep 1

nohup node "$SCRIPT_DIR/scripts/ha-hub.js" start > "$SCRIPT_DIR/logs/hub.log" 2>&1 &
HUB_PID=$!
echo "$HUB_PID" > hub.pid
disown $HUB_PID
echo "Hub started with PID: $HUB_PID"
