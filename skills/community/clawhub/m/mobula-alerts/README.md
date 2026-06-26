# Mobula Alerts - 24/7 Smart Crypto Monitoring

> 24/7 autonomous monitoring for crypto portfolios, whales, and market conditions. Multi-condition alerts via OpenClaw heartbeat.

[![ClawHub](https://img.shields.io/badge/ClawHub-Install-blue)](https://clawhub.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What This Skill Does

**mobula-alerts** transforms your OpenClaw agent into a 24/7 crypto monitoring system. Set conditions once, and your agent continuously monitors prices, portfolios, whales, and market conditions — alerting you only when something important happens.

### Key Features

✅ **Portfolio Guardian** - Alert on concentration risks, drops, allocation changes
✅ **Whale Watching** - Track smart money movements across wallets
✅ **Token Scout** - Autonomously discover new tokens matching your criteria
✅ **Smart Alerts** - Multi-condition logic (price + volume + on-chain signals)
✅ **Market Briefs** - Automated morning/evening summaries

### Perfect For

- Portfolio managers wanting 24/7 risk monitoring
- Traders tracking whale movements
- Alpha hunters discovering new tokens
- Anyone wanting proactive (not reactive) crypto monitoring

---

## How This Is Different

**ChatGPT/Claude chat:**
- You ask → it answers
- You need to remember to check
- No continuous monitoring

**OpenClaw + mobula-alerts:**
- Set conditions once → agent monitors 24/7
- Agent alerts you on Telegram/Discord/WhatsApp
- No prompting needed, it works autonomously

**Example:**
```
You: "Alert me if BTC moves >5% in 1h with volume 2x above average"

Agent: [Monitors every 30min via heartbeat]
        [Only alerts when BOTH conditions met]
        [You do other things while it watches]
```

---

## Quick Start (5 minutes)

### 1. Install All Required Skills

This skill orchestrates monitoring using data from:
- **[mobula-prices](../mobula-prices/)** - For price and market data
- **[mobula-wallet](../mobula-wallet/)** - For portfolio tracking

Install all 3:
```
Tell your agent: "Install mobula-prices, mobula-wallet, and mobula-alerts from ClawHub"
```

### 2. Get Your Free API Key

1. Go to [mobula.io](https://mobula.io)
2. Sign up (takes 30 seconds)
3. Copy your API key from the dashboard

**Free tier includes:**
- 100 requests/minute
- No credit card required
- Sufficient for most monitoring tasks

### 3. Set Your API Key

```bash
export MOBULA_API_KEY="your_api_key_here"
```

**Make it permanent:**
```bash
echo 'export MOBULA_API_KEY="your_key"' >> ~/.zshrc
source ~/.zshrc
```

### 4. Set Up Your First Alert

Ask your agent:
```
"Alert me if BTC moves more than 5% in 1 hour"
```

Your agent will:
1. Acknowledge the monitoring task
2. Store the condition in memory
3. Check every heartbeat (~30min)
4. Alert you only when the condition is met

---

## Monitoring Patterns

### Pattern 1: Portfolio Guardian

**What it does:** Monitors your wallet 24/7 for concentration risks and significant drops.

**Setup:**
```
"Monitor my wallet 0x... and alert me on Telegram if:
- Any token drops more than 15%
- My allocation exceeds 40% on one asset
- Total portfolio value changes by more than 10%

Send me a daily summary at 9am."
```

**How it works:**
- Every heartbeat (~30min):
  - Fetches your portfolio
  - Calculates allocation percentages
  - Compares to previous values
  - Alerts on threshold breaches

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

**What it does:** Tracks smart money movements and alerts on coordinated activity.

**Setup:**
```
"Watch these whale wallets: 0xabc, 0xdef, 0x123

Alert me if:
- Any wallet buys/sells more than $50K
- Multiple whales buy the same token within 6h (priority alert)
- Any whale dumps a token I'm holding
```

**How it works:**
- Every heartbeat:
  - Checks transactions for tracked wallets
  - If significant trade (>$50K):
    - Gets token details
    - Checks if other whales bought same token
    - Cross-references with your holdings

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

### Pattern 3: Token Scout

**What it does:** Autonomously discovers new tokens matching your criteria.

**Setup:**
```
"Find new tokens every 6 hours with these criteria:
- Chains: Base, Arbitrum
- Market cap: under $5M
- Liquidity: over $100K
- Volume: up 50%+ in 24h
- Contract: verified only

Send me top 3 matches with full analysis."
```

**How it works:**
- Every 6 hours (on heartbeat):
  - Searches tokens matching criteria
  - For each match:
    - Gets 7-day price history
    - Checks metadata and verification
    - Calculates risk score
  - Sends top 3 with analysis

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

**What it does:** Multi-condition alerts (not just "price > X").

**Setup:**
```
"Alert me if BTC moves more than 5% in 1 hour,
BUT only if volume is 2x above 24h average.
I want real moves, not noise."
```

**Other examples:**
```
"Alert if ETH breaks $4K after consolidating
between $3,800-$3,950 for 3+ days"

"Alert if any of my watchlist tokens pump >20%
with volume >5x average"

"Alert if BTC drops >3% but ETH is green
(divergence signal)"
```

**How it works:**
- Every heartbeat:
  - Fetches current data
  - Compares to stored previous values
  - Evaluates ALL conditions
  - Only alerts if ALL conditions true

---

### Pattern 5: Market Brief

**What it does:** Automated morning/evening market summaries.

**Setup:**
```
"Send market overview at 7am and 7pm on Telegram.

Include:
- BTC, ETH, SOL performance
- Any top 100 token that moved >10%
- Biggest volume gainers
- Overall sentiment analysis
```

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

## Ready-to-Use Templates

Copy these heartbeat templates to `~/openclaw/heartbeat/`:

**Available templates:**
- [Portfolio Guardian](../../examples/heartbeat-portfolio-guardian.md)
- [Whale Tracker](../../examples/heartbeat-whale-tracker.md)
- [Token Scout](../../examples/heartbeat-token-scout.md)
- [Market Brief](../../examples/heartbeat-market-brief.md)

**How to use:**
1. Copy template to `~/openclaw/heartbeat/`
2. Edit wallet addresses, criteria, timing
3. Agent executes automatically on schedule

---

## Security

✅ **Read-only access** - No trading, no transactions
✅ **No private keys** - Only public blockchain data
✅ **Open source** - [View code on GitHub](https://github.com/Flotapponnier/Crypto-date-openclaw)
✅ **VirusTotal verified** - Benign scan results

This skill only reads public data. It cannot:
- Execute trades
- Access wallets
- Sign transactions
- Transfer funds

---

## Rate Limits & Best Practices

**Free tier:** 100 requests/minute

**Optimization tips:**
- Set heartbeat to 30-60min intervals (not every minute)
- Use batch endpoints for multiple tokens
- Cache metadata (rarely changes)
- Only fetch data for active monitoring tasks

**Example efficient setup:**
- Portfolio checks: every 30min
- Whale watching: every 30min
- Token scout: every 6 hours
- Market brief: twice daily

---

## Troubleshooting

### Agent not monitoring

**Check:**
1. All 3 skills installed (mobula-prices, mobula-wallet, mobula-alerts)
2. API key set: `echo $MOBULA_API_KEY`
3. Agent restarted: `openclaw restart`
4. Monitoring task confirmed by agent

### Alerts not firing

**Possible causes:**
- Conditions not met (verify thresholds are reasonable)
- Rate limit hit (reduce monitoring frequency)
- Agent not running (check `openclaw status`)

### Too many alerts

**Adjust conditions:**
- Increase thresholds (5% → 10%)
- Add multi-condition logic (price + volume)
- Reduce monitoring frequency

---

## Related Skills

This skill requires:
- **[mobula-prices](../mobula-prices/)** - For price and market data
- **[mobula-wallet](../mobula-wallet/)** - For portfolio tracking

---

## Resources

- **Get API Key:** [mobula.io](https://mobula.io)
- **API Documentation:** [docs.mobula.io](https://docs.mobula.io)
- **Main Repository:** [GitHub](https://github.com/Flotapponnier/Crypto-date-openclaw)
- **Report Issues:** [GitHub Issues](https://github.com/Flotapponnier/Crypto-date-openclaw/issues)
- **Skill Documentation:** [SKILL.md](./SKILL.md)

---

## FAQ

**Q: How often does the agent check?**
A: Every heartbeat interval (default ~30min). You can adjust this in your agent settings.

**Q: Can I get instant alerts?**
A: Current heartbeat system checks every ~30min. For instant alerts, WebSocket support is on the roadmap.

**Q: Where do I receive alerts?**
A: Configure your agent to send alerts via Telegram, Discord, WhatsApp, or Slack.

**Q: How many monitoring tasks can I set?**
A: Unlimited, but stay within rate limits (100 req/min free tier). Each monitoring task may use 1-5 requests per heartbeat.

**Q: Can I monitor without being alerted?**
A: Yes. Set up daily/weekly summaries instead of real-time alerts.

---

## License

MIT License - See [LICENSE](../../LICENSE)

---

## Credits

- **Built by:** [Mobula](https://mobula.io)
- **For:** [OpenClaw](https://openclaw.ai)
- **Powered by:** OpenClaw heartbeat system
