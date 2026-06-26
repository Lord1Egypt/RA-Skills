#!/bin/bash
# Archive legacy/non-canonical scratch files older than $1 days (default 30)
# Keeps ERRORS.md, LEARNINGS.md, FEATURE_REQUESTS.md in place.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
resolve_workspace_root() {
    local dir="$SCRIPT_DIR"
    while [ "$dir" != "/" ]; do
        if [ -f "$dir/MEMORY.md" ] && [ -d "$dir/memory" ]; then
            printf '%s\n' "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}
WORKSPACE_ROOT="$(resolve_workspace_root || true)"
if [ -z "$WORKSPACE_ROOT" ]; then
    echo "ERROR: workspace root not found (expected MEMORY.md and memory/ in an ancestor directory)" >&2
    exit 1
fi
LEARNINGS_DIR="$WORKSPACE_ROOT/.learnings"
ARCHIVE_DIR="$WORKSPACE_ROOT/memory/archive/learnings"
RETENTION_DAYS="${1:-30}"

if [ ! -d "$LEARNINGS_DIR" ]; then
    echo "ℹ️  .learnings directory not found"
    exit 0
fi

echo "=== Learnings Archival ($(date '+%Y-%m-%d %H:%M')) ==="
get_archive_year_month() {
    local file="$1"
    local year month
    if year=$(date -r "$file" +%Y 2>/dev/null) && month=$(date -r "$file" +%m 2>/dev/null); then
        printf '%s %s\n' "$year" "$month"
        return 0
    fi
    if year=$(stat -c %y "$file" 2>/dev/null | cut -c1-4) && month=$(stat -c %y "$file" 2>/dev/null | cut -c6-7) && [ -n "$year" ] && [ -n "$month" ]; then
        printf '%s %s\n' "$year" "$month"
        return 0
    fi
    if year=$(stat -f %Sm -t %Y "$file" 2>/dev/null) && month=$(stat -f %Sm -t %m "$file" 2>/dev/null) && [ -n "$year" ] && [ -n "$month" ]; then
        printf '%s %s\n' "$year" "$month"
        return 0
    fi
    date '+%Y %m'
}
count=0
for file in "$LEARNINGS_DIR"/*.md; do
    [ -f "$file" ] || continue
    fname=$(basename "$file")
    case "$fname" in
        ERRORS.md|LEARNINGS.md|FEATURE_REQUESTS.md)
            continue
            ;;
    esac

    pinned=0
    if grep -q '#pinned[[:space:]]*$' "$file" 2>/dev/null; then
        pinned=1
    fi
    [ "$pinned" -eq 1 ] && continue

    if [ "$(find "$file" -mtime +"$RETENTION_DAYS" -print 2>/dev/null)" ]; then
        read -r year month <<EOF
$(get_archive_year_month "$file")
EOF
        dest="$ARCHIVE_DIR/$year/$month"
        mkdir -p "$dest"
        echo "  Archive: $fname → learnings/$year/$month/"
        mv "$file" "$dest/"
        count=$((count + 1))
    fi
done

echo "✅ Archived: $count files (> ${RETENTION_DAYS} days old)"
echo "Done."
