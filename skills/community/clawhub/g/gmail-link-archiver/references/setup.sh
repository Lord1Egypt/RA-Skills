#!/usr/bin/env bash
# Gmail Link Archiver - Auto Setup Script
# Installs Python dependencies and Playwright Chromium browser
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "============================================"
echo "  Gmail Link Archiver - Dependency Setup"
echo "============================================"
echo

# Detect Python
PYTHON=""
for candidate in python3 python; do
    if command -v "$candidate" &>/dev/null; then
        PYTHON="$candidate"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "[ERROR] Python 3 is required but not found."
    echo "Install with: sudo apt-get install python3 python3-pip"
    exit 1
fi

echo "[OK] Using Python: $($PYTHON --version)"

# Create and activate a virtualenv to avoid modifying the system Python
VENV_DIR="$SCRIPT_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo
    echo "[SETUP] Creating virtual environment at $VENV_DIR ..."
    $PYTHON -m venv "$VENV_DIR"
fi
# Use the venv's Python/pip from here on
VENV_PYTHON="$VENV_DIR/bin/python"
VENV_PIP="$VENV_DIR/bin/pip"

# Install pip packages inside the venv
echo
echo "[SETUP] Installing Python packages into virtual environment..."
"$VENV_PIP" install --quiet --upgrade pip
"$VENV_PIP" install --quiet playwright html2text

# Install Playwright Chromium
echo
echo "[SETUP] Installing Chromium browser via Playwright..."
"$VENV_PYTHON" -m playwright install chromium

# Install system dependencies for headless Chromium (Linux)
if [ "$(uname)" = "Linux" ]; then
    echo
    echo "[SETUP] Installing system dependencies for Chromium..."
    "$VENV_PYTHON" -m playwright install-deps chromium 2>/dev/null || {
        echo "[WARN] Could not auto-install system deps."
        echo "       You may need to run: sudo $VENV_PYTHON -m playwright install-deps chromium"
    }
fi

echo
echo "============================================"
echo "  Setup complete!"
echo "============================================"
echo
echo "Activate the virtual environment first:"
echo "  source $VENV_DIR/bin/activate"
echo
echo "Then run the archiver:"
echo "  $VENV_PYTHON $SCRIPT_DIR/gmail_link_archiver.py"
echo
echo "First run will prompt for Gmail IMAP credentials."
echo "Get an App Password at: https://myaccount.google.com/apppasswords"
