#!/usr/bin/env bash
# AIA 发现页推荐课程 - GET /aia/api/v1/discovery/recommendations（需鉴权）
# 用法: discovery_recommendations.sh [limit]
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

limit="${1:-}"
load_config || exit 1
collect_skill_intent "浏览发现页推荐课程" "skill_discovery_recommendations" "发现页推荐课程" "course" "discovery_recommendations" "discovery_recommendations" "$limit" "浏览发现页推荐课程"

path="/aia/api/v1/discovery/recommendations"
[[ -n "$limit" ]] && path="${path}?limit=$(urlencode "$limit")"
raw=$(api_get "$path")
parse_response "$raw"
