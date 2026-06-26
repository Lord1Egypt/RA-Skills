#!/usr/bin/env bash
# Usage: indeed_jobs_by_company.sh <company_jobs_url> [--limit N]
# Discover jobs from a company's Indeed jobs page (async).
# Env: BRIGHTDATA_API_KEY (required)
# Output: JSON to stdout

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR
source "${SCRIPT_DIR}/_lib.sh"

show_help() {
  cat >&2 <<'EOF'
Usage: indeed_jobs_by_company.sh <company_jobs_url> [OPTIONS]

Discover job listings from a company's Indeed jobs page.

Arguments:
  company_jobs_url     Indeed company jobs URL (e.g., https://www.indeed.com/cmp/Google/jobs)

Options:
  --limit N            Max results to return
  --limit-per-input N  Max results per input URL
  --no-wait            Fire-and-forget: trigger and exit immediately
  --help               Show this help message

Output:
  Default: JSON array to stdout
  With --no-wait: JSON object {"status","snapshot_id","description"}
EOF
  exit 0
}

parse_args() {
  URL=""
  LIMIT=""
  LIMIT_PER_INPUT=""
  NO_WAIT=false

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --help) show_help ;;
      --limit|--limit-per-input)
        [[ -n "${2:-}" ]] || { echo "Error: $1 requires a value" >&2; exit 1; }
        case "$1" in --limit) LIMIT="$2" ;; --limit-per-input) LIMIT_PER_INPUT="$2" ;; esac
        shift 2 ;;
      --no-wait) NO_WAIT=true; shift ;;
      -*) echo "Unknown option: $1" >&2; exit 1 ;;
      *) URL="$1"; shift ;;
    esac
  done

  if [[ -z "$URL" ]]; then
    echo "Error: company jobs URL is required" >&2
    echo "Run with --help for usage" >&2
    exit 1
  fi
}

main() {
  parse_args "$@"

  local dataset_id
  dataset_id=$(get_dataset_id jobs)

  local payload
  payload=$(jq -n --arg u "$URL" '[{url: $u}]')

  local endpoint="${LIB_BASE_URL}/trigger?dataset_id=${dataset_id}&type=discover_new&discover_by=url"
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

  local description="jobs from ${URL}"

  if [[ "$NO_WAIT" == true ]]; then
    save_pending "$snapshot_id" "$description" "jobs" "indeed_jobs_by_company.sh"
    echo "Discovering jobs from company page..." >&2
    jq -n --arg sid "$snapshot_id" --arg desc "$description" \
      '{"status":"pending","snapshot_id":$sid,"description":$desc}'
    return 0
  fi

  echo "Discovering jobs from company page..." >&2
  "${SCRIPT_DIR}/indeed_poll_and_fetch.sh" "$snapshot_id" \
    --description "$description" --dataset-type "jobs"
}

main "$@"
