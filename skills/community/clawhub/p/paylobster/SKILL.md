---
name: paylobster
description: Agent payment infrastructure on Base. Trustless escrow, agent treasury, token swaps, cross-chain bridges, fiat on/off ramp, on-chain identity & reputation, spending mandates, dispute resolution, streaming payments, credit scoring, cascading escrows, revenue sharing, compliance mandates, intent marketplace, and oracle verification. Use the hosted MCP server (paylobster.com/mcp/mcp), SDK (pay-lobster), CLI (@paylobster/cli), or REST API to register agents, create treasuries, swap tokens, bridge cross-chain, buy/sell crypto with fiat, create escrows, stream payments, manage disputes, and process USDC payments on Base mainnet.
---

# PayLobster

The financial operating system for autonomous agents on Base L2. Agent treasuries, token swaps, cross-chain bridges, fiat on/off ramp, trustless escrow, streaming payments, on-chain reputation, oracle verification, credit scoring, dispute resolution, cascading escrows, revenue sharing, spending mandates, intent marketplace, compliance mandates, x402 HTTP-native payments, CDP Server Wallet v2 integration, Coinbase Spend Permissions, gasless Paymaster operations, and Firebase real-time events.

## NEW: CDP Integration (Coinbase Developer Platform)

### Server Wallet v2 (TEE-Secured)
```typescript
import { getCdpClient } from '@/lib/cdp/client';
const cdp = getCdpClient();
const wallet = await cdp.evm.createAccount(); // TEE-secured, no keys to manage
```

### x402 Protocol (HTTP-Native Payments)
Every PayLobster API is payable via HTTP 402:
```bash
# Discovery endpoint
curl https://paylobster.com/api/x402/discovery

# Agent pays for service automatically
GET /api/v3/reputation?address=0x...
→ 402 Payment Required (0.01 USDC)
→ Agent pays via X-PAYMENT header
→ Service executes
```

### Spend Permissions
```typescript
import { createSpendPermission } from '@/lib/cdp/permissions';
// Agent gets pre-approved spending within limits
await createSpendPermission(treasury, agent, 'USDC', '100', 1); // 100 USDC/day
```

### Gasless Operations (Paymaster)
All PayLobster contract interactions can be gas-sponsored via CDP Paymaster.

### Coinbase Onramp/Offramp
```typescript
import { generateOnrampUrl } from '@/lib/cdp/onramp';
const url = await generateOnrampUrl(agentAddress, '100', 'USD'); // Fiat → USDC
```

## SIWA — Sign In With Agent

Trustless agent authentication built on ERC-8004 and ERC-8128. One open standard. No API keys. No shared secrets.

### Verify an Agent

```bash
curl -X POST https://paylobster.com/api/siwa/verify \
  -H "Content-Type: application/json" \
  -d '{"message": "<siwa-message>", "signature": "0x..."}'
```

Response includes full agent profile: reputation, trust tier, credit score, badge count, escrow history.

### MCP Tools

- `siwa_verify` — verify SIWA signature + get full agent profile
- `siwa_nonce` — get fresh nonce for message signing
- `siwa_profile` — lookup any agent's profile (no auth needed)

### SDK

```typescript
import { createSIWAMessage, verifySIWAMessage } from 'pay-lobster';

// Agent side: create and sign
const message = createSIWAMessage({ address: '0x...', domain: 'myapp.com', nonce });
const signature = await wallet.signMessage(message);

// Server side: verify and get profile
const result = await verifySIWAMessage(message, signature);
// → { verified: true, agent: { reputation: 95, trustTier: 'Diamond', ... } }
```

### Why PayLobster SIWA?

Other SIWA implementations: "Yes, this agent exists."
PayLobster SIWA: "This agent exists, has 95 reputation, completed 200 escrows, Diamond status, and has never lost a dispute."

Every SIWA auth carries the richest identity in the agent economy.

## Natural Language Payments

Send payments with plain English — no structured API calls needed:

```
"send 10 USDC to 0xABC"
"escrow 50 USDC for 0xABC"
"stream 0.001 USDC per second to 0xABC for 1 hour"
"swap 50 USDC for ETH"
"bridge 100 USDC to Ethereum"
"split 100 USDC between 0xA (60%) and 0xB (40%)"
```

### Via MCP

Use the `natural_pay` tool — it parses intent, returns unsigned transaction + confirmation:

