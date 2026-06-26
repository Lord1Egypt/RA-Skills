#!/usr/bin/env bash
set -euo pipefail

# Project Manager Pro — Setup Script
# Creates the data directory and initializes empty stores.

DATA_DIR="${HOME}/.openclaw/workspace/pm-pro"

echo "🎯 Project Manager Pro — Setup"
echo ""

# Check for jq
if ! command -v jq &>/dev/null; then
    echo "⚠️  jq not found. Installing..."
    if command -v brew &>/dev/null; then
        brew install jq
    elif command -v apt-get &>/dev/null; then
        sudo apt-get install -y jq
    elif command -v dnf &>/dev/null; then
        sudo dnf install -y jq
    else
        echo "❌ Could not install jq automatically."
        echo "   Install it manually: https://jqlang.github.io/jq/download/"
        exit 1
    fi
    echo "✅ jq installed"
fi

# Create data directory
if [ -d "$DATA_DIR" ]; then
    echo "📁 Data directory already exists: $DATA_DIR"
else
    mkdir -p "$DATA_DIR/archive"
    echo "📁 Created data directory: $DATA_DIR"
fi

# Initialize tasks.json
if [ ! -f "$DATA_DIR/tasks.json" ]; then
    echo "[]" > "$DATA_DIR/tasks.json"
    echo "📋 Initialized tasks.json"
else
    TASK_COUNT=$(jq 'length' "$DATA_DIR/tasks.json")
    echo "📋 tasks.json exists ($TASK_COUNT tasks)"
fi

# Initialize projects.json
if [ ! -f "$DATA_DIR/projects.json" ]; then
    echo "[]" > "$DATA_DIR/projects.json"
    echo "📁 Initialized projects.json"
else
    PROJECT_COUNT=$(jq 'length' "$DATA_DIR/projects.json")
    echo "📁 projects.json exists ($PROJECT_COUNT projects)"
fi

# Initialize check-in log
if [ ! -f "$DATA_DIR/check-in-log.json" ]; then
    echo "[]" > "$DATA_DIR/check-in-log.json"
    echo "📝 Initialized check-in-log.json"
else
    echo "📝 check-in-log.json exists"
fi

# Ensure archive directory exists
mkdir -p "$DATA_DIR/archive"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Data directory: $DATA_DIR"
echo "Next step: Start a conversation with your agent to configure preferences."
