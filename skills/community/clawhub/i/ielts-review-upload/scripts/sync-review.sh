#!/bin/bash
# sync-review.sh — Upload Skill-generated review data to the web backend
#
# Usage:
#   bash sync-review.sh <json-file> [--html review.html] [--bilingual bilingual.html]
#
# The JSON file must contain: book, test, passage, score, total
# Optional: band, date, timeSpent, wrongQuestions, errorCategories
#
# Multi-tenant: automatically generates a stable user ID from hostname + username.
# Each user gets their own data space on the web dashboard.
#
# Environment variables (or edit defaults below):
#   IELTS_API_BASE — API base URL (default: https://tuyaya.online/ielts-api)
#   IELTS_API_KEY  — API key for authentication
#   IELTS_USER_ID  — Override auto-generated user ID (optional)

set -e

# ─── Config ───
API_BASE="${IELTS_API_BASE:-https://tuyaya.online/ielts-api}"
API_KEY="${IELTS_API_KEY:-ielts_8b0832b3cfd38884e44ab26ee68acaeed294623ef8da9b201871a7768b072606}"

# ─── Generate stable user ID ───
# Uses SHA256 of (hostname + system username) for anonymity + determinism
if [[ -n "$IELTS_USER_ID" ]]; then
  USER_ID="$IELTS_USER_ID"
else
  RAW_ID="$(hostname)-$(whoami)"
  if command -v shasum &>/dev/null; then
    USER_ID=$(echo -n "$RAW_ID" | shasum -a 256 | cut -c1-16)
  elif command -v sha256sum &>/dev/null; then
    USER_ID=$(echo -n "$RAW_ID" | sha256sum | cut -c1-16)
  else
    # Fallback: use raw string (less ideal but functional)
    USER_ID=$(echo -n "$RAW_ID" | md5sum 2>/dev/null | cut -c1-16 || echo "$RAW_ID")
  fi
fi

# Display name: system username (not sensitive, just a friendly label)
USER_NAME="${IELTS_USER_NAME:-$(whoami)}"

# ─── Parse args ───
JSON_FILE=""
HTML_FILE=""
BILINGUAL_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --html)     HTML_FILE="$2"; shift 2 ;;
    --bilingual) BILINGUAL_FILE="$2"; shift 2 ;;
    -*)         echo "Unknown option: $1"; exit 1 ;;
    *)          JSON_FILE="$1"; shift ;;
  esac
done

if [[ -z "$JSON_FILE" ]]; then
  echo "Usage: bash sync-review.sh <data.json> [--html review.html] [--bilingual bilingual.html]"
  exit 1
fi

if [[ ! -f "$JSON_FILE" ]]; then
  echo "Error: file not found: $JSON_FILE"
  exit 1
fi

echo "=== Syncing review to web ==="
echo "  JSON: $JSON_FILE"
echo "  User: $USER_NAME ($USER_ID)"

# ─── Read JSON and optionally embed HTML content ───
PAYLOAD=$(cat "$JSON_FILE")

# If HTML files provided, embed their content into the JSON payload
if [[ -n "$HTML_FILE" && -f "$HTML_FILE" ]]; then
  echo "  HTML: $HTML_FILE"
  PAYLOAD=$(python3 -c "
import json, sys
data = json.loads(sys.argv[1])
with open(sys.argv[2], 'r') as f:
    data['reviewHtml'] = f.read()
print(json.dumps(data))
" "$PAYLOAD" "$HTML_FILE")
fi

if [[ -n "$BILINGUAL_FILE" && -f "$BILINGUAL_FILE" ]]; then
  echo "  Bilingual: $BILINGUAL_FILE"
  PAYLOAD=$(python3 -c "
import json, sys
data = json.loads(sys.argv[1])
with open(sys.argv[2], 'r') as f:
    data['bilingualHtml'] = f.read()
print(json.dumps(data))
" "$PAYLOAD" "$BILINGUAL_FILE")
fi

# Add source marker
PAYLOAD=$(python3 -c "
import json, sys
data = json.loads(sys.argv[1])
data['source'] = 'skill'
print(json.dumps(data))
" "$PAYLOAD")

# ─── Upload ───
echo "  Uploading to $API_BASE/skill-review ..."
RESPONSE=$(curl -s -w "\n%{http_code}" \
  -X POST "$API_BASE/skill-review" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -H "x-user-id: $USER_ID" \
  -H "x-user-name: $USER_NAME" \
  -d "$PAYLOAD")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]]; then
  echo "  ✅ Upload success ($HTTP_CODE): $BODY"
else
  echo "  ❌ Upload failed ($HTTP_CODE): $BODY"
  exit 1
fi

echo ""
echo "════════════════════════════════════════════"
echo "  📊 你的专属复盘看板："
echo "  $API_BASE/web/?user=$USER_ID&key=$API_KEY"
echo ""
echo "  💡 建议收藏这个链接，随时查看历史复盘记录"
echo "  🔑 你的用户 ID: $USER_ID"
echo "════════════════════════════════════════════"
