---
name: polymarket-negrisk-arb
description: Scan multi-outcome Polymarket markets for mathematical arbitrage. When the sum of all outcome prices falls below $1.00, buy all sides simultaneously via batch trade to lock in risk-free profit. No signals. No AI. Just math.
metadata:
  author: "r2creatorstudios"
  version: "1.0.2"
  displayName: "Polymarket NegRisk Arbitrage"
  difficulty: "intermediate"
---

# Polymarket NegRisk Arbitrage Trader

> **This is a template.** The default signal is NegRisk price sum deviation from $1.00 —
> remix it with tighter thresholds, different min-profit floors, or additional liquidity filters.
> The skill handles all the plumbing (market discovery, grouping, batch execution, safeguards).
> Your agent provides the edge by tuning when and how aggressively to enter.

Scan multi-outcome markets for mathematical arbitrage opportunities. When the sum of all outcome prices deviates from $1.00, buy the mispriced side across all buckets simultaneously using Simmer's batch trade endpoint.

No signals. No AI. Just math.

## Strategy

Polymarket NegRisk markets have multiple mutually exclusive outcomes (e.g., election candidates, tweet count ranges). Exactly one outcome resolves YES = $1.00.

**The Math:**

In an efficient market:
```
sum(all YES prices) = $1.00
sum(all NO prices) = $1.00
```

When markets are inefficient:
```
sum(YES) < $0.95 → Buy ALL YES → guaranteed $1.00 payout, cost < $0.95 → profit
sum(NO)  < $0.95 → Buy ALL NO  → guaranteed $1.00 payout, cost < $0.95 → profit
```

**Example:**
```
Election market — 4 candidates:
  Candidate A: YES = $0.45
  Candidate B: YES = $0.22
  Candidate C: YES = $0.18
  Candidate D: YES = $0.08
  Sum = $0.93 (< $0.95 threshold)

→ Buy ALL YES for $0.93 total
→ One candidate wins → collect $1.00
→ Profit: $0.07 (7.5% return, risk-free)
```

## When to Use This Skill

- Multi-outcome Polymarket events (elections, tweet counts, sports brackets)
- When market makers are slow to rebalance after news
- High-volatility periods where prices shift quickly
- Events with many outcomes (more outcomes = more pricing errors)

## Setup

```bash
pip install simmer-sdk
export SIMMER_API_KEY="your-key-here"
```

## Quick Start

```bash
# Scan for opportunities (dry run, no trades)
python negrisk_arb.py

# Execute real trades
python negrisk_arb.py --live

# Only show YES arbitrage
python negrisk_arb.py --side yes

# Only show NO arbitrage  
python negrisk_arb.py --side no

# Set minimum profit threshold
python negrisk_arb.py --min-profit 0.05

# JSON output
python negrisk_arb.py --json

# Quiet mode for cron
python negrisk_arb.py --live --quiet

# Show stats
python negrisk_arb.py --stats

# Show config
python negrisk_arb.py --config

# Update config
python negrisk_arb.py --set max_position_usd=10.00
```

## Configuration

| Setting | Env Variable | Default | Description |
|---------|-------------|---------|-------------|
| max_yes_sum | SIMMER_NEGRISK_MAX_YES_SUM | 0.95 | Max sum of YES prices to trigger buy |
| max_no_sum | SIMMER_NEGRISK_MAX_NO_SUM | 0.95 | Max sum of NO prices to trigger buy |
| min_profit_pct | SIMMER_NEGRISK_MIN_PROFIT | 0.03 | Min profit % after fees (3%) |
| max_position_usd | SIMMER_NEGRISK_MAX_POSITION | 10.00 | Max USD per outcome bucket |
| max_total_usd | SIMMER_NEGRISK_MAX_TOTAL | 50.00 | Max total USD per event |
| max_trades_per_run | SIMMER_NEGRISK_MAX_TRADES | 2 | Max arbitrage events per cycle |
| daily_budget | SIMMER_NEGRISK_DAILY_BUDGET | 50.00 | Daily spend limit |
| min_outcomes | SIMMER_NEGRISK_MIN_OUTCOMES | 3 | Min outcomes per event (skip binary) |
| max_outcomes | SIMMER_NEGRISK_MAX_OUTCOMES | 15 | Max outcomes (too many = illiquid) |
| slippage_max_pct | SIMMER_NEGRISK_SLIPPAGE | 0.05 | Max slippage tolerance (5%) |
| fee_filter | SIMMER_NEGRISK_FEE_FILTER | true | Skip markets with fees |
| require_simultaneous | SIMMER_NEGRISK_SIMULTANEOUS | true | Use batch trades for simultaneous execution |

## How It Works

Each cycle the script:

1. **Fetch active markets** — GET /api/sdk/markets (all active, sorted by opportunity)
2. **Group by event** — Group markets sharing the same Polymarket event
3. **Calculate sums** — Sum YES prices and NO prices for each event group
4. **Filter opportunities** — Find events where sum < threshold
5. **Validate edge** — Check fee rates, slippage estimates, min profit after costs
6. **Execute batch** — POST /api/sdk/trades/batch with all buckets simultaneously
7. **Track positions** — Tag all trades with source: "sdk:negrisk-arb"

## Safeguards

