#!/bin/bash
# Set up the MeiliSearch learnings index
# Usage: bash setup_index.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load shared config
source "$SKILL_DIR/lib/config.sh" 2>/dev/null || source "/root/.openclaw/workspace/skills/lib/config.sh"

INDEX="learnings"

# Wait for MeiliSearch
for i in $(seq 1 10); do
  if curl -s "${MEILI_HOST}/health" > /dev/null 2>&1; then break; fi
  sleep 1
done

echo "=== Setting up '${INDEX}' index ==="

# Create index
curl -s -X POST "${MEILI_HOST}/indexes" \
  -H "Authorization: Bearer ${MEILI_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"uid\":\"${INDEX}\",\"primaryKey\":\"id\"}" > /dev/null 2>&1 || true

sleep 1

# Configure settings
curl -s -X PATCH "${MEILI_HOST}/indexes/${INDEX}/settings" \
  -H "Authorization: Bearer ${MEILI_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "searchableAttributes": ["what_happened", "fix", "context", "category", "tags"],
    "filterableAttributes": ["category", "importance", "date", "tags", "source"],
    "rankingRules": ["words", "typo", "proximity", "sort", "attribute", "exactness"],
    "typoTolerance": {
      "enabled": true,
      "minWordSizeForTypos": { "oneTypo": 3, "twoTypos": 6 }
    }
  }' > /dev/null

sleep 0.5

# Verify
STATS=$(curl -s "${MEILI_HOST}/indexes/${INDEX}/stats" -H "Authorization: Bearer ${MEILI_KEY}" 2>/dev/null)
COUNT=$(echo "$STATS" | python3 -c "import json,sys; print(json.load(sys.stdin).get('numberOfDocuments','?'))" 2>/dev/null || echo "?")

echo "'${INDEX}' index ready (${COUNT} documents)"
echo "Done."
