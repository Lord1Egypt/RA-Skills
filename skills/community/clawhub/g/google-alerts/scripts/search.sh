#!/bin/bash
# Google Alerts Monitor — Keyword Search via Google Alerts RSS
# Fetches Google Alerts for a keyword via RSS — free, no API key required
# Usage: bash search.sh "<keyword>" [count]
# Required: Set GOOGLE_ALERT_FEED_ID env var before running

set -e

TERM="$1"
COUNT="${2:-10}"

if [ -z "$TERM" ]; then
  echo "Usage: search.sh <keyword> [count]"
  exit 1
fi

if [ -z "$GOOGLE_ALERT_FEED_ID" ]; then
  echo "Error: GOOGLE_ALERT_FEED_ID must be set"
  echo "Set it with: export GOOGLE_ALERT_FEED_ID=your_feed_id"
  exit 1
fi

# URL-encode the search term safely via Python (avoids shell injection)
ENCODED_TERM=$(python3 -c "import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1]))" -- "$TERM")

# Fetch Google Alerts RSS (public feed — works without auth)
curl -s -A "Mozilla/5.0 (compatible)" \
  "https://www.google.com/alerts/feeds/${ENCODED_TERM}/${GOOGLE_ALERT_FEED_ID}" \
  -H "Accept: application/rss+xml, application/xml, text/xml" | \
python3 -c "
import sys, re, json, html
from xml.etree import ElementTree as ET

count = int(sys.argv[1]) if len(sys.argv) > 1 else 10
xml = sys.stdin.read()
try:
    root = ET.fromstring(xml)
    items = root.findall('.//item')
    results = []
    for item in items[:count]:
        title = item.findtext('title', '')
        link = item.findtext('link', '')
        desc = item.findtext('description', '')
        pub = item.findtext('pubDate', '')
        desc = re.sub(r'<[^>]+>', '', desc)
        desc = html.unescape(desc) if hasattr(html, 'unescape') else desc
        results.append({
            'title': title.strip(),
            'link': link.strip(),
            'description': desc.strip(),
            'published': pub.strip()
        })
    print(json.dumps(results, indent=2))
except Exception as e:
    print('[]')
" "$COUNT"
