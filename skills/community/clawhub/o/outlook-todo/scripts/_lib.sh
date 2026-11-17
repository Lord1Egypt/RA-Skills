#!/usr/bin/env bash
# outlook-todo internal helpers (not meant to be run directly)
# Source this from the other scripts:  . "$SCRIPT_DIR/_lib.sh"
#
# Provides:
#   * strict mode (errexit, pipefail, nounset) with safe IFS
#   * config/tokens resolution under $OUTLOOK_TODO_DIR (default ~/.outlook-todo)
#   * load_config / save_config / load_tokens / save_tokens
#   * enforce_token_file_perms
#   * jq/curl/python sanity checks
#   * log helpers (info/warn/err) that NEVER echo tokens
#   * build_graph_url, graph_get, graph_request
#   * json_build_event_payload (uses jq -n + --arg for safe escaping)
#   * print_event_summary (for confirmation prompts)
#
# Security: this file must never print tokens, refresh tokens, or device codes
# to logs. Only non-secret metadata (expiry timestamps, scopes) is allowed.

# Avoid double-sourcing
if [[ -n "${OUTLOOK_TODO_LIB_LOADED:-}" ]]; then
    return 0 2>/dev/null || true
fi
OUTLOOK_TODO_LIB_LOADED=1

set -Eeuo pipefail
IFS=$' \t\n'

# ---- Paths -----------------------------------------------------------------

: "${OUTLOOK_TODO_DIR:=$HOME/.outlook-todo}"
OUTLOOK_TODO_CONFIG="$OUTLOOK_TODO_DIR/config.json"
OUTLOOK_TODO_TOKENS="$OUTLOOK_TODO_DIR/tokens.json"
OUTLOOK_TODO_DEVICE="$OUTLOOK_TODO_DIR/device.json"
OUTLOOK_TODO_LAST_HTTP=""  # set by graph_request for debugging

# ---- Bash version guard ----------------------------------------------------
# We need associative arrays (bash 4+). On macOS the default is 3.2.
if ((BASH_VERSINFO[0] < 4)); then
    echo "outlook-todo: bash 4+ is required (associative arrays). Found: $BASH_VERSION" >&2
    exit 1
fi

# ---- Tool checks -----------------------------------------------------------

_lib__require_bin() {
    local bin="$1"
    if ! command -v "$bin" >/dev/null 2>&1; then
        echo "outlook-todo: required binary not found: $bin" >&2
        return 1
    fi
}

_lib__require_bin jq
_lib__require_bin curl
# python3 is preferred for some pretty-printer paths; warn if missing
if ! command -v python3 >/dev/null 2>&1; then
    echo "outlook-todo: warning: python3 not found, table formatting will fall back to jq" >&2
fi

# ---- Logging (no secrets) --------------------------------------------------

_log_ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

log_info()  { printf '[%s] [info]  %s\n' "$(_log_ts)" "$*" >&2; }
log_warn()  { printf '[%s] [warn]  %s\n' "$(_log_ts)" "$*" >&2; }
log_err()   { printf '[%s] [error] %s\n' "$(_log_ts)" "$*" >&2; }

# die prints a non-secret error and exits 1
die() {
    log_err "$*"
    exit 1
}

# ---- Config & tokens -------------------------------------------------------

ensure_dirs() {
    if [[ ! -d "$OUTLOOK_TODO_DIR" ]]; then
        mkdir -p "$OUTLOOK_TODO_DIR" || die "cannot create $OUTLOOK_TODO_DIR"
    fi
    # chmod 700; a failure here means tokens would sit on a permissive location
    if ! chmod 700 "$OUTLOOK_TODO_DIR" 2>/dev/null; then
        die "could not chmod 700 $OUTLOOK_TODO_DIR; refusing to store tokens in a permissive location"
    fi
}

