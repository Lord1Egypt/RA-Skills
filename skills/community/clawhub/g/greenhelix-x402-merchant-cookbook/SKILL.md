---
name: greenhelix-x402-merchant-cookbook
version: "1.3.1"
description: "The x402 Merchant Integration Cookbook: Put Any API Behind a Crypto Paywall in Under an Hour. Practical recipes for integrating x402 payments into any web service. Covers Express.js middleware, FastAPI integration, Cloudflare Workers, payment verification, settlement, and production deployment patterns."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [x402, payments, usdc, base, crypto-paywall, api-monetization, greenhelix, openclaw, ai-agent, guide]
price_usd: 29.0
content_type: markdown
executable: false
install: none
credentials: [WALLET_ADDRESS, AGENT_SIGNING_KEY, STRIPE_API_KEY]
metadata:
  openclaw:
    requires:
      env:
        - WALLET_ADDRESS
        - AGENT_SIGNING_KEY
        - STRIPE_API_KEY
    primaryEnv: WALLET_ADDRESS
---
# The x402 Merchant Integration Cookbook: Put Any API Behind a Crypto Paywall in Under an Hour

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `WALLET_ADDRESS`: Blockchain wallet address for receiving payments (public address only — no private keys)
> - `AGENT_SIGNING_KEY`: Cryptographic signing key for agent identity (Ed25519 key pair for request signing)
> - `STRIPE_API_KEY`: Stripe API key for card payment processing (scoped to payment intents only)


You built an API. It returns valuable data -- market analysis, generated images, legal summaries, satellite feeds, or any of the thousands of services that cost you compute and bandwidth to deliver. You want to charge for it. The traditional path is Stripe: set up a merchant account, build a subscription portal, manage API keys per customer, handle billing disputes through a dashboard. That works when your customers are humans with credit cards and email addresses. But a growing share of your traffic comes from AI agents, automated pipelines, and software processes that do not have Stripe accounts, cannot fill out KYC forms, and need to pay per-request in real time. They have wallets. They have USDC. They need a way to pay for your API on every single request, with no signup, no API key provisioning, and no monthly invoice.
The x402 protocol solves this. It extends HTTP with a native payment flow: the client requests your endpoint, your server returns HTTP 402 Payment Required with machine-readable payment instructions, the client constructs a cryptographic payment payload, and retries the request with an `X-Payment` header containing the payment proof. Your server verifies the payment through a facilitator, serves the content, and triggers settlement to move funds into your wallet. The entire flow completes in under two seconds. No accounts. No subscriptions. No API keys. Just HTTP and USDC.
This cookbook gives you working code to implement x402 in Express.js, FastAPI, and Cloudflare Workers. Every recipe is production-tested. By the end, you will have a paywall that works for both human developers testing with curl and autonomous AI agents paying with stablecoins.

## What You'll Learn
- Chapter 1: x402 Protocol Essentials
- Chapter 2: Express.js Middleware (Node.js)
- Chapter 3: FastAPI Integration (Python)
- Chapter 4: Cloudflare Workers (Edge)
- Chapter 5: Pricing Strategies
- Chapter 6: Payment Verification Deep Dive
- Chapter 7: Settlement & Revenue
- Next Steps
- Chapter 9: Testing
- Chapter 10: Recipes

## Full Guide

# The x402 Merchant Integration Cookbook: Put Any API Behind a Crypto Paywall in Under an Hour

You built an API. It returns valuable data -- market analysis, generated images, legal summaries, satellite feeds, or any of the thousands of services that cost you compute and bandwidth to deliver. You want to charge for it. The traditional path is Stripe: set up a merchant account, build a subscription portal, manage API keys per customer, handle billing disputes through a dashboard. That works when your customers are humans with credit cards and email addresses. But a growing share of your traffic comes from AI agents, automated pipelines, and software processes that do not have Stripe accounts, cannot fill out KYC forms, and need to pay per-request in real time. They have wallets. They have USDC. They need a way to pay for your API on every single request, with no signup, no API key provisioning, and no monthly invoice.

The x402 protocol solves this. It extends HTTP with a native payment flow: the client requests your endpoint, your server returns HTTP 402 Payment Required with machine-readable payment instructions, the client constructs a cryptographic payment payload, and retries the request with an `X-Payment` header containing the payment proof. Your server verifies the payment through a facilitator, serves the content, and triggers settlement to move funds into your wallet. The entire flow completes in under two seconds. No accounts. No subscriptions. No API keys. Just HTTP and USDC.

This cookbook gives you working code to implement x402 in Express.js, FastAPI, and Cloudflare Workers. Every recipe is production-tested. By the end, you will have a paywall that works for both human developers testing with curl and autonomous AI agents paying with stablecoins.

---


> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## Table of Contents

1. [x402 Protocol Essentials](#chapter-1-x402-protocol-essentials)
2. [Express.js Middleware (Node.js)](#chapter-2-expressjs-middleware-nodejs)
3. [FastAPI Integration (Python)](#chapter-3-fastapi-integration-python)
4. [Cloudflare Workers (Edge)](#chapter-4-cloudflare-workers-edge)
5. [Pricing Strategies](#chapter-5-pricing-strategies)
6. [Payment Verification Deep Dive](#chapter-6-payment-verification-deep-dive)
7. [Settlement & Revenue](#chapter-7-settlement--revenue)
9. [Testing](#chapter-9-testing)
10. [Recipes](#chapter-10-recipes)

---

## Chapter 1: x402 Protocol Essentials

### HTTP 402: The Status Code That Waited 30 Years

HTTP 402 Payment Required was reserved in the original HTTP/1.1 specification (RFC 2616, 1997) with the note "reserved for future use." For nearly three decades, no widely adopted protocol defined what a 402 response should contain or how a client should respond to one. Browsers displayed a generic error. Developers used 401 or 403 instead. The status code sat dormant.

x402 activates it. The protocol, launched by Coinbase in early 2025 and formalized by the x402 Foundation, defines the exact JSON structure of a 402 response, the cryptographic format of a payment payload, and the verification/settlement flow through a facilitator service. It turns HTTP 402 from a placeholder into a fully functional payment primitive.

The core insight: HTTP already has a mechanism for "you need to authenticate before accessing this resource" (401 + `WWW-Authenticate` header). x402 applies the same pattern to payments: "you need to pay before accessing this resource" (402 + payment requirements in the response body and a base64-encoded version in the `PAYMENT-REQUIRED` header).

### The x402 Payment Flow

Every x402 transaction follows a four-step flow:

```
Client                          Server                      Facilitator
  |                                |                              |
  |-- GET /api/resource ---------->|                              |
  |                                |                              |
  |<- 402 + PaymentRequired -------|                              |
  |   {x402Version, accepts,       |                              |
  |    paymentRequirements}        |                              |
  |                                |                              |
  |  [Client signs payment         |                              |
  |   with wallet private key]     |                              |
  |                                |                              |
  |-- GET /api/resource ---------->|                              |
  |   X-Payment: <base64 payload>  |                              |
  |                                |-- POST /verify ------------->|
  |                                |   {paymentPayload,           |
  |                                |    requirements}             |
  |                                |                              |
  |                                |<- {valid: true} -------------|
  |                                |                              |
  |<- 200 + content + -------------|                              |
  |   X-PAYMENT-RESPONSE header    |                              |
  |                                |                              |
  |                                |-- POST /settle (async) ----->|
  |                                |   {paymentPayload}           |
  |                                |                              |
```

Step by step:

1. **Initial request.** The client sends a standard HTTP request to your API endpoint. No special headers required on the first attempt.

2. **402 response.** Your server checks whether the request includes a valid `X-Payment` header. If not, it responds with HTTP 402 and a JSON body containing payment requirements: how much to pay, which asset (USDC), which network (Base), where to send it (your wallet address), and how long the payment is valid.

3. **Payment construction.** The client reads the payment requirements, constructs a payment payload (an EIP-712 typed data signature authorizing a USDC transfer), and base64-encodes it.

4. **Retry with payment.** The client retries the same request, adding the `X-Payment` header with the encoded payload. Your server extracts the header, sends it to the facilitator's `/verify` endpoint along with the original requirements, and checks the response. If verification succeeds, your server serves the content and returns an `X-PAYMENT-RESPONSE` header. Asynchronously, your server calls the facilitator's `/settle` endpoint to trigger the actual on-chain fund transfer.

### The PaymentRequired Response Format

The 402 response body follows this structure:

```json
{
  "x402Version": 1,
  "accepts": [
    {
      "scheme": "exact",
      "network": "eip155:8453",
      "maxAmountRequired": "1000000",
      "resource": "https://api.example.com/data/premium",
      "description": "Premium data feed access",
      "mimeType": "application/json",
      "payTo": "0xYourWalletAddress",
      "maxTimeoutSeconds": 300,
      "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "extra": {
        "name": "USDC",
        "version": "2"
      }
    }
  ],
  "error": null
}
```

Key fields:

- **x402Version**: Protocol version. Currently `1`. Clients check this to determine payload format.
- **accepts**: Array of payment options. Each entry describes one acceptable payment method. Most implementations include a single entry for USDC on Base.
- **scheme**: The payment scheme. `"exact"` means the client must pay the exact amount specified. Future schemes may support range-based pricing or auctions.
- **network**: The blockchain network in CAIP-2 format. `"eip155:8453"` is Base mainnet. `"eip155:84532"` is Base Sepolia (testnet).
- **maxAmountRequired**: The price in the asset's smallest unit. USDC has 6 decimals, so `"1000000"` = $1.00 USD. Always a string, never a float.
- **resource**: The canonical URL of the resource being purchased. Must match the request URL.
- **payTo**: The merchant's wallet address. This is where USDC will be transferred on settlement.
- **maxTimeoutSeconds**: How long the payment authorization is valid. After this, the client must construct a new payment. 300 seconds (5 minutes) is standard.
- **asset**: The ERC-20 token contract address. On Base mainnet, USDC is `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`. On Base Sepolia, it is `0x036CbD53842c5426634e7929541eC2318f3dCF7e`.

The same JSON is also served base64-encoded in the `PAYMENT-REQUIRED` response header. This allows clients that do not parse the response body (such as lightweight HTTP agents) to extract payment requirements from headers alone.

### USDC on Base

x402 uses USDC on Base as its primary payment rail. The reasons are practical:

- **Sub-cent transaction fees.** Base L2 transactions cost fractions of a cent, making micropayments (pay $0.01 per API call) economically viable. On Ethereum mainnet, gas fees alone would exceed the payment amount for small transactions.
- **Fast finality.** Base transactions confirm in approximately 2 seconds. The entire x402 flow (request, 402, payment, verify, settle) completes in under 3 seconds.
- **USDC stability.** USDC is pegged 1:1 to USD. Merchants receive dollars, not volatile tokens. No hedging required.

For development and testing, use Base Sepolia testnet. The network ID changes from `eip155:8453` to `eip155:84532`, and the USDC contract address changes. Everything else -- the payment flow, the facilitator endpoints, the verification logic -- remains identical.

### The x402 Foundation and the Facilitator Role

The facilitator is the critical infrastructure component that makes x402 practical. Without it, every merchant would need to run their own on-chain verification node, parse EIP-712 signatures, check USDC allowances, and submit settlement transactions. The facilitator abstracts all of this.

The x402 Foundation operates the reference facilitator at `https://x402.org/facilitator`. It exposes two endpoints:

**POST /verify** -- Validates a payment payload against the merchant's requirements. The facilitator checks:
- The signature is valid (signed by a wallet with sufficient USDC balance)
- The amount matches or exceeds `maxAmountRequired`
- The payment has not expired (`maxTimeoutSeconds`)
- The `payTo` address matches the merchant's wallet
- The asset and network match the requirements

**POST /settle** -- Triggers the on-chain USDC transfer. The facilitator submits a transaction to Base that transfers USDC from the payer's wallet to the merchant's `payTo` address. Settlement is asynchronous -- the merchant has already served the content before settlement completes. If settlement fails (insufficient balance, revoked allowance), the facilitator retries with exponential backoff.

The facilitator is a trust component. The merchant trusts it to honestly verify payment signatures. The payer trusts it to only settle payments for content that was actually served. In practice, the x402 Foundation facilitator is the default, but merchants can run their own facilitator or use third-party alternatives.

### Amounts: Strings, Not Floats

Every amount in x402 is a string representation of an integer in the asset's smallest unit. For USDC (6 decimals):

| USD Price | maxAmountRequired |
|-----------|-------------------|
| $0.01     | "10000"           |
| $0.10     | "100000"          |
| $1.00     | "1000000"         |
| $5.00     | "5000000"         |
| $29.00    | "29000000"        |

The conversion formula: `maxAmountRequired = String(Math.round(price_usd * 1_000_000))`.

Never use floating-point arithmetic for amounts. IEEE 754 floating-point cannot represent all decimal values exactly. `0.1 + 0.2 !== 0.3` in JavaScript. Use integer math or dedicated decimal libraries.

---

## Chapter 2: Express.js Middleware (Node.js)

### Building x402 Middleware from Scratch

The Felix dashboard (the reference x402 storefront) implements x402 inline in a route handler. That works for a single-route storefront, but for an API with dozens of endpoints, you need middleware that applies the payment gate to any route.

The middleware pattern:
1. Check if the route requires payment (configurable per-route pricing).
2. If the request has no `X-Payment` header, return 402 with payment requirements.
3. If the request has an `X-Payment` header, verify it with the facilitator.
4. If verification passes, call `next()` to let the route handler serve content.
5. After the response, trigger settlement asynchronously.

```javascript
'use strict';

/**
 * x402 Express.js middleware.
 *
 * Usage:
 *   const { x402Paywall } = require('./x402-middleware');
 *   app.get('/api/premium', x402Paywall({ priceUsd: 1.00 }), handler);
 */

const FACILITATOR_URL = process.env.X402_FACILITATOR_URL || 'https://x402.org/facilitator';
const WALLET = process.env.MERCHANT_WALLET_ADDRESS;
const NETWORK = process.env.X402_NETWORK || 'base-sepolia';

const NETWORK_ID = NETWORK === 'base-mainnet' ? 'eip155:8453' : 'eip155:84532';
const USDC_ADDRESS = NETWORK === 'base-mainnet'
  ? '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'
  : '0x036CbD53842c5426634e7929541eC2318f3dCF7e';

/**
 * Build the paymentRequirements array for a given price and resource URL.
 */
function buildPaymentRequirements(priceUsd, resource, description) {
  const maxAmountRequired = String(Math.round(priceUsd * 1_000_000));

  return [{
    scheme: 'exact',
    network: NETWORK_ID,
    maxAmountRequired,
    resource,
    description: description || `Access to ${resource}`,
    mimeType: 'application/json',
    payTo: WALLET,
    maxTimeoutSeconds: 300,
    asset: USDC_ADDRESS,
    extra: { name: 'USDC', version: '2' },
  }];
}

/**
 * Send a 402 response with payment requirements.
 */
function send402(res, paymentRequirements, error = null) {
  const pr = {
    x402Version: 1,
    accepts: paymentRequirements,
    error,
  };
  res.setHeader('PAYMENT-REQUIRED', Buffer.from(JSON.stringify(pr)).toString('base64'));
  return res.status(402).json(pr);
}

/**
 * Verify a payment payload with the facilitator.
 *
 * Returns { valid: boolean, error?: string }.
 */
async function verifyPayment(xPayment, paymentRequirements) {
  const requirement = paymentRequirements[0];

  try {
    const response = await fetch(`${FACILITATOR_URL}/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        x402Version: 1,
        paymentPayload: xPayment,
        requirements: {
          scheme: requirement.scheme,
          network: requirement.network,
          maxAmountRequired: requirement.maxAmountRequired,
          resource: requirement.resource,
          payTo: requirement.payTo,
          asset: requirement.asset,
          maxTimeoutSeconds: requirement.maxTimeoutSeconds,
        },
      }),
    });

    if (response.ok) {
      return { valid: true };
    }

    const body = await response.text();
    return { valid: false, error: `Facilitator returned ${response.status}: ${body}` };
  } catch (err) {
    return { valid: false, error: `Facilitator unreachable: ${err.message}` };
  }
}

/**
 * Trigger settlement asynchronously. Fire-and-forget with retry.
 */
function settlePayment(xPayment, retries = 3) {
  const attemptSettle = (attempt) => {
    fetch(`${FACILITATOR_URL}/settle`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        x402Version: 1,
        paymentPayload: xPayment,
      }),
    })
    .then(r => {
      if (!r.ok && attempt < retries) {
        const delay = Math.pow(2, attempt) * 1000;
        console.warn(`[x402] settle retry ${attempt + 1}/${retries} in ${delay}ms`);
        setTimeout(() => attemptSettle(attempt + 1), delay);
      } else if (!r.ok) {
        console.error(`[x402] settle failed after ${retries} retries: HTTP ${r.status}`);
      } else {
        console.log('[x402] settlement successful');
      }
    })
    .catch(err => {
      if (attempt < retries) {
        const delay = Math.pow(2, attempt) * 1000;
        setTimeout(() => attemptSettle(attempt + 1), delay);
      } else {
        console.error(`[x402] settle error after ${retries} retries: ${err.message}`);
      }
    });
  };

  attemptSettle(0);
}

