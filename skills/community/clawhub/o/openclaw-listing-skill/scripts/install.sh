#!/bin/bash
# ============================================================
# OpenClaw 跨境电商 Listing 生成器 - 一键部署脚本
# 使用方法：bash install.sh
# ============================================================

set -e

SKILL_NAME="listing-generator"
OPENCLAW_WORKSPACE="$HOME/.openclaw/workspace"
SKILL_DIR="$HOME/.openclaw/skills/$SKILL_NAME"

echo ""
echo "🚀 OpenClaw Listing 生成器 技能包安装"
echo "======================================"

# 1. 检查 OpenClaw 是否已安装
if [ ! -d "$OPENCLAW_WORKSPACE" ]; then
  echo "❌ 未找到 OpenClaw workspace: $OPENCLAW_WORKSPACE"
  echo "   请先完成 OpenClaw 初始化配置"
  exit 1
fi

echo "✅ 检测到 OpenClaw workspace"

# 2. 创建技能目录
mkdir -p "$SKILL_DIR"
echo "✅ 创建技能目录: $SKILL_DIR"

# 3. 复制技能文件
cp SKILL.md "$SKILL_DIR/"
cp -r examples "$SKILL_DIR/"
echo "✅ 技能文件已复制"

# 4. 追加 Agent 配置到 AGENTS.md
AGENTS_FILE="$OPENCLAW_WORKSPACE/AGENTS.md"

# 检查是否已安装
if grep -q "listing-generator" "$AGENTS_FILE" 2>/dev/null; then
  echo "⚠️  listing-generator 已存在于 AGENTS.md，跳过追加"
else
  echo "" >> "$AGENTS_FILE"
  echo "---" >> "$AGENTS_FILE"
  cat AGENTS_SNIPPET.md >> "$AGENTS_FILE"
  echo "✅ Agent 配置已追加到 AGENTS.md"
fi

# 5. 完成提示
echo ""
echo "======================================"
echo "🎉 安装完成！"
echo ""
echo "使用方法（在 Telegram 中发送）："
echo "  /listing [产品描述]"
echo "  /listing amazon [产品描述]"
echo "  /listing aliexpress [产品描述]"
echo "  /listing keywords [产品描述]"
echo ""
echo "或直接发送产品图片 + 描述文字"
echo "======================================"
