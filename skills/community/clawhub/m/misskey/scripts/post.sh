#!/bin/bash
# Misskey 发帖脚本
# 用法: post.sh "内容" [图片1] [图片2] ... [--visibility public|home|followers] [--cw "警告"]

set -e

# 配置
HOST="${MISSKEY_HOST:-https://maid.lat}"
TOKEN="${MISSKEY_TOKEN}"

if [ -z "$TOKEN" ]; then
    echo "错误: 请设置 MISSKEY_TOKEN 环境变量"
    exit 1
fi

# 解析参数
TEXT=""
IMAGES=()
VISIBILITY="public"
CW=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --visibility)
            VISIBILITY="$2"
            shift 2
            ;;
        --cw)
            CW="$2"
            shift 2
            ;;
        -*)
            echo "未知参数: $1"
            exit 1
            ;;
        *)
            # 检查是否是图片文件
            if [[ -f "$1" && "$1" =~ \.(png|jpg|jpeg|gif|webp|bmp)$ ]]; then
                IMAGES+=("$1")
            else
                if [ -z "$TEXT" ]; then
                    TEXT="$1"
                fi
            fi
            shift
            ;;
    esac
done

if [ -z "$TEXT" ] && [ ${#IMAGES[@]} -eq 0 ]; then
    echo "错误: 请提供文本内容或图片"
    exit 1
fi

# 上传图片并获取 file_id
FILE_IDS=""
if [ ${#IMAGES[@]} -gt 0 ]; then
    IDS="["
    FIRST=true
    for IMG in "${IMAGES[@]}"; do
        echo "上传图片: $IMG"
        RESPONSE=$(curl -s -X POST "$HOST/api/drive/files/create" \
            -H "Authorization: Bearer $TOKEN" \
            -F "file=@$IMG")
        
        FILE_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null || echo "")
        
        if [ -z "$FILE_ID" ]; then
            echo "上传失败: $RESPONSE"
            exit 1
        fi
        
        if [ "$FIRST" = true ]; then
            FIRST=false
        else
            IDS+=","
        fi
        IDS+="\"$FILE_ID\""
    done
    IDS+="]"
    FILE_IDS=", \"fileIds\": $IDS"
fi

# 构建请求体
REQUEST=$(cat <<EOF
{
    "i": "$TOKEN",
    "text": $(echo "$TEXT" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))"),
    "visibility": "$VISIBILITY"$FILE_IDS
EOF
)

if [ -n "$CW" ]; then
    REQUEST=$(echo "$REQUEST" | python3 -c "import sys,json; d=json.load(sys.stdin); d['cw']=$(echo "$CW" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))'); print(json.dumps(d))")
fi

REQUEST="$REQUEST}"

# 发帖
echo "发帖中..."
RESULT=$(curl -s -X POST "$HOST/api/notes/create" \
    -H "Content-Type: application/json" \
    -d "$REQUEST")

# 检查结果
if echo "$RESULT" | grep -q '"createdNote"'; then
    NOTE_ID=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('createdNote',{}).get('id',''))")
    echo "发帖成功！"
    echo "链接: $HOST/notes/$NOTE_ID"
else
    echo "发帖失败: $RESULT"
    exit 1
fi
