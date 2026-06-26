#!/usr/bin/env bash
# search.sh — KorService2/searchKeyword2: 키워드 검색 조회.
#
# Search KTO content by keyword. Optionally constrain by area/sigungu/contentType.
#
# Usage:
#   search.sh --keyword 강릉 [--area-code 32] [--sigungu-code 1] \
#             [--content-type-id 12] [--cat1 A01] [--cat2 A0101] [--cat3 A01010100] \
#             [--arrange A] [--num 20] [--page 1]
#
# Note: the API expects the keyword UTF-8 encoded; we handle URL encoding.
#
# Output: JSONL — one row per content item.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

keyword="" area_code="" sigungu="" cti="" cat1="" cat2="" cat3=""
arrange="A" num="20" page="1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --keyword)          keyword="$2";   shift 2;;
    --area-code)        area_code="$2"; shift 2;;
    --sigungu-code)     sigungu="$2";   shift 2;;
    --content-type-id)  cti="$2";       shift 2;;
    --cat1)             cat1="$2";      shift 2;;
    --cat2)             cat2="$2";      shift 2;;
    --cat3)             cat3="$2";      shift 2;;
    --arrange)          arrange="$2";   shift 2;;
    --num)              num="$2";       shift 2;;
    --page)             page="$2";      shift 2;;
    -h|--help)
      sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "error: unknown flag '$1'" >&2; exit 64;;
  esac
done

[[ -z "$keyword" ]] && { echo "error: --keyword is required." >&2; exit 64; }
[[ -n "$cti" ]] && valid_content_type "$cti"

require_bin curl jq

resp=$(tourapi_get "searchKeyword2" \
  "keyword=$keyword" \
  "areaCode=$area_code" "sigunguCode=$sigungu" "contentTypeId=$cti" \
  "cat1=$cat1" "cat2=$cat2" "cat3=$cat3" \
  "arrange=$arrange" "numOfRows=$num" "pageNo=$page")
echo "$resp" | emit_items
