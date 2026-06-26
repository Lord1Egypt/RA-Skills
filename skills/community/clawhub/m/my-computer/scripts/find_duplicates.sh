#!/bin/bash
# find_duplicates.sh — Find duplicate files by content hash
#
# Usage:
#   find_duplicates.sh <directory> [options]
#
# Options:
#   --filter <glob>        File filter (e.g., "*.jpg")
#   --recursive            Include subdirectories (default: true)
#   --min-size <bytes>     Minimum file size to check (default: 1, skip empty files)
#   --output <path>        Write results to file (default: stdout)
#   --json                 Output as JSON (default: human-readable)
#   --action <report|move> Action: just report, or move duplicates (default: report)
#   --move-to <dir>        Where to move duplicates (required if --action move)
#
# Algorithm:
#   1. Group files by size (fast pre-filter — different sizes can't be duplicates)
#   2. For same-size groups, compute MD5 hash
#   3. Report groups with identical hashes
#
# Examples:
#   find_duplicates.sh ~/Photos --filter "*.jpg"
#   find_duplicates.sh ~/Documents --json --output dupes.json
#   find_duplicates.sh ~/Downloads --action move --move-to ~/Downloads/_duplicates

set -euo pipefail

DIR="${1:-}"
FILTER="*"
RECURSIVE=true
MIN_SIZE=1
OUTPUT=""
JSON_OUTPUT=false
ACTION="report"
MOVE_TO=""

shift 1 2>/dev/null || true

while [[ $# -gt 0 ]]; do
    case "$1" in
        --filter)    FILTER="$2"; shift 2 ;;
        --recursive) RECURSIVE=true; shift ;;
        --no-recursive) RECURSIVE=false; shift ;;
        --min-size)  MIN_SIZE="$2"; shift 2 ;;
        --output)    OUTPUT="$2"; shift 2 ;;
        --json)      JSON_OUTPUT=true; shift ;;
        --action)    ACTION="$2"; shift 2 ;;
        --move-to)   MOVE_TO="$2"; shift 2 ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

if [[ -z "$DIR" || ! -d "$DIR" ]]; then
    echo "Usage: find_duplicates.sh <directory> [options]" >&2
    exit 1
fi

if [[ "$ACTION" == "move" && -z "$MOVE_TO" ]]; then
    echo "Error: --move-to required when --action is move" >&2
    exit 1
fi

# Choose hash command
if command -v md5sum &>/dev/null; then
    HASH_CMD="md5sum"
elif command -v md5 &>/dev/null; then
    HASH_CMD="md5 -r"
else
    echo "Error: No md5sum or md5 command found" >&2
    exit 1
fi

# Find files
find_args=("$DIR")
if [[ "$RECURSIVE" == false ]]; then
    find_args+=("-maxdepth" "1")
fi
find_args+=("-type" "f" "-name" "$FILTER" "-size" "+${MIN_SIZE}c")

echo "Scanning for files..." >&2

# Step 1: Group by file size
declare -A SIZE_MAP
TOTAL=0
while IFS= read -r filepath; do
    [[ -z "$filepath" ]] && continue
    if [[ "$(uname)" == "Darwin" ]]; then
        fsize=$(stat -f "%z" "$filepath" 2>/dev/null || echo "0")
    else
        fsize=$(stat -c "%s" "$filepath" 2>/dev/null || echo "0")
    fi
    SIZE_MAP["$fsize"]+="$filepath"$'\n'
    TOTAL=$((TOTAL + 1))
done < <(find "${find_args[@]}" 2>/dev/null)

echo "Found $TOTAL files. Checking sizes..." >&2

# Step 2: For same-size groups, compute hashes
declare -A HASH_MAP
HASH_COUNT=0

for size in "${!SIZE_MAP[@]}"; do
    files="${SIZE_MAP[$size]}"
    file_count=$(echo -n "$files" | grep -c . || echo 0)

    # Only hash if there are 2+ files of the same size
    if [[ "$file_count" -lt 2 ]]; then
        continue
    fi

    while IFS= read -r filepath; do
        [[ -z "$filepath" ]] && continue
        hash=$($HASH_CMD "$filepath" 2>/dev/null | awk '{print $1}')
        if [[ -n "$hash" ]]; then
            HASH_MAP["$hash"]+="$filepath"$'\n'
            HASH_COUNT=$((HASH_COUNT + 1))
        fi
    done <<< "$files"
done

echo "Hashed $HASH_COUNT files. Finding duplicates..." >&2

# Step 3: Report duplicates
DUPE_GROUPS=0
DUPE_FILES=0
DUPE_BYTES=0

