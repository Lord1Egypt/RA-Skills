#!/bin/bash
set -euo pipefail
umask 077

# ============================================================
# Content Creator Pro — Calendar Export Script
# Exports a weekly content calendar JSON to markdown or CSV
# ============================================================
# Usage: ./export-calendar.sh [YYYY-MM-DD] [format]
#   YYYY-MM-DD  — Week start date (default: most recent calendar)
#   format      — "markdown" (default) or "csv"
# ============================================================

# --- Workspace root detection ---
WORKSPACE_ROOT=$(pwd)
while [ "$WORKSPACE_ROOT" != "/" ]; do
  [ -f "$WORKSPACE_ROOT/AGENTS.md" ] || [ -f "$WORKSPACE_ROOT/SOUL.md" ] && break
  WORKSPACE_ROOT=$(dirname "$WORKSPACE_ROOT")
done

if [ "$WORKSPACE_ROOT" = "/" ]; then
  echo "ERROR: Could not find workspace root. Make sure AGENTS.md or SOUL.md exists." >&2
  exit 1
fi

DATA_DIR="$WORKSPACE_ROOT/data"
CALENDAR_DIR="$DATA_DIR/content-calendar"
OUTPUT_DIR="$WORKSPACE_ROOT/exports"

# --- Validate data directory ---
if [ ! -d "$CALENDAR_DIR" ]; then
  echo "ERROR: Calendar directory not found at $CALENDAR_DIR" >&2
  echo "Run setup first — see SETUP-PROMPT.md" >&2
  exit 1
fi

# --- Parse arguments ---
DATE="${1:-}"
FORMAT="${2:-markdown}"

validate_date() {
  local value="$1"
  [[ "$value" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]
}

# If no date provided, find the most recent calendar file
if [ -z "$DATE" ]; then
  LATEST=$(find "$CALENDAR_DIR" -maxdepth 1 -type f -name '????-??-??.json' -print | sort -r | head -1)
  if [ -z "$LATEST" ]; then
    echo "ERROR: No calendar files found in $CALENDAR_DIR" >&2
    exit 1
  fi
  CALENDAR_FILE="$LATEST"
  DATE=$(basename "$LATEST" .json)
  if ! validate_date "$DATE"; then
    echo "ERROR: Most recent calendar file has unexpected name format: $DATE" >&2
    exit 1
  fi
else
  if ! validate_date "$DATE"; then
    echo "ERROR: Date must be in YYYY-MM-DD format. Got: $DATE" >&2
    exit 1
  fi
  CALENDAR_FILE="$CALENDAR_DIR/$DATE.json"
  if [ ! -f "$CALENDAR_FILE" ]; then
    echo "ERROR: Calendar file not found: $CALENDAR_FILE" >&2
    exit 1
  fi
fi

# --- Validate format ---
if [ "$FORMAT" != "markdown" ] && [ "$FORMAT" != "csv" ]; then
  echo "ERROR: Format must be 'markdown' or 'csv'. Got: $FORMAT" >&2
  exit 1
fi

# --- Check for jq ---
if ! command -v jq &>/dev/null; then
  echo "ERROR: jq is required but not installed. Install with: brew install jq (macOS) or apt install jq (Linux)" >&2
  exit 1
fi

# --- Create output directory ---
mkdir -p "$OUTPUT_DIR"

# --- Export ---
if [ "$FORMAT" = "markdown" ]; then
  OUTPUT_FILE="$OUTPUT_DIR/calendar-$DATE.md"
  if [ -L "$OUTPUT_FILE" ]; then
    echo "ERROR: Refusing to write to symlinked output file: $OUTPUT_FILE" >&2
    exit 1
  fi
  if [ -e "$OUTPUT_FILE" ] && [ ! -f "$OUTPUT_FILE" ]; then
    echo "ERROR: Output path exists but is not a regular file: $OUTPUT_FILE" >&2
    exit 1
  fi

  echo "# Content Calendar — Week of $DATE" > "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"
  echo "Exported: $(date '+%Y-%m-%d %H:%M')" >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"

  # Extract posts and format as markdown
  jq -r '.posts | sort_by(.date, .time) | group_by(.date)[] | 
    "## " + .[0].date + "\n" +
    (map(
      "- **" + .time + "** | " + .platform + " | " + .topic + "\n" +
      "  - Pillar: " + .pillar_id + "\n" +
      "  - Status: " + .status + "\n" +
      (if .cta then "  - CTA: " + .cta + "\n" else "" end)
    ) | join("\n")) + "\n"' "$CALENDAR_FILE" >> "$OUTPUT_FILE"

  echo "✅ Exported to: $OUTPUT_FILE"

elif [ "$FORMAT" = "csv" ]; then
  OUTPUT_FILE="$OUTPUT_DIR/calendar-$DATE.csv"
  if [ -L "$OUTPUT_FILE" ]; then
    echo "ERROR: Refusing to write to symlinked output file: $OUTPUT_FILE" >&2
    exit 1
  fi
  if [ -e "$OUTPUT_FILE" ] && [ ! -f "$OUTPUT_FILE" ]; then
    echo "ERROR: Output path exists but is not a regular file: $OUTPUT_FILE" >&2
    exit 1
  fi

  echo "Date,Time,Platform,Pillar,Topic,Status,CTA" > "$OUTPUT_FILE"

  jq -r '.posts | sort_by(.date, .time)[] | 
    [.date, .time, .platform, .pillar_id, .topic, .status, (.cta // "")] | 
    @csv' "$CALENDAR_FILE" >> "$OUTPUT_FILE"

  echo "✅ Exported to: $OUTPUT_FILE"
fi
