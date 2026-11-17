#!/usr/bin/env bash
# Removes ~/.claude/skills/imc-publish. Does not touch anything else.
set -euo pipefail
rm -rf "$HOME/.claude/skills/imc-publish"
echo "Removed ~/.claude/skills/imc-publish"
