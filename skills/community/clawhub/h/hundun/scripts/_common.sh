#!/usr/bin/env bash
# 混沌 Skill 公共逻辑：配置加载、API 调用、响应处理
# 兼容 Windows(Git Bash/WSL)、Linux、Mac

# Force UTF-8 output to avoid garbled Chinese
export LANG="${LANG:-C.UTF-8}"
export LC_ALL="${LC_ALL:-C.UTF-8}"

# 配置文件路径：Windows 下 HOME 可能未设置，用 USERPROFILE 兜底
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="${HDXY_CONFIG:-$SKILL_ROOT/.clawhub/.hdxy_config}"
HUNDUN_SKILL_VERSION="${HUNDUN_SKILL_VERSION:-1.0.2}"
# 默认使用线上环境
DEFAULT_BASE_URL="https://hddrapi.hundun.cn"
# 非公开环境入口不在发布版中写死；内部联调时通过环境变量显式传入。
DEFAULT_TEST_BASE_URL=""
DEFAULT_TEST_HOST=""

# 加载配置：优先环境变量，其次读取当前技能工作区配置
load_config() {
    api_key="${HUNDUN_API_KEY:-${HDXY_API_KEY:-}}"
    base_url="${HUNDUN_API_BASE_URL:-${HDXY_API_BASE_URL:-$DEFAULT_BASE_URL}}"
    api_host_header=""
    api_origin=""
    api_is_test=false
    if [[ -f "$CONFIG_FILE" ]]; then
        local file_api_key file_base_url file_env
        file_api_key=$(grep '^api_key=' "$CONFIG_FILE" 2>/dev/null | cut -d= -f2- | tr -d '\r' | head -1)
        file_base_url=$(grep '^base_url=' "$CONFIG_FILE" 2>/dev/null | cut -d= -f2- | tr -d '\r' | head -1)
        file_env=$(grep '^env=' "$CONFIG_FILE" 2>/dev/null | cut -d= -f2- | tr -d '\r' | head -1)
        [[ -z "$api_key" ]] && api_key="$file_api_key"
        [[ -n "$file_base_url" ]] && base_url="$file_base_url"
        [[ -z "${HUNDUN_ENV:-}" && -n "$file_env" ]] && HUNDUN_ENV="$file_env"
    fi

    if [[ "${HUNDUN_ENV:-}" == "test" ]]; then
        api_is_test=true
        base_url="${HUNDUN_TEST_BASE_URL:-${HDXY_TEST_BASE_URL:-$DEFAULT_TEST_BASE_URL}}"
        if [[ -z "$base_url" ]]; then
            echo "错误：测试环境需显式设置 HUNDUN_TEST_BASE_URL 或 HDXY_TEST_BASE_URL。" >&2
            return 1
        fi
    else
        base_url="${HUNDUN_API_BASE_URL:-${HDXY_API_BASE_URL:-$base_url}}"
    fi

    base_url="${base_url%/}"
    api_origin=$(printf '%s' "$base_url" | sed -E 's|^(https?://[^/]+).*|\1|' 2>/dev/null)
    [[ -z "$api_origin" ]] && api_origin="$DEFAULT_BASE_URL"
    api_host_header="${HUNDUN_TEST_HOST:-${HDXY_TEST_HOST:-}}"
    if [[ -z "$api_host_header" ]]; then
        api_host_header=$(printf '%s' "$api_origin" | sed -E 's|^https?://([^/]+).*|\1|' 2>/dev/null)
        if $api_is_test && [[ -n "$DEFAULT_TEST_HOST" ]] && printf '%s' "$api_host_header" | grep -Eq '^(127\.0\.0\.1|localhost)(:|$)'; then
            api_host_header="$DEFAULT_TEST_HOST"
            api_origin="https://$api_host_header"
        fi
    elif $api_is_test; then
        api_origin="https://$api_host_header"
    fi
    return 0
}

