#!/bin/bash
# NoteTaker Pro — Bulk Export Utility
# Exports notes from data/notes/ to the specified format and directory.
# Usage: ./export-notes.sh [format] [output-dir] [--category CAT] [--tag TAG] [--since DATE]
# Formats: markdown (default), json, single-document

set -euo pipefail

# ── Workspace Root Detection ──
# Walk up from script location to find the workspace root marker
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT=""
CHECK_DIR="$SCRIPT_DIR"
for _ in $(seq 1 10); do
    if [ -f "$CHECK_DIR/AGENTS.md" ] || [ -f "$CHECK_DIR/SOUL.md" ] || [ -f "$CHECK_DIR/.openclaw" ]; then
        WORKSPACE_ROOT="$CHECK_DIR"
        break
    fi
    CHECK_DIR="$(dirname "$CHECK_DIR")"
done

if [ -z "$WORKSPACE_ROOT" ]; then
    echo "ERROR: Could not find workspace root. Make sure this script is inside your agent's workspace."
    exit 1
fi

NOTES_DIR="$WORKSPACE_ROOT/data/notes"
INDEX_FILE="$WORKSPACE_ROOT/data/notes-index.json"
EXPORTS_BASE="$WORKSPACE_ROOT/data/exports"

# ── Argument Parsing ──
FORMAT="${1:-markdown}"
RAW_OUTPUT_DIR="${2:-$EXPORTS_BASE/$(date +%Y-%m-%d)}"
FILTER_CATEGORY=""
FILTER_TAG=""
FILTER_SINCE=""

shift 2 2>/dev/null || true
while [ $# -gt 0 ]; do
    case "$1" in
        --category)
            [ $# -ge 2 ] || { echo "ERROR: --category requires a value"; exit 1; }
            FILTER_CATEGORY="$2"
            shift 2
            ;;
        --tag)
            [ $# -ge 2 ] || { echo "ERROR: --tag requires a value"; exit 1; }
            FILTER_TAG="$2"
            shift 2
            ;;
        --since)
            [ $# -ge 2 ] || { echo "ERROR: --since requires a value"; exit 1; }
            FILTER_SINCE="$2"
            shift 2
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# Resolve output dir to an absolute path and keep exports inside workspace.
if [ "${RAW_OUTPUT_DIR#/}" = "$RAW_OUTPUT_DIR" ]; then
    OUTPUT_DIR="$WORKSPACE_ROOT/$RAW_OUTPUT_DIR"
else
    OUTPUT_DIR="$RAW_OUTPUT_DIR"
fi

OUTPUT_DIR="$(python3 - "$OUTPUT_DIR" <<'PY'
import os, sys
print(os.path.realpath(sys.argv[1]))
PY
)"
EXPORTS_BASE="$(python3 - "$EXPORTS_BASE" <<'PY'
import os, sys
print(os.path.realpath(sys.argv[1]))
PY
)"

