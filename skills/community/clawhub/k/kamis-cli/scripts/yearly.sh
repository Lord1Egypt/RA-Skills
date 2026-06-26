#!/usr/bin/env bash
# 연도별 평균 가격 (action=yearlySalesList).
#
# Required: --year YYYY --category <code>
# Optional: --item <code> --kind <code>
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/_common.sh"

year=""; category=""; item=""; kind=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --year) year="$2"; shift 2;;
    --category) category="$2"; shift 2;;
    --item) item="$2"; shift 2;;
    --kind) kind="$2"; shift 2;;
    -h|--help) sed -n '2,5p' "$0"; exit 0;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

require_arg year "$year"
require_arg category "$category"

args=("p_yyyy=${year}" "p_itemcategorycode=${category}")
[[ -n "$item" ]] && args+=("p_itemcode=${item}")
[[ -n "$kind" ]] && args+=("p_kindcode=${kind}")

kamis_call yearlySalesList "${args[@]}"
