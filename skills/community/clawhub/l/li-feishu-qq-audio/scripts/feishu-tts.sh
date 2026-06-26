#!/bin/bash
# 飞书语音发送脚本
# 用法：./feishu-tts.sh <音频文件> [用户 ID]
# 支持用户自定义目录配置

# 加载用户配置的环境变量
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -f "${SCRIPT_DIR}/.env" ]; then
    source "${SCRIPT_DIR}/.env"
fi

# 飞书配置（从环境变量或配置文件读取）
APP_ID="${FEISHU_APP_ID:-}"
APP_SECRET="${FEISHU_APP_SECRET:-}"
USER_ID="${2:-}"

# 如果未配置环境变量，尝试从 openclaw.json 读取
if [ -z "$APP_ID" ] || [ -z "$APP_SECRET" ]; then
    CONFIG_FILE="${OPENCLAW_CONFIG:-${HOME}/.openclaw/openclaw.json}"
    if [ -f "$CONFIG_FILE" ]; then
        APP_ID=$(cat "$CONFIG_FILE" | jq -r '.channels.feishu.appId // empty' 2>/dev/null)
        APP_SECRET=$(cat "$CONFIG_FILE" | jq -r '.channels.feishu.appSecret // empty' 2>/dev/null)
    fi
fi

# 检查配置
if [ -z "$APP_ID" ] || [ -z "$APP_SECRET" ]; then
    echo "错误：请配置飞书凭证"
    echo "方法 1: 设置环境变量"
    echo "  export FEISHU_APP_ID=\"cli_xxx\""
    echo "  export FEISHU_APP_SECRET=\"xxx\""
    echo "方法 2: 配置 openclaw.json"
    exit 1
fi

# 如果未指定用户 ID，提示错误
if [ -z "$USER_ID" ]; then
    echo "错误：请指定用户 ID"
    echo "用法：$0 <音频文件> <用户 open_id>"
    exit 1
fi

if [ -z "$1" ]; then
    echo "用法：$0 <音频文件> [用户 ID]"
    exit 1
fi

AUDIO_FILE="$1"

if [ ! -f "$AUDIO_FILE" ]; then
    echo "错误：文件不存在 - $AUDIO_FILE"
    exit 1
fi

# 转换为 OPUS 格式（飞书要求）
TEMP_DIR="${TEMP_DIR:-/tmp}"
OPUS_FILE="${TEMP_DIR}/feishu-audio-$(date +%s).opus"
ffmpeg -y -i "$AUDIO_FILE" -acodec libopus -ar 48000 -ac 1 "$OPUS_FILE" 2>/dev/null

if [ ! -f "$OPUS_FILE" ]; then
    echo "错误：音频格式转换失败"
    exit 1
fi

# 获取音频时长（毫秒）
DURATION_MS=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 "$OPUS_FILE" 2>/dev/null)
DURATION_MS=$(echo "$DURATION_MS * 1000" | bc | cut -d. -f1)
DURATION_MS=${DURATION_MS:-2000}

# 获取 access_token
TOKEN_URL="https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
ACCESS_TOKEN=$(curl -s -X POST "$TOKEN_URL" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" \
  | jq -r '.tenant_access_token')

if [ -z "$ACCESS_TOKEN" ] || [ "$ACCESS_TOKEN" = "null" ]; then
    echo "错误：获取 access_token 失败"
    rm -f "$OPUS_FILE"
    exit 1
fi

# 上传音频文件（飞书要求 file_type=opus）
UPLOAD_URL="https://open.feishu.cn/open-apis/im/v1/files"
UPLOAD_RESPONSE=$(curl -s -X POST "$UPLOAD_URL" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -F "file_type=opus" \
  -F "file=@$OPUS_FILE" \
  -F "file_name=tts.opus" \
  -F "duration=$DURATION_MS")

FILE_KEY=$(echo "$UPLOAD_RESPONSE" | jq -r '.data.file_key')

if [ -z "$FILE_KEY" ] || [ "$FILE_KEY" = "null" ]; then
    echo "错误：上传音频文件失败"
    echo "$UPLOAD_RESPONSE"
    rm -f "$OPUS_FILE"
    exit 1
fi

# 日志配置
LOG_DIR="${LOG_DIR:-/tmp/openclaw}"
LOG_FILE="${LOG_DIR}/feishu-tts-$(date +%Y-%m-%d).log"
mkdir -p "$LOG_DIR"

# 日志函数（输出到日志文件和 stderr）
log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$msg" >> "$LOG_FILE"
    echo "$msg" >&2
}

# 发送语音消息（msg_type=audio）
# content 必须是 JSON 字符串（需要转义）
CONTENT_ESCAPED=$(jq -n --arg fk "$FILE_KEY" --argjson dur "$DURATION_MS" '{file_key:$fk,duration:$dur}' | jq -Rs .)
SEND_URL="https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
SEND_RESPONSE=$(curl -s -X POST "$SEND_URL" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"$USER_ID\",\"msg_type\":\"audio\",\"content\":$CONTENT_ESCAPED}")

# 清理临时文件
rm -f "$OPUS_FILE"

# 检查结果
SEND_CODE=$(echo "$SEND_RESPONSE" | jq -r '.code')
if [ "$SEND_CODE" = "0" ]; then
    log "语音消息发送成功（用户：$USER_ID, 时长：${DURATION_MS}ms, 文件：$AUDIO_FILE）"
    echo "OK"
else
    log "错误：发送失败（用户：$USER_ID）"
    log "$SEND_RESPONSE"
    echo "ERROR: $SEND_RESPONSE" >&2
    exit 1
fi
