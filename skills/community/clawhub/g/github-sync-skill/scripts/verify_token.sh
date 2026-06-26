#!/bin/bash

# Verify GitHub Token - 验证 Token 权限
# 用法：verify_token.sh <token>

TOKEN="${1:-$GITHUB_TOKEN}"

if [ -z "$TOKEN" ]; then
    echo "❌ Token 为空"
    echo "用法：$0 <token>"
    echo "   或先设置 GITHUB_TOKEN 环境变量"
    exit 1
fi

echo "============================================================"
echo "  GitHub Token 验证"
echo "============================================================"
echo ""

# 验证 Token 所有者
echo "📋 验证 Token 所有者..."
response=$(curl -s -H "Authorization: token $TOKEN" https://api.github.com/user)

if echo "$response" | grep -q '"login"'; then
    login=$(echo "$response" | jq -r '.login')
    echo "✅ Token 所有者：$login"
else
    echo "❌ Token 无效"
    echo "响应：$response"
    exit 1
fi

# 验证 Token Scopes
echo ""
echo "📋 验证 Token Scopes..."
scopes=$(curl -s -I -H "Authorization: token $TOKEN" https://api.github.com | grep -i x-oauth-scopes | tr -d '\r')

if [ -n "$scopes" ]; then
    echo "   $scopes"

    # 检查是否有 repo 权限
    if echo "$scopes" | grep -qi "repo"; then
        echo "✅ 具有 repo 权限"
    else
        echo "⚠️  警告：Token 缺少 repo 权限"
        echo "   请在 GitHub 重新创建 Token，勾选 'repo' scope"
    fi
else
    echo "⚠️  无法获取 Scopes 信息"
fi

# 验证仓库权限
echo ""
echo "📋 验证仓库权限 (kuiilabs/claude-skills)..."
response=$(curl -s -H "Authorization: token $TOKEN" \
    https://api.github.com/repos/kuiilabs/claude-skills)

if echo "$response" | grep -q '"permissions"'; then
    push=$(echo "$response" | jq -r '.permissions.push')
    admin=$(echo "$response" | jq -r '.permissions.admin')

    echo "   Push: $push"
    echo "   Admin: $admin"

    if [ "$push" = "true" ]; then
        echo "✅ 具有写入权限"
    else
        echo "❌ 没有写入权限"
        exit 1
    fi
else
    echo "⚠️  仓库可能不存在或无权访问"
fi

echo ""
echo "============================================================"
echo "  验证完成"
echo "============================================================"
