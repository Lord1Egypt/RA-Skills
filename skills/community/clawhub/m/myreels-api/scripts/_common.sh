#!/usr/bin/env bash
set -euo pipefail

_MYREELS_CONFIG="${MYREELS_CONFIG:-$HOME/.myreels/config}"
[[ -f "$_MYREELS_CONFIG" ]] && source "$_MYREELS_CONFIG"

MYREELS_BASE_URL="${MYREELS_BASE_URL:-https://api.myreels.ai}"
MYREELS_LAST_HTTP_CODE=0
_MYREELS_CONNECT_TIMEOUT="${MYREELS_CONNECT_TIMEOUT:-10}"
_MYREELS_REQUEST_TIMEOUT="${MYREELS_REQUEST_TIMEOUT:-120}"

myreels_config_path() {
  printf '%s\n' "$_MYREELS_CONFIG"
}

myreels_require_base_url() {
  if [[ -z "${MYREELS_BASE_URL:-}" ]]; then
    echo "Missing required config: MYREELS_BASE_URL" >&2
    echo "Set it in $(myreels_config_path) or in the environment." >&2
    return 1
  fi
}

myreels_require_token() {
  if [[ -z "${MYREELS_ACCESS_TOKEN:-}" ]]; then
    echo "Missing required config: MYREELS_ACCESS_TOKEN" >&2
    echo "Set it in $(myreels_config_path) or in the environment." >&2
    return 1
  fi
}

