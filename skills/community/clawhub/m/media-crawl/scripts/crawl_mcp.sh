#!/usr/bin/env bash
set -euo pipefail

TOOL="${1:-}"
TARGET_URL="${2:-}"
BASE_URL="${3:-${BIL_CRAWL_URL:-http://127.0.0.1:39002}}"

if [[ -z "$TOOL" || -z "$TARGET_URL" ]]; then
  echo "Usage: $0 <crawl_bilibili|crawl_douyin|crawl_youtube|crawl_zhihu> <target_url> [base_url]" >&2
  exit 2
fi

case "$TOOL" in
  crawl_bilibili|crawl_douyin|crawl_youtube|crawl_zhihu) ;;
  *)
    echo "Unsupported tool: $TOOL (use mcp_tool.sh for bilibili_search/bilibili_uploader/bilibili_popular/bilibili_weekly)" >&2
    exit 2
    ;;
esac

ARGS=$(node -e 'process.stdout.write(JSON.stringify({url: process.argv[1]}))' "$TARGET_URL")
bash "$(dirname "$0")/mcp_tool.sh" "$TOOL" "$ARGS" "$BASE_URL"
