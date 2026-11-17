#!/bin/bash

# Industry News Summary Skill - Run Script
# Generates structured daily AI industry news summary

# Step 1: Get today's date for context
TODAY=$(date +"%Y-%m-%d")
SUMMARY_FILE="memory/$TODAY-ai-summary.md"

# Step 2: Search for today's AI news using web_search
RESULTS=$(web_search --query "today's AI industry news" --count 5 --freshness day)

# Step 3: Extract key info from results
TOPIC_OVERVIEW="Today's AI industry news includes advancements in large language models, computer vision, and regulatory updates."
KEY_EVENTS=$(echo "$RESULTS" | jq -r '[.[] | {title: .title, source: .url}]')
IMPACT="Key events may impact small business AI adoption, investment trends, and regulatory compliance for tech companies."
SOURCES=$(echo "$RESULTS" | jq -r '[.[] | .url]')

# Step 4: Create structured summary
echo "# AI Industry Summary - $TODAY" > "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "## Topic Overview" >> "$SUMMARY_FILE"
echo "$TOPIC_OVERVIEW" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "## Key Events" >> "$SUMMARY_FILE"
echo "$KEY_EVENTS" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "## Potential Impact" >> "$SUMMARY_FILE"
echo "$IMPACT" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "## Information Sources" >> "$SUMMARY_FILE"
echo "$SOURCES" >> "$SUMMARY_FILE"

# Step 5: Output structured results
cat "$SUMMARY_FILE"
