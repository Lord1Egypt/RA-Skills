#!/usr/bin/env bash
# Giphy GIF Search: Find reaction GIFs by keyword
#
# Required env var:
#   GIPHY_API_KEY - free beta key from developers.giphy.com
#
# Usage: ./giphy-search.sh "search query"
# Output: Top 5 GIF URLs, downloads best match to /tmp/meme.gif

set -euo pipefail

QUERY="${1:?Usage: $0 \"search query\"}"

if [ -z "${GIPHY_API_KEY:-}" ]; then
  echo "Error: GIPHY_API_KEY is not set" >&2
  echo "Get a free beta key at https://developers.giphy.com" >&2
  exit 1
fi

# URL-encode the query
ENCODED_QUERY=$(python3 -c "from urllib.parse import quote; print(quote('${QUERY}'))")

# Fetch top 5 results
RESPONSE=$(curl -s "https://api.giphy.com/v1/gifs/search?api_key=${GIPHY_API_KEY}&q=${ENCODED_QUERY}&limit=5&rating=pg-13")

# Extract and display URLs
echo "$RESPONSE" | python3 -c "
import sys, json

data = json.load(sys.stdin)
if 'data' not in data or not data['data']:
    print('No results found', file=sys.stderr)
    sys.exit(1)

gifs = data['data']
print('Top 5 GIF results:')
for i, gif in enumerate(gifs):
    url = gif['images']['original']['url']
    title = gif.get('title', 'Untitled')
    print(f'  {i+1}. {title}')
    print(f'     {url}')

# Output best match URL for download
best_url = gifs[0]['images']['original']['url']
print(f'\nBest match: {best_url}')
print(best_url)
" | tee /dev/stderr | tail -1 | {
  # Download best match
  read -r BEST_URL
  if [ -n "$BEST_URL" ]; then
    curl -sL -o /tmp/meme.gif "$BEST_URL"
    SIZE=$(stat -f%z /tmp/meme.gif 2>/dev/null || stat -c%s /tmp/meme.gif 2>/dev/null)
    echo "Downloaded to /tmp/meme.gif (${SIZE} bytes)" >&2
  fi
}
