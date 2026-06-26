#!/usr/bin/env bash
# myapp_ping: 安装就绪自检
#
# 输入：
#   session_id     必填（来自 install_prompt）
#   dumi_id        必填
#   cuid           必填（可空）
#   skill_version  必填（如 "1.0.0"）

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

: "${session_id:?param session_id required}"
: "${dumi_id:?param dumi_id required}"
: "${cuid?param cuid required (can be empty)}"
: "${skill_version:?param skill_version required}"

payload=$(jq -n \
  --arg session_id "$session_id" \
  --arg dumi_id "$dumi_id" \
  --arg cuid "$cuid" \
  --arg skill_version "$skill_version" \
  '{
    session_id: $session_id,
    dumi_id: $dumi_id,
    cuid: $cuid,
    skill_version: $skill_version
  }')

curl "${CURL_OPTS[@]}" -X POST "${MYAPP_API_BASE}/myapp/skill/ping" --data-binary "$payload"
