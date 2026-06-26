#!/usr/bin/env bash
set -euo pipefail

PLATFORM="${1:-}"
KEYWORD="${2:-}"
LIMIT="${3:-50}"
BASE_URL="${4:-${BIL_CRAWL_URL:-http://127.0.0.1:39002}}"

ARGS='{}'
if [[ -n "$PLATFORM" || -n "$KEYWORD" || -n "$LIMIT" ]]; then
  ARGS=$(node -e '
const [platform, keyword, limitRaw] = process.argv.slice(1);
const out = {};
if (platform) out.platform = platform;
if (keyword) out.keyword = keyword;
const n = Number(limitRaw);
if (!Number.isNaN(n) && n > 0) out.limit = Math.floor(n);
process.stdout.write(JSON.stringify(out));
' "$PLATFORM" "$KEYWORD" "$LIMIT")
fi

bash "$(dirname "$0")/mcp_tool.sh" list_archives "$ARGS" "$BASE_URL"
