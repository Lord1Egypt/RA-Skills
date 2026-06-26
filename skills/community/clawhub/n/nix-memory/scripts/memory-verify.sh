#!/usr/bin/env bash
# nix-memory: Memory file integrity verification
# Checks all tracked .md files against manifest for unauthorized changes.
set -euo pipefail

WORKSPACE="${NIX_MEMORY_WORKSPACE:-$HOME/.openclaw/workspace}"
STATE_DIR="${WORKSPACE}/.nix-memory"
BASELINE_DIR="${STATE_DIR}/baselines"
MANIFEST="${BASELINE_DIR}/manifest.txt"

if [[ ! -f "$MANIFEST" ]]; then
    echo "MEMORY_NOT_INITIALIZED"
    echo "Run setup.sh first."
    exit 1
fi

NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
CHANGED=0
VERIFIED=0
NEW_FILES=0
DELETED=0
REPORT=""

# Check existing tracked files
while IFS='  ' read -r expected_hash filename; do
    fpath="${WORKSPACE}/${filename}"
    
    if [[ ! -f "$fpath" ]]; then
        REPORT="${REPORT}  [DELETED] ${filename}\n"
        DELETED=$((DELETED + 1))
        continue
    fi
    
    current_hash=$(sha256sum "$fpath" | cut -d' ' -f1)
    
    if [[ "$current_hash" == "$expected_hash" ]]; then
        VERIFIED=$((VERIFIED + 1))
    else
        SIZE_OLD=$(wc -c < "${BASELINE_DIR}/${filename}.baseline" 2>/dev/null || echo "?")
        SIZE_NEW=$(wc -c < "$fpath")
        REPORT="${REPORT}  [CHANGED] ${filename} (${SIZE_OLD} -> ${SIZE_NEW} bytes)\n"
        CHANGED=$((CHANGED + 1))
    fi
done < "$MANIFEST"

# Check for new files not in manifest
while IFS= read -r fpath; do
    fname=$(basename "$fpath")
    if ! grep -q "  ${fname}$" "$MANIFEST" 2>/dev/null; then
        SIZE=$(wc -c < "$fpath")
        REPORT="${REPORT}  [NEW] ${fname} (${SIZE} bytes)\n"
        NEW_FILES=$((NEW_FILES + 1))
    fi
done < <(find "$WORKSPACE" -maxdepth 1 -name "*.md" -type f | sort)

# Memory directory check
MEMORY_DIR="${WORKSPACE}/memory"
if [[ -d "$MEMORY_DIR" ]]; then
    MEMORY_COUNT=$(find "$MEMORY_DIR" -name "*.md" -type f | wc -l)
    LATEST=$(ls -t "$MEMORY_DIR"/*.md 2>/dev/null | head -1)
    if [[ -n "$LATEST" ]]; then
        LATEST_NAME=$(basename "$LATEST")
        LATEST_SIZE=$(wc -c < "$LATEST")
        LATEST_AGE=$(( ($(date +%s) - $(stat -c %Y "$LATEST")) / 3600 ))
    fi
fi

echo "=== Memory Integrity Report: ${NOW} ==="
echo "  Files verified: ${VERIFIED}"
echo "  Files changed: ${CHANGED}"
echo "  Files deleted: ${DELETED}"
echo "  New files: ${NEW_FILES}"
echo ""

if [[ -d "$MEMORY_DIR" ]]; then
    echo "  Memory directory: ${MEMORY_COUNT} daily files"
    if [[ -n "${LATEST_NAME:-}" ]]; then
        echo "  Latest: ${LATEST_NAME} (${LATEST_SIZE} bytes, ${LATEST_AGE}h ago)"
    fi
    echo ""
fi

if [[ -n "$REPORT" ]]; then
    echo "Changes detected:"
    echo -e "$REPORT"
fi

# Log
echo "[${NOW}] verified=${VERIFIED} changed=${CHANGED} deleted=${DELETED} new=${NEW_FILES}" >> "${STATE_DIR}/sessions/$(date +%Y-%m-%d).log"

# Verdict
if [[ $CHANGED -eq 0 && $DELETED -eq 0 ]]; then
    echo "MEMORY_OK"
    if [[ $NEW_FILES -gt 0 ]]; then
        echo "  (${NEW_FILES} new file(s) detected - run setup.sh to add to manifest)"
    fi
    exit 0
else
    echo "MEMORY_CHANGED"
    echo "  ${CHANGED} file(s) modified, ${DELETED} file(s) deleted."
    echo "  Review changes and run setup.sh to accept new state."
    exit 1
fi
