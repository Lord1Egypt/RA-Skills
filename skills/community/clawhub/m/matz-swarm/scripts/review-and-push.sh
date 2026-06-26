#!/bin/bash
# review-and-push.sh - Review code, graded handling, push, create MR
# Usage: ./review-and-push.sh <task-id>

source "$(dirname "$0")/config.sh"

TASK_ID=$1
[ -z "$TASK_ID" ] && echo "Usage: $0 <task-id>" && exit 1

LOG_FILE="${LOGS_DIR}/${TASK_ID}-review.log"
log() { echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG_FILE"; }

# Read task info
TASK=$(jq -r --arg id "$TASK_ID" '.tasks[] | select(.id == $id)' "$TASKS_FILE")
if [ -z "$TASK" ]; then
    log "❌ Task not found: $TASK_ID"
    exit 1
fi

PROJECT=$(echo "$TASK" | jq -r '.project')
WORKTREE=$(echo "$TASK" | jq -r '.worktree')
BRANCH=$(echo "$TASK" | jq -r '.branch')
DESC=$(echo "$TASK" | jq -r '.description')
RETRY=$(echo "$TASK" | jq -r '.retryCount // 0')

notify() {
    local event="$1" summary="$2" action="$3" extra="$4"
    {
        echo "${event}"
        echo "Project: ${PROJECT}"
        echo "Task: ${DESC:0:80}"
        echo "Task ID: ${TASK_ID}"
        echo "Branch: ${BRANCH}"
        echo "Summary: ${summary}"
        echo "Action: ${action}"
        [ -n "$extra" ] && echo "$extra"
    } > "${LOGS_DIR}/${TASK_ID}.notification"
    [ -x "${SCRIPTS_DIR}/send-notifications.sh" ] && "${SCRIPTS_DIR}/send-notifications.sh" >/dev/null 2>&1 || true
}

log "=== Review & Push: $TASK_ID ==="
log "Project: $PROJECT | Branch: $BRANCH | Reviewer: $SWARM_REVIEW_AGENT"

if [ ! -d "$WORKTREE" ]; then
    log "❌ Worktree not found: $WORKTREE"
    notify "❌ REVIEW_BLOCKED" "Worktree not found" "Check worktree path" "Worktree: $WORKTREE"
    exit 1
fi

cd "$WORKTREE"

# Detect changes
CHANGED_FILES=$(git diff --name-only origin/main..HEAD 2>/dev/null || git diff --name-only HEAD~1 2>/dev/null || true)
FILE_COUNT=$(printf "%s\n" "$CHANGED_FILES" | sed '/^$/d' | wc -l | tr -d ' ')
log "Changed files: $FILE_COUNT"

# Docs-only detection
IS_DOCS_ONLY=1
while IFS= read -r f; do
    [ -z "$f" ] && continue
    case "$f" in
        *.md|*.txt|docs/*|README*) ;;
        *) IS_DOCS_ONLY=0; break ;;
    esac
done << EOF
$CHANGED_FILES
EOF

[ "$IS_DOCS_ONLY" -eq 1 ] && log "Change type: DOCS_ONLY" || log "Change type: CODE_CHANGE"

# ─── Review ──────────────────────────────────────────────────────────────────
log "--- Review (${SWARM_REVIEW_AGENT}) ---"

REVIEW_PROMPT_FILE="${LOGS_DIR}/${TASK_ID}-review.prompt"
{
    echo "You are doing a practical, low-false-positive code review for task: ${TASK_ID}"
    echo "Project: ${PROJECT}"
    echo "Task description: ${DESC}"
    echo ""
    echo "Changed files:"
    echo "${CHANGED_FILES}"
    echo ""
    echo "Rules to reduce false positives:"
    echo "1) CRITICAL/HIGH must include concrete evidence and reproduction path."
    echo "2) For docs-only changes, do NOT output CRITICAL/HIGH unless there is a severe factual/security/legal risk."
    echo "3) Prefer MEDIUM/LOW for wording, style, or non-breaking improvements."
    echo ""
    echo "Output each issue in EXACT format:"
    echo "[SEVERITY: CRITICAL|HIGH|MEDIUM|LOW] file:line - issue. Fix: suggestion"
    echo ""
    echo "Then output one line: REVIEW_RESULT: PASS or REVIEW_RESULT: FAIL"
} > "$REVIEW_PROMPT_FILE"

CODEX_EXIT=0
REVIEW_OUTPUT=$(cd "$WORKTREE" && swarm_run_review "$REVIEW_PROMPT_FILE") || CODEX_EXIT=$?

if [ "$CODEX_EXIT" -ne 0 ] || echo "$REVIEW_OUTPUT" | grep -q "REVIEW_ERROR"; then
    log "❌ Review failed"
    jq --arg id "$TASK_ID" '.tasks |= map(if .id == $id then .status = "review-error" else . end)' \
       "$TASKS_FILE" > "${TASKS_FILE}.tmp" && mv "${TASKS_FILE}.tmp" "$TASKS_FILE"
    notify "❌ REVIEW_BLOCKED" "Review tool failed" "Check logs" "Log: $LOG_FILE"
    exit 1
fi

echo "$REVIEW_OUTPUT" >> "$LOG_FILE"

# Parse results
REVIEW_RESULT=$(echo "$REVIEW_OUTPUT" | grep "^REVIEW_RESULT:" | tail -1 | awk '{print $2}')
CRITICAL_COUNT=$(( $(echo "$REVIEW_OUTPUT" | grep -c "\[SEVERITY: CRITICAL\]" || true) + $(echo "$REVIEW_OUTPUT" | grep -Eci "\[P0\]" || true) ))
HIGH_COUNT=$(( $(echo "$REVIEW_OUTPUT" | grep -c "\[SEVERITY: HIGH\]" || true) + $(echo "$REVIEW_OUTPUT" | grep -Eci "\[P1\]" || true) ))
MEDIUM_COUNT=$(( $(echo "$REVIEW_OUTPUT" | grep -c "\[SEVERITY: MEDIUM\]" || true) + $(echo "$REVIEW_OUTPUT" | grep -Eci "\[P2\]" || true) ))
LOW_COUNT=$(( $(echo "$REVIEW_OUTPUT" | grep -c "\[SEVERITY: LOW\]" || true) + $(echo "$REVIEW_OUTPUT" | grep -Eci "\[P3\]" || true) ))

# Docs-only guardrail
if [ "$IS_DOCS_ONLY" -eq 1 ] && { [ "$CRITICAL_COUNT" -gt 0 ] || [ "$HIGH_COUNT" -gt 0 ]; }; then
    log "DOCS_ONLY guardrail: downgrade CRITICAL/HIGH to MEDIUM"
    MEDIUM_COUNT=$((MEDIUM_COUNT + CRITICAL_COUNT + HIGH_COUNT))
    CRITICAL_COUNT=0
    HIGH_COUNT=0
fi

[ -z "$REVIEW_RESULT" ] && { [ "$CRITICAL_COUNT" -gt 0 ] || [ "$HIGH_COUNT" -gt 0 ]; } && REVIEW_RESULT="FAIL"
[ -z "$REVIEW_RESULT" ] && REVIEW_RESULT="PASS"

log "Review: $REVIEW_RESULT (C:$CRITICAL_COUNT H:$HIGH_COUNT M:$MEDIUM_COUNT L:$LOW_COUNT)"

jq --arg id "$TASK_ID" --arg result "$REVIEW_RESULT" \
   --argjson c "$CRITICAL_COUNT" --argjson h "$HIGH_COUNT" --argjson m "$MEDIUM_COUNT" --argjson l "$LOW_COUNT" \
   '.tasks |= map(if .id == $id then .review = {result: $result, critical: $c, high: $h, medium: $m, low: $l} else . end)' \
   "$TASKS_FILE" > "${TASKS_FILE}.tmp" && mv "${TASKS_FILE}.tmp" "$TASKS_FILE"

# ─── Graded handling ─────────────────────────────────────────────────────────
if [ "$CRITICAL_COUNT" -gt 0 ] || [ "$HIGH_COUNT" -gt 0 ]; then
    MAX_RETRIES=2
    if [ "${RETRY:-0}" -ge "$MAX_RETRIES" ]; then
        log "❌ Max retries reached."
        jq --arg id "$TASK_ID" '.tasks |= map(if .id == $id then .status = "needs-manual-fix" else . end)' \
           "$TASKS_FILE" > "${TASKS_FILE}.tmp" && mv "${TASKS_FILE}.tmp" "$TASKS_FILE"
        notify "❌ REVIEW_BLOCKED" "Max retries ($MAX_RETRIES)" "Manual fix needed" "Log: $LOG_FILE"
        exit 1
    fi

    ISSUES=$(echo "$REVIEW_OUTPUT" | grep -E "\[SEVERITY: (CRITICAL|HIGH)\]|\[P0\]|\[P1\]" || echo "See log: $LOG_FILE")
    FIX_PROMPT_FILE="${LOGS_DIR}/${TASK_ID}-fix.prompt"
    {
        echo "Fix ONLY these CRITICAL/HIGH review issues for task ${TASK_ID}:"
        echo "$ISSUES"
        echo "Do not change unrelated code."
        echo "Commit message: fix: address review issues for ${TASK_ID}"
    } > "$FIX_PROMPT_FILE"

    jq --arg id "$TASK_ID" --argjson r "$((RETRY+1))" \
       '.tasks |= map(if .id == $id then .retryCount = $r | .status = "fixing" else . end)' \
       "$TASKS_FILE" > "${TASKS_FILE}.tmp" && mv "${TASKS_FILE}.tmp" "$TASKS_FILE"

    notify "⚠️ REVIEW_FAILED_RETRYING" "Critical issues found, auto-fixing" "Waiting for retry" "Retry: $((RETRY+1))/${MAX_RETRIES}"

    FIX_SESSION="fix-${TASK_ID}"
    FIX_PROMPT=$(cat "$FIX_PROMPT_FILE")
    /usr/local/bin/tmux new-session -d -s "$FIX_SESSION" -c "$WORKTREE" \
        bash -c "source '${SCRIPTS_DIR}/config.sh' && swarm_run_coding_agent \"\$1\" '${LOG_FILE}'" -- "$FIX_PROMPT"

    while /usr/local/bin/tmux has-session -t "$FIX_SESSION" 2>/dev/null; do sleep 10; done
    log "Fix done, re-running review..."
    exec "$0" "$TASK_ID"
fi

# MEDIUM self-fix (non-blocking)
if [ "$MEDIUM_COUNT" -gt 0 ] && [ "$IS_DOCS_ONLY" -eq 0 ]; then
    log "--- MEDIUM self-fix ---"
    MEDIUM_ISSUES=$(echo "$REVIEW_OUTPUT" | grep -E "\[SEVERITY: MEDIUM\]|\[P2\]" || echo "")
    MEDIUM_PROMPT_FILE="${LOGS_DIR}/${TASK_ID}-medium.prompt"
    {
        echo "Address these MEDIUM issues if low-cost and safe:"
        echo "$MEDIUM_ISSUES"
        echo "Skip overengineering."
        echo "Commit as: refactor: address medium review issues for ${TASK_ID}"
    } > "$MEDIUM_PROMPT_FILE"

    MEDIUM_SESSION="selffix-${TASK_ID}"
    MEDIUM_PROMPT=$(cat "$MEDIUM_PROMPT_FILE")
    /usr/local/bin/tmux new-session -d -s "$MEDIUM_SESSION" -c "$WORKTREE" \
        bash -c "source '${SCRIPTS_DIR}/config.sh' && swarm_run_coding_agent \"\$1\" '${LOG_FILE}'" -- "$MEDIUM_PROMPT"

    while /usr/local/bin/tmux has-session -t "$MEDIUM_SESSION" 2>/dev/null; do sleep 5; done
    log "Medium issues addressed"
fi

LOW_NOTES=$(echo "$REVIEW_OUTPUT" | grep -E "\[SEVERITY: LOW\]|\[P3\]" | head -10 || echo "")

# ─── Push & MR ───────────────────────────────────────────────────────────────
log "--- Push & MR ---"
cd "$WORKTREE"

if ! git diff --quiet HEAD 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
    git add -A
    git commit -m "chore: finalize for ${TASK_ID}" || true
fi

git fetch origin main >> "$LOG_FILE" 2>&1
BEHIND=$(git rev-list HEAD..origin/main --count 2>/dev/null || echo "0")
if [ "$BEHIND" -gt 0 ]; then
    log "Branch is $BEHIND commits behind main, rebasing..."
    if ! git rebase origin/main >> "$LOG_FILE" 2>&1; then
        log "❌ Rebase conflict"
        git rebase --abort 2>/dev/null || true
        jq --arg id "$TASK_ID" '.tasks |= map(if .id == $id then .status = "needs-manual-fix" else . end)' \
           "$TASKS_FILE" > "${TASKS_FILE}.tmp" && mv "${TASKS_FILE}.tmp" "$TASKS_FILE"
        notify "⚠️ REVIEW_BLOCKED" "Rebase conflict with main" "Manual fix needed" "Log: $LOG_FILE"
        exit 1
    fi
fi

log "Pushing $BRANCH..."
git push -u origin "$BRANCH" 2>&1 | tee -a "$LOG_FILE"

# Create MR
MR_DESC_FILE="${LOGS_DIR}/${TASK_ID}-mr-desc.txt"
{
    echo "## ${DESC}"
    echo ""
    echo "**Task ID:** ${TASK_ID}  **Project:** ${PROJECT}"
    echo ""
    echo "### Review Summary"
    echo "- Review (${SWARM_REVIEW_AGENT}): ${REVIEW_RESULT}"
    echo "- CRITICAL: ${CRITICAL_COUNT} | HIGH: ${HIGH_COUNT} | MEDIUM: ${MEDIUM_COUNT} | LOW: ${LOW_COUNT}"
    [ -n "$LOW_NOTES" ] && { echo ""; echo "### Low Priority Notes"; echo "$LOW_NOTES"; }
    echo ""; echo "---"; echo "*Auto-generated by Agent Swarm*"
} > "$MR_DESC_FILE"

MR_URL=""
cd "$WORKTREE"
# Sanitize MR title: single line, no special chars, max 80 chars
MR_TITLE=$(echo "$DESC" | head -1 | tr -d '\r\n' | sed 's/[<>\"'\''`\\]//g; s/  */ /g; s/^ *//; s/ *$//' | cut -c1-80)
[ -z "$MR_TITLE" ] && MR_TITLE="Task ${TASK_ID}"
log "Creating MR from $(pwd) for branch $BRANCH"
MR_OUT=$(swarm_mr_create "$MR_TITLE" "$MR_DESC_FILE" "$BRANCH" 2>&1) || true
log "MR create output: $(echo "$MR_OUT" | head -5)"
MR_URL=$(swarm_mr_url "$MR_OUT")

# Fallback: query by branch
if [ -z "$MR_URL" ]; then
    MR_URL=$(swarm_mr_list_by_branch "$BRANCH" | \
        python3 -c 'import sys,json; a=json.load(sys.stdin) if sys.stdin.readable() else []; print((a[0].get("web_url") or a[0].get("webUrl") or a[0].get("url") or "") if a else "")' \
        2>/dev/null || echo "")
fi

log "MR: ${MR_URL:-see git provider}"

jq --arg id "$TASK_ID" --arg url "$MR_URL" \
   '.tasks |= map(if .id == $id then .status = "ready_to_merge" | .mrUrl = $url | .completedAt = (now * 1000 | floor) else . end)' \
   "$TASKS_FILE" > "${TASKS_FILE}.tmp" && mv "${TASKS_FILE}.tmp" "$TASKS_FILE"

notify "✅ PR_READY" "PR ready (reviewed)" "Review and merge" "MR: ${MR_URL:-N/A} | Review C/H/M/L: ${CRITICAL_COUNT}/${HIGH_COUNT}/${MEDIUM_COUNT}/${LOW_COUNT}"
log "✅ Done! Task $TASK_ID ready to merge."
