#!/usr/bin/env bash
#
# 图片搜索 - 基于心流搜索 API
#
# 用法: bash image_search.sh <keywords> [num]
#   keywords: 搜索关键词（必填）
#   num:      返回结果数量（可选，默认 15）
#

set -euo pipefail

KEYWORDS="${1:?用法: bash image_search.sh <keywords> [num]}"
NUM="${2:-15}"

API_KEY="${IFLOW_API_KEY:-}"
if [[ -z "$API_KEY" ]]; then
  echo "错误: 未设置 IFLOW_API_KEY 环境变量" >&2
  echo "请先设置: export IFLOW_API_KEY=your_api_key" >&2
  exit 1
fi

BASE_URL="https://platform.iflow.cn"

curl -s -X POST "${BASE_URL}/api/search/imageSearch" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d "{
    \"keywords\": \"${KEYWORDS}\",
    \"num\": ${NUM}
  }"
