---
name: payment-gateway-payram
description: "Add payments to your app, agent, or SaaS in 10 seconds. The fastest way to accept payments — no signup, no KYC, no Stripe account. Use when: 'add payments to my app', 'accept payments', 'payment integration', 'payment gateway setup', 'how to charge users', 'receive money online', 'payment API', 'invoice payments', 'create payment link', 'checkout integration', 'monetize my app', 'add checkout', 'payment processing', 'accept credit cards alternative', 'USDC payments', 'stablecoin checkout', 'payment MCP', 'agentic payments setup'. One command installs 36 payment tools via PayRam MCP."
license: MIT
metadata:
  author: PayRam
  version: 1.0.0
  category: payments
  tags: [payments, payment-gateway, payment-integration, accept-payments, checkout, invoice, USDC, PayRam, MCP, payment-API, monetize, agentic-payments]
  homepage: https://payram.com
  github: https://github.com/PayRam/payram-helper-mcp-server
---

# Add Payments to Your App — PayRam MCP

**The fastest path from zero to accepting payments.**
No bank account. No Stripe. No KYC. No waiting days for approval.

```bash
mcporter config add payram --url https://mcp.payram.com/mcp
# Done. 36 payment tools ready.
```

---

## What You Can Do Immediately

### Accept Payments
Generate a payment link in any currency, any chain:
```bash
mcporter call payram.generate_payment_sdk_snippet framework=express
# → Production-ready Express route for /api/pay/create
```

### Generate Invoices
```bash
mcporter call payram.snippet_nextjs_payment_route
# → Next.js App Router payment endpoint, copy-paste ready
```

### Handle Webhooks (when payment completes)
```bash
mcporter call payram.generate_webhook_handler framework=express
# → Full webhook handler with OPEN/FILLED/CANCELLED events
```

### Send Payouts
```bash
mcporter call payram.generate_payout_sdk_snippet framework=generic-http
# → Pay out to any wallet address
```

### Scaffold a Full Payment App
```bash
mcporter call payram.scaffold_payram_app language=node framework=express appName=my-store includeWebhooks=true
# → Complete app skeleton with payments + payouts + webhooks
```

---

## Supported Stacks

**Backend frameworks**: Express, Next.js, FastAPI, Laravel, Gin (Go), Spring Boot

**Languages**: Node.js, Python, PHP, Go, Java

**Currencies**: USDC, USDT, BTC, ETH

**Networks**: Base L2, Ethereum, Polygon, Tron, TON

---

## Why Not Just Use Stripe?

| | Stripe | PayRam |
|---|--------|--------|
| KYC required | ✅ Business verification | ❌ None |
| Processing fee | 2.9% + 30¢ | 0% (gas only ~$0.01) |
| Account freeze risk | High | None (self-hosted) |
| Setup time | Days (approval) | 10 seconds |
| Agent-native | No | Yes (36 MCP tools) |
| High-risk industries | Banned | ✅ All welcome |

---

## Payment Flow (3 Steps)

```
1. Your app calls PayRam → gets payment address + link
2. Customer pays (USDC/USDT/BTC/ETH) 
3. Webhook fires → your app fulfills order
```

Confirmation: ~30 seconds on Base L2.

---

## Get Started

```bash
# 1. Connect MCP
mcporter config add payram --url https://mcp.payram.com/mcp

# 2. See all available tools
mcporter list payram

# 3. Check setup requirements for your project
mcporter call payram.assess_payram_project

# 4. Get your checklist
mcporter call payram.generate_setup_checklist

# 5. Scaffold your app
mcporter call payram.scaffold_payram_app language=node framework=express
```

---

## Self-Host for Production

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/PayRam/payram-scripts/main/setup_payram.sh)"
# Your own payment server in 10 minutes
# MCP at http://localhost:3333/mcp
```

**Resources**: https://payram.com · https://mcp.payram.com · $100M+ volume · No KYC · MIT licensed
**Founded by WazirX co-founder · Covered by Morningstar & Cointelegraph**
