#!/bin/bash
# Code context search via SkillBoss API Hub

QUERY="$1"
NUM_RESULTS="${2:-10}"

if [ -z "$QUERY" ]; then
    echo "Usage: $0 \"query\" [num_results]" >&2
    exit 1
fi

if [ -z "${SKILLBOSS_API_KEY:-}" ]; then
    echo "Error: SKILLBOSS_API_KEY is not set." >&2
    echo "Please set SKILLBOSS_API_KEY environment variable." >&2
    exit 1
fi

# Optimized settings for code/docs
PAYLOAD=$(jq -n \
    --arg query "$QUERY" \
    --argjson numResults "$NUM_RESULTS" \
    '{
        type: "search",
        inputs: {
            query: $query,
            type: "auto",
            numResults: $numResults,
            text: true,
            highlights: true
        },
        prefer: "balanced"
    }')

curl -s -X POST 'https://api.heybossai.com/v1/pilot' \
    -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
    -H 'Content-Type: application/json' \
    -d "$PAYLOAD"
