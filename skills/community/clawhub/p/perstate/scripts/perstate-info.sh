#!/bin/bash
# perstate-info.sh — 查看配置、会话和统计信息
# 用法: perstate-info.sh [--session-id <id>] [--worktree <path>] [--status]
# --status: 仅显示配置和会话状态（不显示记忆统计），用于 /perstate 默认命令

set -euo pipefail

WORKTREE=""
SESSION_ID=""
STATUS_ONLY=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --worktree)   WORKTREE="$2"; shift 2 ;;
    --session-id) SESSION_ID="$2"; shift 2 ;;
    --status)     STATUS_ONLY=true; shift ;;
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

CONFIG=~/.perstate/config.yml

echo "═══════════════════════════════════════"
echo "  perstate 信息"
echo "═══════════════════════════════════════"

# --- 1. 初始化配置 ---
echo ""
echo "── 初始化配置 ──"
if [ ! -f "$CONFIG" ]; then
  echo "  状态: 未初始化（config 不存在）"
  echo "  提示: 请先执行 /perstate init"
else
  DEFAULT_REPO=$(grep "^default_repo:" "$CONFIG" | sed 's/^[^:]*: *//' || true)
  DEFAULT_BRANCH=$(grep "^default_branch:" "$CONFIG" | sed 's/^[^:]*: *//' || true)
  echo "  默认仓库: ${DEFAULT_REPO:-未配置}"
  echo "  默认分支: ${DEFAULT_BRANCH:-未配置}"
fi

# --- 2. 当前会话信息 ---
echo ""
echo "── 当前会话 ──"
if [ -n "$SESSION_ID" ]; then
  echo "  会话 ID: $SESSION_ID"
  if [ -f "$CONFIG" ]; then
    SESSION_BRANCH=$(grep -A1 "^  ${SID_SAFE}:" "$CONFIG" 2>/dev/null | grep "branch:" | sed 's/^[^:]*: *//' || true)
    if [ -n "$SESSION_BRANCH" ]; then
      echo "  绑定分支: $SESSION_BRANCH"
    else
      echo "  绑定: 未绑定（首次调用时将提示确认）"
    fi
  else
    echo "  绑定: 未绑定（config 不存在）"
  fi
else
  echo "  会话 ID: 未提供（传 --session-id 查看）"
fi

# --- 状态模式下到此结束 ---
if [ "$STATUS_ONLY" = true ]; then
  echo ""
  echo "═══════════════════════════════════════"
  exit 0
fi

# --- 3. 准备 worktree + 远程同步 ---
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# --worktree 已指定时直接使用，不调用 prepare（支持测试和离线场景）
if [ -z "$WORKTREE" ] && [ -n "$SESSION_ID" ] && [ -f "$CONFIG" ]; then
  # info 是只读操作，使用 --read 模式（可跳过网络同步）
  WORKTREE=$("$SCRIPT_DIR/perstate-prepare.sh" --session-id "$SESSION_ID" --read 2>/dev/null || true)
fi

# --- 4. 当前 state 统计 ---
echo ""
echo "── 记忆统计 ──"
if [ -z "$WORKTREE" ] || [ ! -d "$WORKTREE" ]; then
  echo "  worktree 不存在，无法统计。"
  echo "  提示: 请先执行 /perstate init 或 /perstate 完成初始化。"
