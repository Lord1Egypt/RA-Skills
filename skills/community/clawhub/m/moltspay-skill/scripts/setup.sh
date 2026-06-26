#!/bin/bash
# MoltsPay Skill Setup - runs on first use
# Installs moltspay globally and initializes wallet

set -e

echo "🔧 Setting up MoltsPay skill..."

# Install moltspay globally if not present
if ! command -v moltspay &> /dev/null; then
    echo "📦 Installing moltspay..."
    npm install -g moltspay
    echo "✅ moltspay installed"
else
    echo "✅ moltspay already installed"
fi

# Initialize wallet if not exists
WALLET_FILE="${HOME}/.moltspay/wallet.json"
if [ ! -f "$WALLET_FILE" ]; then
    echo "🔐 Initializing wallet..."
    moltspay init --chain base --max-per-tx 2 --max-per-day 10
    
    if [ -f "$WALLET_FILE" ]; then
        ADDRESS=$(cat "$WALLET_FILE" | jq -r '.address')
        echo ""
        echo "✅ Setup complete!"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "📍 Wallet: $ADDRESS"
        echo "⛓️  Chain: Base (mainnet)"
        echo "💰 Limits: \$2/tx, \$10/day"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "⚠️  Fund wallet with USDC on Base to use services."
    fi
else
    echo "✅ Wallet already exists"
    moltspay status 2>/dev/null || true
fi

echo ""
echo "🎉 MoltsPay skill ready!"
