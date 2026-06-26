#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_FILE="$SCRIPT_DIR/SKILL.md"

if [[ ! -f "$SKILL_FILE" ]]; then
  echo "Error: SKILL.md not found at $SKILL_FILE" >&2
  exit 1
fi

# Parse name from SKILL.md frontmatter, version from version.txt
NAME=$(awk '/^---/{f++} f==1 && /^name:/{print $2; exit}' "$SKILL_FILE")
VERSION=$(cat "$SCRIPT_DIR/version.txt" | tr -d '[:space:]')

if [[ -z "$NAME" || -z "$VERSION" ]]; then
  echo "Error: could not parse name from SKILL.md or version from version.txt" >&2
  exit 1
fi

echo "Publishing skill: $NAME @ $VERSION"

clawhub publish "$SCRIPT_DIR" \
  --slug "hum-writer" \
  --name "$NAME" \
  --version "$VERSION" \
  --tags latest
