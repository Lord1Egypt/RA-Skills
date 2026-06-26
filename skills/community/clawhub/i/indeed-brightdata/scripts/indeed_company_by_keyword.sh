#!/usr/bin/env bash
# Usage: indeed_company_by_keyword.sh <keyword> [--limit N]
# Discover companies by keyword search (async).
# Env: BRIGHTDATA_API_KEY (required)
# Output: JSON to stdout

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR
source "${SCRIPT_DIR}/_lib.sh"

# shellcheck disable=SC2034
readonly DEFAULT_LIMIT_PER_INPUT=25

show_help() {
  cat >&2 <<'EOF'
Usage: indeed_company_by_keyword.sh <keyword> [OPTIONS]

Discover companies on Indeed by keyword search.

Arguments:
  keyword              Company search keyword (e.g., "Tesla", "healthcare")

Options:
  --limit N            Max results to return
  --limit-per-input N  Max results per input keyword
  --no-wait            Fire-and-forget: trigger and exit immediately
  --help               Show this help message

Output:
  Default: JSON array to stdout
  With --no-wait: JSON object {"status","snapshot_id","description"}

Note:
  Requires company dataset ID. Run indeed_list_datasets.sh first if not configured.
EOF
  exit 0
}

parse_args() {
  KEYWORD=""
  LIMIT=""
  LIMIT_PER_INPUT="$DEFAULT_LIMIT_PER_INPUT"
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
      *) KEYWORD="$1"; shift ;;
    esac
  done

  if [[ -z "$KEYWORD" ]]; then
    echo "Error: keyword is required" >&2
    echo "Run with --help for usage" >&2
    exit 1
  fi
}

main() {
  parse_args "$@"

  local dataset_id
  dataset_id=$(get_dataset_id company) || exit 1

  local payload
  payload=$(jq -n --arg kw "$KEYWORD" '[{keyword: $kw}]')

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

  local description="${KEYWORD} companies"

  if [[ "$NO_WAIT" == true ]]; then
    save_pending "$snapshot_id" "$description" "company" "indeed_company_by_keyword.sh"
    echo "Searching Indeed companies for \"${KEYWORD}\"..." >&2
    jq -n --arg sid "$snapshot_id" --arg desc "$description" \
      '{"status":"pending","snapshot_id":$sid,"description":$desc}'
    return 0
  fi

  echo "Searching Indeed companies for \"${KEYWORD}\"..." >&2
  "${SCRIPT_DIR}/indeed_poll_and_fetch.sh" "$snapshot_id" \
    --description "$description" --dataset-type "company"
}

main "$@"
