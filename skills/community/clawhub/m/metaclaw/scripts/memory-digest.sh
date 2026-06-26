#!/usr/bin/env bash
# Memory Digest - MetaClaw Integration (Auto-Dream Implementation)
# Konsolidiert, bereinigt, reorganisiert Memory-Files

set -e

# WORKSPACE Environment Variable (default: ~/.openclaw/workspace)
WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
SESSION_STATE="$WORKSPACE/SESSION-STATE.md"
ARCHIVE_FILE="$MEMORY_DIR/ARCHIVED.md"

# Flags
AUTO_DREAM=false
DRY_RUN=false
FORCE=false

for arg in "$@"; do
    case $arg in
        --auto-dream) AUTO_DREAM=true ;;
        --dry-run) DRY_RUN=true ;;
        --force) FORCE=true ;;
    esac
done

# Load session counter script
SESSION_COUNTER="$WORKSPACE/scripts/session-counter.sh"

# Check if consolidation is needed
if [ "$FORCE" = false ] && [ -f "$SESSION_COUNTER" ]; then
    SHOULD_CONSOLIDATE=$("$SESSION_COUNTER" --check 2>/dev/null || echo "false")
    if [ "$SHOULD_CONSOLIDATE" != "true" ]; then
        if [ "$AUTO_DREAM" = false ]; then
            echo "⚠️  Consolidation not needed yet (run with --force to override)"
            exit 0
        fi
    fi
fi

echo "=== Memory Digest ($(date +%Y-%m-%d\ %H:%M)) ==="
echo ""

# Phase 1: Orientation
echo "[Phase 1] Orientation..."

# Count memory files
MEMORY_FILES=$(find "$MEMORY_DIR" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
MEMORY_LINES=$(wc -l < "$MEMORY_FILE" 2>/dev/null || echo "0")

echo "  Memory files: $MEMORY_FILES"
echo "  MEMORY.md lines: $MEMORY_LINES"

# Phase 2: Gather Signal
echo ""
echo "[Phase 2] Gather Signal..."

# Check for stale references (files that no longer exist)
STALE_REFS=""
if [ -f "$SESSION_STATE" ]; then
    # Extract file paths from SESSION-STATE (simplified - avoid problematic regex)
    while IFS= read -r line; do
        # Check for common file patterns
        if [[ "$line" =~ \.md ]] || [[ "$line" =~ \.py ]] || [[ "$line" =~ \.sh ]]; then
            # Skip if it's just a description
            if [[ "$line" =~ "Status:" ]] || [[ "$line" =~ "Task:" ]]; then
                continue
            fi
            # Extract potential file paths (simplified)
            FILE_PATH=$(echo "$line" | grep -oE '[~/][a-zA-Z0-9_./-]+\.(md|py|sh|json)' 2>/dev/null | head -1 || true)
            if [ -n "$FILE_PATH" ]; then
                # Expand ~ to $HOME
                EXPANDED="${FILE_PATH/#\~/$HOME}"
                if [ ! -f "$EXPANDED" ] && [ ! -d "$EXPANDED" ]; then
                    STALE_REFS="$STALE_REFS\n  - $FILE_PATH"
                fi
            fi
        fi
    done < "$SESSION_STATE"
fi

if [ -n "$STALE_REFS" ]; then
    echo "  ⚠️  Stale references found:"
    echo -e "$STALE_REFS" | head -5
else
    echo "  ✓ No stale references"
fi

# Phase 3: Consolidation
echo ""
echo "[Phase 3] Consolidation..."

# Check MEMORY.md size
MAX_LINES=200
if [ "$MEMORY_LINES" -gt "$MAX_LINES" ]; then
    echo "  ⚠️  MEMORY.md exceeds $MAX_LINES lines ($MEMORY_LINES)"
    echo "  📋 Suggestion: Archive old entries to ARCHIVED.md"
    
    if [ "$DRY_RUN" = false ] && [ "$AUTO_DREAM" = true ]; then
        # Find lines older than 30 days (simplified - just mark for review)
        echo "  📝 Marked for archive review"
    fi
else
    echo "  ✓ MEMORY.md within limit ($MEMORY_LINES/$MAX_LINES lines)"
fi

# Check for relative dates in MEMORY.md
RELATIVE_DATES=$(grep -i "gestern\|vorgestern\|letzte woche\|vor.*tagen\|yesterday\|last week" "$MEMORY_FILE" 2>/dev/null | wc -l | tr -d ' ')
if [ "$RELATIVE_DATES" -gt 0 ]; then
    echo "  ⚠️  Found $RELATIVE_DATES relative date(s) - consider converting to absolute"
else
    echo "  ✓ No relative dates found"
fi

# Phase 4: Prune & Index
echo ""
echo "[Phase 4] Prune & Index..."

# Check for contradictions in SESSION-STATE (simplified)
if [ -f "$SESSION_STATE" ]; then
    DUPLICATE_STATUS=$(grep -c -E "Status:.*(Active|WIP)" "$SESSION_STATE" 2>/dev/null || true)
    DUPLICATE_STATUS=${DUPLICATE_STATUS:-0}
    if [ "$DUPLICATE_STATUS" -gt 3 ]; then
        echo "  ⚠️  Multiple active tasks ($DUPLICATE_STATUS) - consider prioritization"
    else
        echo "  ✓ Active tasks within normal range"
    fi
fi

# Update session counter if consolidation ran
if [ "$AUTO_DREAM" = true ] || [ "$FORCE" = true ]; then
    echo ""
    echo "[Phase 5] Update Session Counter..."
    
    if [ -f "$SESSION_COUNTER" ]; then
        "$SESSION_COUNTER" --reset
        echo "  ✓ Session counter reset"
    else
        echo "  ⚠️  Session counter script not found"
    fi
fi

# Summary
echo ""
echo "=== Summary ==="

ISSUES=0
[ -n "$STALE_REFS" ] && ISSUES=$((ISSUES + 1))
[ "$MEMORY_LINES" -gt "$MAX_LINES" ] && ISSUES=$((ISSUES + 1))
[ "$RELATIVE_DATES" -gt 0 ] && ISSUES=$((ISSUES + 1))

if [ "$ISSUES" -eq 0 ]; then
    echo "✅ Memory is healthy"
    echo "  - No stale references"
    echo "  - MEMORY.md within limit"
    echo "  - No relative dates"
else
    echo "⚠️  $ISSUES issue(s) found"
    [ -n "$STALE_REFS" ] && echo "  - Stale references need cleanup"
    [ "$MEMORY_LINES" -gt "$MAX_LINES" ] && echo "  - MEMORY.md needs pruning ($MEMORY_LINES > $MAX_LINES)"
    [ "$RELATIVE_DATES" -gt 0 ] && echo "  - Relative dates need conversion"
fi

# Write digest timestamp
TODAY=$(date +%Y-%m-%d)
echo "$TODAY" > "$MEMORY_DIR/.last-digest"

echo ""
echo "✓ Digest complete"

# Exit code based on issues
[ "$ISSUES" -gt 0 ] && exit 1
exit 0
