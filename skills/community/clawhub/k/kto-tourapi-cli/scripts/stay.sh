#!/usr/bin/env bash
# stay.sh — KorService2/searchStay2: 숙박정보 조회.
#
# Browse Korean lodgings (hotels, motels, pensions, hanok stays, etc.).
# All entries are contentTypeId=32 by default (the API enforces it).
#
# Usage:
#   stay.sh [--area-code 32] [--sigungu-code 1] \
#           [--arrange A] [--num 20] [--page 1]
#
# Output: JSONL — one row per stay with title, addr1, mapx, mapy, image fields.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

area_code="" sigungu=""
arrange="A" num="20" page="1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --area-code)        area_code="$2"; shift 2;;
    --sigungu-code)     sigungu="$2";   shift 2;;
    --arrange)          arrange="$2";   shift 2;;
    --num)              num="$2";       shift 2;;
    --page)             page="$2";      shift 2;;
    -h|--help)
      sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "error: unknown flag '$1'" >&2; exit 64;;
  esac
done

require_bin curl jq

resp=$(tourapi_get "searchStay2" \
  "areaCode=$area_code" "sigunguCode=$sigungu" \
  "arrange=$arrange" "numOfRows=$num" "pageNo=$page")
echo "$resp" | emit_items
