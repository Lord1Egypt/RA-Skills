#!/usr/bin/env bash
# area.sh — KorService2/areaBasedList2: 지역기반 관광정보 조회.
#
# Browse points-of-interest by area / sigungu / contentType / category.
#
# Usage:
#   area.sh [--area-code 1] [--sigungu-code 24] [--content-type-id 12] \
#           [--cat1 A01] [--cat2 A0101] [--cat3 A01010100] \
#           [--arrange A] [--num 20] [--page 1]
#
# arrange: A=제목순 C=수정일순 D=생성일순 O=제목순(이미지必) Q=수정일순(이미지必) R=생성일순(이미지必)
# contentTypeId: 12 14 15 25 28 32 38 39
#
# Output: JSONL — one row per content item.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

area_code="" sigungu="" cti="" cat1="" cat2="" cat3=""
arrange="A" num="20" page="1"

while [[ $# -gt 0 ]]; do
  case "$1" in
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
      sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "error: unknown flag '$1'" >&2; exit 64;;
  esac
done

[[ -n "$cti" ]] && valid_content_type "$cti"

require_bin curl jq

resp=$(tourapi_get "areaBasedList2" \
  "areaCode=$area_code" "sigunguCode=$sigungu" "contentTypeId=$cti" \
  "cat1=$cat1" "cat2=$cat2" "cat3=$cat3" \
  "arrange=$arrange" "numOfRows=$num" "pageNo=$page")
echo "$resp" | emit_items
