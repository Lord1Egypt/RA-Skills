#!/bin/bash
# Web search via SkillBoss API Hub

QUERY="$1"
NUM_RESULTS="${2:-10}"
TYPE="${3:-auto}"
CATEGORY="$4"

# 1. Check for Query
if [ -z "$QUERY" ]; then
    echo "Usage: $0 \"query\" [num_results] [type] [category]" >&2
    exit 1
fi

# 2. Check for API Key
if [ -z "${SKILLBOSS_API_KEY:-}" ]; then
    echo "Error: SKILLBOSS_API_KEY is not set." >&2
    echo "" >&2
    echo "To fix:" >&2
    echo "1. Get a key from SkillBoss API Hub" >&2
    echo "2. Run: export SKILLBOSS_API_KEY=\"your-key\"" >&2
    exit 1
fi

# 3. Build Payload
PAYLOAD=$(jq -n \
    --arg query "$QUERY" \
    --arg type "$TYPE" \
    --argjson numResults "$NUM_RESULTS" \
    '{
        type: "search",
        inputs: {
            query: $query,
            type: $type,
            numResults: $numResults,
            text: true,
            highlights: true,
            summary: true
        },
        prefer: "balanced"
    }')

if [ -n "$CATEGORY" ]; then
    PAYLOAD=$(echo "$PAYLOAD" | jq --arg cat "$CATEGORY" '.inputs.category = $cat')
fi

# 4. Call API
curl -s -X POST 'https://api.heybossai.com/v1/pilot' \
    -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
    -H 'Content-Type: application/json' \
    -d "$PAYLOAD"
