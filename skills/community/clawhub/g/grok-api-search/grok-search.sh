#!/bin/bash
# Grok 搜索脚本
# 使用 grok-4.1-fast 模型进行网络搜索
# 
# 配置方式：
#   1. 设置环境变量 GROK_API_KEY
#   2. 可选：设置 GROK_API_URL（默认使用中转端点）

# === 配置区域 ===
# 默认使用中转 API（推荐）
API_URL="${GROK_API_URL:-https://apipro.maynor1024.live/v1/chat/completions}"
API_KEY="${GROK_API_KEY:-YOUR_API_KEY_HERE}"
MODEL="${GROK_MODEL:-grok-4.1-fast}"

# 代理设置（可选，国内访问官方API时可能需要）
# PROXY="http://127.0.0.1:7890"
# === 配置结束 ===

# 获取查询内容
QUERY="$*"

if [ -z "$QUERY" ]; then
    echo "用法: grok-search.sh <搜索内容>"
    echo ""
    echo "配置方式："
    echo "  export GROK_API_KEY=\"your-api-key\""
    echo "  export GROK_API_URL=\"https://api.x.ai/v1\"  # 可选，默认使用中转"
    exit 1
fi

# 检查 API Key
if [ "$API_KEY" = "YOUR_API_KEY_HERE" ]; then
    echo "❌ 错误：请先配置 API Key"
    echo ""
    echo "配置方式："
    echo "  export GROK_API_KEY=\"your-api-key\""
    echo ""
    echo "中转 API 推荐："
    echo "  - 成本更低"
    echo "  - 国内网络稳定"
    exit 1
fi

# 设置代理（如果配置了）
if [ -n "$PROXY" ]; then
    export http_proxy="$PROXY"
    export https_proxy="$PROXY"
fi

# 调用 API
curl -s "$API_URL" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
        \"model\": \"$MODEL\",
        \"messages\": [
            {
                \"role\": \"system\",
                \"content\": \"你是一个网络搜索助手。请根据用户的问题，搜索并提供准确、实时的信息。回答要简洁明了，包含关键信息和来源。\"
            },
            {
                \"role\": \"user\",
                \"content\": \"请搜索并回答：$QUERY\"
            }
        ],
        \"max_tokens\": 2000
    }" 2>/dev/null | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if 'error' in data:
        print(f\"❌ API 错误: {data['error'].get('message', '未知错误')}\")
    else:
        content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
        print(content)
except Exception as e:
    print(f'❌ 请求失败: {e}')
"
