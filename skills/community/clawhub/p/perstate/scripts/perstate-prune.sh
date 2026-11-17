#!/bin/bash
# perstate-prune.sh — 清理过期会话绑定、worktree 和无效分支
# 用法: perstate-prune.sh [Nd] [--execute]
#   Nd: 天数（如 30d），默认 30d
#   --execute: 实际执行清理（无此参数则只扫描输出待清理列表）

set -euo pipefail

# --- 参数解析 ---
DAYS_ARG="30d"
EXECUTE=false
CURRENT_SESSION=""
shift_next=false

for arg in "$@"; do
  case "$arg" in
    --execute) EXECUTE=true ;;
    --session-id) shift_next=true ;;
    [0-9]*d) DAYS_ARG="$arg" ;;
    *) [ "$shift_next" = "true" ] && CURRENT_SESSION="$arg" && shift_next=false ;;
  esac
done

DAYS="${DAYS_ARG%d}"

# 防护：0d 会删一切，拒绝执行
if [ "$DAYS" -eq 0 ] 2>/dev/null; then
  echo "错误: 0d 会删除所有 session/worktree/分支，拒绝执行。最小 1d。" >&2
  exit 1
fi
CONFIG=~/.perstate/config.yml

if [ ! -f "$CONFIG" ]; then
  echo "config.yml 不存在，无需清理。"
  exit 0
fi

NOW=$(date +%s)
CUTOFF=$(( NOW - DAYS * 86400 ))

# 读取默认分支（保护不删）
DEFAULT_BRANCH=$(grep "^default_branch:" "$CONFIG" | sed 's/^[^:]*: *//' || true)

# 当前 session 的安全转义
PRUNE_SID_SAFE=""
if [ -n "$CURRENT_SESSION" ]; then
  PRUNE_SID_SAFE=$(printf '%s' "$CURRENT_SESSION" | sed 's/[.[\*^$()+?{|\\]/\\&/g')
fi

# --- 读取 default_repo 确定 repo 目录 ---
DEFAULT_REPO=$(grep "^default_repo:" "$CONFIG" | sed 's/^[^:]*: *//' || true)
if [ -z "$DEFAULT_REPO" ]; then
  echo "default_repo 未配置，无法清理 worktree 和分支。"
  exit 1
fi

REPO_NAME=$(basename "$DEFAULT_REPO" .git)
BARE_REPO="$HOME/.perstate/$REPO_NAME.git"
WORKTREE_DIR="$HOME/.perstate/worktrees/$REPO_NAME"
# 规范化路径（macOS /tmp → /private/tmp 导致字符串比较不匹配）
BARE_REPO=$(cd "$BARE_REPO" 2>/dev/null && pwd -P || echo "$BARE_REPO")

CLEAN_COUNT=0

echo "═══════════════════════════════════════"
echo "  perstate 清理（${DAYS} 天前）"
echo "═══════════════════════════════════════"
echo ""

# --- 1. 过期会话绑定 ---
STALE_SESSIONS=""

# 提取所有 session ID（2 空格缩进 + ID + 冒号）
SESSION_IDS=$(grep "^  [a-zA-Z0-9_-]*:" "$CONFIG" | grep -v "^  -" | sed 's/^  \([a-zA-Z0-9_-]*\):.*/\1/' || true)

for SID in $SESSION_IDS; do
  # 跳过当前 session（保护不删）
  if [ "$SID" = "$CURRENT_SESSION" ]; then
    continue
  fi
  # Escape regex special chars in session ID for grep
  SID_SAFE=$(printf '%s' "$SID" | sed 's/[.[\*^$()+?{|\\]/\\&/g')
  # 读取 session 绑定的 branch
  BRANCH=$(grep -A1 "^  ${SID_SAFE}:" "$CONFIG" 2>/dev/null | grep "branch:" | sed 's/^[^:]*: *//' || true)
  [ -z "$BRANCH" ] && continue
  # 保护默认分支的 session
  if [ "$BRANCH" = "$DEFAULT_BRANCH" ]; then
    continue
  fi

  # 查 worktree 目录 mtime
  WT_PATH="$WORKTREE_DIR/$BRANCH"

  if [ -d "$WT_PATH" ]; then
    if [ "$(uname)" = "Darwin" ]; then
      MTIME=$(stat -f %m "$WT_PATH" 2>/dev/null || echo 0)
    else
      MTIME=$(stat -c %Y "$WT_PATH" 2>/dev/null || echo 0)
    fi
    LAST_DATE=$(date -r "$MTIME" "+%Y-%m-%d" 2>/dev/null || date -d "@$MTIME" "+%Y-%m-%d" 2>/dev/null || echo "unknown")
  else
    MTIME=0
    LAST_DATE="worktree 不存在"
  fi

  if [ "$MTIME" -lt "$CUTOFF" ]; then
    STALE_SESSIONS="${STALE_SESSIONS}${SID} (${LAST_DATE}, branch: ${BRANCH})"$'\n'
  fi
done

