#!/usr/bin/env bash
# graph.sh — Microsoft Graph wrapper for the Intune skill.
#
# Usage:
#   scripts/graph.sh GET    "/deviceManagement/managedDevices?\$select=deviceName"
#   scripts/graph.sh --confirm POST "/deviceManagement/managedDevices/{id}/syncDevice"
#   scripts/graph.sh --confirm POST "/deviceManagement/deviceCompliancePolicies" '{"displayName":"..."}'
#   scripts/graph.sh --confirm PATCH "/identity/conditionalAccess/policies/{id}" '{"state":"disabled"}'
#   scripts/graph.sh --confirm-name "DEVICE-NAME" DELETE "/deviceManagement/managedDevices/{id}"
#
# Behaviour:
#   * Paths default to v1.0; prefix with /beta/ for the beta API.
#   * GET: follows @odata.nextLink and merges all pages into one JSON
#     document ({"value":[...], "pages":N}); non-collection GETs pass through.
#   * Retries HTTP 429 honoring Retry-After (max 5 attempts).
#   * Adds "ConsistencyLevel: eventual" (+ $count=true) automatically for
#     $filter/$search queries on /users and /groups.
#   * Refreshes the token once on 401.
#   * Only documented Intune/Entra API areas are accepted.
#   * INTUNE_READ_ONLY=true blocks every non-GET request.
#   * Writes require --confirm; Tier 3 actions require --confirm-name.
#
# Depends on: curl, jq, scripts/get_token.sh (same directory).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

CONFIRMED=0
CONFIRM_NAME=""
POSITIONAL=()
while (( $# )); do
  case "$1" in
    --confirm)
      CONFIRMED=1
      shift ;;
    --confirm-name)
      [[ $# -ge 2 && -n "$2" ]] || {
        echo "ERROR: --confirm-name requires the exact object name." >&2
        exit 2
      }
      CONFIRM_NAME="$2"
      shift 2 ;;
    --)
      shift
      POSITIONAL+=("$@")
      break ;;
    -*)
      echo "ERROR: unknown option '$1'." >&2
      exit 2 ;;
    *)
      POSITIONAL+=("$1")
      shift ;;
  esac
done

(( ${#POSITIONAL[@]} >= 2 && ${#POSITIONAL[@]} <= 3 )) || {
  echo "Usage: graph.sh [--confirm|--confirm-name NAME] METHOD PATH [JSON_BODY]" >&2
  exit 2
}

METHOD="${POSITIONAL[0]}"; RAW_PATH="${POSITIONAL[1]}"; BODY="${POSITIONAL[2]:-}"
METHOD="$(echo "$METHOD" | tr '[:lower:]' '[:upper:]')"

case "$METHOD" in
  GET|POST|PATCH|PUT|DELETE) ;;
  *) echo "ERROR: unsupported HTTP method '$METHOD'." >&2; exit 2 ;;
esac

# ---- read-only guard --------------------------------------------------------
if [[ "${INTUNE_READ_ONLY:-false}" == "true" && "$METHOD" != "GET" ]]; then
  echo "ERROR: INTUNE_READ_ONLY=true — refusing $METHOD $RAW_PATH" >&2
  exit 4
fi

