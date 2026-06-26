#!/usr/bin/env bash
# MaybeAI Sheet - Workbook Profile
# Usage: export MAYBEAI_API_TOKEN=your_token_here
#        export DOC_ID=your_document_id_here
#        export FORCE_REFRESH=false
#        export BASE_URL=https://play-be.omnimcp.ai
#        bash scripts/10-workbook-profile.sh

set -u

BASE_URL="${BASE_URL:-https://play-be.omnimcp.ai}"
TOKEN="${MAYBEAI_API_TOKEN:?Please set MAYBEAI_API_TOKEN}"
DOC_ID="${DOC_ID:-}"
DOC_URI="${DOC_URI:-}"
FORCE_REFRESH="${FORCE_REFRESH:-false}"
MODEL="${MODEL:-}"

if [ -z "$DOC_ID" ] && [ -z "$DOC_URI" ]; then
  echo "Please set DOC_ID or DOC_URI" >&2
  exit 1
fi

PAYLOAD_FILE="$(mktemp)"

cleanup() {
  rm -f "$PAYLOAD_FILE"
}
trap cleanup EXIT

if [ -n "$MODEL" ]; then
  jq -n \
    --arg document_id "$DOC_ID" \
    --arg uri "$DOC_URI" \
    --argjson force_refresh "$FORCE_REFRESH" \
    --arg model "$MODEL" \
    '{
      document_id: $document_id,
      uri: $uri,
      force_refresh: $force_refresh,
      model: $model
    } | del(.document_id | select(. == "")) | del(.uri | select(. == ""))' > "$PAYLOAD_FILE"
else
  jq -n \
    --arg document_id "$DOC_ID" \
    --arg uri "$DOC_URI" \
    --argjson force_refresh "$FORCE_REFRESH" \
    '{
      document_id: $document_id,
      uri: $uri,
      force_refresh: $force_refresh
    } | del(.document_id | select(. == "")) | del(.uri | select(. == ""))' > "$PAYLOAD_FILE"
fi

echo "=== Workbook Profile ==="
curl -sS -X POST "$BASE_URL/api/v1/excel/workbook_profile" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  --data-binary "@$PAYLOAD_FILE" \
  | jq .
