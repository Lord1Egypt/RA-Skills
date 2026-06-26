#!/bin/bash
# batch_preview.sh — Generate a dry-run preview of a batch file operation
#
# Usage:
#   batch_preview.sh <operation> <source_dir> [options]
#
# Operations:
#   rename    - Preview file renaming (requires --pattern)
#   move      - Preview file moves (requires --dest)
#   organize  - Preview organization by type/date (requires --dest and --by)
#
# Options:
#   --pattern <sed_expr>   Rename pattern (sed expression)
#   --dest <dir>           Destination directory
#   --by <type|date|ext>   Organization method
#   --filter <glob>        File filter (e.g., "*.jpg")
#   --limit <n>            Max files to preview (default: 10)
#   --recursive            Include subdirectories
#
# Examples:
#   batch_preview.sh rename ./invoices --pattern 's/invoice_/INV-2025-/' --filter "*.pdf"
#   batch_preview.sh move ./downloads --dest ./organized --by ext
#   batch_preview.sh organize ~/Photos --dest ~/Photos/Sorted --by date --filter "*.jpg"

set -euo pipefail

OPERATION="${1:-}"
SOURCE_DIR="${2:-}"
PATTERN=""
DEST=""
BY=""
FILTER="*"
LIMIT=10
RECURSIVE=false

shift 2 2>/dev/null || true

while [[ $# -gt 0 ]]; do
    case "$1" in
        --pattern)  PATTERN="$2"; shift 2 ;;
        --dest)     DEST="$2"; shift 2 ;;
        --by)       BY="$2"; shift 2 ;;
        --filter)   FILTER="$2"; shift 2 ;;
        --limit)    LIMIT="$2"; shift 2 ;;
        --recursive) RECURSIVE=true; shift ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

if [[ -z "$OPERATION" || -z "$SOURCE_DIR" ]]; then
    echo "Usage: batch_preview.sh <operation> <source_dir> [options]" >&2
    exit 1
fi

if [[ ! -d "$SOURCE_DIR" ]]; then
    echo "Error: Source directory does not exist: $SOURCE_DIR" >&2
    exit 1
fi

# Find files
find_args=("$SOURCE_DIR")
if [[ "$RECURSIVE" == false ]]; then
    find_args+=("-maxdepth" "1")
fi
find_args+=("-type" "f" "-name" "$FILTER")

FILES=$(find "${find_args[@]}" 2>/dev/null | sort)
TOTAL=$(echo "$FILES" | grep -c . || echo 0)

echo "═══════════════════════════════════════════════════"
echo "  DRY RUN PREVIEW — $OPERATION"
echo "═══════════════════════════════════════════════════"
echo ""
echo "  Source:    $SOURCE_DIR"
echo "  Filter:    $FILTER"
echo "  Total:     $TOTAL files found"
echo "  Showing:   first $LIMIT"
echo ""
echo "───────────────────────────────────────────────────"

COUNT=0
echo "$FILES" | head -n "$LIMIT" | while IFS= read -r filepath; do
    [[ -z "$filepath" ]] && continue
    COUNT=$((COUNT + 1))
    filename=$(basename "$filepath")

    case "$OPERATION" in
        rename)
            if [[ -z "$PATTERN" ]]; then
                echo "Error: --pattern required for rename" >&2
                exit 1
            fi
            new_name=$(echo "$filename" | sed "$PATTERN")
            if [[ "$filename" == "$new_name" ]]; then
                echo "  [$COUNT] $filename  (unchanged)"
            else
                echo "  [$COUNT] $filename"
                echo "    → $new_name"
            fi
            ;;

        move|organize)
            if [[ -z "$DEST" ]]; then
                echo "Error: --dest required for $OPERATION" >&2
                exit 1
            fi

            case "$BY" in
                ext)
                    ext="${filename##*.}"
                    ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
                    target="$DEST/$ext/"
                    ;;
                date)
                    if [[ "$(uname)" == "Darwin" ]]; then
                        mod_date=$(stat -f "%Sm" -t "%Y/%m" "$filepath")
                    else
                        mod_date=$(stat -c "%y" "$filepath" | cut -d'-' -f1-2 | tr '-' '/')
                    fi
                    target="$DEST/$mod_date/"
                    ;;
                type)
                    mime=$(file -b --mime-type "$filepath" 2>/dev/null || echo "unknown")
                    category=$(echo "$mime" | cut -d'/' -f1)
                    target="$DEST/$category/"
                    ;;
                *)
                    target="$DEST/"
                    ;;
            esac

            echo "  [$COUNT] $filename"
            echo "    → $target$filename"
            ;;

        *)
            echo "Error: Unknown operation: $OPERATION" >&2
            exit 1
            ;;
    esac
done

echo ""
echo "───────────────────────────────────────────────────"
if [[ "$TOTAL" -gt "$LIMIT" ]]; then
    REMAINING=$((TOTAL - LIMIT))
    echo "  ... and $REMAINING more files"
fi
echo ""
echo "  This is a preview only. No files were modified."
echo "═══════════════════════════════════════════════════"
