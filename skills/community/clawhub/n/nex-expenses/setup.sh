#!/usr/bin/env bash
# Nex Expenses - Setup Script
# MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
#
# Idempotent installer. Safe to run multiple times.
# Usage: bash setup.sh

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$HOME/.nex-expenses"
VENV_DIR="$DATA_DIR/venv"
BIN_DIR="$HOME/.local/bin"

echo "============================================"
echo "  Nex Expenses - Setup"
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

# Step 2: Create data directory and subdirectories
echo "[2/6] Creating data directories..."
mkdir -p "$DATA_DIR"
mkdir -p "$DATA_DIR/receipts"
mkdir -p "$DATA_DIR/exports"

if [ "$PLATFORM" != "windows" ]; then
    chmod 700 "$DATA_DIR"
fi
echo "  Data directory: $DATA_DIR"

# Step 3: Create virtual environment
echo "[3/6] Setting up Python virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON -m venv "$VENV_DIR"
    echo "  Created venv at $VENV_DIR"
else
    echo "  Venv already exists at $VENV_DIR"
fi

# Activate venv and install deps
VENV_PIP="$VENV_DIR/bin/pip"
VENV_PYTHON="$VENV_DIR/bin/python"
if [ "$PLATFORM" = "windows" ]; then
    VENV_PIP="$VENV_DIR/Scripts/pip"
    VENV_PYTHON="$VENV_DIR/Scripts/python"
fi

echo "[4/6] Installing Python dependencies..."
"$VENV_PIP" install --quiet --upgrade pip

# Core dependencies
"$VENV_PIP" install --quiet \
    "Pillow>=9.0"

echo "  Dependencies installed."

# Step 5: Initialize database
echo "[5/6] Initializing database..."
PYTHONPATH="$SKILL_DIR/lib" "$VENV_PYTHON" -c "
import sys; sys.path.insert(0, '$SKILL_DIR/lib')
from storage import init_db
init_db()
print('  Database ready at $DATA_DIR/expenses.db')
"

# Step 6: Make CLI executable and create symlink
echo "[6/6] Setting up CLI tool..."
chmod +x "$SKILL_DIR/nex-expenses.py"

# Create wrapper script that uses the venv python
mkdir -p "$BIN_DIR"
cat > "$BIN_DIR/nex-expenses" << WRAPPER
#!/usr/bin/env bash
exec "$VENV_PYTHON" "$SKILL_DIR/nex-expenses.py" "\$@"
WRAPPER
chmod +x "$BIN_DIR/nex-expenses"
echo "  CLI installed to $BIN_DIR/nex-expenses"

# Check if ~/.local/bin is on PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "  NOTE: Add $BIN_DIR to your PATH:"
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo "  Add this to your ~/.bashrc or ~/.zshrc"
fi

echo ""
echo "============================================"
echo "  Nex Expenses installed successfully!"
echo "  Built by Nex AI (nex-ai.be)"
echo "============================================"
echo ""

# Check for Tesseract (optional but recommended)
echo "Checking for optional dependencies..."
if ! command -v tesseract &>/dev/null; then
    echo "  WARNING: Tesseract OCR is not installed."
    echo "  Receipt scanning will not work without it."
    echo ""
    if [ "$PLATFORM" = "linux" ]; then
        echo "  Install Tesseract:"
        echo "    Ubuntu/Debian: sudo apt-get install tesseract-ocr"
        echo "    Fedora/RHEL: sudo dnf install tesseract"
    elif [ "$PLATFORM" = "macos" ]; then
        echo "  Install Tesseract:"
        echo "    brew install tesseract"
    elif [ "$PLATFORM" = "windows" ]; then
        echo "  Install Tesseract from:"
        echo "    https://github.com/UB-Mannheim/tesseract/wiki"
    fi
    echo ""
else
    TESSERACT_VERSION="$(tesseract --version 2>&1 | head -1)"
    echo "  Found Tesseract: $TESSERACT_VERSION"
fi

echo ""
echo "Next steps:"
echo "  1. View available categories:"
echo "     nex-expenses categories"
echo ""
echo "  2. Add your first expense:"
echo "     nex-expenses add --vendor 'Example' --amount 10.00 --btw 21"
echo ""
echo "  3. List your expenses:"
echo "     nex-expenses list"
echo ""
echo "  4. Generate a summary:"
echo "     nex-expenses summary quarterly Q1 2026"
echo ""
