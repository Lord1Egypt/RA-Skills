#!/usr/bin/env bash
# myapp_register: 创建一条新应用
#
# 输入（环境变量形式）：
#   dumi_id        必填
#   cuid           必填（可空字符串）
#   query          必填
#   app_name       必填
#   html_content   必填
#   features       必填，JSON 字符串数组（如 '["a","b"]'）
#   icon_base64    可选
#   tag            可选，'app'（默认）或 'doc'

export MYAPP_CURL_MAX_TIME="${MYAPP_CURL_MAX_TIME:-300}"
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

: "${dumi_id:?param dumi_id required}"
: "${cuid?param cuid required (can be empty)}"
: "${query:?param query required}"
: "${app_name:?param app_name required}"
: "${html_content:?param html_content required}"
: "${features:?param features (JSON array string) required}"

payload=$(jq -n \
  --arg dumi_id "$dumi_id" \
  --arg cuid "$cuid" \
  --arg query "$query" \
  --arg app_name "$app_name" \
  --arg html_content "$html_content" \
  --argjson features "$features" \
  --arg icon_base64 "${icon_base64:-}" \
  --arg tag "${tag:-app}" \
  '{
    dumi_id: $dumi_id,
    cuid: $cuid,
    query: $query,
    app_name: $app_name,
    html_content: $html_content,
    features: $features,
    icon_base64: (if $icon_base64 == "" then null else $icon_base64 end),
    tag: $tag
  }')

curl "${CURL_OPTS[@]}" -X POST "${MYAPP_API_BASE}/myapp/register" --data-binary "$payload"
