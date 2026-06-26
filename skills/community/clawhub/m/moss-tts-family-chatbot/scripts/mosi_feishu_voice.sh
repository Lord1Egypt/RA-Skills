#!/bin/bash
# mosi_feishu_voice.sh
# One-shot: TTS → OPUS → upload to Feishu → send voice bubble.
# All intermediate files stay in ~/.openclaw/workspace/ automatically.
# The bot should call this script directly instead of managing files itself.
set -e

WORKSPACE="${HOME}/.openclaw/workspace"

usage() {
  cat <<EOF
Usage: $0 --text TEXT --chat-id CHAT_ID [options]

Options:
  --text,     -t  TEXT      Text to synthesize (required)
  --chat-id,  -c  CHAT_ID   Feishu chat_id to send voice bubble (required)
  --voice-id, -v  ID        Voice ID (default: 2001257729754140672 阿树)
  --api-key,  -k  KEY       Override MOSI_TTS_API_KEY env var

Example:
  $0 --text "你好，世界" --chat-id oc_xxxx
EOF
  exit 1
}

TEXT=""
CHAT_ID=""
VOICE_ID="2001257729754140672"
API_KEY="${MOSI_TTS_API_KEY}"

while [ $# -gt 0 ]; do
  case $1 in
    --text|-t)     TEXT="$2";     shift 2 ;;
    --chat-id|-c)  CHAT_ID="$2";  shift 2 ;;
    --voice-id|-v) VOICE_ID="$2"; shift 2 ;;
    --api-key|-k)  API_KEY="$2";  shift 2 ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

[ -z "$TEXT" ]    && echo "Error: --text required"    && usage
[ -z "$CHAT_ID" ] && echo "Error: --chat-id required" && usage
[ -z "$API_KEY" ] && echo "Error: MOSI_TTS_API_KEY not set" && exit 1

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WAV="${WORKSPACE}/tts_output.wav"
OPUS="${WORKSPACE}/tts_output.opus"

mkdir -p "$WORKSPACE"

# --- Step 1: TTS → WAV ---
echo "[1/5] Generating TTS..."
bash "${SKILL_DIR}/scripts/mosi_tts.sh" \
  --text "$TEXT" \
  --voice-id "$VOICE_ID" \
  --output "$WAV"

# --- Step 2: WAV → OPUS ---
echo "[2/5] Converting to OPUS..."
if ! which ffmpeg > /dev/null 2>&1; then
  echo "Error: ffmpeg not found. Install: apt-get install -y ffmpeg"
  exit 1
fi
ffmpeg -y -i "$WAV" -c:a libopus -b:a 32k "$OPUS" -loglevel error

# --- Step 3: Get duration (ms) ---
echo "[3/5] Getting duration..."
DURATION_MS=$(ffprobe -v error \
  -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 \
  "$OPUS" | awk '{printf "%d", $1 * 1000}')
echo "    Duration: ${DURATION_MS}ms"

# --- Step 4: Get Feishu token ---
echo "[4/5] Getting Feishu token..."
TOKEN=$(curl -sf -X POST \
  "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"${FEISHU_APP_ID}\",\"app_secret\":\"${FEISHU_APP_SECRET}\"}" \
| node -e "
  let d='';
  process.stdin.on('data',c=>d+=c);
  process.stdin.on('end',()=>{
    const r=JSON.parse(d);
    if (!r.tenant_access_token) {
      process.stderr.write('Token error: '+JSON.stringify(r)+'\n');
      process.exit(1);
    }
    process.stdout.write(r.tenant_access_token);
  });
")

# --- Step 5: Upload OPUS + send voice bubble ---
echo "[5/5] Uploading and sending voice bubble..."
FILE_KEY=$(curl -sf -X POST \
  "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer ${TOKEN}" \
  -F "file_type=opus" \
  -F "file_name=voice.opus" \
  -F "duration=${DURATION_MS}" \
  -F "file=@${OPUS}" \
| node -e "
  let d='';
  process.stdin.on('data',c=>d+=c);
  process.stdin.on('end',()=>{
    const r=JSON.parse(d);
    const key=r.data?.file_key||r.file_key;
    if (!key) {
      process.stderr.write('Upload error: '+JSON.stringify(r)+'\n');
      process.exit(1);
    }
    process.stdout.write(key);
  });
")

curl -sf -X POST \
  "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"receive_id\": \"${CHAT_ID}\",
    \"msg_type\": \"audio\",
    \"content\": \"{\\\"file_key\\\":\\\"${FILE_KEY}\\\"}\"
  }" > /dev/null

echo "Voice bubble sent. file_key=${FILE_KEY}"
