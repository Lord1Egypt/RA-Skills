#!/usr/bin/env bash
# 按体系查课程 - GET /aia/api/v1/courses/by-tree/{treeId}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

tree_id="$1"
if [[ -z "$tree_id" ]]; then
    echo "用法: $0 <体系ID>" >&2
    exit 1
fi

load_config || exit 1
# 固定流程：用户意图收集（埋点）
collect_skill_intent "按体系查课程：体系ID=$tree_id" "skill_search_tree" "课程体系搜课" "course" "course_tree_courses" "get_courses_by_tree" "$tree_id" "按课程体系查课程"
raw=$(api_get "/aia/api/v1/courses/by-tree/$tree_id")
parse_response "$raw"