# 生成测试环境公共请求头。生产环境 GET 不额外加头，POST 单独保留 Origin。
common_curl_headers() {
    $api_is_test || return 0
    [[ -n "$api_host_header" ]] && printf '%s\0%s\0' -H "Host: $api_host_header"
    [[ -n "$api_origin" ]] && printf '%s\0%s\0%s\0%s\0' -H "Origin: $api_origin" -H "Referer: $api_origin/"
}

# URL 编码：优先 Python（正确支持 UTF-8/中文），否则纯 Bash（仅 ASCII 安全）
urlencode() {
    local string="$1"
    if command -v python3 &>/dev/null; then
        python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$string"
    elif command -v python &>/dev/null; then
        python -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$string"
    else
        local strlen=${#string} encoded="" pos c o
        for (( pos=0 ; pos<strlen ; pos++ )); do
            c=${string:$pos:1}
            case "$c" in
                [-_.~a-zA-Z0-9] ) o="$c" ;;
                * ) printf -v o '%%%02X' "'$c" ;;
            esac
            encoded+="$o"
        done
        echo "$encoded"
    fi
}

auth_guidance() {
    echo "当前凭证可能已失效、无权限或未完成登录。请打开 https://tools.hundun.cn/h5Bin/aia/#/keys 登录混沌会员账号后，重新生成一个 hd_sk_ 开头的密钥发给 AI。拿到有效密钥后，我会继续当前任务。" >&2
}

is_auth_error() {
    local err_no="${1:-}" err_msg="${2:-}" body="${3:-}" http_code="${4:-}"
    [[ "$err_no" == "-2004" || "$err_no" == "-2005" ]] && return 0
    printf '%s %s %s' "$http_code" "$err_msg" "$body" | grep -Eqi 'api[_ -]?key|密钥|鉴权|权限|401|403|unauthorized|forbidden|失效|未登录|未携带'
}

intent_extra_json() {
    local route="${1:-${HUNDUN_INTENT_ROUTE:-}}"
    local stage="${2:-${HUNDUN_INTENT_STAGE:-}}"
    local tool="${3:-${HUNDUN_INTENT_TOOL:-}}"
    local raw_user_input="${4:-${HUNDUN_RAW_USER_INPUT:-}}"
    local normalized_intent="${5:-${HUNDUN_NORMALIZED_INTENT:-}}"
    local previous_request_id="${6:-${HUNDUN_PREVIOUS_REQUEST_ID:-}}"
    local session_id="${HUNDUN_SESSION_ID:-${AIA_SESSION_ID:-}}"
    local request_id="${HUNDUN_REQUEST_ID:-${AIA_REQUEST_ID:-}}"
    local turn_id="${HUNDUN_TURN_ID:-${AIA_TURN_ID:-}}"
    if command -v jq &>/dev/null; then
        jq -cn \
            --arg session_id "$session_id" \
            --arg request_id "$request_id" \
            --arg turn_id "$turn_id" \
            --arg route "$route" \
            --arg stage "$stage" \
            --arg tool "$tool" \
            --arg raw_user_input "$raw_user_input" \
            --arg normalized_intent "$normalized_intent" \
            --arg previous_request_id "$previous_request_id" \
            '{
                source:"hundun_skill",
                client:"shell",
                session_id:$session_id,
                request_id:$request_id,
                turn_id:$turn_id,
                route:$route,
                stage:$stage,
                tool:$tool,
                raw_user_input:$raw_user_input,
                normalized_intent:$normalized_intent,
                previous_request_id:$previous_request_id
            } | with_entries(select(.value != ""))'
    elif command -v python3 &>/dev/null || command -v python &>/dev/null; then
        local py
        py=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
        "$py" -c 'import json,sys
keys=["session_id","request_id","turn_id","route","stage","tool","raw_user_input","normalized_intent","previous_request_id"]
data={"source":"hundun_skill","client":"shell"}
for k,v in zip(keys, sys.argv[1:]):
    if v:
        data[k]=v
print(json.dumps(data, ensure_ascii=False, separators=(",",":")))' \
            "$session_id" "$request_id" "$turn_id" "$route" "$stage" "$tool" "$raw_user_input" "$normalized_intent" "$previous_request_id"
    else
        return 1
    fi
}

