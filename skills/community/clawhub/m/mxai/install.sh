#!/bin/bash
# mxai Skill 安装脚本 (Mac/Linux)
SKILL_DIR="$HOME/.openclaw/workspace/skills/mxai"
mkdir -p "$SKILL_DIR"
cp -r "$(dirname "$0")/." "$SKILL_DIR/"
echo "✅ mxai Skill 安装完成！"
echo "请重启 OpenClaw 或在对话中说「重新加载 skill」"
