#!/bin/bash
# IQS Search - 阿里云信息查询服务联网搜索 CLI
# 用法：./iqs-search.sh <查询语句>
# 环境变量：TONGXIAO_API_KEY (必填)

set -e

# 检查 API Key
if [ -z "$TONGXIAO_API_KEY" ]; then
    echo "错误：请设置环境变量 TONGXIAO_API_KEY" >&2
    echo "示例：export TONGXIAO_API_KEY='your-api-key'" >&2
    exit 1
fi

# 检查查询参数
if [ -z "$1" ]; then
    echo "用法：$0 <查询语句>" >&2
    echo "示例：$0 '阿里巴巴最新财报'" >&2
    exit 1
fi

QUERY="$1"
BACKEND="https://cloud-iqs.aliyuncs.com"
TIMEOUT=10

# 调用 genericSearch 接口
URL="${BACKEND}/search/genericSearch?query=$(echo "$QUERY" | jq -sRr @uri)"

# 发送请求
RESPONSE=$(curl -s -w "\n%{http_code}" \
    -H "X-API-Key: $TONGXIAO_API_KEY" \
    -H "Accept: application/json" \
    --max-time "$TIMEOUT" \
    "$URL")

# 分离 HTTP 状态码和响应体
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

# 检查响应状态
if [ "$HTTP_CODE" != "200" ]; then
    echo "错误：API 请求失败 (HTTP $HTTP_CODE)" >&2
    echo "$BODY" >&2
    exit 1
fi

# 解析并输出结果
echo "$BODY" | jq -r '
if .pageItems then
    .pageItems | .[] |
    "
---
标题：\(.title // "无标题")
链接：\(.link // "无链接")
摘要：\(.snippet // "无摘要")
正文：\(.mainText // "无正文")
"
else
    "未找到相关结果"
end
'