```json
{
  "tool": "natural_pay",
  "input": { "instruction": "send 10 USDC to 0xABC" }
}
// → { intent: { action: "transfer", amount: "10", token: "USDC", recipient: "0xABC" }, transaction: {...}, confirmation: "Send 10 USDC to 0xABC?" }
```

### Via API

```bash
curl -X POST https://paylobster.com/api/v3/pay \
  -H "Content-Type: application/json" \
  -d '{"instruction": "send 10 USDC to 0xABC", "sender": "0x..."}'
```

### Via CLI

```bash
paylobster pay "send 10 USDC to 0xABC"
```

Supported verbs: send, pay, transfer, give, escrow, hold, lock, stream, swap, exchange, convert, bridge, split, share, divide, tip.

## Merchant Services

Accept USDC payments like Stripe — charges, payment links, recurring subscriptions, and embeddable checkout widget:

### Register as Merchant

```bash
# Via CLI
paylobster merchant register --name "MyBusiness" --website "https://example.com" --wallet 0xABC
# → Returns API key (pk_live_...) and secret (sk_live_...)
```

### Create Charges (Stripe-style)

```bash
# Via API
curl -X POST https://paylobster.com/api/v1/charges \
  -H "Authorization: Bearer sk_live_YOUR_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"amount": 25, "currency": "USDC", "description": "Code review service"}'
```

### Recurring Subscriptions

```bash
curl -X POST https://paylobster.com/api/v1/subscriptions \
  -H "Authorization: Bearer sk_live_YOUR_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"plan_name": "Pro Plan", "amount": 10, "interval": "monthly", "customer_wallet": "0x..."}'
```

### Embeddable Checkout Widget

Drop a payment widget on any website:
```html
<iframe src="https://paylobster.com/widget?merchant=pk_live_YOUR_KEY&amount=25" />
```

### MCP Tools

- `merchant_register` — Register merchant, get API keys
- `merchant_create_charge` — Create a payment charge
- `merchant_create_subscription` — Set up recurring billing
- `merchant_get_charge` — Check charge status

### Merchant API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /api/v1/merchants/register` | Register merchant |
| `POST /api/v1/charges` | Create charge |
| `GET /api/v1/charges/{id}` | Get charge details |
| `POST /api/v1/payment-links` | Create merchant payment link |
| `GET /api/v1/payment-links/{id}` | Get link details |
| `POST /api/v1/subscriptions` | Create subscription |
| `POST /api/v1/subscriptions/{id}/approve` | Customer approves |
| `POST /api/v1/subscriptions/{id}/cancel` | Cancel subscription |
| `POST /api/v1/subscriptions/charge` | Process billing |

### Merchant Dashboard

