#!/usr/bin/env bash
# alert-sender.sh — 多渠道告警推送脚本
# 依赖：bash + curl + jq
# 用法：
#   ./scripts/alert-sender.sh send-feishu <title> <message> [webhook_url]
#   ./scripts/alert-sender.sh send-feishu-user <open_id> <title> <message>
#   ./scripts/alert-sender.sh check-all <config_file>

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
COOLDOWN_DIR="/tmp/monitor-cooldown"
mkdir -p "$COOLDOWN_DIR"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

# 检查告警降噪（cooldown）
check_cooldown() {
  local rule_name="$1"
  local cooldown="${2:-300}"
  local key
  key=$(echo "$rule_name" | tr ' /' '__')
  local cooldown_file="$COOLDOWN_DIR/$key"

  if [[ -f "$cooldown_file" ]]; then
    local last_time
    last_time=$(cat "$cooldown_file")
    local now
    now=$(date +%s)
    local elapsed=$(( now - last_time ))
    if (( elapsed < cooldown )); then
      log "告警降噪：[$rule_name] 距上次告警 ${elapsed}s，冷却期 ${cooldown}s，跳过"
      return 1
    fi
  fi
  date +%s > "$cooldown_file"
  return 0
}

# 发送飞书 Webhook 告警（群机器人）
send_feishu() {
  local title="$1"
  local message="$2"
  local webhook="${3:-${FEISHU_WEBHOOK:-}}"
  local level="${4:-warning}"

  if [[ -z "$webhook" ]]; then
    log "错误：未配置飞书 Webhook URL（FEISHU_WEBHOOK 环境变量或参数）"
    return 1
  fi

  # 根据告警级别设置颜色
  local color
  case "$level" in
    urgent)  color="red" ;;
    warning) color="orange" ;;
    *)       color="blue" ;;
  esac

  local payload
  payload=$(jq -n \
    --arg title "$title" \
    --arg message "$message" \
    --arg color "$color" \
    '{
      "msg_type": "interactive",
      "card": {
        "header": {
          "title": {"tag": "plain_text", "content": $title},
          "template": $color
        },
        "elements": [
          {
            "tag": "div",
            "text": {"tag": "lark_md", "content": $message}
          },
          {
            "tag": "note",
            "elements": [
              {"tag": "plain_text", "content": ("告警时间: " + (now | strftime("%Y-%m-%d %H:%M:%S")))}
            ]
          }
        ]
      }
    }')

  local response
  response=$(curl -s -X POST "$webhook" \
    -H "Content-Type: application/json" \
    -d "$payload")

  if echo "$response" | jq -e '.code == 0' > /dev/null 2>&1; then
    log "✅ 飞书告警发送成功: $title"
  else
    log "❌ 飞书告警发送失败: $response"
    return 1
  fi
}

# 发送飞书私信（需要飞书机器人 token）
send_feishu_user() {
  local open_id="$1"
  local title="$2"
  local message="$3"
  local token="${FEISHU_BOT_TOKEN:-}"

  if [[ -z "$token" ]]; then
    log "错误：未配置 FEISHU_BOT_TOKEN 环境变量"
    return 1
  fi

  local payload
  payload=$(jq -n \
    --arg open_id "$open_id" \
    --arg content "{\"text\":\"【$title】\n$message\"}" \
    '{
      "receive_id": $open_id,
      "msg_type": "text",
      "content": $content
    }')

  local response
  response=$(curl -s -X POST \
    "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
    -H "Authorization: Bearer $token" \
    -H "Content-Type: application/json" \
    -d "$payload")

  if echo "$response" | jq -e '.code == 0' > /dev/null 2>&1; then
    log "✅ 飞书私信发送成功: $open_id"
  else
    log "❌ 飞书私信发送失败: $response"
    return 1
  fi
}

# 根据告警级别路由推送渠道
route_alert() {
  local level="$1"
  local title="$2"
  local message="$3"
  local webhook="${4:-${FEISHU_WEBHOOK:-}}"

  case "$level" in
    urgent)
      log "紧急告警：$title"
      [[ -n "$webhook" ]] && send_feishu "$title" "🚨 **紧急告警**\n\n$message" "$webhook" "urgent"
      ;;
    warning)
      log "重要告警：$title"
      [[ -n "$webhook" ]] && send_feishu "$title" "⚠️ **重要告警**\n\n$message" "$webhook" "warning"
      ;;
    info)
      log "一般告警：$title"
      [[ -n "$webhook" ]] && send_feishu "$title" "ℹ️ **一般通知**\n\n$message" "$webhook" "blue"
      ;;
  esac
}

case "${1:-}" in
  send-feishu)
    send_feishu "${2:-}" "${3:-}" "${4:-}" "${5:-warning}"
    ;;
  send-feishu-user)
    send_feishu_user "${2:-}" "${3:-}" "${4:-}"
    ;;
  route)
    route_alert "${2:-warning}" "${3:-}" "${4:-}" "${5:-}"
    ;;
  check-all)
    # 由 AI 根据 config/monitor-config.yaml 生成具体检查逻辑
    log "check-all: 请根据配置文件实现具体检查逻辑"
    ;;
  *)
    echo "用法:"
    echo "  $0 send-feishu <title> <message> [webhook_url] [level]"
    echo "  $0 send-feishu-user <open_id> <title> <message>"
    echo "  $0 route <level> <title> <message> [webhook_url]"
    echo ""
    echo "  level: urgent | warning | info"
    exit 1
    ;;
esac
