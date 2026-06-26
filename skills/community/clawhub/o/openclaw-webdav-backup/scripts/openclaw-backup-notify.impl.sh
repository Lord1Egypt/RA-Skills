#!/usr/bin/env bash
set -euo pipefail

STATUS="${1:-}"
MSG_FILE="${2:-}"

[[ -n "$STATUS" ]] || { echo "Usage: $0 <success|failure> <message-file>" >&2; exit 1; }
[[ -f "$MSG_FILE" ]] || { echo "Message file not found: $MSG_FILE" >&2; exit 1; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -n "${OPENCLAW_WORKSPACE_DIR:-}" ]]; then
  WORKSPACE_DIR="${OPENCLAW_WORKSPACE_DIR}"
else
  WORKSPACE_DIR="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
fi
STATE_DIR="${HOME}/.openclaw"
CONFIG_FILE="${STATE_DIR}/openclaw.json"
NOTIFY_ENV_FILE="${WORKSPACE_DIR}/.env.backup.notify"

log() { printf '[backup-notify] %s\n' "$*" ; }
has_cmd() { command -v "$1" >/dev/null 2>&1; }

# Save environment overrides before sourcing config file
BACKUP_NOTIFY_ENV="${BACKUP_NOTIFY:-}"
BACKUP_NOTIFY_CHANNEL_ENV="${BACKUP_NOTIFY_CHANNEL:-}"
BACKUP_NOTIFY_TELEGRAM_CHAT_ID_ENV="${BACKUP_NOTIFY_TELEGRAM_CHAT_ID:-}"
BACKUP_NOTIFY_TELEGRAM_BOT_TOKEN_ENV="${BACKUP_NOTIFY_TELEGRAM_BOT_TOKEN:-}"
BACKUP_NOTIFY_WECOM_KEY_ENV="${BACKUP_NOTIFY_WECOM_KEY:-}"
BACKUP_NOTIFY_WECOM_MENTION_ENV="${BACKUP_NOTIFY_WECOM_MENTION:-}"
BACKUP_NOTIFY_FEISHU_TOKEN_ENV="${BACKUP_NOTIFY_FEISHU_TOKEN:-}"
BACKUP_NOTIFY_FEISHU_SECRET_ENV="${BACKUP_NOTIFY_FEISHU_SECRET:-}"


