#!/bin/bash
# send_video.sh - Upload and send a video as a Feishu media bubble
# Usage: bash send_video.sh <video.mp4> <cover.jpg> <chat_id>
#
# Required env vars:
#   FEISHU_APP_ID     - Feishu app ID
#   FEISHU_APP_SECRET - Feishu app secret
# Optional env vars:
#   FFPROBE           - Path to ffprobe (default: ffprobe in PATH)

set -e

VIDEO_FILE="$1"
COVER_FILE="$2"
CHAT_ID="$3"

if [ -z "$VIDEO_FILE" ] || [ -z "$COVER_FILE" ] || [ -z "$CHAT_ID" ]; then
  echo "Usage: bash send_video.sh <video.mp4> <cover.jpg> <chat_id>"
  exit 1
fi

# Read credentials from environment variables
APP_ID="${FEISHU_APP_ID:?Error: FEISHU_APP_ID not set}"
APP_SECRET="${FEISHU_APP_SECRET:?Error: FEISHU_APP_SECRET not set}"

echo "🔑 Getting token..."
TOKEN=$(curl -sf -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\": \"$APP_ID\", \"app_secret\": \"$APP_SECRET\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['tenant_access_token'])")

echo "🖼️  Uploading cover..."
IMAGE_KEY=$(curl -sf -X POST "https://open.feishu.cn/open-apis/im/v1/images" \
  -H "Authorization: Bearer $TOKEN" \
  -F "image_type=message" \
  -F "image=@${COVER_FILE}" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('data',{}).get('image_key','ERR'))")
echo "   image_key: $IMAGE_KEY"

echo "📹 Uploading video ($(basename $VIDEO_FILE))..."
FILE_KEY=$(curl -sf -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=mp4" \
  -F "file_name=$(basename $VIDEO_FILE)" \
  -F "file=@${VIDEO_FILE};type=video/mp4" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('data',{}).get('file_key','ERR'))")
echo "   file_key: $FILE_KEY"

FILENAME=$(basename "$VIDEO_FILE")
FFPROBE_BIN="${FFPROBE:-ffprobe}"
DURATION=$(python3 -c "
import subprocess, sys
r = subprocess.run(['$FFPROBE_BIN','-v','quiet','-show_entries','format=duration','-of','csv=p=0','$VIDEO_FILE'], capture_output=True, text=True)
print(int(float(r.stdout.strip())*1000) if r.stdout.strip() else 0)
" 2>/dev/null || echo 0)

echo "📨 Sending media message..."
RESULT=$(curl -sf -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"$CHAT_ID\",\"msg_type\":\"media\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\",\\\"image_key\\\":\\\"$IMAGE_KEY\\\",\\\"file_name\\\":\\\"$FILENAME\\\",\\\"duration\\\":$DURATION}\"}")
MSG_ID=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('data',{}).get('message_id','?'))" 2>/dev/null || echo "?")
echo "✅ Sent! message_id: $MSG_ID"
