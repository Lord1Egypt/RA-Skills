#!/bin/bash
# disk_report.sh — Generate a comprehensive disk usage report
#
# Usage:
#   disk_report.sh [directory] [options]
#
# Options:
#   --top <n>          Show top N largest items (default: 20)
#   --output <path>    Write report to file (default: stdout)
#   --old-days <n>     Flag files not accessed in N days (default: 365)
#   --include-caches   Include cache directory analysis
#   --json             Output as JSON
#
# Examples:
#   disk_report.sh ~
#   disk_report.sh ~/Documents --top 30 --output report.txt
#   disk_report.sh ~ --include-caches --old-days 180

set -euo pipefail

DIR="${1:-$HOME}"
TOP_N=20
OUTPUT=""
OLD_DAYS=365
INCLUDE_CACHES=false
JSON_OUTPUT=false

shift 1 2>/dev/null || true

while [[ $# -gt 0 ]]; do
    case "$1" in
        --top)            TOP_N="$2"; shift 2 ;;
        --output)         OUTPUT="$2"; shift 2 ;;
        --old-days)       OLD_DAYS="$2"; shift 2 ;;
        --include-caches) INCLUDE_CACHES=true; shift ;;
        --json)           JSON_OUTPUT=true; shift ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

out() {
    if [[ -n "$OUTPUT" ]]; then
        echo "$1" >> "$OUTPUT"
    else
        echo "$1"
    fi
}

if [[ -n "$OUTPUT" ]]; then
    > "$OUTPUT"
fi

PLATFORM=$(uname -s)
REPORT_TIME=$(date "+%Y-%m-%d %H:%M:%S")

out "═══════════════════════════════════════════════════════════════"
out "  DISK USAGE REPORT"
out "  Directory: $DIR"
out "  Generated: $REPORT_TIME"
out "═══════════════════════════════════════════════════════════════"
out ""

# --- Section 1: Disk Overview ---
out "┌─────────────────────────────────────────────────────────────┐"
out "│  DISK OVERVIEW                                              │"
out "└─────────────────────────────────────────────────────────────┘"
out ""

if [[ "$PLATFORM" == "Darwin" ]]; then
    df -h / | tail -1 | awk '{printf "  Filesystem:  %s\n  Total:       %s\n  Used:        %s (%s)\n  Available:   %s\n", $1, $2, $3, $5, $4}'
else
    df -h "$DIR" | tail -1 | awk '{printf "  Filesystem:  %s\n  Total:       %s\n  Used:        %s (%s)\n  Available:   %s\n", $1, $2, $3, $5, $4}'
fi | while IFS= read -r line; do out "$line"; done

out ""

# --- Section 2: Top-Level Directory Sizes ---
out "┌─────────────────────────────────────────────────────────────┐"
out "│  TOP-LEVEL DIRECTORY SIZES                                   │"
out "└─────────────────────────────────────────────────────────────┘"
out ""

du -sh "$DIR"/* 2>/dev/null | sort -rh | head -n "$TOP_N" | while IFS=$'\t' read -r size path; do
    name=$(basename "$path")
    printf "  %-8s %s\n" "$size" "$name"
done | while IFS= read -r line; do out "$line"; done

out ""

# --- Section 3: Largest Files ---
out "┌─────────────────────────────────────────────────────────────┐"
out "│  LARGEST FILES (top $TOP_N)                                  │"
out "└─────────────────────────────────────────────────────────────┘"
out ""

find "$DIR" -type f -not -path "*/.*" -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | \
    xargs ls -lS 2>/dev/null | \
    head -n "$TOP_N" | \
    awk '{
        size = $5;
        if (size >= 1073741824) printf "  %6.1f GB  ", size/1073741824;
        else if (size >= 1048576) printf "  %6.1f MB  ", size/1048576;
        else if (size >= 1024) printf "  %6.1f KB  ", size/1024;
        else printf "  %6d B   ", size;
        # Print filename (everything from field 9 onwards)
        for (i=9; i<=NF; i++) printf "%s ", $i;
        printf "\n";
    }' | while IFS= read -r line; do out "$line"; done

out ""

# --- Section 4: File Type Distribution ---
out "┌─────────────────────────────────────────────────────────────┐"
out "│  FILE TYPE DISTRIBUTION                                      │"
out "└─────────────────────────────────────────────────────────────┘"
out ""

find "$DIR" -type f -not -path "*/.*" -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | \
    awk -F. '{if (NF>1) print tolower($NF); else print "(no extension)"}' | \
    sort | uniq -c | sort -rn | head -n 15 | \
    awk '{printf "  %8d  .%s\n", $1, $2}' | while IFS= read -r line; do out "$line"; done

out ""

# --- Section 5: Old Files ---
out "┌─────────────────────────────────────────────────────────────┐"
out "│  OLD FILES (not accessed in $OLD_DAYS+ days)                 │"
out "└─────────────────────────────────────────────────────────────┘"
out ""

OLD_FILES=$(find "$DIR" -type f -not -path "*/.*" -not -path "*/node_modules/*" -not -path "*/.git/*" -atime +"$OLD_DAYS" 2>/dev/null | wc -l | tr -d ' ')

