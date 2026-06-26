#!/bin/bash
# send_reminder.sh  v2.1
# Quick helper to send a reminder from inside Docker to Mac.
#
# Usage:
#   ./send_reminder.sh "Buy milk"
#   ./send_reminder.sh "Call dentist" "2025-12-31 09:00" "Work"
#
# Requires: jq  (brew install jq  OR  apt install jq)
# Set BRIDGE_SECRET env var if auth is enabled on the listener.

set -euo pipefail

HOST="${BRIDGE_HOST:-http://host.docker.internal:5000}"
SECRET="${BRIDGE_SECRET:-}"
TASK="${1:-}"
DUE="${2:-}"
LIST="${3:-}"

if [ -z "$TASK" ]; then
  echo "Usage: $0 <task> [due: YYYY-MM-DD HH:MM] [list]" >&2
  exit 1
fi

# 🟡 Fix v2.1: use jq to build JSON — handles quotes, backslashes, newlines safely
if ! command -v jq &>/dev/null; then
  echo "Error: 'jq' is required. Install with: brew install jq  OR  apt install jq" >&2
  exit 1
fi

PAYLOAD=$(jq -n \
  --arg task "$TASK" \
  --arg due  "$DUE" \
  --arg list "$LIST" \
  '{task: $task} +
   (if $due  != "" then {due: $due}   else {} end) +
   (if $list != "" then {list: $list} else {} end)')

CURL_ARGS=(
  -s -w "\n%{http_code}"
  -X POST "$HOST/add_reminder"
  -H "Content-Type: application/json"
  -d "$PAYLOAD"
)

if [ -n "$SECRET" ]; then
  CURL_ARGS+=(-H "X-Bridge-Secret: $SECRET")
fi

RESPONSE=$(curl "${CURL_ARGS[@]}")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n -1)

echo "$BODY" | jq . 2>/dev/null || echo "$BODY"

if [ "$HTTP_CODE" != "200" ]; then
  echo "HTTP $HTTP_CODE" >&2
  exit 1
fi
