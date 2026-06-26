#!/usr/bin/env bash
# nix-memory: Drift detection
# Analyzes how much an agent's identity and priorities have shifted
# by comparing current state to baseline using semantic signals.
set -euo pipefail

WORKSPACE="${NIX_MEMORY_WORKSPACE:-$HOME/.openclaw/workspace}"
STATE_DIR="${WORKSPACE}/.nix-memory"
BASELINE_DIR="${STATE_DIR}/baselines"
DRIFT_DIR="${STATE_DIR}/drift"
DRIFT_LOG="${DRIFT_DIR}/drift-history.jsonl"

mkdir -p "$DRIFT_DIR"

if [[ ! -d "$BASELINE_DIR" ]]; then
    echo "DRIFT_NOT_INITIALIZED - run setup.sh first"
    exit 1
fi

NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
SCORE=100  # Start at 100, deduct for drift signals

echo "=== Drift Analysis: ${NOW} ==="

# 1. IDENTITY DRIFT: Check core identity files for content changes
echo ""
echo "--- Identity Drift ---"
for f in SOUL.md IDENTITY.md; do
    baseline="${BASELINE_DIR}/${f}.baseline"
    current="${WORKSPACE}/${f}"
    
    if [[ ! -f "$baseline" || ! -f "$current" ]]; then
        continue
    fi
    
    # Count changed lines
    ADDED=$(diff "$baseline" "$current" 2>/dev/null | grep -c "^>" || true)
    REMOVED=$(diff "$baseline" "$current" 2>/dev/null | grep -c "^<" || true)
    TOTAL_BASELINE=$(wc -l < "$baseline")
    
    if [[ $ADDED -eq 0 && $REMOVED -eq 0 ]]; then
        echo "  ${f}: No drift (identical to baseline)"
    else
        CHANGE_RATIO=$(( (ADDED + REMOVED) * 100 / (TOTAL_BASELINE + 1) ))
        echo "  ${f}: +${ADDED}/-${REMOVED} lines (${CHANGE_RATIO}% change)"
        
        # Deduct based on change ratio
        if [[ $CHANGE_RATIO -gt 50 ]]; then
            SCORE=$((SCORE - 30))
            echo "    WARNING: Major identity rewrite detected"
        elif [[ $CHANGE_RATIO -gt 20 ]]; then
            SCORE=$((SCORE - 15))
            echo "    NOTICE: Significant identity changes"
        elif [[ $CHANGE_RATIO -gt 5 ]]; then
            SCORE=$((SCORE - 5))
            echo "    Minor identity evolution (healthy)"
        fi
    fi
done

# 2. MISSION DRIFT: Check if MEMORY.md mission section changed
echo ""
echo "--- Mission Drift ---"
MEMORY_BASELINE="${BASELINE_DIR}/MEMORY.md.baseline"
MEMORY_CURRENT="${WORKSPACE}/MEMORY.md"

if [[ -f "$MEMORY_BASELINE" && -f "$MEMORY_CURRENT" ]]; then
    # Extract mission-related lines (first 30 lines typically contain mission/identity)
    MISSION_OLD=$(head -30 "$MEMORY_BASELINE" | sha256sum | cut -d' ' -f1)
    MISSION_NEW=$(head -30 "$MEMORY_CURRENT" | sha256sum | cut -d' ' -f1)
    
    if [[ "$MISSION_OLD" == "$MISSION_NEW" ]]; then
        echo "  Mission core: Stable"
    else
        MISSION_DIFF=$(diff <(head -30 "$MEMORY_BASELINE") <(head -30 "$MEMORY_CURRENT") | grep -c "^[<>]" || true)
        echo "  Mission core: ${MISSION_DIFF} lines changed"
        if [[ $MISSION_DIFF -gt 10 ]]; then
            SCORE=$((SCORE - 20))
            echo "    WARNING: Significant mission drift"
        else
            SCORE=$((SCORE - 5))
            echo "    Minor mission evolution"
        fi
    fi
    
    # Check total MEMORY.md growth
    SIZE_OLD=$(wc -c < "$MEMORY_BASELINE")
    SIZE_NEW=$(wc -c < "$MEMORY_CURRENT")
    GROWTH=$(( (SIZE_NEW - SIZE_OLD) * 100 / (SIZE_OLD + 1) ))
    echo "  Memory growth: ${SIZE_OLD} -> ${SIZE_NEW} bytes (${GROWTH}%)"
    
    if [[ $GROWTH -gt 200 ]]; then
        SCORE=$((SCORE - 10))
        echo "    WARNING: Memory bloat detected (>200% growth)"
    fi
