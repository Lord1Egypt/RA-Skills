#!/usr/bin/env bash
# Dump existing DNS zone to YAML

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="${SKILL_DIR}/venv"
CONFIG_FILE="${SKILL_DIR}/config/dump.yaml"
AGENT_CONFIG="${SKILL_DIR}/.agent-config.json"

# Load helper functions
source "${SCRIPT_DIR}/lib/config.sh"

if [ -z "$1" ]; then
    DEFAULT_PROV=$(get_default_provider "$AGENT_CONFIG")
    echo "Usage: $0 <zone> [provider]"
    echo "Example: $0 example.com"
    echo "         $0 example.com route53"
    echo ""
    echo "Default provider from config: $DEFAULT_PROV"
    echo "Override by specifying provider as 2nd argument"
    exit 1
fi

ZONE_INPUT="$1"

# Add trailing dot if not present
if [[ ! "$ZONE_INPUT" =~ \.$ ]]; then
    ZONE="${ZONE_INPUT}."
else
    ZONE="$ZONE_INPUT"
fi

# Get default provider from config, or use command-line override
if [ -n "$2" ]; then
    PROVIDER="$2"
else
    PROVIDER=$(get_default_provider "$AGENT_CONFIG")
fi

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: octoDNS not installed. Run scripts/install.sh first."
    exit 1
fi

# Activate venv
source "${VENV_DIR}/bin/activate"

# Create temporary config with the specific zone
TEMP_CONFIG=$(mktemp)
cat > "$TEMP_CONFIG" <<EOF
---
providers:
  easydns:
    class: octodns_easydns.EasyDnsProvider
    token: env/EASYDNS_TOKEN
    api_key: env/EASYDNS_API_KEY
    portfolio: env/EASYDNS_PORTFOLIO

zones:
  ${ZONE}:
    sources:
      - ${PROVIDER}
EOF

echo "================================================================"
echo "  DUMPING EXISTING ZONE - CRITICAL SAFETY STEP"
echo "================================================================"
echo "Zone: $ZONE"
echo "Provider: $PROVIDER"
echo "Output: ${SKILL_DIR}/config/${ZONE}.yaml"
echo ""
echo "This captures ALL existing records in the zone."
echo "ALWAYS do this before making changes to existing zones!"
echo ""

# Load credentials for the provider
load_provider_credentials "$PROVIDER" "$AGENT_CONFIG"

# Run dump with temporary config
octodns-dump \
    --config-file="$TEMP_CONFIG" \
    --output-dir="${SKILL_DIR}/config" \
    "$ZONE" \
    "$PROVIDER"

# Clean up temp file
rm -f "$TEMP_CONFIG"

echo ""
echo "✓ Zone dumped successfully"
