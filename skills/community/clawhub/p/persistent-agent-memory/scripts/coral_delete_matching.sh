#!/usr/bin/env bash
# Coral Bricks persistent-agent-memory: delete memories matching a query.
# API endpoint: https://search-api.coralbricks.ai (Coral Bricks Memory API).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
HELPER="${SCRIPT_DIR}/json_encode.py"

QUERY="${1:?Usage: coral_delete_matching <query>}"
LIMIT=1

if [ -z "${CORAL_API_KEY:-}" ]; then
  echo '{"error": "CORAL_API_KEY is not set. Get one at https://coralbricks.ai"}' >&2
  exit 1
fi

# Memory API — delete by query (no ids exposed)
QUERY_JSON=$(printf '%s' "$QUERY" | python3 "$HELPER")
curl -s -X POST "https://search-api.coralbricks.ai/api/v1/memories/delete_matching" \
  -H "Authorization: Bearer ${CORAL_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"query\": ${QUERY_JSON}, \"limit\": ${LIMIT}}"
