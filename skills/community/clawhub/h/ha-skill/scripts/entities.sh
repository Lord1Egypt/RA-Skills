#!/bin/bash
# List Home Assistant entities by domain

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CREDENTIALS_FILE="$HOME/.openclaw/credentials/homeassistant.json"

# Parse credentials
URL=$(jq -r '.url' "$CREDENTIALS_FILE")
TOKEN=$(jq -r '.token' "$CREDENTIALS_FILE")

# Get domain from argument
DOMAIN="${1:-all}"

# Build API endpoint
if [[ "$DOMAIN" == "all" ]]; then
    ENDPOINT="/api/states"
else
    ENDPOINT="/api/states"
fi

# Fetch entities
RESPONSE=$(curl -s -X GET "${URL}${ENDPOINT}" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json")

# Check for error
if echo "$RESPONSE" | jq -e '.error' > /dev/null 2>&1; then
    echo "Error: $(echo "$RESPONSE" | jq -r '.error')"
    exit 1
fi

# Filter and format
if [[ "$DOMAIN" == "all" ]]; then
    echo "$RESPONSE" | jq -r '.[] | "\(.entity_id) | \(.state) | \(.attributes.friendly_name // "N/A")"' | sort
elif [[ "$DOMAIN" == "search" ]]; then
    SEARCH="${2:-}"
    if [[ -z "$SEARCH" ]]; then
        echo "Usage: $0 search <keyword>"
        exit 1
    fi
    echo "$RESPONSE" | jq -r '.[] | "\(.entity_id) | \(.state) | \(.attributes.friendly_name // "N/A")"' | grep -i "$SEARCH" | sort
else
    echo "$RESPONSE" | jq -r --arg domain "$DOMAIN" '.[] | select(.entity_id | startswith($domain + ".")) | "\(.entity_id) | \(.state) | \(.attributes.friendly_name // "N/A")"' | sort
fi