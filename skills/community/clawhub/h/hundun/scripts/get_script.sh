#!/usr/bin/env bash
# 获取课程文稿 - GET /aia/api/v1/courses/{course_id}/script（计入一周 50 门课）
# 返回 script_url（AES 加密），解密后下载文稿内容
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

course_id="$1"
if [[ -z "$course_id" ]]; then
    echo "用法: $0 <课程ID>" >&2
    exit 1
fi

load_config || exit 1
collect_skill_intent "读取课程文稿：course_id=$course_id" "skill_get_script" "课程文稿读取" "course" "course_script_read" "get_script" "$course_id" "读取课程文稿"
raw=$(api_get "/aia/api/v1/courses/$course_id/script")
body=$(parse_response "$raw") || exit 1

# Extract script_url from JSON
if command -v jq &>/dev/null; then
    script_url_enc=$(printf '%s' "$body" | jq -r '.data.script_url // .script_url // empty' 2>/dev/null)
elif command -v python3 &>/dev/null; then
    script_url_enc=$(printf '%s' "$body" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('data',{}).get('script_url','') or d.get('script_url',''))" 2>/dev/null)
elif command -v python &>/dev/null; then
    script_url_enc=$(printf '%s' "$body" | python -c "import json,sys; d=json.load(sys.stdin); print(d.get('data',{}).get('script_url','') or d.get('script_url',''))" 2>/dev/null)
else
    echo "Error: need jq or python to parse JSON" >&2
    exit 1
fi

if [[ -z "$script_url_enc" ]]; then
    echo "Error: no script_url in response" >&2
    exit 1
fi

# Decrypt script_url
decrypt_script="$SCRIPT_DIR/_decrypt_script_url.py"
if [[ ! -f "$decrypt_script" ]]; then
    echo "Error: _decrypt_script_url.py not found" >&2
    exit 1
fi

py=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
if [[ -z "$py" ]]; then
    echo "Error: python not found" >&2
    exit 1
fi

decrypted_url=$(printf '%s' "$script_url_enc" | "$py" "$decrypt_script" 2>/dev/null)
if [[ -z "$decrypted_url" ]]; then
    echo "Error: failed to decrypt script_url (pip install pycryptodome)" >&2
    exit 1
fi

# Download and output script content (-L follow redirects, -A User-Agent for OSS)
curl -sS -L -A "hd_skill/1.0" -- "$decrypted_url" || { echo "Error: failed to download script" >&2; exit 1; }
