#!/usr/bin/env bash
# nearby.sh — KorService2/locationBasedList2: 위치기반 관광정보 조회.
#
# Find points-of-interest within <radius> meters of (lng, lat).
# Coordinate frame: WGS-84 (decimal degrees).
#
# Usage:
#   nearby.sh --lng 126.9784 --lat 37.5666 [--radius 1000] \
#             [--content-type-id 39] [--arrange E] [--num 20] [--page 1]
#
# radius: meters, max 20000.
# arrange: E=거리순 (default), A/C/D/O/Q/R as in area.sh.
#
# Output: JSONL — one row per content item, each carries dist (meters).
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

lng="" lat="" radius="1000" cti=""
arrange="E" num="20" page="1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --lng)              lng="$2";       shift 2;;
    --lat)              lat="$2";       shift 2;;
    --radius)           radius="$2";    shift 2;;
    --content-type-id)  cti="$2";       shift 2;;
    --arrange)          arrange="$2";   shift 2;;
    --num)              num="$2";       shift 2;;
    --page)             page="$2";      shift 2;;
    -h|--help)
      sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "error: unknown flag '$1'" >&2; exit 64;;
  esac
done

[[ -z "$lng" || -z "$lat" ]] && { echo "error: --lng and --lat are required." >&2; exit 64; }
[[ -n "$cti" ]] && valid_content_type "$cti"

if (( radius > 20000 )); then
  echo "error: --radius max is 20000 (got $radius)." >&2; exit 64
fi

require_bin curl jq

resp=$(tourapi_get "locationBasedList2" \
  "mapX=$lng" "mapY=$lat" "radius=$radius" \
  "contentTypeId=$cti" "arrange=$arrange" \
  "numOfRows=$num" "pageNo=$page")
echo "$resp" | emit_items
