#!/bin/bash
# memory_consolidate.sh - Memory maintenance (v2: real AI summarization, not raw copy)
# Features: clean garbage files, archive old logs, trim state files, check capacity
# Cron: 0 4 * * * (daily at 04:00)

set -e

WORKSPACE="${MJOLNIR_BRAIN_WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
STATE_FILE="$MEMORY_DIR/memory-state.json"
LOG_FILE="$MEMORY_DIR/consolidate.log"
MEMORY_MD="$WORKSPACE/MEMORY.md"
MAX_MEMORY_KB=20  # MEMORY.md size cap

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Memory maintenance started ==="

# === 1. Clean garbage files (< 200 bytes session headers) ===
CLEANED=0
for file in "$MEMORY_DIR"/????-??-??.md "$MEMORY_DIR"/????-??-??-????.md; do
    [ -f "$file" ] || continue
    SIZE=$(wc -c < "$file")
    if [ "$SIZE" -lt 200 ]; then
        BASENAME=$(basename "$file")
        TODAY=$(date '+%Y-%m-%d')
        if [[ "$BASENAME" == "${TODAY}"* ]]; then continue; fi
        rm -f "$file"
        log "🗑️  Deleted garbage: $BASENAME (${SIZE}B)"
        CLEANED=$((CLEANED + 1))
    fi
done
[ $CLEANED -gt 0 ] && log "Cleaned $CLEANED garbage files"

# === 2. Archive logs older than 30 days ===
ARCHIVE_DIR="$MEMORY_DIR/archive"
ARCHIVED=0
CUTOFF=$(date -d "30 days ago" '+%Y-%m-%d' 2>/dev/null || date -v-30d '+%Y-%m-%d' 2>/dev/null || echo "")
if [ -n "$CUTOFF" ]; then
    for file in "$MEMORY_DIR"/????-??-??.md; do
        [ -f "$file" ] || continue
        BASENAME=$(basename "$file" .md)
        if [[ "$BASENAME" < "$CUTOFF" ]]; then
            mkdir -p "$ARCHIVE_DIR"
            gzip -c "$file" > "$ARCHIVE_DIR/${BASENAME}.md.gz"
            rm -f "$file"
            log "📦 Archived: $BASENAME"
            ARCHIVED=$((ARCHIVED + 1))
        fi
    done
fi
[ $ARCHIVED -gt 0 ] && log "Archived $ARCHIVED old logs"

# === 3. Check MEMORY.md capacity ===
MEMORY_SIZE=$(wc -c < "$MEMORY_MD" | tr -d ' ')
MEMORY_KB=$((MEMORY_SIZE / 1024))
log "📊 MEMORY.md: ${MEMORY_KB}KB / ${MAX_MEMORY_KB}KB"
if [ "$MEMORY_KB" -gt "$MAX_MEMORY_KB" ]; then
    log "⚠️  MEMORY.md exceeds ${MAX_MEMORY_KB}KB cap — needs AI trimming"
fi

# === 4. List pending daily logs (for AI heartbeat to process) ===
PENDING=()
for file in "$MEMORY_DIR"/????-??-??.md; do
    [ -f "$file" ] || continue
    BASENAME=$(basename "$file")
    SIZE=$(wc -c < "$file")
    [ "$SIZE" -lt 200 ] && continue
    if ! grep -q "^# consolidated:" "$file" 2>/dev/null; then
        PENDING+=("$BASENAME")
    fi
done

# Update state file
python3 << PYTHON_SCRIPT
import json
from datetime import datetime, timedelta

state = {
    "lastRun": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
    "pendingConsolidation": [$(printf '"%s",' "${PENDING[@]}" | sed 's/,$//')],
    "memoryMdKB": $MEMORY_KB,
    "maxKB": $MAX_MEMORY_KB,
    "cleaned": $CLEANED,
    "archived": $ARCHIVED
}

with open('$STATE_FILE', 'w') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)
PYTHON_SCRIPT

if [ ${#PENDING[@]} -gt 0 ]; then
    log "📋 Pending: ${PENDING[*]}"
    log "💡 AI will summarize these during next heartbeat"
else
    log "✅ No pending logs"
fi

log "=== Memory maintenance complete ==="