else
  cd "$WORKTREE"

  BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
  REMOTE=$(git remote get-url origin 2>/dev/null || echo "local")
  REPO_SIZE=$(du -sh . 2>/dev/null | cut -f1 || echo "unknown")

  echo "  仓库:   $REMOTE"
  echo "  分支:   $BRANCH"
  echo "  路径:   $WORKTREE"
  echo "  大小:   $REPO_SIZE"
  echo ""

  ENTITY_COUNT=0
  RELATION_COUNT=0
  VALID_RELATIONS=0
  SUPERSEDED=0
  UNDECLARED=0

  if [ -d entities ]; then
    # 优先使用内容索引计数（避免 find 遍历 400k 文件）
    REPO_NAME=$(basename "$(git remote get-url origin 2>/dev/null || echo "local.git")" .git)
    BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "detached")
    INDEX_FILE="$HOME/.perstate/.index/${REPO_NAME}__${BRANCH}.content"
    INDEX_META="$HOME/.perstate/.index/${REPO_NAME}__${BRANCH}.meta"
    CURRENT_HEAD=$(git rev-parse HEAD 2>/dev/null || echo "")
    USE_INDEX=false
    # read 端 ensure-fresh：索引缺失/过期时自动重建，用户无需手动 perstate-index.sh
    _info_index_fresh() {
      [ -n "$CURRENT_HEAD" ] && [ "$CURRENT_HEAD" = "$(cat "$INDEX_META" 2>/dev/null || echo "")" ] && [ -f "$INDEX_FILE" ]
    }
    if ! _info_index_fresh; then
      "$SCRIPT_DIR/perstate-index.sh" --worktree "$WORKTREE" >/dev/null 2>&1 || true
    fi
    if _info_index_fresh; then
      USE_INDEX=true
    fi

    if [ "$USE_INDEX" = true ]; then
      # 索引模式：从索引文件统计（grep -c 标记行，秒级完成 400k 文件）
      ENTITY_COUNT=$(grep -c '===FILE:.*/entity\.md$' "$INDEX_FILE" 2>/dev/null | tr -d ' ' || echo 0)
      _total_files=$(grep -c '^===FILE:' "$INDEX_FILE" 2>/dev/null | tr -d ' ' || echo 0)
      RELATION_COUNT=$(( _total_files - ENTITY_COUNT ))
    else
      ENTITY_COUNT=$(find entities/ -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
      RELATION_COUNT=$(find entities/ -name "*.md" -not -name "entity.md" 2>/dev/null | wc -l | tr -d ' ')
    fi

    # O(n) 统计 valid / superseded
    if [ "$USE_INDEX" = true ]; then
      # 索引模式：awk 单次扫描索引文件，统计 valid/superseded
      read VALID_RELATIONS SUPERSEDED < <(
        awk '
          /^===FILE:/ { if (prev_has) { if (prev_valid) v++; else s++ } prev_has=0; prev_valid=0 }
          /^valid_until:/ { prev_has=1; if ($0 ~ /null/) prev_valid=1 }
          END { if (prev_has) { if (prev_valid) v++; else s++ } print v+0, s+0 }
        ' "$INDEX_FILE" 2>/dev/null
      )
    else
      # 回退模式：find -print0 + xargs -0 awk（避免 ARG_MAX）
      read VALID_RELATIONS SUPERSEDED < <(
        find entities/ -name "*.md" -not -name "entity.md" -print0 2>/dev/null |
        xargs -0 awk '
          FNR==1 {
            if (prev_has) { if (prev_valid) v++; else s++ }
            prev_has=0; prev_valid=0
          }
          /^valid_until:/ { prev_has=1; if ($0 ~ /null/) prev_valid=1 }
          END { if (prev_has) { if (prev_valid) v++; else s++ } print v+0, s+0 }
        ' 2>/dev/null
      )
    fi
    VALID_RELATIONS=${VALID_RELATIONS:-0}
    SUPERSEDED=${SUPERSEDED:-0}
    # 无 valid_until 字段的关系
    UNDECLARED=$(( RELATION_COUNT - VALID_RELATIONS - SUPERSEDED ))
  fi

  echo "  实体数:        $ENTITY_COUNT"
  echo "  关系总数:      $RELATION_COUNT"
  echo "    ├ 有效:      $VALID_RELATIONS"
  echo "    ├ 已取代:    $SUPERSEDED"
  echo "    └ 未声明:    $UNDECLARED"
  echo ""

  echo "  最近提交:"
  git log --oneline -5 2>/dev/null || echo "  无 git 历史"
fi

echo ""
echo "═══════════════════════════════════════"
