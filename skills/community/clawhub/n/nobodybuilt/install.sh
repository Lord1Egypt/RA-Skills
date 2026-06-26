#!/bin/bash
# nobodybuilt installer — works with Claude Code, OpenClaw, and any SKILL.md-compatible agent
set -e

REPO_URL="https://github.com/KeWang0622/nobodybuilt.git"
SKILL_DIR="${HOME}/.claude/skills"
TMPDIR=$(mktemp -d)

git clone --depth 1 "$REPO_URL" "$TMPDIR/nobodybuilt" 2>/dev/null
mkdir -p "$SKILL_DIR"
cp "$TMPDIR/nobodybuilt/SKILL.md" "$SKILL_DIR/nobodybuilt.md"
rm -rf "$TMPDIR"

echo ""
echo "  nobodybuilt installed to ${SKILL_DIR}/nobodybuilt.md"
echo ""
echo "  Usage: tell your agent \"Use nobodybuilt\" or \"Use nobodybuilt. Surprise me.\""
echo ""