if [[ "$OLD_FILES" -gt 0 ]]; then
    OLD_SIZE=$(find "$DIR" -type f -not -path "*/.*" -not -path "*/node_modules/*" -not -path "*/.git/*" -atime +"$OLD_DAYS" 2>/dev/null | \
        xargs ls -l 2>/dev/null | awk '{total += $5} END {
            if (total >= 1073741824) printf "%.1f GB", total/1073741824;
            else if (total >= 1048576) printf "%.1f MB", total/1048576;
            else printf "%.1f KB", total/1024;
        }')

    out "  Found $OLD_FILES files ($OLD_SIZE) not accessed in $OLD_DAYS+ days."
    out ""
    out "  Largest old files:"
    find "$DIR" -type f -not -path "*/.*" -not -path "*/node_modules/*" -not -path "*/.git/*" -atime +"$OLD_DAYS" 2>/dev/null | \
        xargs ls -lS 2>/dev/null | head -10 | \
        awk '{
            size = $5;
            if (size >= 1073741824) printf "    %6.1f GB  ", size/1073741824;
            else if (size >= 1048576) printf "    %6.1f MB  ", size/1048576;
            else printf "    %6.1f KB  ", size/1024;
            for (i=9; i<=NF; i++) printf "%s ", $i;
            printf "\n";
        }' | while IFS= read -r line; do out "$line"; done
else
    out "  No files older than $OLD_DAYS days found."
fi

out ""

# --- Section 6: Cache Analysis (optional) ---
if [[ "$INCLUDE_CACHES" == true ]]; then
    out "┌─────────────────────────────────────────────────────────────┐"
    out "│  CACHE ANALYSIS                                             │"
    out "└─────────────────────────────────────────────────────────────┘"
    out ""

    if [[ "$PLATFORM" == "Darwin" ]]; then
        CACHE_DIRS=(
            "$HOME/Library/Caches"
            "$HOME/Library/Application Support"
            "$HOME/Library/Logs"
            "$HOME/.npm/_cacache"
            "$HOME/.cache"
        )
    else
        CACHE_DIRS=(
            "$HOME/.cache"
            "$HOME/.npm/_cacache"
            "$HOME/.local/share/Trash"
            "/tmp"
        )
    fi

    for cache_dir in "${CACHE_DIRS[@]}"; do
        if [[ -d "$cache_dir" ]]; then
            size=$(du -sh "$cache_dir" 2>/dev/null | awk '{print $1}')
            name=$(echo "$cache_dir" | sed "s|$HOME|~|")
            printf "  %-8s %s\n" "$size" "$name"
        fi
    done | while IFS= read -r line; do out "$line"; done

    out ""

    # Node modules
    NODE_MODULES=$(find "$DIR" -name "node_modules" -type d -maxdepth 4 2>/dev/null | wc -l | tr -d ' ')
    if [[ "$NODE_MODULES" -gt 0 ]]; then
        NM_SIZE=$(find "$DIR" -name "node_modules" -type d -maxdepth 4 2>/dev/null | \
            xargs du -sh 2>/dev/null | awk '{total += $1} END {printf "%.0f", total}')
        out "  Found $NODE_MODULES node_modules directories."
        find "$DIR" -name "node_modules" -type d -maxdepth 4 2>/dev/null | \
            xargs du -sh 2>/dev/null | sort -rh | head -5 | \
            awk '{printf "    %-8s %s\n", $1, $2}' | while IFS= read -r line; do out "$line"; done
    fi

    # Build artifacts
    BUILD_DIRS=$(find "$DIR" \( -name ".build" -o -name "dist" -o -name "build" -o -name "__pycache__" -o -name ".next" \) -type d -maxdepth 4 2>/dev/null | wc -l | tr -d ' ')
    if [[ "$BUILD_DIRS" -gt 0 ]]; then
        out ""
        out "  Found $BUILD_DIRS build artifact directories."
        find "$DIR" \( -name ".build" -o -name "dist" -o -name "build" -o -name "__pycache__" -o -name ".next" \) -type d -maxdepth 4 2>/dev/null | \
            xargs du -sh 2>/dev/null | sort -rh | head -5 | \
            awk '{printf "    %-8s %s\n", $1, $2}' | while IFS= read -r line; do out "$line"; done
    fi

    out ""
fi

# --- Summary ---
out "═══════════════════════════════════════════════════════════════"
TOTAL_SIZE=$(du -sh "$DIR" 2>/dev/null | awk '{print $1}')
TOTAL_FILES=$(find "$DIR" -type f -not -path "*/.*" 2>/dev/null | wc -l | tr -d ' ')
TOTAL_DIRS=$(find "$DIR" -type d -not -path "*/.*" 2>/dev/null | wc -l | tr -d ' ')
out "  Total size: $TOTAL_SIZE  |  Files: $TOTAL_FILES  |  Directories: $TOTAL_DIRS"
out "═══════════════════════════════════════════════════════════════"

if [[ -n "$OUTPUT" ]]; then
    echo "Report written to: $OUTPUT" >&2
fi
