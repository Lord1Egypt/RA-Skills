#!/usr/bin/env bash
# shop-cat.sh — 쇼핑인사이트 분야별 트렌드.
#
# Usage:
#   shop-cat.sh --start YYYY-MM-DD --end YYYY-MM-DD --time-unit (date|week|month) \
#               --category "label:50000000" [--category ...] \
#               [--device pc|mo] [--gender f|m] [--ages 10,20,30]
#
# Up to 3 categories. NOTE: shopping endpoints use age buckets in DECADES
# (10/20/30/40/50/60), unlike /search (which uses 1-9 codes).
# Output: JSONL — one line per (category × period).
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

start="" end="" tu="" device="" gender="" ages=""
declare -a cats=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --start)      start="$2"; shift 2;;
    --end)        end="$2";   shift 2;;
    --time-unit)  tu="$2";    shift 2;;
    --category)   cats+=("$2"); shift 2;;
    --device)     device="$2"; shift 2;;
    --gender)     gender="$2"; shift 2;;
    --ages)       ages="$2";  shift 2;;
    -h|--help)
      sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "error: unknown flag '$1'" >&2; exit 64;;
  esac
done

[[ -z "$start" || -z "$end" || -z "$tu" || ${#cats[@]} -eq 0 ]] && {
  echo "error: --start, --end, --time-unit, and at least one --category are required." >&2
  exit 64
}

valid_date "$start"; valid_date "$end"; valid_time_unit "$tu"
[[ "${#cats[@]}" -gt 3 ]] && { echo "error: max 3 --category blocks (got ${#cats[@]})." >&2; exit 64; }

require_bin curl jq
require_keys

cats_json=$(parse_categories_to_json "${cats[@]}")

body=$(jq -nc \
  --arg s "$start" --arg e "$end" --arg t "$tu" --argjson c "$cats_json" \
  '{startDate:$s, endDate:$e, timeUnit:$t, category:$c}')
body=$(add_filters "$body" "$device" "$gender" "$ages")

resp=$(datalab_post "shopping/categories" "$body")

echo "$resp" | jq -c '
  .results[]? as $r
  | $r.data[]? as $d
  | {category: $r.title, period: $d.period, ratio: $d.ratio}
'
