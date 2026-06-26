#!/usr/bin/env bash
# Title-search KOSIS statistics. Wraps statisticsTitle.do.
#
# Usage: search.sh <query> [--page N] [--per-page N]
#
# Output: JSONL — one statistic per line.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$HERE/_common.sh"
require_bin curl jq
require_key

if [[ $# -lt 1 ]]; then
  echo "usage: search.sh <query> [--page N] [--per-page N]" >&2
  exit 64
fi

q="$1"; shift
page=1
per_page=20

while [[ $# -gt 0 ]]; do
  case "$1" in
    --page)     page="$2"; shift 2 ;;
    --per-page) per_page="$2"; shift 2 ;;
    *) echo "error: unknown arg '$1'" >&2; exit 64 ;;
  esac
done

qs="method=getList"
qs+="&apiKey=$(urlencode "$KOSIS_API_KEY")"
qs+="&searchNm=$(urlencode "$q")"
qs+="&pIndex=$page"
qs+="&pSize=$per_page"
qs+="&format=json&jsonVD=Y&version=v2_1"

kosis_get "statisticsSearch.do" "$qs" | emit_jsonl