myreels_mask_secret() {
  local value="${1:-}"

  if [[ -z "$value" ]]; then
    printf '%s\n' ""
    return 0
  fi

  if [[ ${#value} -le 12 ]]; then
    printf '%s\n' "$value"
    return 0
  fi

  printf '%s...%s\n' "${value:0:8}" "${value: -4}"
}

_myreels_is_json() {
  local payload="${1:-}"
  [[ -n "$payload" ]] && jq -e . >/dev/null 2>&1 <<<"$payload"
}

_myreels_auth_header() {
  printf 'Authorization: Bearer %s' "$MYREELS_ACCESS_TOKEN"
}

_myreels_url() {
  local path="$1"

  if [[ "$path" =~ ^https?:// ]]; then
    printf '%s\n' "$path"
  elif [[ "$path" == /* ]]; then
    printf '%s%s\n' "${MYREELS_BASE_URL%/}" "$path"
  else
    printf '%s/%s\n' "${MYREELS_BASE_URL%/}" "$path"
  fi
}

_myreels_emit_success() {
  local body="${1:-}"

  if [[ -z "$body" ]]; then
    return 0
  fi

  if _myreels_is_json "$body"; then
    jq '.' <<<"$body"
    return 0
  fi

  printf '%s\n' "$body"
}

_myreels_emit_error() {
  local http_code="${1:-0}"
  local body="${2:-}"
  local fallback_message="${3:-request failed}"
  local transport_error="${4:-}"

  export MYREELS_LAST_HTTP_CODE="$http_code"

  if [[ "$http_code" == "0" && -n "$transport_error" ]]; then
    jq -nc \
      --argjson httpCode 0 \
      --arg message "$fallback_message" \
      --arg details "$transport_error" \
      '{ok:false, httpCode:$httpCode, message:$message, details:$details}' >&2
    return 1
  fi

  if _myreels_is_json "$body"; then
    jq -c \
      --argjson httpCode "${http_code:-0}" \
      --arg fallbackMessage "$fallback_message" \
      '
      def data_value(key):
        if (.data | type) == "object" then .data[key] else null end;

      {
        ok: false,
        httpCode: $httpCode,
        message: (.message // .error // data_value("message") // data_value("error") // $fallbackMessage)
      }
      + (if (.status? // "") != "" then {status: .status} else {} end)
      + (if (.code? != null) then {code: .code} else {} end)
      + (if data_value("code") != null then {businessCode: data_value("code")} else {} end)
      + (
          if (.error? // "") != "" then
            {error: .error}
          elif data_value("error") != null and data_value("error") != "" then
            {error: data_value("error")}
          else
            {}
          end
        )
      + (
          if (.details? // "") != "" then
            {details: .details}
          elif data_value("details") != null and data_value("details") != "" then
            {details: data_value("details")}
          else
            {}
          end
        )
      ' <<<"$body" >&2
    return 1
  fi

  jq -nc \
    --argjson httpCode "${http_code:-0}" \
    --arg message "$fallback_message" \
    --arg details "${transport_error:-$body}" \
    '{ok:false, httpCode:$httpCode, message:$message} + (if $details != "" then {details:$details} else {} end)' >&2
  return 1
}

_myreels_request_json() {
  local method="$1"
  local path="$2"
  local body="${3:-}"
  local auth_mode="${4:-required}"
  shift 4 || true

  myreels_require_base_url

  case "$auth_mode" in
    required)
      myreels_require_token
      ;;
    optional|none)
      ;;
    *)
      echo "Error: invalid auth mode: $auth_mode" >&2
      return 1
      ;;
  esac

  local body_file header_file err_file
  local response http_code curl_status=0
  local -a curl_args

  body_file=$(mktemp)
  header_file=$(mktemp)
  err_file=$(mktemp)

  curl_args=(
    -sS
    --connect-timeout "$_MYREELS_CONNECT_TIMEOUT"
    --max-time "$_MYREELS_REQUEST_TIMEOUT"
    -X "$method"
    -H "Content-Type: application/json"
    -D "$header_file"
    -o "$body_file"
    -w '%{http_code}'
  )

  if [[ "$auth_mode" != "none" && -n "${MYREELS_ACCESS_TOKEN:-}" ]]; then
    curl_args+=(-H "$(_myreels_auth_header)")
  fi

  if [[ -n "$body" ]]; then
    curl_args+=(-d "$body")
  fi

  http_code=$(curl "${curl_args[@]}" "$@" "$(_myreels_url "$path")" 2>"$err_file") || curl_status=$?
  response=$(cat "$body_file")
  export MYREELS_LAST_HTTP_CODE="${http_code:-0}"

  if [[ $curl_status -ne 0 && "${http_code:-0}" == "000" ]]; then
    _myreels_emit_error 0 "" "Network request failed" "$(cat "$err_file")"
    rm -f "$body_file" "$header_file" "$err_file"
    return 1
  fi

  if [[ "${http_code:-0}" -ge 400 ]] 2>/dev/null; then
    _myreels_emit_error "$http_code" "$response" "request failed" "$(cat "$err_file")"
    rm -f "$body_file" "$header_file" "$err_file"
    return 1
  fi

  _myreels_emit_success "$response"
  rm -f "$body_file" "$header_file" "$err_file"
}

myreels_require_api_ok() {
  local payload="${1:-}"
  local fallback_message="${2:-request failed}"

  if ! _myreels_is_json "$payload"; then
    _myreels_emit_error "${MYREELS_LAST_HTTP_CODE:-0}" "$payload" "$fallback_message"
    return 1
  fi

  if jq -e '.status? == "failed"' >/dev/null 2>&1 <<<"$payload"; then
    _myreels_emit_error "${MYREELS_LAST_HTTP_CODE:-0}" "$payload" "$fallback_message"
    return 1
  fi

  return 0
}

myreels_get_public() {
  local path="$1"
  shift || true
  _myreels_request_json GET "$path" "" none "$@"
}

myreels_get_optional_auth() {
  local path="$1"
  shift || true
  _myreels_request_json GET "$path" "" optional "$@"
}

myreels_get_auth() {
  local path="$1"
  shift || true
  _myreels_request_json GET "$path" "" required "$@"
}

myreels_post_auth() {
  local path="$1"
  local body="${2:-}"
  shift 2 || true
  _myreels_request_json POST "$path" "$body" required "$@"
}
