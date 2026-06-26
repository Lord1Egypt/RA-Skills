#!/usr/bin/env bash
# Session Counter - MetaClaw Integration
# Track Sessions für konsolidierte Consolidation
# Speichert Sessions in $WORKSPACE/.session-count

set -e

# WORKSPACE Environment Variable (default: ~/.openclaw/workspace)
WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
SESSION_COUNT_FILE="$WORKSPACE/.session-count"
SESSION_DIR="$WORKSPACE/.session-data"

# Default Config
DEFAULT_INTERVAL=10
DEFAULT_MIN_HOURS=6

# Lade Config (überschreibt Defaults)
CONFIG_FILE="$WORKSPACE/memory/config.yaml"
if [ -f "$CONFIG_FILE" ]; then
    # Extrahiere Werte aus YAML (einfache Parsung)
    INTERVAL=$(grep "interval_sessions:" "$CONFIG_FILE" 2>/dev/null | grep -oE '[0-9]+' | head -1)
    MIN_HOURS=$(grep "min_interval_hours:" "$CONFIG_FILE" 2>/dev/null | grep -oE '[0-9]+' | head -1)
fi

# Default falls nicht in Config
INTERVAL=${INTERVAL:-$DEFAULT_INTERVAL}
MIN_HOURS=${MIN_HOURS:-$DEFAULT_MIN_HOURS}

# Hilfsfunktion: Count Datei erstellen wenn nicht existiert
init_counter() {
    if [ ! -f "$SESSION_COUNT_FILE" ]; then
        echo "0" > "$SESSION_COUNT_FILE"
        touch "$SESSION_DIR/last_consolidation"
    fi
}

# Hilfsfunktion: Logger
log() {
    local msg="$1"
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] [SessionCounter] $msg"
}

# Hilfsfunktion: Get current count
get_count() {
    init_counter
    cat "$SESSION_COUNT_FILE" 2>/dev/null || echo "0"
}

# Hilfsfunktion: Increment counter
increment() {
    local current=$(get_count)
    local new=$((current + 1))
    echo "$new" > "$SESSION_COUNT_FILE"
    log "Incremented: $current → $new"
    echo "$new"
}

# Hilfsfunktion: Get last consolidation time (in hours)
get_last_consolidation_hours() {
    if [ -f "$SESSION_DIR/last_consolidation" ]; then
        local last=$(stat -f %m "$SESSION_DIR/last_consolidation" 2>/dev/null || stat -c %Y "$SESSION_DIR/last_consolidation" 2>/dev/null || echo "0")
        local now=$(date +%s)
        local diff=$(( (now - last) / 3600 ))
        echo "${diff:-9999}"
    else
        echo "9999"  # Never consolidated
    fi
}

# Hilfsfunktion: Should consolidate?
should_consolidate() {
    local count=$(get_count)
    local hours=$(get_last_consolidation_hours)
    
    log "Current count: $count/$INTERVAL, Hours since last: $hours/$MIN_HOURS"
    
    if [ "$count" -ge "$INTERVAL" ] && [ "$hours" -ge "$MIN_HOURS" ]; then
        log "✅ Consolidation ready: count=$count/$INTERVAL, hours=$hours/$MIN_HOURS"
        return 0
    else
        log "❌ Not ready: count=$count/$INTERVAL, hours=$hours/$MIN_HOURS"
        return 1
    fi
}

# Hilfsfunktion: Reset counter after consolidation
reset() {
    local current=$(get_count)
    echo "0" > "$SESSION_COUNT_FILE"
    touch "$SESSION_DIR/last_consolidation"
    log "Reset counter: $current → 0"
}

# CLI Interface
case "${1:-}" in
    --increment|-i)
        increment
        ;;
    --get|-g)
        get_count
        ;;
    --reset|-r)
        reset
        ;;
    --check|-c)
        if should_consolidate; then
            echo "true"
            exit 0
        else
            echo "false"
            exit 1
        fi
        ;;
    --status|-s)
        count=$(get_count)
        hours=$(get_last_consolidation_hours)
        echo "Session Counter Status:"
        echo "  Current: $count/$INTERVAL"
        echo "  Hours since last: $hours/$MIN_HOURS"
        if should_consolidate; then
            echo "  ✅ Ready for consolidation"
        else
            echo "  ⏳ Not ready yet"
        fi
        ;;
    --help|-h)
        echo "Session Counter - MetaClaw Integration"
        echo ""
        echo "Usage: $0 [option]"
        echo ""
        echo "Options:"
        echo "  --increment, -i    Increment session counter"
        echo "  --get, -g          Get current count"
        echo "  --reset, -r        Reset counter after consolidation"
        echo "  --check, -c        Check if consolidation should run (exit 0 if yes)"
        echo "  --status, -s       Show detailed status"
        echo "  --help, -h         Show this help"
        ;;
    *)
        # Default: increment on any other call
        increment
        ;;
esac
