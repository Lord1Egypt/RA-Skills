#!/bin/bash
# Push training plans to Likes API
# Usage: ./push_plans.sh <api_key> <plans.json>
#    or: LIKES_API_KEY=xxx ./push_plans.sh <plans.json>

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ $# -eq 1 ]; then
    # Assume API key from env
    node "${SCRIPT_DIR}/push_plans.js" --env "$1"
elif [ $# -eq 2 ]; then
    # API key as first arg
    node "${SCRIPT_DIR}/push_plans.js" "$1" "$2"
else
    echo "Usage: $0 <api_key> <plans.json>"
    echo "   or: LIKES_API_KEY=xxx $0 <plans.json>"
    exit 1
fi
