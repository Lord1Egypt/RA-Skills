#!/bin/bash
# Robust batch indexer with git rollback fallback and watchdog.
# Usage: bash index-batch.sh [PATH1 PATH2 ...]
# If no paths given, indexes all subdirectories of ~/Documenti/github/ recursively.

set -euo pipefail

export TMPDIR="${TMPDIR:-$HOME/.local/share/local-rag/tmp}"
PYTHON="$HOME/.local/share/local-rag/venv/bin/python"
INDEX="$HOME/.openclaw/workspace/skills/lookupmark-local-rag/scripts/index.py"
DB="$HOME/.local/share/local-rag/chromadb"
LOCK="$HOME/.local/share/local-rag/index.lock"
LOG="$HOME/.local/share/local-rag/index-batch.log"
OOM_PROTECT="$HOME/.local/share/local-rag/oom-protect.pid"

MAX_RETRIES=2
TIMEOUT_MINUTES=30

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

cleanup() {
    rm -f "$LOCK" "$OOM_PROTECT" 2>/dev/null
    # Kill any lingering python index process
    pkill -f "lookupmark-local-rag/scripts/index.py" 2>/dev/null || true
}
trap cleanup EXIT

# Ensure DB git repo exists
if [ ! -d "$DB/.git" ]; then
    mkdir -p "$DB"
    cd "$DB" && git init && git commit --allow-empty -m "clean slate"
    log "Initialized git repo at $DB"
fi

git_checkpoint() {
    cd "$DB"
    git add -A
    if git diff --cached --quiet; then
        log "  No changes to commit"
    else
        git commit -m "$1" 2>&1 | tee -a "$LOG"
    fi
    cd -
}

git_rollback() {
    log "  Rolling back to previous checkpoint..."
    cd "$DB"
    # Find last good commit (skip current broken state)
    PREV=$(git log --oneline -2 --format="%H" | tail -1)
    if [ -n "$PREV" ]; then
        git checkout -- .
        git reset --hard "$PREV"
        log "  Rolled back to $(git log --oneline -1)"
    fi
    cd -
}

index_path() {
    local path="$1"
    rm -f "$LOCK"

    # Disk space check
    local free_mb=$(df -m --output=avail "$DB" | tail -1 | tr -d ' ')
    if [ "$free_mb" -lt 500 ]; then
        log "  ❌ Low disk space (${free_mb}MB free < 500MB threshold) — aborting"
        return 1
    fi

    log "Indexing: $path"

    # Run with timeout and OOM protection
    timeout "$((TIMEOUT_MINUTES * 60))" "$PYTHON" "$INDEX" --paths "$path" >> "$LOG" 2>&1
    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        log "  ✅ Success"
        git_checkpoint "$(basename "$path")"
        return 0
    elif [ $exit_code -eq 137 ]; then
        log "  ❌ OOM killed (SIGKILL) — rolling back"
        git_rollback
        return 1
    elif [ $exit_code -eq 124 ]; then
        log "  ❌ Timeout (${TIMEOUT_MINUTES}min) — rolling back"
        git_rollback
        return 1
    else
        log "  ❌ Exit code $exit_code — rolling back"
        git_rollback
        return 1
    fi
}

# Collect paths
if [ $# -gt 0 ]; then
    PATHS=("$@")
else
    # Auto-discover: all subdirs with indexable files
    mapfile -t PATHS < <(find ~/Documenti/github/thesis ~/Documenti/github/polito \
        -mindepth 1 -maxdepth 4 -type d \
        ! -path "*/labs/*" ! -path "*/exercises/*" ! -path "*/.git/*" \
        ! -path "*/node_modules/*" ! -path "*/__pycache__/*" ! -path "*/.venv/*" \
        ! -path "*src*" ! -path "*scripts*" ! -path "*tests*" \
        ! -path "*notebooks*" \
        2>/dev/null | sort -u)
fi

FAILED=()
TOTAL=${#PATHS[@]}
DONE=0

log "=== Starting batch indexing: $TOTAL paths ==="

for p in "${PATHS[@]}"; do
    DONE=$((DONE + 1))
    log "[$DONE/$TOTAL] Processing: $p"

    # Retry loop
    SUCCESS=false
    for attempt in $(seq 1 $((MAX_RETRIES + 1))); do
        if index_path "$p"; then
            SUCCESS=true
            break
        fi
        if [ $attempt -le $MAX_RETRIES ]; then
            log "  Retry $attempt/$MAX_RETRIES in 10s..."
            sleep 10
        fi
    done

    if [ "$SUCCESS" = false ]; then
        FAILED+=("$p")
        log "  ⚠️  Permanently failed after $((MAX_RETRIES + 1)) attempts: $p"
    fi
done

# Summary
log "=== DONE ==="
if [ ${#FAILED[@]} -eq 0 ]; then
    log "All $TOTAL paths indexed successfully! ✅"
else
    log "Completed: $((TOTAL - ${#FAILED[@]}))/$TOTAL"
    log "Failed paths:"
    for f in "${FAILED[@]}"; do
        log "  - $f"
    done
fi

# Print final DB stats
"$PYTHON" -c "
import chromadb
c = chromadb.PersistentClient(path='$DB')
p = c.get_or_create_collection('parents')
ch = c.get_or_create_collection('children')
print(f'DB: {p.count()} parents, {ch.count()} children')
" 2>/dev/null | tee -a "$LOG"
