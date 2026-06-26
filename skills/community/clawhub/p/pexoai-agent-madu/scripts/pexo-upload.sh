#!/usr/bin/env bash
source "$(dirname "$0")/_common.sh"
project_id="$1"
file_path="$2"
[[ -z "$project_id" || -z "$file_path" ]] && { echo "Usage: $0 <project_id> <file_path>" >&2; exit 1; }
asset_type=$(detect_asset_type "$file_path")
mime_type=$(detect_mime "$file_path")
mime_supported_for_asset_type "$mime_type" "$asset_type" || { echo "Error: unsupported file type $mime_type for $asset_type" >&2; exit 1; }
body=$(jq -nc --arg pid "$project_id" --arg type "$asset_type" --arg mime "$mime_type" '{project_id: $pid, asset_type: $type, mime_type: $mime, file_name: "upload"}')
result=$(pexo_post "/api/biz/projects/$project_id/assets/upload" "$body")
upload_url=$(echo "$result" | jq -r '.uploadUrl // empty')
asset_id=$(echo "$result" | jq -r '.assetId // empty')
if [[ -z "$upload_url" || -z "$asset_id" ]]; then
    echo "$result" >&2
    exit 1
fi
curl -sS -X PUT -H "Content-Type: $mime_type" -T "$file_path" "$upload_url"
printf '%s\n' "$asset_id"