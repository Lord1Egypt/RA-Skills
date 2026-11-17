#!/usr/bin/env bash
# fork.sh — Step 2: 副本化 + 自动删内部产物
# Usage:
#   ./fork.sh <source-skill-name-or-abs-path> [<new-slug>]
#
# 源 skill 定位（第一个参数）：
#   - 若传绝对路径且是目录 → 直接用
#   - 否则按 skill 名，在以下路径依次探测（可用 SKILLS_DIR 覆盖首选）：
#       $SKILLS_DIR / ~/.claude/skills / ~/.cursor/skills / ./skills
#       / ~/.openclaw/workspace/skills / ~/.config/skills
# 输出目录（可用 OPENSOURCE_OUT_DIR 覆盖，默认 ./opensourceskills）
set -euo pipefail

SOURCE="${1:-}"
NEW_SLUG="${2:-}"

if [[ -z "$SOURCE" ]]; then
  cat <<EOF >&2
Usage: $0 <source-skill-name-or-abs-path> [<new-slug>]

  源 skill 可传:
    - skill 名（自动在多个 agent skills 目录探测）
    - skill 绝对路径（直接使用）

  可选环境变量:
    SKILLS_DIR          优先探测的 skills 目录
    OPENSOURCE_OUT_DIR  副本输出目录（默认 ./opensourceskills）
EOF
  exit 1
fi

# ---- 定位源 skill ----
SRC_DIR=""
if [[ "$SOURCE" = /* && -d "$SOURCE" ]]; then
  SRC_DIR="$SOURCE"
else
  # 多路径探测
  CANDIDATES=(
    "${SKILLS_DIR:-}"
    "$HOME/.claude/skills"
    "$HOME/.cursor/skills"
    "./skills"
    "$HOME/.openclaw/workspace/skills"
    "$HOME/.config/skills"
  )
  for base in "${CANDIDATES[@]}"; do
    [[ -z "$base" ]] && continue
    if [[ -d "$base/$SOURCE" ]]; then
      SRC_DIR="$base/$SOURCE"
      break
    fi
  done
fi

if [[ -z "$SRC_DIR" || ! -d "$SRC_DIR" ]]; then
  echo "❌ Source skill not found: $SOURCE" >&2
  echo "   探测目录: \$SKILLS_DIR, ~/.claude/skills, ~/.cursor/skills, ./skills, ~/.openclaw/workspace/skills" >&2
  echo "   可直接传绝对路径，或设 SKILLS_DIR。" >&2
  exit 2
fi

# 从源目录推 slug（若未显式传 new-slug）
[[ -z "$NEW_SLUG" ]] && NEW_SLUG="$(basename "$SRC_DIR")"

# ---- 输出目录 ----
OUT_DIR="${OPENSOURCE_OUT_DIR:-./opensourceskills}"
DST_DIR="$OUT_DIR/$NEW_SLUG"

echo "ℹ️  源: $SRC_DIR"
echo "ℹ️  目标: $DST_DIR"

if [[ -e "$DST_DIR" ]]; then
  echo "⚠️  Destination already exists: $DST_DIR" >&2
  echo "   请由用户决定：覆盖（先 rm -rf）/ 换 new-slug / 直接进入既有副本继续工作。" >&2
  exit 3
fi

mkdir -p "$(dirname "$DST_DIR")"
# 用 rsync 排除大目录/内部产物（rsync 不可用时回退 cp -r）
if command -v rsync >/dev/null 2>&1; then
  rsync -a \
    --exclude 'node_modules/' \
    --exclude '.git/' \
    --exclude '__pycache__/' \
    --exclude '*.pyc' \
    --exclude '.skill-data/' \
    --exclude 'output/' \
    --exclude 'opensourceskills/' \
    "$SRC_DIR/" "$DST_DIR/"
else
  cp -r "$SRC_DIR" "$DST_DIR"
  # cp 无 --exclude，复制后逐项清理（与上方 rsync 排除项对齐，含嵌套 opensourceskills 副本）
  rm -rf "$DST_DIR/node_modules" "$DST_DIR/.git" "$DST_DIR/__pycache__" \
         "$DST_DIR/.skill-data" "$DST_DIR/output" "$DST_DIR/opensourceskills" 2>/dev/null || true
  find "$DST_DIR" -name '*.pyc' -delete 2>/dev/null || true
  find "$DST_DIR" -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
fi
echo "✅ Forked: $SRC_DIR → $DST_DIR"

# 自动删内部产物
echo ""
echo "🧹 Cleaning internal artifacts..."

removed=0
for pattern in \
  "$DST_DIR/sign.key" \
  "$DST_DIR/.install-source.json" \
  "$DST_DIR/skill_meta.json"
do
  if [[ -f "$pattern" ]]; then
    rm -f "$pattern"
    echo "   rm $pattern"
    removed=$((removed+1))
  fi
done

# 递归删（用 find 真删并打印实际命中的路径，避免误报"已删"）
del_by_find() {
  # $1=type (d|f), $2=name pattern, $3=human label
  local matches
  matches=$(find "$DST_DIR" -type "$1" -name "$2" 2>/dev/null)
  if [[ -n "$matches" ]]; then
    while IFS= read -r p; do
      [[ -z "$p" ]] && continue
      rm -rf "$p"
      echo "   rm $p"
      removed=$((removed+1))
    done <<< "$matches"
  fi
}

del_by_find d "__pycache__" "__pycache__"
del_by_find f "*.pyc"        "*.pyc"
del_by_find d ".skill-data"  ".skill-data"
del_by_find f "*.json.md"    "*.json.md"

if [[ $removed -eq 0 ]]; then
  echo "   (nothing internal to delete — already clean)"
fi

# USAGE.md 提示（不自动删，可能用户想保留）
if [[ -f "$DST_DIR/USAGE.md" ]] && [[ -f "$DST_DIR/SKILL.md" ]]; then
  echo ""
  echo "⚠️  发现 USAGE.md，请检查与 SKILL.md 是否内容重复。"
  echo "   如重复建议删 USAGE.md（避免双语维护成本，glic-check 实证）"
fi

echo ""
echo "✅ Fork done. Next steps:"
echo "   1. cd $DST_DIR"
echo "   2. Run strip_scan.sh \"$DST_DIR\" to scan internal info"

# 机器可读输出（供 run_all.sh 等编排脚本解析，绝对路径，不依赖中文文案）
FORK_ABS="$(cd "$DST_DIR" && pwd)"
echo "FORK_DIR=$FORK_ABS"