# load_config: reads config.json, exports the standard keys, returns 1 if missing.
# Usage:  load_config || die "run setup-device-code.sh first"
load_config() {
    [[ -f "$OUTLOOK_TODO_CONFIG" ]] || return 1
    # Sanity: must be valid JSON
    if ! jq -e . "$OUTLOOK_TODO_CONFIG" >/dev/null 2>&1; then
        die "config at $OUTLOOK_TODO_CONFIG is not valid JSON; refusing to proceed"
    fi
    # Export known fields
    local tenant_id client_id authority graph_base scopes
    tenant_id=$(jq -r '.tenant_id // empty' "$OUTLOOK_TODO_CONFIG")
    client_id=$(jq -r '.client_id // empty' "$OUTLOOK_TODO_CONFIG")
    authority=$(jq -r '.authority // empty' "$OUTLOOK_TODO_CONFIG")
    graph_base=$(jq -r '.graph_base // empty' "$OUTLOOK_TODO_CONFIG")
    scopes=$(jq -r 'if (.scopes | type) == "array" then .scopes | join(" ") else (.scope // empty) end' "$OUTLOOK_TODO_CONFIG")
    : "${tenant_id:=common}"
    : "${client_id:?config missing client_id}"
    : "${authority:=https://login.microsoftonline.com/$tenant_id}"
    : "${graph_base:=https://graph.microsoft.com/v1.0}"

    # Runtime re-validation: setup-device-code.sh validates these at write time;
    # re-check here so a tampered or hand-edited config cannot silently redirect
    # bearer or refresh tokens to a non-Microsoft endpoint.
    local _auth_re='^https://login\.microsoftonline\.com/[^/]+/?$'
    [[ "$authority" =~ $_auth_re ]] || \
        die "config authority is not a login.microsoftonline.com URL: $authority"
    [[ "$graph_base" == "https://graph.microsoft.com/v1.0" ]] || \
        die "config graph_base is not the Microsoft Graph v1.0 endpoint: $graph_base"

    export OUTLOOK_TODO_TENANT_ID="$tenant_id"
    export OUTLOOK_TODO_CLIENT_ID="$client_id"
    export OUTLOOK_TODO_AUTHORITY="$authority"
    export OUTLOOK_TODO_GRAPH_BASE="$graph_base"
    export OUTLOOK_TODO_SCOPES="${scopes:-offline_access https://graph.microsoft.com/User.Read https://graph.microsoft.com/Tasks.ReadWrite}"
    return 0
}

save_config() {
    # $1 = JSON content (already built with jq -n or similar; we just verify it)
    local content="$1"
    ensure_dirs
    echo "$content" | jq . > "$OUTLOOK_TODO_CONFIG.tmp"
    mv "$OUTLOOK_TODO_CONFIG.tmp" "$OUTLOOK_TODO_CONFIG"
    chmod 600 "$OUTLOOK_TODO_CONFIG" 2>/dev/null || die "could not chmod 600 $OUTLOOK_TODO_CONFIG"
}

# load_tokens: returns 0 with tokens exported as OUTLOOK_TODO_ACCESS_TOKEN,
# OUTLOOK_TODO_REFRESH_TOKEN, OUTLOOK_TODO_TOKEN_EXPIRES (epoch seconds); 1 if missing.
load_tokens() {
    [[ -f "$OUTLOOK_TODO_TOKENS" ]] || return 1
    if ! jq -e . "$OUTLOOK_TODO_TOKENS" >/dev/null 2>&1; then
        die "tokens file $OUTLOOK_TODO_TOKENS is not valid JSON"
    fi
    local access refresh expires
    access=$(jq -r '.access_token // empty' "$OUTLOOK_TODO_TOKENS")
    refresh=$(jq -r '.refresh_token // empty' "$OUTLOOK_TODO_TOKENS")
    expires=$(jq -r '.expires_at // empty' "$OUTLOOK_TODO_TOKENS")
    [[ -n "$access" ]] || return 1
    export OUTLOOK_TODO_ACCESS_TOKEN="$access"
    [[ -n "$refresh" ]] && export OUTLOOK_TODO_REFRESH_TOKEN="$refresh"
    [[ -n "$expires" ]] && export OUTLOOK_TODO_TOKEN_EXPIRES="$expires"
    return 0
}

save_tokens() {
    # $1 = JSON content
    local content="$1"
    ensure_dirs
    echo "$content" | jq . > "$OUTLOOK_TODO_TOKENS.tmp"
    mv "$OUTLOOK_TODO_TOKENS.tmp" "$OUTLOOK_TODO_TOKENS"
    chmod 600 "$OUTLOOK_TODO_TOKENS" 2>/dev/null || die "could not chmod 600 $OUTLOOK_TODO_TOKENS"
}

# ---- Time / timezone helpers -----------------------------------------------

