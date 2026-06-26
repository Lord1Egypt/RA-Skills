#!/bin/bash
# Export all boards from a specific team as PDFs

set -e

TEAM_ID="${1:-}"
OUTPUT_DIR="${2:-.}"
FORMAT="${3:-pdf}"

if [ -z "$TEAM_ID" ]; then
  echo "Usage: $0 <team-id> [output-dir] [format]"
  echo ""
  echo "Examples:"
  echo "  $0 abc123                      # Export as PDF (default)"
  echo "  $0 abc123 ./exports            # Export to custom directory"
  echo "  $0 abc123 ./exports png        # Export as PNG"
  echo ""
  echo "Formats: pdf, png, svg"
  exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo "📋 Fetching boards from team: $TEAM_ID"

# Get all boards from the team
BOARDS=$(mirocli boards list --team-id "$TEAM_ID" --json 2>/dev/null | jq -r '.[] | "\(.id)|\(.name)"')

if [ -z "$BOARDS" ]; then
  echo "❌ No boards found for team $TEAM_ID"
  exit 1
fi

TOTAL=$(echo "$BOARDS" | wc -l)
COUNT=0

echo "📦 Found $TOTAL boards. Starting export..."
echo ""

# Export each board
while IFS='|' read -r BOARD_ID BOARD_NAME; do
  COUNT=$((COUNT + 1))
  
  # Sanitize filename
  SAFE_NAME=$(echo "$BOARD_NAME" | sed 's/[^a-zA-Z0-9_-]/-/g' | sed 's/-\+/-/g')
  OUTPUT_FILE="$OUTPUT_DIR/${SAFE_NAME}_${BOARD_ID}.${FORMAT}"
  
  echo "[$COUNT/$TOTAL] Exporting: $BOARD_NAME"
  
  if mirocli board-export "$BOARD_ID" --format "$FORMAT" --output "$OUTPUT_FILE" 2>/dev/null; then
    echo "       ✅ Saved to: $OUTPUT_FILE"
  else
    echo "       ❌ Failed to export $BOARD_ID"
  fi
done <<< "$BOARDS"

echo ""
echo "✨ Export complete! Files saved to: $OUTPUT_DIR"
