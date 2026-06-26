#!/usr/bin/env bash
# Usage: indeed_smart_search.sh <keyword> <country> <location> [OPTIONS]
# Primary entry point for keyword-based job searches.
# Expands keywords, triggers parallel searches, polls snapshots,
# deduplicates results, and outputs JSON with metadata.
# Env: BRIGHTDATA_API_KEY (required)
# Output: JSON to stdout

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR
source "${SCRIPT_DIR}/_lib.sh"

readonly DEFAULT_DATE_POSTED="Last 7 days"
readonly SMART_LIMIT_PER_INPUT=15
readonly MAX_KEYWORDS=5
readonly MAX_OUTPUT_RESULTS=20
readonly MIN_RESULTS_THRESHOLD=5
readonly POLL_INTERVAL=20
readonly POLL_TIMEOUT=600

# --- Functions ---

show_help() {
  cat >&2 <<'EOF'
Usage: indeed_smart_search.sh <keyword> <country> <location> [OPTIONS]

Smart job search: expands keywords, runs parallel queries, deduplicates results.

Arguments:
  keyword    Search keyword (e.g., "cybersecurity")
  country    Country code (e.g., US, GB, CA)
  location   Location string (e.g., "Remote", "Austin, TX")

Options:
  --date-posted VAL   Date filter (default: "Last 7 days")
  --all-time          No date filter
  --no-expand         Skip keyword expansion, use original only
  --limit N           Max results in output (default: 20)
  --force             Bypass 6-hour cache
  --help              Show this help message

Output:
  JSON object with .meta and .results to stdout

Examples:
  indeed_smart_search.sh "cybersecurity" US "Remote"
  indeed_smart_search.sh "nursing" US "Ohio" --no-expand --limit 10
  indeed_smart_search.sh "data science" US "Austin, TX" --all-time --force
EOF
  exit 0
}

parse_args() {
  KEYWORD=""
  COUNTRY=""
  LOCATION=""
  DATE_POSTED="$DEFAULT_DATE_POSTED"
  NO_EXPAND=false
  FORCE=false
  LIMIT="$MAX_OUTPUT_RESULTS"
  ALL_TIME=false

  local positional=0
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --help) show_help ;;
      --date-posted)
        [[ -n "${2:-}" ]] || { echo "Error: --date-posted requires a value" >&2; exit 1; }
        DATE_POSTED="$2"
        shift 2 ;;
      --limit)
        [[ -n "${2:-}" ]] || { echo "Error: --limit requires a value" >&2; exit 1; }
        [[ "$2" =~ ^[0-9]+$ && "$2" -gt 0 ]] || { echo "Error: --limit must be a positive integer" >&2; exit 1; }
        LIMIT="$2"
        shift 2 ;;
      --all-time) ALL_TIME=true; DATE_POSTED=""; shift ;;
      --no-expand) NO_EXPAND=true; shift ;;
      --force) FORCE=true; shift ;;
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

expand_keywords() {
  local keyword="$1"
  local expansions_file="${SCRIPT_DIR}/../references/keyword-expansions.json"

  if [[ "$NO_EXPAND" == true ]]; then
    echo "$keyword"
    return
  fi

  if [[ -f "$expansions_file" ]]; then
    local keyword_lower
    keyword_lower=$(echo "$keyword" | tr '[:upper:]' '[:lower:]')
    local matches
    matches=$(jq -r --arg kw "$keyword_lower" \
      'to_entries[] | select(.key == $kw) | .value[]' \
      "$expansions_file" 2>/dev/null)

    if [[ -n "$matches" ]]; then
      echo "$matches" | head -n "$MAX_KEYWORDS"
      return
    fi
  fi

  # Fallback: original + suffix variations
  echo "$keyword"
  echo "${keyword} analyst"
  echo "${keyword} engineer"
  echo "${keyword} specialist"
}

trigger_searches() {
  local -a keywords=()
  while IFS= read -r kw; do
    [[ -n "$kw" ]] && keywords+=("$kw")
  done

  local -a snapshot_ids=()
  local keyword_script="${SCRIPT_DIR}/indeed_jobs_by_keyword.sh"

  for kw in "${keywords[@]}"; do
    local args=("$kw" "$COUNTRY" "$LOCATION" "--no-wait" "--limit-per-input" "$SMART_LIMIT_PER_INPUT")

    if [[ -n "$DATE_POSTED" ]]; then
      args+=("--date-posted" "$DATE_POSTED")
    else
      args+=("--all-time")
    fi

    local output
    if output=$("$keyword_script" "${args[@]}" 2>/dev/null); then
      local sid
      sid=$(echo "$output" | jq -r '.snapshot_id // empty' 2>/dev/null)
      if [[ -n "$sid" ]]; then
        snapshot_ids+=("$sid")
      fi
    else
      echo "Warning: failed to trigger search for keyword: ${kw}" >&2
    fi
  done

  echo "${snapshot_ids[*]}"
}

