#!/bin/bash

# GitHub Memory Sync - 定时备份脚本
# 添加到 crontab 实现自动备份

set -e

# 配置
WORKSPACE_DIR="${WORKSPACE_DIR:-/root/.openclaw/workspace}"
GITHUB_REPO="${GITHUB_REPO:-davinwang/openclaw-memory}"
GITHUB_BRANCH="${GITHUB_BRANCH:-main}"
GITHUB_TOKEN="${GITHUBTOKEN}"
SYNC_SCRIPT="/root/.openclaw/workspace/skills/github-memory-sync/sync.sh"
LOG_FILE="/var/log/openclaw-memory-sync.log"

# 检查配置
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ 错误：GITHUBTOKEN 未配置" | tee -a "$LOG_FILE"
    exit 1
fi

if [ ! -f "$SYNC_SCRIPT" ]; then
    echo "❌ 错误：同步脚本不存在：$SYNC_SCRIPT" | tee -a "$LOG_FILE"
    exit 1
fi

# 记录开始时间
echo "========================================" | tee -a "$LOG_FILE"
echo "开始备份：$(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "工作空间：$WORKSPACE_DIR" | tee -a "$LOG_FILE"
echo "GitHub 仓库：$GITHUB_REPO" | tee -a "$LOG_FILE"
echo "----------------------------------------" | tee -a "$LOG_FILE"

# 执行同步
export GITHUBTOKEN="$GITHUB_TOKEN"
export GITHUB_REPO="$GITHUB_REPO"
export GITHUB_BRANCH="$GITHUB_BRANCH"
export WORKSPACE_DIR="$WORKSPACE_DIR"
export SYNC_MODE="full"

cd "$(dirname "$SYNC_SCRIPT")"
bash "$SYNC_SCRIPT" push 2>&1 | tee -a "$LOG_FILE"

EXIT_CODE=$?

# 记录结束时间
echo "----------------------------------------" | tee -a "$LOG_FILE"
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ 备份成功：$(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
else
    echo "❌ 备份失败 (退出码：$EXIT_CODE)：$(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
fi
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

exit $EXIT_CODE
