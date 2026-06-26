#!/bin/bash
# ==========================================
# test_kanban_runner.sh
# Tests the kanban skill via the skill test runner
# ==========================================

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$DIR/test_kanban_runner.log"

echo "[$(date)] Starting Kanban Test Runner..." | tee "$LOG_FILE"
bash "$DIR/skill_test_runner.sh" "skill_util/kanban" "看看板" 2>&1 | tee -a "$LOG_FILE"

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo "[$(date)] Kanban Test Runner Completed Successfully." | tee -a "$LOG_FILE"
    exit 0
else
    echo "[$(date)] Kanban Test Runner Failed." | tee -a "$LOG_FILE"
    exit 1
fi
