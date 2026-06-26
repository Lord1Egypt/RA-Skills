#!/bin/bash
# Atomic write: write to tmp, then mv. Prevents corrupted files on crash.
# Usage: atomic-write.sh /path/to/file.txt "content"
# Or:    echo "content" | atomic-write.sh /path/to/file.txt
set -euo pipefail

FILE="$1"
TMP="${FILE}.tmp.$$"

mkdir -p "$(dirname "$FILE")"

if [ ! -t 0 ]; then
    cat > "$TMP"
else
    shift
    printf '%s\n' "$*" > "$TMP"
fi

sync "$TMP" 2>/dev/null || sync
mv "$TMP" "$FILE"
