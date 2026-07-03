#!/usr/bin/env bash
# MaybeAI Sheet — Permission And Sharing
# Usage:
#   export MAYBEAI_API_TOKEN=your_token_here
#   export BASE_URL=https://play-be.omnimcp.ai
#   export SHEET_ID=<document_id_or_sheet_url>
#   export EMAIL=user@example.com
#   bash scripts/10-permissions-sharing.sh

set -u

BASE_URL="${BASE_URL:-https://play-be.omnimcp.ai}"
TOKEN="${MAYBEAI_API_TOKEN:?Please set MAYBEAI_API_TOKEN}"
SHEET_ID="${SHEET_ID:?Please set SHEET_ID to a document id or sheet URL}"
EMAIL="${EMAIL:-}"

auth_json() {
  curl -sS -X POST "$1" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "$2" | jq .
}

echo "=== Query Current User Permission ==="
auth_json "$BASE_URL/api/v1/share/sheet/permission" \
  "{\"sheet_id\": \"$SHEET_ID\", \"gid\": null}"

echo "=== Set Public Viewer ==="
auth_json "$BASE_URL/api/v1/share/sheet/visibility" \
  "{\"sheet_id\": \"$SHEET_ID\", \"visibility\": \"public\", \"public_permission\": \"viewer\"}"

echo "=== Set Public Editor ==="
auth_json "$BASE_URL/api/v1/share/sheet/visibility" \
  "{\"sheet_id\": \"$SHEET_ID\", \"visibility\": \"public\", \"public_permission\": \"editor\"}"

echo "=== Set Private ==="
auth_json "$BASE_URL/api/v1/share/sheet/visibility" \
  "{\"sheet_id\": \"$SHEET_ID\", \"visibility\": \"private\"}"

echo "=== List Current Shares ==="
auth_json "$BASE_URL/api/v1/share/sheet/list" \
  "{\"sheet_id\": \"$SHEET_ID\"}"

if [ -n "$EMAIL" ]; then
  echo "=== Assign Viewer To Email ==="
  auth_json "$BASE_URL/api/v1/share/sheet/update-permission" \
    "{\"sheet_id\": \"$SHEET_ID\", \"email\": \"$EMAIL\", \"permission\": \"viewer\", \"gid\": null}"

  echo "=== Assign Editor To Email ==="
  auth_json "$BASE_URL/api/v1/share/sheet/update-permission" \
    "{\"sheet_id\": \"$SHEET_ID\", \"email\": \"$EMAIL\", \"permission\": \"editor\", \"gid\": null}"

  echo "=== Remove Email Access ==="
  auth_json "$BASE_URL/api/v1/share/sheet/remove-access" \
    "{\"sheet_id\": \"$SHEET_ID\", \"email\": \"$EMAIL\", \"gid\": null}"
else
  echo "EMAIL not set; skipping assign/remove examples."
fi
