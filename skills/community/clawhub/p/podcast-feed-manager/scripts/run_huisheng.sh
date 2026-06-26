#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_BASE_URL="https://huisheng.fm/api"

json_error() {
  local message="$1"
  printf '{\n  "ok": false,\n  "error": "%s"\n}\n' "$message" >&2
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

print_doctor() {
  local has_token="false"
  local has_curl="false"
  local curl_path=""

  if [[ -n "${HUISHENG_API_TOKEN:-}" ]]; then
    has_token="true"
  fi

  curl_path="$(command -v curl || true)"
  if [[ -n "$curl_path" ]]; then
    has_curl="true"
  fi

  cat <<JSON
{
  "ok": true,
  "scriptDir": "$SCRIPT_DIR",
  "hasToken": $has_token,
  "hasCurl": $has_curl,
  "curl": "$curl_path",
  "apiBaseUrl": "$API_BASE_URL"
}
JSON
}

print_help() {
  local cli="$0"

  cat <<HELP
huisheng.fm API Skill CLI

Usage:
  $cli doctor
  $cli list-feeds
  $cli get-feed <feed-key>
  $cli create-feed --json '{"title":"Daily Brief","siteUrl":"https://example.com"}'
  $cli update-feed <feed-key> --json '{"description":"Updated"}'
  $cli delete-feed <feed-key>
  $cli get-feed-config <feed-key>
  $cli list-episodes <feed-key> [--limit 50]
  $cli get-episode <feed-key> <episode-id>
  $cli create-episode <feed-key> --json '{"title":"Episode","audioUrl":"https://..."}'
  $cli update-episode <feed-key> <episode-id> --json '{"summary":"Updated"}'
  $cli delete-episode <feed-key> <episode-id>

Environment:
  HUISHENG_API_TOKEN is required for API requests.

Notes:
  The API URL is fixed: $API_BASE_URL
  The token is sent as Authorization: Bearer \$HUISHENG_API_TOKEN.
HELP
}

urlencode() {
  local input="$1"
  local output=""
  local i char hex

  LC_CTYPE=C
  for ((i = 0; i < ${#input}; i += 1)); do
    char="${input:i:1}"
    case "$char" in
      [a-zA-Z0-9.~_-])
        output+="$char"
        ;;
      *)
        printf -v hex '%%%02X' "'$char"
        output+="$hex"
        ;;
    esac
  done

  printf '%s' "$output"
}

require_arg() {
  local value="$1"
  local label="$2"

  if [[ -z "$value" ]]; then
    json_error "Missing $label."
    exit 1
  fi
}

read_payload() {
  local json=""
  local json_file=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --json)
        json="${2:-}"
        shift 2
        ;;
      --json=*)
        json="${1#--json=}"
        shift
        ;;
      --json-file)
        json_file="${2:-}"
        shift 2
        ;;
      --json-file=*)
        json_file="${1#--json-file=}"
        shift
        ;;
      *)
        shift
        ;;
    esac
  done

  if [[ -n "$json" && -n "$json_file" ]]; then
    json_error "Use either --json or --json-file, not both."
    exit 1
  fi

  if [[ -n "$json_file" ]]; then
    if [[ ! -f "$json_file" ]]; then
      json_error "JSON payload file not found: $json_file"
      exit 1
    fi
    cat "$json_file"
    return
  fi

  if [[ -n "$json" ]]; then
    printf '%s' "$json"
    return
  fi

  printf '{}'
}

get_flag_value() {
  local flag="$1"
  shift

  while [[ $# -gt 0 ]]; do
    case "$1" in
      "$flag")
        printf '%s' "${2:-}"
        return
        ;;
      "$flag="*)
        printf '%s' "${1#*=}"
        return
        ;;
      *)
        shift
        ;;
    esac
  done
}

require_token() {
  if [[ -z "${HUISHENG_API_TOKEN:-}" ]]; then
    json_error "Missing HUISHENG_API_TOKEN."
    exit 1
  fi
}

