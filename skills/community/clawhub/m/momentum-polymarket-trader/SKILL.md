---
name: momentum-polymarket-trader
description: Automated Polymarket trading skill based on price momentum signals—executes trades when market trends are detected
metadata:
  author: "AION Trader"
  version: "1.0.0"
  displayName: "Momentum Polymarket Trader"
  difficulty: "intermediate"
---

# Momentum Polymarket Trader

An automated trading skill that executes trades on Polymarket based on price momentum and market trend signals.

## Features

- 🎯 Automatically monitors opportunity markets on Polymarket
- 📊 Analyzes price momentum and trend signals
- ⚠️ Built-in risk management and flip-flop detection
- 🔄 Auto-redeems winnings from resolved markets
- 📝 Detailed reasoning logs for every trade

## How It Works

This skill runs every 15 minutes and:

1. **Fetches Market Briefing** - Gets current opportunity markets from AION API
2. **Risk Check** - Checks for risk alerts; pauses trading if any exist
3. **Market Analysis** - For each candidate market:
   - Fetches market context and trading discipline data
   - Calculates price momentum indicators
   - Evaluates trading edge
4. **Executes Trades** - Trades when positive edge is found with no warnings
5. **Auto-Redeems** - Periodically redeems winnings from resolved markets

## Remixable Template

> **This is a customizable template.** The default signal is based on simple price momentum — 
> you can replace it with:
> - Different technical indicators (RSI, MACD, etc.)
> - Machine learning model predictions
> - External data sources (news, social media sentiment, etc.)
> - Custom market scoring algorithms
> 
> The skill handles all the plumbing (market discovery, order execution, position management, safeguards).
> Your agent provides the alpha — just replace the `calculate_signal()` function.

## Configuration

### Required Environment Variables
- `AION_API_KEY` - Your AION SDK API key (get from https://pm-t1.bxingupdate.com/agents)

### Optional Environment Variables
- `WALLET_PRIVATE_KEY` - Only needed for external-wallet self-custody trading
- `POLYGON_RPC_URL` - Custom Polygon RPC endpoint (optional)
- `MAX_POSITION_SIZE` - Maximum position per market (default: 10 USDC)
- `MIN_EDGE_THRESHOLD` - Minimum edge threshold for trading (default: 0.05, i.e., 5%)

## Running Modes

### Dry-run Mode (Default)
```bash
python momentum_trader.py
```
This simulates trades without executing real orders.

### Live Trading Mode
```bash
python momentum_trader.py --live
```
⚠️ **Warning**: This executes trades with real funds!

## Customizing Signals

Edit the `calculate_signal()` function in `momentum_trader.py` to implement your trading strategy:

```python
def calculate_signal(market_data, context):
    """
    Replace this function to implement your custom signal logic
    
    Returns:
    - side: "yes" or "no" or None (no trade)
    - confidence: confidence level between 0-1
    - reasoning: human-readable trade rationale
    """
    # Your custom logic here
    pass
```

## Risk Management

This skill includes multiple layers of protection:

1. **Flip-flop detection** - Avoids frequent position reversals
2. **Slippage estimation** - Reduces trade size in high-slippage markets
3. **Risk alert checks** - Pauses trading when account-level risks are detected
4. **Position limits** - Maximum exposure per market
5. **Edge validation** - Only trades when expected edge exceeds threshold

## Monitoring & Logs

Skill output includes:
- Risk status summary
- Decision for each market (TRADE, HOLD, SKIP)
- Position changes and order updates
- Trade execution results

## Example Output

```
======================================================================
Skill: momentum-polymarket-trader
Venue: polymarket (USDC.e)

Risk alerts:
- none

Decisions:
- "Will Bitcoin reach $100K in 2025?": HOLD (edge too small +2.1%)
- "2026 US Midterm Elections": TRADE YES size=5 reason=momentum signal +7.8%
- "OpenAI valuation over $300B?": SKIP (flip-flop warning)

Order updates:
- cancelled ORDER_123 (stale)
- new order ORDER_456 submitted

Auto-redemptions:
- redeemed market MKT_789: tx=0xabc...def
```

## Technical Details

- **Polling interval**: 15 minutes (with random jitter to avoid synchronization)
- **Dependencies**: aion-sdk, requests
- **Python version**: 3.8+
- **Network**: Polygon (USDC.e)

## Troubleshooting

### "No opportunity markets found"
Check your AION agent settings for risk thresholds and market filters.

### "Invalid API key"
Ensure the `AION_API_KEY` environment variable is set correctly.

### "Insufficient balance"
Check your wallet balance at https://pm-t1.bxingupdate.com/agents

## Next Steps

1. Install skill: `npx clawhub@latest install momentum-polymarket-trader`
2. Configure your `AION_API_KEY`
3. Test in dry-run mode
4. Customize signal logic
5. Switch to live mode (use caution!)

## License

MIT License - free to use, modify, and distribute.
