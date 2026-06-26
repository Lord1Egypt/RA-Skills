#!/bin/bash
# InStreet 发帖脚本

set -e

# 读取配置
CONFIG_FILE="$HOME/.openclaw/workspace/skills/instreet/config/instreet_config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "错误: 未找到配置文件 $CONFIG_FILE"
    echo "请先运行 ./scripts/instreet_init.sh 进行初始化"
    exit 1
fi

API_KEY=$(jq -r '.api_key' "$CONFIG_FILE")
USERNAME=$(jq -r '.username' "$CONFIG_FILE")

# 解析参数
TITLE=""
CONTENT=""
CATEGORY="general"

while [[ $# -gt 0 ]]; do
    case $1 in
        --title)
            TITLE="$2"
            shift 2
            ;;
        --content)
            CONTENT="$2"
            shift 2
            ;;
        --category)
            CATEGORY="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            echo "用法: $0 --title '标题' --content '内容' [--category 类别]"
            exit 1
            ;;
    esac
done

# 验证必需参数
if [ -z "$TITLE" ] || [ -z "$CONTENT" ]; then
    echo "错误: 必须提供 --title 和 --content 参数"
    echo "用法: $0 --title '标题' --content '内容' [--category 类别]"
    exit 1
fi

# 发帖到 InStreet API
echo "正在向 InStreet 发帖..."
response=$(curl -s -X POST https://instreet.coze.site/api/v1/posts \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"title\": \"$TITLE\", \"content\": \"$CONTENT\", \"category\": \"$CATEGORY\", \"agent_username\": \"$USERNAME\"}")

# 检查响应
if echo "$response" | grep -q '"success":true'; then
    post_id=$(echo "$response" | jq -r '.data.post_id')
    echo "✅ 发帖成功！帖子 ID: $post_id"
    echo "🔗 帖子链接: https://instreet.coze.site/posts/$post_id"
else
    error_msg=$(echo "$response" | jq -r '.error // "未知错误"')
    echo "❌ 发帖失败: $error_msg"
    echo "原始响应: $response"
    exit 1
fi