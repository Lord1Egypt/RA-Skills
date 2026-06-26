#!/usr/bin/env bash
# AIA Skill 指定模块详情 - GET /aia/api/v1/skill/modules/:module_key（需鉴权）
# 用法: get_skill_module.sh <module_key> [skill_id]
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

module_key="$1"
skill_id="${2:-hd_skill}"
if [[ -z "$module_key" ]]; then
    echo "用法: $0 <module_key> [skill_id]" >&2
    exit 1
fi

load_config || exit 1
path="/aia/api/v1/skill/modules/$(urlencode "$module_key")?skill_id=$(urlencode "$skill_id")"
raw=$(api_get "$path")
parse_response "$raw"
