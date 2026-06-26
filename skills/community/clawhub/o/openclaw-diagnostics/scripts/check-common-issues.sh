#!/bin/bash
# OpenClaw Doctor Pro - 常见问题检查
# 用法: ./check-common-issues.sh

CONFIG_PATH="$HOME/.openclaw/openclaw.json"

echo "🔍 OpenClaw 常见问题检查"
echo "========================"

if [ ! -f "$CONFIG_PATH" ]; then
    echo "❌ 配置文件不存在: $CONFIG_PATH"
    exit 1
fi

CONFIG=$(cat "$CONFIG_PATH")

# 检查 1: groupPolicy 配置
echo ""
echo "📋 检查 groupPolicy..."
if echo "$CONFIG" | grep -q '"groupPolicy"'; then
    GP=$(echo "$CONFIG" | grep -o '"groupPolicy"[^,]*' | head -1)
    if echo "$GP" | grep -q '"open"'; then
        echo "   ✅ groupPolicy: open (允许所有群)"
    elif echo "$GP" | grep -q '"denylist"'; then
        echo "   ⚠️  groupPolicy: denylist (黑名单模式)"
    elif echo "$GP" | grep -q '"allowlist"'; then
        echo "   ⚠️  groupPolicy: allowlist (白名单模式)"
    else
        echo "   ❓ groupPolicy: 未知配置"
        echo "      $GP"
    fi
else
    echo "   ℹ️  未配置 groupPolicy (使用默认值)"
fi

# 检查 2: ackReactionScope 配置
echo ""
echo "📋 检查 ackReactionScope..."
if echo "$CONFIG" | grep -q '"ackReactionScope"'; then
    ARS=$(echo "$CONFIG" | grep -o '"ackReactionScope"[^,]*' | head -1)
    if echo "$ARS" | grep -q '"group-mentions"'; then
        echo "   ⚠️  ackReactionScope: group-mentions"
        echo "      → 机器人只回复 @ 它的消息"
    elif echo "$ARS" | grep -q '"all"'; then
        echo "   ✅ ackReactionScope: all (回复所有消息)"
    else
        echo "   ❓ ackReactionScope: 未知配置"
        echo "      $ARS"
    fi
else
    echo "   ℹ️  未配置 ackReactionScope (使用默认值)"
fi

# 检查 3: 模型配置
echo ""
echo "📋 检查模型配置..."
if echo "$CONFIG" | grep -q '"model"'; then
    MODEL=$(echo "$CONFIG" | grep -o '"model"[^,]*' | head -1)
    echo "   当前模型: $MODEL"
else
    echo "   ℹ️  未显式配置模型 (使用默认值)"
fi

# 检查 4: 渠道配置
echo ""
echo "📋 检查渠道配置..."
CHANNELS=$(echo "$CONFIG" | grep -o '"channels"[^]]*]' | head -1)
if [ -n "$CHANNELS" ]; then
    echo "   已配置渠道:"
    echo "$CHANNELS" | grep -oE '"[^"]+"\s*:' | sed 's/://g' | while read ch; do
        echo "     - $ch"
    done
else
    echo "   ℹ️  未配置渠道"
fi

# 检查 5: 认证配置
echo ""
echo "📋 检查认证配置..."
if echo "$CONFIG" | grep -q '"auth"'; then
    echo "   ✅ 已配置 auth"
else
    echo "   ⚠️  未配置 auth（可能影响某些功能）"
fi

echo ""
echo "========================"
echo "✅ 检查完成"
