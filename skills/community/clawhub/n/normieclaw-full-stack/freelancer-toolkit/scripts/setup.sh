#!/usr/bin/env bash
set -euo pipefail

# Freelancer Toolkit — Setup Script
# Creates data directory and initializes default config files.

DATA_DIR="$HOME/.freelancer-toolkit"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$(dirname "$SCRIPT_DIR")/config"

echo "🛠  Freelancer Toolkit Setup"
echo "================================"

# Check for jq
if ! command -v jq &>/dev/null; then
    echo ""
    echo "⚠️  'jq' is required but not installed."
    echo "   Install it with:"
    if [[ "$(uname)" == "Darwin" ]]; then
        echo "     brew install jq"
    else
        echo "     sudo apt-get install jq  (Debian/Ubuntu)"
        echo "     sudo yum install jq      (RHEL/CentOS)"
    fi
    echo ""
    read -rp "Attempt to install jq now? (y/N): " install_jq
    if [[ "$install_jq" =~ ^[Yy]$ ]]; then
        if [[ "$(uname)" == "Darwin" ]] && command -v brew &>/dev/null; then
            brew install jq
        elif command -v apt-get &>/dev/null; then
            sudo apt-get install -y jq
        elif command -v yum &>/dev/null; then
            sudo yum install -y jq
        else
            echo "❌ Could not detect package manager. Install jq manually and re-run."
            exit 1
        fi
    else
        echo "❌ jq is required. Install it and re-run setup."
        exit 1
    fi
fi

# Create data directory
if [[ -d "$DATA_DIR" ]]; then
    echo "📁 Data directory already exists: $DATA_DIR"
else
    mkdir -p "$DATA_DIR/exports"
    echo "📁 Created: $DATA_DIR"
    echo "📁 Created: $DATA_DIR/exports"
fi

# Initialize settings.json (never overwrite existing)
if [[ -f "$DATA_DIR/settings.json" ]]; then
    echo "⚙️  settings.json already exists — skipping (your config is preserved)"
else
    cp "$CONFIG_DIR/settings.json" "$DATA_DIR/settings.json"
    echo "⚙️  Created default settings.json"
fi

# Initialize data files
for file in clients.json projects.json time-entries.json; do
    if [[ -f "$DATA_DIR/$file" ]]; then
        echo "📄 $file already exists — skipping"
    else
        echo "[]" > "$DATA_DIR/$file"
        echo "📄 Created $file"
    fi
done

# Initialize timer state
if [[ -f "$DATA_DIR/timers.json" ]]; then
    echo "⏱  timers.json already exists — skipping"
else
    echo '{"active": false}' > "$DATA_DIR/timers.json"
    echo "⏱  Created timers.json"
fi

# Set permissions
chmod 700 "$DATA_DIR"
chmod 600 "$DATA_DIR"/*.json
echo "🔒 Set directory permissions (700) and file permissions (600)"

# Create exports directory if missing
mkdir -p "$DATA_DIR/exports"

echo ""
echo "✅ Freelancer Toolkit is ready!"
echo "   Data directory: $DATA_DIR"
echo ""
echo "Next steps:"
echo "  1. Tell your agent to run the setup prompt"
echo "  2. Configure your default rate and first client"
echo "  3. Start logging: \"I worked 3 hours on [project] today\""
echo ""
