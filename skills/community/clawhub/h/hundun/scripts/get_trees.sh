#!/usr/bin/env bash
# 课程体系树 - GET /aia/api/v1/courses/trees
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

load_config || exit 1
# 固定流程：用户意图收集（埋点）
collect_skill_intent "获取课程体系树" "skill_search_tree" "课程体系搜课" "course" "course_tree" "get_trees" "获取课程体系树" "获取课程体系树"
raw=$(api_get "/aia/api/v1/courses/trees")
parse_response "$raw"