- **Fee check** — Skips any event where any outcome has taker fees
- **Slippage check** — Estimates slippage via context API, skips if too high
- **Simultaneous execution** — Uses batch endpoint to minimize timing risk
- **Position check** — Skips events where you already hold positions
- **Daily budget** — Hard stop when daily limit is reached
- **Min outcomes** — Skips binary markets (YES + NO always = $1.00 by design)
- **Liquidity check** — Skips outcomes with very low volume (< $100 24h)

## Fee-Accurate Profit Calculation

```
yes_cost     = sum of all YES prices in cluster
payout       = $1.00 (exactly one resolves YES)
fee_cost     = sum of (price × fee_rate) for each outcome
net_profit   = payout - yes_cost - fee_cost
profit_pct   = net_profit / yes_cost
```

Only trades when `profit_pct >= min_profit_pct`.

## Simultaneous Execution (Critical)

Standard sequential trades are risky:
```
Buy outcome A → price moves → Buy outcome B → sum now > $1 → no longer profitable
```

This skill uses Simmer's batch endpoint:
```python
POST /api/sdk/trades/batch
{
  "trades": [
    {"market_id": "uuid-A", "side": "yes", "amount": 5.0},
    {"market_id": "uuid-B", "side": "yes", "amount": 5.0},
    {"market_id": "uuid-C", "side": "yes", "amount": 5.0}
  ],
  "venue": "polymarket",
  "source": "sdk:negrisk-arb"
}
```

All trades execute in parallel — minimizes timing risk.

## Example Output

```
🔢 NegRisk Arbitrage Scanner
==================================================

⚙️ Configuration:
  Max YES sum:     $0.95
  Max NO sum:      $0.95
  Min profit:      3.0%
  Max position:    $10.00/bucket
  Daily budget:    $50.00

🔍 Scanning 847 active markets...
  Grouped into 203 multi-outcome events
  Evaluating 203 events for arbitrage...

🎯 Opportunities Found: 2

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Event: "Who wins the 2026 German election?"
Side: YES arbitrage
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CDU/CSU:   $0.38
  SPD:       $0.27
  Greens:    $0.15
  AfD:       $0.09
  FDP:       $0.04
  ──────────────
  Sum:       $0.93 (< $0.95 threshold) ✅
  
  Profit calculation:
  Cost:      $0.93
  Payout:    $1.00
  Net:       +$0.07 (7.5%) ✅
  Fees:      $0.00 (zero-fee market) ✅
  Slippage:  ~1.2% (within limit) ✅

  Executing batch trade...
  ✅ CDU/CSU YES — 13.2 shares @ $0.38
  ✅ SPD YES     — 18.5 shares @ $0.27
  ✅ Greens YES  — 33.3 shares @ $0.15
  ✅ AfD YES     — 55.6 shares @ $0.09
  ✅ FDP YES     — 125.0 shares @ $0.04
  
  Total spent:   $4.65
  Expected gain: $0.35 (7.5%)

📊 Summary:
  Events scanned:    203
  Opportunities:     2
  Trades executed:   8 (batch)
  Total invested:    $9.30
  Expected profit:   $0.70
```

## Win Rate Tracking

The skill tracks every arbitrage in `negrisk_ledger.json`:
- Entry prices and total cost
- Winning outcome after resolution
- Actual profit vs expected
- Slippage impact

Run `--stats` after 20+ events to see real performance vs theoretical edge.

## Troubleshooting

**"No arbitrage opportunities found"**
- Markets may be efficiently priced right now
- Try lowering `min_profit_pct` to 0.02
- Check during high-volatility periods (election night, major events)

**"All events skipped for fees"**
- Only zero-fee markets are traded
- Set `fee_filter=false` to override (not recommended)

**"Batch trade partially filled"**
- Some outcomes may have thin liquidity
- Reduce `max_position_usd` to reduce market impact
- Increase `slippage_max_pct` slightly

**"Sum check passed but trade rejected"**
- Prices moved between scan and execution
- Normal in fast-moving markets
- Skill will retry on next cycle

**"Event has too many outcomes"**
- Increase `max_outcomes` setting
- Or skip — very fragmented markets often have liquidity issues

## API Endpoints Used

- `GET /api/sdk/markets` — Market list with prices and divergence
- `GET /api/sdk/context/{market_id}` — Fee rates and slippage estimates
- `POST /api/sdk/trades/batch` — Simultaneous multi-outcome execution
- `GET /api/sdk/positions` — Current portfolio positions
- `GET /api/sdk/portfolio` — Balance and daily spend tracking

## Cron / Automaton Setup

```json
"automaton": {
  "managed": true,
  "entrypoint": "negrisk_arb.py --live --quiet",
  "cron": "0 */2 * * *"
}
```

Runs every 2 hours. Arbitrage windows can be short — more frequent scanning catches more opportunities.

Or via OpenClaw native cron:
```bash
openclaw cron add \
  --name "NegRisk Arbitrage" \
  --cron "0 */2 * * *" \
  --session isolated \
  --message "Run NegRisk arbitrage scan: cd /path/to/skill && python negrisk_arb.py --live --quiet. Show summary." \
  --announce
```

## Important Notes

- This is mathematical arbitrage, not prediction — you don't need to know who wins
- Works best on events with 4+ outcomes (more outcomes = more pricing errors)
- Elon Tweet markets are a special case of this strategy (you're already doing it!)
- Opportunities are rare but high-confidence when found
- Always verify the batch filled completely before assuming profit is locked
