---
name: lpxpoly
description: AI-powered Polymarket prediction market analysis via Bitcoin Lightning. Find mispriced markets, get AI edge on probability vs market price. ~50 sats per analysis.
acceptLicenseTerms: true
metadata:
  clawdbot:
    emoji: "📊"
    homepage: https://lpxpoly.com
    requires:
      env:
        - LIGHTNINGPROX_SPEND_TOKEN
---

# LPXPoly — AI-Powered Polymarket Analysis

Find edge in prediction markets using AI probability estimation vs current market prices. Pay ~50 sats per analysis via Bitcoin Lightning. No subscription, no account.

## When to Use

- Finding mispriced markets on Polymarket
- Getting AI probability assessment on specific events
- Scanning for arbitrage opportunities in prediction markets
- Comparing AI model probability vs crowd wisdom
- Browsing top markets by volume or category

## Tools

### `get_edge_opportunities`
Scans Polymarket for markets where AI probability significantly diverges from market price.

```
"Find edge opportunities on Polymarket"
→ Returns top mispriced markets with AI vs market probability delta
→ Sorted by edge magnitude
→ Includes recommended position (YES/NO) and confidence
```

### `analyze_market`
Deep AI analysis of a specific Polymarket market.

```
"Analyze the Fed rate cut market"
→ Returns AI probability estimate with reasoning
→ Includes key factors, risks, and recommended position size
→ Compares to current market price
```

### `get_top_markets`
Browse top Polymarket markets by volume, filtered by category.

```
"What are the top crypto markets on Polymarket?"
→ Returns markets sorted by volume
→ Filter by: crypto, politics, sports, science, tech, world
```

### `check_balance`
Check your Lightning balance before running expensive scans.

```
"How much Lightning balance do I have?"
→ Returns current sats balance
→ Includes link to top up if low
```

## Behavior Guidelines

**Before a full market scan:**
1. `check_balance` — confirm enough sats for the scan
2. `get_edge_opportunities` — retrieve top mispriced markets
3. Present findings with edge delta and confidence

**For a specific market:**
1. `analyze_market` with market name or URL
2. Return AI probability, reasoning, and position recommendation

**Cost awareness:**
- Each `get_edge_opportunities` call: ~50 sats
- Each `analyze_market` call: ~50 sats
- Warn if balance < 200 sats before a multi-analysis session

## Example Interactions

**User:** "Find edge opportunities on Polymarket"

**You:** check_balance → get_edge_opportunities → present top 5 markets with edge delta, AI probability vs market price, and recommended positions

---

**User:** "What does AI think about the Bitcoin ETF approval market?"

**You:** analyze_market("Bitcoin ETF approval") → return AI probability estimate, key factors, comparison to market price, recommended position

---

**User:** "What are the biggest crypto prediction markets right now?"

**You:** get_top_markets(category="crypto") → return top markets by volume with current prices

## Payment

~50 sats per analysis. Pay with Bitcoin Lightning. Get a spend token at [lightningprox.com](https://lightningprox.com).

```json
{
  "mcpServers": {
    "lpxpoly": {
      "command": "npx",
      "args": ["lpxpoly-mcp"],
      "env": {
        "LIGHTNINGPROX_SPEND_TOKEN": "lnpx_your_token_here"
      }
    }
  }
}
```

## Security Manifest

| Permission | Scope | Reason |
|------------|-------|--------|
| Network | lpxpoly.com, lightningprox.com | Market data and Lightning payment |
| Env Read | LIGHTNINGPROX_SPEND_TOKEN | Authentication for paid analysis calls |

## Trust Statement

LPXPoly is part of the AIProx ecosystem, operated by LPX Digital Group LLC. Market analysis is AI-generated probability estimation — not financial advice. Sats deducted from LightningProx balance per successful analysis only. Operated at lpxpoly.com.
