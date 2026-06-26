#!/bin/bash
# Scheduled Security Audit Runner
# Add to cron or run manually

SKILL_DIR="$HOME/.openclaw/workspace/skills/pre-publish-security"
STATE_FILE="$SKILL_DIR/audit-state.json"

show_status() {
    echo "=== Security Audit Schedule Status ==="
    echo ""
    
    if [ ! -f "$STATE_FILE" ]; then
        echo "No audit history found."
        exit 0
    fi
    
    echo "Last Scans:"
    jq -r '.lastRun | to_entries[] | "  \(.key): \(.value // "never")"' "$STATE_FILE"
    echo ""
    
    echo "Scan Counts:"
    jq -r '.scanCount | to_entries[] | "  \(.key): \(.value)"' "$STATE_FILE"
    echo ""
    
    echo "Total Findings:"
    jq -r '.findings | to_entries[] | "  \(.key): \(.value)"' "$STATE_FILE"
}

run_scheduled() {
    REPO_PATH="$1"
    
    if [ -z "$REPO_PATH" ]; then
        echo "Usage: $0 run <repo-path>"
        exit 1
    fi
    
    cd "$REPO_PATH" || exit 1
    
    # Check what needs to run based on last run times
    LAST_QUICK=$(jq -r '.lastRun.quickScan // "1970-01-01"' "$STATE_FILE")
    LAST_HISTORY=$(jq -r '.lastRun.historyScan // "1970-01-01"' "$STATE_FILE")
    LAST_DEP=$(jq -r '.lastRun.dependencyScan // "1970-01-01"' "$STATE_FILE")
    
    DAYS_SINCE_HISTORY=$(( ($(date +%s) - $(date -d "$LAST_HISTORY" +%s 2>/dev/null || echo 0)) / 86400 ))
    DAYS_SINCE_DEP=$(( ($(date +%s) - $(date -d "$LAST_DEP" +%s 2>/dev/null || echo 0)) / 86400 ))
    
    echo "=== Scheduled Security Audit ==="
    echo "Repository: $REPO_PATH"
    echo ""
    
    # Quick scan (always)
    echo "Running quick scan..."
    "$SKILL_DIR/audit-full.sh" "$REPO_PATH" quick
    
    # Dependency scan (if >7 days)
    if [ $DAYS_SINCE_DEP -gt 7 ]; then
        echo ""
        echo "Running dependency scan (last: $DAYS_SINCE_DEP days ago)..."
        "$SKILL_DIR/audit-full.sh" "$REPO_PATH" dependencies
    fi
    
    # History scan (if >30 days or never)
    if [ $DAYS_SINCE_HISTORY -gt 30 ] || [ "$LAST_HISTORY" = "1970-01-01" ]; then
        echo ""
        echo "Running git history scan (last: $DAYS_SINCE_HISTORY days ago)..."
        "$SKILL_DIR/audit-full.sh" "$REPO_PATH" history
    fi
}

case "$1" in
    status)
        show_status
        ;;
    run)
        run_scheduled "$2"
        ;;
    *)
        echo "Usage: $0 {status|run <repo-path>}"
        echo ""
        echo "Commands:"
        echo "  status              Show audit history and schedule"
        echo "  run <repo-path>     Run scheduled audits (auto-determines which scans)"
        exit 1
        ;;
esac
