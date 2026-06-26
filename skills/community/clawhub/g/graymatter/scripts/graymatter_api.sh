#!/usr/bin/env bash
set -euo pipefail

METHOD="${1:-}"
PATH_PART="${2:-}"
BODY="${3:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -z "$METHOD" || -z "$PATH_PART" ]]; then
  echo "Usage: $0 <GET|POST|PUT|PATCH|DELETE> <path> [json-body]" >&2
  exit 1
fi

BASE="${VALKYR_API_BASE:-https://api-0.valkyrlabs.com/v1}"
TOKEN=${VALKYR_AUTH_TOKEN:-${VALKYR_JWT_SESSION:-}}
LIGHT_MODE="${GRAYMATTER_LIGHT_MODE:-false}"
KEYCHAIN_SERVICE="${VALKYR_KEYCHAIN_SERVICE:-VALKYR_AUTH}"
USERNAME_SERVICE="${VALKYR_USERNAME_KEYCHAIN_SERVICE:-${KEYCHAIN_SERVICE}_USERNAME}"
PASSWORD_SERVICE="${VALKYR_PASSWORD_KEYCHAIN_SERVICE:-${KEYCHAIN_SERVICE}_PASSWORD}"
USERNAME=${GRAYMATTER_USERNAME:-${VALKYR_USERNAME:-}}
PASSWORD=${GRAYMATTER_PASSWORD:-${VALKYR_PASSWORD:-}}
BUY_CREDITS_URL="${VALKYR_BUY_CREDITS_URL:-https://valkyrlabs.com/graymatter/credits?source=graymatter&intent=recharge&operation=memory_query}"
HUMAN_SIGNUP_URL="${VALKYR_HUMAN_SIGNUP_URL:-https://valkyrlabs.com/graymatter/activate?source=graymatter&intent=signup&operation=memory_query}"
LOGIN_PATH="${GRAYMATTER_LOGIN_PATH:-/auth/login}"
FALLBACK_TMPDIR="${GRAYMATTER_TMPDIR:-${SCRIPT_DIR}/../tmp}"
CURL_CONNECT_TIMEOUT="${GRAYMATTER_CURL_CONNECT_TIMEOUT:-5}"
CURL_MAX_TIME="${GRAYMATTER_CURL_MAX_TIME:-20}"
TOKEN_REFRESH_SKEW_SECONDS="${GRAYMATTER_TOKEN_REFRESH_SKEW_SECONDS:-60}"

portable_mktemp() {
  local template="${1:-graymatter.XXXXXX}"
  local tmp_path=""

  if tmp_path="$(mktemp -t "$template" 2>/dev/null)" || tmp_path="$(mktemp "${template}" 2>/dev/null)"; then
    printf '%s\n' "$tmp_path"
    return 0
  fi

  mkdir -p "$FALLBACK_TMPDIR"
  if tmp_path="$(TMPDIR="$FALLBACK_TMPDIR" mktemp -t "$template" 2>/dev/null)" || tmp_path="$(mktemp "${FALLBACK_TMPDIR%/}/${template}" 2>/dev/null)"; then
    printf '%s\n' "$tmp_path"
    return 0
  fi

  echo "Unable to create temporary file for GrayMatter API transport" >&2
  return 1
}

decode_base64_url() {
  local value="${1:-}"
  local padded="$value"
  local remainder=$(( ${#padded} % 4 ))

  case "$remainder" in
    2) padded="${padded}==" ;;
    3) padded="${padded}=" ;;
    1) padded="${padded}===" ;;
  esac

  padded="$(printf '%s' "$padded" | tr '_-' '/+')"

  if printf '%s' "$padded" | base64 --decode 2>/dev/null; then
    return 0
  fi

  printf '%s' "$padded" | base64 -D 2>/dev/null
}

token_claims_json() {
  local token="${1:-}"
  local payload=""

  [[ -n "$token" ]] || return 1
  payload="$(printf '%s' "$token" | cut -d'.' -f2)"
  [[ -n "$payload" && "$payload" != "$token" ]] || return 1

  decode_base64_url "$payload"
}

