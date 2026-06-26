# x402 Payment Configuration

## Overview

x402 is an HTTP-native payment protocol using USDC on Base chain. This skill supports x402 for receiving payments.

## How x402 Works

```
User Request → 402 Payment Required → User Pays USDC → Access Granted
```

## Configuration

### Step 1: Set Environment Variables

```bash
# Your wallet address to receive USDC payments
export X402_RECIPIENT_ADDRESS="0x75b90dffbd7c75c42d1ef9513ff9be66806fe232"

# Optional: Your private key for payment verification
export X402_PRIVATE_KEY="0x..."
```

### Step 2: Get a Base Chain Wallet

If you don't have one:

1. Install MetaMask or Coinbase Wallet
2. Add Base network: https://base.org
3. Get your address (0x...)
4. Fund with USDC on Base

### Step 3: Test Configuration

```bash
cd skills/hypii-hyperliquid-trader
node -e "
import('./lib/x402.js').then(({X402Billing}) => {
  const billing = new X402Billing(process.env.X402_RECIPIENT_ADDRESS);
  console.log('Status:', billing.getStatus());
});
"
```

## Pricing

| Feature | Price (USDC) | Description |
|---------|--------------|-------------|
| Free Tier | $0 | 5 calls per day |
| Basic Query | 0.01 | Price check, balance view |
| Strategy | 0.05 | DCA, Grid, AI signals |
| Auto Trade | 0.10 | Execute live trades |

## Payment Flow

### For Users

1. User requests paid feature
2. Skill returns payment request with:
   - Amount in USDC
   - Recipient address
   - Payment URL
3. User pays via wallet (MetaMask, Coinbase, etc.)
4. Skill verifies payment and proceeds

### Example Payment Request

```json
{
  "status": "payment_required",
  "amount": 0.05,
  "recipient": "0x14de3De2C46E3Bf2D47B1ca8A6A6fd11A5F9D3Ca",
  "network": "Base",
  "paymentUrl": {
    "generic": "https://x402.org/pay?r=...",
    "coinbase": "https://keys.coinbase.com/pay?r=..."
  }
}
```

## Development Mode

Without `X402_PRIVATE_KEY`, the skill runs in dev mode:
- ✅ All features work
- ⚠️ Payments are simulated
- 💡 Console shows `[DEV MODE]`

## Production Setup

To accept real payments:

1. Set `X402_RECIPIENT_ADDRESS` to your wallet
2. (Optional) Set `X402_PRIVATE_KEY` for auto-verification
3. Users pay USDC on Base chain
4. Revenue goes directly to your wallet

## Resources

- x402 Protocol: https://www.x402.org/
- Base Network: https://base.org
- USDC on Base: https://www.circle.com/en/usdc/developers

## Support

- OpenClaw Discord: https://discord.gg/clawd
- x402 GitHub: https://github.com/coinbase/x402
