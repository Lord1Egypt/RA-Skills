#!/usr/bin/env bash
# Add a zone to production.yaml config

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="${SKILL_DIR}/config/production.yaml"
AGENT_CONFIG="${SKILL_DIR}/.agent-config.json"

# Load helper functions
source "${SCRIPT_DIR}/lib/config.sh"

if [ -z "$1" ]; then
    echo "Usage: $0 <zone> [provider]"
    echo "Example: $0 example.com"
    echo "         $0 example.com route53"
    exit 1
fi

ZONE_INPUT="$1"

# Add trailing dot if not present
if [[ ! "$ZONE_INPUT" =~ \.$ ]]; then
    ZONE="${ZONE_INPUT}."
else
    ZONE="$ZONE_INPUT"
fi

# Get provider
if [ -n "$2" ]; then
    PROVIDER="$2"
else
    PROVIDER=$(get_default_provider "$AGENT_CONFIG")
fi

# Check if zone already exists in config
if grep -q "^  ${ZONE}" "$CONFIG_FILE"; then
    echo "✓ Zone $ZONE already exists in production.yaml"
    exit 0
fi

echo "Adding $ZONE to production.yaml..."
echo "Provider: $PROVIDER"

# Add the zone with proper YAML indentation
cat >> "$CONFIG_FILE" <<EOF

  ${ZONE}:
    sources:
      - config
    targets:
      - ${PROVIDER}
EOF

echo "✓ Zone added successfully"
