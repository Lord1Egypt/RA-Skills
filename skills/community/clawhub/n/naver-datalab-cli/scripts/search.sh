#!/usr/bin/env bash
# search.sh — 통합 검색어 트렌드 (search keyword trends).
#
# Usage:
#   search.sh --start YYYY-MM-DD --end YYYY-MM-DD --time-unit (date|week|month) \
#             --group "label:kw1,kw2" [--group ...] \
#             [--device pc|mo] [--gender f|m] [--ages 1,2,3]
#
# Up to 5 --group flags. Each label is the bucket name; comma-separated
# keywords inside are treated as synonyms (their search counts are summed).
# Output: JSONL — one line per (group × period).
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

start="" end="" tu="" device="" gender="" ages=""
declare -a groups=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --start)      start="$2"; shift 2;;
    --end)        end="$2";   shift 2;;
    --time-unit)  tu="$2";    shift 2;;
    --group)      groups+=("$2"); shift 2;;
    --device)     device="$2"; shift 2;;
    --gender)     gender="$2"; shift 2;;
    --ages)       ages="$2";  shift 2;;
    -h|--help)
      sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "error: unknown flag '$1'" >&2; exit 64;;
  esac
done

[[ -z "$start" || -z "$end" || -z "$tu" || ${#groups[@]} -eq 0 ]] && {
  echo "error: --start, --end, --time-unit, and at least one --group are required." >&2
  exit 64
}

valid_date "$start"; valid_date "$end"; valid_time_unit "$tu"
[[ "${#groups[@]}" -gt 5 ]] && { echo "error: max 5 --group blocks (got ${#groups[@]})." >&2; exit 64; }

require_bin curl jq
require_keys

groups_json=$(parse_groups_to_json "${groups[@]}")

body=$(jq -nc \
  --arg s "$start" --arg e "$end" --arg t "$tu" --argjson g "$groups_json" \
  '{startDate:$s, endDate:$e, timeUnit:$t, keywordGroups:$g}')
body=$(add_filters "$body" "$device" "$gender" "$ages")

resp=$(datalab_post "search" "$body")

echo "$resp" | jq -c '
  .results[]? as $r
  | $r.data[]? as $d
  | {groupName: $r.title, period: $d.period, ratio: $d.ratio}
'
