#!/bin/bash
# Misskey 获取当前用户信息
# 用法: whoami.sh

set -e

HOST="${MISSKEY_HOST:-https://maid.lat}"
TOKEN="${MISSKEY_TOKEN}"

if [ -z "$TOKEN" ]; then
    echo "错误: 请设置 MISSKEY_TOKEN 环境变量"
    exit 1
fi

RESULT=$(curl -s -X POST "$HOST/api/i" \
    -H "Content-Type: application/json" \
    -d "{\"i\": \"$TOKEN\"}")

if echo "$RESULT" | grep -q '"id"'; then
    echo "$RESULT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f\"用户名: @{d.get('username', '')}\")
print(f\"昵称: {d.get('name', '')}\")
print(f\"ID: {d.get('id', '')}\")
desc = d.get('description', '') or ''
print(f\"简介: {desc[:100]}\")
print(f\"关注: {d.get('followingCount', 0)}\")
print(f\"粉丝: {d.get('followersCount', 0)}\")
print(f\"发帖数: {d.get('notesCount', 0)}\")
"
else
    echo "获取失败: $RESULT"
    exit 1
fi
