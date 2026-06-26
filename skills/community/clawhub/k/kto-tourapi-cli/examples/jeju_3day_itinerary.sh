#!/usr/bin/env bash
# Build a rough 3-day Jeju itinerary using TourAPI:
#   - Day 1: 관광지 in 제주시 (sigunguCode=4 under areaCode=39)
#   - Day 2: 레포츠 across Jeju
#   - Day 3: 음식점 within 1 km of 성산일출봉 (mapx/mapy from a quick search)
#
# Output: JSONL — schema {day, kind, title, addr1, mapx, mapy, firstimage}.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
S="$here/../scripts"

bash "$S/area.sh" --area-code 39 --sigungu-code 4 --content-type-id 12 --num 6 \
  | jq -c '{day:1, kind:"sight", title, addr1, mapx, mapy, firstimage}'

bash "$S/area.sh" --area-code 39 --content-type-id 28 --num 6 \
  | jq -c '{day:2, kind:"activity", title, addr1, mapx, mapy, firstimage}'

# Anchor on 성산일출봉 → take its mapx/mapy → nearby 음식점.
seongsan=$(bash "$S/search.sh" --keyword 성산일출봉 --content-type-id 12 --num 1)
lng=$(echo "$seongsan" | jq -r '.mapx')
lat=$(echo "$seongsan" | jq -r '.mapy')
bash "$S/nearby.sh" --lng "$lng" --lat "$lat" --radius 1000 --content-type-id 39 --num 6 \
  | jq -c '{day:3, kind:"food", title, addr1, mapx, mapy, firstimage}'
