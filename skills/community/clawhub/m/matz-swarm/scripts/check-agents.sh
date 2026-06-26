#!/bin/bash
# check-agents.sh - Cron monitor: detect done/stuck agents, auto-close merged MRs

source "$(dirname "$0")/config.sh"

LOG_FILE="${LOGS_DIR}/check-agents.log"
log() { echo "[$(date '+%H:%M:%S')] $1" >> "$LOG_FILE"; }

ACTIVE_TASKS=$(jq -c '[.tasks[] | select(.status == "starting" or .status == "running" or .status == "fixing" or .status == "selffix")]' "$TASKS_FILE" 2>/dev/null || echo "[]")
ACTIVE_COUNT=$(echo "$ACTIVE_TASKS" | jq 'length')
log "Check run. Active tasks: $ACTIVE_COUNT"

if [ "$ACTIVE_COUNT" -gt 0 ]; then
  echo "$ACTIVE_TASKS" | jq -c '.[]' | while read -r TASK; do
    TASK_ID=$(echo "$TASK" | jq -r '.id')
    SESSION=$(echo "$TASK" | jq -r '.tmuxSession')
    STATUS=$(echo "$TASK" | jq -r '.status')
    STARTED=$(echo "$TASK" | jq -r '.startedAt // 0')
    PROJECT=$(echo "$TASK" | jq -r '.project')
    DESC=$(echo "$TASK" | jq -r '.description')
    WORKTREE=$(echo "$TASK" | jq -r '.worktree')

    NOW_S=$(date +%s)
    STARTED_S=$(( STARTED / 1000 ))
    ELAPSED_MIN=$(( (NOW_S - STARTED_S) / 60 ))

    TMUX_ALIVE=0
    /usr/local/bin/tmux has-session -t "$SESSION" 2>/dev/null && TMUX_ALIVE=1

    if [ "$TMUX_ALIVE" -eq 0 ] && [ "$STATUS" = "running" ]; then
      cd "$WORKTREE" 2>/dev/null || continue
      HAS_COMMITS=$(git log --oneline origin/main..HEAD 2>/dev/null | wc -l | tr -d ' ')
      if [ "$HAS_COMMITS" -gt 0 ]; then
        log "Agent done with $HAS_COMMITS commits, triggering review..."
        jq --arg id "$TASK_ID" '.tasks |= map(if .id == $id then .status = "reviewing" else . end)' "$TASKS_FILE" > "${TASKS_FILE}.tmp" && mv "${TASKS_FILE}.tmp" "$TASKS_FILE"
        nohup "$SCRIPTS_DIR/review-and-push.sh" "$TASK_ID" >> "${LOGS_DIR}/${TASK_ID}.log" 2>&1 &
      else
        log "no-output: $TASK_ID"
        jq --arg id "$TASK_ID" '.tasks |= map(if .id == $id then .status = "no-output" else . end)' "$TASKS_FILE" > "${TASKS_FILE}.tmp" && mv "${TASKS_FILE}.tmp" "$TASKS_FILE"
        # Obsidian writeback: reset to ready so user can retrigger
        _NO_NOTE=$(echo "$TASK" | jq -r '.noteFile // ""')
        _NO_TNAME=$(echo "$TASK" | jq -r '.taskName // ""')
        if [ -n "$_NO_NOTE" ] && [ -f "$_NO_NOTE" ] && [ -n "$_NO_TNAME" ]; then
          sed -i '' "s/### ${_NO_TNAME}\nstatus: in_progress/### ${_NO_TNAME}\nstatus: ready/" "$_NO_NOTE" 2>/dev/null || \
          python3 -c "
import pathlib
p = pathlib.Path(r'''$_NO_NOTE''')
t = p.read_text('utf-8')
p.write_text(t.replace('### $_NO_TNAME\nstatus: in_progress', '### $_NO_TNAME\nstatus: ready'), 'utf-8')
" 2>/dev/null
          log "  Obsidian reset to ready: $_NO_TNAME"
        fi
        {
          echo "⚠️ TASK_NO_OUTPUT"
          echo "Project: $PROJECT"
          echo "Task: ${DESC:0:80}"
          echo "Task ID: $TASK_ID"
          echo "Summary: Agent ended with no commits"
          echo "Action: Check log and rerun"
          echo "Log: ${LOGS_DIR}/${TASK_ID}.log"
        } > "${LOGS_DIR}/${TASK_ID}.notification"
      fi
    fi

    if [ "$TMUX_ALIVE" -eq 1 ] && [ "$ELAPSED_MIN" -gt 60 ]; then
      TIMEOUT_FLAG="${LOGS_DIR}/${TASK_ID}.timeout-notified"
      if [ ! -f "$TIMEOUT_FLAG" ]; then
        touch "$TIMEOUT_FLAG"
        {
          echo "⏰ TASK_LONG_RUNNING"
          echo "Project: $PROJECT"
          echo "Task: ${DESC:0:80}"
          echo "Task ID: $TASK_ID"
          echo "Summary: Running ${ELAPSED_MIN} minutes"
          echo "Action: Inspect"
          echo "tmux: tmux attach -t $SESSION"
        } > "${LOGS_DIR}/${TASK_ID}-timeout.notification"
      fi
    fi
  done
fi

