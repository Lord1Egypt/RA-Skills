#!/bin/bash
# Quick helper to generate video via Zen7
# Usage: pay-zen7-video.sh "your prompt here" [chain]

PROMPT="${1:-A beautiful sunset}"
CHAIN="${2:-base}"

# Ensure wallet exists
WALLET_FILE="${HOME}/.moltspay/wallet.json"
if [ ! -f "$WALLET_FILE" ]; then
    echo "❌ Wallet not initialized. Run: moltspay init"
    exit 1
fi

echo "🎬 Generating video with prompt: $PROMPT"
echo "💰 Cost: $0.99 USDC"
echo "⛓️  Chain: $CHAIN"
echo ""

moltspay pay https://juai8.com/zen7 text-to-video --prompt "$PROMPT" --chain "$CHAIN"
