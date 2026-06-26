#!/usr/bin/env bash
# Fetch metadata for a KOSIS table. Wraps statisticsParameterData.do?method=getMeta.
#
# Usage: meta.sh <orgId> <tblId> [--type TYPE]
#
# TYPE values:
#   ITM   — classification items (measure list: 총인구, 남자, …)
#   OBJ   — object dimensions (region, age, sex, …)
#   PRD   — period information (available period range / unit)
#   ALL   — all of the above (default)
#
# Output: JSONL — one metadata row per line.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$HERE/_common.sh"
require_bin curl jq
require_key

if [[ $# -lt 2 ]]; then
  echo "usage: meta.sh <orgId> <tblId> [--type ITM|OBJ|PRD|ALL]" >&2
  exit 64
fi

org_id="$1"; tbl_id="$2"; shift 2
type="ALL"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --type) type="$2"; shift 2 ;;
    *) echo "error: unknown arg '$1'" >&2; exit 64 ;;
  esac
done

qs="method=getMeta"
qs+="&apiKey=$(urlencode "$KOSIS_API_KEY")"
qs+="&orgId=$(urlencode "$org_id")"
qs+="&tblId=$(urlencode "$tbl_id")"
qs+="&type=$(urlencode "$type")"
qs+="&format=json&jsonVD=Y&version=v2_1"

kosis_get "statisticsData.do" "$qs" | emit_jsonl
