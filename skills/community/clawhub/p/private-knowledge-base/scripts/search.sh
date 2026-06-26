#!/bin/bash
# Semantic search across all ingested documents

set -e

KB_ROOT="${KB_ROOT:-$HOME/kb}"
QUERY="$1"

if [ -z "$QUERY" ]; then
    echo "Usage: $0 <search-query>"
    exit 1
fi

echo "Searching for: $QUERY"
echo ""

# Simple grep-based search (fallback)
# In production, use vector embeddings
FOUND=0
for txt in "$KB_ROOT/docs"/*.txt; do
    [ -f "$txt" ] || continue
    DOC_ID=$(basename "$txt" .txt)
    META="$KB_ROOT/index/${DOC_ID}.json"
    [ -f "$META" ] || continue
    
    NAME=$(grep -o '"name": *"[^"]*"' "$META" | cut -d'"' -f4)
    
    if grep -qi "$QUERY" "$txt" 2>/dev/null; then
        MATCHES=$(grep -in "$QUERY" "$txt" | head -3)
        echo "📄 $NAME"
        echo "   $MATCHES" | head -3 | sed 's/^/   /'
        echo ""
        FOUND=1
    fi
done

if [ $FOUND -eq 0 ]; then
    echo "No documents found matching: $QUERY"
    exit 1
fi
