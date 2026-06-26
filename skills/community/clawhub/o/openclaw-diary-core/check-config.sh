#!/bin/bash
# Diary Skill 配置验证脚本

echo "=== Diary Skill 配置检查 ==="
echo ""

# 检查目录结构
echo "1. 检查目录结构..."
if [ -f "diary/skill.json" ] && [ -f "diary/prompt.md" ] && [ -f "diary/config/diary-config.json" ]; then
  echo "   ✓ 核心文件完整"
else
  echo "   ✗ 核心文件缺失"
  exit 1
fi

if [ -f "diary/personalities/intj.md" ] && [ -f "diary/personalities/enfp.md" ]; then
  echo "   ✓ 人设文件完整"
else
  echo "   ✗ 人设文件缺失"
  exit 1
fi

# 检查配置文件
echo ""
echo "2. 检查配置文件..."
if command -v jq &> /dev/null; then
  PERSONALITY=$(jq -r '.personality.type' diary/config/diary-config.json)
  STORAGE=$(jq -r '.storage.type' diary/config/diary-config.json)
  echo "   当前人设: $PERSONALITY"
  echo "   存储位置: $STORAGE"
else
  echo "   ⚠ 未安装 jq，跳过配置解析"
fi

# 检查飞书环境变量
echo ""
echo "3. 检查飞书配置..."
if [ -n "$FEISHU_APP_ID" ] && [ -n "$FEISHU_APP_SECRET" ]; then
  echo "   ✓ 飞书环境变量已设置"
else
  echo "   ⚠ 飞书环境变量未设置（可选）"
fi

# 检查本地目录
echo ""
echo "4. 检查本地日记目录..."
JOURNAL_DIR="$HOME/write_me/00inbox/journal"
if [ -d "$JOURNAL_DIR" ]; then
  echo "   ✓ 日记目录已存在: $JOURNAL_DIR"
else
  echo "   ⚠ 日记目录不存在，将在首次使用时创建"
fi

echo ""
echo "=== 检查完成 ==="
echo ""
echo "下一步："
echo "1. 复制到 OpenClaw workspace: cp -r diary ~/.openclaw/workspace/"
echo "2. 在 OpenClaw 中说：'记一下今天的想法'"