case "$OUTPUT_DIR" in
    "$EXPORTS_BASE"|"$EXPORTS_BASE"/*) ;;
    *)
        echo "ERROR: Output directory must be inside $EXPORTS_BASE"
        exit 1
        ;;
esac

# ── Validation ──
if [ ! -d "$NOTES_DIR" ]; then
    echo "ERROR: Notes directory not found at $NOTES_DIR"
    echo "Have you captured any notes yet?"
    exit 1
fi

if [ ! -f "$INDEX_FILE" ]; then
    echo "ERROR: Notes index not found at $INDEX_FILE"
    exit 1
fi

# ── Create Output Directory ──
mkdir -p "$OUTPUT_DIR"
chmod 700 "$OUTPUT_DIR"

NOTE_COUNT=0

# ── Export ──
case "$FORMAT" in
    markdown)
        echo "Exporting notes as Markdown to $OUTPUT_DIR..."
        for note_file in "$NOTES_DIR"/note_*.json; do
            [ -f "$note_file" ] || continue

            # Apply filters using python3 for JSON parsing
            if ! NOTE_FILE="$note_file" FILTER_CATEGORY="$FILTER_CATEGORY" FILTER_TAG="$FILTER_TAG" FILTER_SINCE="$FILTER_SINCE" python3 - <<'PY' 2>/dev/null
import json
import os
import sys

with open(os.environ["NOTE_FILE"], encoding="utf-8") as fh:
    note = json.load(fh)

category = os.environ["FILTER_CATEGORY"]
tag = os.environ["FILTER_TAG"]
since = os.environ["FILTER_SINCE"]

if category and note.get("category", "") != category:
    sys.exit(1)
if tag and tag not in note.get("tags", []):
    sys.exit(1)
if since and note.get("created_at", "") < since:
    sys.exit(1)
PY
            then
                continue
            fi

            # Convert JSON to Markdown
            NOTE_FILE="$note_file" OUTPUT_DIR="$OUTPUT_DIR" python3 - <<'PY'
import json
import os

with open(os.environ["NOTE_FILE"], encoding="utf-8") as fh:
    note = json.load(fh)

category = note.get("category", "uncategorized")
safe_category = "".join(c if c.isalnum() or c in "-_" else "-" for c in str(category).strip().lower())
safe_category = safe_category.strip("-_") or "uncategorized"

output_root = os.path.realpath(os.environ["OUTPUT_DIR"])
category_dir = os.path.realpath(os.path.join(output_root, safe_category))
if not (category_dir == output_root or category_dir.startswith(output_root + os.sep)):
    raise SystemExit("ERROR: Unsafe category path")

os.makedirs(category_dir, exist_ok=True)
os.chmod(category_dir, 0o700)

title = note.get("title", note.get("id", "untitled"))
safe_title = "".join(c if c.isalnum() or c in " -_" else "" for c in title).strip().replace(" ", "-")
if not safe_title:
    safe_title = note.get("id", "untitled")

output_path = os.path.join(category_dir, f"{safe_title}.md")
with open(output_path, "w", encoding="utf-8") as fh:
    fh.write(f"# {title}\n\n")
    fh.write(f"**Date:** {note.get('created_at', 'unknown')}\n")
    fh.write(f"**Category:** {category}\n")
    fh.write(f"**Tags:** {' '.join(note.get('tags', []))}\n")
    fh.write(f"**Priority:** {note.get('priority', 'normal')}\n\n")
    fh.write("---\n\n")
    fh.write(note.get("content_full", note.get("content_summary", "")))
    fh.write("\n")
    items = note.get("action_items", [])
    if items:
        fh.write("\n## Action Items\n\n")
        for item in items:
            done = "✅" if item.get("done") else "⬜"
            fh.write(f"- {done} {item.get('task', '')}\n")

os.chmod(output_path, 0o600)
PY
            NOTE_COUNT=$((NOTE_COUNT + 1))
        done
        ;;

    json)
        echo "Exporting notes as JSON to $OUTPUT_DIR..."
        cp "$NOTES_DIR"/note_*.json "$OUTPUT_DIR/" 2>/dev/null || true
        NOTE_COUNT=$(ls "$OUTPUT_DIR"/note_*.json 2>/dev/null | wc -l | tr -d ' ')
        chmod 600 "$OUTPUT_DIR"/note_*.json 2>/dev/null || true
        ;;

    single-document)
        echo "Exporting notes as single Markdown document..."
        OUTPUT_FILE="$OUTPUT_DIR/all-notes-$(date +%Y-%m-%d).md"
        echo "# NoteTaker Pro — Full Export" > "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "**Exported:** $(date)" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "---" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"

        for note_file in "$NOTES_DIR"/note_*.json; do
            [ -f "$note_file" ] || continue
            NOTE_FILE="$note_file" python3 - <<'PY' >> "$OUTPUT_FILE"
import json
import os

with open(os.environ["NOTE_FILE"], encoding="utf-8") as fh:
    note = json.load(fh)

print(f"## {note.get('title', note.get('id', 'untitled'))}")
print(f"**Date:** {note.get('created_at', 'unknown')} | **Tags:** {' '.join(note.get('tags', []))}")
print()
print(note.get("content_full", note.get("content_summary", "")))
print()
print("---")
print()
PY
            NOTE_COUNT=$((NOTE_COUNT + 1))
        done
        chmod 600 "$OUTPUT_FILE"
        ;;

    *)
        echo "ERROR: Unknown format '$FORMAT'. Use: markdown, json, single-document"
        exit 1
        ;;
esac

echo "✅ Exported $NOTE_COUNT notes to $OUTPUT_DIR"
