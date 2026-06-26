#!/bin/bash
source "$(dirname "$0")/../env.sh"

WAKE_TIME="${1:?Usage: town_disconnect <HH:MM> [timezone]}"
TZ="${2:-UTC}"

if [ ! -S "$STATE_DIR/daemon.sock" ]; then
    echo '{"error": "Not connected to GooseTown."}'
    exit 1
fi

# Tell daemon to sleep
RESULT=$(echo "{\"action\":\"sleep\",\"wake_time\":\"$WAKE_TIME\",\"timezone\":\"$TZ\"}" | socat - UNIX-CONNECT:"$STATE_DIR/daemon.sock" 2>/dev/null)

if [ $? -ne 0 ]; then
    echo '{"error": "Failed to communicate with daemon."}'
    exit 1
fi

# Wait for daemon to exit gracefully
if [ -f "$STATE_DIR/daemon.pid" ]; then
    PID=$(cat "$STATE_DIR/daemon.pid")
    for i in $(seq 1 10); do
        kill -0 "$PID" 2>/dev/null || break
        sleep 0.5
    done
    # Force kill if still running
    kill -9 "$PID" 2>/dev/null
    rm -f "$STATE_DIR/daemon.pid"
fi

echo "{\"status\":\"sleeping\",\"wake_time\":\"$WAKE_TIME\",\"timezone\":\"$TZ\"}"
