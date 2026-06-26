#!/bin/bash
# Auto-Create SubAgents - 定期检查并创建 pending 的子代理
# 注意：此脚本仅用于记录 pending 队列状态，实际创建由 Gateway 主流程处理
# 添加到 crontab: */5 * * * * ~/.openclaw/skills/multi-user-privacy/auto-create-subagents.sh

SKILL_DIR="$HOME/.openclaw/skills/multi-user-privacy"
PENDING_FILE="$SKILL_DIR/.pending-sessions.json"
LOG_FILE="$HOME/.openclaw/logs/subagent-create.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log "开始检查 pending sessions..."

if [ ! -f "$PENDING_FILE" ]; then
    log "✅ 没有 pending 的 sessions"
    exit 0
fi

# 读取 pending 队列
PENDING_COUNT=$(cat "$PENDING_FILE" | grep -c '"userId"' || echo "0")

if [ "$PENDING_COUNT" -eq 0 ]; then
    log "✅ pending 队列为空"
    exit 0
fi

log "发现 $PENDING_COUNT 个 pending sessions"
log "⚠️  注意：实际创建由 Gateway 主流程处理，此脚本仅记录状态"

# 输出 pending 队列状态
cat "$PENDING_FILE" >> "$LOG_FILE"

log "检查完成"
