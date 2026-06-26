#!/bin/bash
# scripts/version-check.sh — 校验 SKILL.md / plugin.json / git tag 版本一致性
# Usage: ./scripts/version-check.sh [expected-version] [project-dir]
#   expected-version: 可选，预期的版本号（不含 v 前缀）
#   project-dir: 可选，项目目录（默认当前目录）
# Exit 0 = 一致, Exit 1 = 不一致

set -euo pipefail

# 解析参数
EXPECTED_VER="${1:-}"
PROJECT_DIR="${2:-.}"

cd "$PROJECT_DIR"

# --- 提取版本号 ---

# 1. SKILL.md frontmatter version
SKILL_VER=$(grep '^version:' SKILL.md | head -1 | sed 's/version: *//' | tr -d '[:space:]')

# 2. .claude-plugin/plugin.json version（降级策略：node → python3 → 手动解析）
#    注意：Windows 上 python3 可能返回非标准 exit code（如 49），需用 || true 防止 set -e 中断
PLUGIN_VER=""
if command -v node &>/dev/null; then
  PLUGIN_VER=$(node -e "console.log(require('./.claude-plugin/plugin.json').version)" 2>/dev/null || true)
elif command -v python3 &>/dev/null; then
  PLUGIN_VER=$(python3 -c "import json; print(json.load(open('.claude-plugin/plugin.json'))['version'])" 2>/dev/null || true)
elif command -v grep &>/dev/null; then
  PLUGIN_VER=$(grep '"version"' .claude-plugin/plugin.json | head -1 | sed 's/.*"version": *"\([^"]*\)".*/\1/')
fi

# 3. 最新 git tag 版本号（去掉 v 前缀）
TAG_VER=""
if git rev-parse --git-dir &>/dev/null; then
  TAG_VER=$(git tag -l 'v*' --sort=-version:refname 2>/dev/null | head -1 | sed 's/^v//')
fi

# --- 比对 ---

# 确定基准版本：优先使用传入的预期版本，否则使用 SKILL.md 版本
BASE_VER="${EXPECTED_VER:-$SKILL_VER}"

# 结果收集
ALL_MATCH=true
ERRORS=""

check_match() {
  local label="$1"
  local value="$2"
  local base="$3"

  if [ -z "$value" ]; then
    echo "  ❌ $label: (未找到)"
    ALL_MATCH=false
    ERRORS="${ERRORS}  - $label: 未找到版本号\n"
  elif [ "$value" = "$base" ]; then
    echo "  ✅ $label: $value"
  else
    echo "  ❌ $label: $value (期望: $base)"
    ALL_MATCH=false
    ERRORS="${ERRORS}  - $label: $value ≠ $base\n"
  fi
}

echo "=== Version Check ==="
echo ""
check_match "SKILL.md"    "$SKILL_VER"  "$BASE_VER"
check_match "plugin.json" "$PLUGIN_VER" "$BASE_VER"
check_match "Latest tag"  "$TAG_VER"    "$BASE_VER"
echo ""

if [ "$ALL_MATCH" = true ]; then
  echo "✅ All versions match: $BASE_VER"
  exit 0
else
  echo "❌ Version mismatch detected!"
  echo -e "$ERRORS"
  echo "Fix: Update all version sources to $BASE_VER before releasing."
  exit 1
fi
