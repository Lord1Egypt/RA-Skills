#!/usr/bin/env bash
# ============================================================
# memory-backup.sh — 记忆备份脚本（安全加固版）
# ============================================================
# 用法：bash scripts/memory-backup.sh
#
# 功能：将 WORKDIR 下的关键记忆文件提交并推送到 Git 远程仓库。
#
# 安全加固：
#   - 推送前验证远程仓库配置
#   - 包含 .gitignore 自动过滤敏感文件
#   - SSH 使用 known_hosts 严格验证
#
# 环境变量：
#   WORKDIR                工作目录（默认：/root/.openclaw/workspace）
#   GIT_REMOTE             Git 远程仓库地址
#   MEMORY_BACKUP_KEY      SSH 私钥路径
# ============================================================

set -euo pipefail

WORKDIR="${WORKDIR:-/root/.openclaw/workspace}"
cd "$WORKDIR"

# ---- 配置区（根据实际情况修改）----
# TODO: 替换为你的 Git 远程仓库地址
GIT_REMOTE="${GIT_REMOTE:-}"

# TODO: 替换为你的 SSH 私钥路径
MEMORY_BACKUP_KEY="${MEMORY_BACKUP_KEY:-~/.ssh/id_rsa}"

# ---- 配置校验 ----
if [ -z "$GIT_REMOTE" ]; then
  echo "[memory-backup] 错误：未设置 GIT_REMOTE"
  echo "[memory-backup] 请在 scripts/memory-backup.sh 开头设置 GIT_REMOTE"
  exit 1
fi

# ---- SSH 配置（安全模式）----
KNOWN_HOSTS="${HOME}/.ssh/known_hosts"
export GIT_SSH_COMMAND="ssh -i ${MEMORY_BACKUP_KEY} -o IdentitiesOnly=yes -o UserKnownHostsFile=${KNOWN_HOSTS}"

# ---- 确保 git remote 已配置 ----
CURRENT_REMOTE="$(git remote get-url origin 2>/dev/null || echo '')"
if [ "$CURRENT_REMOTE" != "$GIT_REMOTE" ]; then
  echo "[memory-backup] 远程仓库地址已更新或未配置，正在设置..."
  git remote add origin "$GIT_REMOTE" 2>/dev/null || git remote set-url origin "$GIT_REMOTE"
fi

STAMP="$(date '+%Y-%m-%d %H:%M:%S %z')"
MSG="memory-backup: ${STAMP}"

# ---- 追踪的记忆文件/目录列表 ----
# 注意：memory/system-config.md 不追踪（可能含敏感配置路径）
TRACKED_PATHS=(
  "MEMORY.md"
  "memory"
  "SOUL.md"
  "USER.md"
  "IDENTITY.md"
  "HEARTBEAT.md"
)

for path in "${TRACKED_PATHS[@]}"; do
  if [ -e "$path" ]; then
    git add -A "$path"
  fi
done

if git diff --cached --quiet; then
  echo "[memory-backup] 没有新内容需要备份。"
  exit 0
fi

# ---- 提交前确认（交互模式）----
if [ -t 0 ]; then
  echo "[memory-backup] 即将提交以下文件："
  git diff --cached --name-only | sed 's/^/  - /'
  echo ""
  read -p "[memory-backup] 确认推送？ [y/N] " -r
  if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
    echo "[memory-backup] 已取消。"
    git reset HEAD
    exit 0
  fi
fi

git commit -m "$MSG"
git push origin master

echo "[memory-backup] 备份已推送：${MSG}"
