#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LIB_DIR="$SKILL_DIR/data/awesome-gpt-image-2-prompts"
CONFIG_FILE="$SKILL_DIR/config.json"
UPSTREAM="https://github.com/EvoLinkAI/awesome-gpt-image-2-prompts.git"

OLD_VERSION=$(jq -r '.prompt_library_version' "$CONFIG_FILE")

# Detect light install: images directory missing or empty
IMAGES_MISSING=false
if [ ! -d "$LIB_DIR/images" ] || [ -z "$(ls -A "$LIB_DIR/images" 2>/dev/null)" ]; then
  IMAGES_MISSING=true
fi

TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

echo "Fetching latest prompt library..."
git clone --depth=1 "$UPSTREAM" "$TMP_DIR" 2>&1 || {
  echo "Error: failed to fetch from upstream. Check your network connection."
  exit 1
}

NEW_VERSION=$(cd "$TMP_DIR" && git rev-parse --short HEAD)

if [ "$OLD_VERSION" = "$NEW_VERSION" ] && [ "$IMAGES_MISSING" = false ]; then
  echo "Prompt library already up to date ($NEW_VERSION)."
  exit 0
fi

if [ "$OLD_VERSION" = "$NEW_VERSION" ] && [ "$IMAGES_MISSING" = true ]; then
  echo "Prompt library text is current ($NEW_VERSION), but images are missing (light install)."
  echo "Downloading full library with images..."
fi

CHANGES=$(cd "$TMP_DIR" && git log -1 --format='%s' 2>/dev/null || echo "")

rm -rf "$TMP_DIR/.git"
rm -rf "$LIB_DIR"
mv "$TMP_DIR" "$LIB_DIR"

# Update config.json
UPDATED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
jq --arg ver "$NEW_VERSION" --arg ts "$UPDATED_AT" \
  '.prompt_library_version = $ver | .prompt_library_updated = $ts' \
  "$CONFIG_FILE" > "${CONFIG_FILE}.tmp" && mv "${CONFIG_FILE}.tmp" "$CONFIG_FILE"

echo "Updated: ${OLD_VERSION} → ${NEW_VERSION}"
if [ "$OLD_VERSION" = "$NEW_VERSION" ]; then
  echo "(Library version unchanged — full images downloaded for previous light install)"
fi
echo ""
if [ -n "$CHANGES" ]; then
  echo "Changelog:"
  echo "$CHANGES" | while read -r line; do
    echo "  • $line"
  done
fi

CASE_COUNT=$(find "$LIB_DIR/cases" -name "*.md" | wc -l | tr -d ' ')
echo ""
echo "Now at ${CASE_COUNT} case files across 7 categories."
