#!/usr/bin/env bash
# myapp_update: 更新已有应用
#
# 输入（环境变量形式）：
#   app_id         必填
#   query          必填
#   html_content   必填
#   features       必填，JSON 字符串数组
#   icon_base64    可选
#   tag            可选，'app' 或 'doc'（不传则保留原值）

export MYAPP_CURL_MAX_TIME="${MYAPP_CURL_MAX_TIME:-300}"
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

: "${app_id:?param app_id required}"
: "${query:?param query required}"
: "${html_content:?param html_content required}"
: "${features:?param features (JSON array string) required}"

payload=$(jq -n \
  --argjson app_id "$app_id" \
  --arg query "$query" \
  --arg html_content "$html_content" \
  --argjson features "$features" \
  --arg icon_base64 "${icon_base64:-}" \
  --arg tag "${tag:-}" \
  '{
    app_id: $app_id,
    query: $query,
    html_content: $html_content,
    features: $features,
    icon_base64: (if $icon_base64 == "" then null else $icon_base64 end),
    tag: (if $tag == "" then null else $tag end)
  }')

curl "${CURL_OPTS[@]}" -X POST "${MYAPP_API_BASE}/myapp/update" --data-binary "$payload"
