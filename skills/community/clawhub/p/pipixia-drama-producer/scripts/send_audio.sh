#!/bin/bash
# send_audio.sh - Upload and send a voice message as playable audio in Feishu
# Usage: bash send_audio.sh "TTS text" <chat_id> [voice]
#
# Required env vars:
#   FEISHU_APP_ID     - Feishu app ID
#   FEISHU_APP_SECRET - Feishu app secret
# Optional env vars:
#   EDGE_TTS          - Path to edge-tts binary (default: node-edge-tts in PATH)

set -e

TEXT="$1"
CHAT_ID="$2"
VOICE="${3:-zh-CN-YunxiaNeural}"
TMP_AUDIO="/tmp/feishu_audio_$$.mp3"

TTS="${EDGE_TTS:-node-edge-tts}"

# Read credentials from environment variables
APP_ID="${FEISHU_APP_ID:?Error: FEISHU_APP_ID not set}"
APP_SECRET="${FEISHU_APP_SECRET:?Error: FEISHU_APP_SECRET not set}"

$TTS -t "$TEXT" -f "$TMP_AUDIO" -v "$VOICE" -l zh-CN

TOKEN=$(curl -sf -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['tenant_access_token'])")

FILE_KEY=$(curl -sf -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=opus" \
  -F "file_name=voice.mp3" \
  -F "file=@${TMP_AUDIO};type=audio/mpeg" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('data',{}).get('file_key','ERR'))")

curl -sf -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"$CHAT_ID\",\"msg_type\":\"audio\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"}" | python3 -c "import sys,json; d=json.load(sys.stdin); print('✅ Sent:', d.get('data',{}).get('message_id','?'))"

rm -f "$TMP_AUDIO"
