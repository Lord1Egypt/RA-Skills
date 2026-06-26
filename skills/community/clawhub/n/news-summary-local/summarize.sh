#!/usr/bin/env bash
set -e
# summarize.sh – 读取 RSS 并输出简洁标题列表
RSS_FILE="${1:-news.rss}"
if [[ ! -f "$RSS_FILE" ]]; then
  echo "RSS file not found: $RSS_FILE"
  exit 1
fi
echo "📰 今日新闻要点（前10条）:"
./extract.sh "$RSS_FILE"
