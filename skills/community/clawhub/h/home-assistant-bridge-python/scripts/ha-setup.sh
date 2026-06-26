#!/bin/bash
# Home Assistant Setup Script
# Configures HA_URL and HA_TOKEN for API access

set -e

echo "=== Home Assistant Setup ==="
echo

# Check if already configured
if [ -f ~/.homeassistant.conf ]; then
    echo "Found existing config: ~/.homeassistant.conf"
    source ~/.homeassistant.conf
    echo "Current settings:"
    echo "  HA_URL: $HA_URL"
    echo "  HA_TOKEN: ${HA_TOKEN:0:20}..."
    echo
    read -p "Reconfigure? (y/N): " REPLY
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing configuration."
        exit 0
    fi
fi

# Get HA URL
echo "Enter your Home Assistant URL:"
echo "  Examples: http://homeassistant.local:8123"
echo "            http://192.168.1.100:8123"
echo "            https://ha.yourdomain.com"
read -p "HA_URL: " HA_URL

# Validate URL
if [ -z "$HA_URL" ]; then
    echo "Error: HA_URL cannot be empty"
    exit 1
fi

# Test connectivity
echo "Testing connectivity to $HA_URL..."
if ! curl -s -o /dev/null -w "%{http_code}" "$HA_URL" | grep -q "200\|401\|302"; then
    echo "Warning: Could not connect to $HA_URL"
    echo "Make sure Home Assistant is running and accessible."
    read -p "Continue anyway? (y/N): " REPLY
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Get Long-Lived Access Token
echo
echo "Enter your Home Assistant Long-Lived Access Token:"
echo "  (Get it from HA Profile > Long-Lived Access Tokens > Create Token)"
read -s -p "HA_TOKEN: " HA_TOKEN
echo

if [ -z "$HA_TOKEN" ]; then
    echo "Error: HA_TOKEN cannot be empty"
    exit 1
fi

# Save configuration
cat > ~/.homeassistant.conf << EOF
# Home Assistant Configuration
# Generated on $(date)
export HA_URL="$HA_URL"
export HA_TOKEN="$HA_TOKEN"
EOF

chmod 600 ~/.homeassistant.conf

echo
echo "=== Configuration saved to ~/.homeassistant.conf ==="
echo
echo "To use these settings, run:"
echo "  source ~/.homeassistant.conf"
echo
echo "Or add to your ~/.bashrc:"
echo "  source ~/.homeassistant.conf"
echo
echo "Testing API connection..."
source ~/.homeassistant.conf

# Test API call
RESPONSE=$(curl -s -H "Authorization: Bearer $HA_TOKEN" \
    -H "Content-Type: application/json" \
    "$HA_URL/api/" 2>/dev/null || echo "")

if [ -n "$RESPONSE" ]; then
    echo "✓ API connection successful!"
    echo "  Response: $RESPONSE"
else
    echo "✗ API connection failed"
    echo "  Check your token and URL"
fi