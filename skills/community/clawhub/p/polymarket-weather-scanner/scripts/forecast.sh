#!/usr/bin/env bash
set -euo pipefail

# Polymarket Weather Scanner - Get ensemble forecast for a city
# Usage: forecast.sh <city> [date]

HOST="${POLYMARKET_SCANNER_HOST:-https://polymarket-scanner.fly.dev}"
API_KEY="${POLYMARKET_SCANNER_API_KEY:-}"

CITY="${1:?Usage: forecast.sh <city> [YYYY-MM-DD]}"
# Sanitize city input: only allow alphanumeric, spaces, hyphens
CITY=$(echo "$CITY" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9 -]//g' | sed 's/ /%20/g')
DATE="${2:-}"

URL="${HOST}/forecast/${CITY}"
if [ -n "$DATE" ]; then
    URL="${URL}?target_date=${DATE}"
fi

RESPONSE=$(curl -s -w "\n%{http_code}" \
    ${API_KEY:+-H "X-API-Key: ${API_KEY}"} \
    "$URL")
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" != "200" ]; then
    echo "Error ($HTTP_CODE): $(echo "$BODY" | jq -r '.detail // .message // "Unknown error"' 2>/dev/null || echo "$BODY")"
    exit 1
fi

echo "$BODY" | jq '{
    city: .city_name,
    date: .target_date,
    forecast: "\(.high_temp) \(.unit)",
    std_dev: .ensemble_std,
    models_count: .n_models,
    horizon_days: .horizon_days,
    model_predictions: .model_temps
}'
