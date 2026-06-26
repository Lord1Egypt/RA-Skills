#!/usr/bin/env bash
# scripts/_lib.sh — shared functions for Indeed Bright Data scripts
# Source this file: source "${SCRIPT_DIR}/_lib.sh"
#
# Security summary (for auditors):
#   - Single external endpoint: https://api.brightdata.com/datasets/v3
#   - Only credential used: BRIGHTDATA_API_KEY (via Authorization header)
#   - Local writes: ~/.config/indeed-brightdata/ only (pending, history, results, datasets)
#   - No other env vars read, no other network calls, no shell-outs to external tools

# shellcheck disable=SC2034
readonly LIB_BASE_URL="https://api.brightdata.com/datasets/v3"
readonly LIB_JOBS_DATASET_ID="gd_l4dx9j9sscpvs7no2"
readonly LIB_CONFIG_DIR="${HOME}/.config/indeed-brightdata"
readonly LIB_DATASETS_FILE="${LIB_CONFIG_DIR}/datasets.json"
readonly LIB_PENDING_FILE="${LIB_CONFIG_DIR}/pending.json"
readonly LIB_HISTORY_FILE="${LIB_CONFIG_DIR}/history.json"
readonly LIB_RESULTS_DIR="${LIB_CONFIG_DIR}/results"
readonly LIB_CACHE_MAX_AGE_HOURS=6
readonly LIB_HISTORY_MAX_AGE_DAYS=7
readonly LIB_STALE_PENDING_HOURS=24

# Global set by make_api_request for callers to inspect
HTTP_CODE=""

# File used to persist HTTP_CODE across subshells (single-threaded only —
# concurrent calls within the same script will clobber this file)
_LIB_HTTP_CODE_FILE="$(mktemp "${TMPDIR:-/tmp}/.brightdata_http_code_XXXXXX")"
trap 'rm -f "$_LIB_HTTP_CODE_FILE"' EXIT

# make_api_request <method> <endpoint> [payload]
# Makes an authenticated API request to Bright Data.
# Sets global HTTP_CODE (also written to file for subshell access).
# Outputs response body to stdout.
# Returns 0 always (caller checks HTTP_CODE via check_http_status).
make_api_request() {
  local method="$1"
  local endpoint="$2"
  local payload="${3:-}"
  local api_key="${BRIGHTDATA_API_KEY:?Set BRIGHTDATA_API_KEY}"

  local curl_args=(-s -w "\n%{http_code}" -H "Authorization: Bearer ${api_key}")

  if [[ "$method" == "POST" ]]; then
    curl_args+=(-X POST -H "Content-Type: application/json" -d "$payload")
  fi

  local response
  if ! response=$(curl "${curl_args[@]}" "$endpoint"); then
    echo "Error: network request failed" >&2
    HTTP_CODE="000"
    echo "$HTTP_CODE" > "$_LIB_HTTP_CODE_FILE"
    echo ""
    return 0
  fi
  HTTP_CODE=$(echo "$response" | tail -1)
  echo "$HTTP_CODE" > "$_LIB_HTTP_CODE_FILE"
  local body
  body=$(echo "$response" | sed '$d')

  echo "$body"
  return 0
}

# _read_http_code — read HTTP_CODE from file (use after subshell calls)
_read_http_code() {
  if [[ -f "$_LIB_HTTP_CODE_FILE" ]]; then
    HTTP_CODE=$(cat "$_LIB_HTTP_CODE_FILE")
  fi
}

# check_http_status <http_code> <body> <action_description>
# Checks HTTP status code and prints error to stderr if not 200.
# Returns 0 on 200, 1 on any error.
check_http_status() {
  local http_code="$1"
  local body="$2"
  local action="$3"

  if ! [[ "$http_code" =~ ^[0-9]+$ ]]; then
    echo "Error: ${action} failed (invalid HTTP response)" >&2
    return 1
  fi

  if [[ "$http_code" -eq 200 ]]; then
    return 0
  fi

  if [[ "$http_code" -eq 429 ]]; then
    echo "Error: rate limit exceeded (HTTP 429). Try again later." >&2
    return 1
  fi

  echo "Error: ${action} failed (HTTP ${http_code}): ${body}" >&2
  return 1
}

# get_dataset_id <type>
# Returns dataset ID for the given type ("jobs" or "company").
# Jobs: returns hardcoded ID. Company: reads from config file.
# Outputs dataset ID to stdout. Returns 1 if not found.
get_dataset_id() {
  local type="$1"

  if [[ "$type" == "jobs" ]]; then
    echo "$LIB_JOBS_DATASET_ID"
    return 0
  fi

  if [[ "$type" == "company" ]]; then
    if [[ -f "$LIB_DATASETS_FILE" ]]; then
      local id
      id=$(jq -r '.company // empty' "$LIB_DATASETS_FILE")
      if [[ -n "$id" ]]; then
        echo "$id"
        return 0
      fi
    fi
    echo "Error: company dataset ID not configured." >&2
    echo "Run indeed_list_datasets.sh --save to discover and store dataset IDs." >&2
    return 1
  fi

  echo "Error: unknown dataset type: ${type}" >&2
  return 1
}

