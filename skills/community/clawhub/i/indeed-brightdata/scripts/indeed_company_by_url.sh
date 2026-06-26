#!/usr/bin/env bash
# Usage: indeed_company_by_url.sh <url> [url2 ...] [--limit N]
# Collect company info from Indeed company URLs (sync).
# Env: BRIGHTDATA_API_KEY (required)
# Output: JSON to stdout

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR
source "${SCRIPT_DIR}/_lib.sh"

readonly MAX_SYNC_URLS=5

show_help() {
  cat >&2 <<'EOF'
Usage: indeed_company_by_url.sh <url> [url2 ...] [OPTIONS]

Collect company information from Indeed company page URLs.

Arguments:
  url                  One or more Indeed company URLs (e.g., https://www.indeed.com/cmp/Google)

Options:
  --limit N            Max results per URL
  --help               Show this help message

Output:
  JSON array to stdout

Note:
  Requires company dataset ID. Run indeed_list_datasets.sh first if not configured.
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

main() {
  parse_args "$@"

  local dataset_id
  dataset_id=$(get_dataset_id company) || exit 1

  local payload
  payload=$(build_payload)

  local endpoint
  if [[ ${#URLS[@]} -le $MAX_SYNC_URLS ]]; then
    endpoint="${LIB_BASE_URL}/scrape?dataset_id=${dataset_id}"
  else
    endpoint="${LIB_BASE_URL}/trigger?dataset_id=${dataset_id}"
  fi
  if [[ -n "$LIMIT" ]]; then
    endpoint="${endpoint}&limit_per_input=${LIMIT}"
  fi

  local body
  body=$(make_api_request POST "$endpoint" "$payload")
  _read_http_code
  check_http_status "$HTTP_CODE" "$body" "request" || return 1

  # If async, poll for results
  if [[ ${#URLS[@]} -gt $MAX_SYNC_URLS ]]; then
    local snapshot_id
    snapshot_id=$(extract_snapshot_id "$body") || return 1
    "${SCRIPT_DIR}/indeed_poll_and_fetch.sh" "$snapshot_id"
  else
    echo "$body"
  fi
}

main "$@"