echo "── 会话绑定 ──"
if [ -n "$STALE_SESSIONS" ]; then
  echo "$STALE_SESSIONS" | while IFS= read -r line; do
    [ -n "$line" ] && echo "  - $line"
    CLEAN_COUNT=$((CLEAN_COUNT + 1))
  done
else
  echo "  无过期会话"
fi
echo ""

# --- 2. 过期 worktree ---
STALE_WORKTREES=""

if [ -d "$BARE_REPO" ]; then
  cd "$BARE_REPO"
  git worktree prune 2>/dev/null || true

  # 列出所有 worktree 路径
  WT_LIST=$(git worktree list --porcelain 2>/dev/null | grep "^worktree " | sed 's/^worktree //' || true)

  echo "$WT_LIST" | while IFS= read -r wt_path; do
    [ -z "$wt_path" ] && continue
    # 跳过主 clone 目录本身
    [ "$wt_path" = "$BARE_REPO" ] && continue
    # 保护默认分支的 worktree
    [ "$wt_path" = "$WORKTREE_DIR/$DEFAULT_BRANCH" ] && continue

    if [ -d "$wt_path" ]; then
      if [ "$(uname)" = "Darwin" ]; then
        WT_MTIME=$(stat -f %m "$wt_path" 2>/dev/null || echo 0)
      else
        WT_MTIME=$(stat -c %Y "$wt_path" 2>/dev/null || echo 0)
      fi
      WT_DATE=$(date -r "$WT_MTIME" "+%Y-%m-%d" 2>/dev/null || date -d "@$WT_MTIME" "+%Y-%m-%d" 2>/dev/null || echo "unknown")

      if [ "$WT_MTIME" -lt "$CUTOFF" ]; then
        echo "  - $wt_path (last modified: $WT_DATE)"
      fi
    fi
  done | grep -q "^  -" || true
fi

echo "── worktree ──"
if [ -d "$BARE_REPO" ]; then
  WT_FOUND=false
  while IFS= read -r wt_path; do
    [ -z "$wt_path" ] && continue
    [ "$wt_path" = "$BARE_REPO" ] && continue
    # 保护默认分支：不列入待清理，单独标注（与 execute 段的跳过逻辑一致）
    if [ "$wt_path" = "$WORKTREE_DIR/$DEFAULT_BRANCH" ]; then
      echo "  (受保护) $wt_path (默认分支)"
      continue
    fi
    if [ -d "$wt_path" ]; then
      if [ "$(uname)" = "Darwin" ]; then
        WT_MTIME=$(stat -f %m "$wt_path" 2>/dev/null || echo 0)
      else
        WT_MTIME=$(stat -c %Y "$wt_path" 2>/dev/null || echo 0)
      fi
      if [ "$WT_MTIME" -lt "$CUTOFF" ]; then
        WT_DATE=$(date -r "$WT_MTIME" "+%Y-%m-%d" 2>/dev/null || date -d "@$WT_MTIME" "+%Y-%m-%d" 2>/dev/null || echo "unknown")
        echo "  - $wt_path (last modified: $WT_DATE)"
        WT_FOUND=true
      fi
    fi
  done < <(git worktree list --porcelain 2>/dev/null | grep "^worktree " | sed 's/^worktree //')
  [ "$WT_FOUND" = false ] && echo "  无过期 worktree"
else
  echo "  仓库目录不存在"
fi
echo ""

# --- 3. 无效分支 ---
echo "── 无效分支 ──"
if [ -d "$BARE_REPO" ]; then
  cd "$BARE_REPO"
  # 确保 remote tracking ref 存在（bare clone 默认不生成）
  git config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*' 2>/dev/null || true
  git fetch origin 2>/dev/null || true
  BRANCH_FOUND=false

  # 用 for-each-ref 获取干净分支名（避免 +/* 前缀和词分裂）
  while IFS= read -r lb; do
    [ -z "$lb" ] && continue
    # 检查本地分支是否在远程存在
    if ! git show-ref --verify --quiet "refs/remotes/origin/$lb" 2>/dev/null; then
      echo "  - $lb (远程已删除)"
      BRANCH_FOUND=true
    fi
  done < <(git for-each-ref --format='%(refname:short)' refs/heads/ 2>/dev/null)
  [ "$BRANCH_FOUND" = false ] && echo "  无无效分支"
else
  echo "  仓库目录不存在"
fi
echo ""

# --- 4. 孤儿索引 ---
echo "── 孤儿索引 ──"
INDEX_DIR="$HOME/.perstate/.index"
ORPHAN_INDEX_FOUND=false
if [ -d "$INDEX_DIR" ] && [ -d "$BARE_REPO" ]; then
  for f in "$INDEX_DIR"/${REPO_NAME}__*.content; do
    [ -f "$f" ] || continue
    base=$(basename "$f")
    # 仅处理当前 repo 的索引（多 repo 共存，不碰别人的）
    idx_branch="${base#${REPO_NAME}__}"
    [ "$idx_branch" = "$base" ] && continue
    idx_branch="${idx_branch%.content}"
    # 该 branch 是否在 bare repo 仍存在？不存在 = 孤儿
    if ! git --git-dir="$BARE_REPO" show-ref --verify --quiet "refs/heads/$idx_branch" 2>/dev/null; then
      echo "  - $base (分支 $idx_branch 已不存在)"
      ORPHAN_INDEX_FOUND=true
    fi
  done
