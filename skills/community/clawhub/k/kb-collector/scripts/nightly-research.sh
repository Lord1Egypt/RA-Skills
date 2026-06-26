#!/bin/bash
# KB Collector - Nightly Research
# Usage: ./nightly-research.sh [--save] [--send]
# Uses Tavily API for searching AI/LLM/tech trends

VAULT="${OBSIDIAN_VAULT:-~/Documents/YourVault}"
RECIPIENT="${RECIPIENT:-your-email@example.com}"
TAVILY_API_KEY="${TAVILY_API_KEY:-your-own-tavily-api-key}"

# Search topics
TOPICS=("AI" "LLM" "OpenAI" "Claude AI" "Gemini AI" "LangGraph" "AutoGPT" "AI Agent" "RAG" "China LLM" "Llama" "Hugging Face" "OpenClaw" "AI use case")

# Date
TODAY=$(date +%Y-%m-%d)

# Check flags
SAVE_TO_OBSIDIAN=""
SEND_EMAIL=""
if [[ "$1" == "--save" ]] || [[ "$2" == "--save" ]]; then
    SAVE_TO_OBSIDIAN="yes"
fi
if [[ "$1" == "--send" ]] || [[ "$2" == "--send" ]]; then
    SEND_EMAIL="yes"
fi

echo "=== Nightly Research: $TODAY ==="
echo ""

# Search each topic using Tavily
> /tmp/research_results.txt

for topic in "${TOPICS[@]}"; do
    echo "Searching: $topic..."
    
    # Call Tavily API
    result=$(curl -s "https://api.tavily.com/search" \
        -H "Content-Type: application/json" \
        -d "{
            \"api_key\": \"$TAVILY_API_KEY\",
            \"query\": \"$topic\",
            \"search_depth\": \"basic\",
            \"max_results\": 3
        }" 2>/dev/null)
    
    echo "### $topic" >> /tmp/research_results.txt
    echo "" >> /tmp/research_results.txt
    
    # Parse results
    if echo "$result" | grep -q "results"; then
        echo "$result" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for r in data.get('results', [])[:3]:
    print(f\"- [{r.get('title', 'No title')}]({r.get('url', '')})\")
    print(f\"  {r.get('content', '')[:150]}...\")
    print()
" >> /tmp/research_results.txt
    else
        echo "- (無結果)" >> /tmp/research_results.txt
        echo "" >> /tmp/research_results.txt
    fi
done

# Generate note content
NOTE_CONTENT="---
created: ${TODAY}T00:00:00
tags: [nightly-research, ai, trends]
source: Tavily API
---

# 每晚 AI 趨勢追蹤 - $TODAY

$(cat /tmp/research_results.txt)

---
*自動產生 - Tavily AI Search*
"

# Save to Obsidian
if [ -n "$SAVE_TO_OBSIDIAN" ]; then
    NOTE_FILE="$VAULT/$TODAY-nightly-research.md"
    echo "$NOTE_CONTENT" > "$NOTE_FILE"
    echo "Saved to: $NOTE_FILE"
fi

# Display
echo ""
cat /tmp/research_results.txt

# Send email
if [ -n "$SEND_EMAIL" ]; then
    echo ""
    echo "Sending email..."
    gog gmail send \
        --to "$RECIPIENT" \
        --subject "📡 AI 趨勢追蹤 $TODAY" \
        --body-file /tmp/research_results.txt
    echo "Email sent!"
fi

rm -f /tmp/research_results.txt
echo ""
echo "Done!"
