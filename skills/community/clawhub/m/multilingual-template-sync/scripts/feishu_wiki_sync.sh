#!/usr/bin/env bash
set -euo pipefail

# feishu_wiki_sync.sh — Sync a local Markdown file to Feishu Wiki
#
# Usage:
#   bash feishu_wiki_sync.sh --file <path> --space <space_id> --node <node_token>
#
# Environment:
#   FEISHU_APP_ID       — Feishu app ID
#   FEISHU_APP_SECRET   — Feishu app secret
#   FEISHU_BASE_URL     — API base URL (default: https://open.feishu.cn/open-apis)

FEISHU_BASE_URL="${FEISHU_BASE_URL:-https://open.feishu.cn/open-apis}"

usage() {
  echo "Usage: $0 --file <path> --space <space_id> --node <node_token>" >&2
  exit 1
}

FILE=""
SPACE_ID=""
NODE_TOKEN=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --file)  FILE="$2"; shift 2 ;;
    --space) SPACE_ID="$2"; shift 2 ;;
    --node)  NODE_TOKEN="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; usage ;;
  esac
done

[[ -z "$FILE" || -z "$SPACE_ID" || -z "$NODE_TOKEN" ]] && usage
[[ -f "$FILE" ]] || { echo "File not found: $FILE" >&2; exit 1; }

: "${FEISHU_APP_ID:?Set FEISHU_APP_ID}"
: "${FEISHU_APP_SECRET:?Set FEISHU_APP_SECRET}"

# 1. Obtain tenant access token
TOKEN=$(curl -s -X POST "${FEISHU_BASE_URL}/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"${FEISHU_APP_ID}\",\"app_secret\":\"${FEISHU_APP_SECRET}\"}" \
  | jq -r '.tenant_access_token')

if [[ -z "$TOKEN" || "$TOKEN" == "null" ]]; then
  echo "Failed to obtain tenant access token" >&2
  exit 1
fi

# 2. Read file content
CONTENT=$(cat "$FILE")

# 3. Create or update Wiki document
#    This is a simplified example — production use should convert Markdown
#    to Feishu Docx blocks via the docx API.
PAYLOAD=$(jq -n \
  --arg title "Common Responses" \
  --arg content "$CONTENT" \
  '{title: $title, content: $content}')

HTTP_CODE=$(curl -s -o /tmp/feishu_resp.json -w "%{http_code}" \
  -X POST "${FEISHU_BASE_URL}/wiki/v2/spaces/${SPACE_ID}/nodes/${NODE_TOKEN}/docs" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]]; then
  echo "✅ Synced $FILE to Feishu Wiki (node: $NODE_TOKEN)"
else
  echo "❌ Feishu sync failed (HTTP $HTTP_CODE)" >&2
  cat /tmp/feishu_resp.json >&2
  exit 1
fi