fi
[ "$ORPHAN_INDEX_FOUND" = false ] && echo "  无孤儿索引"
echo ""

# --- 执行清理 ---
if [ "$EXECUTE" = true ]; then
  echo "── 执行清理 ──"

  # 清理过期 session 绑定
  for SID in $SESSION_IDS; do
    SID_SAFE=$(printf '%s' "$SID" | sed 's/[.[\*^$()+?{|\\]/\\&/g')
    BRANCH=$(grep -A1 "^  ${SID_SAFE}:" "$CONFIG" 2>/dev/null | grep "branch:" | sed 's/^[^:]*: *//' || true)
    [ -z "$BRANCH" ] && continue

    WT_PATH="$WORKTREE_DIR/$BRANCH"

    if [ -d "$WT_PATH" ]; then
      if [ "$(uname)" = "Darwin" ]; then
        MTIME=$(stat -f %m "$WT_PATH" 2>/dev/null || echo 0)
      else
        MTIME=$(stat -c %Y "$WT_PATH" 2>/dev/null || echo 0)
      fi
    else
      MTIME=0
    fi

    if [ "$MTIME" -lt "$CUTOFF" ]; then
      # 用 awk 删除 session 条目
      awk -v sid="  ${SID_SAFE}:" '
        $0 ~ "^" sid { skip=1; next }
        skip && /^  [^ ]/ && $0 !~ "^" sid { skip=0 }
        skip && /^    / { next }
        skip { skip=0 }
        { print }
      ' "$CONFIG" > "$CONFIG.tmp" && mv "$CONFIG.tmp" "$CONFIG"
      echo "  已删除会话绑定: $SID"
    fi
  done

  # 清理过期 worktree
  if [ -d "$BARE_REPO" ]; then
    cd "$BARE_REPO"
    while IFS= read -r wt_path; do
      [ -z "$wt_path" ] && continue
      [ "$wt_path" = "$BARE_REPO" ] && continue
      # 保护默认分支的 worktree
      [ "$wt_path" = "$WORKTREE_DIR/$DEFAULT_BRANCH" ] && continue
      if [ -d "$wt_path" ]; then
        if [ "$(uname)" = "Darwin" ]; then
          WT_MTIME=$(stat -f %m "$wt_path" 2>/dev/null || echo 0)
        else
          WT_MTIME=$(stat -c %Y "$wt_path" 2>/dev/null || echo 0)
        fi
        if [ "$WT_MTIME" -lt "$CUTOFF" ]; then
          git worktree remove "$wt_path" --force 2>/dev/null && echo "  已移除 worktree: $wt_path" || echo "  移除失败: $wt_path"
        fi
      fi
    done < <(git worktree list --porcelain 2>/dev/null | grep "^worktree " | sed 's/^worktree //')
  fi

  # 清理无效分支
  if [ -d "$BARE_REPO" ]; then
    cd "$BARE_REPO"
    while IFS= read -r lb; do
      [ -z "$lb" ] && continue
      if ! git show-ref --verify --quiet "refs/remotes/origin/$lb" 2>/dev/null; then
        # 先尝试删除 worktree（分支可能被 worktree 占用导致 -d 拒绝）
        WT_FOR_BRANCH="$WORKTREE_DIR/$lb"
        if [ -d "$WT_FOR_BRANCH" ]; then
          git worktree remove "$WT_FOR_BRANCH" --force 2>/dev/null || true
        fi
        git branch -d "$lb" 2>/dev/null && echo "  已删除分支: $lb" || echo "  分支 $lb 未合并，跳过（用 git branch -D 强制删除）"
      fi
    done < <(git for-each-ref --format='%(refname:short)' refs/heads/ 2>/dev/null)
  fi

  # 清理孤儿索引（分支已不存在的 .content/.meta）
  if [ -d "$INDEX_DIR" ] && [ -d "$BARE_REPO" ]; then
    for f in "$INDEX_DIR"/${REPO_NAME}__*.content; do
      [ -f "$f" ] || continue
      base=$(basename "$f")
      idx_branch="${base#${REPO_NAME}__}"
      [ "$idx_branch" = "$base" ] && continue
      idx_branch="${idx_branch%.content}"
      if ! git --git-dir="$BARE_REPO" show-ref --verify --quiet "refs/heads/$idx_branch" 2>/dev/null; then
        rm -f "$f" "${f%.content}.meta"
        echo "  已删除孤儿索引: $base"
      fi
    done
  fi

  echo ""
  echo "清理完成。"
else
  echo "───"
  echo "以上为待清理项。确认后执行："
  echo "  scripts/perstate-prune.sh ${DAYS}d --execute"
fi

echo ""
echo "═══════════════════════════════════════"
