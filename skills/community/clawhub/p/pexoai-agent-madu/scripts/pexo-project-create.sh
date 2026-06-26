#!/usr/bin/env bash
source "$(dirname "$0")/_common.sh"
project_name="${1:-Untitled}"
body=$(jq -nc --arg n "$project_name" '{project_name: $n}')
result=$(pexo_post "/api/biz/projects" "$body")
project_id=$(echo "$result" | jq -r '.data.projectId // empty')
if [[ -z "$project_id" ]]; then
    echo "Error: create project response missing projectId" >&2
    echo "$result" >&2
    exit 1
fi
printf '%s\n' "$project_id"
