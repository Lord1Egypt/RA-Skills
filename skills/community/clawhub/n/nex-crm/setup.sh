#!/usr/bin/env bash
# Nex CRM - Setup Script
# MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
#
# Idempotent installer. Safe to run multiple times.
# Usage: bash setup.sh

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$HOME/.nex-crm"
EXPORT_DIR="$DATA_DIR/exports"
VENV_DIR="$DATA_DIR/venv"
BIN_DIR="$HOME/.local/bin"

echo "============================================"
echo "  Nex CRM - Setup"
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
if [ "$PLATFORM" != "windows" ]; then
    chmod 700 "$DATA_DIR"
fi
echo "  Data directory: $DATA_DIR"

# Step 3: Create export directory
echo "[3/6] Creating export directory..."
mkdir -p "$EXPORT_DIR"
echo "  Export directory: $EXPORT_DIR"

# Step 4: Create virtual environment
echo "[4/6] Setting up Python virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON -m venv "$VENV_DIR"
    echo "  Created venv at $VENV_DIR"
else
    echo "  Venv already exists at $VENV_DIR"
fi

# Activate venv and set up paths
VENV_PIP="$VENV_DIR/bin/pip"
VENV_PYTHON="$VENV_DIR/bin/python"
if [ "$PLATFORM" = "windows" ]; then
    VENV_PIP="$VENV_DIR/Scripts/pip"
    VENV_PYTHON="$VENV_DIR/Scripts/python"
fi

echo "[5/6] Installing Python dependencies..."
"$VENV_PIP" install --quiet --upgrade pip
# Nex CRM uses stdlib only - no external dependencies
echo "  Environment ready (zero external dependencies)."

# Step 6: Initialize database
echo "[6/6] Initializing database..."
PYTHONPATH="$SKILL_DIR/lib" "$VENV_PYTHON" -c "
import sys; sys.path.insert(0, '$SKILL_DIR/lib')
from storage import init_db
init_db()
print('  Database ready at $DATA_DIR/crm.db')
"

# Make CLI executable and create wrapper script
echo "Setting up CLI tool..."
chmod +x "$SKILL_DIR/nex-crm.py"

# Create wrapper script that uses the venv python
mkdir -p "$BIN_DIR"
cat > "$BIN_DIR/nex-crm" << WRAPPER
#!/usr/bin/env bash
exec "$VENV_PYTHON" "$SKILL_DIR/nex-crm.py" "\$@"
WRAPPER
chmod +x "$BIN_DIR/nex-crm"
echo "  CLI installed to $BIN_DIR/nex-crm"

# Check if ~/.local/bin is on PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "  NOTE: Add $BIN_DIR to your PATH:"
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo "  Add this to your ~/.bashrc or ~/.zshrc"
fi

echo ""
echo "============================================"
echo "  Nex CRM installed successfully!"
echo "  Built by Nex AI (nex-ai.be)"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. Add your first prospect:"
echo "     nex-crm add \"Company Name, Gent\""
echo ""
echo "  2. View your prospects:"
echo "     nex-crm list"
echo ""
echo "  3. Check the pipeline:"
echo "     nex-crm pipeline"
echo ""
