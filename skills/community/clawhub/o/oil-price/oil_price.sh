#!/bin/bash
# 油价查询技能
# 来源：https://v2.xxapi.cn/api/oilPrice
# 返回：全国各省市油价信息（无需 API Key）

set -e

# API 配置
API_URL="https://v2.xxapi.cn/api/oilPrice"

# 获取油价信息
RESPONSE=$(curl -s --max-time 15 "${API_URL}" 2>/dev/null || echo "")

if [ -z "$RESPONSE" ]; then
    echo "Error: Failed to fetch oil price data" >&2
    exit 1
fi

# 解析响应
CODE=$(echo "$RESPONSE" | jq -r '.code' 2>/dev/null || echo "")
if [ "$CODE" != "200" ]; then
    MSG=$(echo "$RESPONSE" | jq -r '.msg' 2>/dev/null || echo "Unknown error")
    echo "Error: API returned code $CODE - $MSG" >&2
    exit 1
fi

# 提取油价数据（按地区名过滤）
echo "$RESPONSE" | jq -r '.data | .[] | "\(.regionName)|\(.n92)|\(.n95)|\(.n98)|\(.n0)"' 2>/dev/null
