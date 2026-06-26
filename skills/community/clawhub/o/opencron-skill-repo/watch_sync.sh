#!/bin/sh
# Sync jobs.json to canvas/cron-data.json every 30 seconds.
# Run as: nohup sh skills/opencron/watch_sync.sh &
JOBS="$HOME/.openclaw/cron/jobs.json"
DEST="$HOME/.openclaw/canvas/cron-data.json"
while true; do
    cp "$JOBS" "$DEST" 2>/dev/null
    sleep 30
done
