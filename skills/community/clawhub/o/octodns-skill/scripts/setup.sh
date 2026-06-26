#!/usr/bin/env bash
# Setup script for agent configuration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="${SKILL_DIR}/.agent-config.json"
CREDS_DIR="/Users/markjr/clawd/.credentials"

echo "================================================================"
echo "  OCTODNS AGENT SETUP"
echo "================================================================"
echo ""

# Check if config already exists
if [ -f "$CONFIG_FILE" ]; then
    echo "⚠️  Configuration already exists: $CONFIG_FILE"
    read -p "Overwrite? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi
fi

# Ask for default provider
echo "What DNS provider do you want to use by default?"
echo "  1) easyDNS"
echo "  2) Route53"
echo "  3) Cloudflare"
echo "  4) Other"
read -p "Choice (1-4): " -n 1 -r PROVIDER_CHOICE
echo ""

case $PROVIDER_CHOICE in
    1)
        PROVIDER="easydns"
        PROVIDER_CLASS="octodns_easydns.EasyDnsProvider"
        ;;
    2)
        PROVIDER="route53"
        PROVIDER_CLASS="octodns_route53.Route53Provider"
        ;;
    3)
        PROVIDER="cloudflare"
        PROVIDER_CLASS="octodns_cloudflare.CloudflareProvider"
        ;;
    4)
        read -p "Provider name: " PROVIDER
        read -p "Provider class: " PROVIDER_CLASS
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "Provider: $PROVIDER"
echo "Class: $PROVIDER_CLASS"
echo ""

# Create config
cat > "$CONFIG_FILE" <<EOF
{
  "default_provider": "$PROVIDER",
  "credentials_path": "$CREDS_DIR",
  "providers": {
    "$PROVIDER": {
      "class": "$PROVIDER_CLASS",
      "credentials_file": "${PROVIDER}.json"
    }
  }
}
EOF

echo "✓ Configuration saved to $CONFIG_FILE"
echo ""

# Setup credentials
CREDS_FILE="${CREDS_DIR}/${PROVIDER}.json"

if [ ! -f "$CREDS_FILE" ]; then
    echo "Setting up credentials for $PROVIDER..."
    mkdir -p "$CREDS_DIR"
    
    if [ "$PROVIDER" = "easydns" ]; then
        read -p "easyDNS API Token: " API_TOKEN
        read -p "easyDNS API Key: " API_KEY
        read -p "easyDNS Portfolio (optional): " PORTFOLIO
        
        cat > "$CREDS_FILE" <<EOF
{
  "provider": "easydns",
  "api_token": "$API_TOKEN",
  "api_key": "$API_KEY",
  "portfolio": "$PORTFOLIO",
  "notes": "easyDNS API v3 credentials"
}
EOF
    else
        echo "Creating template credentials file..."
        cat > "$CREDS_FILE" <<EOF
{
  "provider": "$PROVIDER",
  "notes": "Edit this file with your $PROVIDER credentials"
}
EOF
        echo "⚠️  Edit $CREDS_FILE with your credentials"
    fi
    
    echo "✓ Credentials template created: $CREDS_FILE"
else
    echo "✓ Credentials already exist: $CREDS_FILE"
fi

echo ""
echo "================================================================"
echo "  SETUP COMPLETE"
echo "================================================================"
echo ""
echo "Default provider: $PROVIDER"
echo "Configuration: $CONFIG_FILE"
echo "Credentials: $CREDS_FILE"
echo ""
echo "Next steps:"
echo "  1. Run: ./scripts/install.sh"
echo "  2. Dump a zone: ./scripts/dump.sh example.com"
echo "  3. Make changes: vim config/example.com.yaml"
echo "  4. Preview: ./scripts/sync.sh --zone example.com."
echo "  5. Apply: ./scripts/sync.sh --zone example.com. --doit"
echo ""