request() {
  local method="$1"
  local path="$2"
  local body="${3:-}"
  local url="$API_BASE_URL$path"
  local tmp_body=""
  local http_status=""

  require_token

  if ! command_exists curl; then
    json_error "curl is required when bundled scripts are unavailable."
    exit 1
  fi

  tmp_body="$(mktemp)"
  if [[ -n "$body" ]]; then
    http_status="$(
      curl -sS -o "$tmp_body" -w '%{http_code}' \
        -X "$method" \
        -H "Authorization: Bearer $HUISHENG_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data "$body" \
        "$url"
    )"
  else
    http_status="$(
      curl -sS -o "$tmp_body" -w '%{http_code}' \
        -X "$method" \
        -H "Authorization: Bearer $HUISHENG_API_TOKEN" \
        "$url"
    )"
  fi

  cat "$tmp_body"
  rm -f "$tmp_body"

  if [[ "$http_status" -lt 200 || "$http_status" -gt 299 ]]; then
    exit 1
  fi
}

if [[ "${1:-}" == "doctor" ]]; then
  print_doctor
  exit 0
fi

if [[ "${1:-}" == "--help" || "${1:-}" == "help" || $# -eq 0 ]]; then
  print_help
  exit 0
fi

command_name="$1"
shift || true

case "$command_name" in
  list-feeds)
    request GET "/feeds"
    ;;
  get-feed)
    require_arg "${1:-}" "feed key"
    feed_key="$(urlencode "${1:-}")"
    request GET "/feeds/$feed_key"
    ;;
  create-feed)
    request POST "/feeds" "$(read_payload "$@")"
    ;;
  update-feed)
    require_arg "${1:-}" "feed key"
    feed_key="$(urlencode "${1:-}")"
    shift || true
    request PATCH "/feeds/$feed_key" "$(read_payload "$@")"
    ;;
  delete-feed)
    require_arg "${1:-}" "feed key"
    feed_key="$(urlencode "${1:-}")"
    request DELETE "/feeds/$feed_key"
    ;;
  get-feed-config)
    require_arg "${1:-}" "feed key"
    feed_key="$(urlencode "${1:-}")"
    request GET "/feeds/$feed_key/config"
    ;;
  list-episodes)
    require_arg "${1:-}" "feed key"
    feed_key="$(urlencode "${1:-}")"
    limit="$(get_flag_value --limit "$@")"
    if [[ -n "$limit" ]]; then
      request GET "/feeds/$feed_key/episodes?limit=$limit"
    else
      request GET "/feeds/$feed_key/episodes"
    fi
    ;;
  get-episode)
    require_arg "${1:-}" "feed key"
    require_arg "${2:-}" "episode id"
    feed_key="$(urlencode "${1:-}")"
    episode_id="$(urlencode "${2:-}")"
    request GET "/feeds/$feed_key/episodes/$episode_id"
    ;;
  create-episode)
    require_arg "${1:-}" "feed key"
    feed_key="$(urlencode "${1:-}")"
    shift || true
    request POST "/feeds/$feed_key/episodes" "$(read_payload "$@")"
    ;;
  update-episode)
    require_arg "${1:-}" "feed key"
    require_arg "${2:-}" "episode id"
    feed_key="$(urlencode "${1:-}")"
    episode_id="$(urlencode "${2:-}")"
    shift 2 || true
    request PATCH "/feeds/$feed_key/episodes/$episode_id" "$(read_payload "$@")"
    ;;
  delete-episode)
    require_arg "${1:-}" "feed key"
    require_arg "${2:-}" "episode id"
    feed_key="$(urlencode "${1:-}")"
    episode_id="$(urlencode "${2:-}")"
    request DELETE "/feeds/$feed_key/episodes/$episode_id"
    ;;
  *)
    json_error "Unknown command: $command_name"
    exit 1
    ;;
esac
