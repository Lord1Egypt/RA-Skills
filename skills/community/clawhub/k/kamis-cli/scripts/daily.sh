#!/usr/bin/env bash
# 일일 부류별 도/소매가격 (action=dailyPriceByCategoryList).
#
# Required: --category <100|200|300|400|500|600>
# Optional: --cls <01|02> (01=retail, 02=wholesale; default 01)
#           --date YYYY-MM-DD (default: today)
#           --country <code> (e.g. 1101=서울. omit for all)
#           --kg-convert Y|N (default N)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_common.sh
source "${SCRIPT_DIR}/_common.sh"

cls="01"
category=""
date_arg="$(date +%F)"
country=""
kg="N"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --cls) cls="$2"; shift 2;;
    --category) category="$2"; shift 2;;
    --date) date_arg="$2"; shift 2;;
    --country) country="$2"; shift 2;;
    --kg-convert) kg="$2"; shift 2;;
    -h|--help)
      sed -n '2,11p' "$0"
      exit 0;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

require_arg category "$category"

args=(
  "p_product_cls_code=${cls}"
  "p_regday=${date_arg}"
  "p_convert_kg_yn=${kg}"
  "p_item_category_code=${category}"
)
[[ -n "$country" ]] && args+=("p_country_code=${country}")

kamis_call dailyPriceByCategoryList "${args[@]}"
