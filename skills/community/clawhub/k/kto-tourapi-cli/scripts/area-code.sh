#!/usr/bin/env bash
# area-code.sh — KorService2/areaCode2: 지역코드 조회.
#
# Without --area-code: returns top-level 지역 list (서울, 부산, 인천, ...).
# With    --area-code: returns 시군구 list under that 지역.
#
# Usage:
#   area-code.sh [--area-code 1] [--num 100] [--page 1]
#
# Output: JSONL — one row per area item with fields like {code,name,rnum}.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

area_code="" num="100" page="1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --area-code) area_code="$2"; shift 2;;
    --num)       num="$2";       shift 2;;
    --page)      page="$2";      shift 2;;
    -h|--help)
      sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "error: unknown flag '$1'" >&2; exit 64;;
  esac
done

require_bin curl jq

resp=$(tourapi_get "areaCode2" "areaCode=$area_code" "numOfRows=$num" "pageNo=$page")
echo "$resp" | emit_items
