#!/usr/bin/env bash
# Bulk-fetch a user-saved KOSIS slice. Wraps statisticsBigData.do?method=getList.
#
# A 'userStatsId' is created on kosis.kr by saving a query inside OpenAPI 활용신청 UI;
# the bulk endpoint returns up to 100,000 rows per call against that saved slice.
#
# Usage: bulk.sh <userStatsId> [--recent N] [--from YYYY..] [--to YYYY..] [--page N] [--per-page N]
#
# Output: JSONL — one row per line.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$HERE/_common.sh"
require_bin curl jq
require_key

if [[ $# -lt 1 ]]; then
  echo "usage: bulk.sh <userStatsId> [--recent N] [--from YYYY..] [--to YYYY..] [--page N] [--per-page N]" >&2
  exit 64
fi

user_stats_id="$1"; shift
recent=""
prd_from=""
prd_to=""
page=1
per_page=100000

while [[ $# -gt 0 ]]; do
  case "$1" in
    --recent)   recent="$2"; shift 2 ;;
    --from)     prd_from="$2"; shift 2 ;;
    --to)       prd_to="$2"; shift 2 ;;
    --page)     page="$2"; shift 2 ;;
    --per-page) per_page="$2"; shift 2 ;;
    *) echo "error: unknown arg '$1'" >&2; exit 64 ;;
  esac
done

qs="method=getList"
qs+="&apiKey=$(urlencode "$KOSIS_API_KEY")"
qs+="&userStatsId=$(urlencode "$user_stats_id")"
[[ -n "$recent"   ]] && qs+="&newEstPrdCnt=$(urlencode "$recent")"
[[ -n "$prd_from" ]] && qs+="&startPrdDe=$(urlencode "$prd_from")"
[[ -n "$prd_to"   ]] && qs+="&endPrdDe=$(urlencode "$prd_to")"
qs+="&pIndex=$page"
qs+="&pSize=$per_page"
qs+="&format=json&jsonVD=Y&version=v2_1"

kosis_get "statisticsBigData.do" "$qs" | emit_jsonl
