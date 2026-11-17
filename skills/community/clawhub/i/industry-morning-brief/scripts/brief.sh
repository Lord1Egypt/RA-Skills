#!/usr/bin/env bash
# brief.sh — Fetch recent headlines for an industry vertical and emit a
# structured morning brief draft to stdout. Uses public search endpoints and
# openclaw built-in tools. No API key required.
#
# Usage:
#   brief.sh [--industry new-energy|ev|solar|wind|hydrogen|semiconductor|biotech]
#            [--query "free text query"]
#            [--days N]
#            [--count N]
#            [--lang zh|en]
#            [--source bing|baidu|newsnow|yahoo]

set -u

INDUSTRY="new-energy"
QUERY=""
DAYS=1
COUNT=15
LANG="zh"
SOURCE="bing"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --industry) INDUSTRY="$2"; shift 2 ;;
    --query)    QUERY="$2";    shift 2 ;;
    --days)     DAYS="$2";     shift 2 ;;
    --count)    COUNT="$2";    shift 2 ;;
    --lang)     LANG="$2";     shift 2 ;;
    --source)   SOURCE="$2";   shift 2 ;;
    -h|--help)
      sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "unknown arg: $1"; exit 2 ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REFS="$SCRIPT_DIR/../references/sources.md"

# ---- Resolve query --------------------------------------------------------
if [[ -z "$QUERY" ]]; then
  case "$INDUSTRY" in
    new-energy)   QUERY="new energy renewable solar wind battery EV 2026" ;;
    ev)           QUERY="electric vehicle EV battery gigafactory 2026" ;;
    solar)        QUERY="solar photovoltaic module panel polysilicon 2026" ;;
    wind)         QUERY="offshore wind turbine capacity auction 2026" ;;
    hydrogen)     QUERY="green hydrogen electrolyzer refueling 2026" ;;
    semiconductor) QUERY="semiconductor fab chip manufacturing export 2026" ;;
    biotech)      QUERY="biotech clinical trial FDA approval 2026" ;;
    *)            QUERY="$INDUSTRY news" ;;
  esac
fi

# ---- Date range -----------------------------------------------------------
TODAY=$(date -u +%Y-%m-%d)
SINCE=$(date -u -d "$DAYS days ago" +%Y-%m-%d)

# ---- Pull headlines -------------------------------------------------------
echo "# $INDUSTRY Morning Brief — $TODAY"
echo ""
echo "_Query: \`$QUERY\` — window: $SINCE → $TODAY (source: $SOURCE)"
echo ""

fetch_bing_news() {
  # Bing News search (HTML scraped, minimal parsing)
  local q
  q=$(printf '%s' "$QUERY" | tr ' ' '+')
  local url="https://www.bing.com/news/search?q=${q}&qft=interval=%22${DAYS}d%22&FORM=NWSARP"
  curl -sSL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" "$url" \
    | grep -oE 'class="caption"[^>]*>[^<]*</div>|href="https://[^"]+"' \
    | sed 's/^href="//;s/"$//' \
    | grep -E '^https://' \
    | head -n "$COUNT"
}

# Collect URLs into a tempfile for downstream synthesis
URLS_FILE=$(mktemp)
trap 'rm -f "$URLS_FILE"' EXIT

case "$SOURCE" in
  bing)   fetch_bing_news >> "$URLS_FILE" ;;
  *)      fetch_bing_news >> "$URLS_FILE" ;;
esac

# ---- Draft structured sections -------------------------------------------
# The raw fetch is a starting point. The agent is expected to synthesize the
# final Markdown using the Sources list below.
echo "## 1. 重点新闻 / Headlines"
echo "- _Inspect the sources below and pick 3–5 top stories._"
echo ""
echo "## 2. 政策与监管 / Policy & Regulation"
echo "- _Identify any regulatory, subsidy, or tariff moves._"
echo ""
echo "## 3. 产业链动向 / Supply-Chain & Companies"
echo "- _M&A, partnerships, capacity, supply deals._"
echo ""
echo "## 4. 潜在影响 / Potential Impact"
echo "- _What could change for the industry?_ "
echo ""
echo "## 5. 需跟踪事项 / Items to Track"
echo "- _Upcoming catalysts: launches, deadlines, talks._"
echo ""
echo "---"
echo "Sources:"

if [[ -s "$URLS_FILE" ]]; then
  while read -r u; do
    [[ -n "$u" ]] && echo "- $u"
  done < "$URLS_FILE"
else
  echo "- _No URLs returned — try a different --source or --query._"
fi

echo ""
echo "_Draft. Synthesize and deduplicate before publishing._"
