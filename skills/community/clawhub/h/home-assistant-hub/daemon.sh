#!/bin/bash
# Daemon wrapper: forks node properly so it survives shell exit
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Kill any existing instance first
if [ -f hub.pid ]; then
    OLD_PID=$(cat hub.pid)
    kill "$OLD_PID" 2>/dev/null || true
    sleep 1
fi

/usr/bin/node "$SCRIPT_DIR/scripts/ha-hub.js" start >> "$SCRIPT_DIR/logs/hub.log" 2>&1 &
NODEPID=$!
disown $NODEPID
echo "$NODEPID" > hub.pid

# Wait briefly then exit — node stays alive
sleep 1
exit 0