if [[ -f "$NOTIFY_ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$NOTIFY_ENV_FILE"
fi

# Restore environment overrides (they take precedence over config file)
[[ -n "$BACKUP_NOTIFY_ENV" ]] && BACKUP_NOTIFY="$BACKUP_NOTIFY_ENV"
[[ -n "$BACKUP_NOTIFY_CHANNEL_ENV" ]] && BACKUP_NOTIFY_CHANNEL="$BACKUP_NOTIFY_CHANNEL_ENV"
[[ -n "$BACKUP_NOTIFY_TELEGRAM_CHAT_ID_ENV" ]] && BACKUP_NOTIFY_TELEGRAM_CHAT_ID="$BACKUP_NOTIFY_TELEGRAM_CHAT_ID_ENV"
[[ -n "$BACKUP_NOTIFY_TELEGRAM_BOT_TOKEN_ENV" ]] && BACKUP_NOTIFY_TELEGRAM_BOT_TOKEN="$BACKUP_NOTIFY_TELEGRAM_BOT_TOKEN_ENV"
[[ -n "$BACKUP_NOTIFY_WECOM_KEY_ENV" ]] && BACKUP_NOTIFY_WECOM_KEY="$BACKUP_NOTIFY_WECOM_KEY_ENV"
[[ -n "$BACKUP_NOTIFY_WECOM_MENTION_ENV" ]] && BACKUP_NOTIFY_WECOM_MENTION="$BACKUP_NOTIFY_WECOM_MENTION_ENV"
[[ -n "$BACKUP_NOTIFY_FEISHU_TOKEN_ENV" ]] && BACKUP_NOTIFY_FEISHU_TOKEN="$BACKUP_NOTIFY_FEISHU_TOKEN_ENV"
[[ -n "$BACKUP_NOTIFY_FEISHU_SECRET_ENV" ]] && BACKUP_NOTIFY_FEISHU_SECRET="$BACKUP_NOTIFY_FEISHU_SECRET_ENV"

# Set defaults for unset variables
BACKUP_NOTIFY="${BACKUP_NOTIFY:-0}"
BACKUP_NOTIFY_CHANNEL="${BACKUP_NOTIFY_CHANNEL:-telegram}"

# Telegram settings
BACKUP_NOTIFY_TELEGRAM_CHAT_ID="${BACKUP_NOTIFY_TELEGRAM_CHAT_ID:-}"
BACKUP_NOTIFY_TELEGRAM_BOT_TOKEN="${BACKUP_NOTIFY_TELEGRAM_BOT_TOKEN:-}"

# WeCom (企业微信) settings
BACKUP_NOTIFY_WECOM_KEY="${BACKUP_NOTIFY_WECOM_KEY:-}"
BACKUP_NOTIFY_WECOM_MENTION="${BACKUP_NOTIFY_WECOM_MENTION:-}"

# Feishu (飞书) settings
BACKUP_NOTIFY_FEISHU_TOKEN="${BACKUP_NOTIFY_FEISHU_TOKEN:-}"
BACKUP_NOTIFY_FEISHU_SECRET="${BACKUP_NOTIFY_FEISHU_SECRET:-}"

if [[ "${BACKUP_NOTIFY:-0}" != "1" ]]; then
  log 'BACKUP_NOTIFY not enabled; skip'
  exit 0
fi

send_telegram() {
  local text
  text="$(cat "$MSG_FILE")"
  if [[ -z "${BACKUP_NOTIFY_TELEGRAM_BOT_TOKEN:-}" && -f "$CONFIG_FILE" ]]; then
    if has_cmd jq; then
      BACKUP_NOTIFY_TELEGRAM_BOT_TOKEN="$(jq -r '.channels.telegram.botToken // .channels.telegram.accounts.default.botToken // empty' "$CONFIG_FILE")"
    fi
  fi
  if [[ -z "${BACKUP_NOTIFY_TELEGRAM_BOT_TOKEN:-}" ]]; then
    log 'Telegram bot token not configured; skip'
    return 0
  fi
  if [[ -z "${BACKUP_NOTIFY_TELEGRAM_CHAT_ID:-}" ]]; then
    log 'Telegram chat id not configured; skip'
    return 0
  fi
  has_cmd curl || { log 'curl not installed; skip'; return 0; }
  curl --silent --show-error --fail \
    -X POST "https://api.telegram.org/bot${BACKUP_NOTIFY_TELEGRAM_BOT_TOKEN}/sendMessage" \
    --data-urlencode "chat_id=${BACKUP_NOTIFY_TELEGRAM_CHAT_ID}" \
    --data-urlencode "text=${text}" \
    >/dev/null
}

# Generate WeCom (企业微信) mention list
wecom_build_mentioned() {
  local mentioned=""
  if [[ -n "${BACKUP_NOTIFY_WECOM_MENTION:-}" ]]; then
    IFS=',' read -ra mobiles <<< "$BACKUP_NOTIFY_WECOM_MENTION"
    mentioned_list="["
    first=1
    for mobile in "${mobiles[@]}"; do
      [[ -n "$mobile" ]] || continue
      if [[ $first -eq 1 ]]; then
        first=0
      else
        mentioned_list+=","
      fi
      mentioned_list+="\"$mobile\""
    done
    mentioned_list+="]"
    mentioned="\"mentioned_mobile_list\": $mentioned_list,"
  fi
  echo "$mentioned"
}

send_wecom() {
  local text content
  text="$(cat "$MSG_FILE")"
  if [[ -z "${BACKUP_NOTIFY_WECOM_KEY:-}" ]]; then
    log 'WeCom webhook key not configured; skip'
    return 0
  fi
  has_cmd curl || { log 'curl not installed; skip'; return 0; }
  has_cmd jq || { log 'jq not installed; skip'; return 0; }
  
  local mentioned
  mentioned=$(wecom_build_mentioned)
  
  # Escape text for JSON
  # Escape text for JSON using printf to handle special chars
  content=$(printf '%s' "$text" | jq -Rs '.')
  
  local json_payload
  if [[ -n "$mentioned" ]]; then
    json_payload="{\"msgtype\": \"text\", \"text\": {\"content\": $content}, $mentioned \"safe\":0}"
  else
    json_payload="{\"msgtype\": \"text\", \"text\": {\"content\": $content}, \"safe\":0}"
  fi
  
  curl --silent --show-error --fail \
    -X POST "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=${BACKUP_NOTIFY_WECOM_KEY}" \
    -H "Content-Type: application/json" \
    -d "$json_payload" \
    >/dev/null
}

# Generate Feishu (飞书) signature if secret is configured
feishu_gen_sign() {
  local secret="$1"
  local timestamp
  timestamp=$(date +%s)
  local string_to_sign="${timestamp}\n${secret}"
  local sign
  sign=$(echo -n "$string_to_sign" | openssl sha256 -binary | base64)
  echo "{\"timestamp\": $timestamp, \"sign\": \"$sign\"}"
}

send_feishu() {
  local text content
  text="$(cat "$MSG_FILE")"
  if [[ -z "${BACKUP_NOTIFY_FEISHU_TOKEN:-}" ]]; then
    log 'Feishu webhook token not configured; skip'
    return 0
  fi
  has_cmd curl || { log 'curl not installed; skip'; return 0; }
  has_cmd jq || { log 'jq not installed; skip'; return 0; }
  
  # Escape text for JSON using printf to handle special chars
  content=$(printf '%s' "$text" | jq -Rs '.')
  
  local json_payload
  json_payload="{\"msg_type\": \"text\", \"content\": {\"text\": $content}}"
  
  # Add signature if secret is configured
  if [[ -n "${BACKUP_NOTIFY_FEISHU_SECRET:-}" ]]; then
    has_cmd openssl || { log 'openssl not installed; skip signature'; return 0; }
    local sign_data
    sign_data=$(feishu_gen_sign "$BACKUP_NOTIFY_FEISHU_SECRET")
    json_payload=$(echo "$json_payload" | jq --argjson sign "$sign_data" '. + $sign')
  fi
  
  curl --silent --show-error --fail \
    -X POST "https://open.feishu.cn/open-apis/bot/v2/hook/${BACKUP_NOTIFY_FEISHU_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "$json_payload" \
    >/dev/null
}

case "$BACKUP_NOTIFY_CHANNEL" in
  telegram)
    send_telegram
    ;;
  wecom|weixin|wechat|qyweixin)
    send_wecom
    ;;
  feishu|lark)
    send_feishu
    ;;
  *)
    log "Unknown notify channel: $BACKUP_NOTIFY_CHANNEL; skip"
    ;;
esac
