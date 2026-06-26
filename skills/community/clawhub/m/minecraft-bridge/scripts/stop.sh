#!/bin/bash
PID_FILE="${XDG_RUNTIME_DIR:-/tmp}/minecraft-bridge-$(id -u).pid"

if [ ! -f "$PID_FILE" ]; then
  echo "Bridge was not started via start.sh (PID file missing)."
  echo "Trying to stop by process match..."
  pkill -f "bridge-server.js" && echo "Bridge stopped" || echo "No running bridge process found"
  exit 0
fi

PID=$(cat "$PID_FILE")
if kill -0 "$PID" 2>/dev/null; then
  kill "$PID"
  rm "$PID_FILE"
  echo "Minecraft Bridge stopped (PID=$PID)"
else
  echo "Bridge process no longer exists (PID=$PID)"
  rm "$PID_FILE"
fi
