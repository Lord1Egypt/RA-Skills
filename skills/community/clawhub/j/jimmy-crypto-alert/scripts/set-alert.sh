#!/bin/bash
# Set a price alert
# Usage: bash set-alert.sh btc 100000 "BTC above 100K"

STATE_FILE="$HOME/.crypto-alert-state.json"
TOKEN=$1
THRESHOLD=$2
MESSAGE="${3:-Alert for $TOKEN}"

if [ -z "$TOKEN" ] || [ -z "$THRESHOLD" ]; then
    echo "Usage: bash set-alert.sh <token> <threshold> [message]"
    exit 1
fi

mkdir -p "$(dirname "$STATE_FILE")"

# Create state file if doesn't exist
if [ ! -f "$STATE_FILE" ]; then
    echo '{"alerts":[]}' > "$STATE_FILE"
fi

# Add alert
ALERT_ID=$(date +%s)
NEW_ALERT=$(cat <<EOF
{"id":$ALERT_ID,"token":"$TOKEN","threshold":$THRESHOLD,"message":"$MESSAGE","active":true,"created":"$(date -u +%Y-%m-%dT%H:%M:%SZ)"}
EOF
)

# Simple jq-less update
python3 << EOF
import json
with open("$STATE_FILE") as f:
    state = json.load(f)
state["alerts"].append(json.loads('''$NEW_ALERT'''))
with open("$STATE_FILE","w") as f:
    json.dump(state,f,indent=2)
EOF

echo "✅ Alert set: $MESSAGE (ID: $ALERT_ID)"
