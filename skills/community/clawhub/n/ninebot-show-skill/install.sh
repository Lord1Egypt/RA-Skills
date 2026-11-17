#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-current}"
NAME="ninebot-show-skill"

case "$TARGET" in
  current)
    DEST_DIR="$SRC_DIR"
    ;;
  claude)
    DEST_DIR="$HOME/.claude/skills/$NAME"
    ;;
  hermes)
    DEST_DIR="$HOME/.hermes/skills/$NAME"
    ;;
  openclaw)
    DEST_DIR="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}/skills/$NAME"
    ;;
  agents)
    DEST_DIR="$HOME/.agents/skills/$NAME"
    ;;
  *)
    echo "用法: bash install.sh [current|claude|hermes|openclaw|agents]" >&2
    exit 2
    ;;
esac

if [[ "$SRC_DIR" != "$DEST_DIR" ]]; then
  mkdir -p "$(dirname "$DEST_DIR")"
  mkdir -p "$DEST_DIR"
  cp -a "$SRC_DIR/." "$DEST_DIR/"
fi

bash "$DEST_DIR/scripts/setup.sh"

echo
echo "Ninebot Show Skill 已准备完成: $DEST_DIR"
