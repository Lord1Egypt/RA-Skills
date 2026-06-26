#!/usr/bin/env bash
# archive-to-wiki.sh — 将播客转录归档到飞书 Wiki
set -euo pipefail

TITLE="${1:?Usage: archive-to-wiki.sh --title TITLE --transcript FILE --space-id SPACE_ID}"
TRANSCRIPT_FILE=""
SPACE_ID=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --title) TITLE="$2"; shift 2 ;;
    --transcript) TRANSCRIPT_FILE="$2"; shift 2 ;;
    --space-id) SPACE_ID="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

: "${FEISHU_APP_ID:?FEISHU_APP_ID is required}"
: "${FEISHU_APP_SECRET:?FEISHU_APP_SECRET is required}"
: "${SPACE_ID:?--space-id is required}"
: "${TRANSCRIPT_FILE:?--transcript is required}"

# Get token
TOKEN=$(curl -s -X POST \
  'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"$FEISHU_APP_ID\",\"app_secret\":\"$FEISHU_APP_SECRET\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['tenant_access_token'])")

# Create page
RESULT=$(curl -s -X POST \
  "https://open.feishu.cn/open-apis/wiki/v2/spaces/$SPACE_ID/nodes" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"obj_type\":\"docx\",\"node_type\":\"origin\",\"title\":\"$TITLE\"}")

OBJ_TOKEN=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['node']['obj_token'])")
echo "Created page: obj_token=$OBJ_TOKEN"

# Write transcript
TRANSCRIPT=$(cat "$TRANSCRIPT_FILE" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")

curl -s -X POST \
  "https://open.feishu.cn/open-apis/docx/v1/documents/$OBJ_TOKEN/blocks/$OBJ_TOKEN/children" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"children\":[{\"block_type\":2,\"text\":{\"elements\":[{\"text_run\":{\"content\":$TRANSCRIPT}}]}}],\"index\":0}"

echo "Transcript archived to Wiki."
