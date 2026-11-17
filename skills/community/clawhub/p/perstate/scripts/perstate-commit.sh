#!/bin/bash
# perstate-commit.sh — 写入后提交：git add + commit + push
# 用法: perstate-commit.sh --message "<summary>" --worktree <path>
# 用法: perstate-commit.sh --message "<summary>" --session-id <id>

set -euo pipefail

MESSAGE=""
WORKTREE=""
SESSION_ID=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --message)    MESSAGE="$2"; shift 2 ;;
    --worktree)   WORKTREE="$2"; shift 2 ;;
    --session-id) SESSION_ID="$2"; shift 2 ;;
    *) shift ;;
  esac
done

# Escape regex special chars in session ID for grep
SID_SAFE=$(printf '%s' "$SESSION_ID" | sed 's/[.[\*^$()+?{|\\]/\\&/g')

# 防护：--worktree 必须配合 --session-id 使用
if [ -n "$WORKTREE" ] && [ -z "$SESSION_ID" ]; then
  echo "错误: --worktree 必须配合 --session-id 使用，不能绕过会话绑定。" >&2
  exit 1
fi

if [ -z "$MESSAGE" ]; then
  MESSAGE="perstate: update knowledge graph"
fi

# --- 确定 worktree 路径 ---
if [ -z "$WORKTREE" ] && [ -n "$SESSION_ID" ]; then
  CONFIG=~/.perstate/config.yml
  REPO=$(grep "^default_repo:" "$CONFIG" | sed 's/^[^:]*: *//' || true)
  BRANCH=$(grep -A1 "^  ${SID_SAFE}:" "$CONFIG" 2>/dev/null | grep "branch:" | sed 's/^[^:]*: *//' || true)

  if [ -n "$REPO" ] && [ -n "$BRANCH" ]; then
    REPO_NAME=$(basename "$REPO" .git)
    WORKTREE="$HOME/.perstate/worktrees/$REPO_NAME/$BRANCH"
  fi
fi

if [ -z "$WORKTREE" ]; then
  echo "错误: 无法确定 worktree 路径。请通过 --worktree 或 --session-id 指定。" >&2
  exit 1
fi

cd "$WORKTREE"

# --- 提交并推送 ---
# git add -A 同时处理新增、修改、删除（原 git add . 不处理删除的文件）
git add -A

if git diff --cached --quiet; then
  echo "无变更需要提交。"
  exit 0
fi

git commit -m "$MESSAGE"

# 获取当前分支名（用于 rebase）
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# 更新同步缓存：本地已提交，标记为已同步（避免下次 prepare 重复 fetch）
SYNC_CACHE_DIR="$HOME/.perstate/.sync"
# 从 git remote 推导 repo name，与 prepare.sh 的缓存文件名保持一致
SYNC_REPO_NAME=$(basename "$(git remote get-url origin 2>/dev/null || echo "perstate.git")" .git)
SYNC_CACHE_FILE="$SYNC_CACHE_DIR/${SYNC_REPO_NAME}__${BRANCH}.cache"

# push with rebase-retry（不再吞掉错误）
if git push origin HEAD 2>&1; then
  echo "已推送到远程。"
  # push 成功后本地与远程一致，更新同步缓存
  mkdir -p "$SYNC_CACHE_DIR" 2>/dev/null
  date +%s > "$SYNC_CACHE_FILE" 2>/dev/null
else
  # push 失败，确保 bare repo 有 remote tracking refs
  git config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*' 2>/dev/null || true
  git fetch origin >&2 2>/dev/null || true
  # 检查是否 non-fast-forward
  if git merge-base --is-ancestor "origin/$BRANCH" HEAD 2>/dev/null; then
    # origin is ancestor of HEAD → not a fast-forward issue, real error
    echo "错误: push 失败（非 fast-forward 问题）。请手动检查。" >&2
    echo "Worktree 保留在 ${WORKTREE}。"
    exit 1
  fi
  # non-fast-forward → rebase and retry
  echo "远程有新提交，rebase 后重试..." >&2
  for i in 1 2 3; do
    git rebase "origin/$BRANCH" || {
      echo "错误: rebase 冲突。Worktree 保留在 ${WORKTREE} 供手动解决。" >&2
      exit 1
    }
    if git push origin HEAD 2>/dev/null; then
      echo "第 $i 次重试成功。"
      mkdir -p "$SYNC_CACHE_DIR" 2>/dev/null
      date +%s > "$SYNC_CACHE_FILE" 2>/dev/null
      break
    fi
    if [ "$i" -eq 3 ]; then
      echo "错误: push 3 次后仍失败。Worktree 保留在 ${WORKTREE}。" >&2
      exit 1
    fi
    git fetch origin >&2 2>/dev/null || true
  done
fi

echo "提交完成: $MESSAGE"
