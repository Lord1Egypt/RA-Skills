#!/usr/bin/env bash
# Skill 补全 - GET /aia/api/v1/skill/patch?skill_id=&module_key=[&version=]
# 文档：version 选填，不传则返回当前生效版本（patch_status='current'）内容
# --write：版本感知写入 _patch/{module}.md，仅当响应版本与本地不同时覆盖
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

do_write=false
non_flags=()
for arg in "$@"; do
    case "$arg" in
        -w|--write) do_write=true ;;
        *) non_flags+=("$arg") ;;
    esac
done
module_key="${non_flags[0]:-core}"
version="${non_flags[1]:-}"
skill_id="${non_flags[2]:-hd_skill}"
load_config || exit 1

path="/aia/api/v1/skill/patch?skill_id=$(urlencode "$skill_id")&module_key=$(urlencode "$module_key")"
[[ -n "$version" ]] && path="${path}&version=$(urlencode "$version")"
raw=$(api_get "$path")

if $do_write; then
    body=$(parse_response "$raw") || exit 1
    if command -v jq &>/dev/null; then
        ver=$(printf '%s' "$body" | jq -r '.data.version // .version // empty')
        content=$(printf '%s' "$body" | jq -r '.data.content // .content // empty')
    elif command -v python3 &>/dev/null; then
        ver=$(printf '%s' "$body" | python3 -c "import json,sys; d=json.load(sys.stdin); inner=d.get('data',d); print(inner.get('version',''))" 2>/dev/null)
        content=$(printf '%s' "$body" | python3 -c "import json,sys; d=json.load(sys.stdin); inner=d.get('data',d); print(inner.get('content',''))" 2>/dev/null)
    elif command -v python &>/dev/null; then
        ver=$(printf '%s' "$body" | python -c "import json,sys; d=json.load(sys.stdin); inner=d.get('data',d); print(inner.get('version',''))" 2>/dev/null)
        content=$(printf '%s' "$body" | python -c "import json,sys; d=json.load(sys.stdin); inner=d.get('data',d); print(inner.get('content',''))" 2>/dev/null)
    else
        echo "jq or python required for --write" >&2
        exit 1
    fi
    skill_dir="$(cd "$SCRIPT_DIR/.." && pwd)"
    patch_dir="$skill_dir/_patch"
    meta_file="$patch_dir/.meta.json"
    mkdir -p "$patch_dir"
    local_ver=""
    if [[ -f "$meta_file" ]] && command -v jq &>/dev/null; then
        local_ver=$(jq -r --arg k "$module_key" '.[$k] // empty' "$meta_file" 2>/dev/null)
    elif [[ -f "$meta_file" ]] && command -v python3 &>/dev/null; then
        local_ver=$(python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(d.get(sys.argv[2],''))" "$meta_file" "$module_key" 2>/dev/null)
    fi
    if [[ "$local_ver" == "$ver" ]]; then
        echo "Already up to date: $module_key/$ver"
        exit 0
    fi
    content="${content//\\n/$'\n'}"
    printf '%s' "$content" > "$patch_dir/$module_key.md"
    if command -v jq &>/dev/null; then
        if [[ -f "$meta_file" ]]; then
            jq --arg k "$module_key" --arg v "$ver" '.[$k]=$v' "$meta_file" > "${meta_file}.tmp" && mv "${meta_file}.tmp" "$meta_file"
        else
            jq -n --arg k "$module_key" --arg v "$ver" '.[$k]=$v' > "$meta_file"
        fi
    elif command -v python3 &>/dev/null; then
        python3 -c "
import json,os,sys
meta_file='$meta_file'
module_key='$module_key'
ver='$ver'
m={}
if os.path.exists(meta_file):
    with open(meta_file) as f: m=json.load(f)
m[module_key]=ver
with open(meta_file,'w') as f: json.dump(m,f,ensure_ascii=False)
" 2>/dev/null
    fi
    echo "Updated $module_key to version $ver"
else
    parse_response "$raw"
fi
