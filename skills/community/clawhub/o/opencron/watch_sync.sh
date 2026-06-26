#!/bin/sh
# Regenerate the embedded dashboard HTML every 30 seconds.
# This re-reads jobs.json and run history and writes fresh HTML.
# Run as: nohup sh skills/opencron/watch_sync.sh &
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
while true; do
    python3 "$SCRIPT_DIR/update_canvas.py" --sync 2>/dev/null
    sleep 30
done
