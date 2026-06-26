---
name: mobula-alerts
displayName: Mobula - Smart Alerts & Monitoring
description: 24/7 autonomous monitoring for crypto portfolios, whales, and market conditions. Multi-condition alerts via OpenClaw heartbeat.
version: 1.0.0
author: Mobula
category: crypto
tags:
  - crypto
  - alerts
  - monitoring
  - automation
  - heartbeat
requiredEnvVars:
  - MOBULA_API_KEY
homepage: https://mobula.io
docs: https://docs.mobula.io
repository: https://github.com/Flotapponnier/Crypto-date-openclaw
---

# Mobula - Smart Alerts & Monitoring

24/7 autonomous crypto monitoring using OpenClaw's heartbeat system. Set conditions once, let your agent monitor continuously and alert you on Telegram/WhatsApp/Discord.

## Quick Start

**1. Get your free API key** (no credit card required)
- Go to [mobula.io](https://mobula.io) and sign up
- Free tier: 100 requests/minute
- Copy your API key from the dashboard

**2. Set your API key**
```bash
export MOBULA_API_KEY="your_api_key_here"
```

**3. Set up monitoring**
Ask your agent:
- "Alert me if BTC moves more than 5% in 1 hour"
- "Monitor my wallet and alert if any token drops 15%"
- "Watch these whale wallets and alert on large buys"
- "Find new tokens on Base matching my criteria every 6 hours"
- "Send me a market brief every morning at 7am"

---

## Security

✅ **Read-only access** - No trading, no transactions
✅ **No private keys** - Only public blockchain data
✅ **Open source** - [View code on GitHub](https://github.com/Flotapponnier/Crypto-date-openclaw)
✅ **VirusTotal verified** - Benign scan results

---

## How It Works

Unlike ChatGPT/Claude chat, your OpenClaw agent runs continuously. The heartbeat system (~30min intervals) allows your agent to:

1. **Check conditions** you've set (price thresholds, portfolio changes, whale movements)
2. **Fetch data** from Mobula API when needed
3. **Analyze** using multi-condition logic (not just "price > X")
4. **Alert** you on Telegram/WhatsApp/Discord only when conditions are met

This skill provides **monitoring patterns** using Mobula endpoints. Combine with **mobula-prices** and **mobula-wallet** skills for complete functionality.

---

## Monitoring Patterns

### Pattern 1: Portfolio Guardian

Monitor your wallet 24/7 for concentration risks and drops.

**Setup:**
> "Monitor my wallet 0x... and alert me on Telegram if any token drops more than 15% or my allocation exceeds 40% on one asset. Daily summary at 9am."

**How it works:**

Every heartbeat (~30min):
1. Fetch portfolio via `mobula_wallet_portfolio`
2. Calculate allocation percentages
3. Check conditions:
   - Any token >40% of portfolio → suggest rebalancing
   - Any token down >15% in 24h → alert with context
   - Total portfolio changed >10% → notify
4. Store previous values in memory to detect changes
5. Send daily summary at user's preferred time

**Example alert:**
```
⚠️ Portfolio Alert

Your ETH allocation is now 47% (was 38% yesterday).
Consider rebalancing to reduce concentration risk.

Current holdings:
- ETH: $12,340 (47%)
- BRETT: $8,200 (31%) up 12% 24h
- DEGEN: $5,890 (22%) down 3% 24h
```

---

### Pattern 2: Whale Watching

Track smart money and get alerted when whales move.

**Setup:**
> "Watch wallets 0xabc, 0xdef, 0x123. Alert if any buy/sell more than $50K. If multiple whales buy the same token within 6h, priority alert with full analysis."

**How it works:**

Every heartbeat:
1. Check transactions via `mobula_wallet_transactions`
2. If new significant transaction (>$50K):
   - Get token details via `mobula_market_data`
   - Check recent trades via `mobula_market_trades`
   - Cross-check if other tracked whales bought same token
3. If multiple whales buying → **priority alert**

**Example alert:**
```
🚨 Whale Alert - HIGH PRIORITY

Wallet 0x742d... bought $150K of BRETT on Base (2h ago)

Token: BRETT | Price: $0.089 (up 23% 24h)
Mcap: $2.3M | Volume: $1.2M (8x normal)

Cross-signal: 2 other tracked whales also bought BRETT:
- 0x888... bought $80K (4h ago)
- 0x111... bought $120K (1h ago)

⚠️ Possible coordinated accumulation.
```

---

### Pattern 3: Token Scout (Autonomous Discovery)

Agent autonomously finds new tokens matching your criteria.

**Setup:**
> "Find tokens on Base/Arbitrum every 6h: mcap under $5M, liquidity over $100K, volume up 50%+ 24h, verified contract. Send top 3 with analysis."

**How it works:**

Every 4-6 hours on heartbeat:
1. User defines criteria (stored in memory):
   - Chains: Base, Arbitrum
   - Market cap: <$5M
   - Liquidity: >$100K
   - Volume change 24h: >+50%
2. Search/filter tokens via `mobula_market_data`
3. For each match:
   - Get 7-day history via `mobula_market_history`
   - Check metadata via `mobula_metadata`
   - Calculate risk score
4. Send top 3 with analysis

**Example alert:**
```
🔍 Token Scout - 3 New Matches

1. BOOP on Base
   - Price: $0.0042 (up 156% 24h, up 340% 7d)
   - Mcap: $2.1M | Liquidity: $280K
   - Volume: $890K (12x average)
   - Contract: Verified ✅
   - Risk: Medium

2. ZORP on Arbitrum
   - Price: $0.0089 (up 78% 24h)
   - Mcap: $3.4M | Liquidity: $450K
   - Whale buy: $60K (3h ago)
   - Risk: Medium-High

3. [...]
```

---

### Pattern 4: Smart Price Alerts

Contextual alerts with multi-condition logic (not just "price > X").

**Setup:**
> "Alert me if BTC moves more than 5% in 1 hour, BUT only if volume is 2x above 24h average. Real moves, not noise."

**How it works:**

Every heartbeat:
1. Get current price and volume via `mobula_market_data`
2. Compare to price from 1 hour ago (stored in memory)
3. Check if volume condition met
4. Only alert if **BOTH** conditions true

**Other smart alert examples:**
- "Alert if ETH breaks $4K after consolidating $3,800-$3,950 for 3+ days"
- "Alert if any of my watchlist tokens pump >20% with volume >5x average"
- "Alert if BTC drops >3% but ETH is green (divergence signal)"

---

### Pattern 5: Market Brief

Automated morning/evening market overviews.

**Setup:**
> "Send market overview at 7am and 7pm on Telegram. Include BTC, ETH, SOL, and any top 100 token that moved more than 10%."

**How it works:**

Every scheduled time (7am, 7pm):
1. Check major tokens (BTC, ETH, SOL, BNB) via `mobula_market_multi`
2. Identify major moves (>5% in 24h)
3. Check volume leaders
4. Provide concise overview

**Example brief:**
```
📊 Crypto Market Brief - Feb 20, 7:00 AM

Majors:
- BTC: $67,234 (up 2.1% 24h)
- ETH: $3,456 (up 4.3% 24h)
- SOL: $123.45 (down 1.2% 24h)

Big Movers (24h):
- PEPE: up 23%
- ARB: up 15%
- AVAX: down 12%

Sentiment: Cautiously bullish. ETH leading, memes pumping.
```

---

## Setting Up Heartbeat Monitoring

**Step 1: Tell your agent what to monitor**

Be specific about:
- What to track (wallets, tokens, conditions)
- When to alert (thresholds, multi-condition logic)
- How often to check (30min, 1h, 6h)
- Where to alert (Telegram, Discord, WhatsApp)

**Step 2: Agent stores config in memory**

Your agent remembers:
- Monitoring tasks
- Previous values (for change detection)
- Alert preferences
- Scheduling

**Step 3: Agent monitors on heartbeat**

Every heartbeat interval:
- Fetches only necessary data (respects rate limits)
- Compares to previous values
- Evaluates conditions
- Sends alerts when triggered

---

## Combining Endpoints for Rich Analysis

### Full Token Analysis

User asks: "Should I buy this token?"

1. `mobula_market_data` → current price, mcap, volume, liquidity
2. `mobula_market_history` → 7d and 30d trend
3. `mobula_market_trades` → recent activity (accumulation or distribution?)
4. `mobula_metadata` → project info, socials, verification

**Response format:**
```
TOKEN Analysis

Price: $0.042 (down 8% 24h, up 156% 7d)
- Near 7d high, down from $0.051
- Still up 400% from 30d low

Fundamentals:
- Mcap: $2.1M (small cap, high risk/reward)
- Liquidity: $280K (decent for size)
- Volume: $1.2M 24h (healthy)

On-chain:
- Recent trades show buying pressure (3:1 buy/sell ratio)
- 2 large buys ($50K+) in last 2h

Project:
- Contract verified ✅
- Active Twitter (12K followers)

Risk: Small cap, high volatility. Don't ape more than you can lose.
```

---

## Authentication

All requests require your API key in the `Authorization` header:
```
Authorization: ${MOBULA_API_KEY}
```

**If authentication fails (401/403):**
- Verify: `echo $MOBULA_API_KEY`
- Regenerate at [mobula.io](https://mobula.io) if expired
- Check rate limits (100 req/min free tier)

---

## Rate Limits & Best Practices

### Respect Rate Limits
- **Free tier:** 100 requests/minute
- Use `mobula_market_multi` for batch queries
- Cache data in memory (metadata doesn't change often)

### Efficient Heartbeat Usage
- Don't call every endpoint on every heartbeat
- Only fetch what's needed based on active monitoring
- Batch requests when possible
- Store previous values to detect changes

---

## Error Handling

**API Key Issues:**
- "I need a Mobula API key. Get one free at https://mobula.io then set it: `export MOBULA_API_KEY='your_key'`"
- "Invalid API key. Check it at https://mobula.io"
- "Rate limit hit. Upgrade at https://mobula.io or retry later"

**Monitoring Setup:**
- "What conditions should I monitor for?"
- "How often should I check? (30min, 1h, 6h)"
- "Where should I send alerts? (Telegram, Discord, WhatsApp)"

---

## When to Use This Skill

**✅ USE WHEN the user:**
- Wants to set up alerts or monitoring
- Asks for 24/7 tracking
- Wants autonomous discovery
- Needs scheduled reports or briefs
- Mentions "alert me when", "monitor", "track", "watch"

**❌ DON'T USE WHEN:**
- User wants one-time price check (use mobula-prices)
- User wants to check portfolio once (use mobula-wallet)

---

## Related Skills

- **mobula-prices** - Token prices and market data (required for alerts)
- **mobula-wallet** - Portfolio tracking (required for wallet monitoring)

---

## Ready-to-Use Templates

Copy these templates to `~/openclaw/heartbeat/`:

- **[`heartbeat-portfolio-guardian.md`](../../examples/heartbeat-portfolio-guardian.md)**
- **[`heartbeat-whale-tracker.md`](../../examples/heartbeat-whale-tracker.md)**
- **[`heartbeat-token-scout.md`](../../examples/heartbeat-token-scout.md)**
- **[`heartbeat-market-brief.md`](../../examples/heartbeat-market-brief.md)**

---

## Resources

- **Get API Key:** [mobula.io](https://mobula.io)
- **API Docs:** [docs.mobula.io](https://docs.mobula.io)
- **GitHub:** [Mobula OpenClaw Skills](https://github.com/Flotapponnier/Crypto-date-openclaw)
- **Support:** Open issue on GitHub

---

## Version History

**1.0.0** (2024-03-25): Initial release
- Portfolio guardian pattern
- Whale watching pattern
- Autonomous token scout
- Smart price alerts
- Market brief automation
- Heartbeat optimization tips
