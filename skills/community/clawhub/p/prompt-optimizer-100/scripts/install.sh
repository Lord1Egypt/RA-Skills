#!/bin/bash

# Prompt 优化系统 Skill 安装脚本
# 支持 Merge 模式（保留用户原有规则）

set -e

echo "🚀 开始安装 Prompt 优化系统 Skill..."

# 1. 检查依赖
echo "📋 检查依赖..."
if ! command -v openclaw &> /dev/null; then
    echo "❌ OpenClaw 未安装，请先安装 OpenClaw"
    exit 1
fi

# 检查 OpenClaw 版本
OPENCLAW_VERSION=$(openclaw --version | grep -oP '\d+\.\d+\.\d+' | head -1)
if [[ "$OPENCLAW_VERSION" < "2026.3.8" ]]; then
    echo "❌ OpenClaw 版本过低（当前：$OPENCLAW_VERSION，要求：≥2026.3.8）"
    exit 1
fi
echo "✅ OpenClaw 版本：$OPENCLAW_VERSION"

# 2. 检查记忆文件
MEMORY_FILE="$HOME/.openclaw/workspace/memory/agent-notes.md"
if [ ! -f "$MEMORY_FILE" ]; then
    echo "⚠️ 记忆文件不存在，创建新文件..."
    mkdir -p "$(dirname "$MEMORY_FILE")"
    touch "$MEMORY_FILE"
fi

# 3. 备份原有规则（Merge 模式）
if [ -s "$MEMORY_FILE" ]; then
    echo "📦 备份原有规则..."
    cp "$MEMORY_FILE" "$MEMORY_FILE.bak.$(date +%Y%m%d%H%M%S)"
    echo "✅ 备份完成：$MEMORY_FILE.bak.*"
fi

# 4. 复制规则文件
echo "📝 复制规则文件..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RULES_FILE="$SCRIPT_DIR/../rules/prompt-optimization.md"

if [ -f "$RULES_FILE" ]; then
    # Merge 模式：追加到原有文件
    echo "" >> "$MEMORY_FILE"
    echo "---" >> "$MEMORY_FILE"
    echo "" >> "$MEMORY_FILE"
    cat "$RULES_FILE" >> "$MEMORY_FILE"
    echo "✅ 规则文件已写入（Merge 模式）"
else
    echo "❌ 规则文件不存在：$RULES_FILE"
    exit 1
fi

# 5. 验证记忆文件
echo "✅ 验证记忆文件..."
if grep -q "需求分级" "$MEMORY_FILE"; then
    echo "✅ 规则已加载"
else
    echo "❌ 规则未正确加载"
    exit 1
fi

# 6. 检查配置
echo "🔧 检查配置..."
if openclaw config get channels.feishu.streaming 2>/dev/null | grep -q "true"; then
    echo "✅ 流式输出已开启"
else
    echo "⚠️ 流式输出未开启，建议执行：openclaw config set channels.feishu.streaming true"
fi

echo ""
echo "✅ Prompt 优化系统 Skill 安装完成！"
echo ""
echo "📋 测试命令："
echo "  L1: 写一篇 300 字文章"
echo "  L2: 调研一下竞品"
echo "  L3: 技术选型方案"
echo "  L4: 生成客户方案 PPT"
echo ""
echo "📄 完整文档：https://feishu.cn/docx/He9Gdnpd4oTydyxSAZYcVQ1dnTc"
