#!/bin/bash
# Summarize a concept across all documents

set -e

KB_ROOT="${KB_ROOT:-$HOME/kb}"
CONCEPT="$1"

if [ -z "$CONCEPT" ]; then
    echo "Usage: $0 <concept>"
    exit 1
fi

echo "Summarizing: $CONCEPT"
echo ""
echo "=== Relevant Passages ==="
echo ""

# Collect relevant passages
PASSAGES=""
for txt in "$KB_ROOT/docs"/*.txt; do
    [ -f "$txt" ] || continue
    DOC_ID=$(basename "$txt" .txt)
    META="$KB_ROOT/index/${DOC_ID}.json"
    [ -f "$META" ] || continue
    
    NAME=$(grep -o '"name": *"[^"]*"' "$META" | cut -d'"' -f4)
    
    if grep -qi "$CONCEPT" "$txt" 2>/dev/null; then
        echo "📄 $NAME"
        grep -i -A2 -B2 "$CONCEPT" "$txt" | head -10
        echo ""
    fi
done

echo "=== Summary ==="
echo "Use an AI model to synthesize the above passages into a coherent summary."
echo "Command: ollama run qwen3.5 'Summarize the concept of $CONCEPT based on these passages...'"
