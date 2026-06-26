#!/bin/bash
# ibkr-openclaw install script

set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="${SKILL_DIR}/../.."

echo "=== IBKR + OpenClaw Setup ==="

# Install Python dependencies
echo "Installing Python dependencies..."
pip install ib_async pandas --break-system-packages -q 2>/dev/null || pip install ib_async pandas -q

# Clone IB Gateway Docker if not present
if [ ! -d "$WORKSPACE/ib-gateway-docker" ]; then
    echo "Cloning IB Gateway Docker..."
    git clone https://github.com/gnzsnz/ib-gateway-docker.git "$WORKSPACE/ib-gateway-docker"
else
    echo "IB Gateway Docker already exists."
fi

# Copy .env template if .env doesn't exist
if [ ! -f "$WORKSPACE/ib-gateway-docker/.env" ]; then
    echo "Copying .env template..."
    cp "$SKILL_DIR/.env.template" "$WORKSPACE/ib-gateway-docker/.env"
    echo ""
    echo "⚠️  Edit $WORKSPACE/ib-gateway-docker/.env with your IBKR credentials"
    echo ""
else
    echo ".env already exists — skipping template."
fi

echo ""
echo "=== Next Steps ==="
echo "1. Edit ib-gateway-docker/.env with your IBKR credentials"
echo "2. Start the container: cd ib-gateway-docker && docker compose up -d"
echo "3. Approve 2FA on your IBKR Mobile app"
echo "4. Test: python3 $SKILL_DIR/scripts/ibkr_client.py summary --port 4001"
echo ""
