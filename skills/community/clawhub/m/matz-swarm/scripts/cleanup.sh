#!/bin/bash
# cleanup.sh - 每日清理：归档旧任务、清理孤立 worktree
# 由每日 cron 调用

SWARM_DIR="${HOME}/agent-swarm"
TASKS_FILE="${SWARM_DIR}/tasks.json"
LOGS_DIR="${SWARM_DIR}/logs"
WORKTREE_BASE="${HOME}/GitLab/worktrees"

log() { echo "[$(date '+%H:%M:%S')] $1" >> "${LOGS_DIR}/cleanup.log"; }

log "=== Daily cleanup ==="

# 归档 30 天前的完成任务（macOS 兼容毫秒）
NOW_MS=$(python3 - <<'PY'
import time
print(int(time.time()*1000))
PY
)
THRESHOLD_MS=$((NOW_MS - 30 * 24 * 3600 * 1000))

ARCHIVED=$(jq --argjson t "$THRESHOLD_MS" \
    '[.tasks[] | select((.status == "done" or .status == "ready_to_merge" or .status == "completed") and (.completedAt // 0) < $t)] | length' \
    "$TASKS_FILE" 2>/dev/null || echo "0")

if [ "$ARCHIVED" -gt 0 ]; then
    # 移到归档文件
    ARCHIVE_FILE="${LOGS_DIR}/archived-tasks-$(date +%Y-%m).json"
    jq --argjson t "$THRESHOLD_MS" \
        '[.tasks[] | select((.status == "done" or .status == "ready_to_merge" or .status == "completed") and (.completedAt // 0) < $t)]' \
        "$TASKS_FILE" >> "$ARCHIVE_FILE"

    # 从 active tasks 删除
    jq --argjson t "$THRESHOLD_MS" \
        '.tasks |= [.[] | select(not ((.status == "done" or .status == "ready_to_merge" or .status == "completed") and (.completedAt // 0) < $t))]' \
        "$TASKS_FILE" > "${TASKS_FILE}.tmp" && mv "${TASKS_FILE}.tmp" "$TASKS_FILE"

    log "Archived $ARCHIVED old tasks"
fi

# 清理孤立 worktree（分支已合并或任务已完成）
if [ -d "$WORKTREE_BASE" ]; then
    for WORKTREE_DIR in "$WORKTREE_BASE"/*/; do
        TASK_ID=$(basename "$WORKTREE_DIR")
        TASK_STATUS=$(jq -r --arg id "$TASK_ID" '.tasks[] | select(.id == $id) | .status' "$TASKS_FILE" 2>/dev/null || echo "")

        if [ -z "$TASK_STATUS" ] || [ "$TASK_STATUS" = "done" ] || [ "$TASK_STATUS" = "ready_to_merge" ] || [ "$TASK_STATUS" = "completed" ]; then
            # 确认 tmux session 不在运行
            SESSION="agent-${TASK_ID}"
            if ! /usr/local/bin/tmux has-session -t "$SESSION" 2>/dev/null; then
                log "Removing orphan worktree: $TASK_ID"
                # 从主 repo 移除 worktree 引用
                for REPO_DIR in "${HOME}/GitLab/repos"/*/; do
                    cd "$REPO_DIR" 2>/dev/null && git worktree remove -f "$WORKTREE_DIR" 2>/dev/null || true
                done
                rm -rf "$WORKTREE_DIR" 2>/dev/null || true
            fi
        fi
    done
fi

# 清理旧日志（保留 14 天）
find "$LOGS_DIR" -name "*.log" -mtime +14 -delete 2>/dev/null || true
find "$LOGS_DIR" -name "*.notification.sent" -mtime +7 -delete 2>/dev/null || true
find "$LOGS_DIR" -name ".spawned-*" -mtime +30 -delete 2>/dev/null || true
find "$LOGS_DIR" -name ".init-*" -mtime +30 -delete 2>/dev/null || true

log "=== Cleanup done ==="