# Convert "YYYY-MM-DD" + optional "Asia/Shanghai" to ISO 8601 with offset
# Usage: date_with_tz 2026-06-18 Asia/Shanghai
date_with_tz() {
    local date="$1" tz="${2:-Asia/Shanghai}"
    # Validate date
    if ! [[ "$date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        die "invalid date: $date (expected YYYY-MM-DD)"
    fi
    # Validate timezone using Python's zoneinfo (most reliable), fallback to `date`
    if command -v python3 >/dev/null 2>&1; then
        python3 - "$date" "$tz" <<'PY' || die "invalid timezone: $tz"
import sys
from zoneinfo import ZoneInfo, available_timezones
from datetime import datetime
d, tz = sys.argv[1], sys.argv[2]
if tz not in available_timezones():
    sys.exit(2)
dt = datetime.fromisoformat(d).replace(tzinfo=ZoneInfo(tz))
print(dt.isoformat(timespec="seconds"))
PY
    else
        # Fallback: trust the input
        printf '%sT00:00:00+08:00' "$date"
    fi
}

# Now in epoch seconds (cross-platform)
now_epoch() {
    date -u +%s
}

# Pretty-print a token status (NEVER prints the token itself)
token_status() {
    if load_tokens 2>/dev/null; then
        local exp="${OUTLOOK_TODO_TOKEN_EXPIRES:-0}"
        local now
        now=$(now_epoch)
        local left=$(( exp - now ))
        if (( left > 0 )); then
            printf 'token: present, expires in %ss (at %s)\n' "$left" "$exp"
        else
            printf 'token: present but EXPIRED %ss ago (at %s)\n' "$((-left))" "$exp"
        fi
    else
        printf 'token: not present (run setup-device-code.sh)\n'
    fi
}

# ---- Graph HTTP helpers ----------------------------------------------------

# graph_request METHOD PATH [JSON_BODY] [EXTRA_HEADER ...]
#   * uses load_tokens + load_config
#   * follows redirect only on GET (safer for non-GET)
#   * captures status into OUTLOOK_TODO_LAST_HTTP
#   * on 401 with refresh_token present, calls _refresh_access_token once and retries
#   * NEVER logs the access token
#   * any extra "Header: value" strings are passed through as additional -H args
graph_request() {
    local method="$1" path="$2" body="${3:-}"
    shift 3 2>/dev/null || shift $#
    local -a extra_headers=("$@")
    load_config  || die "config missing; run scripts/setup-device-code.sh first"
    load_tokens  || die "tokens missing; run scripts/setup-device-code.sh first"

    local url
    if [[ "$path" =~ ^https?:// ]]; then
        url="$path"
        # Host pinning: absolute URLs may only target the Microsoft Graph endpoint.
        # The one legitimate absolute-URL case is a Graph-provided @odata.nextLink
        # for pagination; anything else must not receive the Graph bearer token.
        if [[ "$url" != https://graph.microsoft.com/* ]]; then
            die "refusing to send a Graph token to a non-Graph endpoint: $url"
        fi
    else
        url="${OUTLOOK_TODO_GRAPH_BASE%/}/${path#/}"
    fi

    local outfile http_code tmp
    outfile=$(mktemp)
    tmp=$(mktemp)
    # shellcheck disable=SC2064  # we want $tmp captured now
    trap "rm -f '$outfile' '$tmp'" RETURN

    _do_http() {
        local m="$1" u="$2" b="$3" of="$4" sf="$5"
        shift 5
        local -a extra=("$@")
        local args=(
            --silent --show-error
            --max-time 30
            -X "$m"
            -H "Authorization: Bearer ${OUTLOOK_TODO_ACCESS_TOKEN}"
            -H "Accept: application/json"
            -o "$of"
            -w '%{http_code}'
        )
        if [[ "$m" == "GET" || "$m" == "HEAD" ]]; then
            args+=( --location )
        fi
        if [[ -n "$b" ]]; then
            args+=( -H "Content-Type: application/json" --data-raw "$b" )
        fi
        if (( ${#extra[@]} > 0 )); then
            local h
            for h in "${extra[@]}"; do
                args+=( -H "$h" )
            done
        fi
        curl "${args[@]}" "$u" > "$sf"
    }

    _do_http "$method" "$url" "$body" "$outfile" "$tmp" "${extra_headers[@]}"
    OUTLOOK_TODO_LAST_HTTP=$(cat "$tmp")
    http_code="$OUTLOOK_TODO_LAST_HTTP"

    # 401 + refresh available? try once.
    if [[ "$http_code" == "401" && -n "${OUTLOOK_TODO_REFRESH_TOKEN:-}" ]]; then
        log_warn "got 401, attempting silent refresh..."
        if _refresh_access_token; then
            _do_http "$method" "$url" "$body" "$outfile" "$tmp" "${extra_headers[@]}"
            OUTLOOK_TODO_LAST_HTTP=$(cat "$tmp")
            http_code="$OUTLOOK_TODO_LAST_HTTP"
        fi
    fi

    if [[ ! "$http_code" =~ ^2 ]]; then
        # Surface a *truncated*, *sanitized* body
        local snippet
        snippet=$(head -c 512 "$outfile" 2>/dev/null || true)
        # Strip any field that looks like a token to avoid accidental leak
        snippet=$(printf '%s' "$snippet" | jq -c '
            if type == "object" then
                with_entries(if .key | test("token|refresh|access|secret|password"; "i") then .value = "[REDACTED]" else . end)
            else . end' 2>/dev/null || printf '%s' "$snippet")
        die "Graph $method $path failed: HTTP $http_code  body=$snippet"
    fi

    cat "$outfile"
}

# _refresh_access_token: writes new access_token (and possibly new refresh_token) to tokens.json
# Requires: load_config + load_tokens already called, and OUTLOOK_TODO_REFRESH_TOKEN set.
_refresh_access_token() {
    [[ -n "${OUTLOOK_TODO_REFRESH_TOKEN:-}" ]] || return 1

    local tenant_path="/oauth2/v2.0/token"
    local url="${OUTLOOK_TODO_AUTHORITY%/}${tenant_path}"

    local resp
    resp=$(curl --silent --show-error --max-time 30 \
        -X POST \
        -H "Accept: application/json" \
        --data-urlencode "client_id=$OUTLOOK_TODO_CLIENT_ID" \
        --data-urlencode "scope=$OUTLOOK_TODO_SCOPES" \
        --data-urlencode "refresh_token=$OUTLOOK_TODO_REFRESH_TOKEN" \
        --data-urlencode "grant_type=refresh_token" \
        "$url") || { log_warn "refresh request transport error"; return 1; }

    local new_access new_refresh new_expires_in
    new_access=$(printf '%s' "$resp" | jq -r '.access_token // empty')
    [[ -n "$new_access" ]] || { log_warn "refresh did not return access_token"; return 1; }
    new_refresh=$(printf '%s' "$resp" | jq -r '.refresh_token // empty')
    new_expires_in=$(printf '%s' "$resp" | jq -r '.expires_in // 3600')

    local now expires_at
    now=$(now_epoch)
    expires_at=$(( now + new_expires_in ))

    # Merge with existing tokens.json (preserves any other fields like scope list).
    # Build the new fields as a single object, then merge.
    local new_fields
    new_fields=$(jq -n \
        --arg a  "$new_access" \
        --arg r  "$new_refresh" \
        --argjson e  "$expires_at" \
        --argjson ei "$new_expires_in" \
        --argjson n  "$now" \
        '{
            access_token: $a,
            refresh_token: (if $r == "" then null else $r end),
            expires_at:   $e,
            expires_in:   $ei,
            refreshed_at: $n
        } | with_entries(select(.value != null))')

    local merged
    if [[ -f "$OUTLOOK_TODO_TOKENS" ]]; then
        merged=$(jq -s '
            .[0] * .[1]
          | with_entries(select(.value != null and .value != ""))
        ' "$OUTLOOK_TODO_TOKENS" <(printf '%s' "$new_fields"))
    else
        merged="$new_fields"
    fi
    save_tokens "$merged"
    export OUTLOOK_TODO_ACCESS_TOKEN="$new_access"
    [[ -n "$new_refresh" ]] && export OUTLOOK_TODO_REFRESH_TOKEN="$new_refresh"
    export OUTLOOK_TODO_TOKEN_EXPIRES="$expires_at"
    log_info "token refreshed; expires in ${new_expires_in}s"
    return 0
}

# Public: refresh_tokens (no-op if still valid)
ensure_fresh_token() {
    load_config || die "config missing; run setup-device-code.sh first"
    load_tokens || die "tokens missing; run setup-device-code.sh"
    local exp="${OUTLOOK_TODO_TOKEN_EXPIRES:-0}"
    local now skew=120
    now=$(now_epoch)
    if (( exp - now < skew )); then
        if [[ -n "${OUTLOOK_TODO_REFRESH_TOKEN:-}" ]]; then
            _refresh_access_token || die "token refresh failed; please re-run setup-device-code.sh"
        else
            die "access token expired and no refresh_token available; please re-run setup-device-code.sh"
        fi
    fi
}

# ---- JSON builders (safe escaping via jq -n) ------------------------------

# build_event_body SUBJECT START_ISO END_ISO [TIMEZONE] [BODY] [LOCATION]
# Returns a JSON string on stdout. Timezone defaults to Asia/Shanghai.
# Use --arg for ALL user-supplied fields: no shell interpolation.
build_event_body() {
    local subject="$1" start="$2" end="$3" tz="${4:-Asia/Shanghai}" body="${5:-}" location="${6:-}"

    # Validate inputs
    [[ -n "$subject" ]] || die "subject must not be empty"
    [[ -n "$start" && -n "$end" ]] || die "start and end are required"

    jq -n \
        --arg subject  "$subject" \
        --arg body     "$body" \
        --arg loc      "$location" \
        --arg start    "$start" \
        --arg end      "$end" \
        --arg tz       "$tz" \
        '{
            subject: $subject,
            body: { contentType: "Text", content: $body },
            start: { dateTime: $start, timeZone: $tz },
            end:   { dateTime: $end,   timeZone: $tz },
            location: (if $loc == "" then null else { displayName: $loc } end)
          } | with_entries(select(.value != null and .value != ""))
        '
}

# Print a compact, human-friendly summary of an event for confirmation prompts
print_event_summary() {
    local json="$1"
    printf '%s' "$json" | jq -r '
        def field(k): .[k] // "-";
        def dt(k):  .[k].dateTime // "-";
        def tz(k):  .[k].timeZone // "-";
        "subject:  \(field("subject"))",
        "start:    \(dt("start"))  (\(tz("start")))",
        "end:      \(dt("end"))  (\(tz("end")))",
        "location: \(.location.displayName // "-")",
        "id:       \(field("id"))"
    ' >&2
}

# ---- Misc -----------------------------------------------------------------

# Format an ISO datetime for display in a table row
fmt_dt() {
    local s="${1:-}"
    [[ -z "$s" ]] && { printf -- "-"; return; }
    printf '%s' "$s" | sed -E 's/T/ /; s/\.[0-9]+//; s/[+-][0-9]{2}:[0-9]{2}$//'
}

# Confirm-prompt that does not echo back the response
# Usage: confirm "Type YES to continue" || exit 1
confirm() {
    local prompt="${1:-Are you sure?}"
    local reply
    printf '%s [type YES to confirm]: ' "$prompt" >&2
    if ! read -r reply </dev/tty 2>/dev/null; then
        # Fall back to stdin if /dev/tty unavailable (e.g. in tests)
        read -r reply
    fi
    if [[ "$reply" != "YES" ]]; then
        echo "Confirmation not received; aborting." >&2
        return 1
    fi
    return 0
}

# require_apply_and_confirm — unified dry-run + confirmation gate
#
# Usage:  require_apply_and_confirm "$apply" "$skip_yes" "description"
#
#   $1 (apply)      — 0 = dry-run, 1 = real write
#   $2 (skip_yes)    — 0 = require "YES" confirmation, 1 = skip
#   $3 (description) — human-readable summary for the prompt
#
# Returns 1 (no error) for dry-run, dies on failed confirmation, returns 0 on success.
# Callers in dry-run mode must echo their payload and exit 0 after receiving return 1.
#
# Non-interactive writes require an explicit --yes flag passed by the caller.
# There is deliberately no environment-variable bypass: an agent must pass --yes
# visibly, and a human at a terminal gets the typed-YES prompt.
require_apply_and_confirm() {
    local _apply="${1:-0}" _yes="${2:-0}" _desc="${3:-this operation}"
    if (( ! _apply )); then
        log_info "DRY-RUN: --apply not set; payload would be:"
        return 1
    fi
    if (( ! _yes )); then
        printf '\n>>> About to: %s\n' "$_desc" >&2
        printf '>>> Type YES within 10s to proceed: ' >&2
        local _reply
        if ! read -r -t 10 _reply </dev/tty 2>/dev/null; then
            read -r -t 10 _reply
        fi
        if [[ "$_reply" != "YES" ]]; then
            die "aborted (no YES confirmation)"
        fi
    fi
    return 0
}
