#!/usr/bin/env bash
# Nex Vault - Setup Script
# MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
#
# Idempotent installer. Safe to run multiple times.
# Usage: bash setup.sh

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$HOME/.nex-vault"
VENV_DIR="$DATA_DIR/venv"
BIN_DIR="$HOME/.local/bin"
SERVICE_NAME="nex-vault"

echo "============================================"
echo "  Nex Vault - Setup"
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

# Step 2: Check for pdftotext
echo "[2/6] Checking for required tools..."
MISSING_TOOLS=""
if ! command -v pdftotext &>/dev/null; then
    MISSING_TOOLS="pdftotext"
fi
if ! command -v tesseract &>/dev/null; then
    [ -z "$MISSING_TOOLS" ] && MISSING_TOOLS="tesseract" || MISSING_TOOLS="$MISSING_TOOLS, tesseract"
fi

if [ -n "$MISSING_TOOLS" ]; then
    echo "  WARNING: Missing tools: $MISSING_TOOLS"
    echo "  Install them for full document parsing support:"
    if [ "$PLATFORM" = "linux" ]; then
        echo "    sudo apt-get install poppler-utils tesseract-ocr"
    elif [ "$PLATFORM" = "macos" ]; then
        echo "    brew install poppler tesseract"
    fi
    echo "  (The tool will continue with limited functionality)"
fi

# Step 3: Create data directory
echo "[3/6] Creating data directory..."
mkdir -p "$DATA_DIR"
if [ "$PLATFORM" != "windows" ]; then
    chmod 700 "$DATA_DIR"
fi
echo "  Data directory: $DATA_DIR"

# Step 4: Create virtual environment and install deps
echo "[4/6] Setting up Python virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON -m venv "$VENV_DIR"
    echo "  Created venv at $VENV_DIR"
else
    echo "  Venv already exists at $VENV_DIR"
fi

VENV_PIP="$VENV_DIR/bin/pip"
VENV_PYTHON="$VENV_DIR/bin/python"
if [ "$PLATFORM" = "windows" ]; then
    VENV_PIP="$VENV_DIR/Scripts/pip"
    VENV_PYTHON="$VENV_DIR/Scripts/python"
fi

echo "[5/6] Installing Python dependencies..."
"$VENV_PIP" install --quiet --upgrade pip
"$VENV_PIP" install --quiet python-docx Pillow
echo "  Core dependencies installed."

# Step 5: Initialize database
echo "[6/6] Initializing database..."
PYTHONPATH="$SKILL_DIR/lib" "$VENV_PYTHON" -c "
import sys; sys.path.insert(0, '$SKILL_DIR/lib')
from storage import init_db
init_db()
print('  Database ready at $DATA_DIR/vault.db')
"

# Make CLI executable and create symlink
chmod +x "$SKILL_DIR/nex-vault.py"
mkdir -p "$BIN_DIR"
cat > "$BIN_DIR/nex-vault" << WRAPPER
#!/usr/bin/env bash
exec "$VENV_PYTHON" "$SKILL_DIR/nex-vault.py" "\$@"
WRAPPER
chmod +x "$BIN_DIR/nex-vault"
echo "  CLI installed to $BIN_DIR/nex-vault"

# Check if ~/.local/bin is on PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "  NOTE: Add $BIN_DIR to your PATH:"
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo "  Add this to your ~/.bashrc or ~/.zshrc"
fi

echo ""
echo "============================================"
echo "  Nex Vault installed successfully!"
echo "  Built by Nex AI (nex-ai.be)"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. Configure Telegram notifications (optional):"
echo "     nex-vault config set-telegram-token YOUR_BOT_TOKEN"
echo "     nex-vault config set-telegram-chat YOUR_CHAT_ID"
echo ""
echo "  2. Add your first document:"
echo "     nex-vault add /path/to/contract.pdf --type contract --party 'Vendor' --end-date 2027-01-01"
echo ""
echo "  3. View upcoming deadlines:"
echo "     nex-vault expiring"
echo ""
echo "  4. Set up daily alerts (optional):"
echo "     Add to crontab: 0 8 * * * $BIN_DIR/nex-vault alerts check"
echo ""
