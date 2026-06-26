#!/bin/bash

# MIT Reasoning Framework Installer
# Quick setup for using MIT Reasoning locally

set -e

echo "======================================"
echo "MIT Reasoning Framework Installer"
echo "======================================"
echo ""

# Define install directory
INSTALL_DIR="$HOME/.mit-reasoning"

# Create directory
echo "Creating installation directory at $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"

# Copy files
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Copying framework files..."
cp "$SCRIPT_DIR/SKILL.md" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/USAGE.md" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/README.md" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/install.sh" "$INSTALL_DIR/"

echo ""
echo "======================================"
echo "Installation Complete!"
echo "======================================"
echo ""
echo "Framework installed at: $INSTALL_DIR"
echo ""
echo "Getting Started:"
echo ""
echo "1. For Claude Code users:"
echo "   Copy SKILL.md to your .claude/skills/ directory"
echo "   Then invoke: /mit-reasoning decision=\"Your decision here\""
echo ""
echo "2. For ChatGPT users:"
echo "   Copy SKILL.md prompt, paste into ChatGPT"
echo "   Then ask: \"Analyze this using MIT Reasoning: [decision]\""
echo ""
echo "3. For local models (Ollama):"
echo "   ollama run mistral < $INSTALL_DIR/SKILL.md"
echo "   Then paste your decision"
echo ""
echo "4. For API integration:"
echo "   See USAGE.md for Python examples"
echo ""
echo "Full documentation:"
echo "   - README.md     - Overview and features"
echo "   - SKILL.md      - The reasoning framework (the actual prompt)"
echo "   - USAGE.md      - Detailed integration guide with examples"
echo ""
echo "Quick start:"
echo "   less $INSTALL_DIR/USAGE.md"
echo ""
echo "======================================"
