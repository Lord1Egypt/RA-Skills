#!/bin/bash
# Ensure MoltsPay wallet exists, auto-init if not

MOLTSPAY_DIR="${HOME}/.moltspay"
WALLET_FILE="${MOLTSPAY_DIR}/wallet.json"

if [ ! -f "$WALLET_FILE" ]; then
    echo "🔐 Initializing MoltsPay wallet..."
    moltspay init --max-per-tx 2 --max-per-day 10
    
    if [ -f "$WALLET_FILE" ]; then
        echo ""
        echo "✅ Wallet created!"
        moltspay status
        echo ""
        echo "⚠️  Fund your wallet with USDC on your preferred chain to start using services."
    else
        echo "❌ Failed to initialize wallet"
        exit 1
    fi
else
    echo "✅ Wallet already exists"
    moltspay status
fi