# ─── MR status check (ready_to_merge) ───────────────────────────────────────
PENDING_CI=$(jq -c '[.tasks[] | select(.status == "ready_to_merge")]' "$TASKS_FILE" 2>/dev/null || echo "[]")
echo "$PENDING_CI" | jq -c '.[]' | while read -r TASK; do
  TASK_ID=$(echo "$TASK" | jq -r '.id')
  PROJECT=$(echo "$TASK" | jq -r '.project')
  DESC=$(echo "$TASK" | jq -r '.description')
  WORKTREE=$(echo "$TASK" | jq -r '.worktree')
  MR_URL=$(echo "$TASK" | jq -r '.mrUrl // ""')
  TASK_NAME=$(echo "$TASK" | jq -r '.taskName // ""')
  NOTE_FILE=$(echo "$TASK" | jq -r '.noteFile // ""')
  TASK_KEY=$(echo "$TASK" | jq -r '.taskKey // ""')
  CI_FLAG="${LOGS_DIR}/${TASK_ID}.ci-checked"

  [ -z "$MR_URL" ] || [ ! -d "$WORKTREE" ] && continue
  cd "$WORKTREE" 2>/dev/null || continue

  MR_IID=$(swarm_mr_iid_from_url "$MR_URL")
  [ -z "$MR_IID" ] && continue

  MR_JSON=$(swarm_mr_view "$MR_IID")
  MR_STATE=$(swarm_mr_state "$MR_JSON")

  if [ "$MR_STATE" = "merged" ]; then
    jq --arg id "$TASK_ID" '.tasks |= map(if .id == $id then .status = "done" | .completedAt = (now * 1000 | floor) else . end)' \
      "$TASKS_FILE" > "${TASKS_FILE}.tmp" && mv "${TASKS_FILE}.tmp" "$TASKS_FILE"

    # Obsidian writeback
    if [ -n "$NOTE_FILE" ] && [ -f "$NOTE_FILE" ] && [ -n "$TASK_NAME" ]; then
      python3 - << PYEOF
import re
note_file = r'''$NOTE_FILE'''
task_name = r'''$TASK_NAME'''
task_desc = r'''$DESC'''
text = open(note_file,'r',encoding='utf-8').read()
parts = re.split(r'(?m)^###\s+', text)
if len(parts) <= 1:
    raise SystemExit(0)
new_parts = [parts[0]]
updated = False
for part in parts[1:]:
    lines = part.splitlines()
    if not lines:
        new_parts.append('### ' + part)
        continue
    name = lines[0].strip()
    block = '\n'.join(lines[1:])
    m_desc = re.search(r'(?m)^>\s*(.+)$', block)
    desc_line = (m_desc.group(1).strip() if m_desc else '')
    m_status = re.search(r'(?m)^status:\s*(\S+)\s*$', block)
    status = (m_status.group(1).strip().lower() if m_status else '')
    if (not updated) and name == task_name and desc_line == task_desc and status in ('in_progress','ready_to_merge'):
        block = re.sub(r'(?m)^status:\s*\S+\s*$', 'status: done', block, count=1)
        updated = True
    new_parts.append('### ' + lines[0] + ('\n' + block if block else ''))
if updated:
    open(note_file,'w',encoding='utf-8').write(''.join(new_parts))
PYEOF
    fi

    [ -x "${SCRIPTS_DIR}/sync-project-main.sh" ] && "${SCRIPTS_DIR}/sync-project-main.sh" "$PROJECT" >> "$LOG_FILE" 2>&1 || true

    {
      echo "✅ TASK_DONE"
      echo "Project: $PROJECT"
      echo "Task: ${DESC:0:80}"
      echo "Task ID: $TASK_ID"
      echo "Summary: MR merged, task closed"
      echo "MR: $MR_URL"
    } > "${LOGS_DIR}/${TASK_ID}-done.notification"
    continue
  fi

  # CI check (once)
  [ -f "$CI_FLAG" ] && continue
  CI_STATUS=$(echo "$MR_JSON" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('head_pipeline',{}).get('status',d.get('statusCheckRollup','unknown')))" 2>/dev/null || echo "unknown")
  log "CI status for $TASK_ID: $CI_STATUS"

  if [ "$CI_STATUS" = "failed" ] || [ "$CI_STATUS" = "FAILURE" ]; then
    {
      echo "⚠️ CI_FAILED"
      echo "Project: $PROJECT"
      echo "Task: ${DESC:0:80}"
      echo "Task ID: $TASK_ID"
      echo "MR: $MR_URL"
    } > "${LOGS_DIR}/${TASK_ID}-ci-fail.notification"
    touch "$CI_FLAG"
  elif [ "$CI_STATUS" = "success" ] || [ "$CI_STATUS" = "SUCCESS" ]; then
    {
      echo "✅ CI_PASSED"
      echo "Project: $PROJECT"
      echo "Task: ${DESC:0:80}"
      echo "Task ID: $TASK_ID"
      echo "MR: $MR_URL"
    } > "${LOGS_DIR}/${TASK_ID}-ci-pass.notification"
    touch "$CI_FLAG"
  fi
done

# Send all pending notifications
[ -x "${SCRIPTS_DIR}/send-notifications.sh" ] && "${SCRIPTS_DIR}/send-notifications.sh" >/dev/null 2>&1 || true
