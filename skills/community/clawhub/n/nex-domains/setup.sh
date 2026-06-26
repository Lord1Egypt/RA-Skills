#!/usr/bin/env bash
# Nex Domains - Setup Script
# MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
#
# Idempotent installer. Safe to run multiple times.
# Usage: bash setup.sh

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$HOME/.nex-domains"
BIN_DIR="$HOME/.local/bin"
SERVICE_NAME="nex-domains"

echo "============================================"
echo "  Nex Domains - Setup"
echo "  DNS & Domain Portfolio Manager"
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
echo "[1/5] Checking Python..."
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

# Step 2: Check required CLI tools
echo "[2/5] Checking required CLI tools..."

MISSING_TOOLS=()

if ! command -v whois &>/dev/null; then
    MISSING_TOOLS+=("whois")
fi

if ! command -v dig &>/dev/null; then
    MISSING_TOOLS+=("dig")
fi

if ! command -v openssl &>/dev/null; then
    MISSING_TOOLS+=("openssl")
fi

if [ ${#MISSING_TOOLS[@]} -gt 0 ]; then
    echo "  Missing tools: ${MISSING_TOOLS[*]}"
    echo ""
    echo "  Install them with:"
    if [ "$PLATFORM" = "linux" ]; then
        echo "    Ubuntu/Debian: sudo apt install ${MISSING_TOOLS[*]}"
        echo "    RHEL/CentOS:   sudo yum install ${MISSING_TOOLS[*]}"
        echo "    Fedora:        sudo dnf install ${MISSING_TOOLS[*]}"
    elif [ "$PLATFORM" = "macos" ]; then
        echo "    brew install ${MISSING_TOOLS[*]}"
    fi
    echo ""
    echo "  For now, continuing setup..."
else
    echo "  All required tools found."
fi

# Step 3: Create data directory
echo "[3/5] Creating data directory..."
mkdir -p "$DATA_DIR"
if [ "$PLATFORM" != "windows" ]; then
    chmod 700 "$DATA_DIR"
fi
echo "  Data directory: $DATA_DIR"

# Step 4: Initialize database
echo "[4/5] Initializing database..."
PYTHONPATH="$SKILL_DIR/lib" "$PYTHON" -c "
import sys; sys.path.insert(0, '$SKILL_DIR/lib')
from storage import init_db
init_db()
print('  Database ready at $DATA_DIR/domains.db')
"

# Step 5: Make CLI executable and create symlink
echo "[5/5] Setting up CLI tool..."
chmod +x "$SKILL_DIR/nex-domains.py"

# Create wrapper script
mkdir -p "$BIN_DIR"
cat > "$BIN_DIR/nex-domains" << WRAPPER
#!/usr/bin/env bash
exec "$PYTHON" "$SKILL_DIR/nex-domains.py" "\$@"
WRAPPER
chmod +x "$BIN_DIR/nex-domains"
echo "  CLI installed to $BIN_DIR/nex-domains"

# Check if ~/.local/bin is on PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "  NOTE: Add $BIN_DIR to your PATH:"
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo "  Add this to your ~/.bashrc or ~/.zshrc"
fi

echo ""
echo "============================================"
echo "  Nex Domains installed successfully!"
echo "  Built by Nex AI (nex-ai.be)"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. (Optional) Configure Cloudflare API:"
echo "     export CF_API_TOKEN='your-token'"
echo "     export CF_EMAIL='your-email'"
echo ""
echo "  2. Test the installation:"
echo "     nex-domains stats"
echo ""
echo "  3. Add your first domain:"
echo "     nex-domains add example.com --registrar cloudflare --client 'Your Company'"
echo ""
echo "  4. Scan the domain:"
echo "     nex-domains scan example.com"
echo ""
echo "  5. View help:"
echo "     nex-domains --help"
echo ""
