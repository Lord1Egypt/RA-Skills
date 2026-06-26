#!/usr/bin/env bash
# Browse the KOSIS statistics catalog tree. Wraps statisticsList.do.
#
# Usage: list.sh [--vw-cd CODE] [--parent ID]
#
# vwCd values: MT_ZTITLE (default, 주제별), MT_OTITLE (기관별),
#              MT_CHITLE (대상별), MT_GTITLE01 (e-지방 주제), MT_GTITLE02 (e-지방 지역).
# parent: parentListId — pass to drill into a sub-tree (omit for the top level).
#
# Output: JSONL — one node per line. Each node has LIST_ID/LIST_NM/STAT_TYPE/etc.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$HERE/_common.sh"
require_bin curl jq
require_key

vw_cd="MT_ZTITLE"
parent=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --vw-cd)  vw_cd="$2"; shift 2 ;;
    --parent) parent="$2"; shift 2 ;;
    *) echo "error: unknown arg '$1'" >&2; exit 64 ;;
  esac
done

qs="method=getList"
qs+="&apiKey=$(urlencode "$KOSIS_API_KEY")"
qs+="&vwCd=$(urlencode "$vw_cd")"
[[ -n "$parent" ]] && qs+="&parentListId=$(urlencode "$parent")"
qs+="&format=json&jsonVD=Y&version=v2_1"

kosis_get "statisticsList.do" "$qs" | emit_jsonl
