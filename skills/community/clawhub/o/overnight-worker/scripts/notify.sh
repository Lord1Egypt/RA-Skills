#!/usr/bin/env bash
# =============================================================================
# notify.sh — 多渠道通知脚本
# 支持: Telegram Bot API / macOS 本地通知 / Webhook (HTTP POST)
# 自动检测可用渠道，优雅降级
# =============================================================================

set -euo pipefail

# ---------- 默认值 ----------
CHANNEL=""
TITLE=""
BODY=""
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-}"
WEBHOOK_URL="${WEBHOOK_URL:-}"

# ---------- 使用说明 ----------
usage() {
    cat <<'USAGE'
用法: notify.sh --channel <渠道> --title <标题> --body <正文>

渠道:
  telegram    通过 Telegram Bot API 发送（需设置 TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID 环境变量）
  macos       macOS 本地通知（使用 osascript 或 terminal-notifier）
  webhook     通用 HTTP POST（需设置 WEBHOOK_URL 环境变量）
  auto        自动检测可用渠道（默认）

环境变量:
  TELEGRAM_BOT_TOKEN   Telegram Bot Token
  TELEGRAM_CHAT_ID     Telegram Chat ID
  WEBHOOK_URL          Webhook 目标 URL

示例:
  notify.sh --channel macos --title "任务完成" --body "3/3 步骤完成"
  notify.sh --channel auto --title "夜间任务" --body "详见 ~/overnight-output/"
USAGE
    exit 0
}

# ---------- 参数解析 ----------
while [[ $# -gt 0 ]]; do
    case "$1" in
        --channel) CHANNEL="$2"; shift 2 ;;
        --title)   TITLE="$2";   shift 2 ;;
        --body)    BODY="$2";    shift 2 ;;
        --help|-h) usage ;;
        *) echo "未知参数: $1"; usage ;;
    esac
done

# 默认渠道
[[ -z "$CHANNEL" ]] && CHANNEL="auto"

# 参数校验
if [[ -z "$TITLE" || -z "$BODY" ]]; then
    echo "错误: --title 和 --body 为必填参数"
    exit 1
fi

# ---------- 通知函数 ----------

# Telegram 通知
send_telegram() {
    if [[ -z "$TELEGRAM_BOT_TOKEN" || -z "$TELEGRAM_CHAT_ID" ]]; then
        echo "[TELEGRAM] 缺少 TELEGRAM_BOT_TOKEN 或 TELEGRAM_CHAT_ID 环境变量"
        return 1
    fi

    local message="*${TITLE}*
${BODY}"

    local response
    response=$(curl -s -w "\n%{http_code}" \
        -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d chat_id="${TELEGRAM_CHAT_ID}" \
        -d text="${message}" \
        -d parse_mode="Markdown" \
        2>&1)

    local http_code
    http_code=$(echo "$response" | tail -n1)
    local body
    body=$(echo "$response" | sed '$d')

    if [[ "$http_code" == "200" ]]; then
        echo "[TELEGRAM] 通知发送成功"
        return 0
    else
        echo "[TELEGRAM] 发送失败 (HTTP $http_code): $body"
        return 1
    fi
}

# macOS 本地通知
send_macos() {
    # 检查是否在 macOS 上
    if [[ "$(uname)" != "Darwin" ]]; then
        echo "[MACOS] 当前系统不是 macOS"
        return 1
    fi

    # 优先使用 terminal-notifier（功能更丰富）
    if command -v terminal-notifier &>/dev/null; then
        terminal-notifier \
            -title "$TITLE" \
            -message "$BODY" \
            -sound default \
            -group "overnight-worker" \
            2>&1
        echo "[MACOS] 通知已发送 (terminal-notifier)"
        return 0
    fi

    # 回退到 osascript
    if command -v osascript &>/dev/null; then
        # 转义双引号，防止注入
        local safe_title
        safe_title=$(echo "$TITLE" | sed 's/"/\\"/g')
        local safe_body
        safe_body=$(echo "$BODY" | sed 's/"/\\"/g')

        osascript -e "display notification \"${safe_body}\" with title \"${safe_title}\"" 2>&1
        echo "[MACOS] 通知已发送 (osascript)"
        return 0
    fi

    echo "[MACOS] 无可用的通知工具（需要 terminal-notifier 或 osascript）"
    return 1
}

# Webhook 通知 (通用 HTTP POST)
send_webhook() {
    if [[ -z "$WEBHOOK_URL" ]]; then
        echo "[WEBHOOK] 缺少 WEBHOOK_URL 环境变量"
        return 1
    fi

    local payload
    # 使用 jq 安全构造 JSON（防止标题/正文中的特殊字符导致注入）
    if command -v jq &>/dev/null; then
        payload=$(jq -n \
            --arg t "$TITLE" \
            --arg b "$BODY" \
            --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
            '{title:$t, body:$b, timestamp:$ts, source:"overnight-worker"}')
    else
        # jq 不可用时，手动转义双引号和反斜杠
        local safe_title safe_body
        safe_title=$(printf '%s' "$TITLE" | sed 's/\\/\\\\/g; s/"/\\"/g' | tr -d '\n')
        safe_body=$(printf '%s' "$BODY" | sed 's/\\/\\\\/g; s/"/\\"/g' | tr -d '\n')
        payload="{\"title\":\"${safe_title}\",\"body\":\"${safe_body}\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"source\":\"overnight-worker\"}"
    fi

    local response
    response=$(curl -s -w "\n%{http_code}" \
        -X POST "$WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d "$payload" \
        2>&1)

    local http_code
    http_code=$(echo "$response" | tail -n1)

    if [[ "$http_code" =~ ^2[0-9][0-9]$ ]]; then
        echo "[WEBHOOK] 通知发送成功 (HTTP $http_code)"
        return 0
    else
        echo "[WEBHOOK] 发送失败 (HTTP $http_code)"
        return 1
    fi
}

# ---------- 自动检测可用渠道 ----------
send_auto() {
    local sent=false

    # 优先 macOS 本地通知（最可靠）
    if [[ "$(uname)" == "Darwin" ]]; then
        if send_macos; then
            sent=true
        fi
    fi

    # 尝试 Telegram
    if [[ -n "$TELEGRAM_BOT_TOKEN" && -n "$TELEGRAM_CHAT_ID" ]]; then
        if send_telegram; then
            sent=true
        fi
    fi

    # 尝试 Webhook
    if [[ -n "$WEBHOOK_URL" ]]; then
        if send_webhook; then
            sent=true
        fi
    fi

    if [[ "$sent" == "false" ]]; then
        echo "[AUTO] 所有通知渠道均不可用，回退到标准输出:"
        echo "============================="
        echo "  $TITLE"
        echo "  $BODY"
        echo "============================="
        # 标准输出作为最终 fallback，不算失败
        return 0
    fi
}

# ---------- 路由到目标渠道 ----------
case "$CHANNEL" in
    telegram) send_telegram ;;
    macos)    send_macos ;;
    webhook)  send_webhook ;;
    auto)     send_auto ;;
    *)
        echo "未知渠道: $CHANNEL"
        echo "支持的渠道: telegram, macos, webhook, auto"
        exit 1
        ;;
esac
