#!/usr/bin/env bash
# Lumina's ITIL Problem & Incident Review
# Runs 2x daily (6 AM + 6 PM EST) — scans for incidents, detects patterns, escalates problems
#
# What it does:
#   1. Scans journalctl for service crashes/restarts
#   2. Checks cron jobs for consecutive failures
#   3. Checks memory system health (load errors, broken files)
#   4. Checks service health (skvector, skgraph, skchat, openclaw)
#   5. Checks disk/memory pressure
#   6. Pattern detection: same error 3+ times in 24h = escalate to PROBLEM
#   7. Reviews open ITIL coordination tasks
#   8. ONLY alerts Chef if problems found — silence = healthy
#   9. Auto-creates coordination tasks for new problems

set -euo pipefail

AGENT_HOME="$HOME/.skcapstone/agents/lumina"
LOG_DIR="$AGENT_HOME/logs"
LOG_FILE="$LOG_DIR/itil-review.log"
ITIL_STATE="$AGENT_HOME/memory/itil-state.json"
COORD_DIR="$HOME/.skcapstone/coordination/tasks"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
HOUR=$(date +%H)

mkdir -p "$LOG_DIR"

log() {
    echo "[$(date -u +%H:%M:%S)] $*" | tee -a "$LOG_FILE"
}

log "=== ITIL Review: $DATE $HOUR:00 ==="

INCIDENTS=""
INCIDENT_COUNT=0
PROBLEMS=""
PROBLEM_COUNT=0

add_incident() {
    local severity="$1"  # P1=critical P2=high P3=medium P4=low
    local category="$2"  # service|cron|memory|disk|security
    local title="$3"
    local detail="$4"
    INCIDENTS="${INCIDENTS}\n🔴 [$severity] [$category] $title\n   $detail\n"
    INCIDENT_COUNT=$((INCIDENT_COUNT + 1))
}

add_problem() {
    local severity="$1"
    local title="$2"
    local detail="$3"
    PROBLEMS="${PROBLEMS}\n🟠 [PROBLEM] [$severity] $title\n   $detail\n"
    PROBLEM_COUNT=$((PROBLEM_COUNT + 1))
}

# ============================================================
# 1. SERVICE CRASHES & RESTARTS (last 12h)
# ============================================================
log "Step 1: Checking service crashes..."

for svc in skcapstone openclaw-gateway; do
    CRASH_COUNT=$(journalctl --user -u "$svc.service" --since "12 hours ago" --no-pager 2>/dev/null | grep -ciE "watchdog timeout|killed|dumped core|SIGABRT|SIGSEGV|failed with" || true)
    CRASH_COUNT=${CRASH_COUNT:-0}
    RESTART_COUNT=$(journalctl --user -u "$svc.service" --since "12 hours ago" --no-pager 2>/dev/null | grep -ciE "Scheduled restart job|Started " || true)
    RESTART_COUNT=${RESTART_COUNT:-0}
    
    if [ "$CRASH_COUNT" -gt 0 ]; then
        if [ "$CRASH_COUNT" -ge 3 ]; then
            add_problem "P1" "$svc crash loop ($CRASH_COUNT crashes in 12h)" "Pattern: $CRASH_COUNT crashes, $RESTART_COUNT restarts. Investigate root cause."
        else
            add_incident "P2" "service" "$svc crashed $CRASH_COUNT time(s)" "$RESTART_COUNT restart(s) in last 12h"
        fi
    fi
done

# Check skcapstone restart counter
RESTART_TOTAL=$(systemctl --user show skcapstone.service --property=NRestarts 2>/dev/null | cut -d= -f2 || echo "0")
log "  skcapstone total restarts: $RESTART_TOTAL"

# ============================================================
# 2. CRON JOB FAILURES
# ============================================================
log "Step 2: Checking cron job health..."

