#!/usr/bin/env bash
# Validate octoDNS zone files

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="${SKILL_DIR}/venv"
CONFIG_FILE="${SKILL_DIR}/config/production.yaml"

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: octoDNS not installed. Run scripts/install.sh first."
    exit 1
fi

# Activate venv
source "${VENV_DIR}/bin/activate"

echo "Validating octoDNS configuration..."
echo ""

octodns-validate \
    --config-file="$CONFIG_FILE" \
    "$@"

echo ""
echo "✓ Validation complete"
