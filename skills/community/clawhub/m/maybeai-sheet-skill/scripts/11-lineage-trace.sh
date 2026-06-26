#!/usr/bin/env bash
# MaybeAI Sheet - Formula Lineage Trace
# Usage: export MAYBEAI_API_TOKEN=your_token_here
#        export DOC_ID=your_document_id_here
#        export TARGET_WORKSHEET=Report
#        export TARGET_CELL=C2
#        export FORMAT=tree
#        export BASE_URL=https://play-be.omnimcp.ai
#        bash scripts/11-lineage-trace.sh

set -uo pipefail

BASE_URL="${BASE_URL:-https://play-be.omnimcp.ai}"
TOKEN="${MAYBEAI_API_TOKEN:?Please set MAYBEAI_API_TOKEN}"
DOC_ID="${DOC_ID:-}"
DOC_URI="${DOC_URI:-}"
TARGET_WORKSHEET="${TARGET_WORKSHEET:-}"
TARGET_GID="${TARGET_GID:-}"
TARGET_CELL="${TARGET_CELL:?Please set TARGET_CELL, for example C2}"
FORMAT="${FORMAT:-tree}"

if [ -z "$DOC_ID" ] && [ -z "$DOC_URI" ]; then
  echo "Please set DOC_ID or DOC_URI" >&2
  exit 1
fi

if [ -z "$TARGET_WORKSHEET" ] && [ -z "$TARGET_GID" ]; then
  echo "Please set TARGET_WORKSHEET or TARGET_GID" >&2
  exit 1
fi

PAYLOAD_FILE="$(mktemp)"

cleanup() {
  rm -f "$PAYLOAD_FILE"
}
trap cleanup EXIT

if [ -n "$TARGET_GID" ]; then
  jq -n \
    --arg document_id "$DOC_ID" \
    --arg uri "$DOC_URI" \
    --argjson gid "$TARGET_GID" \
    --arg cell "$TARGET_CELL" \
    --arg format "$FORMAT" \
    '{
      document_id: $document_id,
      uri: $uri,
      targets: [
        {
          gid: $gid,
          cell: $cell
        }
      ],
      format: $format
    } | del(.document_id | select(. == "")) | del(.uri | select(. == ""))' > "$PAYLOAD_FILE"
else
  jq -n \
    --arg document_id "$DOC_ID" \
    --arg uri "$DOC_URI" \
    --arg worksheet_name "$TARGET_WORKSHEET" \
    --arg cell "$TARGET_CELL" \
    --arg format "$FORMAT" \
    '{
      document_id: $document_id,
      uri: $uri,
      targets: [
        {
          worksheet_name: $worksheet_name,
          cell: $cell
        }
      ],
      format: $format
    } | del(.document_id | select(. == "")) | del(.uri | select(. == ""))' > "$PAYLOAD_FILE"
fi

echo "=== Formula Lineage Trace ==="
curl -sS -X POST "$BASE_URL/api/v1/excel/lineage/trace" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  --data-binary "@$PAYLOAD_FILE" \
  | jq .
