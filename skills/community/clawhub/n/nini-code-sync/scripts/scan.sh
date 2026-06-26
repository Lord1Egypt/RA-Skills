#!/usr/bin/env bash
set -euo pipefail

# scan.sh - Scan a base directory for git repositories and output JSON status report
# Usage: scan.sh [--fetch] [--base-dir <path>]
#   --fetch      Fetch remote before reporting (10s timeout per repo)
#   --base-dir   Base directory to scan (default: ~/code)
#
# Scans <base-dir>/*/ and <base-dir>/*/repos/*/ for git repos.

DO_FETCH=false
BASE_DIR="$HOME/code"
FETCH_TIMEOUT=10

while [[ $# -gt 0 ]]; do
    case "$1" in
        --fetch) DO_FETCH=true; shift ;;
        --base-dir) BASE_DIR="$2"; shift 2 ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

# Expand ~ if needed
BASE_DIR="${BASE_DIR/#\~/$HOME}"

if [[ ! -d "$BASE_DIR" ]]; then
    echo "Error: base directory '$BASE_DIR' not found" >&2
    exit 1
fi

# JSON-escape a string value (handles backslash and double quote)
json_escape() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    printf '%s' "$s"
}

# Run a command with timeout (POSIX-compatible, no coreutils needed on macOS)
run_with_timeout() {
    local secs=$1
    shift
    "$@" &
    local cmd_pid=$!
    (sleep "$secs" && kill "$cmd_pid" 2>/dev/null) &
    local timer_pid=$!
    if wait "$cmd_pid" 2>/dev/null; then
        kill "$timer_pid" 2>/dev/null
        wait "$timer_pid" 2>/dev/null || true
        return 0
    else
        kill "$timer_pid" 2>/dev/null
        wait "$timer_pid" 2>/dev/null || true
        return 1
    fi
}

# Collect candidate directories: <base-dir>/*/ and <base-dir>/*/repos/*/
candidates=()
for dir in "$BASE_DIR"/*/; do
    [[ -d "$dir" ]] && candidates+=("$dir")
done
for dir in "$BASE_DIR"/*/repos/*/; do
    [[ -d "$dir" ]] && candidates+=("$dir")
done

# Output JSON array
first=true
echo "["

for dir in "${candidates[@]}"; do
    # Skip non-git directories
    [[ -d "${dir}.git" ]] || continue

    # Fetch if requested
    fetch_error=false
    if $DO_FETCH; then
        if ! run_with_timeout "$FETCH_TIMEOUT" git -C "$dir" fetch --quiet 2>/dev/null; then
            fetch_error=true
        fi
    fi

    # Branch name (handles detached HEAD)
    branch=$(git -C "$dir" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")

    # Remote and URL for current branch
    remote=$(git -C "$dir" config "branch.${branch}.remote" 2>/dev/null || echo "")
    remote_url=""
    [[ -n "$remote" ]] && remote_url=$(git -C "$dir" config "remote.${remote}.url" 2>/dev/null || echo "")

    # Dirty count: modified + untracked files
    dirty_count=$(git -C "$dir" status --porcelain 2>/dev/null | wc -l | tr -d ' ')

    # Upstream tracking: ahead/behind counts
    has_upstream=false
    ahead=0
    behind=0
    if git -C "$dir" rev-parse --abbrev-ref "@{u}" >/dev/null 2>&1; then
        has_upstream=true
        counts=$(git -C "$dir" rev-list --count --left-right "HEAD...@{u}" 2>/dev/null || echo "0	0")
        ahead=$(echo "$counts" | awk '{print $1}')
        behind=$(echo "$counts" | awk '{print $2}')
    fi

    # Comma separator between objects
    $first && first=false || echo ","

    # Build JSON object
    path_clean="${dir%/}"
    name=$(basename "$dir")

    printf '  {"path":"%s","name":"%s","branch":"%s","remote":"%s","remote_url":"%s","dirty_count":%d,"has_upstream":%s,"ahead":%d,"behind":%d' \
        "$(json_escape "$path_clean")" \
        "$(json_escape "$name")" \
        "$(json_escape "$branch")" \
        "$(json_escape "$remote")" \
        "$(json_escape "$remote_url")" \
        "$dirty_count" \
        "$has_upstream" \
        "$ahead" \
        "$behind"

    # Include fetch_error only when --fetch was used and fetch failed
    if $DO_FETCH && $fetch_error; then
        printf ',"fetch_error":true'
    fi
    printf '}'
done

echo ""
echo "]"
