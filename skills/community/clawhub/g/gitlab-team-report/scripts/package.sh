#!/bin/bash
# Package the skill into a .skill file (zip with .skill extension)

set -euo pipefail

SKILL_NAME="gitlab-weekly-report"
OUTPUT_DIR="${1:-.}"

cd "$(dirname "$0")/.."
mkdir -p "$OUTPUT_DIR"

PACKAGE_PATH="${OUTPUT_DIR}/${SKILL_NAME}.skill"
rm -f "$PACKAGE_PATH"

# Package only distributable files. Exclude local config, generated outputs,
# caches, and other machine-specific artifacts.
zip -r "$PACKAGE_PATH" \
  SKILL.md \
  scripts \
  config/config.example.json \
  config/classification.rules.example.json \
  templates \
  requirements.txt \
  LICENSE \
  VERSION \
  .gitignore \
  -x "*.DS_Store" \
  -x "*/.git/*" \
  -x "*/__pycache__/*" \
  -x "*.pyc" \
  -x "*.bak" \
  -x "reports/*" \
  -x "config/config.json" \
  -x "config/classification.rules.json"

echo "✅ Packaged: $PACKAGE_PATH"
