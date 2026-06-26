#!/bin/bash
# Palest Ink - Git Hook Script
# This script is installed as post-commit, post-merge, post-checkout, pre-push

PALEST_INK_DIR="$HOME/.palest-ink"
HOOK_NAME="$(basename "$0")"
DATE_DIR="$(date +%Y)/$(date +%m)"
DATAFILE="$PALEST_INK_DIR/data/$DATE_DIR/$(date +%d).jsonl"
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Ensure data directory exists
mkdir -p "$(dirname "$DATAFILE")"

# Helper: escape string for JSON
json_escape() {
    python3 -c "import json,sys; print(json.dumps(sys.stdin.read().strip()))" 2>/dev/null <<< "$1"
}

case "$HOOK_NAME" in
    post-commit)
        REPO=$(git rev-parse --show-toplevel 2>/dev/null || echo "unknown")
        HASH=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
        BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
        MESSAGE=$(git log -1 --pretty=%s 2>/dev/null || echo "")
        FILES_JSON=$(git diff-tree --no-commit-id --name-only -r HEAD 2>/dev/null | python3 -c "import sys,json; print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))" 2>/dev/null || echo "[]")
        STATS=$(git diff --stat HEAD~1 HEAD 2>/dev/null | tail -1 || echo "")
        INSERTIONS=$(echo "$STATS" | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+' || echo "0")
        DELETIONS=$(echo "$STATS" | grep -oE '[0-9]+ deletion' | grep -oE '[0-9]+' || echo "0")

        python3 -c "
import json
record = {
    'ts': '$TIMESTAMP',
    'type': 'git_commit',
    'source': 'git_hook',
    'data': {
        'repo': '$REPO',
        'branch': '$BRANCH',
        'hash': '$HASH',
        'message': $(json_escape "$MESSAGE"),
        'files_changed': $FILES_JSON,
        'insertions': int('${INSERTIONS:-0}'),
        'deletions': int('${DELETIONS:-0}')
    }
}
with open('$DATAFILE', 'a') as f:
    f.write(json.dumps(record, ensure_ascii=False) + '\n')
" 2>/dev/null
        ;;

    post-merge)
        REPO=$(git rev-parse --show-toplevel 2>/dev/null || echo "unknown")
        BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
        # $1 is squash flag
        IS_SQUASH="${1:-0}"

        python3 -c "
import json
record = {
    'ts': '$TIMESTAMP',
    'type': 'git_pull',
    'source': 'git_hook',
    'data': {
        'repo': '$REPO',
        'branch': '$BRANCH',
        'is_squash': bool(int('$IS_SQUASH'))
    }
}
with open('$DATAFILE', 'a') as f:
    f.write(json.dumps(record, ensure_ascii=False) + '\n')
" 2>/dev/null
        ;;

    post-checkout)
        REPO=$(git rev-parse --show-toplevel 2>/dev/null || echo "unknown")
        PREV_HEAD="$1"
        NEW_HEAD="$2"
        BRANCH_FLAG="$3"  # 1 = branch checkout, 0 = file checkout

        # Only record branch checkouts
        if [ "$BRANCH_FLAG" = "1" ]; then
            FROM_BRANCH=$(git name-rev --name-only "$PREV_HEAD" 2>/dev/null || echo "unknown")
            TO_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")

            python3 -c "
import json
record = {
    'ts': '$TIMESTAMP',
    'type': 'git_checkout',
    'source': 'git_hook',
    'data': {
        'repo': '$REPO',
        'from_ref': '$FROM_BRANCH',
        'to_branch': '$TO_BRANCH'
    }
}
with open('$DATAFILE', 'a') as f:
    f.write(json.dumps(record, ensure_ascii=False) + '\n')
" 2>/dev/null
        fi
        ;;

    pre-push)
        REPO=$(git rev-parse --show-toplevel 2>/dev/null || echo "unknown")
        BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
        REMOTE_NAME="$1"
        REMOTE_URL="$2"

        python3 -c "
import json
record = {
    'ts': '$TIMESTAMP',
    'type': 'git_push',
    'source': 'git_hook',
    'data': {
        'repo': '$REPO',
        'branch': '$BRANCH',
        'remote': '$REMOTE_NAME',
        'remote_url': '$REMOTE_URL'
    }
}
with open('$DATAFILE', 'a') as f:
    f.write(json.dumps(record, ensure_ascii=False) + '\n')
" 2>/dev/null
        ;;
esac

# Chain to previous global hooks directory (backed up during install)
PREV_HOOKS_PATH=""
if [ -f "$PALEST_INK_DIR/config.json" ]; then
    PREV_HOOKS_PATH=$(python3 -c "
import json
with open('$PALEST_INK_DIR/config.json') as f:
    print(json.load(f).get('previous_hooks_path', ''))
" 2>/dev/null || echo "")
fi
if [ -n "$PREV_HOOKS_PATH" ] && [ -x "$PREV_HOOKS_PATH/$HOOK_NAME" ]; then
    "$PREV_HOOKS_PATH/$HOOK_NAME" "$@"
fi

# Also chain to project-local hook if it exists
LOCAL_HOOK="$(git rev-parse --git-dir 2>/dev/null)/hooks/${HOOK_NAME}.local"
if [ -x "$LOCAL_HOOK" ]; then
    exec "$LOCAL_HOOK" "$@"
fi

exit 0
