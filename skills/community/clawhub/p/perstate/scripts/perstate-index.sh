#!/bin/bash
# perstate-index.sh — 构建/维护搜索内容索引（transient cache，非知识图谱数据源）
# 用法: perstate-index.sh --worktree <path> [--rebuild] [--check]
#   --rebuild: 强制重建索引
#   --check: 仅检查索引是否最新（输出 fresh/stale，不重建）
# 设计哲学：索引是 transient 性能 hint（类似 sync cache），不是单一数据源。
#   知识图谱本体仍是 entities/ 目录。索引缺失/过期时自动回退到 grep -r。
#
# 索引格式：NUL 分隔的记录流，每条记录 = filepath \0 content \0
# 搜索时 grep 索引文件（一次顺序读 ~1GB，远快于 400k 次小文件 open/close）
#
# 大规模压测背景：100k 实体 + 300k 关系 = 400k 文件
#   grep -r 逐文件扫描：~120s（400k 次 stat+open+close）
#   grep 索引文件：~3s（1 次顺序读 1.2GB）

set -euo pipefail

WORKTREE=""
REBUILD=false
CHECK_ONLY=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --worktree) WORKTREE="$2"; shift 2 ;;
    --rebuild)  REBUILD=true; shift ;;
    --check)    CHECK_ONLY=true; shift ;;
    *) shift ;;
  esac
done

if [ -z "$WORKTREE" ] || [ ! -d "$WORKTREE" ]; then
  echo "用法: perstate-index.sh --worktree <path> [--rebuild] [--check]" >&2
  exit 1
fi

cd "$WORKTREE"

# 索引目录（与 sync cache 同级，都是 transient）
INDEX_DIR="$HOME/.perstate/.index"
# 从 git remote 推导 repo name
REPO_NAME=$(basename "$(git remote get-url origin 2>/dev/null || echo "local.git")" .git)
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "detached")
INDEX_FILE="$INDEX_DIR/${REPO_NAME}__${BRANCH}.content"
INDEX_META="$INDEX_DIR/${REPO_NAME}__${BRANCH}.meta"

mkdir -p "$INDEX_DIR" 2>/dev/null || true

# --- 检查索引是否最新（对比 git HEAD 与索引构建时的 commit）---
CURRENT_HEAD=$(git rev-parse HEAD 2>/dev/null || echo "no-git")
INDEX_HEAD=""
if [ -f "$INDEX_META" ]; then
  INDEX_HEAD=$(cat "$INDEX_META" 2>/dev/null || echo "")
fi

is_fresh() {
  [ -n "$INDEX_HEAD" ] && [ "$INDEX_HEAD" = "$CURRENT_HEAD" ] && [ -f "$INDEX_FILE" ]
}

if [ "$CHECK_ONLY" = true ]; then
  if is_fresh; then
    echo "fresh"
  else
    echo "stale"
  fi
  exit 0
fi

# --- 重建或使用缓存 ---
if [ "$REBUILD" = false ] && is_fresh; then
  # 索引最新，无需重建
  exit 0
fi

# --- 构建索引 ---
# 格式：每文件用 ===FILE:path 标记起始行，后接完整内容
# 用 awk 单进程批量读取所有文件（FNR==1 检测文件边界），避免 400k 次 cat fork
# xargs -0 自动分批（ARG_MAX），每批一个 awk 进程，总 fork 数 << 文件数
find entities/ -name "*.md" -print0 2>/dev/null | xargs -0 awk '
  FNR==1 { printf "===FILE:%s\n", FILENAME }
  { print }
' > "$INDEX_FILE"

# 记录构建时的 commit
echo "$CURRENT_HEAD" > "$INDEX_META"

# 输出索引大小（供调试）
if [ -f "$INDEX_FILE" ]; then
  SIZE=$(du -sh "$INDEX_FILE" 2>/dev/null | cut -f1 || echo "?")
  echo "索引已构建: $INDEX_FILE ($SIZE, head=$CURRENT_HEAD)" >&2
fi
