---
name: paradex-portfolio-copilot
description: >
  Conversational portfolio briefings for Paradex accounts and vaults. Unifies
  account summary, positions, fills, balances, market data, and funding into
  natural language answers to questions like "how am I doing?", "what happened
  today?", "what's my P&L?", "summarize my portfolio", "what are my positions?",
  "how much have I made?", or "give me a morning briefing". Use this skill whenever
  a user asks about their Paradex portfolio status, performance, positions, P&L,
  balance, trade history, or wants a high-level summary of their Paradex activity.
  Also trigger for "my account", "my positions", "daily recap", "portfolio overview",
  "how did I do", or any conversational question about the state of their Paradex
  account. This is the go-to skill for any "show me my stuff" type question on Paradex.
---

# Paradex Portfolio Copilot

The conversational interface for "what's going on with my Paradex account."
Turns scattered data from multiple MCP tools into clear, concise briefings.

## Available MCP Tools

| Tool | Portfolio data |
|---|---|
| `paradex_vault_account_summary` | Equity, margin, account health |
| `paradex_vault_positions` | All open positions with P&L |
| `paradex_vault_balance` | Cash balances |
| `paradex_vault_transfers` | Deposit/withdrawal history |
| `paradex_market_summaries` | Current prices, 24h changes for context |
| `paradex_bbo` | Real-time prices for any specific market |
| `paradex_funding_data` | Funding payments for cost tracking |

## Briefing Types

### 1. Quick Status ("How am I doing?")

The minimum viable answer. Pull `vault_account_summary` + `vault_positions`:

```
Your Paradex account has $X equity with N open positions.
Unrealized P&L: +$X (+X%).
Largest position: MARKET at $X notional.
Margin used: X% — [healthy/watch it/tight].
```

Keep it to 3-4 sentences. Only expand if asked.

### 2. Position Breakdown ("What are my positions?")

Pull `vault_positions` and present clearly:

For each position, report:
- Market (e.g., BTC-USD-PERP)
- Direction (Long/Short)
- Size (in base currency and USD notional)
- Entry price (if available)
- Current mark price (from market_summaries)
- Unrealized P&L (dollar and percentage)
- Funding status (paying or receiving)

Sort by: largest notional first, or by P&L if user asks about winners/losers.

### 3. Daily Recap ("What happened today?")

Combine multiple data sources:

1. **Account snapshot**: equity change from start of day (if inferrable from transfers + P&L)
2. **Position changes**: new positions opened, positions closed, size changes
3. **P&L breakdown**: which positions contributed most to today's P&L
4. **Funding costs**: total funding paid/received today
5. **Market context**: how did the user's markets move? (from market_summaries price_change_rate_24h)

### 4. Morning Briefing ("Give me a briefing")

A comprehensive start-of-day view:

1. **Account overview**: equity, margin health, free capital
2. **Position summary**: all positions with overnight P&L
3. **Overnight funding**: total funding cost/income since last session
4. **Market context**: how the user's markets moved overnight
5. **Risk flags**: anything that needs attention (high margin, large unrealized loss, funding drain)
6. **Today's outlook**: key levels or events for the user's markets (if identifiable from data)

### 5. P&L Analysis ("How much have I made?")

The most common question. Answer at the right granularity:

**If they ask about total P&L:**
- Total unrealized from current positions
- Note that realized P&L from closed positions isn't directly available via current MCP tools
- Suggest checking the Paradex UI for full trade history

**If they ask about a specific position:**
- Current unrealized P&L
- Entry price vs. current price
- Funding costs accumulated (estimate from funding_data)

**If they ask about a time period:**
- Use position data + market price changes to estimate
- Be honest about precision: "Based on current positions and recent market moves, approximately..."

### 6. Balance & Cash ("How much do I have?")

Pull `vault_balance`:
- Total balance
- Available (free to trade or withdraw)
- Locked (in positions as margin)
- Ratio of deployed vs. idle capital

If user asks about deposits/withdrawals, also pull `vault_transfers`:
- Recent transfer history
- Net deposits over time
- Any pending transfers

## Conversational Patterns

The copilot should feel like talking to a knowledgeable friend, not reading a report.

**Match the question's energy:**
- "How am I doing?" → 2-3 sentence summary, positive framing, flag concerns
- "Give me everything" → Full detailed briefing
- "Am I making money?" → Lead with the P&L number, then context
- "What's my biggest position?" → Direct answer, then relevant context

**Proactive observations:**
After answering the direct question, add 1 relevant observation if useful:
- "By the way, your ETH position is now 55% of your exposure — worth keeping an eye on."
- "Your funding costs are running about $X/day — mostly from the SOL position."
- "Your margin is at 72% — you don't have much room for new positions."

Don't add observations every time — only when something is noteworthy.

**Follow-up suggestions:**
End with 1 natural follow-up when appropriate:
- "Want me to break down the P&L by position?"
- "Want a risk check on your current positions?"
- "Should I look at what's happening in those markets?"

## Output Style

- Lead with the answer, not the process
- Use dollar amounts for P&L and equity (real money feels concrete)
- Use percentages for changes and ratios
- Round sensibly: $12,345 not $12,345.6789
- Use 🟢🟡🔴 sparingly — only for clear health indicators
- No tables unless the user has 4+ positions (just describe 1-3 positions in prose)
- Tables for 4+ positions with clean columns: Market | Direction | Size | P&L

## Caveats

- Realized P&L from closed trades is not directly available from the current MCP tools.
  Be upfront about this and point users to the Paradex UI for complete history.
- P&L estimates for time periods are approximate — based on current positions and market moves
- Account data is a point-in-time snapshot — positions and prices change continuously
- This is portfolio information, not trading advice

See [briefing-formats.md](references/briefing-formats.md) for detailed output templates with examples.
