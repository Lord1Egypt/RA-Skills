#!/bin/bash
# Installation script for Pretty Mermaid skill

echo "Installing Pretty Mermaid skill dependencies..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed."
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed."
    exit 1
fi

# Install mermaid-cli globally
echo "Installing @mermaid-js/mermaid-cli..."
npm install -g @mermaid-js/mermaid-cli

# Check installation
if command -v mmdc &> /dev/null; then
    echo "✓ mermaid-cli installed successfully"
    mmdc --version
else
    echo "✗ Failed to install mermaid-cli"
    exit 1
fi

# Install Python dependencies if needed
if command -v python3 &> /dev/null; then
    echo "Checking Python dependencies..."
    python3 -c "import argparse, subprocess, tempfile, os, json, sys" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✓ Python dependencies are satisfied"
    else
        echo "Note: Some Python modules may need to be installed"
    fi
else
    echo "Note: Python 3 is not installed, but not required for basic usage"
fi

echo ""
echo "Installation complete!"
echo ""
echo "Quick start:"
echo "1. Generate a basic flowchart:"
echo "   python3 skills/pretty-mermaid/scripts/mermaid-gen.py --type flowchart --output diagram.png"
echo ""
echo "2. Generate with custom theme:"
echo "   python3 skills/pretty-mermaid/scripts/mermaid-gen.py --type sequence --output seq.png --theme dark"
echo ""
echo "3. Use mermaid-cli directly:"
echo "   mmdc -i examples/basic-flowchart.mmd -o output.png -t forest"
echo ""
echo "For more options, see SKILL.md or run:"
echo "   python3 skills/pretty-mermaid/scripts/mermaid-gen.py --help"