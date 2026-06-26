#!/usr/bin/env bash
# 최근 가격 동향 간이조회 (action=recentlyPriceTrendList).
#
# Required: --product <productno>   (e.g. 111 = 쌀)
# Optional: --date YYYY-MM-DD       (anchor; default = today)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/_common.sh"

product=""; date_arg="$(date +%F)"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --product) product="$2"; shift 2;;
    --date) date_arg="$2"; shift 2;;
    -h|--help) sed -n '2,5p' "$0"; exit 0;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

require_arg product "$product"

kamis_call recentlyPriceTrendList \
  "p_productno=${product}" \
  "p_regday=${date_arg}"