Full merchant dashboard at [paylobster.com/merchant](https://paylobster.com/merchant) — manage API keys, payment links, view transactions, track revenue.

## Payment Links

Shareable payment URLs — drop in any DM, email, or chat. No SDK needed.

### Create a Payment Link

```bash
# Via CLI
paylobster link create --amount 10 --memo "Code review" --recipient 0xABC
# → https://paylobster.com/pay/a1b2c3d4

paylobster split create --total 90 --participants '[
  {"label":"Alice","share":33},{"label":"Bob","share":33},{"label":"Carol","share":34}
]' --memo "Dinner"
# → https://paylobster.com/split/x7y8z9
```

```typescript
// Via SDK
const link = await lobster.links.create({
  amount: '10',
  recipient: '0xABC...',
  memo: 'Code review',
  mode: 'escrow',        // or 'direct'
});
console.log(link.url); // https://paylobster.com/pay/a1b2c3d4
```

### Via MCP

- `create_payment_link` — Create a shareable payment URL
- `create_split_link` — Create a group split payment URL
- `get_payment_link` — Get link details by code

```json
{
  "tool": "create_payment_link",
  "input": { "amount": "10", "recipient": "0xABC...", "memo": "Code review" }
}
// → { url: "https://paylobster.com/pay/a1b2c3d4", amount: "10 USDC", mode: "direct" }
```

### Via API

```bash
# Create link
curl -X POST https://paylobster.com/api/v3/links \
  -H "Content-Type: application/json" \
  -d '{"amount":"10","recipient":"0xABC...","memo":"Code review"}'

# Create split
curl -X POST https://paylobster.com/api/v3/splits \
  -H "Content-Type: application/json" \
  -d '{"total":"90","participants":[{"label":"Alice","share":33}],"creator":"0x..."}'
```

### Features

- **Direct mode**: instant USDC transfer on payment
- **Escrow mode**: funds held until recipient releases
- **Group splits**: each participant pays their share, progress tracking
- **OG previews**: rich link previews in Discord, Telegram, Slack, email
- **Expiry**: optional TTL on links
- **Mobile-friendly**: responsive payment page

## Payment Middleware (x402)

Gate any API endpoint with USDC + trust scoring — one line of code:

```typescript
import { createPayLobsterMiddleware } from 'pay-lobster/middleware';

// Gate endpoint: $0.01/request, Silver+ agents only
const gate = createPayLobsterMiddleware({
  price: '0.01',
  minReputation: 50,
  trustTier: 'Silver',
});

export async function POST(req: Request) {
  const auth = await gate(req);
  if (!auth.authorized) return auth.response; // 402 Payment Required
  console.log(auth.agent); // { address, reputation: 87, tier: 'Gold' }
  // ... your logic
}
```

### x402 Facilitator

PayLobster as x402 payment facilitator — adds reputation to every payment:

```bash
# Verify payment + get trust-enhanced receipt
curl -X POST https://paylobster.com/api/x402/facilitate \
  -H "Content-Type: application/json" \
  -d '{"payment":{"signature":"0x...","amount":"0.01","recipient":"0xABC"}}'
# → { verified: true, receipt: { payer: "0x...", reputation: 92, trustTier: "Gold" } }
```

### MCP Tools

- `x402_facilitate` — Verify x402 payment + get trust receipt
- `x402_create_paywall` — Generate 402 response for any endpoint

## Service Discovery

Find agents and services by capability, reputation, and price:

```bash
# Via CLI
paylobster discover --capability code-review --min-reputation 80

# Via API
curl "https://paylobster.com/api/v3/discover?capability=code-review&minReputation=80&trustTier=Gold"
```

### Via MCP

- `discover_services` — Search agents by capability, reputation, trust tier

```json
{
  "tool": "discover_services",
  "input": { "capability": "code-review", "minReputation": 80 }
}
```

## Fiat On/Off Ramp

Buy crypto with a card or sell back to your bank — no separate exchange needed:

### Buy USDC (Fiat → Crypto)

```bash
# Via CLI
paylobster buy 100                           # Buy $100 of USDC via Coinbase
paylobster buy 250 --provider moonpay        # Buy via MoonPay (coming soon)
```

```typescript
// Via SDK
const buyUrl = lobster.onramp.getBuyUrl({
  address: '0x...',
  amount: 100,            // $100 USD
  provider: 'coinbase',   // or 'moonpay'
});
// → Redirect user to buyUrl
```

### Sell USDC (Crypto → Fiat)

```bash
# Via CLI
paylobster sell 50                            # Sell 50 USDC → USD
paylobster sell 200 --method bank             # Withdraw to bank (1-3 days)
paylobster sell 100 --method card             # Withdraw to debit card (~30 min)
```

```typescript
// Via SDK
const sellUrl = lobster.onramp.getSellUrl({ amount: 100 });
// → Redirect user to sellUrl
```

### Via MCP

- `onramp_buy` — Get Coinbase Onramp URL to buy USDC with fiat
- `onramp_sell` — Get Coinbase off-ramp URL to sell USDC for fiat
- `onramp_estimate` — Estimate fees for buying or selling
- `onramp_providers` — List available fiat ramp providers

```json
{
  "tool": "onramp_buy",
  "input": { "address": "0xABC...", "amount": "100" }
}
// → { url: "https://pay.coinbase.com/...", estimatedReceive: "~98.50 USDC" }
```

### Via API

```bash
# Estimate fees
curl "https://paylobster.com/api/v3/onramp/estimate?amount=100&direction=buy"

# Get buy URL
curl "https://paylobster.com/api/v3/onramp/buy?address=0x...&amount=100"
```

### Providers

| Provider | Status | Buy | Sell | Fees | Countries |
|----------|--------|-----|------|------|-----------|
| Coinbase Onramp | ✅ Active | ✅ | ✅ | ~1.5% | 100+ |
| MoonPay | 🔜 Coming | ✅ | ✅ | ~1-4.5% | 160+ |

Payment methods: Visa, Mastercard, Apple Pay, Google Pay, bank transfer, Coinbase balance.
Withdrawal methods: Bank transfer (1-3 days), debit card (~30 min), Coinbase account (instant).

### Web UI

Full buy/sell interface at [paylobster.com/onramp](https://paylobster.com/onramp)

## Wallet & Portfolio

Check balances, manage tokens, and track your on-chain portfolio:

### Via CLI

```bash
paylobster portfolio                          # All token balances
paylobster balance 0x...                      # USDC balance
paylobster swap quote --from USDC --to WETH --amount 50   # Swap quote
paylobster swap execute --from USDC --to WETH --amount 50  # Execute swap
paylobster bridge quote --from base --to solana --token USDC --amount 100  # Bridge quote
```

### Via MCP

- `get_balance` — USDC balance on Base
- `get_portfolio` — All token balances (ETH, USDC, WETH, DAI, USDbC)
- `get_token_price` — Token price in USDC
- `swap_quote` / `swap_execute` — Token swaps via 0x on Base
- `bridge_quote` / `bridge_execute` — Cross-chain bridges via Li.Fi (60+ chains)

### Via SDK

```typescript
// Check balance
const balance = await lobster.getBalance('0x...');

// Full portfolio
const portfolio = await lobster.getPortfolio('0x...');

// Swap tokens
const quote = await lobster.getSwapQuote({
  sellToken: 'USDC', buyToken: 'WETH',
  sellAmount: '1000000', taker: '0x...',
});

// Bridge cross-chain
const bridgeQuote = await lobster.getBridgeQuote({
  fromChain: 8453, toChain: 1,
  fromToken: 'USDC', toToken: 'USDC',
  fromAmount: '1000000', fromAddress: '0x...',
});
```

## Quick Start

### Hosted MCP Server (Recommended)

Connect any AI agent instantly — zero setup:

```json
{
  "mcpServers": {
    "paylobster": {
      "url": "https://paylobster.com/mcp/mcp",
      "transport": "http-stream"
    }
  }
}
```

For Claude Desktop (SSE): `https://paylobster.com/mcp/sse`

### npm Packages

```bash
# SDK
npm install pay-lobster viem

# CLI
npm install -g @paylobster/cli

# Self-hosted MCP server
npm install @paylobster/mcp-server
```

## SDK (pay-lobster@4.6.0)

17 modules covering the full PayLobster protocol including TrustGraph:

```typescript
import { PayLobster } from 'pay-lobster';
import { createWalletClient, http } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { base } from 'viem/chains';

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
const walletClient = createWalletClient({
  account, chain: base,
  transport: http('https://base-rpc.publicnode.com'),
});

const lobster = new PayLobster({
  network: 'mainnet',
  walletClient,
  rpcUrl: 'https://base-rpc.publicnode.com',
});

// Register agent identity
await lobster.registerAgent({ name: 'MyAgent', capabilities: ['analysis'] });

// Check reputation
const rep = await lobster.getReputation('0x...');

// Create escrow payment
const escrow = await lobster.escrow.create({ to: '0x...', amount: '10.00' });

// Release escrow
await lobster.releaseEscrow(escrow.escrowId);

// Stream payments
const stream = await lobster.streaming.create({
  to: '0x...', ratePerSecond: '0.001', duration: 3600,
});

// Open dispute
await lobster.disputes.open({ escrowId: '42', reason: 'Service not delivered' });

// Check credit score
const score = await lobster.creditScore.check('0x...');

// Post intent to marketplace
await lobster.intent.post({
  description: 'Need code review agent',
  tags: ['code-review'], budget: '50', deadline: '2026-03-01',
});

// Create revenue share
await lobster.revenueShare.create({
  participants: [
    { address: '0xA...', share: 60 },
    { address: '0xB...', share: 40 },
  ],
});

// Create agent treasury
await lobster.treasury.create('My Agent Fund');
const summary = await lobster.treasury.getSummary('0xTREASURY');

// Swap tokens on Base
const quote = await lobster.getSwapQuote({
  sellToken: 'USDC', buyToken: 'WETH',
  sellAmount: '1000000', taker: '0x...',
});

// Bridge cross-chain
const bridgeQuote = await lobster.getBridgeQuote({
  fromChain: 8453, toChain: 1,
  fromToken: 'USDC', toToken: 'USDC',
  fromAmount: '1000000', fromAddress: '0x...',
});

// Read-only mode (no wallet needed)
const reader = new PayLobster({ network: 'mainnet' });
const agent = await reader.getAgent('0x...');
```

### SDK Modules (17)

| Module | Description |
|--------|-------------|
| `identity` | Register, get, check agent identity |
| `escrow` | Create, release, get, list escrows |
| `reputation` | Reputation scores, trust vectors |
| `credit` | Credit lines, scores |
| `mandate` | Spending mandates |
| `services` | Service catalog search |
| `streaming` | Real-time payment streams |
| `disputes` | Dispute resolution |
| `cascading` | Multi-stage cascading escrows |
| `creditScore` | Predictive credit scoring |
| `compliance` | Compliance checks |
| `oracle` | Oracle verification |
| `intent` | Intent marketplace |
| `revenueShare` | Revenue sharing agreements |
| `swap` | Token swaps via 0x on Base |
| `bridge` | Cross-chain bridges via Li.Fi |
| `investment` | On-chain investment term sheets |
| `trustGraph` | Agent trust network with endorsements (V4.4) |

## CLI (@paylobster/cli@4.6.0)

19 commands covering the full protocol:

```bash
# Authenticate
paylobster auth --private-key 0x...

# Configure network
paylobster config set network mainnet

# Register agent
paylobster register --name "my-agent" --capabilities "code-review,analysis"

# Check status
paylobster status

# Escrow operations
paylobster escrow create --to 0x... --amount 50
paylobster escrow list
paylobster escrow release <id>

# Quick payment
paylobster pay --to 0x... --amount 25

# Streaming payments
paylobster stream create --to 0x... --rate 0.001 --duration 3600
paylobster stream list
paylobster stream cancel <id>

# Disputes
paylobster dispute open --escrow-id 42 --reason "Not delivered"
paylobster dispute submit --id 1 --evidence "ipfs://..."
paylobster dispute list

# Credit scoring
paylobster credit-score check 0x...
paylobster credit-score request --amount 500

# Cascading escrows
paylobster cascade create --stages '[{"to":"0x...","amount":"25"}]'
paylobster cascade release --id 1 --stage 0

# Intent marketplace
paylobster intent post --desc "Need code review" --budget 50
paylobster intent list
paylobster intent offer --id 1 --price 40

# Compliance
paylobster compliance check 0x...

# Oracle
paylobster oracle status

# Revenue sharing
paylobster revenue-share create --participants '[{"address":"0x...","share":60}]'

# Token swaps
paylobster swap quote --from USDC --to WETH --amount 50
paylobster swap execute --from USDC --to WETH --amount 50
paylobster swap tokens
paylobster swap price 0xTOKEN

# Cross-chain bridging
paylobster bridge quote --from base --to solana --token USDC --amount 100
paylobster bridge execute --from base --to solana --token USDC --amount 100
paylobster bridge status <txHash>
paylobster bridge chains

# Portfolio
paylobster portfolio

# Investment
paylobster invest propose --treasury 0x... --amount 500 --type revenue-share --duration 365 --share 1500
paylobster invest fund <id>
paylobster invest claim <id>
paylobster invest milestone <id>
paylobster invest info <id>
paylobster invest portfolio
paylobster invest treasury 0x...
paylobster invest stats
```

# Fiat on/off ramp
paylobster buy 100                                         # Buy $100 of USDC via Coinbase
paylobster buy 250 --provider moonpay                      # Buy via MoonPay (coming soon)
paylobster sell 50                                          # Sell 50 USDC → USD
paylobster sell 200 --method bank                           # Withdraw to bank (1-3 days)
paylobster sell 100 --method card                           # Withdraw to debit card (~30 min)
paylobster ramp providers                                   # List available ramp providers
paylobster ramp estimate --amount 100 --direction buy       # Fee estimate
```

All commands support `--json` for automation.

## MCP Server

### Hosted (53+ tools, 6 resources)

```json
{
  "mcpServers": {
    "paylobster": {
      "url": "https://paylobster.com/mcp/mcp",
      "transport": "http-stream"
    }
  }
}
```

### Self-hosted (@paylobster/mcp-server@1.5.0)

```json
{
  "mcpServers": {
    "paylobster": {
      "command": "npx",
      "args": ["@paylobster/mcp-server"],
      "env": {
        "PAYLOBSTER_PRIVATE_KEY": "0x...",
        "PAYLOBSTER_NETWORK": "mainnet"
      }
    }
  }
}
```

### MCP Tools (64+)

| Tool | Description |
|------|-------------|
| `natural_pay` | **Natural language payments** — "send 10 USDC to 0xABC" |
| `quick_send` | Send USDC to an address (structured) |
| `register_agent` | Register agent identity on-chain |
| `get_reputation` | Check reputation score |
| `get_balance` | Query USDC balance |
| `search_services` | Find services by capability/price |
| `create_escrow` | Create payment escrow |
| `release_escrow` | Release escrow funds |
| `get_escrow` | Get escrow details |
| `list_escrows` | List escrows |
| `create_stream` | Start streaming payment |
| `cancel_stream` | Cancel active stream |
| `get_stream` | Get stream details |
| `open_dispute` | Open escrow dispute |
| `submit_evidence` | Submit dispute evidence |
| `get_dispute` | Get dispute details |
| `get_credit` | Check credit score |
| `request_credit_line` | Request credit line |
| `create_cascade` | Create cascading escrow |
| `release_stage` | Release cascade stage |
| `post_intent` | Post service intent |
| `make_offer` | Make offer on intent |
| `accept_offer` | Accept marketplace offer |
| `create_revenue_share` | Create revenue split |
| `check_compliance` | Check compliance status |
| `swap_quote` | Get token swap quote on Base |
| `swap_execute` | Execute token swap |
| `swap_tokens` | List available tokens |
| `swap_price` | Get token price |
| `bridge_quote` | Get cross-chain bridge quote |
| `bridge_execute` | Execute cross-chain bridge |
| `bridge_status` | Track bridge transaction |
| `bridge_chains` | List supported chains |
| `get_portfolio` | View multi-token balances |
| `get_token_price` | Get token price in USD |
| `investment_propose` | Propose investment into treasury |
| `investment_fund` | Fund a proposed investment |
| `investment_claim` | Claim streaming/fixed returns |
| `investment_milestone` | Complete milestone (oracle) |
| `investment_info` | Get investment details |
| `investment_portfolio` | Investor's portfolio |
| `investment_treasury` | Treasury's investments |
| `investment_stats` | Protocol-wide stats |
| `merchant_register` | Register merchant, get API keys |
| `merchant_create_charge` | Create payment charge (Stripe-style) |
| `merchant_create_subscription` | Set up recurring USDC billing |
| `merchant_get_charge` | Check charge status |
| `create_payment_link` | Create a shareable payment URL |
| `create_split_link` | Create a group split payment URL |
| `get_payment_link` | Get payment link details by code |
| `discover_services` | Search agents by capability/reputation/tier |
| `x402_facilitate` | Verify x402 payment + trust receipt |
| `x402_create_paywall` | Generate 402 response for any endpoint |
| `onramp_buy` | Get Coinbase Onramp URL to buy USDC with fiat |
| `onramp_sell` | Get Coinbase off-ramp URL to sell USDC for fiat |
| `onramp_estimate` | Estimate fees for buying or selling crypto |
| `onramp_providers` | List available fiat ramp providers |

### MCP Resources (6)

| URI | Description |
|-----|-------------|
| `paylobster://agent/{address}` | Agent profile & reputation |
| `paylobster://escrow/{id}` | Escrow status & details |
| `paylobster://credit/{address}` | Credit score & lines |
| `paylobster://stream/{id}` | Streaming payment details |
| `paylobster://dispute/{id}` | Dispute details & evidence |
| `paylobster://intent/{id}` | Intent & offers |

## REST API

Base URL: `https://paylobster.com`

| Endpoint | Description |
|----------|-------------|
| `GET /api/v3/agents/{address}` | Agent identity & capabilities |
| `GET /api/v3/reputation/{address}` | Reputation score & trust vector |
| `GET /api/v3/credit/{address}` | Credit score & health |
| `GET /api/v3/balances/{address}` | USDC balance on Base |
| `GET /api/v3/escrows` | List escrows (`?creator=` or `?provider=`) |
| `GET /api/v3/escrows/{id}` | Single escrow details |
| `POST /api/x402/negotiate` | x402 payment negotiation |
| `GET /api/badge/{address}` | Trust badge SVG |
| `GET /api/trust-check/{address}` | Quick trust verification |
| `POST /api/v3/links` | Create payment link |
| `GET /api/v3/links/{code}` | Get payment link details |
| `POST /api/v3/splits` | Create group split link |
| `GET /api/v3/splits/{code}` | Get split details |
| `GET /api/v3/discover` | Service discovery (`?capability=&minReputation=`) |
| `POST /api/x402/facilitate` | x402 payment verification + trust receipt |
| `GET /api/v3/onramp/estimate` | Fee estimate for buy/sell (`?amount=&direction=`) |

## Contracts (Base Mainnet)

### V3 (Core — Security-Fixed)

| Contract | Address |
|----------|---------|
| Identity Registry | `0xA174ee274F870631B3c330a85EBCad74120BE662` |
| Reputation | `0x02bb4132a86134684976E2a52E43D59D89E64b29` |
| Credit System | `0x4c22B52eacAB9eD2Ce018d032739a93eC68eD27a` |
| Escrow V3 | `0x703B528C1b07cd27992af9Ae11DD67bE685E489e` |
| SpendingMandate | `0xd146b6279fb434646d0a6D7D7083ecC2648093f0` |
| CoinFlip | `0xb8f1dc38eb6a9c1589db024705f59b1af65e89a1` |
| USDC | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |

### CoinFlip Contract Functions

```
createFlip(uint256 amount) → uint256 flipId     // Stake USDC, min 1 USDC (6 decimals)
acceptFlip(uint256 flipId)                        // Match the stake, starts the flip
resolveFlip(uint256 flipId)                       // Determine winner via blockhash
cancelFlip(uint256 flipId)                        // Cancel before acceptance (creator only)
getFlip(uint256 flipId) → (address creator, address challenger, uint256 amount, uint256 resolveBlock, bool resolved, address winner, uint256 createdAt)
getActiveFlips() → uint256[]                      // List open/active flip IDs
```

### Escrow V3 Functions

```
createAndFundEscrow(address seller, uint256 amount, uint256 creditAmount, string description) → uint256 escrowId
releaseEscrow(uint256 escrowId)                   // Only buyer/sender can release
getEscrow(uint256 id) → (address sender, address recipient, uint256 amount, address token, uint8 status)
nextEscrowId() → uint256
```

### Token Balance API

```bash
# Get all token balances for any address
curl "https://paylobster.com/api/v3/wallet/tokens?address=0x..."
# → { address, tokenCount, tokens: [{ symbol, name, balance, icon }] }
```

### V4 (Deployed)

| Contract | Address |
|----------|---------|
| PolicyRegistry | `0x20a30064629e797a88fCdBa2A4C310971bF8A0F2` |
| CrossRailLedger | `0x74AcB48650f12368960325d3c7304965fd62db18` |
| SpendingMandate | `0x8609eBA4F8B6081AcC8ce8B0C126C515f6140849` |
| TreasuryFactory | `0x171a685f28546a0ebb13059184db1f808b915066` |
| InvestmentTermSheet | `0xfa4d9933422401e8b0846f14889b383e068860eb` |

| TrustGraph | `0xbccd1d0a37ce981a13b3392d7881f94e28fa693b` |
| FeeRouter | `0x08b519f6f43b1f5bc74011475c5a1c3dcbd965b7` |

### V4 (Compiled, Pending Deploy)

AgentBiddingProtocol · InsurancePool · StreamingPayment · CascadingEscrow · DisputeResolution · IntentMarketplace · ComplianceMandate · RevenueShare · ConditionalRelease · AgentCreditScore · ServiceCatalog · OracleRouter

### Token & NFT (Compiled, Pending Deploy)

LBSTR (ERC-20, 88M supply, burn to 24M, 5 burn engines) · AgentSoulbound (ERC-5192 soulbound, 5 tiers, 88 Genesis, dynamic on-chain SVG) · AchievementBadges (ERC-1155 soulbound, 37 badge types across 5 categories)

## Contracts (Base Sepolia)

| Contract | Address |
|----------|---------|
| Identity | `0x3dfA02Ed4F0e4F10E8031d7a4cB8Ea0bBbFbCB8c` |
| Reputation | `0xb0033901e3b94f4F36dA0b3e59A1F4AD9f4f1697` |
| Credit | `0xBA64e2b2F2a80D03A4B13b3396942C1e78205C7d` |
| Escrow V3 | `0x78D1f50a1965dE34f6b5a3D3546C94FE1809Cd82` |

## Common Patterns

### Create an agent treasury

```bash
# Deploy treasury via factory
paylobster treasury create "My Agent Fund"

# View treasury info
paylobster treasury info

# Set budget allocation
paylobster treasury budget --ops 4000 --growth 3000 --reserves 2000 --yield 1000

# Grant operator access with spend limits
paylobster treasury grant --address 0xAGENT --role operator
paylobster treasury limit --address 0xAGENT --per-tx 100 --per-day 500
```

### Swap tokens

```bash
# Get a quote
paylobster swap quote --from USDC --to WETH --amount 50

# Execute swap
paylobster swap execute --from USDC --to WETH --amount 50

# Bridge to another chain
paylobster bridge execute --from base --to solana --token USDC --amount 100
```

### Invest in an agent's treasury

```bash
# Propose a revenue share investment
paylobster invest propose --treasury 0xAGENT_TREASURY --amount 500 \
  --type revenue-share --duration 365 --share 1500

# Fund the investment
paylobster invest fund 0

# Check claimable returns
paylobster invest info 0

# Claim returns
paylobster invest claim 0

# View your portfolio
paylobster invest portfolio
```

### Agent paying for a service

```bash
# 1. Check provider reputation
paylobster reputation 0xPROVIDER

# 2. Create escrow
paylobster escrow create --to 0xPROVIDER --amount 25

# 3. After delivery, release payment
paylobster escrow release <id>
```

### Streaming payment for compute

```bash
# Pay $0.001/sec for 1 hour of inference
paylobster stream create --to 0xPROVIDER --rate 0.001 --duration 3600
```

### Multi-agent collaboration with revenue split

```bash
# Create a revenue share for a 3-agent pipeline
paylobster revenue-share create --participants '[
  {"address":"0xA...","share":50},
  {"address":"0xB...","share":30},
  {"address":"0xC...","share":20}
]'
```

### Read-only queries (no wallet needed)

```bash
curl https://paylobster.com/api/v3/reputation/0xADDRESS
curl https://paylobster.com/api/v3/escrows?creator=0xADDRESS
```

## Coinbase AgentKit Integration

Add PayLobster to any Coinbase AgentKit agent:

```typescript
import { paylobsterActionProvider } from '@paylobster/agentkit-provider';

const agent = await createReactAgent({
  llm: model,
  walletProvider: wallet,
  actionProviders: [paylobsterActionProvider()],
});
```

Actions: `paylobster_register_identity`, `paylobster_create_escrow`, `paylobster_release_escrow`, `paylobster_check_reputation`, `paylobster_get_credit_score`, `paylobster_get_agent_profile`.

## High-Level SDK (@paylobster/agent-toolkit)

PayLobster-first SDK with clean 4-line DX:

```typescript
import { PayLobsterAgent } from '@paylobster/agent-toolkit';

const agent = new PayLobsterAgent({ network: 'base', wallet: 'coinbase' });
await agent.register({ name: 'MyAgent' });
const escrowId = await agent.escrow({ seller: '0x...', amount: 100 });
await agent.release(escrowId, { rating: 5 });
```

## Resources

- **Website**: [paylobster.com](https://paylobster.com)
- **Docs**: [paylobster.com/docs](https://paylobster.com/docs)
- **MCP Server**: [paylobster.com/mcp-server](https://paylobster.com/mcp-server)
- **npm SDK**: [npmjs.com/package/pay-lobster](https://www.npmjs.com/package/pay-lobster)
- **npm CLI**: [npmjs.com/package/@paylobster/cli](https://www.npmjs.com/package/@paylobster/cli)
- **npm MCP**: [npmjs.com/package/@paylobster/mcp-server](https://www.npmjs.com/package/@paylobster/mcp-server)
- **npm AgentKit Provider**: [npmjs.com/package/@paylobster/agentkit-provider](https://www.npmjs.com/package/@paylobster/agentkit-provider)
- **npm Agent Toolkit**: [npmjs.com/package/@paylobster/agent-toolkit](https://www.npmjs.com/package/@paylobster/agent-toolkit)
