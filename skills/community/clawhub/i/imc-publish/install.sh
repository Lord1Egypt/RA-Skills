#!/usr/bin/env bash
# imc-publish installer.
# What this script does (nothing else):
#   1. Copies this skill folder to ~/.claude/skills/imc-publish (Claude Code).
#   2. Prints the AGENTS.md snippet for Codex users.
# It does NOT touch credentials, shell profiles, or any other file.
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude/skills/imc-publish"
mkdir -p "$HOME/.claude/skills"
rm -rf "$DEST"
cp -r "$SRC" "$DEST"
rm -f "$DEST/install.sh" "$DEST/uninstall.sh"
echo "Installed to $DEST"
echo
echo "Next: set your workspace publishing key (ask your InstallMyClaw workspace owner):"
echo "  export IMC_PUBLISH_API_KEY=...   # add to your shell profile or secrets manager"
echo
echo "Codex users — add to AGENTS.md:"
echo "  To publish to social channels, follow ~/.claude/skills/imc-publish/SKILL.md"
echo
echo "Test: python3 $DEST/scripts/imc_publish.py accounts"