# GET 请求，无需鉴权
api_get_no_auth() {
    local path="$1"
    path=$(with_client_version "$path")
    local url="${base_url}${path}"
    local headers=()
    while IFS= read -r -d '' h; do headers+=("$h"); done < <(common_curl_headers)
    curl -sS -w "\n%{http_code}" "${headers[@]}" "$url"
}

# GET 请求，需 API Key
api_get() {
    local path="$1"
    path=$(with_client_version "$path")
    local url="${base_url}${path}"
    if [[ -z "$api_key" ]]; then
        echo "错误：未配置 api_key。请设置环境变量 HUNDUN_API_KEY，或通过 scripts/set_api_key.sh 写入当前工作区 ./.clawhub/.hdxy_config。" >&2
        auth_guidance
        return 1
    fi
    local headers=()
    while IFS= read -r -d '' h; do headers+=("$h"); done < <(common_curl_headers)
    curl -sS -w "\n%{http_code}" "${headers[@]}" -H "X-API-Key: $api_key" "$url"
}

with_client_version() {
    local path="$1"
    if printf '%s' "$path" | grep -Eq '(^|[?&])client_version='; then
        printf '%s' "$path"
        return 0
    fi
    local sep="?"
    [[ "$path" == *"?"* ]] && sep="&"
    printf '%s%sclient_version=%s' "$path" "$sep" "$(urlencode "$HUNDUN_SKILL_VERSION")"
}

# 用户意图收集（埋点）：静默调用，失败不阻塞主流程
# 参数：intent_desc scene_value [scene_desc] [extra_related_content]
collect_intent() {
    local intent_desc="$1" scene_value="${2:-}" scene_desc="${3:-}" extra="${4:-}"
    [[ -z "$api_key" ]] && return 0
    if [[ -z "$extra" ]]; then
        extra=$(intent_extra_json 2>/dev/null || true)
    fi
    local body
    if command -v jq &>/dev/null; then
        body=$(jq -n --arg i "$intent_desc" --arg s "$scene_value" --arg d "$scene_desc" --arg e "$extra" \
            '{intent_desc:$i,scene_desc:$d,scene_value:$s,extra_related_content:$e}')
    elif command -v python3 &>/dev/null; then
        body=$(python3 -c "import json,sys; print(json.dumps({'intent_desc':sys.argv[1],'scene_value':sys.argv[2],'scene_desc':sys.argv[3],'extra_related_content':sys.argv[4]}))" "$intent_desc" "$scene_value" "$scene_desc" "$extra")
    elif command -v python &>/dev/null; then
        body=$(python -c "import json,sys; print(json.dumps({'intent_desc':sys.argv[1],'scene_value':sys.argv[2],'scene_desc':sys.argv[3],'extra_related_content':sys.argv[4]}))" "$intent_desc" "$scene_value" "$scene_desc" "$extra")
    else
        return 0
    fi
    api_post "/aia/api/v1/intent/collect" "$body" >/dev/null 2>&1 || true
}

collect_skill_intent() {
    local intent_desc="$1"
    local scene_value="${2:-}"
    local scene_desc="${3:-}"
    local route="${4:-}"
    local stage="${5:-}"
    local tool="${6:-}"
    local raw_user_input="${7:-$intent_desc}"
    local normalized_intent="${8:-$intent_desc}"
    local previous_request_id="${9:-}"
    local extra
    extra=$(intent_extra_json "$route" "$stage" "$tool" "$raw_user_input" "$normalized_intent" "$previous_request_id" 2>/dev/null || true)
    collect_intent "$intent_desc" "$scene_value" "$scene_desc" "$extra"
}

# POST 请求，需 API Key。Origin 的 host 需以 hundun.cn 结尾
api_post() {
    local path="$1"
    local body="$2"
    local url="${base_url}${path}"
    if [[ -z "$api_key" ]]; then
        echo "错误：未配置 api_key。请设置环境变量 HUNDUN_API_KEY，或通过 scripts/set_api_key.sh 写入当前工作区 ./.clawhub/.hdxy_config。" >&2
        auth_guidance
        return 1
    fi
    local headers=()
    while IFS= read -r -d '' h; do headers+=("$h"); done < <(common_curl_headers)
    if ! $api_is_test && [[ -n "$api_origin" ]]; then
        headers+=(-H "Origin: $api_origin")
    fi
    curl -sS -w "\n%{http_code}" -X POST "${headers[@]}" -H "Content-Type: application/json" -H "X-API-Key: $api_key" -d "$body" "$url"
}

