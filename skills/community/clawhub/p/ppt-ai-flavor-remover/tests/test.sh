#!/bin/bash
# ppt-ai-flavor-remover 测试脚本（验证文档完整性和脱敏）
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
echo "  ppt-ai-flavor-remover 测试套件"
echo "##########################################"

# 1. SKILL.md 存在
run_test "SKILL.md 文件存在" \
  "ls SKILL.md 2>&1" \
  "SKILL.md"

# 2. YAML frontmatter - name
run_test "YAML frontmatter - name 字段" \
  "head -10 SKILL.md 2>&1" \
  "name:"

# 3. YAML frontmatter - description
run_test "YAML frontmatter - description 字段" \
  "head -10 SKILL.md 2>&1" \
  "description:"

# 4. 十个章节齐全
run_test "章节完整 - 一、写作目标" \
  "cat SKILL.md 2>&1" \
  "一、写作目标"

run_test "章节完整 - 五、事实、数据与承诺边界" \
  "cat SKILL.md 2>&1" \
  "五、事实、数据与承诺边界"

run_test "章节完整 - 六、PPT 内容与版式统一" \
  "cat SKILL.md 2>&1" \
  "六、PPT 内容与版式统一"

run_test "章节完整 - 七、备注写法" \
  "cat SKILL.md 2>&1" \
  "七、备注写法"

run_test "章节完整 - 八、禁止使用的表达" \
  "cat SKILL.md 2>&1" \
  "八、禁止使用的表达"

run_test "章节完整 - 十、修改与交付前自检" \
  "cat SKILL.md 2>&1" \
  "十、修改与交付前自检"

# 5. 五轮自检齐全
run_test "自检 - 语气检查" \
  "cat SKILL.md 2>&1" \
  "语气检查"

run_test "自检 - 事实检查" \
  "cat SKILL.md 2>&1" \
  "事实检查"

run_test "自检 - 边界检查" \
  "cat SKILL.md 2>&1" \
  "边界检查"

run_test "自检 - 一致性检查" \
  "cat SKILL.md 2>&1" \
  "一致性检查"

run_test "自检 - 版式检查" \
  "cat SKILL.md 2>&1" \
  "版式检查"

# 6. 改写示例存在（反例/正例）
run_test "改写示例 - 反例标记" \
  "cat SKILL.md 2>&1" \
  "反例"

run_test "改写示例 - 正例标记" \
  "cat SKILL.md 2>&1" \
  "正例"

# 7. 脱敏检查：不应出现具体厂商与客户敏感信息
run_test "脱敏 - 不含腾讯" \
  "cat SKILL.md 2>&1 | grep -c '腾讯' || echo 0" \
  "^0$"

run_test "脱敏 - 不含恒瑞" \
  "cat SKILL.md 2>&1 | grep -c '恒瑞' || echo 0" \
  "^0$"

run_test "脱敏 - 不含法兰克福" \
  "cat SKILL.md 2>&1 | grep -c '法兰克福' || echo 0" \
  "^0$"

# 8. 触发条件清晰
run_test "触发词明确" \
  "cat SKILL.md 2>&1" \
  "去除AI味\|去AI味\|太AI了"

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
