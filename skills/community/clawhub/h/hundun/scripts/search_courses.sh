#!/usr/bin/env bash
# 关键字搜课 - GET /aia/api/v1/courses/search?keyword=xxx
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

keyword="$1"
if [[ -z "$keyword" ]]; then
    echo "用法: $0 <关键词>" >&2
    exit 1
fi

load_config || exit 1
collect_skill_intent "关键字搜课：$keyword" "skill_search_keyword" "关键字搜课" "course" "course_search" "search_courses" "$keyword" "$keyword"
path="/aia/api/v1/courses/search?keyword=$(urlencode "$keyword")"
raw=$(api_get "$path")
parse_response "$raw" || exit 1
