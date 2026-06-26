#!/usr/bin/env bash
# AIA Skill 模块清单 - GET /aia/api/v1/skill/modules/manifest（需鉴权）
# 用法: get_skill_modules.sh [skill_id]
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

skill_id="${1:-hd_skill}"
load_config || exit 1

path="/aia/api/v1/skill/modules/manifest?skill_id=$(urlencode "$skill_id")"
raw=$(api_get "$path")
parse_response "$raw"
