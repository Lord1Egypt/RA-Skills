#!/usr/bin/env bash
# SECURITY MANIFEST:
# Environment variables accessed: MENGRAM_API_KEY (only)
# External endpoints called: https://mengram.io/v1/procedures/*/feedback (only)
# Local files read: none
# Local files written: none
set -euo pipefail

MENGRAM_BASE_URL="${MENGRAM_BASE_URL:-https://mengram.io}"
API_KEY="${MENGRAM_API_KEY:-}"

if [ -z "$API_KEY" ]; then
  echo "ERROR: MENGRAM_API_KEY not set. Get your free key at https://mengram.io"
  exit 1
fi

PROC_ID="${1:-}"
SUCCESS="${2:-true}"
CONTEXT="${3:-}"
FAILED_STEP="${4:-}"

if [ -z "$PROC_ID" ]; then
  echo "Usage: mengram-feedback.sh <procedure-id> [true|false] [context] [failed_at_step]"
  echo ""
  echo "Examples:"
  echo "  mengram-feedback.sh abc-123 true"
  echo "  mengram-feedback.sh abc-123 false \"OOM on step 3\" 3"
  exit 1
fi

# Build request body for failure with context
BODY=""
if [ "$SUCCESS" = "false" ] && [ -n "$CONTEXT" ]; then
  BODY=$(python3 -c "
import json, sys
body = {'context': sys.argv[1]}
if sys.argv[2]:
    body['failed_at_step'] = int(sys.argv[2])
print(json.dumps(body))
" "$CONTEXT" "$FAILED_STEP")
fi

if [ -n "$BODY" ]; then
  RESPONSE=$(curl -s -w "\n%{http_code}" \
    -X PATCH "${MENGRAM_BASE_URL}/v1/procedures/${PROC_ID}/feedback?success=${SUCCESS}" \
    -H "Authorization: Bearer ${API_KEY}" \
    -H "Content-Type: application/json" \
    -d "$BODY")
else
  RESPONSE=$(curl -s -w "\n%{http_code}" \
    -X PATCH "${MENGRAM_BASE_URL}/v1/procedures/${PROC_ID}/feedback?success=${SUCCESS}" \
    -H "Authorization: Bearer ${API_KEY}" \
    -H "Content-Type: application/json")
fi

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY_RESP=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -ne 200 ]; then
  echo "ERROR: Mengram API returned HTTP ${HTTP_CODE}"
  echo "$BODY_RESP"
  exit 1
fi

# Format output
python3 -c "
import json, sys

try:
    data = json.loads(sys.argv[1])
except json.JSONDecodeError:
    print('Feedback recorded.')
    sys.exit(0)

name = data.get('name', 'Unknown')
feedback = data.get('feedback', '')
success = data.get('success_count', 0)
fail = data.get('fail_count', 0)
evolved = data.get('evolution_triggered', False)

print(f'Procedure: {name}')
print(f'Feedback: {feedback} (success: {success}, fail: {fail})')
if evolved:
    print('EVOLUTION TRIGGERED: Procedure is being improved based on failure analysis.')
" "$BODY_RESP"
