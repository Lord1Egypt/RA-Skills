#!/bin/bash
# run-agent.sh - Execute coding agent in tmux, then trigger review
# Called by spawn-agent.sh, not directly
# Usage: ./run-agent.sh <task-id> <prompt-file> <log-file>

source "$(dirname "$0")/config.sh"

TASK_ID=$1
PROMPT_FILE=$2
LOG_FILE=$3

log() { echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG_FILE"; }

log "=== Agent Started: $TASK_ID (${SWARM_CODING_AGENT}) ==="

TASK_DESC=$(python3 -c "
import json
with open('$TASKS_FILE') as f:
    data = json.load(f)
tasks = data if isinstance(data, list) else data.get('tasks', [])
for t in tasks:
    if isinstance(t, dict) and t.get('id') == '$TASK_ID':
        print(t.get('description', '')[:80])
        break
" 2>/dev/null || echo "")

set_task_status() {
    python3 - "$TASKS_FILE" "$TASK_ID" "$1" <<'PYEOF'
import json, sys
tasks_file, task_id, status = sys.argv[1], sys.argv[2], sys.argv[3]
try:
    with open(tasks_file) as f:
        data = json.load(f)
    tasks = data if isinstance(data, list) else data.get("tasks", [])
    for t in tasks:
        if isinstance(t, dict) and t.get("id") == task_id:
            t["status"] = status
            break
    with open(tasks_file, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
except Exception as e:
    print(f"[tasks.json update failed: {e}]", file=sys.stderr)
PYEOF
}

has_new_commits() {
    local count
    count=$(git log --oneline origin/main..HEAD 2>/dev/null | wc -l | tr -d ' ')
    [ "${count:-0}" -gt 0 ]
}

# ─── Run coding agent ────────────────────────────────────────────────────────
PROMPT=$(cat "$PROMPT_FILE")
swarm_run_coding_agent "$PROMPT" "$LOG_FILE"
AGENT_EXIT=${PIPESTATUS[0]}

log "=== Agent Exited (code: $AGENT_EXIT) ==="

# ─── Check output ────────────────────────────────────────────────────────────
if ! has_new_commits; then
    log "⚠️ No new git commits — agent may have failed."
    set_task_status "no-output"

    cat > "${LOGS_DIR}/${TASK_ID}.notification" <<EOF
🚫 Task No-Output
Task: ${TASK_DESC}
Task ID: ${TASK_ID}
Agent (${SWARM_CODING_AGENT}) 未产出任何 git commit。
EOF
    [ -x "${SCRIPTS_DIR}/send-notifications.sh" ] && "${SCRIPTS_DIR}/send-notifications.sh" >/dev/null 2>&1 || true
    exit 1
fi

log "=== Triggering Review ==="
"$SCRIPTS_DIR/review-and-push.sh" "$TASK_ID" 2>&1 | tee -a "$LOG_FILE"
