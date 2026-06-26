#!/usr/bin/env bash
# Nex Changelog - Setup Script
# MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
#
# Idempotent installer. Safe to run multiple times.
# Usage: bash setup.sh

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$HOME/.nex-changelog"
BIN_DIR="$HOME/.local/bin"
SERVICE_NAME="nex-changelog"

echo "============================================"
echo "  Nex Changelog - Setup"
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
echo "[1/4] Checking Python..."
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

# Step 2: Check Git
echo "[2/4] Checking Git..."
if command -v git &>/dev/null; then
    GIT_VERSION="$(git --version 2>&1)"
    echo "  Found: $GIT_VERSION"
else
    echo "WARNING: Git is required for git import functionality." >&2
    echo "Install Git from https://git-scm.com" >&2
fi

# Step 3: Create data directory
echo "[3/4] Creating data directory..."
mkdir -p "$DATA_DIR"
if [ "$PLATFORM" != "windows" ]; then
    chmod 700 "$DATA_DIR"
fi
echo "  Data directory: $DATA_DIR"

# Step 4: Create CLI symlink
echo "[4/4] Installing CLI tool..."
mkdir -p "$BIN_DIR"

# Create wrapper script
WRAPPER_SCRIPT="$BIN_DIR/nex-changelog"
cat > "$WRAPPER_SCRIPT" << 'EOF'
#!/usr/bin/env bash
# Nex Changelog wrapper script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Try to find the skill directory
# First, check if we're in the skill directory
if [ -f "nex-changelog.py" ]; then
    SKILL_DIR="$(pwd)"
elif [ -f "$HOME/.local/share/nex-changelog/nex-changelog.py" ]; then
    SKILL_DIR="$HOME/.local/share/nex-changelog"
elif [ -f "/opt/nex-changelog/nex-changelog.py" ]; then
    SKILL_DIR="/opt/nex-changelog"
else
    # Fallback: find relative to this script (works if properly linked from skill directory)
    SCRIPT_REAL_PATH="$(cd "$(dirname "$(readlink -f "$WRAPPER_SCRIPT")")/../.." && pwd)/nex-changelog"
    if [ -f "$SCRIPT_REAL_PATH/nex-changelog.py" ]; then
        SKILL_DIR="$SCRIPT_REAL_PATH"
    else
        echo "ERROR: Could not find nex-changelog installation" >&2
        exit 1
    fi
fi

# Run the Python script
python3 "$SKILL_DIR/nex-changelog.py" "$@"
EOF

chmod +x "$WRAPPER_SCRIPT"

# Try to symlink the actual script directly if possible
if [ "$PLATFORM" != "windows" ]; then
    # Remove old symlink if it exists
    [ -L "$BIN_DIR/nex-changelog-real" ] && rm "$BIN_DIR/nex-changelog-real"
    # Create symlink to the actual Python script
    ln -sf "$SKILL_DIR/nex-changelog.py" "$BIN_DIR/nex-changelog-real" 2>/dev/null || true
fi

# Ensure the wrapper is in PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo ""
    echo "Add $BIN_DIR to your PATH by running:"
    if grep -q "bashrc" <<< "$SHELL"; then
        echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
        echo "  source ~/.bashrc"
    else
        echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.zshrc"
        echo "  source ~/.zshrc"
    fi
fi

echo ""
echo "============================================"
echo "  Setup Complete!"
echo "============================================"
echo ""
echo "Data directory: $DATA_DIR"
echo "CLI command: nex-changelog"
echo ""
echo "Getting started:"
echo "  1. Add a project:"
echo "     nex-changelog project add --name \"My App\" --description \"My application\""
echo ""
echo "  2. Add entries:"
echo "     nex-changelog add --project \"My App\" --description \"Fixed bug\" --type fixed"
echo ""
echo "  3. Show changelog:"
echo "     nex-changelog show --project \"My App\""
echo ""
echo "Or import from git:"
echo "  nex-changelog git /path/to/repo --project \"My App\""
echo ""
echo "For more help:"
echo "  nex-changelog --help"
echo ""
