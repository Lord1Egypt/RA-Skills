#!/usr/bin/env bash
set -euo pipefail

SCRIPT_NAME=$(basename "$0")
HEALTH_EXPORT_CACHE=""
HEALTH_EXPORT_TEMPFILE=0
EXPORT_JSON_WARN_THRESHOLD=100000

phi_warning() {
  cat <<'PHI' >&2
===============================================================================
WARNING: Apple Health exports contain protected health information (PHI/PII).
Review the data before sharing, and delete any copies you no longer need.
===============================================================================
PHI
}

prepare_output_file() {
  local target="$1"
  local dir
  dir=$(dirname "$target")
  mkdir -p "$dir"
  local prev_umask
  prev_umask=$(umask)
  umask 0077
  : > "$target"
  umask "$prev_umask"
  chmod 600 "$target"
}

cleanup_export_cache() {
  if [[ "$HEALTH_EXPORT_TEMPFILE" -eq 1 && -n "$HEALTH_EXPORT_CACHE" ]]; then
    rm -f "$HEALTH_EXPORT_CACHE"
  fi
}
trap cleanup_export_cache EXIT

die() {
  echo "$SCRIPT_NAME: $*" >&2
  exit 1
}

usage() {
  cat <<'USAGE'
Usage: health-data.sh <command> [options]

Commands:
  list-types <export-path>
      List every HealthKit record type found in the export, sorted by frequency.

  summary <export-path>
      Report record count, coverage window, step/distance totals, sleep counts, and top sources.

  export-json <record-type> <export-path> [--limit N] [--out <file>]
      Emit JSON records of the requested type. Use --limit to avoid overwhelming output
      and/or --out to write to a restricted (600) file instead of stdout.

  help
      Show this help message.

Export paths can be either the folder Apple Health produces (containing export.xml) or the
zip file returned by the Health export workflow. Requires: xmlstarlet, jq, unzip.
USAGE
  exit 0
}

check_dependencies() {
  for bin in xmlstarlet jq unzip; do
    if ! command -v "$bin" >/dev/null 2>&1; then
      die "required dependency '$bin' is not installed"
    fi
  done
}

prepare_export() {
  local source="$1"
  [[ -n "$source" ]] || die "missing export path"

  if [[ -d "$source" ]]; then
    if [[ -f "$source/export.xml" ]]; then
      HEALTH_EXPORT_CACHE="$source/export.xml"
      return
    elif [[ -f "$source/apple_health_export/export.xml" ]]; then
      HEALTH_EXPORT_CACHE="$source/apple_health_export/export.xml"
      return
    else
      die "directory '$source' does not contain export.xml"
    fi
  elif [[ -f "$source" ]]; then
    local tmp
    tmp=$(mktemp)
    for member in export.xml apple_health_export/export.xml; do
      if unzip -p "$source" "$member" > "$tmp" 2>/dev/null; then
        HEALTH_EXPORT_CACHE="$tmp"
        HEALTH_EXPORT_TEMPFILE=1
        return
      fi
    done
    rm -f "$tmp"
    die "zip '$source' does not contain export.xml"
  else
    die "no such file or directory: '$source'"
  fi
}

ensure_export_loaded() {
  [[ -n "$HEALTH_EXPORT_CACHE" ]] || die "export not loaded"
}

records_tsv() {
  ensure_export_loaded
  xmlstarlet sel -t \
    -m '/HealthData/Record' \
    -v '@type' -o $'\t' \
    -v '@value' -o $'\t' \
    -v '@unit' -o $'\t' \
    -v '@startDate' -o $'\t' \
    -v '@endDate' -o $'\t' \
    -v '@sourceName' -o $'\t' \
    -v '@sourceVersion' -o $'\t' \
    -v '@device' -n \
    "$HEALTH_EXPORT_CACHE"
}

list_types_command() {
  ensure_export_loaded
  local count
  count=$(xmlstarlet sel -t -v 'count(/HealthData/Record)' "$HEALTH_EXPORT_CACHE")
  if [[ "$count" -eq 0 ]]; then
    echo "No HealthKit records found."
    return
  fi

  echo "Record type frequency (most to least common):"
  xmlstarlet sel -t -m '/HealthData/Record' -v '@type' -n "$HEALTH_EXPORT_CACHE" |
    sort |
    uniq -c |
    sort -rn |
    awk '{printf "%7s %s\n", $1, $2}'
}

