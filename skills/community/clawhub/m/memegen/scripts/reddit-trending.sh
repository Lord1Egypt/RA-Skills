#!/usr/bin/env bash
# Reddit OAuth: Fetch trending meme templates from r/MemeTemplates
#
# Required env vars:
#   REDDIT_CLIENT_ID      - from reddit.com/prefs/apps (script type)
#   REDDIT_CLIENT_SECRET   - from reddit.com/prefs/apps
#   REDDIT_USERNAME        - your Reddit account
#   REDDIT_PASSWORD        - your Reddit password
#
# Usage: ./reddit-trending.sh [limit]
# Output: JSON array of {title, url, score, created_utc}

set -euo pipefail

LIMIT="${1:-20}"

# Validate env vars
for var in REDDIT_CLIENT_ID REDDIT_CLIENT_SECRET REDDIT_USERNAME REDDIT_PASSWORD; do
  if [ -z "${!var:-}" ]; then
    echo "Error: $var is not set" >&2
    exit 1
  fi
done

# Step 1: Get OAuth access token
TOKEN_RESPONSE=$(curl -s -X POST \
  -d "grant_type=password&username=${REDDIT_USERNAME}&password=${REDDIT_PASSWORD}" \
  --user "${REDDIT_CLIENT_ID}:${REDDIT_CLIENT_SECRET}" \
  -H "User-Agent: MemeBot/1.0" \
  "https://www.reddit.com/api/v1/access_token")

ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)

if [ -z "$ACCESS_TOKEN" ] || [ "$ACCESS_TOKEN" = "null" ]; then
  echo "Error: Failed to get access token. Response: $TOKEN_RESPONSE" >&2
  exit 1
fi

# Step 2: Fetch trending templates from r/MemeTemplates
POSTS=$(curl -s \
  -H "Authorization: bearer ${ACCESS_TOKEN}" \
  -H "User-Agent: MemeBot/1.0" \
  "https://oauth.reddit.com/r/MemeTemplates/hot?limit=${LIMIT}")

# Step 3: Extract image posts and output JSON
echo "$POSTS" | python3 -c "
import sys, json

data = json.load(sys.stdin)
results = []
for child in data['data']['children']:
    post = child['data']
    url = post.get('url', '')
    # Only include direct image URLs
    if url.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
        results.append({
            'title': post['title'],
            'url': url,
            'score': post['score'],
            'created_utc': int(post['created_utc'])
        })

print(json.dumps(results, indent=2))
"
