---
name: neckr0ik-polymarket-paper
version: 1.0.0
description: Paper trading platform for Polymarket. Practice prediction market trading with virtual money, learn strategies, track performance, and compete on leaderboards. Use for training before risking real capital.
---

# Polymarket Paper Trading

Practice Polymarket trading with virtual money. Learn strategies. Compete on leaderboards.

## Quick Start

```bash
# Create account with $10,000 virtual
neckr0ik-polymarket-paper create-account --name "MyPortfolio"

# View available markets
neckr0ik-polymarket-paper markets --limit 20

# Place a trade
neckr0ik-polymarket-paper trade --market "will-bitcoin-reach-100k" --side YES --amount 500

# Check portfolio
neckr0ik-polymarket-paper portfolio

# View leaderboard
neckr0ik-polymarket-paper leaderboard --weekly
```

## What This Does

- **Virtual trading** — $10,000 practice account
- **Real market data** — Live Polymarket prices
- **Simulated execution** — Orders filled at market price
- **Performance tracking** — Win rate, ROI, Sharpe ratio
- **Leaderboards** — Compete with other paper traders
- **Strategy guides** — Learn before risking real money

## Account Types

| Tier | Virtual Cash | Markets/Day | Analytics |
|------|---------------|--------------|-----------|
| Free | $10,000 | 5 | Basic |
| Pro ($9/mo) | $100,000 | Unlimited | Advanced |
| Team ($29/mo) | Multiple accounts | Unlimited | Full |

## Commands

### create-account

Create a paper trading account.

```bash
neckr0ik-polymarket-paper create-account [options]

Options:
  --name <name>        Account name
  --tier <tier>        Account tier (free, pro, team)
  --initial <amount>   Starting cash (default: 10000)
```

### markets

View available Polymarket markets.

```bash
neckr0ik-polymarket-paper markets [options]

Options:
  --limit <n>         Max results (default: 20)
  --category <name>   Filter by category (crypto, politics, sports)
  --search <query>     Search by keyword
```

### trade

Place a paper trade.

```bash
neckr0ik-polymarket-paper trade [options]

Options:
  --market <id>        Market ID or slug
  --side <side>        YES or NO
  --amount <dollars>   Amount to trade
  --limit <price>      Limit price (optional)
```

### portfolio

View your portfolio.

```bash
neckr0ik-polymarket-paper portfolio [options]

Options:
  --history            Show transaction history
  --performance        Show performance metrics
```

### resolve

Manually resolve a market (for practice).

```bash
neckr0ik-polymarket-paper resolve --market <id> --outcome <YES|NO>
```

### leaderboard

View top paper traders.

```bash
neckr0ik-polymarket-paper leaderboard [options]

Options:
  --period <period>    weekly, monthly, all-time
  --strategy <type>    Filter by strategy
```

### analytics

View detailed analytics.

```bash
neckr0ik-polymarket-paper analytics [options]

Options:
  --period <days>      Analysis period (default: 30)
  --strategy           Breakdown by strategy
```

### export

Export your trading history.

```bash
neckr0ik-polymarket-paper export [options]

Options:
  --format <format>    csv, json
  --output <file>      Output file
```

## Trading Strategies

### 1. Spread Arbitrage (Practice)

Buy both YES and NO when combined < $1.00.

```
Example:
Market: "Will Bitcoin hit $100k?"
YES: $0.48
NO: $0.50
Combined: $0.98

Trade: Buy $490 YES + $500 NO = $990 total
Guaranteed payout: $1,000
Profit: $10 (1.01%)
```

### 2. Endgame Trading

Buy near-certain outcomes close to resolution.

```
Example:
Market: "Will X happen by March 31?"
Current: March 28
YES price: $0.97
Days remaining: 3

Trade: Buy YES at $0.97
Hold until resolution at $1.00
Profit: 3.1% in 3 days (376% annualized)
```

### 3. News Correlation

Trade on news before market adjusts.

```
Example:
News: "Israel strikes Tehran. Trump demands surrender."
Market: "Will Trump declare war on Iran?" @ 40%

Analysis: Military action ≠ formal war declaration
Market likely overpriced
Trade: Sell YES (or buy NO)
```

## Performance Metrics

| Metric | Description |
|--------|-------------|
| Total PnL | Total profit/loss |
| Win Rate | % of trades profitable |
| Average Return | Mean return per trade |
| Sharpe Ratio | Risk-adjusted return |
| Max Drawdown | Largest peak-to-trough |
| Calmar Ratio | Return / max drawdown |

## Leaderboard Categories

| Category | Ranking By |
|----------|-----------|
| Overall | Total PnL |
| ROI | Return on investment |
| Win Rate | % profitable trades |
| Sharpe | Risk-adjusted return |
| Streak | Longest win streak |

## Educational Content

### Strategy Guides

1. **Spread Arbitrage 101** — Risk-free profit basics
2. **Endgame Trading** — Near-certain outcomes
3. **News Correlation** — Event-driven trading
4. **Risk Management** — Position sizing, stop-losses
5. **Advanced Strategies** — Cross-market, cross-platform

### Practice Scenarios

1. **Scenario: Crypto Bull Run**
   - Start with $50,000
   - Market: "Will BTC hit $150k by EOY?"
   - Learn: Position sizing, timing

2. **Scenario: Election Night**
   - Start with $25,000
   - Markets: Multiple election outcomes
   - Learn: Hedging, correlation

3. **Scenario: Market Crash**
   - Start with $100,000
   - Market: "Will S&P drop below 4000?"
   - Learn: Risk management, stop-losses

## Example Session

```bash
$ neckr0ik-polymarket-paper create-account --name "Learning"
✓ Created account: Learning
  Virtual cash: $10,000

$ neckr0ik-polymarket-paper markets --search "bitcoin"
Found 5 markets:
  1. "Will Bitcoin hit $100k by EOY 2026?" YES: 0.45
  2. "Will Bitcoin drop below $50k?" NO: 0.65
  3. "Will Bitcoin be banned?" NO: 0.92
  ...

$ neckr0ik-polymarket-paper trade --market "bitcoin-100k" --side YES --amount 1000
✓ Trade executed
  Market: "Will Bitcoin hit $100k by EOY 2026?"
  Side: YES
  Amount: $1,000
  Price: $0.45
  Shares: 2,222.22
  Fee: $0.01

$ neckr0ik-polymarket-paper portfolio
Portfolio: Learning
Cash: $8,999.99
Positions:
  - "bitcoin-100k" YES: 2,222.22 shares @ $0.45 = $999.99
Total Value: $10,000.00 (0.00% return)

$ neckr0ik-polymarket-paper leaderboard --weekly
Weekly Leaderboard:
  1. @trader1: +15.2% ($1,520 profit)
  2. @trader2: +12.8% ($1,280 profit)
  3. @trader3: +10.5% ($1,050 profit)
  ...
  127. @Learning: 0.0% ($0 profit)
```

## See Also

- `references/strategies.md` — Detailed strategy guides
- `scripts/paper_trading.py` — Main implementation
- `projects/polymarket-paper-trading/` — Full platform design