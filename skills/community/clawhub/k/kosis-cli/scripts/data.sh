#!/usr/bin/env bash
# Fetch actual data rows from a KOSIS table.
# Wraps statisticsParameterData.do?method=getList.
#
# Usage: data.sh <orgId> <tblId> [options]
#
# Options:
#   --prd-se M|Q|Y|H|IR     period unit (required for time-series tables)
#   --recent N              shorthand for newEstPrdCnt=N (latest N periods)
#   --from YYYY[MM|Q|H]     start period (paired with --to)
#   --to   YYYY[MM|Q|H]     end period
#   --itm "A B C"           space- or +-separated itmId list (passed as +-joined)
#   --obj-l1 "A B"          objL1 codes — same convention; "ALL" passes through
#   --obj-l2 …  …  --obj-l8
#   --page N                pIndex (default 1)
#   --per-page N            pSize (default 10000, KOSIS hard cap)
#
# Output: JSONL — one row per line.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$HERE/_common.sh"
require_bin curl jq
require_key

if [[ $# -lt 2 ]]; then
  echo "usage: data.sh <orgId> <tblId> [options]" >&2
  exit 64
fi

org_id="$1"; tbl_id="$2"; shift 2

prd_se=""
recent=""
prd_from=""
prd_to=""
itm=""
obj_l1=""; obj_l2=""; obj_l3=""; obj_l4=""
obj_l5=""; obj_l6=""; obj_l7=""; obj_l8=""
page=1
per_page=10000

# Joins a space/comma-separated list into KOSIS '+'-separated form (passes ALL through).
join_plus() {
  local v="$1"
  if [[ "$v" == "ALL" ]]; then
    printf 'ALL'
    return
  fi
  printf '%s' "$v" | tr ', ' '++' | tr -s '+'
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prd-se)   prd_se="$2"; shift 2 ;;
    --recent)   recent="$2"; shift 2 ;;
    --from)     prd_from="$2"; shift 2 ;;
    --to)       prd_to="$2"; shift 2 ;;
    --itm)      itm="$2"; shift 2 ;;
    --obj-l1)   obj_l1="$2"; shift 2 ;;
    --obj-l2)   obj_l2="$2"; shift 2 ;;
    --obj-l3)   obj_l3="$2"; shift 2 ;;
    --obj-l4)   obj_l4="$2"; shift 2 ;;
    --obj-l5)   obj_l5="$2"; shift 2 ;;
    --obj-l6)   obj_l6="$2"; shift 2 ;;
    --obj-l7)   obj_l7="$2"; shift 2 ;;
    --obj-l8)   obj_l8="$2"; shift 2 ;;
    --page)     page="$2"; shift 2 ;;
    --per-page) per_page="$2"; shift 2 ;;
    *) echo "error: unknown arg '$1'" >&2; exit 64 ;;
  esac
done

qs="method=getList"
qs+="&apiKey=$(urlencode "$KOSIS_API_KEY")"
qs+="&orgId=$(urlencode "$org_id")"
qs+="&tblId=$(urlencode "$tbl_id")"
[[ -n "$prd_se"   ]] && qs+="&prdSe=$(urlencode "$prd_se")"
[[ -n "$recent"   ]] && qs+="&newEstPrdCnt=$(urlencode "$recent")"
[[ -n "$prd_from" ]] && qs+="&startPrdDe=$(urlencode "$prd_from")"
[[ -n "$prd_to"   ]] && qs+="&endPrdDe=$(urlencode "$prd_to")"
[[ -n "$itm"      ]] && qs+="&itmId=$(urlencode "$(join_plus "$itm")")"
for k in 1 2 3 4 5 6 7 8; do
  varname="obj_l${k}"
  v="${!varname:-}"
  [[ -n "$v" ]] && qs+="&objL${k}=$(urlencode "$(join_plus "$v")")"
done
qs+="&pIndex=$page"
qs+="&pSize=$per_page"
qs+="&format=json&jsonVD=Y&version=v2_1"

kosis_get "statisticsData.do" "$qs" | emit_jsonl
