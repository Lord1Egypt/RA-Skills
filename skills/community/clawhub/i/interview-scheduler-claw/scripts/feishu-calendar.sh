#!/usr/bin/env bash
# feishu-calendar.sh — 飞书日历 CLI（面试协调专用，支持视频会议）
# 用法：
#   ./scripts/feishu-calendar.sh token                    # 获取 access token
#   ./scripts/feishu-calendar.sh freebusy <user_id> <start> <end>  # 查询空闲（单用户）
#   ./scripts/feishu-calendar.sh freebusy-batch <user_ids_json> <start> <end>  # 批量查询
#   ./scripts/feishu-calendar.sh primary-calendar          # 获取主日历 ID
#   ./scripts/feishu-calendar.sh create-event <cal_id> <title> <start_ts> <end_ts> [desc] [--meeting]
#   ./scripts/feishu-calendar.sh get-event <cal_id> <event_id>  # 获取日程详情（含会议链接）
#   ./scripts/feishu-calendar.sh add-attendees <cal_id> <event_id> <attendees.json>
#   ./scripts/feishu-calendar.sh list-events <cal_id> <start_rfc3339> <end_rfc3339>
#   ./scripts/feishu-calendar.sh delete-event <cal_id> <event_id>
#
# 时间戳格式：秒级 Unix 时间戳字符串，如 "1711497600"
# RFC3339 格式：如 "2026-03-26T14:00:00+08:00"
#
# 环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET

set -euo pipefail

BASE_URL="https://open.feishu.cn/open-apis"

# 缓存 token 到文件（2小时有效）
TOKEN_CACHE="/tmp/feishu_interview_token_cache"

get_token() {
  if [[ -f "$TOKEN_CACHE" ]]; then
    cached=$(cat "$TOKEN_CACHE")
    expire=$(echo "$cached" | jq -r '.expire // 0')
    now=$(date +%s)
    if (( now < expire )); then
      echo "$cached" | jq -r '.token'
      return
    fi
  fi

  local resp
  resp=$(curl -s -X POST "$BASE_URL/auth/v3/tenant_access_token/internal" \
    -H "Content-Type: application/json" \
    -d "{\"app_id\":\"${FEISHU_APP_ID}\",\"app_secret\":\"${FEISHU_APP_SECRET}\"}")

  local token expire_at
  token=$(echo "$resp" | jq -r '.tenant_access_token // empty')
  if [[ -z "$token" ]]; then
    echo "ERROR: Failed to get token: $resp" >&2
    exit 1
  fi
  expire_at=$(( $(date +%s) + 7000 ))
  echo "{\"token\":\"$token\",\"expire\":$expire_at}" > "$TOKEN_CACHE"
  echo "$token"
}

