#!/bin/bash

# Payment Skill Setup Script (Linux/macOS)
# Auto-detect Python version and install dependencies

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo ""
echo "========================================"
echo "Payment Skill Setup"
echo "========================================"
echo ""

echo "Checking Python version..."
python3 --version 2>/dev/null || {
    echo "Error: Python 3 is not installed"
    exit 1
}

# Detect Python version
PYTHON_VERSION_TYPE=$(python3 -c "import sys; print('py38' if sys.version_info >= (3, 8) else 'py36')")

if [ "$PYTHON_VERSION_TYPE" = "py38" ]; then
    echo "Python 3.8+ detected (recommended)"
    REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"
else
    echo "Python 3.6 detected (deprecated)"
    REQUIREMENTS_FILE="$SCRIPT_DIR/requirements-py36.txt"
fi

echo ""
echo "Checking virtual environment..."
if [ -d "$PROJECT_DIR/venv" ]; then
    echo "Virtual environment already exists"
else
    echo "Creating virtual environment..."
    python3 -m venv "$PROJECT_DIR/venv"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        exit 1
    fi
    echo "Virtual environment created"
fi
echo ""

echo "Activating virtual environment..."
source "$PROJECT_DIR/venv/bin/activate"
echo "Virtual environment activated"
echo ""

echo "Upgrading pip..."
python3 -m pip install --upgrade pip
echo "pip upgraded"
echo ""

echo "Installing dependencies..."
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo "Error: \"$REQUIREMENTS_FILE\" not found"
    exit 1
fi

echo "Installing from $REQUIREMENTS_FILE..."
pip install -r "$REQUIREMENTS_FILE"
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi
echo "Dependencies installed successfully!"
echo ""

# echo "Creating directories..."
# mkdir -p "$PROJECT_DIR/logs"
# mkdir -p "$PROJECT_DIR/data"
# echo "Directories created"

echo ""
echo "Running diagnostics..."
if [ -f "$SCRIPT_DIR/diagnose.py" ]; then
    python3 "$SCRIPT_DIR/diagnose.py"
else
    echo "Warning: diagnose.py not found, skipping diagnostics"
fi

echo ""
echo "========================================"
echo "Setup completed successfully!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Set environment variables:"
echo "   export PAYMENT_API_KEY=your_key"
echo "   export PAYMENT_API_SECRET=your_secret"
echo "3. Run tests: python3 -m pytest tests/ -v"
echo "4. Read documentation: cat README.md"
echo ""
