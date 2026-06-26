#!/usr/bin/env bash
# yearly-search.sh — compare "전기차" vs "하이브리드" vs "내연기관" monthly through 2024.
# Requires NAVER_CLIENT_ID / NAVER_CLIENT_SECRET in env.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$here/../scripts/search.sh" \
  --start 2024-01-01 --end 2024-12-31 --time-unit month \
  --group "전기차:전기차,EV" \
  --group "하이브리드:하이브리드,HEV" \
  --group "내연기관:내연기관,휘발유,경유"
