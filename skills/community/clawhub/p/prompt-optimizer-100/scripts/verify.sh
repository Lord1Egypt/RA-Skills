#!/bin/bash

# Prompt 优化系统 Skill 验证脚本

set -e

echo "🔍 开始验证 Prompt 优化系统..."

# 1. 检查记忆文件
echo "📋 检查记忆文件..."
MEMORY_FILE="$HOME/.openclaw/workspace/memory/agent-notes.md"
if grep -q "需求分级" "$MEMORY_FILE"; then
    echo "✅ 规则已加载"
else
    echo "❌ 规则未加载"
    exit 1
fi

# 2. 检查 L1-L4 分级规则
echo "🔍 检查分级规则..."
if grep -q "L1" "$MEMORY_FILE" && grep -q "L2" "$MEMORY_FILE" && grep -q "L3" "$MEMORY_FILE" && grep -q "L4" "$MEMORY_FILE"; then
    echo "✅ L1-L4 分级规则完整"
else
    echo "❌ 分级规则不完整"
    exit 1
fi

# 3. 检查角色使用规则
echo "🔍 检查角色使用规则..."
if grep -q "角色" "$MEMORY_FILE"; then
    echo "✅ 角色使用规则已加载"
else
    echo "⚠️ 角色使用规则未加载"
fi

# 4. 检查工具
echo "🔧 检查工具..."
if openclaw config get channels.feishu.streaming 2>/dev/null | grep -q "true"; then
    echo "✅ 流式输出已开启"
else
    echo "⚠️ 流式输出未开启，建议执行：openclaw config set channels.feishu.streaming true"
fi

if openclaw config get channels.feishu.renderMode 2>/dev/null | grep -q "card"; then
    echo "✅ 卡片渲染模式已开启"
else
    echo "⚠️ 卡片渲染模式未开启，建议执行：openclaw config set channels.feishu.renderMode card"
fi

# 5. 检查 Agent
echo "🤖 检查 Agent..."
AGENT_COUNT=$(openclaw agents list 2>/dev/null | grep -c "agent" || echo "0")
if [ "$AGENT_COUNT" -ge 5 ]; then
    echo "✅ Agent 数量：$AGENT_COUNT"
else
    echo "⚠️ Agent 数量不足（当前：$AGENT_COUNT，推荐：≥5）"
fi

echo ""
echo "✅ 验证完成！"
echo ""
echo "📋 运行测试用例："
echo "  cd tests/"
echo "  ./run-tests.sh"
