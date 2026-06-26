#!/usr/bin/env bash
set -euo pipefail

BASE="https://happythoughts.proteeninjector.workers.dev"

# Health
curl "$BASE/health"
echo

echo "\n# Discover providers"
curl "$BASE/discover?specialty=trading"
echo

echo "\n# Preview routing without payment"
curl "$BASE/route?specialty=trading/signals"
echo

echo "\n# Buy a thought (will return 402 unless you attach x402 payment or owner bypass header)"
curl -X POST "$BASE/think" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Should I long BTC here? There is an FVG near 94200 in a trending regime.",
    "buyer_wallet": "0xYOURWALLET",
    "specialty": "trading/signals"
  }'
echo

echo "\n# Register as a provider (requires x402 payment)"
curl -X POST "$BASE/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Trading Agent",
    "description": "Specializing in BTC momentum and FVG setups",
    "specialties": ["trading/signals", "trading/thesis"],
    "payout_wallet": "0xYOURWALLET",
    "human_in_loop": false
  }'
echo

echo "\n# Purchase a bundle (requires x402 payment)"
curl -X POST "$BASE/bundle" \
  -H "Content-Type: application/json" \
  -d '{
    "tier": "starter",
    "buyer_wallet": "0xYOURWALLET"
  }'
echo

echo "\n# Score details"
curl "$BASE/score/founding-pi-signals"
echo

echo "\n# Leaderboard"
curl "$BASE/leaderboard"
echo
