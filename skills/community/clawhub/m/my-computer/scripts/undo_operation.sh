#!/bin/bash
# undo_operation.sh — Reverse a batch operation using its manifest
#
# Usage:
#   undo_operation.sh <manifest_path> [--dry-run]
#
# Options:
#   --dry-run   Show what would be undone without doing it
#
# Supports undoing: rename, move, organize, copy (copy undo = delete the copies)

set -euo pipefail

MANIFEST="${1:-}"
DRY_RUN=false

if [[ "${2:-}" == "--dry-run" ]]; then
    DRY_RUN=true
fi

if [[ -z "$MANIFEST" || ! -f "$MANIFEST" ]]; then
    echo "Usage: undo_operation.sh <manifest_path> [--dry-run]" >&2
    echo "  Manifest file not found: ${MANIFEST:-<none>}" >&2
    exit 1
fi

# Check for jq or use python as fallback
if command -v jq &>/dev/null; then
    JSON_TOOL="jq"
elif command -v python3 &>/dev/null; then
    JSON_TOOL="python3"
else
    echo "Error: Requires jq or python3 to parse manifest" >&2
    exit 1
fi

json_get() {
    local key="$1"
    if [[ "$JSON_TOOL" == "jq" ]]; then
        jq -r "$key" "$MANIFEST"
    else
        python3 -c "import json,sys; d=json.load(open('$MANIFEST')); print(eval(f'$key'.replace('.','[\"').replace(']',']\"]').replace('\"\"','\"')))" 2>/dev/null || echo ""
    fi
}

json_array_len() {
    local key="$1"
    if [[ "$JSON_TOOL" == "jq" ]]; then
        jq "$key | length" "$MANIFEST"
    else
        python3 -c "import json; d=json.load(open('$MANIFEST')); print(len(d['actions']))"
    fi
}

OPERATION=$(json_get '.operation')
TIMESTAMP=$(json_get '.timestamp')
ACTION_COUNT=$(json_array_len '.actions')

echo "═══════════════════════════════════════════════════"
if [[ "$DRY_RUN" == true ]]; then
    echo "  UNDO DRY RUN"
else
    echo "  UNDO OPERATION"
fi
echo "═══════════════════════════════════════════════════"
echo "  Operation:  $OPERATION"
echo "  Timestamp:  $TIMESTAMP"
echo "  Actions:    $ACTION_COUNT to reverse"
echo "───────────────────────────────────────────────────"
echo ""

SUCCESS=0
ERRORS=0

# Process actions in reverse order
for ((i=ACTION_COUNT-1; i>=0; i--)); do
    if [[ "$JSON_TOOL" == "jq" ]]; then
        ACTION=$(jq -r ".actions[$i].action" "$MANIFEST")
        FROM=$(jq -r ".actions[$i].from" "$MANIFEST")
        TO=$(jq -r ".actions[$i].to" "$MANIFEST")
    else
        ACTION=$(python3 -c "import json; d=json.load(open('$MANIFEST')); print(d['actions'][$i]['action'])")
        FROM=$(python3 -c "import json; d=json.load(open('$MANIFEST')); print(d['actions'][$i]['from'])")
        TO=$(python3 -c "import json; d=json.load(open('$MANIFEST')); print(d['actions'][$i]['to'])")
    fi

    case "$ACTION" in
        rename|move)
            # Undo by moving back: to -> from
            if [[ "$DRY_RUN" == true ]]; then
                echo "  Would move: $TO"
                echo "        back: $FROM"
            else
                # Ensure parent directory exists
                mkdir -p "$(dirname "$FROM")"
                if mv "$TO" "$FROM" 2>/dev/null; then
                    SUCCESS=$((SUCCESS + 1))
                else
                    echo "  ERROR: Failed to move $TO -> $FROM" >&2
                    ERRORS=$((ERRORS + 1))
                fi
            fi
            ;;

        copy)
            # Undo by removing the copy
            if [[ "$DRY_RUN" == true ]]; then
                echo "  Would delete copy: $TO"
            else
                if rm "$TO" 2>/dev/null; then
                    SUCCESS=$((SUCCESS + 1))
                else
                    echo "  ERROR: Failed to remove $TO" >&2
                    ERRORS=$((ERRORS + 1))
                fi
            fi
            ;;

        *)
            echo "  WARNING: Unknown action '$ACTION', skipping" >&2
            ;;
    esac
done

# Clean up empty directories left behind (for move/organize operations)
if [[ "$DRY_RUN" == false && ("$OPERATION" == "move" || "$OPERATION" == "organize") ]]; then
    DEST_DIR=$(json_get '.actions[0].to' | xargs dirname 2>/dev/null || echo "")
    if [[ -n "$DEST_DIR" && -d "$DEST_DIR" ]]; then
        find "$DEST_DIR" -type d -empty -delete 2>/dev/null || true
    fi
fi

echo ""
echo "───────────────────────────────────────────────────"
if [[ "$DRY_RUN" == true ]]; then
    echo "  Dry run complete. No changes made."
else
    echo "  Reversed:  $SUCCESS actions"
    echo "  Errors:    $ERRORS"
    if [[ $ERRORS -eq 0 ]]; then
        echo ""
        echo "  Undo complete. Manifest preserved at:"
        echo "  $MANIFEST"
    fi
fi
echo "═══════════════════════════════════════════════════"
