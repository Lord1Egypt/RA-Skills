#!/bin/bash
set -e

echo "🎰 Installing kalshi-agent skill..."

# Install kalshi-cli from npm (recommended)
if ! command -v kalshi &> /dev/null; then
    echo "📦 Installing kalshi-cli from npm..."
    npm install -g kalshi-cli
else
    echo "✅ kalshi-cli is already installed"
fi

# Set up credentials directory
mkdir -p "$HOME/.kalshi"
if [ ! -f "$HOME/.kalshi/.env" ]; then
    cat > "$HOME/.kalshi/.env" << 'EOF'
# Kalshi API Configuration
# Get credentials at: https://kalshi.com/api
KALSHI_ACCESS_KEY=your_access_key_here
EOF
    echo "📄 Created ~/.kalshi/.env — edit it with your API key"
fi

if [ ! -f "$HOME/.kalshi/private_key.pem" ]; then
    echo "⚠️  Place your RSA private key at ~/.kalshi/private_key.pem"
fi

echo ""
echo "✅ kalshi-agent installed!"
echo ""
echo "📋 Quick Start:"
echo "  1. Edit ~/.kalshi/.env with your API key"
echo "  2. Place your RSA private key at ~/.kalshi/private_key.pem"
echo "  3. kalshi --help"
