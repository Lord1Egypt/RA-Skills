#!/bin/bash
# Onebound gateway request helper
# Usage: gateway-request.sh <path> <title> [key=value ...]

set -euo pipefail

if ! command -v curl >/dev/null 2>&1; then
  echo "Error: curl is required." >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "Error: jq is required." >&2
  exit 1
fi

if [ -z "${ONEBOUND_API_KEY:-}" ]; then
  echo "Error: ONEBOUND_API_KEY environment variable is not set." >&2
  echo "Please register on the Onebound platform, create an API key, and export it before using this skill." >&2
  exit 1
fi

PATH_SUFFIX="${1:?Error: path is required}"
TITLE="${2:?Error: title is required}"
shift 2

BASE_URL="${ONEBOUND_BASE_URL:-https://onebound.vercel.app}"

REQUEST_ARGS=()
for pair in "$@"; do
  REQUEST_ARGS+=(--data-urlencode "$pair")
done

RESPONSE=$(curl -sS -G -w "\n%{http_code}" "${BASE_URL}${PATH_SUFFIX}" \
  -H "Authorization: Bearer ${ONEBOUND_API_KEY}" \
  "${REQUEST_ARGS[@]}")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" != "200" ]; then
  echo "Error: API request failed (HTTP $HTTP_CODE)" >&2
  echo "$BODY" | jq -r '.reason // .error // .' >&2
  exit 1
fi

echo "## ${TITLE}"
echo ""
echo "**Gateway:** ${BASE_URL}${PATH_SUFFIX}"
echo ""
echo '```json'
echo "$BODY" | jq '.'
echo '```'
