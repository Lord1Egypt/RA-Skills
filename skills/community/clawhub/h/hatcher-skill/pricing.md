---
name: hatcher-skill-pricing
version: 1.0.0
description: Hatcher tiers, addons, and payment rails (credits, Stripe, SOL, USDC, HATCHER)
homepage: https://hatcher.host
api_base: https://api.hatcher.host
---

# Pricing & Payments

## Tiers

All charges are **one-time** — 30 days (monthly) or 365 days (annual, 15% off). Founding Member is **lifetime**. Renewal stacks days on current expiry. Upgrades refund unused days as HATCHER credits.

| Tier | Monthly | Agents | Msg/day | Searches/day | CPU/RAM | Storage | Auto-sleep | Plugins |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Free** | $0 | 1 | 20 | 3 | 0.5/1GB | 50 MB | 1h | 3 |
| **Starter** | $6.99 | 1 | 50 | 10 | 1/1.5GB | 150 MB | 4h | 10 |
| **Pro** | $19.99 | 3 | 100 | 50 | 1.5/2GB | 500 MB | 12h | 25 |
| **Business** | $49.99 | 10 | 300 | 200 | 2/3GB | 1 GB | Always-on | 50 |
| **Founding** | **$99 lifetime** | 10 | 300 | 200 | 2/4GB | 2 GB | Always-on | 50 |

Founding Member is capped at **20 lifetime slots total**. Check availability:
```bash
curl -sS https://api.hatcher.host/features | jq '.foundingMemberSlotsLeft'
```

## Decision tree

- One free-tier chat agent for testing? → **Free**
- One always-running agent with a single integration? → **Starter**
- 3 agents with various integrations and sustained traffic? → **Pro**
- Multiple always-on production agents with high message volume? → **Business**
- Want to support Hatcher + skip paying every month? → **Founding** (if slots remain)

## Addons

### Account-level (stack BY COUNT — each purchase adds a row; caps sum)

- **+1/3/5/10 Agents** — $2.99 / $6.99 / $11.99 / $19.99 /mo
- **+20/50/100/200 msg/day** — $1.99 / $3.99 / $5.99 / $9.99 /mo
- **+25/50 searches/day** — $3.99 / $6.99 /mo

### Per-agent (extend expiry on renewal)

- **Always On** $7.99/mo — keep agent running 24/7
- **File Manager** $4.99 one-time — permanent unlock
- **Full Logs** $2.99/mo — without it, log viewer caps at last 20 lines
- **+10 Plugins** $5.99/mo — stack extra plugin slots on one agent

All subscription addons have annual variants at 15% off. Business + Founding include File Manager + Full Logs by default.

## Payment rails — 4 options

### 1. HATCHER Credits (recommended for agents)

Simplest. User pre-funds their account with any rail below, agent consumes credits for tier/addon purchases.

```bash
# Check balance (requires auth)
curl -sS https://api.hatcher.host/api/v1/me \
  -H "Authorization: Bearer $HATCHER_KEY" | jq '.data.hatchCredits'

# Subscribe to a tier using credits (server-side settle, no wallet popup)
curl -sS -X POST https://api.hatcher.host/features/subscribe-with-credits \
  -H "Authorization: Bearer $HATCHER_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "tier": "starter", "billingPeriod": "monthly" }'
```

Response:
```json
{ "success": true, "data": { "tier": "starter", "expiresAt": "...", "creditsUsed": 6.99, "creditsRemaining": 13.01 } }
```

### 2. Stripe Card (one-time checkout)

Backend returns a hosted checkout URL. Agent opens URL in browser (or hands to human).

```bash
curl -sS -X POST https://api.hatcher.host/stripe/checkout/subscription \
  -H "Authorization: Bearer $HATCHER_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "tier": "pro", "billingPeriod": "annual" }'
```

Response: `{ "data": { "url": "https://checkout.stripe.com/..." } }`. On success, webhook activates the tier server-side — agent polls `GET /api/v1/me` until `tier === "pro"`.

### 3. SOL (native Solana)

Agent signs a transaction sending SOL to the treasury wallet returned by `/prices`. Must include `memo` with the intended purchase.

```bash
# Get SOL amount + treasury address
curl -sS "https://api.hatcher.host/prices?tier=starter&billingPeriod=monthly" | jq '.'

# After signing and submitting to Solana, notify Hatcher:
curl -sS -X POST https://api.hatcher.host/features/subscribe \
  -H "Authorization: Bearer $HATCHER_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "tier": "starter", "billingPeriod": "monthly", "paymentToken": "sol", "txSignature": "..." }'
```

Backend verifies tx on-chain before activating.

### 4. USDC / HATCHER (SPL tokens)

Same flow as SOL but `"paymentToken": "usdc"` or `"hatch"`. HATCHER gets 10% burned on every payment (deflationary); 90% to treasury.

## Upgrade / downgrade

Upgrading to a higher tier refunds unused days of the current tier as HATCHER credits, then charges the new tier:

```bash
curl -sS -X POST https://api.hatcher.host/features/subscribe-with-credits \
  -H "Authorization: Bearer $HATCHER_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "tier": "pro", "billingPeriod": "monthly" }'
```

Downgrade: no refund. Current tier runs until expiry, then the chosen lower tier takes effect.

## BYOK (Bring Your Own Key)

Any tier can switch to BYOK for LLM keys (OpenAI, Anthropic, Groq, etc.) — bypasses all message/search quotas but user pays the LLM provider directly.

```bash
curl -sS -X PATCH https://api.hatcher.host/api/v1/agents/$AGENT_ID/config \
  -H "Authorization: Bearer $HATCHER_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "byok.provider": "anthropic", "byok.apiKey": "sk-ant-..." }'
```

The API key is encrypted at rest (AES-256-GCM) and never logged.

## See also

- [`agents.md`](./agents.md) — what each tier lets you create
- [`integrations.md`](./integrations.md) — addon-level features vary by integration
