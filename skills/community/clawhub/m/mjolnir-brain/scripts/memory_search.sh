#!/bin/bash
# memory_search.sh - Memory search tool (v2: fuzzy match + multi-source)
# Usage: ./memory_search.sh <keyword> [options]
# Options: -f fuzzy search  -a search archive  -c N context lines (default 2)

WORKSPACE="${MJOLNIR_BRAIN_WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_MD="$WORKSPACE/MEMORY.md"
MEMORY_DIR="$WORKSPACE/memory"
ARCHIVE_DIR="$WORKSPACE/memory/archive"
CORE_FILES=("$WORKSPACE/MEMORY.md" "$WORKSPACE/TOOLS.md" "$WORKSPACE/AGENTS.md" "$WORKSPACE/SOUL.md" "$WORKSPACE/HEARTBEAT.md")

FUZZY=0
SEARCH_ARCHIVE=0
CONTEXT=2

while [[ $# -gt 0 ]]; do
    case "$1" in
        -f) FUZZY=1; shift ;;
        -a) SEARCH_ARCHIVE=1; shift ;;
        -c) CONTEXT="$2"; shift 2 ;;
        -*) echo "Unknown option: $1"; exit 1 ;;
        *) KEYWORD="$1"; shift ;;
    esac
done

if [ -z "$KEYWORD" ]; then
    echo "🔍 memory_search v2 — Memory search tool"
    echo ""
    echo "Usage: $0 <keyword> [options]"
    echo ""
    echo "Options:"
    echo "  -f    Fuzzy search (allows gaps between characters)"
    echo "  -a    Also search archive files (memory/archive/)"
    echo "  -c N  Context lines to show (default 2)"
    echo ""
    echo "Examples:"
    echo "  $0 deployment"
    echo "  $0 -f 'server port'"
    echo "  $0 -a -c 5 database"
    exit 1
fi

if [ "$FUZZY" -eq 1 ]; then
    PATTERN=$(echo "$KEYWORD" | sed 's/./&.{0,10}/g' | sed 's/.{0,10}$//')
    GREP_OPTS="-P -i"
    echo "🔍 Fuzzy search: $KEYWORD"
else
    PATTERN="$KEYWORD"
    GREP_OPTS="-i"
    echo "🔍 Exact search: $KEYWORD"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

TOTAL_HITS=0

count_matches() {
    local file="$1"
    grep $GREP_OPTS "$PATTERN" "$file" 2>/dev/null | wc -l
}

echo -e "\n📋 Core files:"
for file in "${CORE_FILES[@]}"; do
    [ -f "$file" ] || continue
    HITS=$(count_matches "$file")
    if [ "$HITS" -gt 0 ]; then
        BN=$(basename "$file")
        echo "  ✅ $BN ($HITS matches)"
        grep $GREP_OPTS -n -B 1 -A "$CONTEXT" "$PATTERN" "$file" 2>/dev/null | head -20 | sed 's/^/     /'
        TOTAL_HITS=$((TOTAL_HITS + HITS))
    fi
done

echo -e "\n📝 Daily logs:"
for file in "$MEMORY_DIR"/*.md; do
    [ -f "$file" ] || continue
    HITS=$(count_matches "$file")
    if [ "$HITS" -gt 0 ]; then
        BN=$(basename "$file")
        echo "  ✅ $BN ($HITS matches)"
        grep $GREP_OPTS -n "$PATTERN" "$file" 2>/dev/null | head -5 | sed 's/^/     /'
        TOTAL_HITS=$((TOTAL_HITS + HITS))
    fi
done

if [ "$SEARCH_ARCHIVE" -eq 1 ] && [ -d "$ARCHIVE_DIR" ]; then
    echo -e "\n📦 Archive:"
    for file in "$ARCHIVE_DIR"/*.md.gz; do
        [ -f "$file" ] || continue
        HITS=$(zgrep $GREP_OPTS "$PATTERN" "$file" 2>/dev/null | wc -l)
        if [ "$HITS" -gt 0 ]; then
            BN=$(basename "$file")
            echo "  ✅ $BN ($HITS matches)"
            zgrep $GREP_OPTS -n "$PATTERN" "$file" 2>/dev/null | head -5 | sed 's/^/     /'
            TOTAL_HITS=$((TOTAL_HITS + HITS))
        fi
    done
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ "$TOTAL_HITS" -gt 0 ]; then
    echo "📊 Found $TOTAL_HITS matches"
else
    echo "❌ No matches found"
    [ "$FUZZY" -eq 0 ] && echo "💡 Try fuzzy search: $0 -f $KEYWORD"
fi
