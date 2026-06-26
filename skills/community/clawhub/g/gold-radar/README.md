---
name: gold-intel-monitor
description: Real-time gold price monitoring and investment decision support system. Use when users ask about gold prices, gold investment analysis, market trends for precious metals, gold trading signals, or portfolio management for gold holdings. Also trigger when users mention XAU/USD, gold market outlook, Federal Reserve impact on gold, or when they want alerts for gold price movements. Helps track price fluctuations, analyze market trends, set price alerts, monitor technical indicators, and make trading decisions.
---

# Gold Intelligence Monitor

Real-time gold price monitoring and investment alert system.

## When to Use This Skill

This skill should be triggered when the user:
- Asks about current gold prices or XAU/USD rates
- Wants gold investment analysis or trading advice
- Requests market briefings or price alerts
- Mentions gold-related economic indicators (Fed rates, USD, inflation)
- Needs help tracking their gold portfolio or positions

## Quick Start

1. Check `config.json` for user profile (currency, timezone, watchlist)
2. Use the workflow below based on user request type

## Workflows

### Daily Briefing

When user asks for "daily briefing", "market update", or "what's happening with gold today":

```
Generate market briefing:
1. Get price trends for the past 24 hours
2. Check US Dollar Index movement
3. Review Fed officials' speeches/economic data releases
4. Provide position holding advice and risk management
```

**Output format:**
```
📋 Gold Market Briefing - {Date}

🎯 Market Overview:
{Summary}

💰 Price Quotes:
| Instrument | Price | Change | Key Level |
|------------|-------|--------|-----------|
| {Name} | {Price} | {Change} | {Key Level} |

📊 Technical Analysis:
- Support: {levels}
- Resistance: {levels}
- Trend: {Direction}

📅 Economic Calendar:
- {Time}: {Event} (Impact: {High/Medium/Low})

💡 Investment Recommendations:
- Holding Cost: {cost}
- Current P&L: {P&L}
- Recommended Action: {recommendation}

⚠️ Risk Warning: {level}
{Risk Description}
```

### Price Alert

When user asks for "alert me when...", "notify me if...", or mentions price targets:

**Alert Levels:**

| Level | Trigger Conditions | Response |
|-------|-------------------|----------|
| 🔴 Red | Price breaks target profit/stop-loss levels, daily movement >8%, major geopolitical conflicts | Immediate notification, execute trading decisions |
| 🟡 Yellow | Price breaks key round numbers, technical divergence, Fed officials' speeches | Prepare to trade, closely monitor |
| 🟢 Green | Normal price fluctuations, routine market monitoring | Regular briefings |

**Alert output format:**
```
🚨 [Alert Level] {Alert Type}

💰 Instrument: {Gold Type}
📈 Current Price: {Price} ({Change})
🎯 Key Level: {Breakout Level}

⚡ Recommended Actions:
1. {Action 1}
2. {Action 2}
3. {Action 3}

📊 Market Analysis:
{Brief Analysis}

🔗 Influencing Factors:
- US Dollar Index: {DXY}
- Treasury Yield: {US10Y}
- Major Events: {event}
```

### Weekly Analysis

When user asks for "weekly outlook", "this week", or "Monday analysis":

```
Generate weekly outlook:
1. Review last week's gold price performance
2. This week's economic calendar (Fed meetings, NFP, etc.)
3. Technical analysis (trends, key support/resistance)
4. Next week's trading strategy recommendations
```

### Buy/Sell Signal Check

When user asks "should I buy?", "sell now?", or "is it a good time to invest":

**Buy Signals:**
- Federal Reserve rate cut expectations rise
- Geopolitical risks escalate
- Technical breakout (breaks consolidation range)

**Sell Signals:**
- Federal Reserve rate hike expectations rise
- Technical breakdown (breaks support level)
- Position reaches expected profit (take profit)

## Data Sources Priority

1. **Official:** Shanghai Gold Exchange (SGE), World Gold Council (WGC)
2. **Market:** Bloomberg/Reuters, TradingView, Kitco
3. **Macro:** Federal Reserve, Non-farm payroll, CPI/PPI
4. **Sentiment:** X/Twitter posts, geopolitical news, central bank reports

## Configuration

Edit `config.json` to customize:
- Holding cost and target price levels
- Alert thresholds (price change percentage)
- Gold instruments to monitor (spot, futures, ETFs)
- Local timezone and currency

## Disclaimer

This system is for reference only and does not constitute investment advice. Gold investment involves risks; invest with caution.
