#!/bin/bash
# batch_executor.sh — Execute batch file operations with logging and undo manifest
#
# Usage:
#   batch_executor.sh <operation> <source_dir> [options]
#
# Operations:
#   rename    - Rename files (requires --pattern)
#   move      - Move files to dest (requires --dest)
#   organize  - Organize by type/date/ext (requires --dest and --by)
#   copy      - Copy files to dest (requires --dest)
#
# Options:
#   --pattern <sed_expr>   Rename pattern (sed expression)
#   --dest <dir>           Destination directory
#   --by <type|date|ext>   Organization method
#   --filter <glob>        File filter (e.g., "*.jpg")
#   --recursive            Include subdirectories
#   --batch-size <n>       Report progress every N files (default: 50)
#   --manifest <path>      Custom manifest path (default: auto-generated)
#
# The script creates an undo manifest at ~/.my-computer-manifests/ that can be
# used with undo_operation.sh to reverse the operation.

set -euo pipefail

OPERATION="${1:-}"
SOURCE_DIR="${2:-}"
PATTERN=""
DEST=""
BY=""
FILTER="*"
RECURSIVE=false
BATCH_SIZE=50
MANIFEST_DIR="$HOME/.my-computer-manifests"
MANIFEST_PATH=""

shift 2 2>/dev/null || true

while [[ $# -gt 0 ]]; do
    case "$1" in
        --pattern)    PATTERN="$2"; shift 2 ;;
        --dest)       DEST="$2"; shift 2 ;;
        --by)         BY="$2"; shift 2 ;;
        --filter)     FILTER="$2"; shift 2 ;;
        --recursive)  RECURSIVE=true; shift ;;
        --batch-size) BATCH_SIZE="$2"; shift 2 ;;
        --manifest)   MANIFEST_PATH="$2"; shift 2 ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

if [[ -z "$OPERATION" || -z "$SOURCE_DIR" ]]; then
    echo "Usage: batch_executor.sh <operation> <source_dir> [options]" >&2
    exit 1
fi

if [[ ! -d "$SOURCE_DIR" ]]; then
    echo "Error: Source directory does not exist: $SOURCE_DIR" >&2
    exit 1
fi

# Setup manifest
mkdir -p "$MANIFEST_DIR"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SAFE_SOURCE=$(echo "$SOURCE_DIR" | tr '/' '_' | tr ' ' '_')
if [[ -z "$MANIFEST_PATH" ]]; then
    MANIFEST_PATH="$MANIFEST_DIR/${OPERATION}_${SAFE_SOURCE}_$(date +%Y%m%d_%H%M%S).json"
fi

# Initialize manifest
cat > "$MANIFEST_PATH" << INITEOF
{
  "operation": "$OPERATION",
  "source_dir": "$SOURCE_DIR",
  "timestamp": "$TIMESTAMP",
  "filter": "$FILTER",
  "actions": [],
  "errors": [],
  "total_files": 0,
  "success_count": 0,
  "error_count": 0
}
INITEOF

# Temp files for collecting actions and errors
ACTIONS_TMP=$(mktemp)
ERRORS_TMP=$(mktemp)
trap 'rm -f "$ACTIONS_TMP" "$ERRORS_TMP"' EXIT

# Find files
find_args=("$SOURCE_DIR")
if [[ "$RECURSIVE" == false ]]; then
    find_args+=("-maxdepth" "1")
fi
find_args+=("-type" "f" "-name" "$FILTER")

FILES=$(find "${find_args[@]}" 2>/dev/null | sort)
TOTAL=$(echo "$FILES" | grep -c . || echo 0)

echo "Starting $OPERATION on $TOTAL files..."
echo "Manifest: $MANIFEST_PATH"
echo ""

SUCCESS=0
ERRORS=0
COUNT=0

