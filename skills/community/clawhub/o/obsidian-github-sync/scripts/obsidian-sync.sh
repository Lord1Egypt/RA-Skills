#!/bin/bash
# Obsidian Vault GitHub 同步脚本
# 
# 环境变量配置（必需）：
#   OBSIDIAN_VAULT_DIR    - Obsidian vault 本地路径
#   GITHUB_REMOTE_URL     - GitHub 远程仓库地址 (如: git@github.com:username/repo.git)
#
# 可选环境变量：
#   GIT_USER_NAME         - Git 用户名
#   GIT_USER_EMAIL        - Git 邮箱
#   SYNC_LOG_FILE         - 同步日志文件路径 (默认: /tmp/obsidian-sync.log)
#   CONFLICT_FLAG_FILE    - 冲突标记文件路径 (默认: /tmp/obsidian-sync-conflict.flag)

set -e

# 配置检查
if [ -z "$OBSIDIAN_VAULT_DIR" ]; then
    echo "ERROR: OBSIDIAN_VAULT_DIR environment variable not set"
    exit 1
fi

if [ -z "$GITHUB_REMOTE_URL" ]; then
    echo "ERROR: GITHUB_REMOTE_URL environment variable not set"
    exit 1
fi

# 默认值
SYNC_LOG_FILE="${SYNC_LOG_FILE:-/tmp/obsidian-sync.log}"
CONFLICT_FLAG_FILE="${CONFLICT_FLAG_FILE:-/tmp/obsidian-sync-conflict.flag}"

cd "$OBSIDIAN_VAULT_DIR" || {
    echo "ERROR: Cannot change to directory $OBSIDIAN_VAULT_DIR"
    exit 1
}

# 初始化 git（如果需要）
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git remote add origin "$GITHUB_REMOTE_URL"
fi

# 设置 git 用户信息（如果提供）
if [ -n "$GIT_USER_NAME" ]; then
    git config user.name "$GIT_USER_NAME"
fi
if [ -n "$GIT_USER_EMAIL" ]; then
    git config user.email "$GIT_USER_EMAIL"
fi

echo "=== Obsidian Sync started at $(date) ===" >> "$SYNC_LOG_FILE"

# 检查工作区是否有未提交的更改
if ! git diff --quiet HEAD 2>/dev/null || ! git diff --cached --quiet HEAD 2>/dev/null; then
    echo "Local changes detected, committing..." >> "$SYNC_LOG_FILE"
    git add -A
    git commit -m "Auto sync: $(date '+%Y-%m-%d %H:%M:%S')" >> "$SYNC_LOG_FILE" 2>&1 || true
fi

# 尝试 pull --rebase
echo "Pulling from GitHub with rebase..." >> "$SYNC_LOG_FILE"
if ! git pull --rebase origin master >> "$SYNC_LOG_FILE" 2>&1; then
    echo "ERROR: Pull rebase failed, possible conflict" >> "$SYNC_LOG_FILE"
    
    # 标记冲突状态
    echo "Conflict detected at $(date)" > "$CONFLICT_FLAG_FILE"
    echo "Repository: $OBSIDIAN_VAULT_DIR" >> "$CONFLICT_FLAG_FILE"
    echo "Remote: $GITHUB_REMOTE_URL" >> "$CONFLICT_FLAG_FILE"
    echo "" >> "$CONFLICT_FLAG_FILE"
    echo "To resolve:" >> "$CONFLICT_FLAG_FILE"
    echo "  1. cd $OBSIDIAN_VAULT_DIR" >> "$CONFLICT_FLAG_FILE"
    echo "  2. git status" >> "$CONFLICT_FLAG_FILE"
    echo "  3. Resolve conflict files" >> "$CONFLICT_FLAG_FILE"
    echo "  4. git add -A" >> "$CONFLICT_FLAG_FILE"
    echo "  5. git rebase --continue" >> "$CONFLICT_FLAG_FILE"
    echo "  6. git push" >> "$CONFLICT_FLAG_FILE"
    
    echo "Git sync conflict detected. Check $CONFLICT_FLAG_FILE for details."
    exit 1
fi

# 推送
echo "Pushing to GitHub..." >> "$SYNC_LOG_FILE"
if git push origin master >> "$SYNC_LOG_FILE" 2>&1; then
    echo "Sync completed successfully at $(date)" >> "$SYNC_LOG_FILE"
    rm -f "$CONFLICT_FLAG_FILE"
    exit 0
else
    echo "ERROR: Push failed" >> "$SYNC_LOG_FILE"
    exit 1
fi
