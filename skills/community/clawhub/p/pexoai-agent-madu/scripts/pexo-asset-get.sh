#!/usr/bin/env bash
source "$(dirname "$0")/_common.sh"
project_id="$1"
asset_id="$2"
[[ -z "$project_id" || -z "$asset_id" ]] && { echo "Usage: $0 <project_id> <asset_id>" >&2; exit 1; }
result=$(pexo_get "/api/biz/projects/$project_id/assets/$asset_id")
echo "$result"