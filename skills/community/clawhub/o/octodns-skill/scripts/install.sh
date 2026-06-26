#!/usr/bin/env bash
# Install octoDNS and easyDNS provider

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="${SKILL_DIR}/venv"

echo "Installing octoDNS..."

# Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate venv
source "${VENV_DIR}/bin/activate"

# Install packages
pip install --quiet --upgrade pip
pip install --quiet octodns octodns-easydns

echo "✓ octoDNS installed successfully"
echo "  Location: $VENV_DIR"
echo ""
echo "To use octoDNS:"
echo "  source ${VENV_DIR}/bin/activate"
echo "  octodns-sync --config-file=config/production.yaml"
