---
name: lobpay
description: LobPay Agent Skill - Purchase items via X402 protocol on Base network. Use when agents need to buy products, checkout, pay merchants, or leave feedback. Handles checkout info retrieval, X402 payment initiation, transaction recording, and merchant ratings. Triggers on: "Buy", "Purchase", "Pay", "Checkout", "X402", "Leave feedback", "Rate merchant".
---

# 🦞 LobPay Agent Skill

AI-powered commerce via X402 protocol on Base network.

## 🚀 Quick Start

```bash
cd ~/.openclaw/workspace/skills/lobpay/scripts
npm install
```

## 🔧 Configuration

Set environment variables (optional):
```bash
LOBPAY_API_URL=https://lobpay.cash  # Default: https://lobpay.market
```

## 📋 Core Workflows

### 1. Purchase Items

**Get checkout info first:**
```bash
node checkout.js <product_id> [quantity]
```

**Then complete purchase:**
```bash
node purchase.js <product_id> [quantity]
```

**Combined quick purchase:**
```bash
node buy.js <product_id> [quantity]
```

### 2. Leave Feedback

```bash
# Rate last purchase
node feedback.js <rating> "<comment>"

# Rate specific transaction
node feedback.js <transaction_id> <rating> "<comment>"
```

### 3. View Purchase History

```bash
node history.js [limit]
```

## 🔗 API Endpoints

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/v1/public/checkout-info` | GET | Public | Get pricing & merchant wallet |
| `/api/v1/agents/purchase` | POST | API Key + X402 | Execute purchase |
| `/api/v1/agents/feedback` | POST | API Key | Leave rating/comment |
| `/api/v1/agents/history` | GET | API Key | View transactions |

## 💰 X402 Payment Flow

1. **Checkout** → Get merchant wallet + pricing
2. **Sign** → Create X402 payment header
3. **Purchase** → Send to `/agents/purchase` with payment proof
4. **Confirm** → Transaction recorded on Base

See `references/api.md` for detailed request/response schemas.

## 🛡️ Security

- Private keys stored in `~/.lobpay/config.json`
- X402 headers signed locally
- API keys only sent to configured endpoints
- Supports Base Sepolia (testnet) and Base Mainnet

## 📚 References

- `references/api.md` - Full API documentation
- `references/schemas.md` - Database schemas
- `references/x402.md` - X402 protocol details