# extract_snapshot_id <json_body>
# Extracts snapshot_id from a /trigger response.
# Outputs snapshot_id to stdout. Returns 1 if not found.
extract_snapshot_id() {
  local body="$1"
  local snapshot_id
  if ! snapshot_id=$(echo "$body" | jq -r '.snapshot_id // empty' 2>/dev/null); then
    echo "Error: invalid JSON response: ${body:0:200}" >&2
    return 1
  fi
  if [[ -z "$snapshot_id" ]]; then
    echo "Error: no snapshot_id in response: ${body}" >&2
    return 1
  fi
  echo "$snapshot_id"
}

# _validate_snapshot_id <snapshot_id>
# Validates snapshot_id matches expected format. Returns 1 if invalid.
_validate_snapshot_id() {
  local snapshot_id="$1"
  if [[ ! "$snapshot_id" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    echo "Error: invalid snapshot_id: ${snapshot_id}" >&2
    return 1
  fi
}

# save_pending <snapshot_id> <description> <dataset_type> <script_name>
# Appends a pending snapshot entry to pending.json. Atomic write via temp+mv.
# Creates the file and config dir if they don't exist.
# Skips if snapshot_id is already in pending.
save_pending() {
  local snapshot_id="$1"
  local description="$2"
  local dataset_type="$3"
  local script_name="$4"

  _validate_snapshot_id "$snapshot_id" || return 1

  mkdir -p "$LIB_CONFIG_DIR"

  local existing="[]"
  if [[ -f "$LIB_PENDING_FILE" ]]; then
    existing=$(jq '.' "$LIB_PENDING_FILE" 2>/dev/null || echo "[]")
  fi

  # Skip duplicate
  if echo "$existing" | jq -e --arg id "$snapshot_id" 'any(.[]; .snapshot_id == $id)' >/dev/null 2>&1; then
    return 0
  fi

  local tmp_file
  tmp_file=$(mktemp "${LIB_CONFIG_DIR}/.pending_XXXXXX")

  local triggered_at
  triggered_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  if ! echo "$existing" | jq --arg sid "$snapshot_id" \
    --arg desc "$description" \
    --arg dtype "$dataset_type" \
    --arg scr "$script_name" \
    --arg ts "$triggered_at" \
    '. + [{"snapshot_id": $sid, "description": $desc, "dataset_type": $dtype, "triggered_at": $ts, "script": $scr}]' \
    > "$tmp_file"; then
    rm -f "$tmp_file"
    echo "Error: failed to update pending file" >&2
    return 1
  fi

  mv -f "$tmp_file" "$LIB_PENDING_FILE"
}

# load_pending
# Outputs pending.json contents to stdout. Returns empty array if file missing or invalid.
load_pending() {
  if [[ -f "$LIB_PENDING_FILE" ]]; then
    jq '.' "$LIB_PENDING_FILE" 2>/dev/null || echo "[]"
  else
    echo "[]"
  fi
}

# remove_pending <snapshot_id>
# Removes a pending entry by snapshot_id. Atomic write.
remove_pending() {
  local snapshot_id="$1"

  _validate_snapshot_id "$snapshot_id" || return 1

  if [[ ! -f "$LIB_PENDING_FILE" ]]; then
    return 0
  fi

  local tmp_file
  tmp_file=$(mktemp "${LIB_CONFIG_DIR}/.pending_XXXXXX")

  if ! jq --arg id "$snapshot_id" '[.[] | select(.snapshot_id != $id)]' \
    "$LIB_PENDING_FILE" > "$tmp_file"; then
    rm -f "$tmp_file"
    echo "Error: failed to update pending file" >&2
    return 1
  fi

  mv -f "$tmp_file" "$LIB_PENDING_FILE"
}

# save_result_file <snapshot_id> <json_content>
# Writes JSON results to results/<snapshot_id>.json. Creates dir if needed.
save_result_file() {
  local snapshot_id="$1"
  local json_content="$2"

  _validate_snapshot_id "$snapshot_id" || return 1
  mkdir -p "$LIB_RESULTS_DIR"

  local tmp_file
  tmp_file=$(mktemp "${LIB_RESULTS_DIR}/.result_XXXXXX")

  if ! echo "$json_content" | jq '.' > "$tmp_file" 2>/dev/null; then
    rm -f "$tmp_file"
    echo "Error: invalid JSON for result file" >&2
    return 1
  fi

  mv -f "$tmp_file" "${LIB_RESULTS_DIR}/${snapshot_id}.json"
}

# save_history <type> <params_json> <snapshot_id> <result_count> <result_file>
# Appends a search history entry. Atomic write.
save_history() {
  local type="$1"
  local params_json="$2"
  local snapshot_id="$3"
  local result_count="$4"
  local result_file="$5"

  mkdir -p "$LIB_CONFIG_DIR"

  local existing="[]"
  if [[ -f "$LIB_HISTORY_FILE" ]]; then
    existing=$(jq '.' "$LIB_HISTORY_FILE" 2>/dev/null || echo "[]")
  fi

  local tmp_file
  tmp_file=$(mktemp "${LIB_CONFIG_DIR}/.history_XXXXXX")

  local timestamp
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  if ! echo "$existing" | jq \
    --arg ts "$timestamp" \
    --arg tp "$type" \
    --argjson pr "$params_json" \
    --arg sid "$snapshot_id" \
    --argjson rc "$result_count" \
    --arg rf "$result_file" \
    '. + [{"timestamp": $ts, "type": $tp, "params": $pr, "snapshot_id": $sid, "result_count": $rc, "result_file": $rf}]' \
    > "$tmp_file"; then
    rm -f "$tmp_file"
    echo "Error: failed to update history file" >&2
    return 1
  fi

  mv -f "$tmp_file" "$LIB_HISTORY_FILE"
}

# check_history_cache <keyword> <country> <location> [<date_posted>]
# Checks for a matching search in history from the last 6 hours.
# If found and result file exists, outputs the result file path. Returns 0.
# If not found, returns 1.
check_history_cache() {
  local keyword="$1"
  local country="$2"
  local location="$3"
  local date_posted="${4:-}"

  if [[ ! -f "$LIB_HISTORY_FILE" ]]; then
    return 1
  fi

  local now_epoch
  now_epoch=$(date -u +%s)
  local cutoff_epoch=$((now_epoch - LIB_CACHE_MAX_AGE_HOURS * 3600))

  local result_file
  result_file=$(jq -r \
    --arg kw "$keyword" \
    --arg co "$country" \
    --arg loc "$location" \
    --arg dp "$date_posted" \
    --argjson cutoff "$cutoff_epoch" \
    '[.[] | select(
      (.params.keyword // "") == $kw and
      (.params.country // "") == $co and
      (.params.location // "") == $loc and
      (.params.date_posted // "") == $dp and
      ((.timestamp | fromdateiso8601) > $cutoff)
    )] | sort_by(.timestamp) | last | .result_file // empty' \
    "$LIB_HISTORY_FILE" 2>/dev/null)

  if [[ -n "$result_file" && -f "$result_file" ]]; then
    echo "$result_file"
    return 0
  fi

  return 1
}

# cleanup_old_entries
# Removes history entries older than 7 days and their result files.
# Removes stale pending entries older than 24 hours.
cleanup_old_entries() {
  local now_epoch
  now_epoch=$(date -u +%s)

  # Clean old history entries
  if [[ -f "$LIB_HISTORY_FILE" ]]; then
    local history_cutoff=$((now_epoch - LIB_HISTORY_MAX_AGE_DAYS * 86400))

    # Delete old result files
    jq -r --argjson cutoff "$history_cutoff" \
      '.[] | select((.timestamp | fromdateiso8601) <= $cutoff) | .result_file // empty' \
      "$LIB_HISTORY_FILE" 2>/dev/null | while IFS= read -r file; do
      [[ -n "$file" && -f "$file" ]] && rm -f "$file"
    done

    # Remove old entries from history
    local tmp_file
    tmp_file=$(mktemp "${LIB_CONFIG_DIR}/.history_XXXXXX")
    if jq --argjson cutoff "$history_cutoff" \
      '[.[] | select((.timestamp | fromdateiso8601) > $cutoff)]' \
      "$LIB_HISTORY_FILE" > "$tmp_file" 2>/dev/null; then
      mv -f "$tmp_file" "$LIB_HISTORY_FILE"
    else
      rm -f "$tmp_file"
    fi
  fi

  # Clean stale pending entries (>24h)
  if [[ -f "$LIB_PENDING_FILE" ]]; then
    local pending_cutoff=$((now_epoch - LIB_STALE_PENDING_HOURS * 3600))

    jq -r --argjson cutoff "$pending_cutoff" \
      '.[] | select((.triggered_at | fromdateiso8601) <= $cutoff) | .description // "unknown"' \
      "$LIB_PENDING_FILE" 2>/dev/null | while IFS= read -r desc; do
      echo "Warning: removing stale pending entry: ${desc}" >&2
    done

    local tmp_file
    tmp_file=$(mktemp "${LIB_CONFIG_DIR}/.pending_XXXXXX")
    if jq --argjson cutoff "$pending_cutoff" \
      '[.[] | select((.triggered_at | fromdateiso8601) > $cutoff)]' \
      "$LIB_PENDING_FILE" > "$tmp_file" 2>/dev/null; then
      mv -f "$tmp_file" "$LIB_PENDING_FILE"
    else
      rm -f "$tmp_file"
    fi
  fi
}
