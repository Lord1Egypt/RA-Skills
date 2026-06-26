#!/bin/bash
# 每周回顾脚本
# 由 cron 每周日 22:00 执行

WORKSPACE="/root/.openclaw/workspace"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
MEMORY_DIR="$WORKSPACE/memory"
CONFIG_FILE="$WORKSPACE/.memory-workflow-config"
LOG_FILE="$WORKSPACE/logs/weekly-review.log"

# 读取配置
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
fi

KEEP_DAYS=${KEEP_DAYS:-7}

mkdir -p "$WORKSPACE/logs"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log "=== 开始每周回顾 ==="

# 1. 清理过期的每日笔记
log "清理 ${KEEP_DAYS}天前的每日笔记..."
find "$MEMORY_DIR" -name "*.md" -type f -mtime +$KEEP_DAYS -exec rm -v {} \; >> "$LOG_FILE" 2>&1

# 2. 检查 MEMORY.md 是否存在
if [ ! -f "$MEMORY_FILE" ]; then
    log "⚠️  MEMORY.md 不存在，跳过回顾"
    exit 0
fi

# 3. 标记回顾时间
echo "" >> "$MEMORY_FILE"
echo "---" >> "$MEMORY_FILE"
echo "*本周回顾时间：$(date '+%Y-%m-%d %H:%M:%S')*" >> "$MEMORY_FILE"

log "✅ 每周回顾完成"
log "=== 每周回顾结束 ==="

exit 0
