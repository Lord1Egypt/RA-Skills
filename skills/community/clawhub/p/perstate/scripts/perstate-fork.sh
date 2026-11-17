#!/bin/bash
# perstate-fork.sh — 基于当前分支 fork 新分支并重新绑定
# 用法: perstate-fork.sh --name <new-branch> --session-id <id>

set -euo pipefail

NEW_BRANCH=""
SESSION_ID=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)       NEW_BRANCH="$2"; shift 2 ;;
    --session-id) SESSION_ID="$2"; shift 2 ;;
    *) shift ;;
  esac
done

# Escape regex special chars in session ID for grep
SID_SAFE=$(printf '%s' "$SESSION_ID" | sed 's/[.[\*^$()+?{|\\]/\\&/g')

if [ -z "$NEW_BRANCH" ]; then
  echo "用法: perstate-fork.sh --name <new-branch> --session-id <id>"
  exit 1
fi

CONFIG=~/.perstate/config.yml
if [ ! -f "$CONFIG" ]; then
  echo "错误: 配置文件不存在。请先执行 perstate-init.sh。" >&2
  exit 1
fi

# --- 读取当前 session 绑定的 branch ---
if [ -n "$SESSION_ID" ]; then
  CURRENT_BRANCH=$(grep -A1 "^  ${SID_SAFE}:" "$CONFIG" 2>/dev/null | grep "branch:" | sed 's/^[^:]*: *//' || true)
fi
CURRENT_BRANCH="${CURRENT_BRANCH:-$(grep "^default_branch:" "$CONFIG" | sed 's/^[^:]*: *//' || true)}"

if [ -z "$CURRENT_BRANCH" ]; then
  echo "错误: 无法确定当前分支。" >&2
  exit 1
fi

# --- 读取 repo ---
REPO=$(grep "^default_repo:" "$CONFIG" | sed 's/^[^:]*: *//' || true)
if [ -z "$REPO" ]; then
  echo "错误: default_repo 未配置。" >&2
  exit 1
fi

echo "当前分支: $CURRENT_BRANCH"
echo "新分支:   $NEW_BRANCH"

# --- 定位主 clone ---
REPO_NAME=$(basename "$REPO" .git)
BARE_REPO="$HOME/.perstate/$REPO_NAME.git"
NEW_WORKTREE="$HOME/.perstate/worktrees/$REPO_NAME/$NEW_BRANCH"

cd "$BARE_REPO"
git worktree prune
git fetch origin

# --- 创建新分支（基于最新当前分支）---
if git show-ref --verify --quiet "refs/heads/$NEW_BRANCH"; then
  echo "错误: 分支 '$NEW_BRANCH' 已存在。" >&2
  exit 1
fi

if git show-ref --verify --quiet "refs/remotes/origin/$CURRENT_BRANCH"; then
  git branch "$NEW_BRANCH" "origin/$CURRENT_BRANCH"
else
  git branch "$NEW_BRANCH" "$CURRENT_BRANCH"
fi
echo "已创建分支: $NEW_BRANCH (基于 $CURRENT_BRANCH)"

# --- 创建 worktree ---
if git worktree add "$NEW_WORKTREE" "$NEW_BRANCH" 2>/dev/null; then
  echo "worktree 已创建: $NEW_WORKTREE"
elif [ -d "$NEW_WORKTREE" ]; then
  echo "复用已有 worktree: $NEW_WORKTREE"
else
  echo "错误: 无法创建 worktree。" >&2
  exit 1
fi

# --- 更新 session 绑定 ---
if [ -n "$SESSION_ID" ]; then
  # 删除旧 session 绑定（用 awk 避免 sed 兼容问题）
  awk -v sid="  ${SID_SAFE}:" '
    $0 ~ "^" sid { skip=1; next }
    skip && /^  [^ ]/ && $0 !~ "^" sid { skip=0 }
    skip && /^    / { next }
    skip { skip=0 }
    { print }
  ' "$CONFIG" > "$CONFIG.tmp" && mv "$CONFIG.tmp" "$CONFIG"
  # 写入新绑定
  cat >> "$CONFIG" << EOF
  ${SESSION_ID}:
    branch: $NEW_BRANCH
EOF
  echo "session 绑定已更新: $SESSION_ID → $NEW_BRANCH"
fi

# --- 推送新分支 ---
git push origin "$NEW_BRANCH" 2>/dev/null && echo "已推送分支 $NEW_BRANCH" || echo "推送跳过（可能需要配置远程）"

# 设置正确的上游跟踪
git branch --set-upstream-to="origin/$NEW_BRANCH" "$NEW_BRANCH" 2>/dev/null || true

echo ""
echo "Fork 完成。"
echo "  原分支: $CURRENT_BRANCH"
echo "  新分支: $NEW_BRANCH"
echo "  worktree: $NEW_WORKTREE"
echo "  当前会话已绑定到新分支。"