output_text() {
    if [[ -n "$OUTPUT" ]]; then
        echo "$1" >> "$OUTPUT"
    else
        echo "$1"
    fi
}

# Clear output file
if [[ -n "$OUTPUT" ]]; then
    > "$OUTPUT"
fi

if [[ "$JSON_OUTPUT" == true ]]; then
    output_text "{"
    output_text "  \"scan_directory\": \"$DIR\","
    output_text "  \"total_files\": $TOTAL,"
    output_text "  \"duplicate_groups\": ["
fi

FIRST_GROUP=true

for hash in "${!HASH_MAP[@]}"; do
    files="${HASH_MAP[$hash]}"
    file_count=$(echo -n "$files" | grep -c . || echo 0)

    if [[ "$file_count" -lt 2 ]]; then
        continue
    fi

    DUPE_GROUPS=$((DUPE_GROUPS + 1))
    group_dupes=$((file_count - 1))  # -1 for the original
    DUPE_FILES=$((DUPE_FILES + group_dupes))

    # Get size of one file for byte calculation
    first_file=$(echo "$files" | head -1)
    if [[ "$(uname)" == "Darwin" ]]; then
        fsize=$(stat -f "%z" "$first_file" 2>/dev/null || echo "0")
    else
        fsize=$(stat -c "%s" "$first_file" 2>/dev/null || echo "0")
    fi
    group_waste=$((fsize * group_dupes))
    DUPE_BYTES=$((DUPE_BYTES + group_waste))

    if [[ "$JSON_OUTPUT" == true ]]; then
        if [[ "$FIRST_GROUP" == false ]]; then
            output_text "    ,"
        fi
        FIRST_GROUP=false
        output_text "    {"
        output_text "      \"hash\": \"$hash\","
        output_text "      \"size\": $fsize,"
        output_text "      \"count\": $file_count,"
        output_text "      \"files\": ["
        FIRST_FILE=true
        while IFS= read -r filepath; do
            [[ -z "$filepath" ]] && continue
            if [[ "$FIRST_FILE" == false ]]; then
                output_text "        ,"
            fi
            FIRST_FILE=false
            output_text "        \"$filepath\""
        done <<< "$files"
        output_text "      ]"
        output_text "    }"
    else
        output_text ""
        output_text "Duplicate group (hash: ${hash:0:8}..., ${file_count} files, $(numfmt --to=iec $fsize 2>/dev/null || echo "${fsize} bytes") each):"
        FIRST_IN_GROUP=true
        while IFS= read -r filepath; do
            [[ -z "$filepath" ]] && continue
            if [[ "$FIRST_IN_GROUP" == true ]]; then
                output_text "  [keep] $filepath"
                FIRST_IN_GROUP=false
            else
                output_text "  [dupe] $filepath"

                # Move duplicate if requested
                if [[ "$ACTION" == "move" ]]; then
                    mkdir -p "$MOVE_TO"
                    mv "$filepath" "$MOVE_TO/" 2>/dev/null && \
                        output_text "         → moved to $MOVE_TO/"
                fi
            fi
        done <<< "$files"
    fi
done

# Human-readable size
if command -v numfmt &>/dev/null; then
    WASTE_HR=$(numfmt --to=iec "$DUPE_BYTES" 2>/dev/null || echo "$DUPE_BYTES bytes")
else
    WASTE_HR="$((DUPE_BYTES / 1048576)) MB"
fi

if [[ "$JSON_OUTPUT" == true ]]; then
    output_text "  ],"
    output_text "  \"summary\": {"
    output_text "    \"duplicate_groups\": $DUPE_GROUPS,"
    output_text "    \"duplicate_files\": $DUPE_FILES,"
    output_text "    \"wasted_bytes\": $DUPE_BYTES"
    output_text "  }"
    output_text "}"
else
    output_text ""
    output_text "═══════════════════════════════════════════════════"
    output_text "  DUPLICATE SCAN RESULTS"
    output_text "═══════════════════════════════════════════════════"
    output_text "  Scanned:         $TOTAL files"
    output_text "  Duplicate groups: $DUPE_GROUPS"
    output_text "  Duplicate files:  $DUPE_FILES"
    output_text "  Wasted space:     $WASTE_HR"
    if [[ "$ACTION" == "move" ]]; then
        output_text "  Duplicates moved: $MOVE_TO"
    fi
    output_text "═══════════════════════════════════════════════════"
fi

if [[ -n "$OUTPUT" ]]; then
    echo "Results written to: $OUTPUT" >&2
fi