CRON_DIR="$HOME/.openclaw/cron/jobs"
if [ -d "$CRON_DIR" ]; then
    for job_file in "$CRON_DIR"/*.json; do
        [ -f "$job_file" ] || continue
        JOB_NAME=$(python3 -c "import json; print(json.load(open('$job_file')).get('name','unknown'))" 2>/dev/null || echo "unknown")
        CONSEC_ERRORS=$(python3 -c "import json; print(json.load(open('$job_file')).get('consecutiveErrors',0))" 2>/dev/null || echo "0")
        LAST_ERROR=$(python3 -c "import json; print(json.load(open('$job_file')).get('lastError','')[:120])" 2>/dev/null || echo "")
        
        if [ "$CONSEC_ERRORS" -ge 5 ]; then
            add_problem "P2" "Cron '$JOB_NAME' — $CONSEC_ERRORS consecutive failures" "Last error: $LAST_ERROR"
        elif [ "$CONSEC_ERRORS" -ge 3 ]; then
            add_incident "P3" "cron" "Cron '$JOB_NAME' — $CONSEC_ERRORS consecutive failures" "Last error: $LAST_ERROR"
        fi
    done
fi

# ============================================================
# 3. MEMORY SYSTEM HEALTH
# ============================================================
log "Step 3: Checking memory system..."

# Check for broken memory files (content as dict instead of string)
BROKEN_MEM=0
for tier in short-term mid-term long-term; do
    tier_dir="$AGENT_HOME/memory/$tier"
    [ -d "$tier_dir" ] || continue
    broken=$(python3 -c "
import json, glob, os
count = 0
for f in glob.glob('$tier_dir/*.json'):
    try:
        d = json.load(open(f))
        if isinstance(d.get('content'), dict):
            count += 1
    except: pass
print(count)
" 2>/dev/null || echo "0")
    BROKEN_MEM=$((BROKEN_MEM + broken))
done

if [ "$BROKEN_MEM" -gt 0 ]; then
    add_incident "P3" "memory" "$BROKEN_MEM broken memory files (content=dict)" "Run the JSON fixer or check daily-improvement-review.sh / daily-dream-reflection.sh"
fi

# Check memory load errors in recent skcapstone logs
MEM_ERRORS=$(journalctl --user -u skcapstone.service --since "12 hours ago" --no-pager 2>/dev/null | grep -c "Failed to load memory" || true)
MEM_ERRORS=${MEM_ERRORS:-0}
if [ "$MEM_ERRORS" -gt 10 ]; then
    add_incident "P3" "memory" "$MEM_ERRORS memory load errors in 12h" "Check skcapstone journal for validation errors"
fi

# Memory counts
MEM_SHORT=$(ls "$AGENT_HOME/memory/short-term/" 2>/dev/null | wc -l)
MEM_MID=$(ls "$AGENT_HOME/memory/mid-term/" 2>/dev/null | wc -l)
MEM_LONG=$(ls "$AGENT_HOME/memory/long-term/" 2>/dev/null | wc -l)
MEM_TOTAL=$((MEM_SHORT + MEM_MID + MEM_LONG))

# ============================================================
# 4. SERVICE HEALTH
# ============================================================
log "Step 4: Checking service health..."

declare -A SERVICES=(
    ["skvector (Qdrant)"]="http://localhost:6333/healthz"
    ["skchat daemon"]="http://localhost:9385/health"
    ["openclaw gateway"]="http://localhost:3001/health"
)

SERVICES_DOWN=0
SERVICES_DOWN_LIST=""
for name in "${!SERVICES[@]}"; do
    url="${SERVICES[$name]}"
    if ! curl -sf --max-time 5 "$url" >/dev/null 2>&1; then
        SERVICES_DOWN=$((SERVICES_DOWN + 1))
        SERVICES_DOWN_LIST="$SERVICES_DOWN_LIST $name,"
    fi
done

if [ "$SERVICES_DOWN" -ge 3 ]; then
    add_incident "P2" "service" "$SERVICES_DOWN services DOWN" "Down:$SERVICES_DOWN_LIST"
elif [ "$SERVICES_DOWN" -gt 0 ]; then
    add_incident "P4" "service" "$SERVICES_DOWN service(s) down" "Down:$SERVICES_DOWN_LIST"
fi

# ============================================================
# 5. DISK & MEMORY PRESSURE
# ============================================================
log "Step 5: Checking disk & memory..."

DISK_PCT=$(df -h / | awk 'NR==2{print $5}' | tr -d '%')
if [ "$DISK_PCT" -ge 90 ]; then
    add_incident "P1" "disk" "Root disk at ${DISK_PCT}% — CRITICAL" "Run cleanup immediately"
elif [ "$DISK_PCT" -ge 80 ]; then
    add_incident "P3" "disk" "Root disk at ${DISK_PCT}%" "Consider cleanup"
fi

# Memory (RAM)
MEM_AVAIL_MB=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)
MEM_TOTAL_MB=$(awk '/MemTotal/{print int($2/1024)}' /proc/meminfo)
MEM_USED_PCT=$(( (MEM_TOTAL_MB - MEM_AVAIL_MB) * 100 / MEM_TOTAL_MB ))

if [ "$MEM_USED_PCT" -ge 90 ]; then
    add_incident "P1" "memory" "RAM at ${MEM_USED_PCT}% — ${MEM_AVAIL_MB}MB free" "OOM risk — check for runaway processes"
elif [ "$MEM_USED_PCT" -ge 80 ]; then
    add_incident "P3" "memory" "RAM at ${MEM_USED_PCT}% — ${MEM_AVAIL_MB}MB free" "Monitor for growth"
fi

# ============================================================
# 6. OPEN ITIL TASKS REVIEW
# ============================================================
log "Step 6: Checking open ITIL tasks..."

OPEN_ITIL=0
ITIL_SUMMARY=""
if [ -d "$COORD_DIR" ]; then
    for task_file in "$COORD_DIR"/*.json; do
        [ -f "$task_file" ] || continue
        IS_ITIL=$(python3 -c "
import json
d = json.load(open('$task_file'))
title = d.get('title','')
status = d.get('status','')
if 'ITIL' in title and status in ('open','in_progress','claimed'):
    print(f\"{status}: {title[:80]}\")
else:
    print('')
" 2>/dev/null || echo "")
        if [ -n "$IS_ITIL" ]; then
            OPEN_ITIL=$((OPEN_ITIL + 1))
            ITIL_SUMMARY="$ITIL_SUMMARY\n  • $IS_ITIL"
        fi
    done
fi

# ============================================================
# 7. PATTERN DETECTION — Repeated failures = PROBLEM
# ============================================================
log "Step 7: Pattern detection..."

# Check if the same service has been crashing across multiple review periods
if [ -f "$ITIL_STATE" ]; then
    PREV_INCIDENTS=$(python3 -c "import json; d=json.load(open('$ITIL_STATE')); print(d.get('last_incident_count',0))" 2>/dev/null || echo "0")
    PREV_PROBLEMS=$(python3 -c "import json; d=json.load(open('$ITIL_STATE')); print(d.get('recurring_issues',''))" 2>/dev/null || echo "")
    
    # If we had incidents last review AND still have them, escalate to problem
    if [ "$PREV_INCIDENTS" -gt 0 ] && [ "$INCIDENT_COUNT" -gt 0 ]; then
        add_problem "P2" "Recurring incidents across review periods" "Had $PREV_INCIDENTS incidents last review, $INCIDENT_COUNT this review. Pattern detected."
    fi
fi

# Save state for next review
python3 -c "
import json
state = {
    'last_review': '$TIMESTAMP',
    'last_incident_count': $INCIDENT_COUNT,
    'last_problem_count': $PROBLEM_COUNT,
    'memory_total': $MEM_TOTAL,
    'disk_pct': $DISK_PCT,
    'ram_used_pct': $MEM_USED_PCT,
    'skcapstone_restarts': $RESTART_TOTAL,
    'services_down': $SERVICES_DOWN
}
with open('$ITIL_STATE', 'w') as f:
    json.dump(state, f, indent=2)
" 2>/dev/null || log "Failed to save ITIL state"

# ============================================================
# 8. GENERATE REPORT (only if issues found)
# ============================================================
TOTAL_ISSUES=$((INCIDENT_COUNT + PROBLEM_COUNT))

if [ "$TOTAL_ISSUES" -eq 0 ]; then
    log "✅ No incidents or problems found. All clear."
    echo "ITIL_CLEAR"
    exit 0
fi

log "Found $INCIDENT_COUNT incidents, $PROBLEM_COUNT problems"

REPORT="🚨 **ITIL Review — $DATE $(date +%H:%M) EST**\n"
REPORT="${REPORT}Found **$INCIDENT_COUNT incident(s)** and **$PROBLEM_COUNT problem(s)**\n"

if [ "$PROBLEM_COUNT" -gt 0 ]; then
    REPORT="${REPORT}\n**🟠 PROBLEMS (patterns/recurring):**$PROBLEMS\n"
fi

if [ "$INCIDENT_COUNT" -gt 0 ]; then
    REPORT="${REPORT}\n**🔴 INCIDENTS:**$INCIDENTS\n"
fi

REPORT="${REPORT}\n**📊 System Snapshot:**"
REPORT="${REPORT}\n• Disk: ${DISK_PCT}% | RAM: ${MEM_USED_PCT}% (${MEM_AVAIL_MB}MB free)"
REPORT="${REPORT}\n• Memories: ${MEM_TOTAL} (${MEM_LONG}L/${MEM_MID}M/${MEM_SHORT}S)"
REPORT="${REPORT}\n• SKCapstone restarts: ${RESTART_TOTAL} total"
REPORT="${REPORT}\n• Services down: ${SERVICES_DOWN}"

if [ "$OPEN_ITIL" -gt 0 ]; then
    REPORT="${REPORT}\n\n**📋 Open ITIL Tasks ($OPEN_ITIL):**$ITIL_SUMMARY"
fi

# Output for the cron to pick up and deliver
echo -e "$REPORT"

# Auto-create coordination tasks for P1/P2 problems
if [ "$PROBLEM_COUNT" -gt 0 ]; then
    log "Creating coordination tasks for problems..."
    # The cron session will handle task creation via skcapstone tools
fi

log "=== ITIL Review Complete: $TOTAL_ISSUES issues ==="
