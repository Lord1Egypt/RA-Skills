#!/bin/bash
# OpenClaw 终极套件 - 安全扫描脚本

echo "🛡️ 开始安全审计..."

# 检查 ironclaw-guardian-evolved 是否存在
if [ ! -f "skills/ironclaw-guardian-evolved/scripts/ironclaw_audit.py" ]; then
  echo "❌ ironclaw-guardian-evolved 未找到"
  exit 1
fi

# 扫描所有技能
echo "📊 扫描所有技能..."
scan_count=0
safe_count=0
warning_count=0

for file in skills/*/SKILL.md; do
  echo "扫描：$file"
  result=$(python3 skills/ironclaw-guardian-evolved/scripts/ironclaw_audit.py scan "$file" 2>&1)
  
  if echo "$result" | grep -q "✅ 安全"; then
    echo "  ✅ 安全"
    ((safe_count++))
  elif echo "$result" | grep -q "⚠️ 警告"; then
    echo "  ⚠️ 警告"
    ((warning_count++))
  else
    echo "  ❌ 威胁"
    ((warning_count++))
  fi
  
  ((scan_count++))
done

# 统计结果
echo ""
echo "📊 审计结果:"
echo "  扫描总数：$scan_count"
echo "  ✅ 安全：$safe_count"
echo "  ⚠️ 警告：$warning_count"
echo ""

if [ $warning_count -eq 0 ]; then
  echo "✅ 所有技能通过安全检测"
  exit 0
else
  echo "⚠️ 发现 $warning_count 个警告，请审查"
  exit 1
fi
