#!/usr/bin/env bash
# Compare KAMIS 도매가 trend with BOK ECOS CPI-Food.
#
# Pairs kamis-cli + bank-of-korea-ecos-cli (assumes both installed). Demonstrates
# that wholesale agri prices are the leading indicator that consumer-CPI follows
# 1-2 months later — useful for inflation reporters & macro analysts.
#
# Usage: ./cpi-vs-wholesale.sh <item-code>
# Example: ./cpi-vs-wholesale.sh 211   # 양파
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ITEM="${1:-211}"

YEAR=$(date +%Y)
LAST_YEAR=$((YEAR - 1))

echo "# 양파(${ITEM}) — 도매가 vs 식료품 CPI"
echo

# 1) KAMIS monthly wholesale, last 2 years.
echo "## KAMIS 월별 도매 평균"
"${SKILL_DIR}/scripts/monthly.sh" --year "${YEAR}" --period "${LAST_YEAR},${YEAR}" --category 200 --item "${ITEM}" --kind 01 \
  | jq -r '.data[] | select(.item_name) | "\(.yyyymm): \(.price)원"' 2>/dev/null || echo "(API key needed for monthly endpoint)"

echo
echo "## BOK ECOS — 식료품·비주류음료 CPI (요청예시)"
echo "  bank-of-korea-ecos-cli/scripts/series.sh --series 901Y009 --item E11 --start ${LAST_YEAR}01 --end ${YEAR}12"
echo
echo "_도매가 변화는 통상 1-2개월 시차로 CPI에 전이됨._"
