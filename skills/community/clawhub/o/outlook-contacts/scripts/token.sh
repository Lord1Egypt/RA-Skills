#!/usr/bin/env bash
# scripts/token.sh
# Inspect or refresh the Microsoft Graph access token used by outlook-contacts.
#
# Subcommands:
#   status    Show token presence & expiry (no token value ever printed).
#   refresh   Force a refresh using the refresh_token.
#   scopes    Show the scopes the token was issued for.
#   clear     Delete config.json + tokens.json (irreversible; user must re-run setup).
#
# Notes:
#   - Never prints the access_token or refresh_token to stdout or stderr.
#   - The /me probe used in `status` only requests `id,userPrincipalName`,
#     so it does not pull any email/calendar data.
#   - If the access token is still valid, `refresh` is a no-op (with a notice).
#   - Tokens and config are scoped to ~/.outlook-contacts/ by default; they are
#     not shared with outlook-calendar or outlook-todo.

set -Eeuo pipefail
IFS=$' \t\n'

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
# shellcheck source=./_lib.sh
. "$SCRIPT_DIR/_lib.sh"

usage() {
    cat >&2 <<'USAGE'
Usage: token.sh <subcommand>

Subcommands:
  status    Show whether tokens are present and when the access token expires.
            Also does a tiny /me probe (User.Read only) to confirm the token works.
  refresh   Force-refresh the access token (uses refresh_token). No-op if still valid.
  scopes    Print the scopes the stored token was issued for.
  clear     Delete config.json and tokens.json (you will need to re-run setup).
  -h, --help  Show this help.
USAGE
}

SUBCMD="${1:-status}"
shift || true

case "$SUBCMD" in
    -h|--help|"") usage; exit 0 ;;
    status|refresh|scopes|clear) : ;;
    *) usage; die "unknown subcommand: $SUBCMD" ;;
esac

ensure_dirs
load_config || die "config missing at $OUTLOOK_CONTACTS_CONFIG  (run scripts/setup-device-code.sh)"

cmd_status() {
    if ! load_tokens 2>/dev/null; then
        cat >&2 <<EOF
token: NOT PRESENT
config: $OUTLOOK_CONTACTS_CONFIG  (present)
next:   run scripts/setup-device-code.sh to sign in
EOF
        exit 2
    fi
    token_status
    cat >&2 <<EOF
config:   $OUTLOOK_CONTACTS_CONFIG
tokens:   $OUTLOOK_CONTACTS_TOKENS
client:   $OUTLOOK_CONTACTS_CLIENT_ID
tenant:   $OUTLOOK_CONTACTS_TENANT_ID
authority: $OUTLOOK_CONTACTS_AUTHORITY
EOF

    # Tiny /me probe to confirm reachability (User.Read only)
    local probe upn http
    probe=$(curl --silent --show-error --max-time 15 \
        -H "Authorization: Bearer ${OUTLOOK_CONTACTS_ACCESS_TOKEN}" \
        -H "Accept: application/json" \
        -o /dev/null -w '%{http_code}' \
        "${OUTLOOK_CONTACTS_GRAPH_BASE}/me?\$select=id,userPrincipalName") || http=000 || true
    http="$probe"
    if [[ "$http" =~ ^2 ]]; then
        log_info "/me probe OK (HTTP $http)"
    else
        log_warn "/me probe failed (HTTP $http); token may be stale or revoked"
        exit 3
    fi
}

cmd_refresh() {
    if ! load_tokens 2>/dev/null; then
        die "no tokens to refresh; run scripts/setup-device-code.sh"
    fi
    local now exp left
    now=$(now_epoch)
    exp="${OUTLOOK_CONTACTS_TOKEN_EXPIRES:-0}"
    left=$(( exp - now ))
    if (( left > 120 )); then
        cat >&2 <<EOF
token still valid for ${left}s; nothing to do.
(pass --force to refresh anyway)
EOF
        if [[ "${1:-}" != "--force" ]]; then
            exit 0
        fi
    fi
    if ! _refresh_access_token; then
        die "refresh failed; please re-run scripts/setup-device-code.sh"
    fi
    log_info "refresh OK"
}

cmd_scopes() {
    if [[ ! -f "$OUTLOOK_CONTACTS_TOKENS" ]]; then
        die "no tokens file; run scripts/setup-device-code.sh"
    fi
    jq -r '.scope // ""' "$OUTLOOK_CONTACTS_TOKENS" | tr ' ' '\n' | sort -u
}

cmd_clear() {
    if [[ "${1:-}" != "--yes-i-really-mean-it" ]]; then
        die "this deletes $OUTLOOK_CONTACTS_CONFIG and $OUTLOOK_CONTACTS_TOKENS.  Re-run with --yes-i-really-mean-it"
    fi
    rm -f "$OUTLOOK_CONTACTS_CONFIG" "$OUTLOOK_CONTACTS_TOKENS" "$OUTLOOK_CONTACTS_DEVICE"
    log_info "config and tokens deleted"
}

case "$SUBCMD" in
    status)  cmd_status  "$@" ;;
    refresh) cmd_refresh "$@" ;;
    scopes)  cmd_scopes  "$@" ;;
    clear)   cmd_clear   "$@" ;;
esac
