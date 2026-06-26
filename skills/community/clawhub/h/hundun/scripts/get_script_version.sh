#!/usr/bin/env bash
# 获取文稿版本 - GET /aia/api/v1/courses/{course_id}/script/version（不计入用量）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

course_id="$1"
if [[ -z "$course_id" ]]; then
    echo "用法: $0 <课程ID>" >&2
    exit 1
fi

load_config || exit 1
collect_skill_intent "获取课程文稿版本：course_id=$course_id" "skill_get_script_version" "课程文稿版本" "course" "course_script_version" "get_script_version" "$course_id" "获取课程文稿版本"
raw=$(api_get "/aia/api/v1/courses/$course_id/script/version")
parse_response "$raw"
