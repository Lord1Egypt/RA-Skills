#!/bin/bash
# Monday.com API helper for Accountability board
# Reads config from environment variables. Set these:
#   MONDAY_API_TOKEN  — your Monday.com API v2 token
#   MONDAY_BOARD_ID   — the board ID to operate on
#   MONDAY_COL_LAST_CHECKED — column ID for last-checked date (default: date_mm0y8p9j)
#   MONDAY_COL_STATUS       — column ID for status (default: color_mm0yr4nm)
set -euo pipefail

# Read token from env, then fallback to .env file
TOKEN="${MONDAY_API_TOKEN:-$(grep MONDAY_API_TOKEN ~/.openclaw/.env 2>/dev/null | cut -d= -f2 || echo '')}"
BOARD="${MONDAY_BOARD_ID:-}"
COL_LAST_CHECKED="${MONDAY_COL_LAST_CHECKED:-date_mm0y8p9j}"
COL_STATUS="${MONDAY_COL_STATUS:-color_mm0yr4nm}"
API="https://api.monday.com/v2"

if [ -z "$TOKEN" ]; then
  echo "Error: MONDAY_API_TOKEN not set and not found in ~/.openclaw/.env" >&2
  exit 1
fi

if [ -z "$BOARD" ]; then
  echo "Error: MONDAY_BOARD_ID not set. Pass it as env var or set it in your shell." >&2
  exit 1
fi

query() {
  curl -s -X POST "$API" \
    -H "Content-Type: application/json" \
    -H "Authorization: $TOKEN" \
    -d "{\"query\": \"$1\"}"
}

case "${1:-help}" in
  list)
    query "{ boards(ids: $BOARD) { items_page(limit: 50) { items { id name column_values { id text value } updates(limit: 3) { body created_at } } } } }" | jq .
    ;;
  update)
    ITEM_ID="$2"
    BODY="$3"
    query "mutation { create_update(item_id: $ITEM_ID, body: \"$BODY\") { id } }" | jq .
    ;;
  checked)
    ITEM_ID="$2"
    DATE=$(date +%Y-%m-%d)
    query "mutation { change_column_value(board_id: $BOARD, item_id: $ITEM_ID, column_id: \\\"$COL_LAST_CHECKED\\\", value: \\\"{\\\\\\\"date\\\\\\\":\\\\\\\"$DATE\\\\\\\"}\\\") { id } }" | jq .
    ;;
  status)
    ITEM_ID="$2"
    LABEL="$3"
    query "mutation { change_column_value(board_id: $BOARD, item_id: $ITEM_ID, column_id: \\\"$COL_STATUS\\\", value: \\\"{\\\\\\\"label\\\\\\\":\\\\\\\"$LABEL\\\\\\\"}\\\") { id } }" | jq .
    ;;
  *)
    echo "Usage: $0 {list|update <id> <html>|checked <id>|status <id> <label>}"
    echo ""
    echo "Environment variables:"
    echo "  MONDAY_API_TOKEN        (required) Monday.com API token"
    echo "  MONDAY_BOARD_ID         (required) Board ID"
    echo "  MONDAY_COL_LAST_CHECKED (optional) Last-checked column ID (default: date_mm0y8p9j)"
    echo "  MONDAY_COL_STATUS       (optional) Status column ID (default: color_mm0yr4nm)"
    ;;
esac
