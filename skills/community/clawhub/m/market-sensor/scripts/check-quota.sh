#!/bin/bash
# MarketSensor 额度查询脚本
# 用法: ./check-quota.sh

set -e

if [ -z "$MARKETSENSOR_API_KEY" ]; then
  echo "错误: 未设置 MARKETSENSOR_API_KEY 环境变量" >&2
  exit 1
fi

BASE_URL="https://api.marketsensor.ai"
AUTH="Authorization: Bearer $MARKETSENSOR_API_KEY"

echo "==> 查询账户额度..."
curl -s -H "$AUTH" "$BASE_URL/api/open/quota" | python3 -m json.tool 2>/dev/null || \
curl -s -H "$AUTH" "$BASE_URL/api/open/quota"