process_file() {
    local filepath="$1"
    local filename
    filename=$(basename "$filepath")
    local dir
    dir=$(dirname "$filepath")

    case "$OPERATION" in
        rename)
            local new_name
            new_name=$(echo "$filename" | sed "$PATTERN")
            if [[ "$filename" != "$new_name" ]]; then
                if mv "$filepath" "$dir/$new_name" 2>/dev/null; then
                    echo "{\"action\":\"rename\",\"from\":\"$filepath\",\"to\":\"$dir/$new_name\"}" >> "$ACTIONS_TMP"
                    return 0
                else
                    echo "{\"file\":\"$filepath\",\"error\":\"rename failed\"}" >> "$ERRORS_TMP"
                    return 1
                fi
            fi
            ;;

        move|organize)
            local target_dir
            case "$BY" in
                ext)
                    local ext="${filename##*.}"
                    ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
                    target_dir="$DEST/$ext"
                    ;;
                date)
                    local mod_date
                    if [[ "$(uname)" == "Darwin" ]]; then
                        mod_date=$(stat -f "%Sm" -t "%Y/%m" "$filepath")
                    else
                        mod_date=$(stat -c "%y" "$filepath" | cut -d'-' -f1-2 | tr '-' '/')
                    fi
                    target_dir="$DEST/$mod_date"
                    ;;
                type)
                    local mime
                    mime=$(file -b --mime-type "$filepath" 2>/dev/null || echo "unknown/unknown")
                    local category
                    category=$(echo "$mime" | cut -d'/' -f1)
                    target_dir="$DEST/$category"
                    ;;
                *)
                    target_dir="$DEST"
                    ;;
            esac

            mkdir -p "$target_dir"

            # Handle name collisions
            local target_path="$target_dir/$filename"
            if [[ -e "$target_path" ]]; then
                local base="${filename%.*}"
                local ext="${filename##*.}"
                local counter=1
                while [[ -e "$target_dir/${base}_${counter}.${ext}" ]]; do
                    counter=$((counter + 1))
                done
                target_path="$target_dir/${base}_${counter}.${ext}"
            fi

            if mv "$filepath" "$target_path" 2>/dev/null; then
                echo "{\"action\":\"move\",\"from\":\"$filepath\",\"to\":\"$target_path\"}" >> "$ACTIONS_TMP"
                return 0
            else
                echo "{\"file\":\"$filepath\",\"error\":\"move failed\"}" >> "$ERRORS_TMP"
                return 1
            fi
            ;;

        copy)
            mkdir -p "$DEST"
            local target_path="$DEST/$filename"
            if [[ -e "$target_path" ]]; then
                local base="${filename%.*}"
                local ext="${filename##*.}"
                local counter=1
                while [[ -e "$DEST/${base}_${counter}.${ext}" ]]; do
                    counter=$((counter + 1))
                done
                target_path="$DEST/${base}_${counter}.${ext}"
            fi

            if cp "$filepath" "$target_path" 2>/dev/null; then
                echo "{\"action\":\"copy\",\"from\":\"$filepath\",\"to\":\"$target_path\"}" >> "$ACTIONS_TMP"
                return 0
            else
                echo "{\"file\":\"$filepath\",\"error\":\"copy failed\"}" >> "$ERRORS_TMP"
                return 1
            fi
            ;;
    esac
}

echo "$FILES" | while IFS= read -r filepath; do
    [[ -z "$filepath" ]] && continue
    COUNT=$((COUNT + 1))

    if process_file "$filepath"; then
        SUCCESS=$((SUCCESS + 1))
    else
        ERRORS=$((ERRORS + 1))
    fi

    # Progress report
    if [[ $((COUNT % BATCH_SIZE)) -eq 0 ]]; then
        echo "  Progress: $COUNT / $TOTAL ($SUCCESS ok, $ERRORS errors)"
    fi
done

# Build final manifest
ACTIONS_JSON="["
FIRST=true
while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    if [[ "$FIRST" == true ]]; then
        ACTIONS_JSON+="$line"
        FIRST=false
    else
        ACTIONS_JSON+=",$line"
    fi
done < "$ACTIONS_TMP"
ACTIONS_JSON+="]"

ERRORS_JSON="["
FIRST=true
while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    if [[ "$FIRST" == true ]]; then
        ERRORS_JSON+="$line"
        FIRST=false
    else
        ERRORS_JSON+=",$line"
    fi
done < "$ERRORS_TMP"
ERRORS_JSON+="]"

SUCCESS_COUNT=$(grep -c "action" "$ACTIONS_TMP" 2>/dev/null || echo 0)
ERROR_COUNT=$(grep -c "error" "$ERRORS_TMP" 2>/dev/null || echo 0)

cat > "$MANIFEST_PATH" << MANIFESTEOF
{
  "operation": "$OPERATION",
  "source_dir": "$SOURCE_DIR",
  "timestamp": "$TIMESTAMP",
  "filter": "$FILTER",
  "total_files": $TOTAL,
  "success_count": $SUCCESS_COUNT,
  "error_count": $ERROR_COUNT,
  "actions": $ACTIONS_JSON,
  "errors": $ERRORS_JSON
}
MANIFESTEOF

echo ""
echo "═══════════════════════════════════════════════════"
echo "  COMPLETE"
echo "═══════════════════════════════════════════════════"
echo "  Total:     $TOTAL files"
echo "  Success:   $SUCCESS_COUNT"
echo "  Errors:    $ERROR_COUNT"
echo "  Manifest:  $MANIFEST_PATH"
echo ""
echo "  To undo: undo_operation.sh $MANIFEST_PATH"
echo "═══════════════════════════════════════════════════"
