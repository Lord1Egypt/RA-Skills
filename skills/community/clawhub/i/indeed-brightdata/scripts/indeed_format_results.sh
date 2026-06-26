#!/usr/bin/env bash
# Usage: indeed_format_results.sh [--type jobs|companies] [--format summary|csv] [--top N] [FILE]
# Formats raw JSON results from Bright Data into human-readable summaries or CSV.
# No API key required — this is a pure formatting script.
# Output: Formatted text to stdout, errors to stderr.

set -euo pipefail

readonly MAX_CHUNK_SIZE=3500
readonly SPLIT_MARKER="---SPLIT---"

show_help() {
  cat >&2 <<'EOF'
Usage: indeed_format_results.sh [OPTIONS] [FILE]

Format raw Indeed JSON results into human-readable summaries or CSV export.

Arguments:
  FILE                 JSON file to read (or pipe via stdin)

Options:
  --type TYPE          Result type: jobs or companies (default: jobs)
  --format FORMAT      Output format: summary or csv (default: summary)
  --top N              Limit to first N results
  --help               Show this help message

Input:
  Accepts JSON array directly or {"meta": {...}, "results": [...]} envelope.
  Reads from file argument or stdin (pipe).

Output:
  summary: Human-readable Telegram-friendly text with chunking
  csv:     RFC 4180 compliant CSV (no chunking)

Examples:
  indeed_format_results.sh results.json
  indeed_format_results.sh --type companies --format csv companies.json
  cat results.json | indeed_format_results.sh --top 5
  indeed_jobs_by_keyword.sh "nurse" US "Ohio" | indeed_format_results.sh
EOF
  exit 0
}

parse_args() {
  TYPE="jobs"
  FORMAT="summary"
  TOP=""
  INPUT_FILE=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --help) show_help ;;
      --type)
        [[ -n "${2:-}" ]] || { echo "Error: --type requires a value" >&2; exit 1; }
        case "$2" in
          jobs|companies) TYPE="$2" ;;
          *) echo "Error: --type must be 'jobs' or 'companies'" >&2; exit 1 ;;
        esac
        shift 2 ;;
      --format)
        [[ -n "${2:-}" ]] || { echo "Error: --format requires a value" >&2; exit 1; }
        case "$2" in
          summary|csv) FORMAT="$2" ;;
          *) echo "Error: --format must be 'summary' or 'csv'" >&2; exit 1 ;;
        esac
        shift 2 ;;
      --top)
        [[ -n "${2:-}" ]] || { echo "Error: --top requires a value" >&2; exit 1; }
        if ! [[ "$2" =~ ^[0-9]+$ ]] || [[ "$2" -eq 0 ]]; then
          echo "Error: --top must be a positive integer" >&2
          exit 1
        fi
        TOP="$2"
        shift 2 ;;
      -*)
        echo "Error: unknown option: $1" >&2; exit 1 ;;
      *)
        if [[ -n "$INPUT_FILE" ]]; then
          echo "Error: unexpected argument: $1" >&2; exit 1
        fi
        INPUT_FILE="$1"
        shift ;;
    esac
  done
}

