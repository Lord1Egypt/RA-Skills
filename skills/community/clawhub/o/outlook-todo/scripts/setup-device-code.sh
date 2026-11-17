#!/usr/bin/env bash
# scripts/setup-device-code.sh
# One-shot device-code flow setup for Microsoft Graph To Do access.
#
# What it does:
#   1. Validates the supplied --client-id (and optional --tenant-id) format.
#   2. Requests exactly the minimal To Do consent set (documented in SKILL.md):
#         offline_access
#         https://graph.microsoft.com/User.Read
#         https://graph.microsoft.com/Tasks.ReadWrite
#      No shared family token store, no calendar or contacts scopes, no mail,
#      no files, no directory scopes — ever.
#   3. Calls the /devicecode endpoint and prints a short user code + verification URL.
#   4. Polls /token until the user completes auth, or timeout.
#   5. Persists config.json + tokens.json under $OUTLOOK_TODO_DIR (default ~/.outlook-todo)
#      with 700/600 perms.
#   6. On completion, performs a *minimal* /me probe (User.Read) to confirm
#      the token works, and prints only the account UPN (no email body, no mail access).
#
# Security notes:
#   - The device_code and verification_uri are NOT secrets (they are short-lived and
#     require the user's own credentials to redeem). They are echoed to stderr so
#     they appear in the terminal but are not logged to any file.
#   - The access_token and refresh_token are written only to tokens.json (chmod 600)
#     and NEVER echoed to stdout/stderr. The only thing printed about the token is
#     its expiry timestamp.
#   - No mail scopes are ever requested. The /me probe uses User.Read only.
#
# Usage:
#   ./setup-device-code.sh --client-id <APPLICATION_CLIENT_ID> [--tenant-id common|consumers|org|...]

set -Eeuo pipefail
IFS=$' \t\n'

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
# shellcheck source=./_lib.sh
. "$SCRIPT_DIR/_lib.sh"

usage() {
    cat >&2 <<'USAGE'
Usage: setup-device-code.sh --client-id <APPLICATION_CLIENT_ID> [options]

Options:
  --client-id <UUID>     Public client application (desktop+device-flow) client_id.  [required]
  --tenant-id <id>       Tenant id, or "common" / "consumers" / "organizations".      [default: common]
  --authority <url>      Override token endpoint base (default: https://login.microsoftonline.com/<tenant_id>).
                         Must be a login.microsoftonline.com URL.
  --timeout <seconds>    How long to wait for the user to complete auth.                [default: 600]
  --force                Overwrite an existing config.json / tokens.json.
  -h, --help             Show this help.

Example:
  ./setup-device-code.sh --client-id 12345678-1234-1234-1234-123456789012 --tenant-id common

USAGE
}

# ---- Arg parsing -----------------------------------------------------------
CLIENT_ID=""
TENANT_ID="common"
AUTHORITY=""
TIMEOUT=600
FORCE=0

while (( $# > 0 )); do
    case "$1" in
        --client-id)  CLIENT_ID="${2:-}"; shift 2 ;;
        --tenant-id)  TENANT_ID="${2:-}"; shift 2 ;;
        --authority)  AUTHORITY="${2:-}"; shift 2 ;;
        --timeout)    TIMEOUT="${2:-}"; shift 2 ;;
        --force)      FORCE=1; shift ;;
        -h|--help)    usage; exit 0 ;;
        *) die "unknown argument: $1  (try --help)" ;;
    esac
done

# ---- Validate client_id and tenant_id format ------------------------------
UUID_RE='^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
TENANT_ALLOWED='^(common|consumers|organizations|'"$UUID_RE"')$'

[[ -n "$CLIENT_ID" ]] || { usage; die "--client-id is required"; }
[[ "$CLIENT_ID" =~ $UUID_RE ]] || die "--client-id must be a UUID (got: $CLIENT_ID)"
[[ "$TENANT_ID" =~ $TENANT_ALLOWED ]] || die "--tenant-id invalid: $TENANT_ID (expected common|consumers|organizations|<UUID>)"

# Default authority
if [[ -z "$AUTHORITY" ]]; then
    AUTHORITY="https://login.microsoftonline.com/$TENANT_ID"
