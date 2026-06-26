# Global Market Intelligence Skill

A comprehensive market intelligence tool for OpenClaw that provides real-time global market data, news aggregation, geopolitical event monitoring, and AI-powered market analysis with a focus on Indian and global stock markets.

## 🚀 Quick Start

```bash
# SUPER COMMAND - Get EVERYTHING in one command! ⭐
uv run --script scripts/market_analysis.py all

# Or individual commands:

# Get global market overview
uv run --script scripts/market_analysis.py overview

# Analyze Indian market
uv run --script scripts/market_analysis.py india

# Generate comprehensive report
uv run --script scripts/market_analysis.py report

# Get latest market news
uv run --script scripts/market_analysis.py news
```

## 📊 Features

### 1. **Real-Time Market Data**
- Global indices (US, Europe, Asia, India)
- Commodities (Gold, Silver, Oil)
- Currency pairs (USD/INR, EUR/USD, etc.)
- Individual stock tracking

### 2. **News Aggregation**
- Yahoo Finance
- Moneycontrol
- Economic Times
- Business Standard
- Reuters

### 3. **Geopolitical Monitoring**
- Central bank decisions (Fed, RBI, ECB, BoJ)
- Elections and political events
- Trade wars and tariffs
- Regional conflicts
- Economic sanctions

### 4. **Market Analysis**
- Sentiment analysis
- Sector performance
- Intermarket correlations
- VIX fear gauge
- Support/resistance levels

### 5. **Indian Market Focus**
- NIFTY 50 & SENSEX tracking
- Top gainers/losers
- Sector-wise analysis
- FII/DII activity (when available)

## 🎯 Use Cases

### For Day Traders
```bash
# Quick market overview before market open
uv run --script scripts/market_analysis.py overview

# Monitor specific stocks
uv run --script scripts/market_analysis.py watchlist RELIANCE.NS TCS.NS INFY.NS
```

### For Long-Term Investors
```bash
# Weekly comprehensive report
uv run --script scripts/market_analysis.py report

# Sector rotation analysis
uv run --script scripts/market_analysis.py sectors --india
```

### For Risk Managers
```bash
# Geopolitical risk monitoring
uv run --script scripts/market_analysis.py geopolitical

# Intermarket correlations
uv run --script scripts/market_analysis.py intermarket
```

## 📖 Command Reference
### `all` ⭐⭐⭐ SUPER COMMAND
Execute all commands for complete market intelligence with advanced analytics.

**Includes 9 comprehensive sections:**
1. Global market overview
2. Indian market deep dive with ASCII price charts
3. **Probability & Technical Analysis** (RSI, Momentum, Volatility)
4. **Risk Assessment Dashboard** (1-10 risk score with visual gauge)
5. Sector performance analysis
6. Intermarket correlations
7. Geopolitical events & VIX
8. Latest news (Indian + Global)
9. **Market Outlook & Decision Support** (Trading matrix, recommendations)

**Advanced Analytics:**
- ✅ Probability predictions (Bullish/Bearish %)
- ✅ Risk scoring system with visual gauges
- ✅ Technical indicators (RSI, Momentum, Volatility)
- ✅ ASCII price charts
- ✅ Trading decision matrix
- ✅ Position sizing guidelines
- ✅ Stop loss calculations

**Execution time:** ~20-25 seconds
### `overview`
Global market snapshot with all major indices, commodities, and currencies.

### `india`
Detailed Indian market analysis with NIFTY/SENSEX data and top movers.

### `news [--india] [--geopolitical] [--ticker SYMBOL]`
Fetch latest market news with optional filters.

### `geopolitical`
Monitor geopolitical events and VIX fear index.

### `report [--region global|india|us]`
Generate comprehensive market intelligence report.

### `sectors [--india]`
Sector performance analysis.

### `intermarket`
Analyze correlations between stocks, bonds, commodities, and currencies.

### `watchlist SYMBOL1 SYMBOL2 ...`
Monitor custom list of symbols.

## 📈 Interpreting the Data

### Market Sentiment
- **BULLISH**: Average change > +1%
- **NEUTRAL**: Average change between -1% and +1%
- **BEARISH**: Average change < -1%

### VIX Levels
- **< 15**: Low volatility, calm markets
- **15-25**: Moderate volatility
- **> 25**: High volatility, fear in markets

### Color Coding
- 🟢 **Green**: Positive changes
- 🔴 **Red**: Negative changes
- 🟡 **Yellow**: Warnings or neutral

## 🔍 Ticker Symbols

### Indian Market
- `^NSEI` - NIFTY 50
- `^NSEBANK` - NIFTY Bank
- `^BSESN` - BSE SENSEX
- `RELIANCE.NS` - Reliance Industries
- `TCS.NS` - Tata Consultancy Services
- `INFY.NS` - Infosys

### Global Indices
- `^GSPC` - S&P 500
- `^DJI` - Dow Jones
- `^IXIC` - NASDAQ
- `^FTSE` - FTSE 100
- `^N225` - Nikkei 225
- `^HSI` - Hang Seng

## 🛠️ Technical Details

### Data Sources
- **Yahoo Finance**: Primary source for market data
- **RSS Feeds**: News aggregation from trusted sources
- **yfinance API**: Real-time and historical data

### Dependencies
All dependencies are automatically managed via PEP 723:
- yfinance
- pandas
- rich
- requests
- beautifulsoup4
- feedparser
- numpy

### Performance
- Typical response time: 2-5 seconds
- Concurrent data fetching for speed
- Caching where appropriate

## 🚨 Important Notes

### Disclaimers
⚠️ **NOT FINANCIAL ADVICE**: This tool is for informational purposes only. Always consult qualified financial advisors before making investment decisions.

⚠️ **Data Accuracy**: Market data is sourced from public APIs and may have delays. Verify critical information from official sources.

⚠️ **Rate Limits**: Respect API rate limits. Excessive requests may result in temporary blocks.

### Limitations
- News aggregation depends on RSS feed availability
- Some international markets may have limited data
- Real-time data may have 15-minute delays for some exchanges
- FII/DII data requires additional APIs (not included)

## 🎨 Customization

### Adding Custom Indices
Edit `market_analysis.py` and add to `GLOBAL_INDICES`:

```python
"Custom Region": {
    "^SYMBOL": "Index Name"
}
```

### Adding News Sources
Edit `news_fetcher.py` and add to `NEWS_SOURCES`:

```python
"source_id": {
    "name": "Source Name",
    "rss": "https://feed-url.com/rss",
    "category": "india|global"
}
```

## 📝 Examples

### Morning Routine
```bash
# BEST: Complete analysis with super command
uv run --script scripts/market_analysis.py all

# OR quick version for time-sensitive checks
uv run --script scripts/market_analysis.py overview
uv run --script scripts/market_analysis.py india
```

### Risk Assessment
```bash
# 1. Check VIX and geopolitical events
uv run --script scripts/market_analysis.py geopolitical

# 2. Analyze intermarket relationships
uv run --script scripts/market_analysis.py intermarket

# 3. Generate full report
uv run --script scripts/market_analysis.py report
```

## 🤝 Contributing

Feel free to extend this skill with:
- Additional data sources
- More technical indicators
- Enhanced news filtering
- Portfolio tracking features
- Alert systems

## 📄 License

This skill uses publicly available data and open-source libraries. Respect the terms of service of all data providers.

---

**Made with ❤️ for OpenClaw**

*Stay informed. Trade wisely. Manage risk.*
