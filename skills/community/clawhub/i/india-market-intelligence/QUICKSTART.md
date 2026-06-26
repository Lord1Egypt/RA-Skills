# Quick Reference Guide - Global Market Intelligence

## 🚀 Most Common Commands

### 🌟 Super Command (ALL Data + Advanced Analytics)
```bash
uv run --script scripts/market_analysis.py all
```
**The ultimate command - 9 sections with probability analysis, risk scoring, charts, and trading decisions!**

**Includes:**
- 📊 ASCII price charts
- 🎯 Probability predictions
- ⚠️ Risk assessment (1-10 score)
- 📈 Technical indicators
- 💡 Trading decision matrix

### Daily Market Check
```bash
uv run --script scripts/market_analysis.py overview
```

### Indian Market Focus
```bash
uv run --script scripts/market_analysis.py india
```

### Latest News
```bash
uv run --script scripts/market_analysis.py news
```

### Full Report
```bash
uv run --script scripts/market_analysis.py report
```

---

## 🎯 Cheat Sheet

| Command | Purpose | Time to Run |
|---------|---------|-------------|
| `all` ⭐ | **Complete intelligence + Advanced Analytics** | ~20-25s |
| `overview` | Quick global market snapshot | ~3s |
| `india` | Detailed Indian market analysis | ~4s |
| `news` | Latest headlines | ~5s |
| `geopolitical` | Risk events monitoring | ~5s |
| `report` | Complete intelligence report | ~8s |
| `sectors --india` | Indian sector performance | ~4s |
| `intermarket` | Asset correlation analysis | ~3s |
| `watchlist SYMBOL1 SYMBOL2` | Track specific stocks | ~2s |

---

## 📊 Key Symbols to Know

### Must-Track Indices
```
^NSEI        - NIFTY 50 (Indian blue chips)
^BSESN       - BSE SENSEX (India)
^GSPC        - S&P 500 (US large cap)
^IXIC        - NASDAQ (US tech)
^VIX         - Volatility/Fear Index
```

### Important Commodities
```
GC=F         - Gold (safe haven)
CL=F         - Crude Oil WTI (inflation indicator)
USDINR=X     - USD/INR (rupee strength)
```

### Top Indian Stocks
```
RELIANCE.NS  - Reliance Industries
TCS.NS       - Tata Consultancy Services
INFY.NS      - Infosys
HDFCBANK.NS  - HDFC Bank
```

---

## 💡 Pro Tips

### 1. Market Open Routine
```bash
# BEST: Use super command for complete analysis
uv run --script scripts/market_analysis.py all

# OR quick version before Indian market opens (9:00 AM IST)
uv run --script scripts/market_analysis.py overview
uv run --script scripts/market_analysis.py news --india
```

### 2. Risk Check
```bash
# Check for high-risk events
uv run --script scripts/market_analysis.py geopolitical
# If VIX > 25, reduce position sizes!
```

### 3. Weekly Analysis
```bash
# Every Sunday evening - SUPER COMMAND!
uv run --script scripts/market_analysis.py all

# OR individual commands
uv run --script scripts/market_analysis.py report
uv run --script scripts/market_analysis.py sectors --india
```

### 4. Track Portfolio
```bash
# Monitor your holdings
uv run --script scripts/market_analysis.py watchlist TCS.NS INFY.NS RELIANCE.NS HDFCBANK.NS
```

### 5. News Filtering
```bash
# India-specific news only
uv run --script scripts/market_analysis.py news --india

# Geopolitical events only
uv run --script scripts/market_analysis.py news --geopolitical

# News for specific stock
uv run --script scripts/market_analysis.py news --ticker AAPL
```

---

## 🚨 Warning Signals

### High Risk Indicators
- ⚠️ VIX > 30 → Very high volatility
- ⚠️ Major index down > 2% → Strong selling
- ⚠️ Dollar Index up sharply → Emerging markets under pressure
- ⚠️ Crude oil up > 5% → Inflation concerns
- ⚠️ Multiple negative headlines → Sentiment shift

### Opportunity Indicators
- ✅ VIX < 15 → Calm markets, good for risk-taking
- ✅ Major indices up > 1% → Bullish momentum
- ✅ Gold declining → Risk-on sentiment
- ✅ Positive sector rotation → Healthy market

---

## 🎓 Understanding Output

### Color Codes
- **Green** = Positive/Up/Bullish
- **Red** = Negative/Down/Bearish
- **Yellow** = Warning/Neutral
- **Cyan** = Information/Titles

### Sentiment Levels
- **BULLISH**: Avg change > +1% (Buy opportunity)
- **NEUTRAL**: Avg change -1% to +1% (Wait and watch)
- **BEARISH**: Avg change < -1% (Caution/hedge)

### VIX Interpretation
- **0-15**: Low volatility (normal market)
- **15-25**: Moderate volatility (some uncertainty)
- **25-40**: High volatility (major concerns)
- **40+**: Extreme fear (potential panic)

---

## ⚡ Quick Troubleshooting

### No data showing?
```bash
# Check internet connection
# Some feeds may be temporarily down
# Try again in a few minutes
```

### Slow response?
```bash
# Normal for comprehensive report (8-10s)
# Network speed dependent
# Use simpler commands for quick checks
```

### Wrong symbols?
```bash
# Indian stocks need .NS suffix (e.g., TCS.NS)
# US stocks are plain symbols (e.g., AAPL)
# Indices start with ^ (e.g., ^NSEI)
```

---

## 📱 Mobile Workflow

If accessing from mobile terminal:
```bash
# Use short commands
uv run --script scripts/market_analysis.py overview
uv run --script scripts/market_analysis.py india

# Avoid heavy commands like full report
# Use targeted queries instead
```

---

## 🔔 Creating Alerts (Manual)

While automated alerts aren't built-in, you can:

1. Set calendar reminder for daily market check
2. Run `overview` before market hours
3. Check `geopolitical` on Sundays
4. Monitor `watchlist` for your holdings

---

## 📖 Learn More

- Full documentation: See SKILL.md
- Technical details: See README.md
- Source code: Check scripts/ folder

---

**Remember**: This tool provides information, not advice. Always do your own research! 📚

*Happy Trading! 🚀*
