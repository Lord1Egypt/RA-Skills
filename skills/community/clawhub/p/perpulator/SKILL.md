---
name: perpulator
description: Analyze perpetual futures positions directly in Claude Code — liquidation price, risk/reward, PnL, and probability-based trade plans. Powered by Perpulator.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - PERPULATOR_API_KEY
      bins:
        - curl
    primaryEnv: PERPULATOR_API_KEY
    emoji: "📊"
    homepage: https://perpulator.vercel.app
---

You are running the **Perpulator** skill — a perpetual futures position analyzer powered by the Perpulator API.

## Step 1 — Get the API key

Check for the environment variable `PERPULATOR_API_KEY` using the Bash tool:
```bash
echo $PERPULATOR_API_KEY
```

If it is empty or unset, tell the user:
> "No API key found. Set it with: `export PERPULATOR_API_KEY=perp_...`
> Generate one free at https://perpulator.vercel.app/settings (sign in → create a key)"

Stop here if no key is available.

## Step 2 — Parse position parameters

Extract the following from the user's message:

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `symbol` | Yes | Asset ticker | `BTC`, `ETH`, `SOL` |
| `side` | Yes | Direction | `long` or `short` |
| `entryPrice` | Yes | Entry price in USD | `71000` |
| `positionSize` | Yes | Margin in USD (not notional) | `1000` |
| `leverage` | Yes | Multiplier (1–125) | `10` |
| `stopLoss` | Optional | Stop loss price | `65000` |
| `takeProfit` | Optional | Take profit price | `80000` |
| `currentPrice` | Optional | Current market price for live PnL | `71500` |

Accept flexible input formats:
- Leverage: `10`, `10x`, `10X` → always convert to number `10`
- Side: `long`, `LONG`, `buy` → `"long"` | `short`, `SHORT`, `sell` → `"short"`
- SL/TP labels: `SL:`, `stop:`, `sl`, `stop loss` → `stopLoss` | `TP:`, `target:`, `tp`, `take profit` → `takeProfit`

If any required parameter is missing, ask the user for it before proceeding.

## Step 3 — Call the Perpulator API

Build and execute the curl command with real values substituted (no placeholders). Always include `X-Perpulator-Client: perpulator/1.0` so the server can identify this as a Perpulator skill request.

Example for BTC long at 71000, size 1000, 10x, SL 65000, TP 82000:

```bash
curl -s -X POST https://perpulator.vercel.app/api/v1/calculate \
  -H "Authorization: Bearer $PERPULATOR_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-Perpulator-Client: perpulator/1.0" \
  -d '{"symbol":"BTC","side":"long","entryPrice":71000,"positionSize":1000,"leverage":10,"stopLoss":65000,"takeProfit":82000}'
```

Omit `stopLoss`, `takeProfit`, and `currentPrice` from the JSON if the user didn't provide them.

## Step 4 — Format the result

Parse the JSON response and present a clean analysis:

---

**Perpulator Analysis — {SYMBOL} {SIDE}**

| | |
|---|---|
| Entry Price | `${entryPrice}` |
| Margin | `${positionSize}` |
| Leverage | `{leverage}x` |
| Notional Size | `${notionalSize}` |
| Liquidation Price | `${liquidationPrice}` |
| Stop Loss | `${stopLoss}` *(if provided)* |
| Take Profit | `${takeProfit}` *(if provided)* |
| Risk Amount | `${riskAmount}` *(if SL set)* |
| Reward Amount | `${rewardAmount}` *(if TP set)* |
| Risk/Reward | `{riskRewardRatio}:1` *(if both set)* |
| Current PnL | `${pnl} ({pnlPercentage}%)` *(if currentPrice set)* |

Then add a one-sentence risk note:
> "At {leverage}x leverage, a {pct}% adverse move triggers liquidation."
> (pct = `|(entryPrice - liquidationPrice) / entryPrice * 100|`, rounded to 2 decimal places)

---

If the API returns an error, show the error message clearly and suggest how to fix it.

## Valid invocation examples

```
/perpulator BTC long 71000 1000 10x SL:65000 TP:82000
/perpulator ETH short 3200 500 5x stop 3400 target 2800 current 3180
/perpulator SOL long 145 200 20x
/perpulator analyze my BTC long: entry 71000, size $1000, 10x leverage, stop at 65000
```