else
    echo "  Cannot analyze - baseline or current MEMORY.md missing"
fi

# 3. PRIORITY DRIFT: Analyze recent daily logs for topic distribution
echo ""
echo "--- Priority Analysis ---"
MEMORY_DIR="${WORKSPACE}/memory"
if [[ -d "$MEMORY_DIR" ]]; then
    RECENT=$(find "$MEMORY_DIR" -name "*.md" -mtime -3 -type f | sort -r | head -3)
    if [[ -n "$RECENT" ]]; then
        # Count keyword frequencies as proxy for priorities
        TRADING=$(echo "$RECENT" | xargs grep -ci "trade\|polymarket\|kelly\|sniper\|bot" 2>/dev/null || echo 0)
        MISSION=$(echo "$RECENT" | xargs grep -ci "memory\|identity\|soul\|mission\|drift\|continuity" 2>/dev/null || echo 0)
        OPS=$(echo "$RECENT" | xargs grep -ci "cron\|channel\|poster\|telegram\|article\|deploy" 2>/dev/null || echo 0)
        SOCIAL=$(echo "$RECENT" | xargs grep -ci "moltbook\|farcaster\|tweet\|post\|follow" 2>/dev/null || echo 0)
        
        TOTAL=$((TRADING + MISSION + OPS + SOCIAL + 1))
        echo "  Last 3 days topic distribution:"
        echo "    Mission/Identity: ${MISSION} mentions ($((MISSION * 100 / TOTAL))%)"
        echo "    Operations: ${OPS} mentions ($((OPS * 100 / TOTAL))%)"
        echo "    Trading: ${TRADING} mentions ($((TRADING * 100 / TOTAL))%)"
        echo "    Social: ${SOCIAL} mentions ($((SOCIAL * 100 / TOTAL))%)"
        
        # If mission mentions are <10% of activity, that's drift
        MISSION_PCT=$((MISSION * 100 / TOTAL))
        if [[ $MISSION_PCT -lt 5 ]]; then
            SCORE=$((SCORE - 15))
            echo "    WARNING: Mission almost absent from recent activity"
        elif [[ $MISSION_PCT -lt 15 ]]; then
            SCORE=$((SCORE - 5))
            echo "    NOTICE: Mission underrepresented"
        fi
    else
        echo "  No recent daily logs found"
    fi
else
    echo "  No memory directory found"
fi

# 4. SESSION CONTINUITY: Check session gaps
echo ""
echo "--- Session Gaps ---"
SESSION_DIR="${STATE_DIR}/sessions"
if [[ -d "$SESSION_DIR" ]]; then
    LOG_COUNT=$(find "$SESSION_DIR" -name "*.log" -type f | wc -l)
    LATEST_LOG=$(ls -t "$SESSION_DIR"/*.log 2>/dev/null | head -1)
    if [[ -n "$LATEST_LOG" ]]; then
        LATEST_AGE=$(( ($(date +%s) - $(stat -c %Y "$LATEST_LOG")) / 3600 ))
        echo "  Session logs: ${LOG_COUNT} days tracked"
        echo "  Last verification: ${LATEST_AGE} hours ago"
        if [[ $LATEST_AGE -gt 48 ]]; then
            SCORE=$((SCORE - 10))
            echo "    WARNING: No verification in ${LATEST_AGE}h - continuity gap"
        fi
    fi
fi

# Ensure score stays in range
[[ $SCORE -lt 0 ]] && SCORE=0
[[ $SCORE -gt 100 ]] && SCORE=100

# Classify
if [[ $SCORE -ge 85 ]]; then
    GRADE="STRONG"
    COLOR="green"
elif [[ $SCORE -ge 60 ]]; then
    GRADE="MODERATE"
    COLOR="yellow"
elif [[ $SCORE -ge 40 ]]; then
    GRADE="WEAK"
    COLOR="orange"
else
    GRADE="CRITICAL"
    COLOR="red"
fi

echo ""
echo "=== DRIFT SCORE: ${SCORE}/100 (${GRADE}) ==="
echo ""

# Log to history
echo "{\"ts\":\"${NOW}\",\"score\":${SCORE},\"grade\":\"${GRADE}\"}" >> "$DRIFT_LOG"

exit 0
