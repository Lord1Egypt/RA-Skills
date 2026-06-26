#!/usr/bin/env bash
# Usage: indeed_jobs_by_keyword.sh <keyword> <country> <location> [OPTIONS]
# Discover jobs by keyword search (async).
# Env: BRIGHTDATA_API_KEY (required)
# Output: JSON to stdout

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR
source "${SCRIPT_DIR}/_lib.sh"

readonly DEFAULT_DOMAIN="indeed.com"
# shellcheck disable=SC2034
readonly DEFAULT_LIMIT_PER_INPUT=25
# shellcheck disable=SC2034
readonly DEFAULT_DATE_POSTED="Last 7 days"

show_help() {
  cat >&2 <<'EOF'
Usage: indeed_jobs_by_keyword.sh <keyword> <country> <location> [OPTIONS]

Discover job listings by keyword search on Indeed.

Arguments:
  keyword              Search keyword (e.g., "software engineer")
  country              Country code (e.g., US, GB, CA)
  location             Location string (e.g., "Austin, TX")

Options:
  --domain DOMAIN      Indeed domain (default: indeed.com)
  --date-posted VAL    Filter: "Last 24 hours", "Last 3 days", "Last 7 days", "Last 14 days"
  --pay RANGE          Filter by pay range
  --radius MILES       Location radius in miles
  --limit N            Max results to return
  --limit-per-input N  Max results per input keyword
  --all-time           Remove default date filter (default: "Last 7 days")
  --no-wait            Fire-and-forget: trigger and exit immediately
  --help               Show this help message

Output:
  Default: JSON array to stdout
  With --no-wait: JSON object {"status","snapshot_id","description"}

Examples:
  indeed_jobs_by_keyword.sh "nurse" US "Ohio"
  indeed_jobs_by_keyword.sh "software engineer" US "Austin, TX" --date-posted "Last 7 days"
  indeed_jobs_by_keyword.sh "warehouse" US "Dallas, TX" --limit 20
EOF
  exit 0
}

parse_args() {
  KEYWORD=""
  COUNTRY=""
  LOCATION=""
  DOMAIN="$DEFAULT_DOMAIN"
  DATE_POSTED="$DEFAULT_DATE_POSTED"
  PAY=""
  RADIUS=""
  LIMIT=""
  LIMIT_PER_INPUT="$DEFAULT_LIMIT_PER_INPUT"
  NO_WAIT=false

  local positional=0
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --help) show_help ;;
      --domain|--date-posted|--pay|--radius|--limit|--limit-per-input)
        [[ -n "${2:-}" ]] || { echo "Error: $1 requires a value" >&2; exit 1; }
        case "$1" in
          --domain) DOMAIN="$2" ;;
          --date-posted) DATE_POSTED="$2" ;;
          --pay) PAY="$2" ;;
          --radius) RADIUS="$2" ;;
          --limit) LIMIT="$2" ;;
          --limit-per-input) LIMIT_PER_INPUT="$2" ;;
        esac
        shift 2 ;;
      --all-time) DATE_POSTED=""; shift ;;
      --no-wait) NO_WAIT=true; shift ;;
      -*)
        echo "Unknown option: $1" >&2; exit 1 ;;
      *)
        case $positional in
          0) KEYWORD="$1" ;;
          1) COUNTRY="$1" ;;
          2) LOCATION="$1" ;;
          *) echo "Error: unexpected argument: $1" >&2; exit 1 ;;
        esac
        positional=$((positional + 1))
        shift
        ;;
    esac
  done

  if [[ -z "$KEYWORD" || -z "$COUNTRY" || -z "$LOCATION" ]]; then
    echo "Error: keyword, country, and location are required" >&2
    echo "Run with --help for usage" >&2
    exit 1
  fi
}

build_payload() {
  local payload
  payload=$(jq -n \
    --arg kw "$KEYWORD" \
    --arg co "$COUNTRY" \
    --arg dom "$DOMAIN" \
    --arg loc "$LOCATION" \
    '[{keyword_search: $kw, country: $co, domain: $dom, location: $loc}]')

  # Add optional fields
  if [[ -n "$DATE_POSTED" ]]; then
    payload=$(echo "$payload" | jq --arg v "$DATE_POSTED" '.[0].date_posted = $v')
  fi
  if [[ -n "$PAY" ]]; then
    payload=$(echo "$payload" | jq --arg v "$PAY" '.[0].pay = $v')
  fi
  if [[ -n "$RADIUS" ]]; then
    payload=$(echo "$payload" | jq --arg v "$RADIUS" '.[0].location_radius = $v')
  fi

  echo "$payload"
}

trigger_discovery() {
  local payload="$1"
  local dataset_id
  dataset_id=$(get_dataset_id jobs)
  local endpoint="${LIB_BASE_URL}/trigger?dataset_id=${dataset_id}&type=discover_new&discover_by=keyword"
  if [[ -n "$LIMIT" ]]; then
    endpoint="${endpoint}&limit_multiple_results=${LIMIT}"
  fi
  if [[ -n "$LIMIT_PER_INPUT" ]]; then
    endpoint="${endpoint}&limit_per_input=${LIMIT_PER_INPUT}"
  fi

  local body
  body=$(make_api_request POST "$endpoint" "$payload")
  _read_http_code
  check_http_status "$HTTP_CODE" "$body" "trigger" || return 1

  local snapshot_id
  snapshot_id=$(extract_snapshot_id "$body") || return 1

  local description="${KEYWORD} jobs in ${LOCATION}, ${COUNTRY}"

  if [[ "$NO_WAIT" == true ]]; then
    save_pending "$snapshot_id" "$description" "jobs" "indeed_jobs_by_keyword.sh"
    echo "Searching Indeed for \"${KEYWORD}\" in ${LOCATION}, ${COUNTRY}..." >&2
    jq -n --arg sid "$snapshot_id" --arg desc "$description" \
      '{"status":"pending","snapshot_id":$sid,"description":$desc}'
    return 0
  fi

  echo "Searching Indeed for \"${KEYWORD}\" in ${LOCATION}, ${COUNTRY}..." >&2
  "${SCRIPT_DIR}/indeed_poll_and_fetch.sh" "$snapshot_id" \
    --description "$description" --dataset-type "jobs"
}

main() {
  parse_args "$@"
  local payload
  payload=$(build_payload)
  trigger_discovery "$payload"
}

main "$@"
