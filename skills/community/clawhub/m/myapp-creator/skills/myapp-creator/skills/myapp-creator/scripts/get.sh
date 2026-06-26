#!/usr/bin/env bash
# myapp_get: 读取应用详情（用于更新前拿旧 features）
#
# 输入：
#   app_id   必填

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

: "${app_id:?param app_id required}"

# 校验 app_id 是数字
if ! [[ "$app_id" =~ ^[0-9]+$ ]]; then
  echo "error: app_id must be a positive integer" >&2
  exit 2
fi

curl "${CURL_OPTS[@]}" -X GET "${MYAPP_API_BASE}/myapp/get?app_id=${app_id}"
