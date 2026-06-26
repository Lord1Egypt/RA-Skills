#!/bin/bash
# 记忆系统自动提交脚本
# 功能：检测记忆文件变化，自动提交并推送到远程仓库

MEMORY_DIR="/home/claw/.openclaw/workspace/memory"
MAIN_FILE="/home/claw/.openclaw/workspace/MEMORY.md"
LOG_FILE="/home/claw/.openclaw/workspace/memory/state/sync.log"

# 确保日志目录存在
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 检查是否有变化
cd /home/claw/.openclaw/workspace

if git diff --quiet && git diff --cached --quiet; then
    log "No changes detected. Skipping commit."
    exit 0
fi

log "Changes detected. Preparing commit..."

# 添加所有变化
git add MEMORY.md memory/

# 生成提交信息
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
MESSAGE="Auto-sync memory at $TIMESTAMP"

# 提交
git commit -m "$MESSAGE"

# 推送到远程 (如果有配置)
if git remote -v | grep -q origin; then
    git push origin main 2>/dev/null && log "Pushed successfully." || log "Push failed (check remote config)."
else
    log "No remote configured. Commit only."
fi

log "Sync completed."
