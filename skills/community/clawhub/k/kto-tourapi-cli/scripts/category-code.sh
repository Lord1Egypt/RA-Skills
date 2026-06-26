#!/usr/bin/env bash
# category-code.sh — KorService2/categoryCode2: 서비스분류코드 조회.
#
# Drill into the 3-level KTO category tree (cat1 → cat2 → cat3).
# Pass none → top-level cat1 list. Pass --cat1 A01 → cat2 under it. Etc.
#
# Usage:
#   category-code.sh [--cat1 A01] [--cat2 A0101] [--cat3 A01010100] \
#                    [--content-type-id 12] [--num 100] [--page 1]
#
# Output: JSONL — {code, name, rnum} rows.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

cat1="" cat2="" cat3="" cti="" num="100" page="1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --cat1)             cat1="$2"; shift 2;;
    --cat2)             cat2="$2"; shift 2;;
    --cat3)             cat3="$2"; shift 2;;
    --content-type-id)  cti="$2";  shift 2;;
    --num)              num="$2";  shift 2;;
    --page)             page="$2"; shift 2;;
    -h|--help)
      sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "error: unknown flag '$1'" >&2; exit 64;;
  esac
done

[[ -n "$cti" ]] && valid_content_type "$cti"

require_bin curl jq

resp=$(tourapi_get "categoryCode2" \
  "cat1=$cat1" "cat2=$cat2" "cat3=$cat3" \
  "contentTypeId=$cti" "numOfRows=$num" "pageNo=$page")
echo "$resp" | emit_items
