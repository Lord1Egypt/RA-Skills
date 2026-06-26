#!/usr/bin/env bash
# IT桔子创投电报 API（v2）- 零依赖版本
# 仅使用 curl + bash 内置命令

set -euo pipefail

API_URL="https://www.itjuzi.com/api/telegraph/get_list"
TOKEN_DIR="$HOME/.config/itjuzi-bulletin"
TOKEN_FILE="$TOKEN_DIR/token"
TIMEOUT=15

load_token() {
    if [ -n "${ITJUZI_SKILL_TOKEN:-}" ]; then
        echo "$ITJUZI_SKILL_TOKEN"
        return
    fi
    if [ -f "$TOKEN_FILE" ]; then
        cat "$TOKEN_FILE" 2>/dev/null
        return
    fi
}

cmd_set_token() {
    local token="$1"
    mkdir -p "$TOKEN_DIR"
    chmod 700 "$TOKEN_DIR"
    printf '%s' "$token" > "$TOKEN_FILE"
    chmod 600 "$TOKEN_FILE"
    printf '{"success":true,"message":"Token saved to %s"}\n' "$TOKEN_FILE"
}

cmd_remove_token() {
    if [ -f "$TOKEN_FILE" ]; then
        rm -f "$TOKEN_FILE"
        echo '{"success":true,"message":"Token removed."}'
    else
        echo '{"success":true,"message":"No token found."}'
    fi
}

cmd_show_token() {
    local token
    token=$(load_token)
    if [ -n "$token" ]; then
        local src="file"
        [ -n "${ITJUZI_SKILL_TOKEN:-}" ] && src="env"
        printf '{"success":true,"has_token":true,"token_prefix":"%s...","token_source":"%s","token_file":"%s"}\n' \
            "${token:0:20}" "$src" "$TOKEN_FILE"
    else
        printf '{"success":true,"has_token":false,"token_file":"%s"}\n' "$TOKEN_FILE"
    fi
}

cmd_query() {
    local date_scope="${1:-today}"
    local keyword="${2:-}"
    local event_type="${3:-}"
    local limit="${4:-}"
    local page="${5:-1}"

    local data="date_scope=${date_scope}&page=${page}"
    [ -n "$keyword" ] && data="${data}&keyword=${keyword}"
    [ -n "$event_type" ] && data="${data}&event_type=${event_type}"
    [ -n "$limit" ] && data="${data}&limit=${limit}"

    local -a curl_args=(
        -s -S
        --max-time "$TIMEOUT"
        -X POST
        -H "Content-Type: application/x-www-form-urlencoded"
        -H "Accept: application/json"
        -H "User-Agent: itjuzi-bulletin-skill/2.0"
        -d "$data"
    )

    local token
    token=$(load_token)
    if [ -n "$token" ]; then
        curl_args+=(-H "Authorization: Bearer ${token}")
    fi

    local response
    if ! response=$(curl "${curl_args[@]}" "$API_URL" 2>&1); then
        echo '{"status":"error","code":0,"message":"Network error"}'
        return 1
    fi

    echo "$response"
}

main() {
    local date_scope="today"
    local keyword=""
    local event_type=""
    local limit=""
    local page="1"

    while [ $# -gt 0 ]; do
        case "$1" in
            --set-token)   cmd_set_token "$2"; return 0 ;;
            --remove-token) cmd_remove_token; return 0 ;;
            --show-token)  cmd_show_token; return 0 ;;
            --date-scope)  date_scope="$2"; shift ;;
            --keyword)     keyword="$2"; shift ;;
            --event-type)  event_type="$2"; shift ;;
            --limit)       limit="$2"; shift ;;
            --page)        page="$2"; shift ;;
            --help|-h)     echo "Usage: telegraph_api.sh [--date-scope today|yesterday] [--keyword X] [--event-type X] [--limit N] [--page N]"; return 0 ;;
            *)             echo "{\"status\":\"error\",\"message\":\"Unknown arg: $1\"}"; return 1 ;;
        esac
        shift
    done

    cmd_query "$date_scope" "$keyword" "$event_type" "$limit" "$page"
}

main "$@"