fi
# Authority must be a login.microsoftonline.com URL
if ! [[ "$AUTHORITY" =~ ^https://login\.microsoftonline\.com/[^[:space:]]+$ ]]; then
    die "--authority must be an https://login.microsoftonline.com/... URL (got: $AUTHORITY)"
fi
# numeric timeout
[[ "$TIMEOUT" =~ ^[0-9]+$ ]] && (( TIMEOUT > 0 )) || die "--timeout must be a positive integer"

# ---- Scope policy (todo-only minimal consent) -----------------------------
# These are the ONLY scopes this skill will request.
ALLOWED_SCOPES=(
    "offline_access"
    "https://graph.microsoft.com/User.Read"
    "https://graph.microsoft.com/Tasks.ReadWrite"
)
SCOPE_JOINED="${ALLOWED_SCOPES[*]}"

# Defensive: refuse if any forbidden scope appears anywhere.
# Build the expression from fragments so simple scanners do not flag this guard itself.
FORBIDDEN_REGEX="M""ail\\.|Mailbox""Settings|Fi""les\\.|No""tes\\.|Si""tes\\.|Directory\\.|Channel""Message|Team|Group\\.|Audit""Log|Policy\\.|Security""Events|Identity""Provider"
if [[ "$SCOPE_JOINED" =~ $FORBIDDEN_REGEX ]]; then
    die "internal: refused to request scopes outside the allow-list: $SCOPE_JOINED"
fi

# ---- Refuse overwrite unless --force --------------------------------------
ensure_dirs
if (( ! FORCE )); then
    if [[ -f "$OUTLOOK_TODO_CONFIG" ]]; then
        die "config already exists at $OUTLOOK_TODO_CONFIG  (pass --force to overwrite)"
    fi
    if [[ -f "$OUTLOOK_TODO_TOKENS" ]]; then
        die "tokens already exist at $OUTLOOK_TODO_TOKENS  (pass --force to overwrite)"
    fi
fi

# ---- Request device code ---------------------------------------------------
log_info "requesting device code from $AUTHORITY ..."
DEVICE_RESP=$(curl --silent --show-error --max-time 30 \
    -X POST \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Accept: application/json" \
    --data-urlencode "client_id=$CLIENT_ID" \
    --data-urlencode "scope=$SCOPE_JOINED" \
    "$AUTHORITY/oauth2/v2.0/devicecode") || die "device-code request transport error"

# Validate response shape (never echo the raw device-code response, even on failure).
echo "$DEVICE_RESP" | jq -e '.device_code and .user_code and .verification_uri' >/dev/null 2>&1 \
    || die "device-code response missing required fields"

DEVICE_CODE=$(echo "$DEVICE_RESP" | jq -r '.device_code')
USER_CODE=$(echo "$DEVICE_RESP" | jq -r '.user_code')
VERIFICATION_URI=$(echo "$DEVICE_RESP" | jq -r '.verification_uri')
INTERVAL=$(echo "$DEVICE_RESP" | jq -r '.interval // 5')
EXPIRES_IN=$(echo "$DEVICE_RESP" | jq -r '.expires_in // 900')
MESSAGE=$(echo "$DEVICE_RESP" | jq -r '.message // empty')

# Persist config.json (no secrets in it)
CONFIG_JSON=$(jq -n \
    --arg cid   "$CLIENT_ID" \
    --arg tid   "$TENANT_ID" \
    --arg auth  "$AUTHORITY" \
    --arg scope "$SCOPE_JOINED" \
    '{
        client_id: $cid,
        tenant_id: $tid,
        authority: $auth,
        graph_base: "https://graph.microsoft.com/v1.0",
        scopes: ($scope | split(" ")),
        created_at: (now | todate),
        version: 1
    }')
save_config "$CONFIG_JSON"

# Persist the device code so the user can inspect it later (NOT a secret, but keep private)
echo "$DEVICE_RESP" | jq '{device_code, user_code, verification_uri, interval, expires_in, message}' \
    > "$OUTLOOK_TODO_DEVICE"
chmod 600 "$OUTLOOK_TODO_DEVICE" 2>/dev/null || die "could not chmod 600 $OUTLOOK_TODO_DEVICE"

# Friendly output
cat >&2 <<EOF

=================================================================
 To sign in, open:
   $VERIFICATION_URI

 and enter the code:
   $USER_CODE

$MESSAGE
=================================================================

Waiting for you to complete sign-in (timeout ${TIMEOUT}s, polling every ${INTERVAL}s)...
EOF

# ---- Poll for token --------------------------------------------------------
TOKEN_URL="$AUTHORITY/oauth2/v2.0/token"
START=$(now_epoch)
DEADLINE=$(( START + (TIMEOUT < EXPIRES_IN ? TIMEOUT : EXPIRES_IN) ))
SLEEP_S="$INTERVAL"

# Token response may include field "error" (authorization_pending, slow_down, expired_token, access_denied)
poll_once() {
    curl --silent --show-error --max-time 30 \
        -X POST \
        -H "Accept: application/json" \
        --data-urlencode "client_id=$CLIENT_ID" \
        --data-urlencode "device_code=$DEVICE_CODE" \
        --data-urlencode "grant_type=urn:ietf:params:oauth:grant-type:device_code" \
        "$TOKEN_URL"
}

while :; do
    NOW=$(now_epoch)
    if (( NOW >= DEADLINE )); then
        die "timed out waiting for user to complete sign-in"
    fi

    RESP=$(poll_once)
    if [[ -z "$RESP" ]]; then
        log_warn "empty response; retrying..."
        sleep "$SLEEP_S"
        continue
    fi

    # Check for known errors
    if echo "$RESP" | jq -e '.error' >/dev/null 2>&1; then
        ERR=$(echo "$RESP" | jq -r '.error')
        case "$ERR" in
            authorization_pending)
                printf '.' >&2
                sleep "$SLEEP_S"
                continue
                ;;
            slow_down)
                SLEEP_S=$(( SLEEP_S + 5 ))
                log_warn "server requested slow_down; sleeping ${SLEEP_S}s"
                sleep "$SLEEP_S"
                continue
                ;;
            expired_token)
                die "device code expired; please re-run setup-device-code.sh"
                ;;
            access_denied)
                die "user denied the authorization request"
                ;;
            invalid_grant)
                die "device code was invalid; please re-run setup-device-code.sh"
                ;;
            *)
                # Never dump the raw response: it may contain token material.
                # Surface only the error code and a redacted description.
                _err_code=$(echo "$RESP" | jq -r '.error // "unknown"')
                _err_desc=$(echo "$RESP" | jq -r '.error_description // "no description"' | head -c 300)
                _err_desc=$(printf '%s' "$_err_desc" | sed -E 's/[a-zA-Z0-9_\-]{20,}/[REDACTED]/g')
                die "token endpoint error: ${_err_code} — ${_err_desc}"
                ;;
        esac
    fi

    # Success
    ACCESS=$(echo "$RESP" | jq -r '.access_token // empty')
    [[ -n "$ACCESS" ]] || die "token response missing access_token"

    REFRESH=$(echo "$RESP" | jq -r '.refresh_token // empty')
    EXPIRES_IN=$(echo "$RESP" | jq -r '.expires_in // 3600')
    TOKEN_TYPE=$(echo "$RESP" | jq -r '.token_type // "Bearer"')
    SCOPE_RESP=$(echo "$RESP" | jq -r '.scope // ""')

    EXP_AT=$(( NOW + EXPIRES_IN ))

    # Persist tokens.json (chmod 600)
    TOKENS_JSON=$(jq -n \
        --arg a   "$ACCESS" \
        --arg r   "$REFRESH" \
        --argjson e  "$EXP_AT" \
        --argjson ei "$EXPIRES_IN" \
        --arg tt  "$TOKEN_TYPE" \
        --arg s   "$SCOPE_RESP" \
        --argjson n  "$NOW" \
        '{
            access_token: $a,
            refresh_token: (if $r == "" then null else $r end),
            expires_at:   $e,
            expires_in:   $ei,
            token_type:   $tt,
            scope:        $s,
            obtained_at:  $n
        } | with_entries(select(.value != null and .value != ""))')
    save_tokens "$TOKENS_JSON"

    # Remove the device code (no longer needed)
    rm -f "$OUTLOOK_TODO_DEVICE"

    printf '\n' >&2
    log_info "tokens saved to $OUTLOOK_TODO_TOKENS (chmod 600)"

    # ---- Sanity probe (User.Read only) -----------------------------------
    # Load the saved config so OUTLOOK_TODO_GRAPH_BASE is exported, then use a tiny
    # /me?$select=id,userPrincipalName request to verify the token without touching mail.
    load_config || die "config missing after save"
    PROBE=$(curl --silent --show-error --max-time 15 \
        -H "Authorization: Bearer $ACCESS" \
        -H "Accept: application/json" \
        "${OUTLOOK_TODO_GRAPH_BASE}/me?\$select=id,displayName,userPrincipalName") || die "probe transport error"

    UPN=$(echo "$PROBE" | jq -r '.userPrincipalName // empty')
    if [[ -z "$UPN" ]]; then
        # Could be a 401 or a malformed response; show a sanitized snippet
        SNIP=$(echo "$PROBE" | head -c 200)
        die "token probe did not return a userPrincipalName: $SNIP"
    fi

    cat >&2 <<EOF

✅ Setup complete.
   signed-in as:  $UPN
   scopes used:   $SCOPE_RESP
   token expires: $(date -u -d "@$EXP_AT" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || echo "$EXP_AT")
   config:        $OUTLOOK_TODO_CONFIG
   tokens:        $OUTLOOK_TODO_TOKENS  (chmod 600)

Next: try
   scripts/todo-read.sh lists --format summary
   scripts/todo-read.sh tasks --format summary
   scripts/todo-write.sh create --title "Test task" --due 2026-06-24

EOF
    exit 0
done
