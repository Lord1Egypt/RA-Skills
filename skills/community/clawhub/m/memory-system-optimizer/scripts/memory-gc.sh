#!/usr/bin/env bash
# memory-gc.sh — 记忆垃圾回收脚本

MEMORY_DIR="${MEMORY_DIR:-$HOME/.openclaw/workspace/memory}"
ARCHIVE_DIR="$MEMORY_DIR/.archive"

mkdir -p "$ARCHIVE_DIR"

echo "=== Memory GC ==="

# 归档超过30天的日志
for f in "$MEMORY_DIR"/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].md; do
    [[ -f "$f" ]] || continue
    age_days=$(( ($(date +%s) - $(stat -f %m "$f")) / 86400 ))
    if [[ $age_days -gt 30 ]]; then
        mv "$f" "$ARCHIVE_DIR/" 2>/dev/null || true
        echo "Archived: $(basename $f)"
    fi
done

echo "=== GC Done ==="
