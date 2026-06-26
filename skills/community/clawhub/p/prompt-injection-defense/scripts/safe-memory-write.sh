#!/usr/bin/env bash
# safe-memory-write.sh — Scan content before writing to memory files
# Usage: safe-memory-write.sh --source "web_search" --target "daily" --text "content"
#        echo "content" | safe-memory-write.sh --source "gmail" --target "longterm"
# Target: daily (memory/YYYY-MM-DD.md) or longterm (MEMORY.md)
# If scan severity >= threshold, content goes to memory/quarantine/
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
THRESHOLD="medium"  # quarantine at medium+ severity

# Parse args
SOURCE=""
TARGET="daily"
TEXT=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --source) SOURCE="$2"; shift 2 ;;
        --target) TARGET="$2"; shift 2 ;;
        --text) TEXT="$2"; shift 2 ;;
        --threshold) THRESHOLD="$2"; shift 2 ;;
        *) shift ;;
    esac
done

if [ -z "$SOURCE" ]; then
    echo '{"error": "Missing --source"}' >&2
    exit 2
fi

# Read from stdin if no --text
if [ -z "$TEXT" ]; then
    TEXT=$(cat)
fi

if [ -z "$TEXT" ]; then
    echo '{"error": "No text provided"}' >&2
    exit 2
fi

# Scan (capture stdout, ignore exit code since high severity = exit 1)
SCAN_RESULT=$(echo "$TEXT" | python3 "$SCRIPT_DIR/scan-content.py" 2>/dev/null; true)
if [ -z "$SCAN_RESULT" ]; then
    SCAN_RESULT='{"severity":"unknown","score":0,"findings":[],"sanitized":""}'
fi
SEVERITY=$(echo "$SCAN_RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('severity','unknown'))" 2>/dev/null || echo "unknown")
SCORE=$(echo "$SCAN_RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('score',0))" 2>/dev/null || echo "0")

# Severity ranking
sev_rank() {
    case $1 in
        none) echo 0 ;; low) echo 1 ;; medium) echo 2 ;; high) echo 3 ;; *) echo 99 ;;
    esac
}

SEV_NUM=$(sev_rank "$SEVERITY")
THRESH_NUM=$(sev_rank "$THRESHOLD")

TODAY=$(date -u +%Y-%m-%d)
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
SANITIZED=$(echo "$SCAN_RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('sanitized',''))" 2>/dev/null || echo "$TEXT")

if [ "$SEV_NUM" -ge "$THRESH_NUM" ] && [ "$SEV_NUM" -gt 0 ]; then
    # Quarantine
    QDIR="$WORKSPACE/memory/quarantine"
    mkdir -p "$QDIR"
    QFILE="$QDIR/$TODAY.md"

    cat >> "$QFILE" << QEOF

## Quarantined — $NOW
Source: $SOURCE
Scan: severity=$SEVERITY score=$SCORE
Findings: $(echo "$SCAN_RESULT" | python3 -c "import json,sys; f=json.load(sys.stdin).get('findings',[]); print(', '.join(x['pattern'] for x in f) if f else 'none')" 2>/dev/null)

Original text:
\`\`\`
$(echo "$TEXT" | head -20)
\`\`\`

Sanitized:
$SANITIZED

Status: **Review required before promoting to memory.**
QEOF

    echo "{\"status\":\"quarantined\",\"severity\":\"$SEVERITY\",\"score\":$SCORE,\"quarantine_to\":\"$QFILE\"}"
else
    # Accept — write to target
    if [ "$TARGET" = "longterm" ]; then
        OUTFILE="$WORKSPACE/MEMORY.md"
    else
        OUTFILE="$WORKSPACE/memory/$TODAY.md"
    fi

    echo "- [$NOW] (source: $SOURCE) $SANITIZED" >> "$OUTFILE"
    echo "{\"status\":\"accepted\",\"severity\":\"$SEVERITY\",\"score\":$SCORE,\"written_to\":\"$OUTFILE\"}"
fi
