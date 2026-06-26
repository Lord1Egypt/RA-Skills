#!/bin/bash
# OpenClaw 终极套件 - 一键安装脚本

echo "🚀 开始安装 OpenClaw 终极套件..."

# 检查 OpenClaw 是否安装
if ! command -v openclaw &> /dev/null; then
  echo "❌ OpenClaw 未安装，请先安装 OpenClaw"
  exit 1
fi

# 创建技能目录
mkdir -p ~/.openclaw/workspace/skills

# 方式 1：ClawHub 安装 (推荐)
echo "📦 使用 ClawHub 安装..."
clawhub install openclaw-ultimate-suite

if [ $? -eq 0 ]; then
  echo "✅ ClawHub 安装成功"
else
  echo "⚠️ ClawHub 安装失败，尝试本地安装..."
  
  # 方式 2：本地安装
  cd ~/.openclaw/workspace/openclaw-ultimate-suite
  cp -r skills/* ~/.openclaw/workspace/skills/
  
  if [ $? -eq 0 ]; then
    echo "✅ 本地安装成功"
  else
    echo "❌ 安装失败"
    exit 1
  fi
fi

# 验证安装
echo "🔍 验证安装..."
cd ~/.openclaw/workspace/skills
skill_count=$(ls -d */ 2>/dev/null | wc -l)

if [ $skill_count -ge 30 ]; then
  echo "✅ 验证成功：已安装 $skill_count 个技能"
else
  echo "⚠️ 验证失败：仅安装 $skill_count 个技能"
  exit 1
fi

# 初始化配置
echo "⚙️ 初始化配置..."

# Playwright 安装 (可选)
read -p "是否安装 Playwright? (y/n): " install_playwright
if [ "$install_playwright" = "y" ]; then
  playwright install
  playwright install-deps
  echo "✅ Playwright 安装完成"
fi

# 安全检测
echo "🛡️ 运行安全检测..."
python3 ironclaw-guardian-evolved/scripts/ironclaw_audit.py scan office/SKILL.md

echo "🎉 安装完成！"
echo ""
echo "使用示例:"
echo "  # 自动激活 (推荐)"
echo "  \"我想做个电商网站\""
echo ""
echo "  # 手动调用"
echo "  /orchestrator \"开发一个电商网站 MVP\""
echo ""
echo "  # 查看技能"
echo "  ls ~/.openclaw/workspace/skills/"
echo ""