# ---- build URL ---------------------------------------------------------------
BASE="https://graph.microsoft.com"
case "$RAW_PATH" in
  https://graph.microsoft.com/*) URL="$RAW_PATH" ;;   # absolute (e.g. nextLink)
  https://*|http://*)
    echo "ERROR: refusing non-Graph URL '$RAW_PATH' — the bearer token is only ever sent to graph.microsoft.com" >&2
    exit 5 ;;
  /beta/*|/v1.0/*) URL="${BASE}${RAW_PATH}" ;;
  /*) URL="${BASE}/v1.0${RAW_PATH}" ;;
  *) URL="${BASE}/v1.0/${RAW_PATH}" ;;
esac

# ---- endpoint allowlist ------------------------------------------------------
API_PATH="${URL#"$BASE"}"
API_PATH="${API_PATH%%\?*}"
case "$API_PATH" in
  /v1.0/deviceManagement|/v1.0/deviceManagement/*|/beta/deviceManagement|/beta/deviceManagement/*|\
  /v1.0/deviceAppManagement|/v1.0/deviceAppManagement/*|/beta/deviceAppManagement|/beta/deviceAppManagement/*|\
  /v1.0/users|/v1.0/users/*|/beta/users|/beta/users/*|\
  /v1.0/groups|/v1.0/groups/*|/beta/groups|/beta/groups/*|\
  /v1.0/identity/conditionalAccess|/v1.0/identity/conditionalAccess/*|\
  /beta/identity/conditionalAccess|/beta/identity/conditionalAccess/*|\
  /v1.0/auditLogs|/v1.0/auditLogs/*|/beta/auditLogs|/beta/auditLogs/*)
    ;;
  *)
    echo "ERROR: Graph endpoint '$API_PATH' is outside the Intune skill allowlist." >&2
    exit 5 ;;
esac

# ---- enforced confirmation tiers -------------------------------------------
TIER=0
if [[ "$METHOD" != "GET" ]]; then
  TIER=2
  case "$METHOD:$API_PATH" in
    POST:*/managedDevices/*/syncDevice|POST:*/managedDevices/*/rebootNow|\
    POST:*/managedDevices/*/remoteLock|POST:*/managedDevices/*/locateDevice|\
    POST:*/notificationMessageTemplates/*/sendTestMessage|\
    POST:*/deviceManagement/reports/exportJobs)
      TIER=1 ;;
    POST:*/managedDevices/*/wipe|POST:*/managedDevices/*/retire|\
    POST:*/managedDevices/*/bypassActivationLock|\
    DELETE:*/deviceManagement/managedDevices/*|\
    DELETE:*/deviceManagement/windowsAutopilotDeviceIdentities/*|\
    DELETE:*/identity/conditionalAccess/policies/*)
      TIER=3 ;;
  esac
fi

if (( TIER == 3 )) && [[ -z "$CONFIRM_NAME" ]]; then
  echo "ERROR: Tier 3 action refused. Re-run with --confirm-name and the exact user-confirmed object name." >&2
  exit 7
fi
if (( TIER == 1 || TIER == 2 )) && (( CONFIRMED == 0 )); then
  echo "ERROR: Tier $TIER action refused. Obtain explicit user confirmation, then re-run with --confirm." >&2
  exit 7
fi

# ---- advanced-query headers for /users & /groups ------------------------------
# shellcheck disable=SC2016  # literal $filter/$search/$count are intentional
EXTRA_HEADER=""
if [[ "$URL" =~ /v1\.0/(users|groups)(/|\?|$) || "$URL" =~ /beta/(users|groups)(/|\?|$) ]]; then
  if [[ "$URL" == *'$filter='* || "$URL" == *'$search='* || "$URL" == *'$count='* ]]; then
    EXTRA_HEADER="ConsistencyLevel: eventual"
    [[ "$URL" != *'$count='* ]] && URL="${URL}$([[ "$URL" == *\?* ]] && echo '&' || echo '?')\$count=true"
  fi
fi

TOKEN_FILE="$("$SCRIPT_DIR/get_token.sh")"
TOKEN="$(jq -r '.access_token // empty' "$TOKEN_FILE")"
if [[ -z "$TOKEN" ]]; then
  echo "ERROR: token cache did not contain an access token." >&2
  exit 3
fi

# ---- single request with 429/401 handling -------------------------------------
do_request() { # $1=url ; echoes body ; returns 0/1
  local url="$1" attempt=0 http body hdrs
  local curl_args
  case "$url" in
    https://graph.microsoft.com/*) ;;
    *) echo "ERROR: refusing non-Graph URL '$url'" >&2; return 1 ;;
  esac
  while :; do
    attempt=$((attempt+1))
    hdrs="$(mktemp)"
    curl_args=(-sS -D "$hdrs" -o - -w '' \
      -X "$METHOD" "$url" \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json")
    [[ -n "$EXTRA_HEADER" ]] && curl_args+=(-H "$EXTRA_HEADER")
    [[ -n "$BODY" ]] && curl_args+=(--data "$BODY")
    body="$(curl "${curl_args[@]}")" || { rm -f "$hdrs"; return 1; }
    http="$(awk 'toupper($1) ~ /^HTTP/ {code=$2} END {print code}' "$hdrs")"

    if [[ "$http" == "429" ]]; then
      local wait
      wait="$(awk 'tolower($1)=="retry-after:" {gsub(/\r/,"",$2); print $2}' "$hdrs")"
      rm -f "$hdrs"
      [[ "$wait" =~ ^[0-9]+$ ]] || wait=10
      if (( attempt >= 5 )); then
        echo "ERROR: throttled (429) after $attempt attempts" >&2; return 1
      fi
      echo "throttled, waiting ${wait}s (attempt $attempt/5)…" >&2
      sleep "$wait"; continue
    fi

    if [[ "$http" == "401" && $attempt -eq 1 ]]; then
      rm -f "$hdrs"
      TOKEN_FILE="$("$SCRIPT_DIR/get_token.sh" --force)"
      TOKEN="$(jq -r '.access_token // empty' "$TOKEN_FILE")"
      [[ -n "$TOKEN" ]] || {
        echo "ERROR: refreshed token cache did not contain an access token." >&2
        return 1
      }
      continue
    fi

    rm -f "$hdrs"
    if [[ "$http" =~ ^2 ]]; then
      echo "$body"; return 0
    fi
    echo "ERROR: HTTP $http for $METHOD $url" >&2
    echo "$body" | jq -r '.error.message // .error_description // .' >&2 2>/dev/null || echo "$body" >&2
    return 1
  done
}

# ---- GET: paginate; others: single call ---------------------------------------
if [[ "$METHOD" == "GET" ]]; then
  merged='[]'; pages=0; next="$URL"
  while [[ -n "$next" ]]; do
    resp="$(do_request "$next")" || exit 1
    pages=$((pages+1))
    if echo "$resp" | jq -e 'has("value")' >/dev/null 2>&1; then
      merged="$(jq -c --argjson acc "$merged" '$acc + .value' <<<"$resp")"
      next="$(jq -r '."@odata.nextLink" // empty' <<<"$resp")"
    else
      # non-collection response (single object) — pass through
      echo "$resp"; exit 0
    fi
  done
  jq -n --argjson v "$merged" --argjson p "$pages" \
    --argjson c "$(jq 'length' <<<"$merged")" \
    '{value:$v, count:$c, pages:$p}'
else
  resp="$(do_request "$URL")" || exit 1
  [[ -n "$resp" ]] && echo "$resp" || echo '{"status":"ok"}'
fi
