#!/usr/bin/env bash
# Usage: indeed_list_datasets.sh [--save]
# List available Bright Data dataset IDs and optionally save company ID to config.
# Env: BRIGHTDATA_API_KEY (required)
# Output: JSON to stdout

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR
source "${SCRIPT_DIR}/_lib.sh"

readonly LIST_URL="https://api.brightdata.com/datasets/list"

show_help() {
  cat >&2 <<'EOF'
Usage: indeed_list_datasets.sh [OPTIONS]

List available Bright Data Indeed dataset IDs.
Filters for Indeed-related datasets and displays them.

Options:
  --save               Save discovered dataset IDs to config file
  --help               Show this help message

Output:
  JSON object with jobs and company dataset IDs

Config:
  Saved to ~/.config/indeed-brightdata/datasets.json
EOF
  exit 0
}

parse_args() {
  SAVE=false

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --help) show_help ;;
      --save) SAVE=true; shift ;;
      -*) echo "Unknown option: $1" >&2; exit 1 ;;
      *) echo "Unknown argument: $1" >&2; exit 1 ;;
    esac
  done
}

fetch_datasets() {
  local body
  body=$(make_api_request GET "$LIST_URL")
  _read_http_code
  check_http_status "$HTTP_CODE" "$body" "list datasets" || return 1

  echo "$body"
}

filter_indeed_datasets() {
  local all_datasets="$1"
  # Filter for Indeed-related datasets by name/description
  echo "$all_datasets" | jq '[.[] | select(.name // "" | test("indeed"; "i"))]'
}

save_config() {
  local datasets="$1"
  if ! mkdir -p "$LIB_CONFIG_DIR"; then
    echo "Error: failed to create config directory: $LIB_CONFIG_DIR" >&2
    return 1
  fi

  # Extract company dataset ID (not the known jobs one)
  local company_id
  company_id=$(echo "$datasets" | jq -r \
    --arg jobs_id "$LIB_JOBS_DATASET_ID" \
    '[.[] | select(.id != $jobs_id)] | .[0].id // empty')

  local config
  config=$(jq -n \
    --arg jobs "$LIB_JOBS_DATASET_ID" \
    --arg company "$company_id" \
    '{jobs: $jobs, company: $company}')

  if ! echo "$config" > "$LIB_DATASETS_FILE"; then
    echo "Error: failed to write config file: $LIB_DATASETS_FILE" >&2
    return 1
  fi
  echo "Saved dataset IDs to ${LIB_DATASETS_FILE}" >&2
  echo "  Jobs: ${LIB_JOBS_DATASET_ID}" >&2
  echo "  Company: ${company_id:-not found}" >&2
}

main() {
  parse_args "$@"

  local all_datasets indeed_datasets
  all_datasets=$(fetch_datasets) || exit 1
  indeed_datasets=$(filter_indeed_datasets "$all_datasets")

  if [[ "$SAVE" == true ]]; then
    save_config "$indeed_datasets"
  fi

  echo "$indeed_datasets"
}

main "$@"
