#!/usr/bin/env bash
# 기간별 도매가격 (action=periodProductList).
#
# Required: --start YYYY-MM-DD --end YYYY-MM-DD
#           --category <code> --item <code> --kind <code> --rank <code> --country <code>
# Optional: --kg-convert Y|N (default N)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/_common.sh"

start=""; end=""; category=""; item=""; kind=""; rank=""; country=""; kg="N"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --start) start="$2"; shift 2;;
    --end) end="$2"; shift 2;;
    --category) category="$2"; shift 2;;
    --item) item="$2"; shift 2;;
    --kind) kind="$2"; shift 2;;
    --rank) rank="$2"; shift 2;;
    --country) country="$2"; shift 2;;
    --kg-convert) kg="$2"; shift 2;;
    -h|--help) sed -n '2,9p' "$0"; exit 0;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

for n in start end category item kind rank country; do
  require_arg "$n" "${!n}"
done

kamis_call periodProductList \
  "p_startday=${start}" \
  "p_endday=${end}" \
  "p_itemcategorycode=${category}" \
  "p_itemcode=${item}" \
  "p_kindcode=${kind}" \
  "p_productrankcode=${rank}" \
  "p_countrycode=${country}" \
  "p_convert_kg_yn=${kg}"
