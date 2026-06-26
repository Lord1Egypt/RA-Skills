# Momentum Polymarket Trader

A complete AION automated trading skill that executes trades on Polymarket based on price momentum signals.

## 📁 File Structure

```
momentum-polymarket-trader/
├── SKILL.md              # AION skill specification and documentation
├── clawhub.json          # ClawHub configuration and automation settings
├── momentum_trader.py    # Main trading logic
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
export AION_API_KEY="your-api-key"  # Get from https://pm-t1.bxingupdate.com/agents
```

Optional configuration:
```bash
export MAX_POSITION_SIZE="10.0"      # Max trade amount per market (USDC)
export MIN_EDGE_THRESHOLD="0.05"     # Minimum trading edge (5%)
```

### 3. Test Run (Dry-run Mode)

```bash
# Single execution
python momentum_trader.py

# Continuous mode
python momentum_trader.py --continuous
```

### 4. Live Trading (⚠️ Use Caution)

```bash
# Single live trade
python momentum_trader.py --live

# Continuous live trading
python momentum_trader.py --live --continuous
```

## 🎯 Features

- ✅ **Auto Market Discovery** - Monitors AION-recommended opportunity markets
- ✅ **Momentum Signal Detection** - Identifies trading opportunities based on price trends
- ✅ **Multi-layer Risk Management** - Flip-flop detection, slippage estimation, risk alerts
- ✅ **Auto-Redemption** - Periodically redeems winnings from resolved markets
- ✅ **Detailed Logging** - Records all decisions and trade reasoning
- ✅ **Customizable Template** - Easy to replace with your own trading signals

## 🔧 Customizing Strategy

Edit the `calculate_signal()` function in `momentum_trader.py`:

```python
def calculate_signal(market: Dict, context: Dict) -> Signal:
    """
    Implement your custom trading strategy here!
    
    You can use:
    - Technical indicators (RSI, MACD, Bollinger Bands, etc.)
    - Machine learning models
    - External data sources (news, social media sentiment, etc.)
    - Any other signal logic
    """
    # Your strategy code...
    pass
```

## 📊 Example Output

```
======================================================================
Skill: momentum-polymarket-trader
Venue: polymarket
Mode: DRY-RUN (simulation)
======================================================================

🔄 Checking for positions to redeem...
✓ Redeemed market abc123...: tx=0xdef456...

📊 Fetching market briefing...
✓ No risk alerts

🎯 Found 5 opportunity markets

Analyzing: Will Bitcoin reach $100K in 2025?...
  • HOLD: No clear momentum signal (YES=0.520, NO=0.480)

Analyzing: 2026 US Midterm Elections...
  💰 TRADE YES: Edge 7.8%
  [DRY-RUN] Simulating trade: YES 6.5 USDC
  Reason: Positive momentum detected for YES (current price=0.680)

======================================================================
Execution Summary
======================================================================
Auto-redeemed: 1 positions
Markets analyzed: 5
Trades executed: 1
Hold decisions: 3
Markets skipped: 1
======================================================================
```

## 📦 Publishing to ClawHub

### 1. Publish Skill

```bash
npx clawhub@latest publish . --slug momentum-polymarket-trader --version 1.0.0
```

### 2. Verify Installation

```bash
npx clawhub@latest install momentum-polymarket-trader
```

### 3. Wait for Sync

The skill will automatically appear in the AION registry within 6 hours: https://pm-t1.bxingupdate.com/agents

### 4. Update Skill

```bash
npx clawhub@latest publish . --slug momentum-polymarket-trader --bump patch
```

## ⚠️ Risk Disclaimer

1. **This is an educational template** - The default momentum strategy is very simple, for demonstration only
2. **Requires customization** - You should implement your own trading logic and signals
3. **Live trading risks** - May result in loss of funds, use with caution
4. **Test thoroughly** - Test extensively in dry-run mode before live trading
5. **Position management** - Set reasonable `MAX_POSITION_SIZE` to limit risk exposure

## 🛠️ Troubleshooting

### Issue: `No opportunity markets found`
**Solution**: Check AION agent settings for market filters and risk thresholds

### Issue: `Invalid API key`
**Solution**: Ensure `AION_API_KEY` environment variable is set correctly

### Issue: `Insufficient balance`
**Solution**: Check wallet balance at https://pm-t1.bxingupdate.com/agents and top up

### Issue: `Failed to import aion_sdk`
**Solution**: Run `pip install aion-sdk`

## 📚 Related Resources

- [AION Documentation](https://docs-t.aionmarket.com/)
- [Building Skills Guide](https://docs-t.aionmarket.com/essentials/building-skills)
- [ClawHub Documentation](https://clawhub.com/docs)
- [Polymarket API](https://docs.polymarket.com/)

## 📝 License

MIT License - free to use, modify, and distribute

## 🤝 Contributing

Issues and pull requests are welcome to improve this skill template!

---

**Note**: This is a customizable template skill. The skill handles all infrastructure (market discovery, order execution, position management, safeguards) - you just provide the trading signal (alpha).
