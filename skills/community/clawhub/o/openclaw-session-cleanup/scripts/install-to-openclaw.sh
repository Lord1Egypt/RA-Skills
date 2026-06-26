#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/NeoCh3n/openclaw-session-cleanup-skill.git}"
SKILL_NAME="${SKILL_NAME:-openclaw-session-cleanup}"
TARGET_ROOT="${OPENCLAW_SKILLS_DIR:-$HOME/.openclaw/skills}"
TARGET_DIR="$TARGET_ROOT/$SKILL_NAME"
TMP_DIR="$(mktemp -d)"
SOURCE_DIR=""

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

mkdir -p "$TARGET_ROOT"

if [ -d "$REPO_URL" ]; then
  SOURCE_DIR="$REPO_URL"
else
  if command -v git >/dev/null 2>&1; then
    git clone --depth=1 "$REPO_URL" "$TMP_DIR/repo" >/dev/null 2>&1
    SOURCE_DIR="$TMP_DIR/repo"
  else
    echo "git is required for installation." >&2
    exit 1
  fi
fi

rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR"

cp -R \
  "$SOURCE_DIR/SKILL.md" \
  "$SOURCE_DIR/docs" \
  "$SOURCE_DIR/scripts" \
  "$SOURCE_DIR/templates" \
  "$TARGET_DIR"/

echo "Installed $SKILL_NAME to:"
echo "  $TARGET_DIR"
echo
echo "Next steps:"
echo "  1. Start a new OpenClaw session, or restart the gateway."
echo "  2. Ask OpenClaw to diagnose session buildup or gateway instability."