# Read JSON input from file or stdin, unwrap envelope if present, apply --top
read_input() {
  local raw_json

  if [[ -n "$INPUT_FILE" ]]; then
    if [[ ! -f "$INPUT_FILE" ]]; then
      echo "Error: file not found: ${INPUT_FILE}" >&2
      exit 1
    fi
    raw_json=$(cat "$INPUT_FILE")
  else
    if [[ -t 0 ]]; then
      echo "Error: no input file specified and stdin is a terminal" >&2
      echo "Run with --help for usage" >&2
      exit 1
    fi
    raw_json=$(cat)
  fi

  # Unwrap {"meta": ..., "results": [...]} envelope
  local unwrapped
  unwrapped=$(echo "$raw_json" | jq '
    if (type == "object") and has("results") and (.results | type == "array")
    then .results
    else .
    end
  ')

  # Apply --top limit
  if [[ -n "$TOP" ]]; then
    unwrapped=$(echo "$unwrapped" | jq --argjson n "$TOP" '.[:$n]')
  fi

  echo "$unwrapped"
}

# Replace null/"null" with a fallback value using jq
jq_val() {
  local json="$1"
  local field="$2"
  local fallback="$3"
  echo "$json" | jq -r --arg fb "$fallback" "
    .${field} // null | if . == null or . == \"\" or . == \"null\" then \$fb else tostring end
  "
}

# Format a single job entry as summary text
format_job_summary() {
  local entry="$1"
  local index="$2"

  local title company rating reviews location job_type salary date_posted url

  title=$(jq_val "$entry" "job_title" "N/A")
  company=$(jq_val "$entry" "company_name" "N/A")
  rating=$(jq_val "$entry" "company_rating" "N/A")
  reviews=$(jq_val "$entry" "company_reviews_count" "N/A")
  location=$(jq_val "$entry" "job_location" "N/A")
  job_type=$(jq_val "$entry" "job_type" "N/A")
  salary=$(jq_val "$entry" "salary_formatted" "Not listed")
  date_posted=$(jq_val "$entry" "date_posted" "N/A")
  url=$(jq_val "$entry" "url" "N/A")

  # Build rating display — use printf to render the star emoji bytes
  local rating_display
  if [[ "$rating" == "N/A" ]]; then
    rating_display="N/A"
  else
    rating_display=$(printf '%s\xe2\xad\x90' "$rating")
  fi

  # Build qualifications
  local quals
  quals=$(echo "$entry" | jq -r '
    .qualifications // null |
    if . == null or (type == "array" and length == 0) then
      "See listing"
    else
      [.[:3][] | gsub("<[^>]*>"; "")] | join(", ")
    end
  ')

  printf '\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\n'
  printf '%s. %s\n' "$index" "$title"
  printf '\xf0\x9f\x8f\xa2 %s (%s, %s reviews)\n' "$company" "$rating_display" "$reviews"
  printf '\xf0\x9f\x93\x8d %s | %s\n' "$location" "$job_type"
  printf '\xf0\x9f\x92\xb0 %s\n' "$salary"
  printf '\xf0\x9f\x93\x85 Posted: %s\n' "$date_posted"
  printf '\xf0\x9f\x94\x97 %s\n' "$url"
  printf '\nKey qualifications: %s\n' "$quals"
  printf '\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\xe2\x94\x81\n'
}

# Format a single company entry as summary text
format_company_summary() {
  local entry="$1"
  local index="$2"

  local name rating reviews industry size hq website jobs_count

  name=$(jq_val "$entry" "name" "N/A")
  rating=$(jq_val "$entry" "overall_rating" "N/A")
  reviews=$(jq_val "$entry" "reviews_count" "N/A")
  industry=$(jq_val "$entry" "industry" "N/A")
  size=$(jq_val "$entry" "company_size" "Size N/A")
  hq=$(jq_val "$entry" "headquarters" "HQ N/A")
  website=$(jq_val "$entry" "website" "N/A")
  jobs_count=$(jq_val "$entry" "jobs_count" "N/A")

  printf '%s. %s\n' "$index" "$name"
  printf '\xe2\xad\x90 %s (%s reviews)\n' "$rating" "$reviews"
  printf '\xf0\x9f\x8f\xa2 %s | %s\n' "$industry" "$size"
  printf '\xf0\x9f\x93\x8d %s\n' "$hq"
  printf '\xf0\x9f\x8c\x90 %s\n' "$website"
  printf '\xf0\x9f\x92\xbc %s open positions\n' "$jobs_count"
}

# RFC 4180: escape a CSV field (double-quote if contains comma, quote, or newline)
csv_escape() {
  local field="$1"
  if [[ "$field" == *","* || "$field" == *'"'* || "$field" == *$'\n'* ]]; then
    # Double any internal quotes, then wrap in quotes
    field="${field//\"/\"\"}"
    field="\"${field}\""
  fi
  echo "$field"
}

# Build a CSV row from an array of fields
csv_row() {
  local first=true
  local result=""
  for field in "$@"; do
    local escaped
    escaped=$(csv_escape "$field")
    if [[ "$first" == true ]]; then
      result="$escaped"
      first=false
    else
      result="${result},${escaped}"
    fi
  done
  echo "$result"
}

# Format all results as jobs CSV
format_jobs_csv() {
  local data="$1"

  echo "job_title,company_name,location,salary,date_posted,url"

  local count
  count=$(echo "$data" | jq 'length')

  local i
  for (( i = 0; i < count; i++ )); do
    local entry
    entry=$(echo "$data" | jq ".[$i]")

    local title company location salary date_posted url
    title=$(jq_val "$entry" "job_title" "N/A")
    company=$(jq_val "$entry" "company_name" "N/A")
    location=$(jq_val "$entry" "job_location" "N/A")
    salary=$(jq_val "$entry" "salary_formatted" "Not listed")
    date_posted=$(jq_val "$entry" "date_posted" "N/A")
    url=$(jq_val "$entry" "url" "N/A")

    csv_row "$title" "$company" "$location" "$salary" "$date_posted" "$url"
  done
}

# Format all results as companies CSV
format_companies_csv() {
  local data="$1"

  echo "name,rating,industry,headquarters,website,jobs_count"

  local count
  count=$(echo "$data" | jq 'length')

  local i
  for (( i = 0; i < count; i++ )); do
    local entry
    entry=$(echo "$data" | jq ".[$i]")

    local name rating industry hq website jobs_count
    name=$(jq_val "$entry" "name" "N/A")
    rating=$(jq_val "$entry" "overall_rating" "N/A")
    industry=$(jq_val "$entry" "industry" "N/A")
    hq=$(jq_val "$entry" "headquarters" "N/A")
    website=$(jq_val "$entry" "website" "N/A")
    jobs_count=$(jq_val "$entry" "jobs_count" "N/A")

    csv_row "$name" "$rating" "$industry" "$hq" "$website" "$jobs_count"
  done
}

# Split summary output into chunks at entry boundaries (blank lines)
chunk_output() {
  local input="$1"
  local chunk=""
  local chunk_len=0

  while IFS= read -r line || [[ -n "$line" ]]; do
    local line_len=${#line}
    local new_len=$(( chunk_len + line_len + 1 ))  # +1 for newline

    # Check if this line starts a new entry (the separator line)
    # and if adding it would exceed the chunk size
    if [[ $chunk_len -gt 0 && $new_len -gt $MAX_CHUNK_SIZE ]]; then
      # Output current chunk (trim trailing newline)
      printf '%s' "$chunk"
      printf '\n%s\n' "$SPLIT_MARKER"
      chunk=""
      chunk_len=0
    fi

    if [[ $chunk_len -eq 0 ]]; then
      chunk="$line"
      chunk_len=$line_len
    else
      chunk="${chunk}"$'\n'"${line}"
      chunk_len=$(( chunk_len + line_len + 1 ))
    fi
  done <<< "$input"

  # Output remaining chunk
  if [[ -n "$chunk" ]]; then
    printf '%s\n' "$chunk"
  fi
}

# Format all results as summary text
format_summary() {
  local data="$1"
  local type="$2"

  local count
  count=$(echo "$data" | jq 'length')

  if [[ "$count" -eq 0 ]]; then
    echo "No results found." >&2
    return 0
  fi

  local all_output=""
  local i
  for (( i = 0; i < count; i++ )); do
    local entry
    entry=$(echo "$data" | jq ".[$i]")
    local index=$(( i + 1 ))

    local entry_text
    if [[ "$type" == "jobs" ]]; then
      entry_text=$(format_job_summary "$entry" "$index")
    else
      entry_text=$(format_company_summary "$entry" "$index")
    fi

    if [[ -z "$all_output" ]]; then
      all_output="$entry_text"
    else
      all_output="${all_output}"$'\n'"${entry_text}"
    fi
  done

  chunk_output "$all_output"
}

main() {
  parse_args "$@"

  local data
  data=$(read_input)

  # Validate JSON is an array
  local json_type
  json_type=$(echo "$data" | jq -r 'type')
  if [[ "$json_type" != "array" ]]; then
    echo "Error: expected JSON array, got ${json_type}" >&2
    exit 1
  fi

  if [[ "$FORMAT" == "csv" ]]; then
    if [[ "$TYPE" == "jobs" ]]; then
      format_jobs_csv "$data"
    else
      format_companies_csv "$data"
    fi
  else
    format_summary "$data" "$TYPE"
  fi
}

main "$@"
