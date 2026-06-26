#!/bin/bash
# Kamivision Video Recorder - Environment Setup Script
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
REQUIREMENTS="$SCRIPT_DIR/requirements.txt"

echo "=========================================="
echo "  Kamivision Recorder - Environment Setup"
echo "=========================================="
echo ""

# Step 1: Find or install Python 3.10
echo "[1/4] Checking Python 3.10 ..."

PYTHON_CMD=""

# Only look for python3.10
if command -v python3.10 &>/dev/null; then
    PYTHON_CMD="python3.10"
else
    # Check if python3/python happens to be 3.10.x
    for cmd in python3 python; do
        if command -v "$cmd" &>/dev/null; then
            ver=$("$cmd" --version 2>&1 | awk '{print $2}')
            major=$(echo "$ver" | cut -d. -f1)
            minor=$(echo "$ver" | cut -d. -f2)
            if [ "$major" -eq 3 ] && [ "$minor" -eq 10 ]; then
                PYTHON_CMD="$cmd"
                break
            fi
        fi
    done
fi

# If not found, try to install (no sudo required)
if [ -z "$PYTHON_CMD" ]; then
    echo "⚠️  Python 3.10 not found. Attempting to install..."
    if command -v brew &>/dev/null; then
        echo "   Installing via Homebrew..."
        brew install python@3.10
        PYTHON_CMD="python3.10"
    elif command -v conda &>/dev/null; then
        echo "   Installing via conda..."
        conda install -y python=3.10
        PYTHON_CMD="python"
    else
        # Use pyenv for user-level install (no sudo needed)
        echo "   Installing via pyenv (user-level, no sudo required)..."
        if ! command -v pyenv &>/dev/null; then
            echo "   Installing pyenv first..."
            curl -fsSL https://pyenv.run | bash
            export PYENV_ROOT="$HOME/.pyenv"
            export PATH="$PYENV_ROOT/bin:$PATH"
            eval "$(pyenv init -)"
        fi
        pyenv install 3.10 -s
        PYTHON_CMD="$HOME/.pyenv/versions/3.10.*/bin/python3.10"
        # Resolve glob to actual path
        PYTHON_CMD=$(ls $PYTHON_CMD 2>/dev/null | head -1)
        if [ -z "$PYTHON_CMD" ]; then
            echo "❌ pyenv install failed. Please install Python 3.10 manually."
            exit 1
        fi
    fi

    # Verify installation succeeded
    if ! command -v "$PYTHON_CMD" &>/dev/null && [ ! -f "$PYTHON_CMD" ]; then
        echo "❌ Installation failed. Please install Python 3.10 manually:"
        echo "   - macOS:  brew install python@3.10"
        echo "   - Linux:  curl https://pyenv.run | bash && pyenv install 3.10"
        echo "   - conda:  conda install python=3.10"
        exit 1
    fi
    echo "✅ Python 3.10 installed successfully"
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "✅ Python $PYTHON_VERSION ($PYTHON_CMD)"
echo ""

# Step 2: Create virtual environment
echo "[2/4] Setting up virtual environment..."

if [ -d "$VENV_DIR" ] && [ -f "$VENV_DIR/bin/python" -o -f "$VENV_DIR/Scripts/python.exe" ]; then
    echo "✅ Virtual environment already exists"
else
    $PYTHON_CMD -m venv "$VENV_DIR"
    echo "✅ Virtual environment created"
fi
echo ""

# Step 3: Install dependencies
echo "[3/4] Installing dependencies..."

if [ -f "$VENV_DIR/bin/pip" ]; then
    PIP="$VENV_DIR/bin/pip"
    PYTHON_VENV="$VENV_DIR/bin/python"
elif [ -f "$VENV_DIR/Scripts/pip.exe" ]; then
    PIP="$VENV_DIR/Scripts/pip.exe"
    PYTHON_VENV="$VENV_DIR/Scripts/python.exe"
else
    echo "❌ Cannot find pip in venv. Delete .venv and re-run."
    exit 1
fi

$PIP install --upgrade pip -q
$PIP install -r "$REQUIREMENTS" -q
echo "✅ Dependencies installed"
echo ""

# Step 4: Verify
echo "[4/4] Verifying installation..."
$PYTHON_VENV -c "import numpy; import requests; import cv2; print('✅ All dependencies OK')"

echo ""
echo "=========================================="
echo "  ✅ Setup complete! Ready to record."
echo "=========================================="
