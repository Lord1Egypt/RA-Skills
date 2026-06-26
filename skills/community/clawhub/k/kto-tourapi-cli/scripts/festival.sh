#!/usr/bin/env bash
# festival.sh — KorService2/searchFestival2: 행사정보 조회.
#
# List festivals/events whose period overlaps a given date window.
#
# Usage:
#   festival.sh --start YYYYMMDD [--end YYYYMMDD] [--area-code 1] \
#               [--sigungu-code 24] [--arrange A] [--num 20] [--page 1]
#
# - --start eventStartDate (lower bound; festivals starting on/after this).
# - --end   eventEndDate   (optional; festivals ending on/before this).
#
# Output: JSONL — one row per festival with eventstartdate / eventenddate.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

start="" end="" area_code="" sigungu=""
arrange="A" num="20" page="1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --start)            start="$2";     shift 2;;
    --end)              end="$2";       shift 2;;
    --area-code)        area_code="$2"; shift 2;;
    --sigungu-code)     sigungu="$2";   shift 2;;
    --arrange)          arrange="$2";   shift 2;;
    --num)              num="$2";       shift 2;;
    --page)             page="$2";      shift 2;;
    -h|--help)
      sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "error: unknown flag '$1'" >&2; exit 64;;
  esac
done

[[ -z "$start" ]] && { echo "error: --start (YYYYMMDD) is required." >&2; exit 64; }
valid_yyyymmdd "$start"
[[ -n "$end" ]] && valid_yyyymmdd "$end"

require_bin curl jq

resp=$(tourapi_get "searchFestival2" \
  "eventStartDate=$start" "eventEndDate=$end" \
  "areaCode=$area_code" "sigunguCode=$sigungu" \
  "arrange=$arrange" "numOfRows=$num" "pageNo=$page")
echo "$resp" | emit_items
