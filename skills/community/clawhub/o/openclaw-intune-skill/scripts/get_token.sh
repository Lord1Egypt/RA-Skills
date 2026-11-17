#!/usr/bin/env bash
# get_token.sh — obtain (and cache) a Microsoft Graph app-only access token.
#
# Usage:
#   scripts/get_token.sh            # ensure a valid token is cached; print cache path
#   scripts/get_token.sh --force    # ignore cache and fetch a fresh token
#
# Env (single tenant):
#   INTUNE_TENANT_ID, INTUNE_CLIENT_ID, INTUNE_CLIENT_SECRET
#
# Env (multi-tenant / MSP):
#   INTUNE_PROFILE=contoso  → uses INTUNE_CONTOSO_TENANT_ID,
#                             INTUNE_CONTOSO_CLIENT_ID,
#                             INTUNE_CONTOSO_CLIENT_SECRET
#
# The client secret is read from the environment and sent only to
# login.microsoftonline.com. It is NEVER printed, logged or cached.

set -euo pipefail

FORCE=0
for arg in "$@"; do
  case "$arg" in
    --force) FORCE=1 ;;
    *)
      echo "ERROR: unknown option '$arg'." >&2
      exit 2 ;;
  esac
done

# ---- resolve credentials (optionally via profile) --------------------------
PROFILE="${INTUNE_PROFILE:-}"
if [[ -n "$PROFILE" ]]; then
  P="$(echo "$PROFILE" | tr '[:lower:]-' '[:upper:]_')"
  TENANT_VAR="INTUNE_${P}_TENANT_ID"
  CLIENT_VAR="INTUNE_${P}_CLIENT_ID"
  SECRET_VAR="INTUNE_${P}_CLIENT_SECRET"
  TENANT_ID="${!TENANT_VAR:-}"
  CLIENT_ID="${!CLIENT_VAR:-}"
  CLIENT_SECRET="${!SECRET_VAR:-}"
  CACHE_KEY="$PROFILE"
else
  TENANT_ID="${INTUNE_TENANT_ID:-}"
  CLIENT_ID="${INTUNE_CLIENT_ID:-}"
  CLIENT_SECRET="${INTUNE_CLIENT_SECRET:-}"
  CACHE_KEY="default"
fi

if [[ -z "$TENANT_ID" || -z "$CLIENT_ID" || -z "$CLIENT_SECRET" ]]; then
  echo "ERROR: missing credentials. Set INTUNE_TENANT_ID, INTUNE_CLIENT_ID," >&2
  echo "INTUNE_CLIENT_SECRET (or the INTUNE_<PROFILE>_* variants with INTUNE_PROFILE)." >&2
  exit 2
fi

# ---- cache ------------------------------------------------------------------
CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/intune-skill"
mkdir -p "$CACHE_DIR"
chmod 700 "$CACHE_DIR"
CACHE_FILE="$CACHE_DIR/token_${CACHE_KEY}.json"

now="$(date +%s)"
if [[ $FORCE -eq 0 && -f "$CACHE_FILE" ]]; then
  exp="$(jq -r '.expires_at // 0' "$CACHE_FILE" 2>/dev/null || echo 0)"
  # refresh 5 min before actual expiry
  if [[ "$exp" =~ ^[0-9]+$ ]] && (( now < exp - 300 )); then
    chmod 600 "$CACHE_FILE"
    printf '%s\n' "$CACHE_FILE"
    exit 0
  fi
fi

# ---- fetch ------------------------------------------------------------------
resp="$(curl -sS --fail-with-body \
  -X POST "https://login.microsoftonline.com/${TENANT_ID}/oauth2/v2.0/token" \
  --data-urlencode "client_id=${CLIENT_ID}" \
  --data-urlencode "scope=https://graph.microsoft.com/.default" \
  --data-urlencode "client_secret=${CLIENT_SECRET}" \
  --data-urlencode "grant_type=client_credentials")" || {
    # never echo the request (it contains the secret); show sanitized error only
    echo "ERROR: token request failed for tenant ${TENANT_ID}." >&2
    echo "$resp" | jq -r '.error_description // .error // "no details"' >&2 2>/dev/null || true
    exit 3
  }

token="$(echo "$resp" | jq -r '.access_token // empty')"
ttl="$(echo "$resp" | jq -r '.expires_in // 3599')"
if [[ -z "$token" ]]; then
  echo "ERROR: no access_token in response:" >&2
  echo "$resp" | jq -r '.error_description // .error // "unknown error"' >&2
  exit 3
fi

umask 077
jq -n --arg t "$token" --argjson e "$(( now + ttl ))" \
  '{access_token:$t, expires_at:$e}' > "$CACHE_FILE"
chmod 600 "$CACHE_FILE"

printf '%s\n' "$CACHE_FILE"
