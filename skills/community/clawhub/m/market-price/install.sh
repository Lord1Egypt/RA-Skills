#!/bin/bash
set -euo pipefail

SKILL_DIR="${HOME}/.claude/skills/price"
REPO_URL="https://raw.githubusercontent.com/juglans-ai/juglans-price/main"

echo "Installing juglans-price skill..."

mkdir -p "$SKILL_DIR"
curl -fsSL "$REPO_URL/SKILL.md" -o "$SKILL_DIR/SKILL.md"

echo "Installed to $SKILL_DIR"
echo ""
echo "Restart Claude Code, then try:"
echo "  /price BTC"
echo "  /price AAPL"
echo "  /price 0700.HK"
