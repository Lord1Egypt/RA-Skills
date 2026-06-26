#!/bin/bash
# Get content from URLs via SkillBoss API Hub

if [ $# -eq 0 ]; then
    echo "Usage: $0 url1 [url2 ...]" >&2
    exit 1
fi

if [ -z "${SKILLBOSS_API_KEY:-}" ]; then
    echo "Error: SKILLBOSS_API_KEY is not set." >&2
    echo "Please set SKILLBOSS_API_KEY environment variable." >&2
    exit 1
fi

for URL in "$@"; do
    PAYLOAD=$(jq -n \
        --arg url "$URL" \
        '{
            type: "scraping",
            inputs: {
                url: $url
            }
        }')

    curl -s -X POST 'https://api.heybossai.com/v1/pilot' \
        -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
        -H 'Content-Type: application/json' \
        -d "$PAYLOAD"
done
