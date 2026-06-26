#!/usr/bin/env bash
# Install Nous from GitHub
# Usage: bash install.sh

set -euo pipefail

REPO="https://github.com/dario-github/nous.git"
INSTALL_DIR="${NOUS_INSTALL_DIR:-$HOME/.nous}"

echo "🧠 Installing Nous — Ontology-Driven Agent Safety Engine"
echo "=================================================="

# Check Python version
python3 -c "import sys; assert sys.version_info >= (3, 11), f'Python 3.11+ required, got {sys.version}'" 2>/dev/null || {
    echo "❌ Python 3.11+ is required"
    exit 1
}

# Clone or update
if [ -d "$INSTALL_DIR" ]; then
    echo "📦 Updating existing installation..."
    cd "$INSTALL_DIR"
    git pull --ff-only 2>/dev/null || {
        echo "⚠️  git pull failed, doing fresh clone..."
        cd /tmp
        rm -rf "$INSTALL_DIR"
        git clone "$REPO" "$INSTALL_DIR"
        cd "$INSTALL_DIR"
    }
else
    echo "📦 Cloning from GitHub..."
    git clone "$REPO" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# Install with cozo support (recommended for knowledge graph)
echo "📦 Installing Python package..."
pip install -e ".[cozo]" 2>/dev/null || {
    echo "⚠️  cozo-embedded install failed (expected on some platforms)"
    echo "📦 Installing without KG support..."
    pip install -e .
}

# Verify
python3 -c "from nous.gate import evaluate_request; print('✅ Nous installed successfully')" 2>/dev/null || {
    echo "❌ Installation verification failed"
    exit 1
}

echo ""
echo "✅ Nous installed at: $INSTALL_DIR"
echo ""
echo "Quick start:"
echo "  from nous.gate import evaluate_request"
echo "  result = evaluate_request(action='send_email', target='user', content='hello')"
echo ""
echo "Shadow mode (default) — observe and log, no blocking."
echo "Edit $INSTALL_DIR/config.yaml to switch to primary mode."