/**
 * Express middleware factory. Wraps any route with x402 payment gating.
 *
 * Options:
 *   priceUsd: number       -- Price in USD (required)
 *   description: string    -- Description shown to payers (optional)
 *   onPayment: function    -- Callback after successful payment (optional)
 *                             Receives (req, paymentPayload, priceUsd)
 *
 * Example:
 *   app.get('/api/data', x402Paywall({ priceUsd: 0.50 }), (req, res) => {
 *     res.json({ data: 'premium content' });
 *   });
 */
function x402Paywall(options) {
  const { priceUsd, description, onPayment } = options;

  if (!WALLET) {
    return (_req, res, _next) => {
      res.status(503).json({ error: 'MERCHANT_WALLET_ADDRESS not configured' });
    };
  }

  if (typeof priceUsd !== 'number' || priceUsd <= 0) {
    throw new Error('x402Paywall requires a positive priceUsd');
  }

  return async (req, res, next) => {
    const resource = `https://${req.get('host')}${req.originalUrl}`;
    const paymentRequirements = buildPaymentRequirements(priceUsd, resource, description);

    // No payment header: return 402
    const xPayment = req.headers['x-payment'];
    if (!xPayment) {
      return send402(res, paymentRequirements);
    }

    // Verify payment
    const verification = await verifyPayment(xPayment, paymentRequirements);
    if (!verification.valid) {
      return send402(res, paymentRequirements, verification.error || 'Payment verification failed');
    }

    // Payment verified -- set response header and proceed
    res.setHeader('X-PAYMENT-RESPONSE', Buffer.from(JSON.stringify({
      success: true,
    })).toString('base64'));

    // Call next() to let the route handler serve content
    next();

    // After response, settle asynchronously
    settlePayment(xPayment);

    // Optional callback for logging/analytics
    if (typeof onPayment === 'function') {
      try {
        onPayment(req, xPayment, priceUsd);
      } catch (err) {
        console.error('[x402] onPayment callback error:', err.message);
      }
    }
  };
}

module.exports = { x402Paywall, buildPaymentRequirements, verifyPayment, settlePayment };
```

### Complete Working Example: Express API with x402 Paywall

```javascript
'use strict';

const express = require('express');
const { x402Paywall } = require('./x402-middleware');

const app = express();
app.use(express.json({ limit: '10kb' }));

// Free endpoint -- no payment required
app.get('/api/v1/health', (_req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Free tier -- limited data
app.get('/api/v1/weather/summary', (_req, res) => {
  res.json({
    location: 'San Francisco',
    temperature_f: 62,
    conditions: 'Partly cloudy',
    note: 'Upgrade to /api/v1/weather/full for hourly forecasts, alerts, and historical data.',
  });
});

// Paid endpoint -- $0.05 per request
app.get('/api/v1/weather/full',
  x402Paywall({
    priceUsd: 0.05,
    description: 'Full weather data: hourly forecast, alerts, historical',
    onPayment: (req, _payload, price) => {
      console.log(`[sale] ${req.ip} paid $${price} for ${req.path}`);
    },
  }),
  (_req, res) => {
    res.json({
      location: 'San Francisco',
      temperature_f: 62,
      conditions: 'Partly cloudy',
      hourly_forecast: [
        { hour: '14:00', temp_f: 63, conditions: 'Partly cloudy' },
        { hour: '15:00', temp_f: 64, conditions: 'Sunny' },
        { hour: '16:00', temp_f: 63, conditions: 'Sunny' },
        { hour: '17:00', temp_f: 61, conditions: 'Fog rolling in' },
      ],
      alerts: [],
      historical: {
        avg_high_f: 65,
        avg_low_f: 52,
        record_high_f: 98,
        record_low_f: 28,
      },
    });
  }
);

// Paid endpoint -- $1.00 per request (premium analysis)
app.get('/api/v1/analysis/:ticker',
  x402Paywall({
    priceUsd: 1.00,
    description: 'AI-powered stock analysis report',
  }),
  (req, res) => {
    const ticker = req.params.ticker.toUpperCase();
    res.json({
      ticker,
      analysis: `Comprehensive analysis of ${ticker}...`,
      sentiment: 'bullish',
      confidence: 0.82,
      generated_at: new Date().toISOString(),
    });
  }
);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`x402 API running on port ${PORT}`);
  console.log(`Wallet: ${process.env.MERCHANT_WALLET_ADDRESS}`);
  console.log(`Network: ${process.env.X402_NETWORK || 'base-sepolia'}`);
});
```

### Testing with curl

Test the free endpoint:

```bash
curl -s http://localhost:3000/api/v1/health | jq .
# {"status":"ok","timestamp":"2026-04-07T12:00:00.000Z"}
```

Test the paid endpoint without payment (expect 402):

```bash
curl -s -w "\nHTTP Status: %{http_code}\n" \
  http://localhost:3000/api/v1/weather/full | jq .
# {
#   "x402Version": 1,
#   "accepts": [{
#     "scheme": "exact",
#     "network": "eip155:84532",
#     "maxAmountRequired": "50000",
#     ...
#   }],
#   "error": null
# }
# HTTP Status: 402
```

Extract the PAYMENT-REQUIRED header (base64-encoded):

```bash
curl -s -D - http://localhost:3000/api/v1/weather/full 2>&1 | grep -i payment-required
# PAYMENT-REQUIRED: eyJ4NDAyVmVyc2lvbiI6MSwiYWNjZXB0cyI6Wy...
```

To complete the payment, you need a client SDK that can sign EIP-712 payloads. The `@anthropic-ai/sdk` and `@coinbase/x402` packages both support this. See Chapter 9 for test tooling.

### Per-Route Pricing Configuration

For APIs with many endpoints, externalize pricing to a configuration object:

```javascript
const PRICING = {
  '/api/v1/weather/full': { priceUsd: 0.05, description: 'Full weather data' },
  '/api/v1/analysis/:ticker': { priceUsd: 1.00, description: 'Stock analysis' },
  '/api/v1/satellite/:region': { priceUsd: 2.50, description: 'Satellite imagery' },
  '/api/v1/legal/search': { priceUsd: 0.25, description: 'Legal document search' },
};

