#!/bin/bash
# 每日摘要生成脚本
# 由 cron 每分钟检查一次，实现超时机制

WORKSPACE="/root/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
MARKER_FILE="$WORKSPACE/.daily-summary-pending"
TIMESTAMP_FILE="$WORKSPACE/.daily-summary-timestamp"
CONFIG_FILE="$WORKSPACE/.memory-workflow-config"
LOG_FILE="$WORKSPACE/logs/daily-summary.log"

# 读取配置
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
fi

# 默认值
DAILY_SUMMARY_HOUR=${DAILY_SUMMARY_HOUR:-23}
SUMMARY_TIMEOUT_MINUTES=${SUMMARY_TIMEOUT_MINUTES:-5}

DATE=$(date +%Y-%m-%d)
MEMORY_FILE="$MEMORY_DIR/$DATE.md"
TEMPLATE_FILE="$WORKSPACE/skills/memory-workflow/templates/daily-note-template.md"

# 确保日志目录存在
mkdir -p "$WORKSPACE/logs"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 步骤 1: 检查是否到了配置时间（每小时的第 0 分钟）
CURRENT_HOUR=$(date +%H)
CURRENT_MINUTE=$(date +%M)

if [ "$CURRENT_MINUTE" = "00" ] && [ "$CURRENT_HOUR" = "$DAILY_SUMMARY_HOUR" ]; then
    # 创建待处理标记
    echo "$DATE" > "$MARKER_FILE"
    date +%s > "$TIMESTAMP_FILE"
    log "Created pending marker for daily summary"
    exit 0
fi

# 步骤 2: 检查是否有待处理标记
if [ ! -f "$MARKER_FILE" ]; then
    exit 0
fi

# 步骤 3: 检查是否已存在今日笔记
if [ -f "$MEMORY_FILE" ]; then
    log "Daily summary already exists: $MEMORY_FILE"
    rm -f "$MARKER_FILE" "$TIMESTAMP_FILE"
    exit 0
fi

# 步骤 4: 检查超时
if [ -f "$TIMESTAMP_FILE" ]; then
    TIMESTAMP=$(cat "$TIMESTAMP_FILE")
    CURRENT_TS=$(date +%s)
    ELAPSED=$(( (CURRENT_TS - TIMESTAMP) / 60 ))
    
    if [ "$ELAPSED" -lt "$SUMMARY_TIMEOUT_MINUTES" ]; then
        # 还未超时，继续等待
        exit 0
    fi
fi

# 步骤 5: 超时，自动创建基础模板
log "Timeout reached, auto-creating daily summary"

# 使用模板或默认模板
if [ -f "$TEMPLATE_FILE" ]; then
    # 替换模板变量
    sed -e "s/{{DATE}}/$DATE/g" \
        -e "s/{{TIMESTAMP}}/$(date '+%Y-%m-%d %H:%M:%S')/g" \
        "$TEMPLATE_FILE" > "$MEMORY_FILE"
else
    # 默认模板
    cat > "$MEMORY_FILE" << TEMPLATE
# $DATE - 每日摘要

## 📋 今日重点
_待填充..._

## 💬 重要对话
_待填充..._

## 🎯 关键决策
_待填充..._

## 📝 待办更新
_待填充..._

---
*自动生成时间：$(date '+%Y-%m-%d %H:%M:%S')*
*记录者：[助手名称]*
TEMPLATE
fi

# 清理标记
rm -f "$MARKER_FILE" "$TIMESTAMP_FILE"
log "Auto-created daily summary: $MEMORY_FILE"

exit 0
