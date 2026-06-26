#!/usr/bin/env bash
# shop-keyword.sh — 쇼핑인사이트 분야 내 키워드 트렌드.
#
# Usage:
#   shop-keyword.sh --start YYYY-MM-DD --end YYYY-MM-DD --time-unit (date|week|month) \
#                   --category 50000000 \
#                   --keyword "label:kw1,kw2" [--keyword ...] \
#                   [--device pc|mo] [--gender f|m] [--ages 10,20,30]
#
# One category, up to 5 keyword buckets. Output: JSONL per (keyword × period).
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

start="" end="" tu="" cat="" device="" gender="" ages=""
declare -a kws=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --start)      start="$2"; shift 2;;
    --end)        end="$2";   shift 2;;
    --time-unit)  tu="$2";    shift 2;;
    --category)   cat="$2";   shift 2;;
    --keyword)    kws+=("$2"); shift 2;;
    --device)     device="$2"; shift 2;;
    --gender)     gender="$2"; shift 2;;
    --ages)       ages="$2";  shift 2;;
    -h|--help)
      sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "error: unknown flag '$1'" >&2; exit 64;;
  esac
done

[[ -z "$start" || -z "$end" || -z "$tu" || -z "$cat" || ${#kws[@]} -eq 0 ]] && {
  echo "error: --start, --end, --time-unit, --category, and at least one --keyword are required." >&2
  exit 64
}

valid_date "$start"; valid_date "$end"; valid_time_unit "$tu"
[[ "${#kws[@]}" -gt 5 ]] && { echo "error: max 5 --keyword blocks (got ${#kws[@]})." >&2; exit 64; }

require_bin curl jq
require_keys

kws_json=$(parse_keywords_to_json "${kws[@]}")

body=$(jq -nc \
  --arg s "$start" --arg e "$end" --arg t "$tu" --arg c "$cat" --argjson k "$kws_json" \
  '{startDate:$s, endDate:$e, timeUnit:$t, category:$c, keyword:$k}')
body=$(add_filters "$body" "$device" "$gender" "$ages")

resp=$(datalab_post "shopping/category/keywords" "$body")

echo "$resp" | jq -c '
  .results[]? as $r
  | $r.data[]? as $d
  | {keyword: $r.title, period: $d.period, ratio: $d.ratio}
'
