---
name: polymarket-valuation-divergence
displayName: Polymarket Valuation Divergence
description: Trade Polymarket markets based on valuation divergence. When your probability model differs from Polymarket's price by >threshold, enter using Kelly sizing. Works with any probability model (Simmer AI consensus, user model, external API).
metadata: {"clawdbot":{"emoji":"💹","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":true,"entrypoint":"valuation_trader.py"}}}
authors:
  - Simmer (@simmer_markets)
version: "1.0.0"
published: false
---

# Polymarket Valuation Divergence Trader

Trade markets where model probability diverges from Polymarket price.

> **This is a template.** The default uses Simmer AI consensus as your probability model. Remix it with your own model, external APIs, or custom forecasting logic. The skill handles market scanning, Kelly sizing, and safe trade execution.

## When to Use This Skill

Use this when:
- You have a probability model (AI, statistical, fundamental analysis)
- You want to trade when market prices diverge from your model
- You need Kelly criterion sizing for risk management
- You want to catch structural mispricings (mergers, earnings, regulatory events)

## Quick Start

### Setup

1. **Set your API key:**
   ```bash
   export SIMMER_API_KEY=sk_live_...
   ```

2. **Check config:**
   ```bash
   python valuation_trader.py --config
   ```

3. **Dry run (no trades):**
   ```bash
   python valuation_trader.py
   ```

4. **Live trading:**
   ```bash
   python valuation_trader.py --live
   ```

### Configuration

| Setting | Env Var | Default | Description |
|---------|---------|---------|-------------|
| edge_threshold | `SIMMER_VALUATION_EDGE` | 0.015 | Min edge to trade (1.5%) |
| kelly_fraction | `SIMMER_VALUATION_KELLY` | 0.25 | Kelly criterion fraction (cap at 25%) |
| max_position_usd | `SIMMER_VALUATION_MAX_POSITION` | 5.00 | Max per trade |
| max_trades_per_run | `SIMMER_VALUATION_MAX_TRADES` | 5 | Max trades per cycle |
| probability_source | `SIMMER_VALUATION_SOURCE` | simmer_ai | "simmer_ai" or "user_model" |

**Update settings:**
```bash
python valuation_trader.py --set edge_threshold=0.02
```

## How It Works

### 1. Scan Markets

Fetches active markets from Simmer. For each:

### 2. Get Model Probability

Default: **Simmer AI consensus** from `/api/sdk/context/{market_id}`

To use your own model: Edit `get_model_probability()` function.

### 3. Calculate Edge

```
edge = model_probability - market_price
```

If `edge > threshold`: trade signal ✓

### 4. Kelly Sizing

```
kelly_fraction = edge / (1 - market_price)
kelly_fraction = min(kelly_fraction, MAX_KELLY)
position_size = kelly_fraction * bankroll
position_size = min(position_size, max_position_usd)
```

### 5. Execute Trade

- **If edge > 0:** Buy YES (model thinks it's underpriced)
- **If edge < 0:** Buy NO (model thinks it's overpriced)
- Include reasoning for transparency
- Execute with safeguards (flip-flop detection, slippage warnings)

### 6. Hold to Resolution

Positions held until market resolves. Check `--positions` to see current holdings.

## Interpreting the Output

```
🎯 Valuation Trader Scan
   Markets scanned: 50
   Signals found: 3
   Executed: 2

📰 BTC hits $100k by EOY?
   Model: 65% | Market: 52% | Edge: +13%
   💰 BUY YES $4.50 (Kelly: 2.25 shares)

📰 Will Trump win in 2028?
   Model: 58% | Market: 71% | Edge: -13%
   💰 BUY NO $3.75 (Kelly: 2.05 shares)
```

## Customizing Your Model

Edit `get_model_probability()` to use any source:

**Option 1: User-provided probabilities (config)**
```python
def get_model_probability(market_id, market_question):
    # Return fixed probability from config
    return USER_PROBABILITIES.get(market_id)
```

**Option 2: External API (e.g., Synth, Metaculus)**
```python
def get_model_probability(market_id, market_question):
    # Fetch forecast from external API
    resp = fetch_json(f"{EXTERNAL_API}/forecast?q={market_question}")
    return resp["probability"]
```

**Option 3: Rules-based model**
```python
def get_model_probability(market_id, market_question):
    if "crypto" in market_question.lower():
        return 0.55  # Crypto has historical upside
    elif "election" in market_question.lower():
        return 0.50  # No strong signal on elections
    return None  # Skip if no model
```

## Commands

```bash
# Dry run (simulate trades, no real execution)
python valuation_trader.py

# Live trading
python valuation_trader.py --live

# Show current positions
python valuation_trader.py --positions

# Show config
python valuation_trader.py --config

# Update config
python valuation_trader.py --set edge_threshold=0.02

# Quiet mode (cron-friendly)
python valuation_trader.py --live --quiet
```

## Risk Management

- **Position size cap:** `max_position_usd` limits each trade
- **Kelly fraction cap:** Limited to 25% of bankroll (never bet >25% on one trade)
- **Trade limit:** `max_trades_per_run` prevents over-trading
- **Safeguards:** Simmer SDK checks for flip-flop warnings, slippage, expiring positions
- **--no-safeguards:** Skip checks (use only if you know what you're doing)

## Troubleshooting

**"No signals found"**
- Model probabilities and market prices are close
- Increase `edge_threshold` in config if too conservative
- Check your model source — is it generating probabilities?

**"Markets scanned: 0"**
- No active markets available
- Try during peak market hours

**"Edge is negative but we're buying YES"**
- This is correct! Edge < 0 means market is overpriced. Buy NO instead (which we do).

**"Flip-flop warning: CAUTION"**
- You recently changed direction on this market
- Discipline tracking prevents over-trading. Wait or use `--no-safeguards`.

## Performance Metrics

Check your performance:
```bash
python valuation_trader.py --positions
```

Shows: realized P&L, win rate, average edge per trade, largest positions.

## When This Works Best

1. **Structural mispricings:** Merger arb, earnings surprises, regulatory news
2. **Consensus divergence:** Market hasn't caught up to known information
3. **Model > crowd:** Your probability model is better than crowd estimates
4. **Short-dated markets:** Errors correct faster

## When This Doesn't Work

1. **Crowd is right:** Market prices reflect true probabilities
2. **Model is calibrated wrong:** Your probability estimates are worse than market
3. **Latency:** By the time you execute, price moved against you
4. **Liquidity:** Slippage eats the edge on illiquid markets

---

**Start small.** Test with dry-run first. Verify your model against historical outcomes. Then go live with small position sizes.
