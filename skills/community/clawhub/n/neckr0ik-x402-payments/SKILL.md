---
name: neckr0ik-x402-payments
version: 1.0.0
description: x402 payment protocol for AI agents. Enables autonomous micropayments using HTTP 402 status codes and stablecoins. Use when you need to pay for API access, accept payments for your services, or interact with x402-enabled endpoints.
---

# x402 Payments for AI Agents

Autonomous payment protocol for AI agents using HTTP 402 + stablecoins.

## What is x402?

x402 is an open standard for internet-native payments. It enables AI agents to pay for API calls automatically using stablecoins, without accounts or human intervention.

**How it works:**
1. Agent requests API endpoint
2. Server responds with HTTP 402 + payment details
3. Agent signs payment authorization
4. Payment settled on blockchain
5. Request fulfilled automatically

**Key benefits:**
- No accounts or API keys
- Instant settlement
- Micropayments per request
- Blockchain-agnostic (EVM + Solana)
- Perfect for autonomous agents

## Quick Start

### Check if endpoint supports x402

```bash
neckr0ik-x402-payments check https://api.example.com/premium
```

### Pay for API access

```bash
neckr0ik-x402-payments pay https://api.example.com/premium --amount 0.01
```

### Accept payments (for your API)

```bash
neckr0ik-x402-payments serve --port 8080 --price 0.01
```

## Payment Flow

```
Agent                x402 Facilitator           API Server
  |                        |                        |
  |-- GET /premium ------>|----------------------->|
  |                        |                        |
  |<-- HTTP 402 -----------|------------------------|
  |    (payment required)  |                        |
  |    {amount, address,   |                        |
  |     chain, facilitator}|                        |
  |                        |                        |
  |-- Sign payment ------>|                        |
  |                        |                        |
  |                        |-- Submit to chain --->|
  |                        |                        |
  |                        |<-- Confirmation ------|
  |                        |                        |
  |-- GET /premium --------|----------------------->|
  |    PAYMENT-SIGNATURE   |                        |
  |                        |                        |
  |<-- 200 OK -------------|------------------------|
  |    (data)              |                        |
```

## Supported Chains

- Ethereum (Mainnet, L2s)
- Polygon
- Base
- Arbitrum
- Optimism
- Solana

## Supported Stablecoins

- USDC
- USDT
- DAI

## Commands

### check

Check if an endpoint supports x402 payments.

```bash
neckr0ik-x402-payments check <url>

Options:
  --timeout <ms>    Request timeout (default: 10000)
```

### pay

Pay for API access and receive data.

```bash
neckr0ik-x402-payments pay <url> [options]

Options:
  --amount <amount>    Maximum amount to pay (in USD)
  --chain <chain>      Preferred chain (default: base)
  --token <token>      Stablecoin token (default: usdc)
  --wallet <address>   Wallet to use for payment
  --dry-run            Show payment details without paying
```

### serve

Start an x402-enabled API server.

```bash
neckr0ik-x402-payments serve [options]

Options:
  --port <port>        Server port (default: 8080)
  --price <amount>     Price per request (in USD)
  --chain <chain>      Accept payments on chain (default: base)
  --token <token>      Accept stablecoin (default: usdc)
  --wallet <address>   Receiving wallet address
```

### balance

Check your payment wallet balance.

```bash
neckr0ik-x402-payments balance [options]

Options:
  --chain <chain>      Chain to check (default: all)
```

### history

View payment history.

```bash
neckr0ik-x402-payments history [options]

Options:
  --limit <n>         Number of transactions (default: 10)
  --chain <chain>      Filter by chain
```

## Configuration

Set up your wallet for payments:

```bash
# Set wallet private key (stored securely)
neckr0ik-x402-payments config set wallet.private_key <key>

# Or use environment variable
export X402_PRIVATE_KEY=<key>

# Set receiving address for payments
neckr0ik-x402-payments config set wallet.address <address>
```

## Use Cases

### As an Agent (Pay for API Access)

```python
# Before: Need API key, account, subscription
response = requests.get("https://api.example.com/data", 
    headers={"Authorization": "Bearer YOUR_API_KEY"})

# After: Autonomous payment, no account needed
response = x402.get("https://api.example.com/data")
```

### As a Provider (Accept Payments)

```python
from x402 import PaymentMiddleware

app = Flask(__name__)
app.wsgi_app = PaymentMiddleware(app.wsgi_app, price=0.01)

@app.route("/premium-data")
def premium_data():
    return {"data": "only accessible after payment"}

# Requests to /premium-data automatically require payment
```

## Security

- Private keys never leave your machine
- Payments signed locally
- Transaction broadcast through facilitators
- All settlements verified on-chain
- Payment receipts stored for audit

## See Also

- `references/x402-spec.md` — Full protocol specification
- `references/facilitators.md` — List of known facilitators
- `scripts/x402.py` — Payment implementation