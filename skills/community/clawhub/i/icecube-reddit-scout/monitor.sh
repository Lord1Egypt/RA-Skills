#!/bin/bash
# IceCube Reddit Scout - Basic Monitor
# Usage: ./monitor.sh [keyword] [subreddit] [limit]

KEYWORD="${1:-openclaw}"
SUBREDDIT="${2:-indiehackers}"
LIMIT="${3:-10}"

WORKSPACE="$HOME/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory/reddit-mentions"
TODAY_FILE="$MEMORY_DIR/$(date +%Y-%m-%d).md"

# Create memory dir if not exists
mkdir -p "$MEMORY_DIR"

# Fetch Reddit search results (anonymous API)
URL="https://www.reddit.com/r/${SUBREDDIT}/search.json?q=${KEYWORD}&sort=new&limit=${LIMIT}"

echo "🔍 Searching r/${SUBREDDIT} for: ${KEYWORD}"

# Fetch and parse
RESPONSE=$(curl -s -A "IceCube-Reddit-Scout/1.0" "$URL")

if [ -z "$RESPONSE" ]; then
    echo "❌ No response from Reddit (rate limited or network error)"
    exit 1
fi

# Extract posts using jq (if available)
if command -v jq &> /dev/null; then
    COUNT=$(echo "$RESPONSE" | jq '.data.children | length')
    
    echo "Found $COUNT results"
    
    # Write to memory file
    echo "" >> "$TODAY_FILE"
    echo "## Reddit Scout Check ($(date +%H:%M))" >> "$TODAY_FILE"
    echo "- Keyword: ${KEYWORD}" >> "$TODAY_FILE"
    echo "- Subreddit: r/${SUBREDDIT}" >> "$TODAY_FILE"
    echo "- Results: $COUNT" >> "$TODAY_FILE"
    
    # Extract each post
    echo "$RESPONSE" | jq -r '.data.children[] | 
        "- Thread: [\(.data.title)](https://reddit.com/r/${SUBREDDIT}/comments/\(.data.id))\n  Score: \(.data.score) | Author: \(.data.author)"' >> "$TODAY_FILE"
else
    echo "⚠️ jq not installed - raw output:"
    echo "$RESPONSE" | head -100
fi

echo ""
echo "📝 Logged to: $TODAY_FILE"