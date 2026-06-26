#!/usr/bin/env bash
# Coral Bricks persistent-agent-memory: store a memory.
# API endpoint: https://search-api.coralbricks.ai (Coral Bricks Memory API).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
HELPER="${SCRIPT_DIR}/json_encode.py"

TEXT="${1:?Usage: coral_store <text> [metadata_json]}"
METADATA_RAW="${2:-{}}"

if [ -z "${CORAL_API_KEY:-}" ]; then
  echo '{"error": "CORAL_API_KEY is not set. Get one at https://coralbricks.ai"}' >&2
  exit 1
fi

# Safely JSON-encode the text to handle quotes, newlines, and special characters
ESCAPED_TEXT=$(printf '%s' "$TEXT" | python3 "$HELPER")

# Validate metadata is valid JSON object; fall back to {} if not (prevents 422)
METADATA=$(printf '%s' "$METADATA_RAW" | python3 "$HELPER" --metadata 2>/dev/null || echo "{}")

# Memory API — simpler "remember this" interface
RESP=$(curl -s -X POST "https://search-api.coralbricks.ai/api/v1/memories" \
  -H "Authorization: Bearer ${CORAL_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"text\": ${ESCAPED_TEXT}, \"metadata\": ${METADATA}}")
echo "$RESP" | python3 "$HELPER" --store-response 2>/dev/null || echo "$RESP"
