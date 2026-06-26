#!/usr/bin/env bash
# L0 静态校验脚本 - 验证 OpenClaw Memory System 交付物质量
# 用法：bash scripts/validate.sh

set -euo pipefail

PASS=0
FAIL=0
BASE=$(cd "$(dirname "$0")/.." && pwd)

check() {
  local desc="$1"
  local result="$2"
  if [ "$result" = "0" ]; then
    echo "✅ $desc"
    PASS=$((PASS + 1))
  else
    echo "❌ $desc"
    FAIL=$((FAIL + 1))
  fi
}

echo "===== OpenClaw Memory System 静态校验 ====="
echo ""

# 1. 文件完整性
count=$(find "$BASE/prompts" -name "*.md" | wc -l)
[ "$count" -ge 7 ] && r=0 || r=1
check "Prompt 文件数量（期望≥7，实际 $count）" "$r"

count=$(find "$BASE/templates" -name "*.md" | wc -l)
[ "$count" -eq 3 ] && r=0 || r=1
check "模板文件数量（期望 3，实际 $count）" "$r"

count=$(find "$BASE/references" -name "*.md" | wc -l)
[ "$count" -eq 3 ] && r=0 || r=1
check "参考文档数量（期望 3，实际 $count）" "$r"

# 2. 文件非空
empty=$(find "$BASE/prompts" "$BASE/templates" "$BASE/references" -name "*.md" -empty 2>/dev/null | wc -l)
[ "$empty" -eq 0 ] && r=0 || r=1
check "无空文件（空文件数: $empty）" "$r"

# 3. 无 ~ 符号（检查实际路径使用，排除文档说明中的 `~`）
tilde=$(grep -rl '^\s*~\/' "$BASE/prompts"/*.md 2>/dev/null | wc -l || true)
[ "$tilde" -eq 0 ] && r=0 || r=1
check "Prompt 无 ~ 路径（违规文件数: $tilde）" "$r"

# 4. 关键段落
for f in "$BASE/prompts"/*.md; do
  name=$(basename "$f")
  has_role=$(grep -c '## 角色' "$f" || true)
  has_steps=$(grep -c '## 执行步骤' "$f" || true)
  has_errors=$(grep -cE '## (错误处理|失败处理)' "$f" || true)
  if [ "$has_role" -gt 0 ] && [ "$has_steps" -gt 0 ] && [ "$has_errors" -gt 0 ]; then
    r=0
  else
    r=1
    echo "   详情: $name 缺少段落 (角色:$has_role 步骤:$has_steps 错误处理:$has_errors)"
  fi
  check "$name 关键段落完整" "$r"
done

# 5. 动态日期
for f in l2-nightly-prompt.md l3-weekly-prompt.md; do
  has_date=$(grep -c 'date' "$BASE/prompts/$f" || true)
  [ "$has_date" -gt 0 ] && r=0 || r=1
  check "$f 包含动态日期获取" "$r"
done

# 6. 游标机制
for f in l1-hourly-prompt.md l2-nightly-prompt.md; do
  has_cursor=$(grep -c 'Last_Extracted_Time' "$BASE/prompts/$f" || true)
  [ "$has_cursor" -gt 0 ] && r=0 || r=1
  check "$f 包含游标机制" "$r"
done

# 7. Cron 表达式一致性（SKILL.md 内部自洽）
cron_l1=$(grep -c '0 9-23' "$BASE/SKILL.md" || true)
cron_l2=$(grep -c '5 23' "$BASE/SKILL.md" || true)
cron_l3=$(grep -c '30 23' "$BASE/SKILL.md" || true)
cron_gc=$(grep -c '10 23' "$BASE/SKILL.md" || true)
if [ "$cron_l1" -gt 0 ] && [ "$cron_l2" -gt 0 ] && \
   [ "$cron_l3" -gt 0 ] && [ "$cron_gc" -gt 0 ]; then
  r=0
else
  r=1
fi
check "SKILL.md Cron 表达式完整" "$r"

# 8. SKILL.md 命令对应
has_install=$(grep -c 'install-memory' "$BASE/SKILL.md" || true)
has_check=$(grep -c 'check-memory' "$BASE/SKILL.md" || true)
[ "$has_install" -gt 0 ] && [ "$has_check" -gt 0 ] && r=0 || r=1
check "SKILL.md 包含可用命令说明" "$r"

echo ""
echo "===== 总计: $PASS 通过, $FAIL 失败 ====="
[ "$FAIL" -eq 0 ] && echo "🎉 全部通过！" || exit 1
