#!/usr/bin/env bash
# feishu_send_audio.sh — 将 WAV 音频转码为 opus 并发送到飞书
#                     Send WAV audio to Feishu as voice message (中文/English)
#
# 必需环境变量 / Required env vars:
#   FEISHU_APP_ID      飞书应用 App ID / Feishu app ID
#   FEISHU_APP_SECRET  飞书应用 App Secret / Feishu app secret
#
# 位置参数 / Positional args:
#   $1  音频文件路径（wav）/ Audio file path
#   $2  接收者 ID 类型 / Receiver ID type (open_id / chat_id)
#   $3  接收者 ID / Receiver ID
#
# 用法 / Usage:
#   bash feishu_send_audio.sh <audio.wav> <receive_id_type> <receive_id>
#
# 依赖 / Dependencies:
#   ffmpeg, curl, python3 (JSON 解析 / JSON parsing)
#
# 流程 / Flow: wav → opus (ffmpeg) → get tenant_access_token → upload file → send audio message

# ── 参数检查 ──────────────────────────────────────────────

if [[ $# -lt 3 ]]; then
  echo "用法 / Usage: $0 <audio.wav> <receive_id_type> <receive_id>" >&2
  exit 1
fi

AUDIO_FILE="$1"
if [[ ! -f "$AUDIO_FILE" ]]; then
  echo "错误 / Error: 文件不存在 / File not found — $AUDIO_FILE" >&2
  exit 1
fi

RECEIVE_ID_TYPE="$2"
FEISHU_RECEIVE_ID="$3"

for var in FEISHU_APP_ID FEISHU_APP_SECRET; do
  if [[ -z "${!var:-}" ]]; then
    echo "错误 / Error: 环境变量 / env var $var 未设置 / not set" >&2
    exit 1
  fi
done

# 临时文件目录
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

# ── Step 1: 转码 opus ────────────────────────────────────

OPUS_FILE="$TMP_DIR/voice.opus"
ffmpeg -y -i "$AUDIO_FILE" -c:a libopus -b:a 32k "$OPUS_FILE" 2>/dev/null

# ── Step 2: 获取 tenant_access_token ─────────────────────

TOKEN=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"$FEISHU_APP_ID\",\"app_secret\":\"$FEISHU_APP_SECRET\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['tenant_access_token'])")

# ── Step 3: 上传音频文件 ──────────────────────────────────

DURATION_MS=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OPUS_FILE" \
  | python3 -c "import sys; print(int(float(sys.stdin.read().strip())*1000))")

FILE_KEY=$(curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/files' \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=opus" -F "file_name=voice.opus" -F "duration=$DURATION_MS" \
  -F "file=@$OPUS_FILE" \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('data',{}).get('file_key',''))")

if [[ -z "$FILE_KEY" ]]; then
  echo "错误 / Error: 文件上传失败 / Upload failed，未获取到 file_key / no file_key returned" >&2
  exit 1
fi

# ── Step 4: 发送语音消息 ─────────────────────────────────

RESULT=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=$RECEIVE_ID_TYPE" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"receive_id\":\"$FEISHU_RECEIVE_ID\",\"msg_type\":\"audio\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"}")

echo "$RESULT"
