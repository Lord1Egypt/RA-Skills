#!/bin/bash
# ============================================
# Git 自动提交并推送脚本
# ============================================

cd /home/admin/.openclaw/workspace

LOG_FILE="/home/admin/.openclaw/logs/git-auto-push.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查是否有变化
if git diff --quiet && git diff --cached --quiet; then
    # 无变化，退出
    exit 0
fi

log "🔄 检测到文件变化，开始提交..."

# 添加所有变化
git add -A

# 提交
COMMIT_MSG="🤖 auto: $(date '+%Y-%m-%d %H:%M')"
git commit -m "$COMMIT_MSG" --no-verify 2>&1 | tee -a "$LOG_FILE"

# 推送
log "⬆️  推送到 Gitee..."
git push origin main 2>&1 | tee -a "$LOG_FILE"

if [ $? -eq 0 ]; then
    log "✅ 推送成功"
else
    log "❌ 推送失败，尝试拉取后重试..."
    git pull --rebase origin main 2>&1 | tee -a "$LOG_FILE"
    git push origin main 2>&1 | tee -a "$LOG_FILE"
fi
