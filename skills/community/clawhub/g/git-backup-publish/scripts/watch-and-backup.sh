#!/bin/bash
# Watch for file changes and trigger backup
# Usage: ./watch-and-backup.sh [--daemon]
#
# Requirements: inotify-tools (apt install inotify-tools)
#
# If inotify-tools not available, falls back to polling mode

set -e

WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
BACKUP_SCRIPT="$(dirname "$0")/backup-to-gitee.sh"
PID_FILE="/tmp/openclaw-backup-watcher.pid"
LOG_FILE="/tmp/openclaw-backup-watcher.log"

# Core files to watch (relative to workspace)
WATCH_FILES=(
    "AGENTS.md"
    "SOUL.md"
    "IDENTITY.md"
    "USER.md"
    "MEMORY.md"
    "TOOLS.md"
    "HEARTBEAT.md"
)

# Directories to watch
WATCH_DIRS=(
    "memory"
    "skills"
)

# Check if already running
if [[ -f "$PID_FILE" ]]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "Watcher already running (PID: $PID)"
        echo "Use: kill $PID to stop"
        exit 1
    fi
fi

# Check for inotify-tools
if command -v inotifywait &> /dev/null; then
    echo "Using inotify for real-time monitoring..."
    MODE="inotify"
else
    echo "inotify-tools not found, using polling mode (60s interval)..."
    echo "Install with: apt install inotify-tools"
    MODE="poll"
fi

# Build watch list
WATCH_PATHS=()
for file in "${WATCH_FILES[@]}"; do
    path="$WORKSPACE_DIR/$file"
    [[ -f "$path" ]] && WATCH_PATHS+=("$path")
done
for dir in "${WATCH_DIRS[@]}"; do
    path="$WORKSPACE_DIR/$dir"
    [[ -d "$path" ]] && WATCH_PATHS+=("$path")
done

echo "Watching ${#WATCH_PATHS[@]} paths:"
for p in "${WATCH_PATHS[@]}"; do
    echo "  - $(basename "$p")"
done

# Function to trigger backup
do_backup() {
    local reason="$1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Change detected: $reason" >> "$LOG_FILE"
    echo "Triggering backup..."

    # Run backup script
    if [[ -n "$GITEE_TOKEN" && -n "$GITEE_REPO" ]]; then
        "$BACKUP_SCRIPT" "Auto backup: $reason" >> "$LOG_FILE" 2>&1
    else
        echo "Error: GITEE_TOKEN or GITEE_REPO not set" >> "$LOG_FILE"
    fi
}

# Daemon mode
if [[ "$1" == "--daemon" ]]; then
    echo "Starting in daemon mode..."
    echo $$ > "$PID_FILE"

    if [[ "$MODE" == "inotify" ]]; then
        # inotify mode
        inotifywait -m -r -e modify,create,delete,move "${WATCH_PATHS[@]}" 2>/dev/null | while read path action file; do
            # Debounce: wait 2 seconds for more changes
            sleep 2
            do_backup "$action on $file"
        done
    else
        # Polling mode
        while true; do
            sleep 60
            # Check for changes using git
            cd "$WORKSPACE_DIR"
            if [[ -n $(git status --porcelain 2>/dev/null) ]]; then
                do_backup "polling detected changes"
            fi
        done
    fi
else
    # One-shot check mode (for heartbeat)
    echo "Checking for changes..."

    # Use git to check for changes if this is a git repo
    cd "$WORKSPACE_DIR"

    # Create a simple state file to track changes
    STATE_FILE="$WORKSPACE_DIR/.backup-state"
    CURRENT_STATE=$(find "${WATCH_PATHS[@]}" -type f -exec md5sum {} \; 2>/dev/null | sort | md5sum | cut -d' ' -f1)

    if [[ -f "$STATE_FILE" ]]; then
        PREVIOUS_STATE=$(cat "$STATE_FILE")
        if [[ "$CURRENT_STATE" != "$PREVIOUS_STATE" ]]; then
            echo "$CURRENT_STATE" > "$STATE_FILE"
            do_backup "file state changed"
        else
            echo "No changes detected."
        fi
    else
        echo "$CURRENT_STATE" > "$STATE_FILE"
        echo "Initial state recorded."
    fi
fi