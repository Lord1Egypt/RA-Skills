#!/bin/bash
# JobClaw Daily Runner
# Called by cron / OpenClaw scheduler every weekday morning.
#
# Usage:
#   ./run_daily.sh
#   ./run_daily.sh --mode coding
#   ./run_daily.sh --mode noncoding
#   ./run_daily.sh --mode all         (default)
#   ./run_daily.sh --dry-run

set -euo pipefail

# ── Resolve paths ─────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# JOBCLAW_DIR: where config.json and data/ live
# Default: ~/Documents/JobClaw  (can be overridden by env)
export JOBCLAW_DIR="${JOBCLAW_DIR:-$HOME/Documents/JobClaw}"

LOG_DIR="$JOBCLAW_DIR/logs"
LOG_FILE="$LOG_DIR/daily.log"
SUMMARY_FILE="$JOBCLAW_DIR/data/search_summary.json"

mkdir -p "$LOG_DIR" "$JOBCLAW_DIR/data"

# ── Parse args ────────────────────────────────────────────────────────────────
MODE="all"
DRY_RUN=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --mode) MODE="$2"; shift 2 ;;
        --dry-run) DRY_RUN="--dry-run"; shift ;;
        *) echo "Unknown arg: $1"; exit 1 ;;
    esac
done

# ── Logging ───────────────────────────────────────────────────────────────────
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "=== JobClaw Daily Search Started ==="
log "Mode: $MODE | Dry-run: ${DRY_RUN:-no} | JOBCLAW_DIR: $JOBCLAW_DIR"

# ── Check config ──────────────────────────────────────────────────────────────
if [ ! -f "$JOBCLAW_DIR/config.json" ]; then
    log "ERROR: config.json not found at $JOBCLAW_DIR. Run setup.py first."
    exit 1
fi

# ── Run search ────────────────────────────────────────────────────────────────
log "Starting search (mode=$MODE)..."

python3 "$SCRIPT_DIR/search.py" \
    --mode "$MODE" \
    $DRY_RUN \
    2>&1 | tee -a "$LOG_FILE"

SEARCH_EXIT=${PIPESTATUS[0]}

if [ "$SEARCH_EXIT" -ne 0 ]; then
    log "WARNING: search.py exited with code $SEARCH_EXIT"
fi

# ── Read results ──────────────────────────────────────────────────────────────
CODING_ADDED=0
NONCODING_ADDED=0
CODING_TOP="None"
NONCODING_TOP="None"

if [ -f "$SUMMARY_FILE" ]; then
    CODING_ADDED=$(python3 -c "import json; d=json.load(open('$SUMMARY_FILE')); print(d.get('coding',{}).get('added',0))" 2>/dev/null || echo "0")
    NONCODING_ADDED=$(python3 -c "import json; d=json.load(open('$SUMMARY_FILE')); print(d.get('noncoding',{}).get('added',0))" 2>/dev/null || echo "0")
    CODING_TOP=$(python3 -c "import json; d=json.load(open('$SUMMARY_FILE')); print(d.get('coding',{}).get('top','None'))" 2>/dev/null || echo "None")
    NONCODING_TOP=$(python3 -c "import json; d=json.load(open('$SUMMARY_FILE')); print(d.get('noncoding',{}).get('top','None'))" 2>/dev/null || echo "None")
fi

TOTAL_ADDED=$((CODING_ADDED + NONCODING_ADDED))

# ── Get tracker stats ─────────────────────────────────────────────────────────
TOTAL_JOBS=$(python3 -c "
import sys; sys.path.insert(0, '$SCRIPT_DIR')
from tracker import JobTracker
t = JobTracker()
s = t.stats()
print(s['total'])
" 2>/dev/null || echo "?")

NEW_TODAY=$(python3 -c "
import sys; sys.path.insert(0, '$SCRIPT_DIR')
from tracker import JobTracker
t = JobTracker()
s = t.stats()
print(s['new_today'])
" 2>/dev/null || echo "0")

log "Results: coding=$CODING_ADDED, noncoding=$NONCODING_ADDED, total=$TOTAL_ADDED"
log "Tracker: total=$TOTAL_JOBS, new_today=$NEW_TODAY"

# ── Send notification ─────────────────────────────────────────────────────────
log "Sending notification..."

python3 "$SCRIPT_DIR/notify.py" <<EOF 2>&1 | tee -a "$LOG_FILE" || true
# (inline invocation via module)
EOF

# Use module call instead
python3 - <<PYEOF 2>&1 | tee -a "$LOG_FILE" || true
import sys, json, os
sys.path.insert(0, '$SCRIPT_DIR')
os.environ['JOBCLAW_DIR'] = '$JOBCLAW_DIR'
from notify import send_summary

with open('$JOBCLAW_DIR/config.json') as f:
    config = json.load(f)

send_summary(
    config=config,
    total_jobs=$TOTAL_JOBS if '$TOTAL_JOBS' != '?' else 0,
    new_today=$NEW_TODAY,
    coding_added=$CODING_ADDED,
    noncoding_added=$NONCODING_ADDED,
    top_coding='$CODING_TOP',
    top_noncoding='$NONCODING_TOP',
    archived=${ARCHIVED_COUNT:-0},
)
PYEOF

# ── Auto-archive expired jobs ──────────────────────────────────────────────
log "Running auto-archive..."
ARCHIVE_RESULT=$(python3 "$SCRIPT_DIR/archiver.py" --commit 2>&1 | tee -a "$LOG_FILE")
ARCHIVED_COUNT=$(echo "$ARCHIVE_RESULT" | grep -oP "Archived: \K[0-9]+" || echo "0")
log "Auto-archived: ${ARCHIVED_COUNT:-0} expired jobs"

log "=== JobClaw Daily Search Complete ==="
log "Summary: +$TOTAL_ADDED jobs today (coding: $CODING_ADDED, noncoding: $NONCODING_ADDED), archived: ${ARCHIVED_COUNT:-0}"
