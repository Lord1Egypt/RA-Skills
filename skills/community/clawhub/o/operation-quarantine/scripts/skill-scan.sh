#!/bin/bash
# Operation Quarantine — Skill Scanner
# Usage: bash skill-scan.sh <skill_name> [skill_content_file]
# Fetches from ClawHub if no file provided

QUARANTINE_PORT=${QUARANTINE_PORT:-8085}
QUARANTINE_URL="http://localhost:$QUARANTINE_PORT/quarantine/skill"

SKILL_NAME="$1"
SKILL_FILE="$2"

if [ -z "$SKILL_NAME" ]; then
  echo '{"error": "Usage: skill-scan.sh <skill_name> [content_file]"}'
  exit 1
fi

if [ -n "$SKILL_FILE" ] && [ -f "$SKILL_FILE" ]; then
  CONTENT=$(cat "$SKILL_FILE")
elif [ ! -t 0 ]; then
  CONTENT=$(cat)
else
  # Try fetching from ClawHub
  CONTENT=$(curl -s "https://clawhub.com/skills/$SKILL_NAME" 2>/dev/null)
  if [ -z "$CONTENT" ]; then
    CONTENT=$(curl -s "https://clawhub.com/api/skills/$SKILL_NAME" 2>/dev/null)
  fi
fi

if [ -z "$CONTENT" ]; then
  echo '{"error": "Could not fetch skill content"}'
  exit 1
fi

echo "$CONTENT" | jq -Rs --arg name "$SKILL_NAME" '{content: ., name: $name, source: "clawhub"}' | \
  curl -s -X POST "$QUARANTINE_URL" -H "Content-Type: application/json" -d @-