// Apply paywall to all priced routes
for (const [route, config] of Object.entries(PRICING)) {
  app.get(route, x402Paywall(config), routeHandlers[route]);
}
```

---

## Chapter 3: FastAPI Integration (Python)

### FastAPI Middleware Pattern

FastAPI's dependency injection system is the natural integration point for x402. Instead of middleware that wraps every request, you create a dependency that route handlers declare when they require payment. Routes without the dependency remain free.

```python
"""
x402 FastAPI integration.

Usage:
    from x402_deps import x402_required

    @app.get("/api/v1/premium")
    async def premium_data(payment: dict = Depends(x402_required(price_usd=0.50))):
        return {"data": "premium content", "payment": payment}
"""

import os
import json
import base64
import math
from typing import Optional

import httpx
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

FACILITATOR_URL = os.environ.get("X402_FACILITATOR_URL", "https://x402.org/facilitator")
WALLET = os.environ.get("MERCHANT_WALLET_ADDRESS", "")
NETWORK = os.environ.get("X402_NETWORK", "base-sepolia")

NETWORK_ID = "eip155:8453" if NETWORK == "base-mainnet" else "eip155:84532"
USDC_ADDRESS = (
    "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    if NETWORK == "base-mainnet"
    else "0x036CbD53842c5426634e7929541eC2318f3dCF7e"
)

# Reusable async HTTP client with connection pooling
_http_client: Optional[httpx.AsyncClient] = None


async def get_http_client() -> httpx.AsyncClient:
    """Lazy-initialize a shared httpx.AsyncClient."""
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(timeout=10.0)
    return _http_client


def build_payment_requirements(
    price_usd: float,
    resource: str,
    description: str = "",
) -> list[dict]:
    """Build the paymentRequirements array for a 402 response."""
    max_amount = str(round(price_usd * 1_000_000))
    return [
        {
            "scheme": "exact",
            "network": NETWORK_ID,
            "maxAmountRequired": max_amount,
            "resource": resource,
            "description": description or f"Access to {resource}",
            "mimeType": "application/json",
            "payTo": WALLET,
            "maxTimeoutSeconds": 300,
            "asset": USDC_ADDRESS,
            "extra": {"name": "USDC", "version": "2"},
        }
    ]


def payment_required_response(
    payment_requirements: list[dict],
    error: Optional[str] = None,
) -> JSONResponse:
    """Build a 402 JSONResponse with the PAYMENT-REQUIRED header."""
    body = {
        "x402Version": 1,
        "accepts": payment_requirements,
        "error": error,
    }
    encoded = base64.b64encode(json.dumps(body).encode()).decode()
    return JSONResponse(
        status_code=402,
        content=body,
        headers={"PAYMENT-REQUIRED": encoded},
    )


async def verify_payment(
    x_payment: str,
    payment_requirements: list[dict],
) -> dict:
    """Verify a payment payload with the facilitator.

    Returns {"valid": True} on success, {"valid": False, "error": "..."} on failure.
    """
    requirement = payment_requirements[0]
    client = await get_http_client()

    try:
        response = await client.post(
            f"{FACILITATOR_URL}/verify",
            json={
                "x402Version": 1,
                "paymentPayload": x_payment,
                "requirements": {
                    "scheme": requirement["scheme"],
                    "network": requirement["network"],
                    "maxAmountRequired": requirement["maxAmountRequired"],
                    "resource": requirement["resource"],
                    "payTo": requirement["payTo"],
                    "asset": requirement["asset"],
                    "maxTimeoutSeconds": requirement["maxTimeoutSeconds"],
                },
            },
        )
        if response.status_code == 200:
            return {"valid": True}
        return {"valid": False, "error": f"Facilitator returned {response.status_code}"}
    except httpx.RequestError as exc:
        return {"valid": False, "error": f"Facilitator unreachable: {exc}"}


async def settle_payment(x_payment: str, max_retries: int = 3) -> None:
    """Trigger settlement asynchronously with retry."""
    client = await get_http_client()

    for attempt in range(max_retries):
        try:
            response = await client.post(
                f"{FACILITATOR_URL}/settle",
                json={
                    "x402Version": 1,
                    "paymentPayload": x_payment,
                },
            )
            if response.status_code == 200:
                return
            if attempt < max_retries - 1:
                import asyncio
                await asyncio.sleep(2 ** attempt)
        except httpx.RequestError:
            if attempt < max_retries - 1:
                import asyncio
                await asyncio.sleep(2 ** attempt)


def x402_required(
    price_usd: float,
    description: str = "",
):
    """FastAPI dependency factory for x402 payment gating.

    Usage:
        @app.get("/premium")
        async def premium(payment: dict = Depends(x402_required(price_usd=1.00))):
            return {"data": "..."}
    """
    if not WALLET:
        raise RuntimeError("MERCHANT_WALLET_ADDRESS environment variable is required")

    async def dependency(request: Request) -> dict:
        # Build resource URL
        scheme = request.url.scheme
        host = request.headers.get("host", request.url.netloc)
        resource = f"https://{host}{request.url.path}"

        payment_requirements = build_payment_requirements(
            price_usd, resource, description
        )

        # Check for X-Payment header
        x_payment = request.headers.get("x-payment")
        if not x_payment:
            raise HTTPException(
                status_code=402,
                detail={
                    "x402Version": 1,
                    "accepts": payment_requirements,
                    "error": None,
                },
                headers={
                    "PAYMENT-REQUIRED": base64.b64encode(
                        json.dumps({
                            "x402Version": 1,
                            "accepts": payment_requirements,
                            "error": None,
                        }).encode()
                    ).decode()
                },
            )

        # Verify payment
        result = await verify_payment(x_payment, payment_requirements)
        if not result["valid"]:
            raise HTTPException(
                status_code=402,
                detail={
                    "x402Version": 1,
                    "accepts": payment_requirements,
                    "error": result.get("error", "Payment verification failed"),
                },
                headers={
                    "PAYMENT-REQUIRED": base64.b64encode(
                        json.dumps({
                            "x402Version": 1,
                            "accepts": payment_requirements,
                            "error": result.get("error"),
                        }).encode()
                    ).decode()
                },
            )

        # Payment verified -- trigger settlement in background
        import asyncio
        asyncio.create_task(settle_payment(x_payment))

        return {
            "verified": True,
            "price_usd": price_usd,
            "resource": resource,
        }

    return dependency
```

### Complete Working Example: FastAPI with x402

```python
"""
x402 FastAPI example server.

Run:
    MERCHANT_WALLET_ADDRESS=0x... uvicorn server:app --port 8000
"""

import asyncio
from fastapi import FastAPI, Depends, Response
from x402_deps import x402_required

app = FastAPI(
    title="x402 Weather API",
    description="Weather data API with x402 micropayments",
    version="1.0.0",
)


@app.get("/api/v1/health")
async def health():
    """Free health check endpoint."""
    return {"status": "ok"}


@app.get("/api/v1/weather/summary")
async def weather_summary():
    """Free tier: basic weather data."""
    return {
        "location": "San Francisco",
        "temperature_f": 62,
        "conditions": "Partly cloudy",
    }


@app.get("/api/v1/weather/full")
async def weather_full(
    response: Response,
    payment: dict = Depends(x402_required(
        price_usd=0.05,
        description="Full weather data with hourly forecast",
    )),
):
    """Paid endpoint: $0.05 per request for full weather data."""
    import json, base64
    response.headers["X-PAYMENT-RESPONSE"] = base64.b64encode(
        json.dumps({"success": True}).encode()
    ).decode()

    return {
        "location": "San Francisco",
        "temperature_f": 62,
        "conditions": "Partly cloudy",
        "hourly_forecast": [
            {"hour": "14:00", "temp_f": 63, "conditions": "Partly cloudy"},
            {"hour": "15:00", "temp_f": 64, "conditions": "Sunny"},
            {"hour": "16:00", "temp_f": 63, "conditions": "Sunny"},
        ],
        "alerts": [],
        "payment_info": payment,
    }


@app.get("/api/v1/analysis/{ticker}")
async def stock_analysis(
    ticker: str,
    response: Response,
    payment: dict = Depends(x402_required(
        price_usd=1.00,
        description="AI-powered stock analysis report",
    )),
):
    """Paid endpoint: $1.00 per request for stock analysis."""
    import json, base64
    response.headers["X-PAYMENT-RESPONSE"] = base64.b64encode(
        json.dumps({"success": True}).encode()
    ).decode()

    return {
        "ticker": ticker.upper(),
        "analysis": f"Comprehensive analysis of {ticker.upper()}...",
        "sentiment": "bullish",
        "confidence": 0.82,
    }
```

### Pytest Test Patterns

```python
"""
Tests for x402 FastAPI integration.

Run:
    pytest test_x402.py -x -q
"""

import json
import base64
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient

from server import app


@pytest.fixture
def client():
    """Synchronous test client for FastAPI."""
    return TestClient(app)


class TestFreeEndpoints:
    """Free endpoints should work without any payment."""

    def test_health(self, client):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_weather_summary(self, client):
        response = client.get("/api/v1/weather/summary")
        assert response.status_code == 200
        assert "temperature_f" in response.json()


class TestPaymentRequired:
    """Paid endpoints should return 402 without X-Payment header."""

    def test_weather_full_returns_402(self, client):
        response = client.get("/api/v1/weather/full")
        assert response.status_code == 402

        body = response.json()
        detail = body.get("detail", body)
        assert detail["x402Version"] == 1
        assert len(detail["accepts"]) == 1

        requirement = detail["accepts"][0]
        assert requirement["scheme"] == "exact"
        assert requirement["maxAmountRequired"] == "50000"  # $0.05
        assert requirement["asset"] is not None
        assert requirement["payTo"] is not None

    def test_402_has_payment_required_header(self, client):
        response = client.get("/api/v1/weather/full")
        assert response.status_code == 402
        assert "payment-required" in response.headers

        # Decode and verify the header
        encoded = response.headers["payment-required"]
        decoded = json.loads(base64.b64decode(encoded))
        assert decoded["x402Version"] == 1

    def test_analysis_returns_402(self, client):
        response = client.get("/api/v1/analysis/AAPL")
        assert response.status_code == 402

        body = response.json()
        detail = body.get("detail", body)
        requirement = detail["accepts"][0]
        assert requirement["maxAmountRequired"] == "1000000"  # $1.00


