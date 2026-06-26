#!/bin/bash
# Lineage Code Mini — OpenClaw Skill Setup
# Creates data directories and ensures the npm package is available

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$SKILL_DIR/data"
PROFILES_DIR="$DATA_DIR/profiles"

mkdir -p "$DATA_DIR" "$PROFILES_DIR"

# Initialize empty interaction history if it doesn't exist
if [ ! -f "$DATA_DIR/interactions.json" ]; then
  echo "[]" > "$DATA_DIR/interactions.json"
  echo "Initialized interaction history at $DATA_DIR/interactions.json"
fi

# Check if lineage-code-mini is installed
if ! node --input-type=module -e "await import('lineage-code-mini')" 2>/dev/null; then
  echo "Installing lineage-code-mini..."
  npm install -g lineage-code-mini
fi

echo "Lineage Code Mini skill ready."
