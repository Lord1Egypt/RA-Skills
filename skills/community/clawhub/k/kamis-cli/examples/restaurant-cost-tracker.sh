#!/usr/bin/env bash
# Restaurant cost tracker — emits a daily Markdown brief for chefs/buyers.
#
# Tracks 양파, 대파, 마늘, 배추, 무, 돼지고기, 닭고기, 달걀 — pulls today's 도매가
# alongside 1-week-ago and 1-month-ago, computes % deltas, and flags anything
# moving >5% week-over-week as a 🔥 alert.
#
# Pairs naturally with cron + telegram/slack hooks.
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

categories=("100" "200" "200" "200" "200" "200" "500" "500" "500")
labels=("쌀(20kg)" "양파(상품)" "대파(상품)" "마늘(깐마늘)" "배추(상품)" "무(상품)" "돼지고기(삼겹)" "닭고기(육계)" "달걀(특란)")

today=$(date +%F)
echo "# 🍳 식자재 도매가 일일 브리핑 — ${today}"
echo
echo "| 품목 | 오늘 | 1주전 | 1달전 | WoW |"
echo "|---|---:|---:|---:|---:|"

# Single API call per 부류 — collect everything in one shot.
declare -A seen
for cat in "100" "200" "500"; do
  json=$("${SKILL_DIR}/scripts/daily.sh" --cls 02 --category "${cat}" --date "${today}" 2>/dev/null || echo "{}")
  echo "$json" | jq -r '
    .data.item // [] |
    map(select(.kind_code != null)) |
    .[] |
    (.dpr1|gsub(",";"")|tonumber? // 0) as $today |
    (.dpr3|gsub(",";"")|tonumber? // 0) as $week |
    (.dpr5|gsub(",";"")|tonumber? // 0) as $month |
    (if $week > 0 then (($today - $week) / $week * 100) else 0 end) as $wow |
    "\(.item_name) (\(.kind_name))|\(.dpr1)|\(.dpr3)|\(.dpr5)|\($wow|.*100|round/100)%"
  ' 2>/dev/null | while IFS='|' read -r name today_p week_p month_p wow; do
    flag=""
    case "$wow" in
      *-*[0-9]*\%) [[ "${wow//[^0-9.-]/}" =~ ^-?[0-9]+\.?[0-9]*$ ]] && awk "BEGIN{exit !(${wow%\%} >= 5 || ${wow%\%} <= -5)}" 2>/dev/null && flag=" 🔥";;
    esac
    echo "| $name | ${today_p} | ${week_p} | ${month_p} | ${wow}${flag} |"
  done
done

echo
echo "_데이터: KAMIS (kamis.or.kr) • 단가는 조사 시점의 도매가격_"
