#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
SKILL_DIR_NAME="$(basename "$SCRIPT_DIR")"
OUTPUT_NAME="moneysharks.skill"
OUTPUT_PATH="${PARENT_DIR}/${OUTPUT_NAME}"

cd "$PARENT_DIR"
rm -f "$OUTPUT_PATH"
zip -r "$OUTPUT_PATH" "$SKILL_DIR_NAME" \
  -x "*/.DS_Store" \
  -x "*/__pycache__/*" \
  -x "*/.git/*" \
  -x "*/logs/*.log"

echo "Created: $OUTPUT_PATH"
