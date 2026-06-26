#!/bin/bash
# Installation script for human-like-reply skill

echo "========================================"
echo "自然对话助手 (Human-like Reply) 安装"
echo "========================================"

# Check if we're in the right directory
if [ ! -f "SKILL.md" ]; then
    echo "错误：请在技能目录中运行此脚本"
    exit 1
fi

# Determine OpenClaw skills directory
OPENCLAW_SKILLS="${OPENCLAW_SKILLS_DIR:-$HOME/.openclaw/workspace/skills}"

if [ ! -d "$OPENCLAW_SKILLS" ]; then
    echo "创建 OpenClaw skills 目录..."
    mkdir -p "$OPENCLAW_SKILLS"
fi

# Copy skill to OpenClaw
echo "复制技能到 $OPENCLAW_SKILLS/human-like-reply..."
cp -r . "$OPENCLAW_SKILLS/human-like-reply"

# Copy config template if not exists
if [ ! -f "$OPENCLAW_SKILLS/human-like-reply/config.yaml" ]; then
    echo "创建配置文件..."
    cp config.example.yaml "$OPENCLAW_SKILLS/human-like-reply/config.yaml"
    echo "配置文件已创建，你可以根据需要编辑。"
fi

# Create memory directory
mkdir -p "$OPENCLAW_SKILLS/human-like-reply/memory"

echo ""
echo "========================================"
echo "安装完成！"
echo "========================================"
echo ""
echo "下一步："
echo "1. (可选) 编辑配置文件："
echo "   $OPENCLAW_SKILLS/human-like-reply/config.yaml"
echo ""
echo "2. 测试技能："
echo "   cd $OPENCLAW_SKILLS/human-like-reply"
echo "   python3 scripts/test_formatter.py"
echo ""
echo "3. 重启 OpenClaw 使技能生效"
echo ""