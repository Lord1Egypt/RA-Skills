#!/bin/bash
set -e
source "$(dirname "$0")/../env.sh"

# Check if daemon already running
if [ -f "$STATE_DIR/daemon.pid" ]; then
    PID=$(cat "$STATE_DIR/daemon.pid")
    if kill -0 "$PID" 2>/dev/null; then
        # Daemon running, return current state
        cat "$STATE_DIR/state.json" 2>/dev/null || echo '{"status": "connected", "state": "loading"}'
        exit 0
    fi
    # Stale PID file
    rm -f "$STATE_DIR/daemon.pid"
fi

# Start daemon in background, capture initial state from its stdout
python3 "$(dirname "$0")/../daemon/town_daemon.py" > "$STATE_DIR/initial_output.txt" 2>"$STATE_DIR/daemon.log" &
DAEMON_PID=$!

# Wait for state file to appear (daemon writes it on connect)
for i in $(seq 1 30); do
    if [ -f "$STATE_DIR/state.json" ]; then
        cat "$STATE_DIR/state.json"
        exit 0
    fi
    # Check daemon still alive
    if ! kill -0 "$DAEMON_PID" 2>/dev/null; then
        echo '{"error": "daemon exited unexpectedly", "log": "'$(tail -1 "$STATE_DIR/daemon.log" 2>/dev/null)'"}'
        exit 1
    fi
    sleep 0.5
done

echo '{"error": "timeout waiting for daemon to connect"}'
exit 1
