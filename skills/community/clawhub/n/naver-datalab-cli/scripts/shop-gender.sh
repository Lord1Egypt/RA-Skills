#!/usr/bin/env bash
# shop-gender.sh — 분야의 성별 트렌드 (f / m).
#
# Usage:
#   shop-gender.sh --start YYYY-MM-DD --end YYYY-MM-DD --time-unit (date|week|month) \
#                  --category 50000000
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

start="" end="" tu="" cat=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --start)      start="$2"; shift 2;;
    --end)        end="$2";   shift 2;;
    --time-unit)  tu="$2";    shift 2;;
    --category)   cat="$2";   shift 2;;
    -h|--help)
      sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "error: unknown flag '$1'" >&2; exit 64;;
  esac
done

[[ -z "$start" || -z "$end" || -z "$tu" || -z "$cat" ]] && {
  echo "error: --start, --end, --time-unit, --category are required." >&2
  exit 64
}

valid_date "$start"; valid_date "$end"; valid_time_unit "$tu"
require_bin curl jq
require_keys

body=$(jq -nc \
  --arg s "$start" --arg e "$end" --arg t "$tu" --arg c "$cat" \
  '{startDate:$s, endDate:$e, timeUnit:$t, category:$c}')

resp=$(datalab_post "shopping/category/gender" "$body")

echo "$resp" | jq -c '
  .results[]? as $r
  | $r.data[]? as $d
  | {category: ($r.title // ""), group: $d.group, period: $d.period, ratio: $d.ratio}
'
