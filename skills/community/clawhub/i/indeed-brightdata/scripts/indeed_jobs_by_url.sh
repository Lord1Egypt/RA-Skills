#!/usr/bin/env bash
# Usage: indeed_jobs_by_url.sh <url> [url2 ...] [--limit N]
# Collect job listing details from Indeed job URLs (sync).
# Env: BRIGHTDATA_API_KEY (required)
# Output: JSON to stdout

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR
source "${SCRIPT_DIR}/_lib.sh"

readonly MAX_SYNC_URLS=5

show_help() {
  cat >&2 <<'EOF'
Usage: indeed_jobs_by_url.sh <url> [url2 ...] [OPTIONS]

Collect detailed job listing data from Indeed job URLs.

Arguments:
  url                  One or more Indeed job URLs (e.g., https://www.indeed.com/viewjob?jk=abc123)

Options:
  --limit N            Max results per URL
  --help               Show this help message

Output:
  JSON array to stdout

Examples:
  indeed_jobs_by_url.sh "https://www.indeed.com/viewjob?jk=abc123"
  indeed_jobs_by_url.sh url1 url2 url3
EOF
  exit 0
}

parse_args() {
  URLS=()
  LIMIT=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --help) show_help ;;
      --limit) LIMIT="$2"; shift 2 ;;
      -*) echo "Unknown option: $1" >&2; exit 1 ;;
      *) URLS+=("$1"); shift ;;
    esac
  done

  if [[ ${#URLS[@]} -eq 0 ]]; then
    echo "Error: at least one URL is required" >&2
    echo "Run with --help for usage" >&2
    exit 1
  fi
}

build_payload() {
  local payload="[]"
  for url in "${URLS[@]}"; do
    payload=$(echo "$payload" | jq --arg u "$url" '. + [{"url": $u}]')
  done
  echo "$payload"
}

scrape_sync() {
  local payload="$1"
  local dataset_id
  dataset_id=$(get_dataset_id jobs)
  local endpoint="${LIB_BASE_URL}/scrape?dataset_id=${dataset_id}"
  if [[ -n "$LIMIT" ]]; then
    endpoint="${endpoint}&limit_per_input=${LIMIT}"
  fi

  local body
  body=$(make_api_request POST "$endpoint" "$payload")
  _read_http_code
  check_http_status "$HTTP_CODE" "$body" "scrape" || return 1

  echo "$body"
}

trigger_async() {
  local payload="$1"
  local dataset_id
  dataset_id=$(get_dataset_id jobs)
  local endpoint="${LIB_BASE_URL}/trigger?dataset_id=${dataset_id}"
  if [[ -n "$LIMIT" ]]; then
    endpoint="${endpoint}&limit_per_input=${LIMIT}"
  fi

  local body
  body=$(make_api_request POST "$endpoint" "$payload")
  _read_http_code
  check_http_status "$HTTP_CODE" "$body" "trigger" || return 1

  local snapshot_id
  snapshot_id=$(extract_snapshot_id "$body") || return 1

  echo "Triggered async job: ${snapshot_id}" >&2
  "${SCRIPT_DIR}/indeed_poll_and_fetch.sh" "$snapshot_id"
}

main() {
  parse_args "$@"

  local payload
  payload=$(build_payload)

  if [[ ${#URLS[@]} -le $MAX_SYNC_URLS ]]; then
    scrape_sync "$payload"
  else
    trigger_async "$payload"
  fi
}

main "$@"
