#!/bin/bash
# 妙音 AI 音乐助手 Skill 安装脚本 (Mac/Linux)

echo "========================================"
echo "妙音 AI 音乐助手 Skill 安装程序"
echo "========================================"
echo ""

SKILL_DIR="$HOME/.openclaw/workspace/skills/miaoyin-ai-music"
echo "目标目录: $SKILL_DIR"
echo ""

# 创建目标目录
mkdir -p "$SKILL_DIR"

# 复制所有文件
echo "正在复制文件..."
cp -r "$(dirname "$0")/." "$SKILL_DIR/"

echo ""
echo "========================================"
echo "✅ 妙音 AI 音乐助手 Skill 安装完成！"
echo "========================================"
echo ""
echo "下一步操作："
echo "1. 请重启 OpenClaw"
echo "2. 或在对话中说「重新加载 skill」"
echo ""
echo "配置 API Token："
echo "请访问 https://ai.growingth.com/api-service"
echo "获取您的 API Token 并配置环境变量 MIAOYIN_API_TOKEN"
echo ""
echo "配置方法："
echo "  export MIAOYIN_API_TOKEN=your-token"
echo "  或将其添加到 ~/.bashrc 或 ~/.zshrc 中"
echo ""