summary_command() {
  ensure_export_loaded
  phi_warning
  local total_records
  total_records=$(xmlstarlet sel -t -v 'count(/HealthData/Record)' "$HEALTH_EXPORT_CACHE")
  if [[ "$total_records" -eq 0 ]]; then
    echo "Export contains no HealthKit records."
    return
  fi

  local earliest_start
  earliest_start=$(xmlstarlet sel -t -m '/HealthData/Record' -v '@startDate' -n "$HEALTH_EXPORT_CACHE" | sort | head -n1 || true)
  local latest_end
  latest_end=$(xmlstarlet sel -t -m '/HealthData/Record' -v '@endDate' -n "$HEALTH_EXPORT_CACHE" | sort | tail -n1 || true)

  local total_steps
  total_steps=$(
    { xmlstarlet sel -t -m "/HealthData/Record[@type='HKQuantityTypeIdentifierStepCount']" -v '@value' -n "$HEALTH_EXPORT_CACHE" || true; } |
      awk '{sum+=$1} END {printf "%.2f", sum+0}'
  )
  local total_distance
  total_distance=$(
    { xmlstarlet sel -t -m "/HealthData/Record[@type='HKQuantityTypeIdentifierDistanceWalkingRunning']" -v '@value' -n "$HEALTH_EXPORT_CACHE" || true; } |
      awk '{sum+=$1} END {printf "%.2f", sum+0}'
  )

  echo "Health export summary"
  echo "---------------------"
  echo "Records: $total_records"
  if [[ -n "$earliest_start" && -n "$latest_end" ]]; then
    echo "Coverage: $earliest_start → $latest_end"
  fi
  echo
  echo "Totals (distance usually reported in meters):"
  printf "  Step count total: %s steps\n" "$total_steps"
  printf "  Distance (walking/running): %s meters\n" "$total_distance"
  echo
  echo "Sleep analysis counts (HKCategoryValueSleepAnalysis*):"
  local sleep_breakdown
  sleep_breakdown=$(
    { xmlstarlet sel -t -m "/HealthData/Record[@type='HKCategoryTypeIdentifierSleepAnalysis']" -v '@value' -n "$HEALTH_EXPORT_CACHE" || true; } |
      sort | uniq -c | awk '{printf "  %7s %s\n", $1, $2}'
  )
  if [[ -z "$sleep_breakdown" ]]; then
    echo "  (none recorded)"
  else
    printf "%s" "$sleep_breakdown"
  fi
  echo
  echo "Top data sources (up to 5):"
  local source_breakdown
  source_breakdown=$(
    { xmlstarlet sel -t -m '/HealthData/Record' -v '@sourceName' -n "$HEALTH_EXPORT_CACHE" || true; } |
      sort | uniq -c | sort -rn | head -n5 | awk '{printf "  %7s %s\n", $1, $2}'
  )
  if [[ -z "$source_breakdown" ]]; then
    echo "  (no sources found)"
  else
    printf "%s" "$source_breakdown"
  fi
}

export_json_command() {
  ensure_export_loaded
  phi_warning
  local record_type="$1"
  local limit="$2"
  local output_path="${3:-}"
  local sink_fd=1
  local close_sink=0

  if [[ -n "$output_path" ]]; then
    prepare_output_file "$output_path"
    exec 3>"$output_path"
    sink_fd=3
    close_sink=1
  fi

  local jq_filter
  jq_filter=$(cat <<'EOF'
# parse_record keeps the same fields as the legacy output so downstream users are unaffected
def parse_record:
  split("\t") as $cols |
  ($cols[1]) as $raw |
  {
    type: $cols[0],
    value: (if $raw == "" then null
             elif ($raw | test("^-?[0-9]+\\.?[0-9]*$")) then ($raw | tonumber)
             else $raw end),
    unit: $cols[2],
    startDate: $cols[3],
    endDate: $cols[4],
    sourceName: $cols[5],
    sourceVersion: $cols[6],
    device: $cols[7]
  };
parse_record |
(if $type != "" then select(.type == $type) else . end)
EOF
)

  printf '[' >&$sink_fd
  local first=1
  local emitted=0
  local limit_number=$((limit + 0))

  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    local parsed
    if ! parsed=$(printf '%s\n' "$line" | jq -R -c --arg type "$record_type" "$jq_filter"); then
      die "failed to parse health record"
    fi
    [[ -z "$parsed" ]] && continue

    if [[ $first -eq 1 ]]; then
      first=0
    else
      printf ',\n' >&$sink_fd
    fi
    printf '%s' "$parsed" >&$sink_fd
    emitted=$((emitted + 1))

    if (( limit_number > 0 && emitted >= limit_number )); then
      break
    fi
    if (( limit_number == 0 && emitted == EXPORT_JSON_WARN_THRESHOLD )); then
      echo "$SCRIPT_NAME: warning: export-json has emitted $EXPORT_JSON_WARN_THRESHOLD records. Re-run with --limit to bound output." >&2
    fi
  done < <(records_tsv)

  if [[ $first -eq 1 ]]; then
    printf ']\n' >&$sink_fd
  else
    printf '\n]\n' >&$sink_fd
  fi

  if [[ $close_sink -eq 1 ]]; then
    exec 3>&-
  fi
}

main() {
  [[ $# -gt 0 ]] || die "missing command"
  local cmd="$1"
  shift

  case "$cmd" in
    help|-h|--help)
      usage
      ;;
    list-types)
      [[ $# -ge 1 ]] || usage
      check_dependencies
      prepare_export "$1"
      list_types_command
      ;;
    summary)
      [[ $# -ge 1 ]] || usage
      check_dependencies
      prepare_export "$1"
      summary_command
      ;;
    export-json)
      [[ $# -ge 2 ]] || usage
      local record_type="$1"
      local path="$2"
      shift 2
      local limit=0
      local out_path=""
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --limit)
            shift
            [[ $# -gt 0 ]] || die "--limit requires a value"
            limit="$1"
            if ! [[ "$limit" =~ ^[0-9]+$ ]]; then
              die "limit must be a non-negative integer"
            fi
            shift
            ;;
          --out)
            shift
            [[ $# -gt 0 ]] || die "--out requires a file path"
            out_path="$1"
            shift
            ;;
          *)
            die "unknown option '$1'"
            ;;
        esac
      done
      check_dependencies
      prepare_export "$path"
      export_json_command "$record_type" "$limit" "$out_path"
      ;;
    *)
      die "unknown command '$cmd'"
      ;;
  esac
}

main "$@"
