#!/usr/bin/env bash
#
# 网页内容抓取 - 基于心流搜索 API
#
# 用法: bash web_fetch.sh <url>
#   url: 目标网页 URL（必填）
#

set -euo pipefail

URL="${1:?用法: bash web_fetch.sh <url>}"

API_KEY="${IFLOW_API_KEY:-}"
if [[ -z "$API_KEY" ]]; then
  echo "错误: 未设置 IFLOW_API_KEY 环境变量" >&2
  echo "请先设置: export IFLOW_API_KEY=your_api_key" >&2
  exit 1
fi

BASE_URL="https://platform.iflow.cn"

curl -s -X POST "${BASE_URL}/api/search/webFetch" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d "{
    \"url\": \"${URL}\"
  }"
