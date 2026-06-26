#!/usr/bin/env bash
# AIA telemetry 事件上报 - POST /aia/api/v1/telemetry/events（需鉴权）
# 用法: telemetry_event.sh <event_name> <request_id> [extra_json]
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

event_name="$1"
request_id="$2"
if [[ $# -ge 3 ]]; then
    extra_json="$3"
else
    extra_json="{}"
fi
if [[ -z "$event_name" || -z "$request_id" ]]; then
    echo "用法: $0 <event_name> <request_id> [extra_json]" >&2
    exit 1
fi

load_config || exit 1
ts=$(date +%s)

if command -v jq &>/dev/null; then
    if ! printf '%s' "$extra_json" | jq -e . >/dev/null 2>&1; then
        echo "错误：extra_json 必须是合法 JSON" >&2
        exit 1
    fi
    properties=$(printf '%s' "$extra_json" | jq -c --arg source "hundun_skill" '. + {source:$source}')
    body=$(jq -n \
        --arg event_name "$event_name" \
        --arg request_id "$request_id" \
        --arg properties "$properties" \
        --arg client_version "$HUNDUN_SKILL_VERSION" \
        --argjson timestamp "$ts" \
        '{events:[{event_name:$event_name,client_id:"hundun-skill",platform:"codex",arch:"skill",client_version:$client_version,module_key:"core",module_version:"1.0.0",scene_value:"hundun_skill",request_id:$request_id,timestamp:$timestamp,properties:$properties}]}')
elif command -v python3 &>/dev/null || command -v python &>/dev/null; then
    py=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
    body=$("$py" -c 'import json,sys; extra=json.loads(sys.argv[3]); extra["source"]="hundun_skill"; print(json.dumps({"events":[{"event_name":sys.argv[1],"client_id":"hundun-skill","platform":"codex","arch":"skill","client_version":sys.argv[5],"module_key":"core","module_version":"1.0.0","scene_value":"hundun_skill","request_id":sys.argv[2],"timestamp":int(sys.argv[4]),"properties":json.dumps(extra, ensure_ascii=False)}]}, ensure_ascii=False))' "$event_name" "$request_id" "$extra_json" "$ts" "$HUNDUN_SKILL_VERSION") || exit 1
else
    echo "错误：需要 jq 或 python/python3 生成 JSON，请安装其一" >&2
    exit 1
fi

raw=$(api_post "/aia/api/v1/telemetry/events" "$body")
parse_response "$raw"
