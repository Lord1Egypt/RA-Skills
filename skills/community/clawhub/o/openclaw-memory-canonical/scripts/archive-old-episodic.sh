#!/bin/bash
# Archive episodic files older than $1 days (default 30)
# Places archived files into archive/YYYY/MM/ structure
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
MEMORY_DIR="$WORKSPACE_ROOT/memory"
ARCHIVE_DIR="$MEMORY_DIR/archive"
RETENTION_DAYS="${1:-30}"

echo "=== Episodic Archival ($(date '+%Y-%m-%d %H:%M')) ==="
count=0
for file in "$MEMORY_DIR"/episodic/*.md; do
    [ -f "$file" ] || continue
    if [ "$(find "$file" -mtime +"$RETENTION_DAYS" -print 2>/dev/null)" ]; then
        fname=$(basename "$file")
        year="${fname:0:4}"
        month="${fname:5:2}"
        dest="$ARCHIVE_DIR/$year/$month"
        mkdir -p "$dest"
        echo "  Archive: $fname → $year/$month/"
        mv "$file" "$dest/"
        count=$((count + 1))
    fi
done

echo "✅ Archived: $count files (> ${RETENTION_DAYS} days old)"
echo "Done."
