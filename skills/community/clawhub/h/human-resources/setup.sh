#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_URL="https://github.com/anthropics/knowledge-work-plugins.git"
TMP_DIR="$(mktemp -d)"

cleanup() { rm -rf "$TMP_DIR"; }
trap cleanup EXIT

echo "Fetching dependencies from ${REPO_URL%.git}..."

git clone --depth 1 --quiet "$REPO_URL" "$TMP_DIR"

for dir in "$TMP_DIR/human-resources/skills"/*/; do
  name="$(basename "$dir")"
  mkdir -p "$SKILL_DIR/sub-skills/$name"
  cp "$dir/SKILL.md" "$SKILL_DIR/sub-skills/$name/SKILL.md"
  echo "  + $name"
done

cp "$TMP_DIR/human-resources/CONNECTORS.md" "$SKILL_DIR/CONNECTORS.md"
cp "$TMP_DIR/LICENSE" "$SKILL_DIR/LICENSE"
echo "  + CONNECTORS.md"
echo "  + LICENSE"

echo "Done."
