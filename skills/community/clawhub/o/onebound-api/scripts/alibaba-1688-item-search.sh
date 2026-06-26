#!/bin/bash
# Usage: alibaba-1688-item-search.sh <keyword> [page] [page_size] [sort] [cat]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KEYWORD="${1:?Error: keyword is required}"
PAGE="${2:-1}"
PAGE_SIZE="${3:-40}"
SORT="${4:-}"
CAT="${5:-0}"

bash "${SCRIPT_DIR}/gateway-request.sh" \
  "/v1/1688/item-search" \
  "1688关键词搜索结果" \
  "q=${KEYWORD}" \
  "page=${PAGE}" \
  "page_size=${PAGE_SIZE}" \
  "sort=${SORT}" \
  "cat=${CAT}"