token_is_clearly_read_only() {
  local token="${1:-}"
  local claims=""

  command -v jq >/dev/null 2>&1 || return 1

  claims="$(token_claims_json "$token" 2>/dev/null)" || return 1

  jq -e '
    def normalized_roles:
      ((.roles // []) + (.roleList // []) + (.authorities // []) + (.authorityList // []))
      | map(select(type == "string"))
      | unique;
    def non_trivial_roles:
      normalized_roles
      | map(select(. != "EVERYONE" and . != "FREE"));
    def normalized_scopes:
      (.scopes // [])
      | map(select(type == "string"))
      | unique;
    def non_readonly_scopes:
      normalized_scopes
      | map(select(. != "SCOPE_schema.read"));

    (non_trivial_roles | length) == 0 and (non_readonly_scopes | length) == 0
  ' >/dev/null 2>&1 <<<"$claims"
}

token_expires_soon() {
  local token="${1:-}"
  local claims=""
  local now=""

  command -v jq >/dev/null 2>&1 || return 1
  claims="$(token_claims_json "$token" 2>/dev/null)" || return 1
  now="$(date +%s)"

  jq -e \
    --argjson now "$now" \
    --argjson skew "$TOKEN_REFRESH_SKEW_SECONDS" \
    '(.exp? | type == "number") and (.exp <= ($now + $skew))' \
    >/dev/null 2>&1 <<<"$claims"
}

method_requires_write_access() {
  case "$METHOD_UPPER" in
    POST|PUT|PATCH|DELETE)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

fail_read_only_token() {
  local username_hint="${USERNAME:-unknown}"
  printf '{"error":"READ_ONLY_TOKEN","message":"GrayMatter auth token is read-only for %s. The current ValkyrAI login only grants schema-read access, so mutating requests cannot succeed. Update the account roles/scopes or supply a write-capable VALKYR_AUTH token."}\n' "$username_hint"
  exit 23
}

keychain_read() {
  local account="$1"
  local service="$2"
  security find-generic-password -a "$account" -s "$service" -w 2>/dev/null || true
}

store_token() {
  local token="$1"
  if [[ -z "$token" ]] || ! command -v security >/dev/null 2>&1; then
    return 0
  fi
  if [[ -n "$USERNAME" ]]; then
    security add-generic-password -U -a "$USERNAME" -s "$KEYCHAIN_SERVICE" -w "$token" >/dev/null
  fi
  security add-generic-password -U -a default -s "$KEYCHAIN_SERVICE" -w "$token" >/dev/null
}

run_login() {
  local login_cmd="${GRAYMATTER_LOGIN_COMMAND:-${SCRIPT_DIR}/gm-login}"
  if [[ ! -x "$login_cmd" ]]; then
    login_cmd="$(command -v gm-login 2>/dev/null || true)"
  fi

  if [[ -z "$login_cmd" || ! -x "$login_cmd" ]]; then
    return 1
  fi

  eval "$("$login_cmd" env)"
  TOKEN=${VALKYR_AUTH_TOKEN:-${VALKYR_JWT_SESSION:-}}
  if [[ -z "$USERNAME" ]] && command -v security >/dev/null 2>&1; then
    USERNAME=$(keychain_read default "$USERNAME_SERVICE")
  fi
  if [[ -z "$PASSWORD" && -n "$USERNAME" ]] && command -v security >/dev/null 2>&1; then
    PASSWORD=$(keychain_read "$USERNAME" "$PASSWORD_SERVICE")
  fi
}

if [[ -z "$USERNAME" ]] && command -v security >/dev/null 2>&1; then
  USERNAME=$(keychain_read default "$USERNAME_SERVICE")
fi

if [[ -z "$PASSWORD" && -n "$USERNAME" ]] && command -v security >/dev/null 2>&1; then
  PASSWORD=$(keychain_read "$USERNAME" "$PASSWORD_SERVICE")
fi

if [[ -z "$TOKEN" ]] && command -v security >/dev/null 2>&1; then
  if [[ -n "$USERNAME" ]]; then
    TOKEN=$(keychain_read "$USERNAME" "$KEYCHAIN_SERVICE")
  fi
  if [[ -z "$TOKEN" ]]; then
    TOKEN=$(keychain_read default "$KEYCHAIN_SERVICE")
  fi
  if [[ -z "$TOKEN" ]]; then
    TOKEN=$(keychain_read default openclaw-valkyrai-admin-jwtSession)
  fi
  if [[ -z "$TOKEN" && "$KEYCHAIN_SERVICE" != "VALKYR_AUTH" ]]; then
    TOKEN=$(keychain_read default VALKYR_AUTH)
  fi
fi

if [[ -z "$TOKEN" && "$LIGHT_MODE" != "true" ]]; then
  if ! run_login || [[ -z "$TOKEN" ]]; then
    echo "VALKYR_AUTH token is required. Checked VALKYR_AUTH_TOKEN, VALKYR_JWT_SESSION, keychain ${KEYCHAIN_SERVICE}, keychain openclaw-valkyrai-admin-jwtSession, and login did not produce a token." >&2
    exit 2
  fi
fi

URL="${BASE%/}/${PATH_PART#/}"
METHOD_UPPER="$(echo "$METHOD" | tr '[:lower:]' '[:upper:]')"

COMMON_HEADERS=(
  -H "accept: application/json"
)
if [[ -n "$TOKEN" ]]; then
  COMMON_HEADERS+=(
    -H "Authorization: Bearer ${TOKEN}"
    -H "VALKYR_AUTH: ${TOKEN}"
    -H "Cookie: VALKYR_AUTH=${TOKEN}"
  )
fi

show_insufficient_funds_guidance() {
  echo "Insufficient credits. Buy credits: ${BUY_CREDITS_URL}" >&2
  echo "Need an account? Sign up here: ${HUMAN_SIGNUP_URL}" >&2

  if command -v osascript >/dev/null 2>&1; then
    if osascript >/dev/null 2>&1 <<EOF
set buyUrl to "${BUY_CREDITS_URL}"
set signupUrl to "${HUMAN_SIGNUP_URL}"
set dialogText to "Your GrayMatter account has insufficient credits." & return & return & "Buy credits:" & return & buyUrl & return & return & "Human signup form:" & return & signupUrl
set resultButton to button returned of (display dialog dialogText buttons {"Not now", "Sign up", "Buy credits"} default button "Buy credits" with title "GrayMatter Credits")
if resultButton is "Buy credits" then
  do shell script "open " & quoted form of buyUrl
else if resultButton is "Sign up" then
  do shell script "open " & quoted form of signupUrl
end if
EOF
    then
      return
    fi
  fi

  if command -v powershell.exe >/dev/null 2>&1; then
    if VALKYR_BUY_URL="$BUY_CREDITS_URL" VALKYR_SIGNUP_URL="$HUMAN_SIGNUP_URL" powershell.exe -NoProfile -Command '
Add-Type -AssemblyName PresentationFramework
$buyUrl = $env:VALKYR_BUY_URL
$signupUrl = $env:VALKYR_SIGNUP_URL
$message = "Your GrayMatter account has insufficient credits.`n`nYes: Buy credits`nNo: Open human signup form`n`nBuy credits:`n$buyUrl`n`nSignup:`n$signupUrl"
$result = [System.Windows.MessageBox]::Show($message, "GrayMatter Credits", "YesNoCancel", "Warning")
if ($result -eq "Yes") { Start-Process $buyUrl }
elseif ($result -eq "No") { Start-Process $signupUrl }
' >/dev/null 2>&1; then
      return
    fi
  fi

  if command -v open >/dev/null 2>&1; then
    open "$BUY_CREDITS_URL" >/dev/null 2>&1 || true
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$BUY_CREDITS_URL" >/dev/null 2>&1 || true
  elif command -v cmd.exe >/dev/null 2>&1; then
    cmd.exe /C start "" "$BUY_CREDITS_URL" >/dev/null 2>&1 || true
  fi
}

RESPONSE_FILE="$(portable_mktemp graymatter-response.XXXXXX)"
RESPONSE_HEADERS="$(portable_mktemp graymatter-headers.XXXXXX)"
STATEFUL_COOKIE_JAR=""
STATEFUL_XSRF_TOKEN=""
cleanup() {
  rm -f "$RESPONSE_FILE"
  rm -f "$RESPONSE_HEADERS"
  if [[ -n "$STATEFUL_COOKIE_JAR" ]]; then
    rm -f "$STATEFUL_COOKIE_JAR"
  fi
}
trap cleanup EXIT

extract_token_from_login_response() {
  local body_file="$1"
  local headers_file="$2"
  local token=""

  if command -v jq >/dev/null 2>&1; then
    token="$(jq -r '.VALKYR_AUTH // .data.VALKYR_AUTH // .token // .session // .jwt // .jwtSession // .data.jwtSession // empty' "$body_file" 2>/dev/null || true)"
  fi
  if [[ -n "$token" && "$token" != "null" ]]; then
    printf '%s\n' "$token"
    return 0
  fi

  token="$(tr -d '\r' < "$headers_file" | grep -i 'set-cookie: .*VALKYR_AUTH=' | sed -E 's/.*VALKYR_AUTH=([^;]+).*/\1/' | head -n 1 || true)"
  if [[ -n "$token" ]]; then
    printf '%s\n' "$token"
    return 0
  fi

  token="$(tr -d '\r' < "$headers_file" | grep -i '^VALKYR_AUTH:' | sed -E 's/^[^:]+:[[:space:]]*//' | head -n 1 || true)"
  if [[ -n "$token" ]]; then
    printf '%s\n' "$token"
    return 0
  fi

  token="$(tr -d '\r' < "$headers_file" | grep -i '^authorization:' | sed -E 's/^[^:]+:[[:space:]]*Bearer[[:space:]]+//' | head -n 1 || true)"
  if [[ -n "$token" ]]; then
    printf '%s\n' "$token"
    return 0
  fi
}

refresh_token() {
  if [[ -z "$USERNAME" || -z "$PASSWORD" ]]; then
    return 1
  fi

  local login_body
  local login_headers
  local login_status
  login_body="$(portable_mktemp graymatter-login-body.XXXXXX)"
  login_headers="$(portable_mktemp graymatter-login-headers.XXXXXX)"

  set +e
  login_status="$(
    curl -sS \
      --connect-timeout "$CURL_CONNECT_TIMEOUT" \
      --max-time "$CURL_MAX_TIME" \
      -o "$login_body" -D "$login_headers" -w "%{http_code}" \
      -X POST "${BASE%/}/${LOGIN_PATH#/}" \
      -H "accept: application/json" \
      -H "content-type: application/json" \
      --data "$(jq -nc --arg username "$USERNAME" --arg password "$PASSWORD" '{username:$username,password:$password}')"
  )"
  local curl_status=$?
  set -e

  if (( curl_status != 0 )) || [[ ! "$login_status" =~ ^[0-9]{3}$ ]] || (( login_status >= 400 )); then
    rm -f "$login_body" "$login_headers"
    return 1
  fi

  local refreshed_token
  refreshed_token=$(extract_token_from_login_response "$login_body" "$login_headers")
  rm -f "$login_body" "$login_headers"

  if [[ -z "$refreshed_token" ]]; then
    return 1
  fi

  TOKEN=$refreshed_token
  if token_is_clearly_read_only "$TOKEN"; then
    return 0
  fi
  store_token "$TOKEN"
  return 0
}

prepare_stateful_auth_for_write() {
  if [[ -z "$USERNAME" || -z "$PASSWORD" || "$LIGHT_MODE" == "true" ]]; then
    return 1
  fi

  local login_body
  local login_headers
  local login_status
  login_body="$(portable_mktemp graymatter-login-body.XXXXXX)"
  login_headers="$(portable_mktemp graymatter-login-headers.XXXXXX)"
  STATEFUL_COOKIE_JAR="$(portable_mktemp graymatter-login-cookie.XXXXXX)"

  set +e
  login_status="$(
    curl -sS \
      --connect-timeout "$CURL_CONNECT_TIMEOUT" \
      --max-time "$CURL_MAX_TIME" \
      -o "$login_body" -D "$login_headers" -c "$STATEFUL_COOKIE_JAR" \
      -w "%{http_code}" \
      -X POST "${BASE%/}/${LOGIN_PATH#/}" \
      -H "accept: application/json" \
      -H "content-type: application/json" \
      --data "$(jq -nc --arg username "$USERNAME" --arg password "$PASSWORD" '{username:$username,password:$password}')"
  )"
  local curl_status=$?
  set -e

  if (( curl_status != 0 )) || [[ ! "$login_status" =~ ^[0-9]{3}$ ]] || (( login_status >= 400 )); then
    rm -f "$login_body" "$login_headers"
    return 1
  fi

  local refreshed_token
  refreshed_token=$(extract_token_from_login_response "$login_body" "$login_headers")
  if [[ -z "$refreshed_token" && -s "$STATEFUL_COOKIE_JAR" ]]; then
    refreshed_token=$(awk '$6 == "VALKYR_AUTH" {print $7}' "$STATEFUL_COOKIE_JAR" | tail -n 1)
  fi
  STATEFUL_XSRF_TOKEN="$(awk '$6 == "XSRF-TOKEN" {print $7}' "$STATEFUL_COOKIE_JAR" | tail -n 1)"
  rm -f "$login_body" "$login_headers"

  if [[ -n "$refreshed_token" ]]; then
    TOKEN=$refreshed_token
    store_token "$TOKEN"
  fi

  [[ -s "$STATEFUL_COOKIE_JAR" && -n "$STATEFUL_XSRF_TOKEN" ]]
}

if [[ -n "$TOKEN" ]] && token_expires_soon "$TOKEN"; then
  if refresh_token && [[ -n "$TOKEN" ]] && ! token_expires_soon "$TOKEN"; then
    :
  elif run_login && [[ -n "$TOKEN" ]] && ! token_expires_soon "$TOKEN"; then
    :
  fi
fi

if method_requires_write_access && [[ -n "$TOKEN" ]] && token_is_clearly_read_only "$TOKEN"; then
  if refresh_token && [[ -n "$TOKEN" ]] && ! token_is_clearly_read_only "$TOKEN"; then
    :
  elif run_login && [[ -n "$TOKEN" ]] && ! token_is_clearly_read_only "$TOKEN"; then
    :
  else
    fail_read_only_token
  fi
fi

perform_request() {
  COMMON_HEADERS=(
    -H "accept: application/json"
  )
  if [[ -n "$TOKEN" ]]; then
    COMMON_HEADERS+=(
      -H "Authorization: Bearer ${TOKEN}"
      -H "VALKYR_AUTH: ${TOKEN}"
    )
    if [[ -z "$STATEFUL_COOKIE_JAR" ]]; then
      COMMON_HEADERS+=(
        -H "Cookie: VALKYR_AUTH=${TOKEN}"
      )
    fi
  fi
  if [[ -n "$STATEFUL_XSRF_TOKEN" ]]; then
    COMMON_HEADERS+=(
      -H "X-XSRF-TOKEN: ${STATEFUL_XSRF_TOKEN}"
    )
  fi

  CURL_ARGS=(
    -sS
    --connect-timeout "$CURL_CONNECT_TIMEOUT"
    --max-time "$CURL_MAX_TIME"
    -o "$RESPONSE_FILE"
    -D "$RESPONSE_HEADERS"
    -w "%{http_code}"
    -X "$METHOD_UPPER"
    "$URL"
    "${COMMON_HEADERS[@]}"
  )

  if [[ -n "$STATEFUL_COOKIE_JAR" && -s "$STATEFUL_COOKIE_JAR" ]]; then
    CURL_ARGS+=(
      -b "$STATEFUL_COOKIE_JAR"
    )
  fi

  if [[ -n "$BODY" ]]; then
    CURL_ARGS+=(
      -H "content-type: application/json"
      --data "$BODY"
    )
  fi

  set +e
  HTTP_STATUS="$(curl "${CURL_ARGS[@]}")"
  CURL_STATUS=$?
  set -e
}

if method_requires_write_access; then
  prepare_stateful_auth_for_write || true
fi

perform_request

if [[ "$HTTP_STATUS" == "401" || "$HTTP_STATUS" == "403" ]]; then
  if refresh_token; then
    perform_request
  elif run_login && [[ -n "$TOKEN" ]]; then
    perform_request
  fi
fi

if (( CURL_STATUS != 0 )); then
  if [[ -s "$RESPONSE_FILE" ]]; then
    cat "$RESPONSE_FILE"
    echo >&2
  fi
  exit "$CURL_STATUS"
fi

if [[ "$HTTP_STATUS" =~ ^[0-9]{3}$ ]] && (( HTTP_STATUS >= 400 )); then
  cat "$RESPONSE_FILE"
  echo >&2

  if command -v jq >/dev/null 2>&1; then
    if jq -e '.error == "INSUFFICIENT_FUNDS" or .insufficientFunds == true' "$RESPONSE_FILE" >/dev/null 2>&1; then
      show_insufficient_funds_guidance
    fi
  elif grep -q "INSUFFICIENT_FUNDS" "$RESPONSE_FILE" 2>/dev/null; then
    show_insufficient_funds_guidance
  fi

  exit 22
fi

cat "$RESPONSE_FILE"
