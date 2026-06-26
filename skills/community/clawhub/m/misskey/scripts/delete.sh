#!/bin/bash
# Misskey 删除帖子脚本
# 用法: delete.sh <note_id>

set -e

HOST="${MISSKEY_HOST:-https://maid.lat}"
TOKEN="${MISSKEY_TOKEN}"

if [ -z "$TOKEN" ]; then
    echo "错误: 请设置 MISSKEY_TOKEN 环境变量"
    exit 1
fi

if [ -z "$1" ]; then
    echo "用法: delete.sh <帖子ID>"
    echo "示例: delete.sh ak4lrcfalen102bc"
    exit 1
fi

NOTE_ID="$1"

echo "删除帖子: $NOTE_ID"
RESULT=$(curl -s -X POST "$HOST/api/notes/delete" \
    -H "Content-Type: application/json" \
    -d "{\"i\": \"$TOKEN\", \"noteId\": \"$NOTE_ID\"}")

if [ -z "$RESULT" ] || [ "$RESULT" = "{}" ]; then
    echo "删除成功！"
else
    echo "删除失败: $RESULT"
    exit 1
fi
