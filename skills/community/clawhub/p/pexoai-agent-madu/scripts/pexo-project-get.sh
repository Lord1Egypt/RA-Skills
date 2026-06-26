#!/usr/bin/env bash
source "$(dirname "$0")/_common.sh"
project_id="$1"
[[ -z "$project_id" ]] && { echo "Usage: $0 <project_id>" >&2; exit 1; }
body=$(jq -nc '{project_id: $project_id}')
result=$(pexo_get "/api/biz/projects/$project_id" "-G" "--data-urlencode" "fields=nextAction,nextActionHint,recentMessages")
echo "$result"