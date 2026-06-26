#!/bin/bash
# prompt-optimizer 测试脚本（实用版 - 验证文档完整性和实用要素）
set +e

SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SKILL_ROOT" || exit 1

PASS=0
FAIL=0
RESULTS=()

run_test() {
  local name="$1"
  local cmd="$2"
  local expect="$3"
  echo ""
  echo "=========================================="
  echo "  [测试] $name"
  echo "=========================================="
  local output
  output=$(eval "$cmd" 2>&1)
  if echo "$output" | grep -q "$expect"; then
    echo "[PASS] $name"
    PASS=$((PASS + 1))
    RESULTS+=("[PASS] $name")
  else
    echo "[FAIL] $name (期望: $expect)"
    FAIL=$((FAIL + 1))
    RESULTS+=("[FAIL] $name")
  fi
}

echo ""
echo "##########################################"
echo "  prompt-optimizer 测试套件（实用版）"
echo "##########################################"

# 1. SKILL.md 存在
run_test "SKILL.md 文件存在" \
  "ls SKILL.md 2>&1" \
  "SKILL.md"

# 2. YAML frontmatter
run_test "YAML frontmatter - name 字段" \
  "head -10 SKILL.md 2>&1" \
  "name:"

# 3. YAML frontmatter - description
run_test "YAML frontmatter - description 字段" \
  "head -10 SKILL.md 2>&1" \
  "description:"

# 4. 包含 RTCF 实用框架
run_test "实用框架 - RTCF" \
  "cat SKILL.md 2>&1" \
  "RTCF"

# 5. 包含角色（Role）补全说明
run_test "RTCF - Role 角色" \
  "cat SKILL.md 2>&1" \
  "Role"

# 6. 包含格式（Format）补全说明
run_test "RTCF - Format 格式" \
  "cat SKILL.md 2>&1" \
  "Format"

# 7. 至少有 4 个真实示例
run_test "示例数量 - 至少 4 个" \
  "grep -c '示例 [0-9]' SKILL.md 2>&1" \
  "[4-9]"

# 8. 包含工作流程（诊断 → 补全 → 输出）
run_test "工作流程 - 诊断" \
  "cat SKILL.md 2>&1" \
  "诊断"

# 9. 双语支持
run_test "双语支持 - 检测语言提示" \
  "cat SKILL.md 2>&1" \
  "Chinese\|English\|双语\|中文"

# 10. 已移除论文方法论引用（实用化验证）
run_test "已去除学术化方法论 - 不应包含 ACON" \
  "cat SKILL.md 2>&1 | grep -c 'ACON' || echo 0" \
  "^0$"

# 11. 删除的 en 版本不应存在
run_test "prompt-optimizer-en 已删除" \
  "ls ../prompt-optimizer-en 2>&1 || echo 'NOT_FOUND'" \
  "NOT_FOUND"

# 12. 触发条件清晰
run_test "明确触发条件" \
  "cat SKILL.md 2>&1" \
  "优化提示词\|改进prompt\|优化一下"

# 总结
echo ""
echo "##########################################"
echo "  测试结果汇总"
echo "##########################################"
for r in "${RESULTS[@]}"; do
  echo "$r"
done
echo ""
echo "通过: $PASS / $((PASS + FAIL))"
echo ""

if [ $FAIL -eq 0 ]; then
  echo "全部测试通过"
  exit 0
else
  echo "$FAIL 项失败"
  exit 1
fi
