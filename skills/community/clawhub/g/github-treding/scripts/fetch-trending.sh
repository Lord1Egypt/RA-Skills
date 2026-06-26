#!/usr/bin/env bash
# Fetch top trending GitHub repos via search API and summarize
# Usage: bash fetch-trending.sh [since-date] [count]

set -euo pipefail

# Cross-platform date: macOS (date -v) vs Linux (date -d)
if date -d '7 days ago' >/dev/null 2>&1; then
  SINCE="${1:-$(date -d '7 days ago' +%Y-%m-%d)}"
else
  SINCE="${1:-$(date -v-7d +%Y-%m-%d)}"
fi
COUNT="${2:-15}"
API="https://api.github.com/search/repositories"

# Optional auth header
AUTH=""
if [ -n "${GH_TOKEN:-}" ]; then
  AUTH="-H \"Authorization: token $GH_TOKEN\""
fi

echo "📈 GitHub Trending — Top $COUNT repos since $SINCE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

curl -sf "$API?q=created:>=$SINCE&sort=stars&order=desc&per_page=$COUNT" \
  $AUTH \
  -H "Accept: application/vnd.github.v3+json" \
  -H "User-Agent: openclaw-trending" \
  | jq -r '.items | to_entries[] | 
    "\(.key+1). \(.value.full_name)
   ⭐ \(.value.stargazers_count)  🍴 \(.value.forks_count)  🔤 \(.value.language // "N/A")
   📝 \(.value.description // "No description" | .[0:120])
   🔗 https://github.com/\(.value.full_name)
"'