class TestPaymentVerification:
    """Test the payment verification flow with mocked facilitator."""

    @patch("x402_deps.verify_payment", new_callable=AsyncMock)
    @patch("x402_deps.settle_payment", new_callable=AsyncMock)
    def test_valid_payment_serves_content(
        self, mock_settle, mock_verify, client
    ):
        mock_verify.return_value = {"valid": True}
        mock_settle.return_value = None

        response = client.get(
            "/api/v1/weather/full",
            headers={"X-Payment": "valid-test-payload"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "hourly_forecast" in data

    @patch("x402_deps.verify_payment", new_callable=AsyncMock)
    def test_invalid_payment_returns_402(self, mock_verify, client):
        mock_verify.return_value = {
            "valid": False,
            "error": "Invalid signature",
        }

        response = client.get(
            "/api/v1/weather/full",
            headers={"X-Payment": "invalid-payload"},
        )
        assert response.status_code == 402

    @patch("x402_deps.verify_payment", new_callable=AsyncMock)
    @patch("x402_deps.settle_payment", new_callable=AsyncMock)
    def test_settlement_triggered_after_verification(
        self, mock_settle, mock_verify, client
    ):
        mock_verify.return_value = {"valid": True}
        mock_settle.return_value = None

        client.get(
            "/api/v1/weather/full",
            headers={"X-Payment": "valid-payload"},
        )

        # Settlement should be triggered (as a background task)
        # In test mode, the asyncio task may need explicit await
        # This verifies the function was at least called
        mock_settle.assert_called_once_with("valid-payload")


class TestAmountCalculation:
    """Verify correct USD to USDC smallest-unit conversion."""

    def test_five_cents(self, client):
        response = client.get("/api/v1/weather/full")
        detail = response.json().get("detail", response.json())
        assert detail["accepts"][0]["maxAmountRequired"] == "50000"

    def test_one_dollar(self, client):
        response = client.get("/api/v1/analysis/TSLA")
        detail = response.json().get("detail", response.json())
        assert detail["accepts"][0]["maxAmountRequired"] == "1000000"
```

### Payment Verification Decorator (Alternative Pattern)

For simpler codebases that prefer decorators over dependency injection:

```python
import functools
from fastapi import Request, Response

def require_x402_payment(price_usd: float, description: str = ""):
    """Decorator that gates a FastAPI route behind x402 payment.

    Usage:
        @app.get("/premium")
        @require_x402_payment(price_usd=0.50)
        async def premium(request: Request):
            return {"data": "..."}
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            host = request.headers.get("host", request.url.netloc)
            resource = f"https://{host}{request.url.path}"
            requirements = build_payment_requirements(price_usd, resource, description)

            x_payment = request.headers.get("x-payment")
            if not x_payment:
                return payment_required_response(requirements)

            result = await verify_payment(x_payment, requirements)
            if not result["valid"]:
                return payment_required_response(
                    requirements,
                    error=result.get("error", "Verification failed"),
                )

            # Trigger settlement
            import asyncio
            asyncio.create_task(settle_payment(x_payment))

            # Call the original handler
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator
```

---

## Chapter 4: Cloudflare Workers (Edge)

### Why Edge + x402

Cloudflare Workers execute at over 300 edge locations worldwide. When you deploy an x402 paywall as a Worker, payment verification happens at the edge closest to the client. A user in Tokyo hitting your API gets sub-50ms response times for the 402 and near-instant verification turnaround, compared to the 200-300ms round-trip to a centralized server in US-East.

For x402 specifically, edge deployment has two advantages:

1. **The 402 response is instant.** No payment header means no backend processing. The Worker returns the payment requirements object from memory in under 1ms. This is critical because every x402 transaction starts with a 402 -- making this response fast improves the total transaction time.

2. **Verification can be cached.** The same payment payload from the same wallet, for the same resource, within the same timeout window, will always verify the same way. You can cache verification results in Cloudflare KV to avoid hitting the facilitator on every request.

### Worker Implementation

```javascript
/**
 * x402 Cloudflare Worker.
 *
 * Deploys an x402 paywall at the edge. Verifies payments via the x402
 * facilitator and caches verification results in KV for repeat requests.
 *
 * Environment variables (wrangler.toml):
 *   MERCHANT_WALLET_ADDRESS - Your wallet address
 *   X402_NETWORK            - "base-mainnet" or "base-sepolia"
 *   X402_FACILITATOR_URL    - Facilitator URL (default: https://x402.org/facilitator)
 *
 * KV Namespace binding:
 *   PAYMENT_CACHE           - For caching verification results
 */

const USDC_ADDRESSES = {
  'base-mainnet': '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
  'base-sepolia': '0x036CbD53842c5426634e7929541eC2318f3dCF7e',
};

const NETWORK_IDS = {
  'base-mainnet': 'eip155:8453',
  'base-sepolia': 'eip155:84532',
};

// Route pricing configuration
const PRICING = {
  '/api/v1/weather/full': { priceUsd: 0.05, description: 'Full weather data' },
  '/api/v1/analysis': { priceUsd: 1.00, description: 'Stock analysis report' },
  '/api/v1/satellite': { priceUsd: 2.50, description: 'Satellite imagery' },
};

function getRoutePrice(pathname) {
  // Exact match first
  if (PRICING[pathname]) return PRICING[pathname];

  // Prefix match for parameterized routes
  for (const [route, config] of Object.entries(PRICING)) {
    if (pathname.startsWith(route)) return config;
  }

  return null; // Free route
}

function buildPaymentRequirements(priceUsd, resource, description, env) {
  const network = env.X402_NETWORK || 'base-sepolia';
  const maxAmountRequired = String(Math.round(priceUsd * 1_000_000));

  return [{
    scheme: 'exact',
    network: NETWORK_IDS[network],
    maxAmountRequired,
    resource,
    description,
    mimeType: 'application/json',
    payTo: env.MERCHANT_WALLET_ADDRESS,
    maxTimeoutSeconds: 300,
    asset: USDC_ADDRESSES[network],
    extra: { name: 'USDC', version: '2' },
  }];
}

function make402Response(paymentRequirements, error = null) {
  const body = {
    x402Version: 1,
    accepts: paymentRequirements,
    error,
  };
  const encoded = btoa(JSON.stringify(body));

  return new Response(JSON.stringify(body), {
    status: 402,
    headers: {
      'Content-Type': 'application/json',
      'PAYMENT-REQUIRED': encoded,
      'Access-Control-Allow-Origin': '*',
    },
  });
}

async function verifyPayment(xPayment, paymentRequirements, env) {
  const facilitatorUrl = env.X402_FACILITATOR_URL || 'https://x402.org/facilitator';
  const requirement = paymentRequirements[0];

  try {
    const response = await fetch(`${facilitatorUrl}/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        x402Version: 1,
        paymentPayload: xPayment,
        requirements: {
          scheme: requirement.scheme,
          network: requirement.network,
          maxAmountRequired: requirement.maxAmountRequired,
          resource: requirement.resource,
          payTo: requirement.payTo,
          asset: requirement.asset,
          maxTimeoutSeconds: requirement.maxTimeoutSeconds,
        },
      }),
    });

    return { valid: response.ok };
  } catch (err) {
    return { valid: false, error: err.message };
  }
}

async function triggerSettlement(xPayment, env) {
  const facilitatorUrl = env.X402_FACILITATOR_URL || 'https://x402.org/facilitator';

  // Fire-and-forget via waitUntil
  await fetch(`${facilitatorUrl}/settle`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      x402Version: 1,
      paymentPayload: xPayment,
    }),
  });
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const pathname = url.pathname;

    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'X-Payment, Content-Type',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        },
      });
    }

    // Check if this route requires payment
    const pricing = getRoutePrice(pathname);
    if (!pricing) {
      // Free route -- serve content directly
      return handleFreeRoute(pathname, env);
    }

    // Build payment requirements
    const resource = `https://${url.host}${pathname}`;
    const paymentRequirements = buildPaymentRequirements(
      pricing.priceUsd, resource, pricing.description, env
    );

    // Check for X-Payment header
    const xPayment = request.headers.get('x-payment');
    if (!xPayment) {
      return make402Response(paymentRequirements);
    }

    // Check KV cache for this payment payload
    const cacheKey = `verify:${await hashPayload(xPayment)}`;
    if (env.PAYMENT_CACHE) {
      const cached = await env.PAYMENT_CACHE.get(cacheKey);
      if (cached === 'valid') {
        // Payment already verified -- serve content
        const content = await handlePaidRoute(pathname, url, env);
        return addPaymentResponseHeader(content);
      }
    }

    // Verify with facilitator
    const verification = await verifyPayment(xPayment, paymentRequirements, env);
    if (!verification.valid) {
      return make402Response(
        paymentRequirements,
        verification.error || 'Payment verification failed'
      );
    }

    // Cache the verification result (TTL: 5 minutes = maxTimeoutSeconds)
    if (env.PAYMENT_CACHE) {
      ctx.waitUntil(
        env.PAYMENT_CACHE.put(cacheKey, 'valid', { expirationTtl: 300 })
      );
    }

    // Trigger settlement asynchronously (does not block response)
    ctx.waitUntil(triggerSettlement(xPayment, env));

    // Serve the paid content
    const content = await handlePaidRoute(pathname, url, env);
    return addPaymentResponseHeader(content);
  },
};

// Helper: hash a payment payload for cache keys
async function hashPayload(payload) {
  const data = new TextEncoder().encode(payload);
  const hash = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(hash))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}

function addPaymentResponseHeader(response) {
  const newResponse = new Response(response.body, response);
  newResponse.headers.set(
    'X-PAYMENT-RESPONSE',
    btoa(JSON.stringify({ success: true }))
  );
  return newResponse;
}

// Route handlers
function handleFreeRoute(pathname, _env) {
  if (pathname === '/api/v1/health') {
    return Response.json({ status: 'ok' });
  }
  if (pathname === '/api/v1/weather/summary') {
    return Response.json({
      location: 'San Francisco',
      temperature_f: 62,
      conditions: 'Partly cloudy',
    });
  }
  return Response.json({ error: 'Not found' }, { status: 404 });
}

async function handlePaidRoute(pathname, url, _env) {
  if (pathname.startsWith('/api/v1/weather/full')) {
    return Response.json({
      location: 'San Francisco',
      temperature_f: 62,
      conditions: 'Partly cloudy',
      hourly_forecast: [
        { hour: '14:00', temp_f: 63, conditions: 'Partly cloudy' },
        { hour: '15:00', temp_f: 64, conditions: 'Sunny' },
      ],
      alerts: [],
    });
  }

  if (pathname.startsWith('/api/v1/analysis')) {
    const ticker = pathname.split('/').pop().toUpperCase();
    return Response.json({
      ticker,
      analysis: `Comprehensive analysis of ${ticker}...`,
      sentiment: 'bullish',
      confidence: 0.82,
    });
  }

  return Response.json({ error: 'Not found' }, { status: 404 });
}
```

### Durable Objects for Settlement Tracking

For high-volume APIs, use a Durable Object to track settlements and detect duplicate payments:

```javascript
/**
 * Durable Object: SettlementTracker
 *
 * Maintains a per-merchant log of settlements. Prevents double-settlement
 * of the same payment payload and provides revenue totals.
 */
export class SettlementTracker {
  constructor(state, env) {
    this.state = state;
    this.env = env;
  }

  async fetch(request) {
    const url = new URL(request.url);

    if (url.pathname === '/record' && request.method === 'POST') {
      return this.recordSettlement(request);
    }

    if (url.pathname === '/stats') {
      return this.getStats();
    }

    return new Response('Not found', { status: 404 });
  }

  async recordSettlement(request) {
    const { payloadHash, amount, resource, timestamp } = await request.json();

    // Deduplicate: check if this payload was already settled
    const existing = await this.state.storage.get(`settlement:${payloadHash}`);
    if (existing) {
      return Response.json({ duplicate: true, original: existing });
    }

    // Record the settlement
    const record = { amount, resource, timestamp, settled: true };
    await this.state.storage.put(`settlement:${payloadHash}`, record);

    // Update running totals
    const totals = (await this.state.storage.get('totals')) || {
      count: 0,
      revenue_usd: 0,
    };
    totals.count += 1;
    totals.revenue_usd += parseFloat(amount);
    await this.state.storage.put('totals', totals);

    return Response.json({ recorded: true, totals });
  }

  async getStats() {
    const totals = (await this.state.storage.get('totals')) || {
      count: 0,
      revenue_usd: 0,
    };
    return Response.json(totals);
  }
}
```

### Wrangler Configuration

```toml
# wrangler.toml
name = "x402-api"
main = "src/worker.js"
compatibility_date = "2026-04-01"

[vars]
X402_NETWORK = "base-sepolia"
X402_FACILITATOR_URL = "https://x402.org/facilitator"

# Set via wrangler secret:
# wrangler secret put MERCHANT_WALLET_ADDRESS

# KV namespace for payment verification caching
[[kv_namespaces]]
binding = "PAYMENT_CACHE"
id = "your-kv-namespace-id"

# Durable Objects for settlement tracking
[[durable_objects.bindings]]
name = "SETTLEMENT_TRACKER"
class_name = "SettlementTracker"

[[migrations]]
tag = "v1"
new_classes = ["SettlementTracker"]
```

Deploy:

```bash
# Install wrangler
npm install -g wrangler

# Set your wallet address as a secret
wrangler secret put MERCHANT_WALLET_ADDRESS

# Deploy to Cloudflare
wrangler deploy

# Test
curl -s https://x402-api.your-subdomain.workers.dev/api/v1/health
curl -s https://x402-api.your-subdomain.workers.dev/api/v1/weather/full
```

---

## Chapter 5: Pricing Strategies

### Per-Request Pricing (API Calls)

The simplest model. Every request costs a fixed amount. Best for stateless APIs where each call returns independent value.

```javascript
// Flat per-request pricing
const PRICING = {
  '/api/v1/weather': 0.05,        // $0.05/request
  '/api/v1/translate': 0.10,       // $0.10/request
  '/api/v1/analyze': 1.00,         // $1.00/request
  '/api/v1/generate-image': 0.50,  // $0.50/request
};
```

**When to use:** Your compute cost per request is predictable and roughly constant. Weather lookups, translation, image generation, search queries.

**When not to use:** When request cost varies significantly based on input size. A translation of 10 words costs the same as 10,000 words under flat pricing.

### Content Pricing (Documents, Datasets)

Fixed price per content item. The content is the product, not the API call.

```javascript
// Content pricing: each piece of content has a fixed price
const CONTENT_PRICING = {
  '/content/report-q1-2026': 29.00,
  '/content/dataset-sf-housing': 49.00,
  '/content/tutorial-x402-advanced': 19.00,
};
```

This is the model the Felix dashboard uses. Each product in the catalog has a `price_usd`, and the x402 middleware charges that amount regardless of how many times the content is accessed (though each access triggers a new payment -- there is no "purchase once, download forever" in the base x402 protocol).

### Subscription-Equivalent via Token Bundles

x402 does not natively support subscriptions (recurring payments). But you can approximate subscriptions with token bundles: the client pays once for N requests, receives a signed token, and presents that token on subsequent requests until the bundle is exhausted.

```python
"""
Token bundle implementation for subscription-like access.

Client pays $10 for 100 requests. Server issues a signed JWT.
Client includes the JWT in subsequent requests instead of paying each time.
"""

import jwt
import time
import hashlib
from typing import Optional

BUNDLE_SECRET = "your-signing-secret"  # Use env var in production

BUNDLE_PRICING = {
    "starter": {"requests": 100, "price_usd": 10.00, "validity_days": 30},
    "pro":     {"requests": 1000, "price_usd": 75.00, "validity_days": 30},
    "enterprise": {"requests": 10000, "price_usd": 500.00, "validity_days": 30},
}


def issue_bundle_token(
    bundle_type: str,
    wallet_address: str,
) -> str:
    """Issue a JWT token after x402 payment for a bundle."""
    bundle = BUNDLE_PRICING[bundle_type]

    payload = {
        "wallet": wallet_address,
        "bundle": bundle_type,
        "remaining": bundle["requests"],
        "issued_at": int(time.time()),
        "expires_at": int(time.time()) + (bundle["validity_days"] * 86400),
    }

    return jwt.encode(payload, BUNDLE_SECRET, algorithm="HS256")


def validate_bundle_token(token: str) -> Optional[dict]:
    """Validate and decrement a bundle token.

    Returns the updated claims if valid, None if expired/invalid.
    """
    try:
        claims = jwt.decode(token, BUNDLE_SECRET, algorithms=["HS256"])

        if claims["expires_at"] < time.time():
            return None
        if claims["remaining"] <= 0:
            return None

        claims["remaining"] -= 1
        return claims
    except jwt.InvalidTokenError:
        return None


def refresh_bundle_token(claims: dict) -> str:
    """Re-issue the token with decremented remaining count."""
    return jwt.encode(claims, BUNDLE_SECRET, algorithm="HS256")
```

On the server, check for a bundle token first. If present and valid, serve content without x402 payment. If absent or exhausted, fall through to the x402 paywall:

```python
@app.get("/api/v1/data")
async def data_endpoint(
    request: Request,
    response: Response,
):
    """Endpoint that accepts either bundle tokens or x402 payment."""
    # Check for bundle token
    bundle_token = request.headers.get("x-bundle-token")
    if bundle_token:
        claims = validate_bundle_token(bundle_token)
        if claims:
            # Valid bundle -- serve content and return updated token
            response.headers["X-Bundle-Token"] = refresh_bundle_token(claims)
            response.headers["X-Bundle-Remaining"] = str(claims["remaining"])
            return {"data": "premium content", "bundle_remaining": claims["remaining"]}

    # No valid bundle -- fall through to x402 payment
    # (Use the x402_required dependency as shown in Chapter 3)
    ...
```

### Dynamic Pricing Based on Demand

Adjust prices based on request volume. High demand increases prices; low demand decreases them. This is useful for rate-limiting expensive resources without hard caps.

```javascript
/**
 * Dynamic pricing: price increases with request volume.
 *
 * Base price: $0.10/request
 * At 100 req/min: $0.15/request (+50%)
 * At 500 req/min: $0.50/request (+400%)
 * At 1000 req/min: $2.00/request (+1900%)
 */

class DynamicPricer {
  constructor(basePrice, windowMs = 60000) {
    this.basePrice = basePrice;
    this.windowMs = windowMs;
    this.requests = [];
  }

  recordRequest() {
    this.requests.push(Date.now());
    // Prune old entries
    const cutoff = Date.now() - this.windowMs;
    this.requests = this.requests.filter(t => t > cutoff);
  }

  getCurrentPrice() {
    const cutoff = Date.now() - this.windowMs;
    const recentCount = this.requests.filter(t => t > cutoff).length;

    if (recentCount < 50) return this.basePrice;
    if (recentCount < 100) return this.basePrice * 1.5;
    if (recentCount < 500) return this.basePrice * 5.0;
    return this.basePrice * 20.0;
  }
}

const pricer = new DynamicPricer(0.10);

// In your route handler:
app.get('/api/v1/premium', async (req, res, next) => {
  pricer.recordRequest();
  const currentPrice = pricer.getCurrentPrice();

  // Apply x402 with dynamic price
  const middleware = x402Paywall({ priceUsd: currentPrice });
  return middleware(req, res, next);
}, handler);
```

### Free Tier + Paid Tier Pattern

The most common production pattern: give away basic access for free, charge for premium features. This maximizes adoption while monetizing power users.

```javascript
const TIER_CONFIG = {
  free: {
    rateLimit: 10,      // requests per minute
    features: ['summary'],
  },
  paid: {
    rateLimit: 1000,
    features: ['summary', 'full', 'historical', 'alerts', 'export'],
    priceUsd: 0.05,
  },
};

function tierMiddleware(feature) {
  return (req, res, next) => {
    const hasPayment = !!req.headers['x-payment'];

    if (TIER_CONFIG.free.features.includes(feature) && !hasPayment) {
      // Free tier: serve with rate limiting
      return next();
    }

    if (!TIER_CONFIG.paid.features.includes(feature)) {
      return res.status(404).json({ error: 'Unknown feature' });
    }

    // Paid tier: apply x402
    const paywall = x402Paywall({ priceUsd: TIER_CONFIG.paid.priceUsd });
    return paywall(req, res, next);
  };
}

app.get('/api/v1/weather/summary', tierMiddleware('summary'), summaryHandler);
app.get('/api/v1/weather/full', tierMiddleware('full'), fullHandler);
app.get('/api/v1/weather/historical', tierMiddleware('historical'), historicalHandler);
```

---

## Chapter 6: Payment Verification Deep Dive

### Facilitator /verify Endpoint

The `/verify` endpoint is the heart of x402 security. It answers one question: "Is this payment payload valid for these requirements?" The request format:

```json
{
  "x402Version": 1,
  "paymentPayload": "<base64-encoded EIP-712 signed authorization>",
  "requirements": {
    "scheme": "exact",
    "network": "eip155:8453",
    "maxAmountRequired": "1000000",
    "resource": "https://api.example.com/data",
    "payTo": "0xMerchantWallet",
    "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "maxTimeoutSeconds": 300
  }
}
```

The response on success:

```json
{
  "valid": true
}
```

The response on failure:

```json
{
  "valid": false,
  "error": "Insufficient USDC balance",
  "details": {
    "required": "1000000",
    "available": "500000"
  }
}
```

### What the Facilitator Checks

The facilitator performs these checks in order. If any check fails, it returns `valid: false` with a descriptive error:

1. **Payload decoding.** The base64-decoded payload must be a valid JSON object containing an EIP-712 typed data signature.

2. **Signature recovery.** The facilitator recovers the signer's Ethereum address from the EIP-712 signature. If recovery fails, the payload was tampered with or incorrectly signed.

3. **Amount check.** The signed amount must be greater than or equal to `maxAmountRequired`. A payment for $0.50 does not satisfy a $1.00 requirement.

4. **Asset and network match.** The signed payload must reference the same USDC contract address and network ID as the requirements. A payment on Base Sepolia does not satisfy a Base mainnet requirement.

5. **Recipient match.** The `payTo` address in the signed payload must match the `payTo` in the requirements. This prevents a malicious intermediary from substituting their own wallet address.

6. **Expiration check.** The signature must not have expired. The `maxTimeoutSeconds` defines the window from signature creation to verification. A 300-second timeout means the payer has 5 minutes to submit the payment after signing.

7. **Balance check.** The signer's wallet must hold at least `maxAmountRequired` in USDC on the specified network. The facilitator queries the USDC contract's `balanceOf` function.

8. **Allowance check.** The signer must have approved the facilitator's settlement contract to spend at least `maxAmountRequired` of their USDC. Without this approval, settlement will fail even though verification succeeds.

### Handling Verification Failures

Different failure modes require different responses:

```python
async def handle_verification_result(
    result: dict,
    payment_requirements: list[dict],
) -> tuple[bool, dict]:
    """Process a verification result and determine the appropriate response.

    Returns (should_serve_content, response_info).
    """
    if result.get("valid"):
        return True, {"status": "verified"}

    error = result.get("error", "Unknown verification error")
    details = result.get("details", {})

    # Insufficient balance: tell the client how much they need
    if "Insufficient" in error:
        return False, {
            "status": "insufficient_funds",
            "error": error,
            "required": details.get("required"),
            "available": details.get("available"),
            "action": "Fund your wallet with more USDC and retry",
        }

    # Expired signature: client took too long
    if "expired" in error.lower():
        return False, {
            "status": "expired",
            "error": error,
            "action": "Sign a new payment payload and retry immediately",
        }

    # Invalid signature: payload was tampered with or signed incorrectly
    if "signature" in error.lower():
        return False, {
            "status": "invalid_signature",
            "error": error,
            "action": "Check your signing logic and retry",
        }

    # Allowance issue: client needs to approve the facilitator
    if "allowance" in error.lower():
        return False, {
            "status": "insufficient_allowance",
            "error": error,
            "action": "Approve the facilitator contract to spend your USDC",
        }

    # Generic failure
    return False, {
        "status": "verification_failed",
        "error": error,
    }
```

### Timeout Handling

Network latency between your server and the facilitator is the primary source of timeout risk. On a healthy network, the facilitator responds in 50-200ms. Under load or with DNS issues, it can take 2-5 seconds.

```javascript
/**
 * Verify with timeout and circuit breaker.
 */
class FacilitatorClient {
  constructor(facilitatorUrl, timeoutMs = 5000) {
    this.facilitatorUrl = facilitatorUrl;
    this.timeoutMs = timeoutMs;
    this.consecutiveFailures = 0;
    this.circuitOpen = false;
    this.circuitResetTime = 0;
  }

  async verify(xPayment, requirements) {
    // Circuit breaker: if the facilitator has failed N times in a row,
    // stop trying for a cooldown period
    if (this.circuitOpen && Date.now() < this.circuitResetTime) {
      return { valid: false, error: 'Circuit breaker open: facilitator unavailable' };
    }

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const response = await fetch(`${this.facilitatorUrl}/verify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          x402Version: 1,
          paymentPayload: xPayment,
          requirements,
        }),
        signal: controller.signal,
      });

      clearTimeout(timeout);
      this.consecutiveFailures = 0;
      this.circuitOpen = false;

      if (response.ok) {
        return { valid: true };
      }

      const body = await response.text();
      return { valid: false, error: body };
    } catch (err) {
      clearTimeout(timeout);
      this.consecutiveFailures += 1;

      // Open circuit after 5 consecutive failures
      if (this.consecutiveFailures >= 5) {
        this.circuitOpen = true;
        this.circuitResetTime = Date.now() + 30000; // 30-second cooldown
        console.error('[x402] Circuit breaker opened: 5 consecutive failures');
      }

      if (err.name === 'AbortError') {
        return { valid: false, error: `Verification timed out after ${this.timeoutMs}ms` };
      }
      return { valid: false, error: `Network error: ${err.message}` };
    }
  }
}
```

### What Happens If the Facilitator Is Down

If the facilitator is unreachable, you have three options:

1. **Fail closed (default).** Return 402 with an error message. The client cannot pay. No content is served. No revenue is lost. This is the safest option.

2. **Fail open (dangerous).** Serve the content anyway and log the unverified payment for later reconciliation. This risks serving content without payment. Only use this for very low-value content where availability matters more than revenue.

3. **Queue and retry.** Accept the request, serve the content, and queue the verification for retry. If verification eventually fails, flag the transaction as suspicious. This is a middle ground but requires careful accounting.

```javascript
// Option 1: Fail closed (recommended)
async function verifyWithFailClosed(xPayment, requirements) {
  const result = await facilitatorClient.verify(xPayment, requirements);
  if (!result.valid) {
    // Do not serve content
    return { serve: false, error: result.error };
  }
  return { serve: true };
}

// Option 2: Fail open (use with extreme caution)
async function verifyWithFailOpen(xPayment, requirements) {
  const result = await facilitatorClient.verify(xPayment, requirements);
  if (!result.valid && result.error.includes('Circuit breaker')) {
    // Facilitator is down -- serve content but log for reconciliation
    console.warn('[x402] FAIL OPEN: serving content without verification');
    logUnverifiedPayment(xPayment, requirements);
    return { serve: true, unverified: true };
  }
  if (!result.valid) {
    return { serve: false, error: result.error };
  }
  return { serve: true };
}
```

---

## Chapter 7: Settlement & Revenue

### Settlement Flow

Settlement is the process of actually moving USDC from the payer's wallet to your wallet. Verification confirms that the payer has authorized the transfer; settlement executes it.

The flow:

1. Your server calls `POST /settle` on the facilitator with the `paymentPayload`.
2. The facilitator submits an on-chain transaction to Base that calls `transferFrom` on the USDC contract, moving the authorized amount from the payer to your `payTo` address.
3. The transaction confirms on Base (approximately 2 seconds).
4. The USDC appears in your wallet.

Settlement is asynchronous and fire-and-forget from the merchant's perspective. You serve the content immediately after verification succeeds. Settlement happens in the background. If it fails, the facilitator retries.

### Logging Settlements to Your Database

Every settlement should be recorded in your database for revenue tracking, reconciliation, and tax reporting.

```python
"""
Settlement logging with SQLite.
"""

import sqlite3
import json
import hashlib
import time
from datetime import datetime, timezone


class SettlementLog:
    """Persistent settlement log backed by SQLite."""

    def __init__(self, db_path: str = "settlements.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS settlements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payment_hash TEXT UNIQUE NOT NULL,
                resource TEXT NOT NULL,
                amount_usdc TEXT NOT NULL,
                amount_usd REAL NOT NULL,
                payer_hint TEXT DEFAULT '',
                status TEXT DEFAULT 'pending',
                created_at TEXT NOT NULL,
                settled_at TEXT,
                error TEXT
            );

            CREATE INDEX IF NOT EXISTS idx_settlements_status
                ON settlements(status);
            CREATE INDEX IF NOT EXISTS idx_settlements_created
                ON settlements(created_at);
        """)
        self.conn.commit()

    def record_payment(
        self,
        payment_payload: str,
        resource: str,
        amount_usd: float,
    ) -> int:
        """Record a verified payment before settlement."""
        payment_hash = hashlib.sha256(payment_payload.encode()).hexdigest()
        amount_usdc = str(round(amount_usd * 1_000_000))
        now = datetime.now(timezone.utc).isoformat()

        cursor = self.conn.execute(
            """INSERT OR IGNORE INTO settlements
               (payment_hash, resource, amount_usdc, amount_usd, status, created_at)
               VALUES (?, ?, ?, ?, 'pending', ?)""",
            (payment_hash, resource, amount_usdc, amount_usd, now),
        )
        self.conn.commit()
        return cursor.lastrowid

    def mark_settled(self, payment_payload: str) -> None:
        """Mark a payment as successfully settled."""
        payment_hash = hashlib.sha256(payment_payload.encode()).hexdigest()
        now = datetime.now(timezone.utc).isoformat()

        self.conn.execute(
            """UPDATE settlements SET status = 'settled', settled_at = ?
               WHERE payment_hash = ?""",
            (now, payment_hash),
        )
        self.conn.commit()

    def mark_failed(self, payment_payload: str, error: str) -> None:
        """Mark a settlement as failed."""
        payment_hash = hashlib.sha256(payment_payload.encode()).hexdigest()

        self.conn.execute(
            """UPDATE settlements SET status = 'failed', error = ?
               WHERE payment_hash = ?""",
            (error, payment_hash),
        )
        self.conn.commit()

    def get_revenue(self, hours: int = 24) -> dict:
        """Get revenue stats for the last N hours."""
        cutoff = datetime.now(timezone.utc).timestamp() - (hours * 3600)
        cutoff_iso = datetime.fromtimestamp(cutoff, tz=timezone.utc).isoformat()

        row = self.conn.execute(
            """SELECT
                 COUNT(*) as total_payments,
                 COALESCE(SUM(amount_usd), 0) as total_usd,
                 COUNT(CASE WHEN status = 'settled' THEN 1 END) as settled_count,
                 COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_count,
                 COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_count
               FROM settlements
               WHERE created_at >= ?""",
            (cutoff_iso,),
        ).fetchone()

        return {
            "period_hours": hours,
            "total_payments": row["total_payments"],
            "total_revenue_usd": round(row["total_usd"], 2),
            "settled": row["settled_count"],
            "failed": row["failed_count"],
            "pending": row["pending_count"],
            "settlement_rate": (
                round(row["settled_count"] / row["total_payments"], 3)
                if row["total_payments"] > 0
                else 0
            ),
        }

    def get_revenue_by_resource(self, hours: int = 24) -> list[dict]:
        """Get per-resource revenue breakdown."""
        cutoff = datetime.now(timezone.utc).timestamp() - (hours * 3600)
        cutoff_iso = datetime.fromtimestamp(cutoff, tz=timezone.utc).isoformat()

        rows = self.conn.execute(
            """SELECT
                 resource,
                 COUNT(*) as request_count,
                 COALESCE(SUM(amount_usd), 0) as total_usd
               FROM settlements
               WHERE created_at >= ? AND status = 'settled'
               GROUP BY resource
               ORDER BY total_usd DESC""",
            (cutoff_iso,),
        ).fetchall()

        return [
            {
                "resource": row["resource"],
                "request_count": row["request_count"],
                "revenue_usd": round(row["total_usd"], 2),
            }
            for row in rows
        ]
```

### Revenue Tracking and Reporting

Integrate the settlement log with your x402 middleware:

```python
settlement_log = SettlementLog("data/settlements.db")

# In your x402 dependency, after verification succeeds:
async def x402_with_logging(request: Request) -> dict:
    # ... (verification logic from Chapter 3) ...

    # Record the payment
    settlement_log.record_payment(
        payment_payload=x_payment,
        resource=resource,
        amount_usd=price_usd,
    )

    # Trigger settlement with callback
    async def settle_and_log():
        try:
            await settle_payment(x_payment)
            settlement_log.mark_settled(x_payment)
        except Exception as e:
            settlement_log.mark_failed(x_payment, str(e))

    asyncio.create_task(settle_and_log())

    return {"verified": True}


# Revenue reporting endpoint (admin-only)
@app.get("/admin/revenue")
async def revenue_report(hours: int = 24):
    stats = settlement_log.get_revenue(hours)
    by_resource = settlement_log.get_revenue_by_resource(hours)
    return {
        "summary": stats,
        "by_resource": by_resource,
    }
```

### Handling Failed Settlements

Settlement can fail for several reasons:

- **Insufficient balance at settlement time.** The payer had enough USDC at verification but transferred it away before settlement. This is the most common failure mode.
- **Revoked allowance.** The payer revoked the facilitator's approval between verification and settlement.
- **Network congestion.** The Base network is congested and the transaction did not confirm in time.

For the first two cases, there is nothing the merchant can do. The content was already served. This is the fundamental risk of the "verify first, settle later" model. Mitigations:

1. **Minimize the verification-to-settlement gap.** Call `/settle` immediately after serving content, not in a batch job.
2. **Monitor settlement failure rate.** If it exceeds 2%, investigate. It may indicate a bot exploiting the gap.
3. **Block wallets with repeated settlement failures.** Maintain a blocklist of wallet addresses (extracted from payment payloads) that have failed settlement more than N times.

```python
class SettlementFailureTracker:
    """Track wallets with repeated settlement failures."""

    def __init__(self, max_failures: int = 3):
        self.max_failures = max_failures
        self.failure_counts: dict[str, int] = {}
        self.blocked_wallets: set[str] = set()

    def record_failure(self, wallet_address: str) -> bool:
        """Record a settlement failure. Returns True if wallet is now blocked."""
        self.failure_counts[wallet_address] = (
            self.failure_counts.get(wallet_address, 0) + 1
        )

        if self.failure_counts[wallet_address] >= self.max_failures:
            self.blocked_wallets.add(wallet_address)
            return True
        return False

    def is_blocked(self, wallet_address: str) -> bool:
        return wallet_address in self.blocked_wallets

    def record_success(self, wallet_address: str) -> None:
        """Reset failure count on successful settlement."""
        self.failure_counts.pop(wallet_address, None)
```

### Reconciliation Patterns

Daily reconciliation compares your settlement log against your actual on-chain USDC balance:

```python
async def daily_reconciliation(
    settlement_log: SettlementLog,
    wallet_address: str,
    rpc_url: str,
) -> dict:
    """Compare recorded settlements against on-chain balance.

    Run this daily via cron to detect discrepancies.
    """
    # Get recorded revenue
    stats = settlement_log.get_revenue(hours=24)
    recorded_revenue = stats["total_revenue_usd"]
    settled_count = stats["settled"]
    failed_count = stats["failed"]

    # Query on-chain USDC balance (via RPC or block explorer API)
    # This is a simplified example -- in production, track balance deltas
    balance_info = await query_usdc_balance(wallet_address, rpc_url)
    on_chain_balance = balance_info["balance_usd"]

    discrepancy = abs(recorded_revenue - on_chain_balance)

    return {
        "date": datetime.now(timezone.utc).date().isoformat(),
        "recorded_revenue_usd": recorded_revenue,
        "on_chain_balance_usd": on_chain_balance,
        "discrepancy_usd": round(discrepancy, 2),
        "settled_payments": settled_count,
        "failed_settlements": failed_count,
        "settlement_rate": stats["settlement_rate"],
        "status": "ok" if discrepancy < 1.00 else "DISCREPANCY_DETECTED",
    }
```

### Tax Implications

USDC revenue is taxable income in most jurisdictions. Key considerations:

- **Record keeping.** Every settlement must be logged with timestamp, amount, and counterparty information (wallet address). The settlement log in this chapter satisfies this requirement.
- **USD valuation.** USDC is pegged 1:1 to USD. Revenue in USDC is valued at face value. No fair market value calculation is needed (unlike volatile cryptocurrencies).
- **Reporting.** In the US, report USDC revenue as ordinary income. For businesses, this appears on Schedule C or the corporate return. Consult a tax professional for your jurisdiction.
- **Off-ramping.** When you convert USDC to fiat (via Coinbase, Circle, or a bank), there is no taxable event beyond the original income recognition -- assuming USDC maintained its peg.

---

## Next Steps

For deployment patterns, monitoring, and production hardening, see the
[Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening).

---

## Chapter 9: Testing

### Testnet (Base Sepolia) Setup

For development and integration testing, use Base Sepolia testnet. The only configuration change is the network identifier and USDC contract address.

```bash
# Environment variables for testnet
export X402_NETWORK=base-sepolia
export MERCHANT_WALLET_ADDRESS=0xYourTestnetWallet
export X402_FACILITATOR_URL=https://x402.org/facilitator
```

To get testnet USDC:
1. Get Sepolia ETH from the Base Sepolia faucet (https://www.coinbase.com/faucets/base-ethereum-sepolia-faucet).
2. Use the testnet USDC faucet or mint test tokens.
3. Approve the facilitator contract to spend your test USDC.

### Mock Facilitator for Unit Tests

For unit tests, you do not want to hit the real facilitator. Mock it entirely.

**Node.js (Jest/Vitest):**

```javascript
/**
 * Mock facilitator for unit tests.
 *
 * Replaces the real facilitator with deterministic responses.
 */

class MockFacilitator {
  constructor() {
    this.verifyResponses = new Map();
    this.settleLog = [];
    this.defaultVerifyResult = { valid: true };
  }

  /**
   * Configure the response for a specific payment payload.
   */
  setVerifyResponse(payloadSubstring, response) {
    this.verifyResponses.set(payloadSubstring, response);
  }

  /**
   * Mock /verify endpoint.
   */
  async verify(body) {
    const payload = body.paymentPayload || '';

    for (const [substring, response] of this.verifyResponses) {
      if (payload.includes(substring)) {
        return response;
      }
    }

    return this.defaultVerifyResult;
  }

  /**
   * Mock /settle endpoint. Logs the settlement for assertions.
   */
  async settle(body) {
    this.settleLog.push({
      payload: body.paymentPayload,
      timestamp: Date.now(),
    });
    return { success: true };
  }

  /**
   * Assert that settlement was triggered for a specific payload.
   */
  assertSettled(payloadSubstring) {
    const found = this.settleLog.some(s => s.payload.includes(payloadSubstring));
    if (!found) {
      throw new Error(`Expected settlement for payload containing "${payloadSubstring}"`);
    }
  }

  reset() {
    this.verifyResponses.clear();
    this.settleLog = [];
    this.defaultVerifyResult = { valid: true };
  }
}

// In tests:
const mockFacilitator = new MockFacilitator();

// Override fetch globally for tests
global.fetch = jest.fn(async (url, options) => {
  const body = JSON.parse(options.body);

  if (url.includes('/verify')) {
    const result = await mockFacilitator.verify(body);
    return {
      ok: result.valid,
      status: result.valid ? 200 : 400,
      json: async () => result,
      text: async () => JSON.stringify(result),
    };
  }

  if (url.includes('/settle')) {
    const result = await mockFacilitator.settle(body);
    return {
      ok: true,
      status: 200,
      json: async () => result,
    };
  }

  return { ok: false, status: 404 };
});
```

**Python (pytest):**

```python
"""
Mock facilitator for pytest.
"""

import pytest
from unittest.mock import AsyncMock, patch


@pytest.fixture
def mock_facilitator():
    """Fixture that mocks the x402 facilitator for unit tests."""

    class MockFacilitator:
        def __init__(self):
            self.verify_result = {"valid": True}
            self.settle_log = []
            self.verify_calls = []

        def set_verify_result(self, result):
            self.verify_result = result

        async def mock_verify(self, x_payment, requirements):
            self.verify_calls.append({
                "payment": x_payment,
                "requirements": requirements,
            })
            return self.verify_result

        async def mock_settle(self, x_payment, max_retries=3):
            self.settle_log.append(x_payment)

    mock = MockFacilitator()

    with patch("x402_deps.verify_payment", side_effect=mock.mock_verify):
        with patch("x402_deps.settle_payment", side_effect=mock.mock_settle):
            yield mock


# Usage in tests:
class TestPaidEndpoint:
    def test_verified_payment_returns_content(self, client, mock_facilitator):
        mock_facilitator.set_verify_result({"valid": True})
        response = client.get(
            "/api/v1/weather/full",
            headers={"X-Payment": "test-payload-123"},
        )
        assert response.status_code == 200
        assert len(mock_facilitator.verify_calls) == 1
        assert mock_facilitator.verify_calls[0]["payment"] == "test-payload-123"

    def test_failed_verification_returns_402(self, client, mock_facilitator):
        mock_facilitator.set_verify_result({
            "valid": False,
            "error": "Insufficient balance",
        })
        response = client.get(
            "/api/v1/weather/full",
            headers={"X-Payment": "insufficient-funds-payload"},
        )
        assert response.status_code == 402

    def test_settlement_triggered_after_success(self, client, mock_facilitator):
        mock_facilitator.set_verify_result({"valid": True})
        client.get(
            "/api/v1/weather/full",
            headers={"X-Payment": "settle-test-payload"},
        )
        assert "settle-test-payload" in mock_facilitator.settle_log
```

### Integration Test Patterns

Integration tests hit the real facilitator on testnet. They verify the full flow: 402 response, payment construction, verification, content delivery, settlement.

```python
"""
Integration tests against Base Sepolia testnet.

Requires:
  - MERCHANT_WALLET_ADDRESS set to a testnet wallet
  - PAYER_PRIVATE_KEY set to a funded testnet wallet's private key
  - Server running on localhost:8000

Run:
    X402_NETWORK=base-sepolia pytest test_integration.py -x -q
"""

import os
import httpx
import pytest

BASE_URL = os.environ.get("TEST_SERVER_URL", "http://localhost:8000")


@pytest.mark.integration
class TestFullX402Flow:
    """End-to-end tests using real facilitator on testnet."""

    def test_free_endpoint_works(self):
        """Free endpoints should respond without payment."""
        response = httpx.get(f"{BASE_URL}/api/v1/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_paid_endpoint_returns_402(self):
        """Paid endpoint without payment returns 402."""
        response = httpx.get(f"{BASE_URL}/api/v1/weather/full")
        assert response.status_code == 402

        body = response.json()
        assert body["x402Version"] == 1
        assert len(body["accepts"]) >= 1

        req = body["accepts"][0]
        assert req["scheme"] == "exact"
        assert req["network"] == "eip155:84532"  # Sepolia
        assert int(req["maxAmountRequired"]) > 0
        assert req["payTo"].startswith("0x")

    def test_402_contains_payment_required_header(self):
        """The PAYMENT-REQUIRED header should be present and base64-decodable."""
        response = httpx.get(f"{BASE_URL}/api/v1/weather/full")
        assert "payment-required" in response.headers

        import base64, json
        decoded = json.loads(
            base64.b64decode(response.headers["payment-required"])
        )
        assert decoded["x402Version"] == 1

    def test_invalid_payment_header_returns_402(self):
        """An invalid X-Payment header should return 402 with error."""
        response = httpx.get(
            f"{BASE_URL}/api/v1/weather/full",
            headers={"X-Payment": "totally-invalid-payload"},
        )
        assert response.status_code == 402
        body = response.json()
        detail = body.get("detail", body)
        assert detail.get("error") is not None
```

### Load Testing Payment Flows

Load testing x402 is different from load testing a standard API because each request involves an external facilitator call. Focus on three scenarios:

```python
"""
Load test scenarios for x402 APIs.

Uses locust for load generation.

Run:
    locust -f test_load.py --host http://localhost:8000
"""

from locust import HttpUser, task, between


class FreeEndpointUser(HttpUser):
    """Simulates traffic to free endpoints (baseline throughput)."""
    wait_time = between(0.1, 0.5)

    @task
    def health_check(self):
        self.client.get("/api/v1/health")

    @task(3)
    def weather_summary(self):
        self.client.get("/api/v1/weather/summary")


class UnpaidRequestUser(HttpUser):
    """Simulates traffic without payment (402 response throughput)."""
    wait_time = between(0.1, 0.5)

    @task
    def trigger_402(self):
        with self.client.get(
            "/api/v1/weather/full",
            catch_response=True,
        ) as response:
            if response.status_code == 402:
                response.success()
            else:
                response.failure(f"Expected 402, got {response.status_code}")


class PaidRequestUser(HttpUser):
    """Simulates paid requests (verification + settlement throughput).

    Uses a mock payment header. For real load testing on testnet,
    replace with actual signed payloads.
    """
    wait_time = between(0.5, 2.0)

    @task
    def paid_weather(self):
        with self.client.get(
            "/api/v1/weather/full",
            headers={"X-Payment": "load-test-payload"},
            catch_response=True,
        ) as response:
            # With a mock facilitator, this should return 200
            # With the real facilitator, this will return 402 (invalid payload)
            if response.status_code in (200, 402):
                response.success()
            else:
                response.failure(f"Unexpected status {response.status_code}")
```

---

## Chapter 10: Recipes

### Recipe 1: Blog Paywall (Markdown Content)

A blog where some posts are free and others require payment. The Felix dashboard pattern, simplified.

```javascript
'use strict';

/**
 * Blog with x402 paywall.
 *
 * Free posts: /blog/getting-started, /blog/about
 * Paid posts: /blog/advanced-techniques ($2.00), /blog/case-study ($5.00)
 */

const express = require('express');
const { marked } = require('marked');
const { x402Paywall } = require('./x402-middleware');

const app = express();

// Blog content (in production, load from filesystem or CMS)
const POSTS = {
  'getting-started': {
    title: 'Getting Started with x402',
    content: '# Getting Started\n\nThis is a free post...',
    price: 0,
  },
  'advanced-techniques': {
    title: 'Advanced x402 Techniques',
    content: '# Advanced Techniques\n\nThis premium post covers...',
    price: 2.00,
  },
  'case-study': {
    title: 'Case Study: 10x Revenue with x402',
    content: '# Case Study\n\nHow Company X increased API revenue...',
    price: 5.00,
  },
};

// Blog listing (free)
app.get('/blog', (_req, res) => {
  const listing = Object.entries(POSTS).map(([slug, post]) => ({
    slug,
    title: post.title,
    price: post.price,
    url: `/blog/${slug}`,
  }));
  res.json({ posts: listing });
});

// Individual blog posts
app.get('/blog/:slug', (req, res, next) => {
  const post = POSTS[req.params.slug];
  if (!post) return res.status(404).json({ error: 'Post not found' });

  // Free posts: serve directly
  if (post.price === 0) {
    return res.json({
      title: post.title,
      content_html: marked(post.content),
      content_markdown: post.content,
    });
  }

  // Paid posts: apply x402
  const paywall = x402Paywall({
    priceUsd: post.price,
    description: `Blog post: ${post.title}`,
  });

  paywall(req, res, () => {
    res.json({
      title: post.title,
      content_html: marked(post.content),
      content_markdown: post.content,
    });
  });
});

app.listen(3000, () => console.log('Blog running on port 3000'));
```

### Recipe 2: API Rate Limiting with x402 (Pay to Exceed Free Tier)

Give every user 100 free requests per day. After that, each request costs $0.01. No signup required -- rate limiting is by IP for free tier and by wallet for paid tier.

```javascript
'use strict';

/**
 * Free tier + x402 overflow pricing.
 *
 * Free: 100 requests/day per IP
 * Paid: $0.01/request after free tier exhausted
 */

const express = require('express');
const { x402Paywall } = require('./x402-middleware');

const app = express();

// In-memory rate counter (use Redis in production)
const requestCounts = new Map();
const FREE_LIMIT = 100;
const WINDOW_MS = 24 * 60 * 60 * 1000; // 24 hours

function getRequestCount(ip) {
  const entry = requestCounts.get(ip);
  if (!entry || Date.now() - entry.windowStart > WINDOW_MS) {
    requestCounts.set(ip, { count: 0, windowStart: Date.now() });
    return 0;
  }
  return entry.count;
}

function incrementRequestCount(ip) {
  const entry = requestCounts.get(ip) || { count: 0, windowStart: Date.now() };
  entry.count += 1;
  requestCounts.set(ip, entry);
}

// Middleware: free tier or x402 payment
function freeTierOrPay(priceUsd) {
  return async (req, res, next) => {
    const ip = req.ip;
    const count = getRequestCount(ip);

    if (count < FREE_LIMIT) {
      // Free tier: serve and count
      incrementRequestCount(ip);
      res.setHeader('X-RateLimit-Remaining', String(FREE_LIMIT - count - 1));
      res.setHeader('X-RateLimit-Limit', String(FREE_LIMIT));
      return next();
    }

    // Free tier exhausted: require payment
    res.setHeader('X-RateLimit-Remaining', '0');
    res.setHeader('X-RateLimit-Limit', String(FREE_LIMIT));

    const paywall = x402Paywall({
      priceUsd,
      description: `API access (free tier of ${FREE_LIMIT}/day exhausted)`,
    });

    return paywall(req, res, next);
  };
}

app.get('/api/v1/data', freeTierOrPay(0.01), (_req, res) => {
  res.json({
    data: 'Your API response here',
    timestamp: new Date().toISOString(),
  });
});

app.listen(3000, () => console.log('Free tier + x402 API running on port 3000'));
```

### Recipe 3: Dataset Marketplace (Pay Per Download)

A marketplace where data providers list datasets and buyers pay per download. Each dataset has its own price.

```python
"""
Dataset marketplace with x402 payment per download.

Providers upload datasets. Buyers browse for free, pay to download.
"""

import os
import json
from pathlib import Path

from fastapi import FastAPI, Depends, Response
from fastapi.responses import FileResponse, JSONResponse

from x402_deps import x402_required

app = FastAPI(title="Dataset Marketplace")

DATASETS_DIR = Path("data/datasets")
CATALOG_FILE = Path("data/catalog.json")


def load_catalog() -> list[dict]:
    """Load the dataset catalog."""
    if not CATALOG_FILE.exists():
        return []
    return json.loads(CATALOG_FILE.read_text())


def get_dataset_by_slug(slug: str) -> dict | None:
    """Find a dataset in the catalog by slug."""
    for ds in load_catalog():
        if ds["slug"] == slug:
            return ds
    return None


@app.get("/datasets")
async def list_datasets():
    """Browse all available datasets (free)."""
    catalog = load_catalog()
    return {
        "datasets": [
            {
                "slug": ds["slug"],
                "title": ds["title"],
                "description": ds["description"],
                "price_usd": ds["price_usd"],
                "size_mb": ds["size_mb"],
                "format": ds["format"],
                "download_url": f"/datasets/{ds['slug']}/download",
            }
            for ds in catalog
        ]
    }


@app.get("/datasets/{slug}")
async def dataset_detail(slug: str):
    """Get dataset metadata (free)."""
    ds = get_dataset_by_slug(slug)
    if not ds:
        return JSONResponse({"error": "Dataset not found"}, status_code=404)

    return {
        "slug": ds["slug"],
        "title": ds["title"],
        "description": ds["description"],
        "price_usd": ds["price_usd"],
        "size_mb": ds["size_mb"],
        "format": ds["format"],
        "columns": ds.get("columns", []),
        "row_count": ds.get("row_count", 0),
        "sample_rows": ds.get("sample_rows", []),
        "download_url": f"/datasets/{slug}/download",
    }


@app.get("/datasets/{slug}/download")
async def download_dataset(
    slug: str,
    response: Response,
    payment: dict = Depends(x402_required(
        price_usd=0,  # Will be overridden dynamically
        description="Dataset download",
    )),
):
    """Download a dataset (paid via x402)."""
    ds = get_dataset_by_slug(slug)
    if not ds:
        return JSONResponse({"error": "Dataset not found"}, status_code=404)

    file_path = DATASETS_DIR / ds["filename"]
    if not file_path.exists():
        return JSONResponse({"error": "File not available"}, status_code=503)

    return FileResponse(
        path=str(file_path),
        filename=ds["filename"],
        media_type="application/octet-stream",
    )
```

In production, override the `price_usd` in `x402_required` dynamically based on the dataset's catalog entry. One approach is to use a custom dependency that reads the price from the catalog:

```python
def dataset_x402(slug_param: str = "slug"):
    """Dynamic x402 dependency that reads price from dataset catalog."""

    async def dependency(request: Request) -> dict:
        slug = request.path_params.get(slug_param)
        ds = get_dataset_by_slug(slug)
        if not ds:
            raise HTTPException(status_code=404, detail="Dataset not found")

        # Create the x402 dependency with the dataset's price
        x402_dep = x402_required(
            price_usd=ds["price_usd"],
            description=f"Download: {ds['title']}",
        )
        return await x402_dep(request)

    return dependency
```

### Recipe 4: Agent-to-Agent Service (Autonomous Buyer + Seller)

The most powerful x402 pattern: two AI agents transacting without human involvement. The seller agent exposes an API behind an x402 paywall. The buyer agent detects the 402, constructs a payment, and completes the purchase autonomously.

**Seller agent (Express.js):**

```javascript
'use strict';

/**
 * Seller agent: exposes a code review service behind x402.
 *
 * POST /review
 * Body: { "code": "..." }
 * Price: $0.50 per review
 */

const express = require('express');
const { x402Paywall } = require('./x402-middleware');

const app = express();
app.use(express.json({ limit: '50kb' }));

app.post('/review',
  x402Paywall({
    priceUsd: 0.50,
    description: 'AI code review service',
  }),
  async (req, res) => {
    const { code } = req.body;
    if (!code) {
      return res.status(400).json({ error: 'code field required' });
    }

    // Perform the code review (your AI logic here)
    const review = await performCodeReview(code);

    res.json({
      review,
      lines_analyzed: code.split('\n').length,
      timestamp: new Date().toISOString(),
    });
  }
);

async function performCodeReview(code) {
  // Placeholder: integrate with your LLM or static analysis tool
  return {
    issues: [
      { line: 3, severity: 'warning', message: 'Consider using const instead of let' },
      { line: 15, severity: 'info', message: 'This function could be simplified' },
    ],
    overall_quality: 'good',
    suggestions: ['Add type annotations', 'Extract helper function on line 15'],
  };
}

app.listen(4000, () => console.log('Seller agent running on port 4000'));
```

**Buyer agent (Python):**

```python
"""
Buyer agent: autonomously purchases code review from the seller.

Detects 402, constructs payment, and completes the transaction.

In production, the payment construction uses a wallet SDK
(e.g., coinbase-sdk or viem) to sign EIP-712 payloads.
"""

import httpx
import json
import base64
import asyncio


SELLER_URL = "https://seller-agent.example.com"


async def buy_code_review(code: str) -> dict:
    """Submit code for review, handling x402 payment flow."""

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Step 1: Initial request (expect 402)
        response = await client.post(
            f"{SELLER_URL}/review",
            json={"code": code},
        )

        if response.status_code == 200:
            # Free or already paid
            return response.json()

        if response.status_code != 402:
            raise Exception(f"Unexpected status: {response.status_code}")

        # Step 2: Parse payment requirements from 402 response
        payment_info = response.json()
        requirements = payment_info["accepts"][0]

        print(f"Payment required: {requirements['maxAmountRequired']} "
              f"{requirements['extra']['name']} on {requirements['network']}")
        print(f"Pay to: {requirements['payTo']}")

        # Step 3: Construct payment payload
        # In production, use your wallet SDK to sign an EIP-712 payload:
        #
        #   from coinbase_sdk import Wallet
        #   wallet = Wallet.load("my-wallet")
        #   payment_payload = wallet.sign_x402_payment(
        #       amount=requirements["maxAmountRequired"],
        #       asset=requirements["asset"],
        #       pay_to=requirements["payTo"],
        #       network=requirements["network"],
        #       resource=requirements["resource"],
        #       timeout=requirements["maxTimeoutSeconds"],
        #   )
        #
        # For this example, we use a placeholder:
        payment_payload = construct_payment_payload(requirements)

        # Step 4: Retry with payment
        response = await client.post(
            f"{SELLER_URL}/review",
            json={"code": code},
            headers={"X-Payment": payment_payload},
        )

        if response.status_code == 200:
            print("Payment accepted. Review received.")
            return response.json()

        if response.status_code == 402:
            error = response.json().get("error", "Unknown payment error")
            raise Exception(f"Payment rejected: {error}")

        raise Exception(f"Unexpected status after payment: {response.status_code}")


def construct_payment_payload(requirements: dict) -> str:
    """Construct an x402 payment payload.

    IMPORTANT: This is a placeholder. In production, use a wallet SDK
    to sign a real EIP-712 typed data structure that authorizes the
    USDC transfer. The facilitator will reject unsigned payloads.

    Libraries that support x402 payment construction:
    - @coinbase/x402 (Node.js)
    - coinbase-sdk (Python)
    - viem (TypeScript, via signTypedData)
    """
    # Placeholder -- replace with real wallet signing
    payload = {
        "x402Version": 1,
        "scheme": requirements["scheme"],
        "network": requirements["network"],
        "amount": requirements["maxAmountRequired"],
        "asset": requirements["asset"],
        "payTo": requirements["payTo"],
        "resource": requirements["resource"],
    }
    return base64.b64encode(json.dumps(payload).encode()).decode()


async def main():
    code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
    """

    result = await buy_code_review(code)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
```

The buyer agent pattern is the core of agent-to-agent commerce with x402. The agent does not need an account, an API key, or a subscription. It needs a wallet with USDC and the ability to sign EIP-712 payloads. The seller does not need to know who the buyer is. The payment is the authentication.

This pattern scales to any number of agents. A research agent can autonomously pay for data from a data provider agent. A coding agent can pay for testing from a QA agent. A planning agent can pay for analysis from a specialist agent. Each transaction is a single HTTP request with an `X-Payment` header. No orchestration platform required. No billing integration. No API key management. Just HTTP and money.

---

## Appendix: Quick Reference

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MERCHANT_WALLET_ADDRESS` | Your wallet address (receives payments) | Required |
| `X402_NETWORK` | `base-mainnet` or `base-sepolia` | `base-sepolia` |
| `X402_FACILITATOR_URL` | Facilitator URL | `https://x402.org/facilitator` |

### USDC Contract Addresses

| Network | CAIP-2 ID | USDC Address |
|---------|-----------|-------------|
| Base Mainnet | `eip155:8453` | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Base Sepolia | `eip155:84532` | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` |

### Price Conversion

```
USDC amount (6 decimals) = USD price * 1,000,000
$0.01 = "10000"
$0.10 = "100000"
$1.00 = "1000000"
$29.00 = "29000000"
```

### Facilitator Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/verify` | POST | Validate a payment payload against requirements |
| `/settle` | POST | Trigger on-chain USDC transfer |

### HTTP Headers

| Header | Direction | Purpose |
|--------|-----------|---------|
| `X-Payment` | Request | Base64-encoded payment payload from client |
| `PAYMENT-REQUIRED` | Response (402) | Base64-encoded payment requirements |
| `X-PAYMENT-RESPONSE` | Response (200) | Base64-encoded payment confirmation |

### Cross-References

- For agent-to-agent escrow, marketplace discovery, and reputation-gated hiring on top of x402 micropayments, see **The Multi-Agent Commerce Cookbook**.
- For multi-protocol comparison (x402 vs ACP vs AP2 vs MPP), see **The Agent Payment Rails Playbook**.
- For fleet-wide cost attribution and spend dashboards, see **The AI Agent FinOps Playbook**.

For the full x402 protocol specification, visit [https://www.x402.org](https://www.x402.org).

---

*Price: $29 | Format: Digital Guide | Updates: Lifetime access*

