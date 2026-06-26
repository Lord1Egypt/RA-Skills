#!/usr/bin/env bash
set -euo pipefail

# Polymarket Weather Scanner - List available cities

HOST="${POLYMARKET_SCANNER_HOST:-https://polymarket-scanner.fly.dev}"
API_KEY="${POLYMARKET_SCANNER_API_KEY:-}"

RESPONSE=$(curl -s -w "\n%{http_code}" \
    ${API_KEY:+-H "X-API-Key: ${API_KEY}"} \
    "${HOST}/cities")
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" != "200" ]; then
    echo "Error ($HTTP_CODE): $(echo "$BODY" | jq -r '.detail // "Unknown error"' 2>/dev/null || echo "$BODY")"
    exit 1
fi

echo "$BODY" | jq '{
    tier: .tier,
    cities: [.cities[] | {
        key: .key,
        name: .name,
        unit: .unit,
        available: .available,
        requires: .requires
    }]
}'
