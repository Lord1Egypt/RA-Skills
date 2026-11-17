#!/bin/bash
# ============================================================
# Project Daily Recap - 项目进度定时提醒
# 完全独立于 LLM，直接通过 openclaw CLI 推送到微信
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/config"
LOG_FILE="${SCRIPT_DIR}/reminder.log"

# ---------- 自动检测 Node.js ----------
detect_node() {
    # 优先级：nvm 中的 v22+ > PATH 中的 node
    if [ -s "$HOME/.nvm/nvm.sh" ]; then
        . "$HOME/.nvm/nvm.sh" 2>/dev/null
        NV=$(nvm which 22 2>/dev/null)
        [ -n "$NV" ] && [ -x "$NV" ] && { echo "$NV"; return 0; }
    fi
    local candidates=(
        "$HOME/.nvm/versions/node/v22.22.3/bin/node"
        "/usr/local/bin/node"
        "/usr/bin/node"
    )
    for c in "${candidates[@]}"; do
        [ -x "$c" ] && { echo "$c"; return 0; }
    done
    command -v node
}

NODE_CMD=$(detect_node)

# ---------- 确保 Node 和 openclaw 在 PATH ----------
export PATH="$(dirname "$NODE_CMD"):$HOME/.local/share/pnpm:/usr/local/bin:/usr/bin:$PATH"

# ---------- 加载配置 ----------
PROJECT_NAME="我的项目"
TODAY_PROGRESS=""
TOMORROW_PLAN=""
CHECKLIST="发了技术内容?,有客户沟通?,项目有推进?"
PUSH_HOUR=20
PUSH_MINUTE=0
WEIXIN_CHANNEL="openclaw-weixin"
WEIXIN_TARGET=""
WEIXIN_ACCOUNT=""

[ -f "$CONFIG_FILE" ] && source "$CONFIG_FILE"

# ---------- 生成消息 ----------
WEEKDAYS=("日" "一" "二" "三" "四" "五" "六")
WEEKDAY_INDEX=$(date +%w)
DATE_STR=$(date "+%Y-%m-%d")
WEEKDAY_CN=${WEEKDAYS[$WEEKDAY_INDEX]}

CHECKLIST_TEXT=""
IFS=',' read -ra ITEMS <<< "$CHECKLIST"
for item in "${ITEMS[@]}"; do
    item=$(echo "$item" | xargs)
    [ -n "$item" ] && CHECKLIST_TEXT="${CHECKLIST_TEXT}▶ ${item}
"
done

MESSAGE="📋 【${PROJECT_NAME}】进度复盘

📅 ${DATE_STR} 周${WEEKDAY_CN}

——— 今日复盘 ———
${CHECKLIST_TEXT}——— 明日计划 ———
明天准备干啥？想好了没？"

[ -n "$TODAY_PROGRESS" ] && MESSAGE="${MESSAGE}

📊 已记录进度：${TODAY_PROGRESS}"
[ -n "$TOMORROW_PLAN" ] && MESSAGE="${MESSAGE}
📌 明日计划：${TOMORROW_PLAN}"

# ---------- 日志 ----------
log_msg() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"; }

log_msg "🔄 发送提醒 | Node: $($NODE_CMD --version 2>/dev/null || echo '?')"

# ---------- 发送 ----------
SEND_CMD=(openclaw message send --message "$MESSAGE")
[ -n "$WEIXIN_TARGET" ]  && SEND_CMD+=(--target "$WEIXIN_TARGET")
[ -n "$WEIXIN_ACCOUNT" ] && SEND_CMD+=(--account "$WEIXIN_ACCOUNT")
[ -n "$WEIXIN_CHANNEL" ] && SEND_CMD+=(--channel "$WEIXIN_CHANNEL")

RESULT=$("${SEND_CMD[@]}" 2>&1) || {
    log_msg "❌ 发送失败: ${RESULT}"
    echo "[ERROR] ${RESULT}" >&2
    exit 1
}

log_msg "✅ 发送成功 → ${WEIXIN_TARGET:-当前会话}"
exit 0
