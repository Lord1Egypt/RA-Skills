#!/usr/bin/env bash
set -euo pipefail

# Polymarket Weather Scanner - Scan for mispriced markets
# Requires: POLYMARKET_SCANNER_API_KEY, POLYMARKET_SCANNER_HOST

HOST="${POLYMARKET_SCANNER_HOST:-https://polymarket-scanner.fly.dev}"
API_KEY="${POLYMARKET_SCANNER_API_KEY:-}"
DAYS="${1:-1}"

RESPONSE=$(curl -s -w "\n%{http_code}" \
    ${API_KEY:+-H "X-API-Key: ${API_KEY}"} \
    "${HOST}/scan/weather?days_ahead=${DAYS}")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" != "200" ]; then
    echo "Error ($HTTP_CODE): $(echo "$BODY" | jq -r '.detail // .message // "Unknown error"' 2>/dev/null || echo "$BODY")"
    exit 1
fi

# Output formatted JSON
echo "$BODY" | jq '{
    scan_time: .scan_time,
    tier: .tier,
    markets_scanned: .markets_scanned,
    opportunities: [.opportunities[] | {
        city: .city_name,
        date: .target_date,
        forecast: "\(.forecast_temp)\(.forecast_unit)",
        confidence: .confidence_tier,
        models: .n_models,
        agreement: "\(.model_agreement * 100 | round)%",
        edge: "\(.total_edge * 100 | . * 10 | round / 10)%",
        cost: "$\(.total_cost)",
        ranges: [.ranges[] | {
            range: .range_desc,
            prob: "\(.forecast_prob * 100 | round)%",
            price: "$\(.market_price)",
            edge: "\(.edge * 100 | . * 10 | round / 10)%",
            slug: .market_slug
        }]
    }]
}'
