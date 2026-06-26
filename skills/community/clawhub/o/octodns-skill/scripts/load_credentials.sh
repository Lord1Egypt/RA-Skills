#!/usr/bin/env bash
# Load easyDNS credentials from JSON and export as environment variables

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CREDS_FILE="/Users/markjr/clawd/.credentials/easydns.json"

if [ ! -f "$CREDS_FILE" ]; then
    echo "Error: Credentials file not found: $CREDS_FILE"
    exit 1
fi

# Extract values from JSON and export
export EASYDNS_TOKEN=$(python3 -c "import json; print(json.load(open('$CREDS_FILE'))['api_token'])")
export EASYDNS_API_KEY=$(python3 -c "import json; print(json.load(open('$CREDS_FILE'))['api_key'])")
export EASYDNS_PORTFOLIO=$(python3 -c "import json; print(json.load(open('$CREDS_FILE'))['portfolio'])")

# Verify credentials are loaded
if [ -z "$EASYDNS_TOKEN" ] || [ -z "$EASYDNS_API_KEY" ]; then
    echo "Error: Failed to load credentials from $CREDS_FILE"
    exit 1
fi

echo "✓ easyDNS credentials loaded"
