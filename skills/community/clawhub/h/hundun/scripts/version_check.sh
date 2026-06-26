#!/usr/bin/env bash
# AIA version preflight. The version endpoint itself does not require a key.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

print_login_guidance() {
    auth_guidance
}

print_upgrade_notice() {
    local body="$1"
    if ! printf '%s' "$body" | grep -q '"_notice"'; then
        return 0
    fi
    local message current latest upgrade_url severity
    if command -v jq &>/dev/null; then
        message=$(printf '%s' "$body" | jq -r '._notice.update.message // empty' 2>/dev/null)
        current=$(printf '%s' "$body" | jq -r '._notice.update.current // empty' 2>/dev/null)
        latest=$(printf '%s' "$body" | jq -r '._notice.update.latest // empty' 2>/dev/null)
        upgrade_url=$(printf '%s' "$body" | jq -r '._notice.update.upgrade_url // empty' 2>/dev/null)
        severity=$(printf '%s' "$body" | jq -r '._notice.update.severity // empty' 2>/dev/null)
    elif command -v python3 &>/dev/null || command -v python &>/dev/null; then
        local py parsed
        py=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
        parsed=$(printf '%s' "$body" | "$py" -c 'import json,sys
try:
    u=json.load(sys.stdin).get("_notice",{}).get("update",{})
except Exception:
    u={}
print("\n".join([u.get("message",""),u.get("current",""),u.get("latest",""),u.get("upgrade_url",""),u.get("severity","")]))' 2>/dev/null)
        message=$(printf '%s\n' "$parsed" | sed -n '1p')
        current=$(printf '%s\n' "$parsed" | sed -n '2p')
        latest=$(printf '%s\n' "$parsed" | sed -n '3p')
        upgrade_url=$(printf '%s\n' "$parsed" | sed -n '4p')
        severity=$(printf '%s\n' "$parsed" | sed -n '5p')
    fi
    [[ -z "$message" || -z "$latest" ]] && return 0
    printf '版本提示：%s' "$message" >&2
    [[ -n "$current" ]] && printf '（当前 %s，最新 %s）' "$current" "$latest" >&2
    [[ -n "$upgrade_url" ]] && printf '。更新地址：%s' "$upgrade_url" >&2
    [[ -n "$severity" ]] && printf '。级别：%s' "$severity" >&2
    printf '\n' >&2
}

load_config || exit 1

raw=$(api_get_no_auth "/aia/api/v1/version?client_version=$(urlencode "$HUNDUN_SKILL_VERSION")")
output=$(parse_response "$raw" 2>&1)
status=$?

if [[ $status -eq 0 ]]; then
    printf '%s\n' "$output"
    print_upgrade_notice "$output"
    exit 0
fi

if printf '%s' "$output" | grep -Eqi 'api[_ -]?key|密钥|鉴权|权限|401|403|unauthorized|forbidden|失效|未登录'; then
    print_login_guidance
    exit 1
fi

printf '%s\n' "$output" >&2
exit 1
