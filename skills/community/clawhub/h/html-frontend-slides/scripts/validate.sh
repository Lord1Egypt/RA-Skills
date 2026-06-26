# validate.sh — frontend-slides 技能结构验证脚本
# 用法: bash scripts/validate.sh [--verbose]

VERBOSE=false
[ "$1" = "--verbose" ] && VERBOSE=true

ERRORS=0
WARNINGS=0

echo "🔍 验证 frontend-slides 技能结构..."
echo ""

# 必须存在的文件
REQUIRED_FILES=(
  "SKILL.md"
  "README.md"
  "LICENSE"
  "agents/openai.yaml"
  "references/animation-patterns.md"
  "references/html-template.md"
  "references/STYLE_PRESETS.md"
  "references/viewport-base.css"
  "scripts/deploy.sh"
  "scripts/export-pdf.sh"
  "scripts/extract-pptx.py"
)

# 检查必需文件
echo "📦 检查必需文件..."
for file in "${REQUIRED_FILES[@]}"; do
  if [ -f "$file" ]; then
    size=$(wc -c < "$file" 2>/dev/null || echo 0)
    [ "$VERBOSE" = true ] && echo "  ✅ $file ($size bytes)"
  else
    echo "  ❌ 缺失: $file"
    ((ERRORS++))
  fi
done

echo ""

# 检查 SKILL.md 关键节点
echo "📖 检查 SKILL.md 内容完整性..."
SKILL_CONTENT=$(cat SKILL.md 2>/dev/null)

check_section() {
  if echo "$SKILL_CONTENT" | grep -q "$1"; then
    [ "$VERBOSE" = true ] && echo "  ✅ 包含: $1"
    return 0
  else
    echo "  ❌ 缺失章节: $1"
    ((ERRORS++))
    return 1
  fi
}

check_section "Mode A" || true
check_section "Mode B" || true
check_section "Mode C" || true
check_section "viewport-base.css" || true
check_section "STYLE_PRESETS.md" || true

echo ""

# 检查引用文件行数（避免空文件）
echo "📊 检查参考资源文件大小..."
for ref in "references/animation-patterns.md" "references/html-template.md" "references/STYLE_PRESETS.md" "references/viewport-base.css"; do
  if [ -f "$ref" ]; then
    lines=$(wc -l < "$ref" 2>/dev/null || echo 0)
    if [ "$lines" -lt 5 ]; then
      echo "  ⚠️  文件过小: $ref ($lines 行)"
      ((WARNINGS++))
    else
      [ "$VERBOSE" = true ] && echo "  ✅ $ref ($lines 行)"
    fi
  fi
done

echo ""

# 检查脚本可执行性
echo "⚙️  检查脚本有效性..."
for script in "scripts/deploy.sh" "scripts/export-pdf.sh" "scripts/extract-pptx.py"; do
  if [ -f "$script" ]; then
    # 检查 shebang 或 python 声明
    first_line=$(head -n1 "$script" 2>/dev/null)
    if [[ "$first_line" =~ ^#!.*/(bash|sh) ]] || [[ "$first_line" =~ ^#!.*python ]]; then
      [ "$VERBOSE" = true ] && echo "  ✅ $script (可执行)"
    else
      echo "  ⚠️  $script 缺少 shebang"
      ((WARNINGS++))
    fi
  fi
done

echo ""

# 检查 openai.yaml 内容
echo "🤖 检查 agent 配置..."
if [ -f "agents/openai.yaml" ]; then
  yaml_size=$(wc -c < "agents/openai.yaml" 2>/dev/null || echo 0)
  if [ "$yaml_size" -lt 300 ]; then
    echo "  ⚠️  openai.yaml 过小 ($yaml_size bytes)，可能缺少字段"
    ((WARNINGS++))
  else
    [ "$VERBOSE" = true ] && echo "  ✅ openai.yaml 配置完整 ($yaml_size bytes)"
  fi

  # 检查必要字段
  for field in "name:" "description:" "triggers:" "keywords:"; do
    if grep -q "$field" "agents/openai.yaml" 2>/dev/null; then
      [ "$VERBOSE" = true ] && echo "  ✅ 包含字段: $field"
    else
      echo "  ⚠️  缺少字段: $field"
      ((WARNINGS++))
    fi
  done
else
  echo "  ❌ agents/openai.yaml 不存在"
  ((ERRORS++))
fi

echo ""

# 检查 Windows 脚本（可选）
echo "🪟 检查 Windows 兼容性..."
if [ -f "scripts/deploy.bat" ] && [ -f "scripts/export-pdf.bat" ]; then
  echo "  ✅ Windows 批处理脚本齐全"
else
  echo "  ⚠️  缺少 Windows 批处理脚本 (.bat)"
  ((WARNINGS++))
fi

echo ""
echo "═══════════════════════════════════════"
echo "📋 验证结果"
echo "═══════════════════════════════════════"
echo "错误: $ERRORS"
echo "警告: $WARNINGS"
echo ""

if [ "$ERRORS" -eq 0 ] && [ "$WARNINGS" -eq 0 ]; then
  echo "✅ 技能结构完整，所有检查通过！"
  exit 0
elif [ "$ERRORS" -eq 0 ]; then
  echo "⚠️  结构完整，但有 $WARNINGS 个警告"
  exit 0
else
  echo "❌ 存在 $ERRORS 个错误，$WARNINGS 个警告"
  exit 1
fi
