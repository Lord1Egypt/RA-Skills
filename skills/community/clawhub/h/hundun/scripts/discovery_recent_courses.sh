#!/usr/bin/env bash
# AIA 最近上线课程 - GET /aia/api/v1/discovery/recent-courses（需鉴权）
# 用法: discovery_recent_courses.sh [limit]
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

limit="${1:-}"
load_config || exit 1
collect_skill_intent "浏览最近上线课程" "skill_discovery_recent_courses" "最近上线课程" "course" "discovery_recent_courses" "discovery_recent_courses" "$limit" "浏览最近上线课程"

path="/aia/api/v1/discovery/recent-courses"
[[ -n "$limit" ]] && path="${path}?limit=$(urlencode "$limit")"
raw=$(api_get "$path")
parse_response "$raw"
