#!/bin/bash
# IceCube Reddit Scout - Basic Monitor

KEYWORD="${1:-openclaw}"
SUBREDDIT="${2:-indiehackers}"
LIMIT="${3:-10}"

WORKSPACE="$HOME/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory/reddit-mentions"
TODAY_FILE="$MEMORY_DIR/$(date +%Y-%m-%d).md"

mkdir -p "$MEMORY_DIR"

URL="https://www.reddit.com/r/${SUBREDDIT}/search.json?q=${KEYWORD}&sort=new&limit=${LIMIT}"

echo "🔍 Searching r/${SUBREDDIT} for: ${KEYWORD}"

RESPONSE=$(curl -s -A "IceCube-Reddit-Scout/1.0" "$URL")

if [ -z "$RESPONSE" ]; then
    echo "❌ No response"
    exit 1
fi

if command -v jq &> /dev/null; then
    COUNT=$(echo "$RESPONSE" | jq '.data.children | length')
    echo "Found $COUNT results"
    
    echo "" >> "$TODAY_FILE"
    echo "## Reddit Scout ($(date +%H:%M)) - r/${SUBREDDIT}: ${KEYWORD}" >> "$TODAY_FILE"
    
    echo "$RESPONSE" | jq -r '.data.children[] | 
        "- [\(.data.title)](https://reddit.com/r/indiehackers/comments/\(.data.id)) (score: \(.data.score))"' >> "$TODAY_FILE"
    
    echo "📝 Logged to: $TODAY_FILE"
else
    echo "⚠️ jq not installed"
fi