#!/usr/bin/env bash
# Local code lookup. No API call. Reads reference/codes.json.
#
# Usage:
#   codes.sh categories                  # 부류 (식량/채소/특용/과일/축산/수산)
#   codes.sh items [--category <code>]   # 품목 (filtered if --category given)
#   codes.sh countries                   # 시도 (1101 서울, 2300 대전, ...)
#   codes.sh ranks                       # 등급 (04 상품, 05 중품)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA="${SCRIPT_DIR}/../reference/codes.json"

[[ -f "$DATA" ]] || { echo "missing reference/codes.json" >&2; exit 1; }
command -v jq >/dev/null || { echo "jq required" >&2; exit 1; }

mode="${1:-}"
shift || true

case "$mode" in
  categories)
    jq '.categories' "$DATA";;
  items)
    cat_filter=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --category) cat_filter="$2"; shift 2;;
        *) shift;;
      esac
    done
    if [[ -n "$cat_filter" ]]; then
      jq --arg c "$cat_filter" '.items[] | select(.category == $c)' "$DATA"
    else
      jq '.items' "$DATA"
    fi;;
  countries) jq '.countries' "$DATA";;
  ranks) jq '.ranks' "$DATA";;
  ""|-h|--help)
    sed -n '2,9p' "$0"; exit 0;;
  *) echo "unknown mode: $mode" >&2; exit 2;;
esac
