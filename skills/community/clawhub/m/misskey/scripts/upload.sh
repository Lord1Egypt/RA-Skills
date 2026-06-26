#!/bin/bash
# Misskey 上传文件脚本
# 用法: upload.sh "/path/to/file" [folder_id]

set -e

HOST="${MISSKEY_HOST:-https://maid.lat}"
TOKEN="${MISSKEY_TOKEN}"

if [ -z "$TOKEN" ]; then
    echo "错误: 请设置 MISSKEY_TOKEN 环境变量"
    exit 1
fi

if [ -z "$1" ]; then
    echo "用法: upload.sh <文件路径> [文件夹ID]"
    exit 1
fi

FILE="$1"
FOLDER_ID="${2:-}"

if [ ! -f "$FILE" ]; then
    echo "错误: 文件不存在: $FILE"
    exit 1
fi

# 构建请求
CMD="curl -s -X POST '$HOST/api/drive/files/create' -H 'Authorization: Bearer $TOKEN' -F 'file=@$FILE'"

if [ -n "$FOLDER_ID" ]; then
    CMD="$CMD -F 'folderId=$FOLDER_ID'"
fi

# 上传
echo "上传: $FILE"
RESULT=$(eval "$CMD")

# 检查结果
if echo "$RESULT" | grep -q '"id"'; then
    FILE_ID=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")
    FILE_NAME=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('name',''))")
    echo "上传成功！"
    echo "文件ID: $FILE_ID"
    echo "文件名: $FILE_NAME"
else
    echo "上传失败: $RESULT"
    exit 1
fi