poll_all_snapshots() {
  local -a snapshot_ids
  read -ra snapshot_ids <<< "$1"
  local -a remaining=("${snapshot_ids[@]}")
  local all_results="[]"
  local elapsed=0

  echo "Polling ${#remaining[@]} snapshot(s)..." >&2

  while [[ ${#remaining[@]} -gt 0 && "$elapsed" -lt "$POLL_TIMEOUT" ]]; do
    local -a still_pending=()

    for sid in "${remaining[@]}"; do
      local body
      body=$(make_api_request GET "${LIB_BASE_URL}/progress/${sid}")
      _read_http_code

      if ! check_http_status "$HTTP_CODE" "$body" "progress check for ${sid}" 2>/dev/null; then
        echo "Warning: failed to check progress for ${sid}" >&2
        still_pending+=("$sid")
        continue
      fi

      local status
      status=$(echo "$body" | jq -r '.status // "unknown"' 2>/dev/null)

      case "$status" in
        ready)
          echo "Snapshot ${sid} ready. Fetching..." >&2
          local result_body
          result_body=$(make_api_request GET "${LIB_BASE_URL}/snapshot/${sid}?format=json")
          _read_http_code

          if check_http_status "$HTTP_CODE" "$result_body" "fetch ${sid}" 2>/dev/null; then
            # Save individual result file
            save_result_file "$sid" "$result_body" 2>/dev/null || true

            # Merge into all_results — handle both array and object responses
            all_results=$(jq -n \
              --argjson existing "$all_results" \
              --argjson new_data "$result_body" \
              'if ($new_data | type) == "array" then $existing + $new_data
               else $existing + [$new_data] end')
          else
            echo "Warning: failed to fetch results for ${sid}" >&2
          fi
          ;;
        failed)
          echo "Warning: snapshot ${sid} failed" >&2
          ;;
        *)
          still_pending+=("$sid")
          ;;
      esac
    done

    remaining=("${still_pending[@]+"${still_pending[@]}"}")

    if [[ ${#remaining[@]} -gt 0 ]]; then
      echo "Status: ${#remaining[@]} pending (${elapsed}s/${POLL_TIMEOUT}s)" >&2
      sleep "$POLL_INTERVAL"
      elapsed=$((elapsed + POLL_INTERVAL))
    fi
  done

  # Save any remaining as pending
  for sid in "${remaining[@]+"${remaining[@]}"}"; do
    if [[ -n "$sid" ]]; then
      save_pending "$sid" "smart_search: ${KEYWORD}" "jobs" "indeed_smart_search.sh" 2>/dev/null || true
      echo "Warning: snapshot ${sid} still processing, saved to pending" >&2
    fi
  done

  echo "$all_results"
}

dedup_and_filter() {
  local raw_json="$1"
  echo "$raw_json" | jq '
    # Group by jobid, preserving jobs without jobid (use index as fallback)
    to_entries
    | group_by(.value.jobid // ("_no_id_" + (.key | tostring)))
    | map(.[0].value)
    # Filter expired
    | [.[] | select((.is_expired // false) != true)]
    # Sort by date descending
    | sort_by(.date_posted_parsed // "1970-01-01") | reverse
  '
}

apply_limit() {
  local json="$1"
  echo "$json" | jq --argjson limit "$LIMIT" '.[:$limit]'
}

build_output() {
  local results="$1"
  local total_raw="$2"
  local keywords_json="$3"
  local date_expanded_to="${4:-}"
  local after_dedup="${5:-0}"

  local after_filter
  after_filter=$(echo "$results" | jq 'length')

  local date_filter_display
  if [[ -n "$DATE_POSTED" ]]; then
    date_filter_display="$DATE_POSTED"
  else
    date_filter_display="all time"
  fi

  jq -n \
    --arg query "$KEYWORD" \
    --arg location "$LOCATION" \
    --arg country "$COUNTRY" \
    --arg date_filter "$date_filter_display" \
    --arg expanded_to_raw "$date_expanded_to" \
    --argjson keywords_used "$keywords_json" \
    --argjson total_raw "$total_raw" \
    --argjson after_dedup "$after_dedup" \
    --argjson after_filter "$after_filter" \
    --argjson results "$results" \
    '{
      "meta": {
        "query": $query,
        "location": $location,
        "country": $country,
        "date_filter": $date_filter,
        "expanded_to": (if $expanded_to_raw == "" then null else $expanded_to_raw end),
        "keywords_used": $keywords_used,
        "total_raw": $total_raw,
        "after_dedup": $after_dedup,
        "after_filter": $after_filter
      },
      "results": $results
    }'
}

main() {
  parse_args "$@"

  # Check cache unless --force
  if [[ "$FORCE" != true ]]; then
    local cached_file
    if cached_file=$(check_history_cache "$KEYWORD" "$COUNTRY" "$LOCATION" "$DATE_POSTED"); then
      echo "Using cached results from: ${cached_file}" >&2
      cat "$cached_file"
      return 0
    fi
  fi

  # Expand keywords
  local -a keywords=()
  while IFS= read -r kw; do
    [[ -n "$kw" ]] && keywords+=("$kw")
  done < <(expand_keywords "$KEYWORD")

  local keywords_json
  keywords_json=$(printf '%s\n' "${keywords[@]}" | jq -R . | jq -s .)

  echo "Searching with ${#keywords[@]} keyword(s): ${keywords[*]}" >&2

  # Trigger parallel searches
  local snapshot_ids_str
  snapshot_ids_str=$(printf '%s\n' "${keywords[@]}" | trigger_searches)

  if [[ -z "$snapshot_ids_str" ]]; then
    echo "Error: no searches could be triggered" >&2
    exit 1
  fi

  local -a snapshot_ids
  read -ra snapshot_ids <<< "$snapshot_ids_str"
  echo "Triggered ${#snapshot_ids[@]} search(es)" >&2

  # Poll all snapshots
  local raw_results
  raw_results=$(poll_all_snapshots "$snapshot_ids_str")

  local total_raw
  total_raw=$(echo "$raw_results" | jq 'length')

  # Dedup and filter (without limit cap) for threshold check
  local deduped
  deduped=$(dedup_and_filter "$raw_results")

  local deduped_count
  deduped_count=$(echo "$deduped" | jq 'length')

  local date_expanded_to=""

  # If too few results with default date filter, expand to 30 days
  if [[ "$deduped_count" -lt "$MIN_RESULTS_THRESHOLD" \
     && "$DATE_POSTED" == "$DEFAULT_DATE_POSTED" \
     && "$ALL_TIME" != true ]]; then
    echo "Only ${deduped_count} results found. Expanding to Last 30 days..." >&2

    local saved_date="$DATE_POSTED"
    DATE_POSTED="Last 30 days"

    local expanded_ids_str
    expanded_ids_str=$(printf '%s\n' "${keywords[@]}" | trigger_searches)

    if [[ -n "$expanded_ids_str" ]]; then
      local expanded_results
      expanded_results=$(poll_all_snapshots "$expanded_ids_str")

      # Merge with existing results
      raw_results=$(jq -n --argjson a "$raw_results" --argjson b "$expanded_results" '$a + $b')
      total_raw=$(echo "$raw_results" | jq 'length')

      deduped=$(dedup_and_filter "$raw_results")
      deduped_count=$(echo "$deduped" | jq 'length')
      date_expanded_to="Last 30 days"
    fi

    DATE_POSTED="$saved_date"
  fi

  # Apply limit cap
  local processed
  processed=$(apply_limit "$deduped")

  local result_count
  result_count=$(echo "$processed" | jq 'length')

  # Build output envelope
  local output
  output=$(build_output "$processed" "$total_raw" "$keywords_json" "$date_expanded_to" "$deduped_count")

  # Save result file and history
  local smart_snapshot_id
  smart_snapshot_id="smart_$(date -u +%s)_$$"
  local result_file="${LIB_RESULTS_DIR}/${smart_snapshot_id}.json"

  save_result_file "$smart_snapshot_id" "$output"

  local params_json
  params_json=$(jq -n \
    --arg kw "$KEYWORD" \
    --arg co "$COUNTRY" \
    --arg loc "$LOCATION" \
    --arg dp "$DATE_POSTED" \
    '{"keyword": $kw, "country": $co, "location": $loc, "date_posted": $dp}')

  save_history "smart_search" "$params_json" "$smart_snapshot_id" "$result_count" "$result_file"

  # Output JSON to stdout
  echo "$output"
}

main "$@"
