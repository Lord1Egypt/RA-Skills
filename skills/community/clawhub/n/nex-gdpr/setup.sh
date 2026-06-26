#!/usr/bin/env bash
# Nex GDPR - Setup Script
# MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
#
# Idempotent installer. Safe to run multiple times.
# Usage: bash setup.sh

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$HOME/.nex-gdpr"
VENV_DIR="$DATA_DIR/venv"
BIN_DIR="$HOME/.local/bin"
SCRIPT_NAME="nex-gdpr"

echo "============================================"
echo "  Nex GDPR - Setup"
echo "  Built by Nex AI (nex-ai.be)"
echo "============================================"
echo ""

# Detect OS
OS="$(uname -s)"
case "$OS" in
    Linux*)  PLATFORM="linux";;
    Darwin*) PLATFORM="macos";;
    MINGW*|CYGWIN*|MSYS*) PLATFORM="windows";;
    *)       PLATFORM="unknown";;
esac
echo "Platform: $PLATFORM"
echo "Skill directory: $SKILL_DIR"
echo ""

# Step 1: Check Python
echo "[1/6] Checking Python..."
if command -v python3 &>/dev/null; then
    PYTHON="python3"
elif command -v python &>/dev/null; then
    PYTHON="python"
else
    echo "ERROR: Python 3 is required but not found." >&2
    echo "Install Python 3.9+ from https://python.org" >&2
    exit 1
fi

PY_VERSION="$($PYTHON --version 2>&1)"
echo "  Found: $PY_VERSION"

# Step 2: Create data directory
echo "[2/6] Creating data directory..."
mkdir -p "$DATA_DIR"
mkdir -p "$DATA_DIR/exports"
mkdir -p "$DATA_DIR/audit"
echo "  Created: $DATA_DIR"

# Step 3: Create virtual environment
echo "[3/6] Creating virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON -m venv "$VENV_DIR"
    echo "  Created: $VENV_DIR"
else
    echo "  Already exists: $VENV_DIR"
fi

# Step 4: Activate and install dependencies
echo "[4/6] Installing dependencies..."
source "$VENV_DIR/bin/activate"

# Install required packages
pip install -q --upgrade pip setuptools
pip install -q tabulate

echo "  Installed: tabulate"

# Step 5: Initialize database
echo "[5/6] Initializing database..."
$PYTHON -c "
import sys
sys.path.insert(0, '$SKILL_DIR')
from lib.storage import GDPRStorage
storage = GDPRStorage()
print('  Database initialized at: $DATA_DIR/gdpr.db')
"

# Step 6: Create executable wrapper
echo "[6/6] Creating executable wrapper..."
mkdir -p "$BIN_DIR"

cat > "$BIN_DIR/$SCRIPT_NAME" << 'WRAPPER'
#!/usr/bin/env bash
SKILL_DIR="$(cd "$(dirname "$(dirname "$0")")" && find . -name "nex-gdpr" -type d 2>/dev/null | head -1)"
if [ -z "$SKILL_DIR" ]; then
    SKILL_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
    if [ ! -d "$SKILL_DIR/nex-gdpr" ]; then
        # Try standard location
        SKILL_DIR="$HOME/.local/share/nex-gdpr"
        if [ ! -d "$SKILL_DIR" ]; then
            echo "ERROR: Could not find nex-gdpr skill directory" >&2
            exit 1
        fi
    else
        SKILL_DIR="$SKILL_DIR/nex-gdpr"
    fi
fi

VENV_DIR="$HOME/.nex-gdpr/venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "ERROR: Virtual environment not found at $VENV_DIR" >&2
    echo "Run setup.sh first" >&2
    exit 1
fi

source "$VENV_DIR/bin/activate"
$VENV_DIR/bin/python "$SKILL_DIR/nex-gdpr.py" "$@"
WRAPPER

chmod +x "$BIN_DIR/$SCRIPT_NAME"
echo "  Created: $BIN_DIR/$SCRIPT_NAME"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" == *":$BIN_DIR:"* ]]; then
    echo ""
    echo "Setup complete!"
    echo ""
    echo "Try it out:"
    echo "  nex-gdpr list"
    echo "  nex-gdpr new --type access --name 'Test User' --email 'test@example.be'"
else
    echo ""
    echo "Setup complete, but $BIN_DIR is not in your PATH"
    echo ""
    echo "Add this to your shell profile (~/.bashrc, ~/.zshrc, etc.):"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "Or run directly:"
    echo "  $VENV_DIR/bin/python $SKILL_DIR/nex-gdpr.py list"
fi

echo ""
echo "Data directory: $DATA_DIR"
echo "Database: $DATA_DIR/gdpr.db"
echo "Exports: $DATA_DIR/exports"
echo ""
