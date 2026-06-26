#!/bin/bash
source "$(dirname "$0")/../env.sh"

if [ -f "$STATE_DIR/state.json" ]; then
    cat "$STATE_DIR/state.json"
else
    # Check alarm
    if [ -f "$STATE_DIR/alarm.json" ]; then
        echo '{"status": "sleeping", "alarm": '$(cat "$STATE_DIR/alarm.json")'}'
    else
        echo '{"status": "not_connected", "message": "Run town_connect to join GooseTown"}'
    fi
fi
