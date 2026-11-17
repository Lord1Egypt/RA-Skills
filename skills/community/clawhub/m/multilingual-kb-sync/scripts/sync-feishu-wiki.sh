#!/usr/bin/env bash
# sync-feishu-wiki.sh — Sync a markdown file to Feishu Wiki as a document.
#
# Usage:
#   sync-feishu-wiki.sh <file-path> [wiki-space-id] [parent-node-token]
#
# Environment:
#   FEISHU_APP_ID       — Feishu app ID (required)
#   FEISHU_APP_SECRET   — Feishu app secret (required)
#   FEISHU_WIKI_SPACE_ID — Default wiki space ID (optional, used if not passed as arg)
#
# Requirements: curl, jq

set -euo pipefail

FILE_PATH="${1:?Usage: $0 <file-path> [wiki-space-id] [parent-node-token]}"
SPACE_ID="${2:-${FEISHU_WIKI_SPACE_ID:-}}"
PARENT_TOKEN="${3:-}"

if [[ -z "$SPACE_ID" ]]; then
  echo "Error: wiki space ID required (pass as arg or set FEISHU_WIKI_SPACE_ID)" >&2
  exit 1
fi

if [[ ! -f "$FILE_PATH" ]]; then
  echo "Error: file not found: $FILE_PATH" >&2
  exit 1
fi

# --- 1. Get tenant access token ---
TOKEN_RESP=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"${FEISHU_APP_ID}\",\"app_secret\":\"${FEISHU_APP_SECRET}\"}")

TOKEN=$(echo "$TOKEN_RESP" | jq -r '.tenant_access_token')
if [[ -z "$TOKEN" || "$TOKEN" == "null" ]]; then
  echo "Error: failed to get tenant access token: $TOKEN_RESP" >&2
  exit 1
fi

# --- 2. Create wiki document ---
TITLE=$(grep -m1 '^# ' "$FILE_PATH" | sed 's/^# //')
TITLE="${TITLE:-Untitled Document}"

CREATE_PAYLOAD=$(jq -n \
  --arg space_id "$SPACE_ID" \
  --arg title "$TITLE" \
  --arg parent "$PARENT_TOKEN" \
  '{
    space_id: $space_id,
    title: $title,
    parent_node_token: ($parent | select(. != "") // empty)
  }')

CREATE_RESP=$(curl -s -X POST 'https://open.feishu.cn/open-apis/wiki/v2/spaces/.../nodes' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "$CREATE_PAYLOAD")

NODE_TOKEN=$(echo "$CREATE_RESP" | jq -r '.data.node.node_token // empty')
OBJ_TOKEN=$(echo "$CREATE_RESP" | jq -r '.data.node.obj_token // empty')

if [[ -z "$NODE_TOKEN" ]]; then
  echo "Error: failed to create wiki node: $CREATE_RESP" >&2
  exit 1
fi

echo "Created wiki node: $NODE_TOKEN (obj_token: $OBJ_TOKEN)"

# --- 3. Convert markdown to blocks and insert ---
# For simplicity, this creates a single text block with the raw markdown.
# For production, parse markdown and convert to Feishu block types:
#   https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document-block/create
CONTENT=$(cat "$FILE_PATH")
BLOCKS_PAYLOAD=$(jq -n \
  --arg text "$CONTENT" \
  '{
    children: [
      {
        block_type: 2,
        text: {
          elements: [{ text_run: { content: $text } }],
          style: {}
        }
      }
    ],
    index: 0
  }')

curl -s -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/${OBJ_TOKEN}/blocks/${OBJ_TOKEN}/children" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "$BLOCKS_PAYLOAD" | jq .

echo "✅ Synced to Feishu Wiki: https://open.feishu.cn/wiki/${NODE_TOKEN}"