case "${1:-}" in
  token)
    get_token
    ;;

  freebusy)
    if [[ $# -ne 4 ]]; then echo "用法: freebusy <user_id> <start_rfc3339> <end_rfc3339>" >&2; exit 1; fi
    user_id="$2"; time_min="$3"; time_max="$4"
    token=$(get_token)
    curl -s -X POST "$BASE_URL/calendar/v4/freebusy/list?user_id_type=open_id" \
      -H "Authorization: Bearer $token" \
      -H "Content-Type: application/json" \
      -d "{\"user_id\":\"$user_id\",\"time_min\":\"$time_min\",\"time_max\":\"$time_max\",\"only_busy\":false}"
    ;;

  freebusy-batch)
    if [[ $# -ne 4 ]]; then echo "用法: freebusy-batch <user_ids.json> <start_rfc3339> <end_rfc3339>" >&2; exit 1; fi
    user_ids_file="$2"; time_min="$3"; time_max="$4"
    user_ids=$(cat "$user_ids_file")
    token=$(get_token)
    curl -s -X POST "$BASE_URL/calendar/v4/freebusy/batch?user_id_type=open_id" \
      -H "Authorization: Bearer $token" \
      -H "Content-Type: application/json" \
      -d "{\"user_ids\":$user_ids,\"time_min\":\"$time_min\",\"time_max\":\"$time_max\",\"only_busy\":false}"
    ;;

  primary-calendar)
    token=$(get_token)
    resp=$(curl -s -X GET "$BASE_URL/calendar/v4/calendars" \
      -H "Authorization: Bearer $token")
    echo "$resp" | jq -r '.data.calendar_list[] | select(.type=="primary") | .calendar_id // empty'
    ;;

  create-event)
    if [[ $# -lt 5 ]]; then echo "用法: create-event <cal_id> <title> <start_ts> <end_ts> [desc] [--meeting]" >&2; exit 1; fi
    cal_id="$2"; summary="$3"; start_ts="$4"; end_ts="$5"
    desc=""; meeting=false
    shift 5
    for arg in "$@"; do
      case "$arg" in
        --meeting) meeting=true ;;
        *) desc="$arg" ;;
      esac
    done
    token=$(get_token)
    local_body=$(jq -n \
      --arg s "$summary" --arg st "$start_ts" --arg et "$end_ts" \
      '{
        summary: $s,
        need_notification: true,
        start_time: {timestamp: $st},
        end_time: {timestamp: $et},
        color: -1,
        visibility: 0,
        reminders: [{minutes: 15}]
      }')
    if [[ -n "$desc" ]]; then
      local_body=$(echo "$local_body" | jq --arg d "$desc" '. + {description: $d}')
    fi
    if $meeting; then
      local_body=$(echo "$local_body" | jq '. + {
        meeting_settings: {
          is_meeting: true,
          meeting_type: 0,
          require_attendee_info: false
        }
      }')
    fi
    curl -s -X POST "$BASE_URL/calendar/v4/calendars/$cal_id/events" \
      -H "Authorization: Bearer $token" \
      -H "Content-Type: application/json" \
      -d "$local_body"
    ;;

  get-event)
    if [[ $# -ne 3 ]]; then echo "用法: get-event <cal_id> <event_id>" >&2; exit 1; fi
    cal_id="$2"; event_id="$3"
    token=$(get_token)
    curl -s -X GET "$BASE_URL/calendar/v4/calendars/$cal_id/events/$event_id" \
      -H "Authorization: Bearer $token"
    ;;

  add-attendees)
    if [[ $# -ne 4 ]]; then echo "用法: add-attendees <cal_id> <event_id> <attendees.json>" >&2; exit 1; fi
    cal_id="$2"; event_id="$3"; attendees_file="$4"
    attendees=$(cat "$attendees_file")
    token=$(get_token)
    curl -s -X POST "$BASE_URL/calendar/v4/calendars/$cal_id/events/$event_id/attendees?user_id_type=open_id" \
      -H "Authorization: Bearer $token" \
      -H "Content-Type: application/json" \
      -d "{\"attendees\":$attendees,\"need_notification\":true}"
    ;;

  list-events)
    if [[ $# -ne 4 ]]; then echo "用法: list-events <cal_id> <start_rfc3339> <end_rfc3339>" >&2; exit 1; fi
    cal_id="$2"; time_min="$3"; time_max="$4"
    token=$(get_token)
    curl -s -X GET "$BASE_URL/calendar/v4/calendars/$cal_id/events?time_min=$time_min&time_max=$time_max&page_size=50" \
      -H "Authorization: Bearer $token"
    ;;

  delete-event)
    if [[ $# -ne 3 ]]; then echo "用法: delete-event <cal_id> <event_id>" >&2; exit 1; fi
    cal_id="$2"; event_id="$3"
    token=$(get_token)
    curl -s -X DELETE "$BASE_URL/calendar/v4/calendars/$cal_id/events/$event_id" \
      -H "Authorization: Bearer $token"
    ;;

  *)
    echo "飞书日历 CLI（面试协调版）"
    echo ""
    echo "用法: $0 <command> [args...]"
    echo ""
    echo "命令："
    echo "  token                                  获取 access token"
    echo "  freebusy <user_id> <start> <end>      查询单人空闲"
    echo "  freebusy-batch <ids.json> <start> <end>  批量查询空闲"
    echo "  primary-calendar                       获取主日历 ID"
    echo "  create-event <cal> <title> <start> <end> [desc] [--meeting]"
    echo "                                         创建日程（--meeting 自动创建飞书视频会议）"
    echo "  get-event <cal_id> <event_id>          获取日程详情（含 meeting_url）"
    echo "  add-attendees <cal> <evt> <json>       添加参会者"
    echo "  list-events <cal> <start> <end>        查询日程列表"
    echo "  delete-event <cal> <evt>               删除日程"
    echo ""
    echo "时间戳：秒级 Unix 时间戳字符串（如 \"1711497600\"）"
    echo "RFC3339：如 \"2026-03-26T14:00:00+08:00\""
    exit 1
    ;;
esac