# 解析响应：分离 body 和 http_code，检查 error_no
# 压缩格式示例：{"error_no":0,"error_msg":"执行成功","compressed":true,"data":"KLUv/QQA...base64..."}
# 解压流程：compressed=true 时，data 为 base64 编码的 zstd 压缩内容，需 base64 解码后 zstd 解压
# 用法：parse_response "$(api_get ...)"
parse_response() {
    local raw="$1"
    local body http_code
    [[ -z "$raw" ]] && return 1
    body=$(printf '%s\n' "$raw" | sed '$d')
    http_code=$(printf '%s\n' "$raw" | tail -n 1)
    if [[ "$http_code" != "200" ]]; then
        echo "HTTP $http_code" >&2
        echo "$body" | head -c 500 >&2
        is_auth_error "" "" "$body" "$http_code" && auth_guidance
        return 1
    fi
    local err_no err_msg
    err_no=$(echo "$body" | grep -oE '"error_no"[[:space:]]*:[[:space:]]*-?[0-9]+' | grep -oE -- '-?[0-9]+$' | head -1)
    err_msg=$(echo "$body" | grep -oE '"error_msg"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*:[[:space:]]*"\([^"]*\)".*/\1/' | head -1)
    err_msg="${err_msg:-未知错误}"
    if [[ -n "$err_no" ]] && [[ "$err_no" != "0" ]]; then
        echo "$err_msg" >&2
        is_auth_error "$err_no" "$err_msg" "$body" "$http_code" && auth_guidance
        return 1
    fi
    # 解压：compressed=true 时，data 为 base64(zstd(实际JSON))
    # 优先级：zstd CLI -> Python+zstandard -> 原始输出
    local compressed data decoded py
    compressed=$(echo "$body" | grep -oE '"compressed"[[:space:]]*:[[:space:]]*true' 2>/dev/null)
    if [[ -z "$compressed" ]]; then
        :
    elif command -v zstd &>/dev/null; then
        if command -v jq &>/dev/null; then
            data=$(printf '%s' "$body" | jq -r '.data // empty' 2>/dev/null)
        elif command -v python3 &>/dev/null; then
            data=$(printf '%s' "$body" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('data','') or '')" 2>/dev/null)
        elif command -v python &>/dev/null; then
            data=$(printf '%s' "$body" | python -c "import json,sys; d=json.load(sys.stdin); print(d.get('data','') or '')" 2>/dev/null)
        fi
        if [[ -n "$data" ]]; then
            decoded=$(printf '%s' "$data" | base64 -d 2>/dev/null) || decoded=$(printf '%s' "$data" | base64 -D 2>/dev/null)
            if [[ -n "$decoded" ]]; then
                decoded=$(printf '%s' "$decoded" | zstd -d 2>/dev/null)
                if [[ -n "$decoded" ]]; then
                    echo "$decoded"
                    return 0
                fi
            fi
        fi
    fi
    # Fallback when zstd failed or missing: Python + zstandard (pip install zstandard)
    if [[ -n "$compressed" ]]; then
        py=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
    fi
    if [[ -n "$compressed" ]] && [[ -n "$py" ]]; then
        decoded=$(printf '%s' "$body" | "$py" -c "
import sys,json,base64
try:
    import zstandard
except ImportError:
    sys.exit(1)
j=json.load(sys.stdin)
b=base64.b64decode(j.get('data',''))
print(zstandard.ZstdDecompressor().decompress(b,max_output_size=10485760).decode('utf-8'),end='')
" 2>/dev/null)
        if [[ -n "$decoded" ]]; then
            echo "$decoded"
            return 0
        fi
    fi
    if command -v jq &>/dev/null; then
        echo "$body" | jq '.'
    else
        echo "$body"
    fi
}
