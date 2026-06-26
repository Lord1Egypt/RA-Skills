#!/usr/bin/env bash
# Sync DNS zones using octoDNS

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="${SKILL_DIR}/venv"
CONFIG_FILE="${SKILL_DIR}/config/production.yaml"
AGENT_CONFIG="${SKILL_DIR}/.agent-config.json"

# Load helper functions
source "${SCRIPT_DIR}/lib/config.sh"

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: octoDNS not installed. Run scripts/install.sh first."
    exit 1
fi

# Activate venv
source "${VENV_DIR}/bin/activate"

# Load credentials for default provider
DEFAULT_PROVIDER=$(get_default_provider "$AGENT_CONFIG")
load_provider_credentials "$DEFAULT_PROVIDER" "$AGENT_CONFIG"

# Default to dry-run (no --doit flag)
MODE=""
ZONE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --doit)
            MODE="--doit"
            shift
            ;;
        --zone)
            ZONE="$2"
            shift 2
            ;;
        --config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--doit] [--zone ZONE] [--config FILE]"
            echo ""
            echo "  (no flags)  = dry-run (preview only)"
            echo "  --doit      = actually apply changes"
            exit 1
            ;;
    esac
done

# If zone specified, ensure it's in production.yaml
if [ -n "$ZONE" ]; then
    if ! grep -q "^  ${ZONE}" "$CONFIG_FILE" 2>/dev/null; then
        echo "Zone $ZONE not in config, adding it..."
        "${SCRIPT_DIR}/add-zone.sh" "$ZONE" "$DEFAULT_PROVIDER"
    fi
fi

# Build command
CMD="octodns-sync --config-file=$CONFIG_FILE $MODE"

if [ -n "$ZONE" ]; then
    CMD="$CMD $ZONE"
fi

echo "Running: $CMD"
echo ""

# Execute and capture output
OUTPUT=$($CMD 2>&1)
EXIT_CODE=$?

# Display output
echo "$OUTPUT"

# Safety check: warn about deletes
if echo "$OUTPUT" | grep -q "Delete <"; then
    echo ""
    echo "⚠️  WARNING: This sync will DELETE records!"
    echo "⚠️  Review the 'Delete' lines above carefully."
    if [ -n "$MODE" ]; then
        echo "⚠️  Run again with --doit to apply (currently in apply mode)"
    else
        echo "⚠️  This was a preview. Deletes will happen if you run with --doit"
    fi
    echo ""
fi

exit $EXIT_CODE
