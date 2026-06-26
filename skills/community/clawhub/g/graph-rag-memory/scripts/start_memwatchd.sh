#!/bin/bash
# start_memwatchd.sh — Start the memory watcher daemon if not already running.
# Call from HEARTBEAT.md or session startup.

WORKSPACE="${1:-/home/node/.openclaw/workspace}"
DAEMON="$WORKSPACE/memory-upgrade/memwatchd"
PIDFILE="/tmp/memwatchd.pid"
LOGFILE="/tmp/memwatchd.log"

# Rebuild if binary missing
if [ ! -x "$DAEMON" ]; then
    echo "[memwatchd] Binary not found, building..."
    gcc -O2 -o "$DAEMON" "$WORKSPACE/memory-upgrade/memwatchd.c" 2>&1
fi

# Check if already running
if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "[memwatchd] Already running (pid $PID)"
        exit 0
    fi
fi

# Start daemon
"$DAEMON" "$WORKSPACE" >> "$LOGFILE" 2>&1 &
sleep 0.5
if [ -f "$PIDFILE" ]; then
    echo "[memwatchd] Started (pid $(cat $PIDFILE))"
else
    echo "[memwatchd] Failed to start"
    exit 1
fi
