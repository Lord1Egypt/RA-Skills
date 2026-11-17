#!/bin/bash
# perstate-switch.sh — 切换当前会话绑定的分支
# 用法: perstate-switch.sh --name <branch> --session-id <id>

set -euo pipefail

NAME=""
SESSION_ID=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)       NAME="$2"; shift 2 ;;
    --session-id) SESSION_ID="$2"; shift 2 ;;
    *) shift ;;
  esac
done

# Escape regex special chars in session ID for grep
SID_SAFE=$(printf '%s' "$SESSION_ID" | sed 's/[.[\*^$()+?{|\\]/\\&/g')

if [ -z "$NAME" ] || [ -z "$SESSION_ID" ]; then
  echo "用法: perstate-switch.sh --name <branch> --session-id <id>" >&2
  exit 1
fi

CONFIG=~/.perstate/config.yml
if [ ! -f "$CONFIG" ]; then
  echo "错误: config.yml 不存在。请先执行 /perstate init。" >&2
  exit 1
fi

# --- 读取 default_repo 确定 repo 目录 ---
DEFAULT_REPO=$(grep "^default_repo:" "$CONFIG" | sed 's/^[^:]*: *//' || true)
if [ -z "$DEFAULT_REPO" ]; then
  echo "错误: default_repo 未配置。" >&2
  exit 1
fi

REPO_NAME=$(basename "$DEFAULT_REPO" .git)
BARE_REPO="$HOME/.perstate/$REPO_NAME.git"

# --- 读取当前绑定的 branch ---
CURRENT_BRANCH=$(grep -A1 "^  ${SID_SAFE}:" "$CONFIG" 2>/dev/null | grep "branch:" | sed 's/^[^:]*: *//' || true)

# --- 幂等检查 ---
if [ "$CURRENT_BRANCH" = "$NAME" ]; then
  echo "已在 ${NAME}，无需切换。"
  exit 0
fi

# --- 校验目标分支存在 ---
cd "$BARE_REPO"
git fetch origin >&2 2>/dev/null || true

BRANCH_EXISTS=false
if git show-ref --verify --quiet "refs/heads/$NAME" 2>/dev/null; then
  BRANCH_EXISTS=true
elif git show-ref --verify --quiet "refs/remotes/origin/$NAME" 2>/dev/null; then
  # 远程存在，创建本地跟踪分支
  git branch "$NAME" "origin/$NAME" >&2
  BRANCH_EXISTS=true
fi

if [ "$BRANCH_EXISTS" = false ]; then
  echo "错误: 分支 '$NAME' 不存在。请先 /perstate fork $NAME 或 /perstate init。" >&2
  exit 1
fi

# --- 原地改写 config 绑定 ---
if [ -n "$CURRENT_BRANCH" ]; then
  # 替换现有 session 的 branch 值（用 | 作分隔符，避免分支名含 / 导致 sed 崩溃）
  if [ "$(uname)" = "Darwin" ]; then
    sed -i '' "/^  ${SID_SAFE}:/,/branch:/s|branch: .*|branch: ${NAME}|" "$CONFIG"
  else
    sed -i "/^  ${SID_SAFE}:/,/branch:/s|branch: .*|branch: ${NAME}|" "$CONFIG"
  fi
else
  # session 不存在，追加
  grep -q "^sessions:" "$CONFIG" 2>/dev/null || { echo "" >> "$CONFIG"; echo "sessions:" >> "$CONFIG"; }
  cat >> "$CONFIG" << EOF
  ${SESSION_ID}:
    branch: ${NAME}
EOF
fi

# --- 调 prepare 为目标分支创建/复用 worktree 并 pull ---
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
"$SCRIPT_DIR/perstate-prepare.sh" --session-id "$SESSION_ID" >&2 2>/dev/null || true

# --- 输出确认 ---
echo "已切换: ${CURRENT_BRANCH:-未绑定} → $NAME"
echo "worktree: $HOME/.perstate/worktrees/$REPO_NAME/$NAME"
