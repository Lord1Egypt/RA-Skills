#!/usr/bin/env bash
# Initialize octoDNS config for a new zone

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_DIR="${SKILL_DIR}/config"

if [ -z "$1" ]; then
    echo "Usage: $0 <zone>"
    echo "Example: $0 example.com"
    exit 1
fi

ZONE="$1"

# Create config directory
mkdir -p "$CONFIG_DIR"

# Create production.yaml if it doesn't exist
PROD_CONFIG="${CONFIG_DIR}/production.yaml"

if [ ! -f "$PROD_CONFIG" ]; then
    cat > "$PROD_CONFIG" <<'EOF'
---
providers:
  config:
    class: octodns.provider.yaml.YamlProvider
    directory: ./config
    default_ttl: 300
  
  easydns:
    class: octodns_easydns.EasyDnsProvider
    token: env/EASYDNS_TOKEN
    api_key: env/EASYDNS_API_KEY
    portfolio: env/EASYDNS_PORTFOLIO

zones:
  '*':
    sources:
      - config
    targets:
      - easydns
EOF
    echo "✓ Created config/production.yaml"
fi

# Create zone file template
ZONE_FILE="${CONFIG_DIR}/${ZONE}.yaml"

if [ ! -f "$ZONE_FILE" ]; then
    cat > "$ZONE_FILE" <<EOF
---
# ${ZONE} DNS zone

# Root A record
'':
  ttl: 300
  type: A
  value: 192.0.2.1

# www subdomain
www:
  ttl: 300
  type: CNAME
  value: ${ZONE}.
EOF
    echo "✓ Created config/${ZONE}.yaml"
fi

echo ""
echo "⚠️  WARNING: If ${ZONE} already has records in DNS:"
echo "⚠️  Run 'scripts/dump.sh ${ZONE}' first to capture them!"
echo "⚠️  Otherwise you'll DELETE existing records when you sync."
echo ""
echo "Next steps:"
echo "1. Set environment variables:"
echo "   export EASYDNS_TOKEN='your-token'"
echo "   export EASYDNS_API_KEY='your-api-key'"
echo "   export EASYDNS_PORTFOLIO='your-portfolio'"
echo ""
echo "2. Edit config/${ZONE}.yaml with your DNS records"
echo ""
echo "3. Preview changes:"
echo "   scripts/sync.sh --noop"
echo ""
echo "4. Apply changes:"
echo "   scripts/sync.sh --doit"
