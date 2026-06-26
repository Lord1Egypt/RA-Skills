#!/usr/bin/env bash
source "$(dirname "$0")/_common.sh"
[[ $# -lt 2 ]] && { echo "Usage: $0 <project_id> <message> [--choice <asset_id>]" >&2; exit 2; }
pid="$1"; msg="$2"; shift 2
choice=""
while [[ $# -gt 0 ]]; do
    case "$1" in --choice) choice="$2"; shift 2 ;; *) shift ;; esac
done
ts=$(date +%s000)
if [[ -n "$choice" ]]; then
    body=$(jq -nc --arg pid "$pid" --arg msg "$msg" --arg ts "$ts" --arg ch "$choice" \
        '{project_id:$pid, timestamp:$ts, user_visible:true, native_inputs:{text:$msg}, choices:{preview_id:$ch}}')
else
    body=$(jq -nc --arg pid "$pid" --arg msg "$msg" --arg ts "$ts" \
        '{project_id:$pid, timestamp:$ts, user_visible:true, native_inputs:{text:$msg}}')
fi
pexo_post_sse_ack "/api/chat" "$body" "20"
jq -nc --arg pid "$pid" --arg ts "$ts" \
    '{"projectId": $pid, "status": "submitted", "submissionMode": "async", "submittedAt": $ts, "pollAfterSeconds": 60}'
