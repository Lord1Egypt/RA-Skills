#!/bin/bash
ANALYZER_URL="${PRESIDIO_ANALYZER_URL:-http://localhost:5002}"
ANONYMIZER_URL="${PRESIDIO_ANONYMIZER_URL:-http://localhost:5001}"

analyzer_ok=false
anonymizer_ok=false

analyzer_status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 "$ANALYZER_URL/analyze" \
  -X POST -H "Content-Type: application/json" \
  -d '{"text":"health check","language":"en"}' 2>/dev/null)
[ "$analyzer_status" = "200" ] && analyzer_ok=true

anonymizer_status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 "$ANONYMIZER_URL/anonymize" \
  -X POST -H "Content-Type: application/json" \
  -d '{"text":"health check","anonymizers":{"DEFAULT":{"type":"replace","new_value":"[OK]"}},"analyzer_results":[]}' 2>/dev/null)
[ "$anonymizer_status" = "200" ] && anonymizer_ok=true

if $analyzer_ok && $anonymizer_ok; then
  echo '{"status":"healthy","analyzer":"up","anonymizer":"up"}'
  exit 0
elif $analyzer_ok; then
  echo '{"status":"unhealthy","analyzer":"up","anonymizer":"down"}'
  exit 1
elif $anonymizer_ok; then
  echo '{"status":"unhealthy","analyzer":"down","anonymizer":"up"}'
  exit 1
else
  echo '{"status":"unhealthy","analyzer":"down","anonymizer":"down"}'
  exit 1
fi
