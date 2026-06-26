#!/bin/bash
# OpenClaw 终极套件 - 部署脚本

echo "🚀 开始部署 OpenClaw 终极套件..."

# 检查是否在正确的目录
if [ ! -d "skills" ]; then
  echo "❌ 请在 openclaw-ultimate-suite 目录运行此脚本"
  exit 1
fi

# Git 操作
echo "📂 Git 操作..."
git add -A
git commit -m "deploy: OpenClaw 终极套件 v3.0.0"

if [ $? -eq 0 ]; then
  echo "✅ Git commit 成功"
else
  echo "⚠️ Git commit 失败，继续..."
fi

# GitHub push (需要网络)
echo "🌐 推送到 GitHub..."
git push origin main

if [ $? -eq 0 ]; then
  echo "✅ GitHub push 成功"
  echo "📦 仓库：https://github.com/wd041216-bit/openclaw-ultimate-suite"
else
  echo "⚠️ GitHub push 失败 (网络问题)"
  echo "💡 稍后网络恢复时手动 push: git push origin main"
fi

# ClawHub 发布 (可选)
echo ""
read -p "是否发布到 ClawHub? (y/n): " publish_clawhub
if [ "$publish_clawhub" = "y" ]; then
  echo "📦 发布到 ClawHub..."
  clawhub publish .
  
  if [ $? -eq 0 ]; then
    echo "✅ ClawHub 发布成功"
  else
    echo "⚠️ ClawHub 发布失败"
  fi
fi

# 验证部署
echo ""
echo "🔍 验证部署..."
echo "  GitHub 仓库：https://github.com/wd041216-bit/openclaw-ultimate-suite"
echo "  技能数量：$(ls skills/ | wc -l) 个"
echo "  文档数量：$(ls docs/ 2>/dev/null | wc -l) 个"
echo "  示例数量：$(ls examples/ 2>/dev/null | wc -l) 个"
echo "  脚本数量：$(ls scripts/ 2>/dev/null | wc -l) 个"

echo ""
echo "🎉 部署完成！"
echo ""
echo "下一步:"
echo "  1. 测试安装：clawhub install openclaw-ultimate-suite"
echo "  2. 使用技能：\"我想做个电商网站\""
echo "  3. 推广材料：参考 docs/MARKETING.md"
echo ""
