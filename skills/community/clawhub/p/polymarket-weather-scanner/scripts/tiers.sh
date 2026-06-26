#!/usr/bin/env bash
set -euo pipefail

# Polymarket Weather Scanner - Show subscription tiers

HOST="${POLYMARKET_SCANNER_HOST:-https://polymarket-scanner.fly.dev}"

RESPONSE=$(curl -s -w "\n%{http_code}" "${HOST}/tiers")
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" != "200" ]; then
    echo "Error ($HTTP_CODE): $(echo "$BODY" | jq -r '.detail // "Unknown error"' 2>/dev/null || echo "$BODY")"
    exit 1
fi

echo "$BODY" | jq '.'
