#!/bin/bash
# fetch-articles.sh — Fetch articles from Google News RSS or local file
# Usage:
#   fetch-articles.sh <domain_query>                    # live fetch from Google News RSS
#   fetch-articles.sh --from-file <rss.xml> <domain>    # parse local RSS file (for testing)
#   fetch-articles.sh --list-domains <domains.md>       # list domains from config file
# Output: One JSON object per line (JSONL) to stdout
set -euo pipefail

# --- Parse domains from config file ---
list_domains() {
  local config="$1"
  grep -E '^[[:space:]]*-[[:space:]]+' "$config" | sed 's/^[[:space:]]*-[[:space:]]*//' | sed 's/[[:space:]]*$//'
}

# --- Parse RSS XML into JSONL ---
parse_rss_to_jsonl() {
  local rss_content="$1"
  local domain="$2"
  local today
  today=$(date +%Y-%m-%d)

  # Pure awk-based RSS parsing (no xmllint dependency)
  echo "$rss_content" | awk -v domain="$domain" -v today="$today" '
    BEGIN { RS="</item>"; FS="\n" }
    {
      title=""; link=""; pubDate=""; desc=""; src=""
      for (i=1; i<=NF; i++) {
        if ($i ~ /<title>/) { gsub(/.*<title>|<\/title>.*/, "", $i); title=$i }
        if ($i ~ /<link>/) { gsub(/.*<link>|<\/link>.*/, "", $i); link=$i }
        if ($i ~ /<pubDate>/) { gsub(/.*<pubDate>|<\/pubDate>.*/, "", $i); pubDate=$i }
        if ($i ~ /<description>/) { gsub(/.*<description>|<\/description>.*/, "", $i); desc=$i }
        if ($i ~ /<source/) { gsub(/.*<source[^>]*>|<\/source>.*/, "", $i); src=$i }
      }
      if (title != "") {
        gsub(/"/, "\\\"", title)
        gsub(/"/, "\\\"", desc)
        gsub(/"/, "\\\"", src)
        printf "{\"title\":\"%s\",\"url\":\"%s\",\"date\":\"%s\",\"description\":\"%s\",\"source\":\"%s\",\"domain\":\"%s\",\"harvested\":\"%s\"}\n", title, link, pubDate, desc, src, domain, today
      }
    }
  '
}

# --- Main ---
case "${1:-}" in
  --list-domains)
    CONFIG="${2:?Usage: fetch-articles.sh --list-domains <domains.md>}"
    list_domains "$CONFIG"
    ;;
  --from-file)
    RSS_FILE="${2:?Usage: fetch-articles.sh --from-file <rss.xml> <domain>}"
    DOMAIN="${3:?Usage: fetch-articles.sh --from-file <rss.xml> <domain>}"
    RSS_CONTENT=$(cat "$RSS_FILE")
    parse_rss_to_jsonl "$RSS_CONTENT" "$DOMAIN"
    ;;
  *)
    QUERY="${1:?Usage: fetch-articles.sh <domain_query>}"
    ENCODED_QUERY=$(printf '%s' "$QUERY" | jq -sRr @uri 2>/dev/null || printf '%s' "$QUERY" | sed 's/ /+/g')
    RSS_URL="https://news.google.com/rss/search?q=${ENCODED_QUERY}&hl=en&gl=US&ceid=US:en"
    RSS_CONTENT=$(curl -sL --max-time 15 "$RSS_URL" 2>/dev/null || echo "")
    if [ -z "$RSS_CONTENT" ]; then
      echo "ERROR: Failed to fetch RSS from Google News" >&2
      exit 1
    fi
    parse_rss_to_jsonl "$RSS_CONTENT" "$QUERY"
    ;;
esac
