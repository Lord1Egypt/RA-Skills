# TradingView Quantitative Investment Analysis Skill for OpenClaw

[![Install with skills](https://img.shields.io/badge/install-skills-blue)](https://skills.sh/ljsd666/openclaw-tradingview-quant/openclaw-tradingview-quant)
[![GitHub](https://img.shields.io/github/stars/ljsd666/openclaw-tradingview-quant?style=social)](https://github.com/ljsd666/openclaw-tradingview-quant)

Professional quantitative investment analysis guidance system based on TradingView API data structures, providing intelligent stock screening, technical pattern recognition, market review, risk management, and event-driven analysis frameworks and methodologies.

## Highlights

✨ **Ready to Use** - No configuration required, install and start using
🔒 **Safe and Secure** - No API keys needed, no external dependencies
📚 **Professional Methodologies** - Analysis frameworks based on real API data structures
🎯 **Practical Oriented** - Actionable analysis guidance and strategy recommendations

## Installation

Install this skill with one command:

```bash
npx skills add ljsd666/openclaw-tradingview-quant
```

## Features

- ✅ **Smart Stock Screening Framework** - Multi-factor comprehensive scoring methodology, dual filtering strategies for technical + fundamental aspects
- 📊 **Technical Pattern Recognition** - Classic pattern recognition algorithms, confidence assessment and trading strategy guidance
- 📈 **Market Review Methods** - Hot sector tracking, capital flow analysis frameworks
- 🛡️ **Risk Management System** - Position management, stop-loss/take-profit, volatility analysis methodologies
- 📰 **Event-Driven Analysis** - Market impact analysis frameworks for earnings, policies, and news
- 🔍 **Deep Individual Stock Analysis** - Multi-timeframe technical analysis + fundamentals + news comprehensive evaluation methods
- 💰 **Fundamental Screening** - High dividend, low valuation, profitability screening strategies
- 🔄 **Sector Rotation Analysis** - Strong sector identification and rotation trend analysis methods

## Quick Start

### 1. Install the Skill

```bash
npx skills add ljsd666/openclaw-tradingview-quant
```

### 2. Start Using

Just ask questions in natural language, for example:

- "How to screen strong stocks from China A-share technology sector? Give me an analysis framework"
- "What technical indicators should I focus on when analyzing BTC/USDT?"
- "How to conduct market review? What methodologies are available?"
- "What's the position management strategy for 100k capital?"
- "How to analyze the impact of financial news on the market?"

## Usage Examples

### Smart Stock Screening Framework

```
Please provide an analysis framework for screening strong stocks from China A-share technology sector, including:
- Technical indicator selection (RSI, MACD, etc.)
- Fundamental indicator selection (PE, ROE, etc.)
- Screening process and scoring methods
```

### Individual Stock Analysis Methods

```
How to conduct deep analysis on a stock? Please provide an analysis framework, including:
- Multi-timeframe technical analysis methods
- Fundamental data interpretation
- News event impact analysis
- Buy timing judgment criteria
```

### Market Review Framework

```
How to conduct China A-share market review? Please provide an analysis framework, including:
- Hot sector identification methods
- Capital flow analysis
- Investment opportunity discovery strategies
```

### Risk Management Methods

```
What's the position management strategy for 100k capital? Please provide:
- Position allocation principles
- Stop-loss/take-profit setting methods
- Risk-reward ratio calculation
```

## Supported Markets

This skill provides analysis frameworks and methodologies for the following markets:

- 🇨🇳 **China A-shares** - SSE, SZSE, BSE
- 🇺🇸 **United States** - NYSE, NASDAQ
- 🇭🇰 **Hong Kong** - HKEX
- 🇯🇵 **Japan** - TSE
- 🇰🇷 **South Korea** - KRX
- 🪙 **Cryptocurrency** - Binance, Coinbase, OKX, etc.
- 💱 **Forex** - Major currency pairs
- 📦 **Futures** - Commodity, index futures

For complete market list and data structures, see `references/api-documentation.md`.

## Frequently Asked Questions

### Q: Does this skill provide real-time data?

**A**: This skill provides analysis frameworks and methodology guidance based on TradingView API data structures. For real-time data, you can:
1. Visit https://rapidapi.com/hypier/api/tradingview-data1 to get API keys
2. Refer to examples in `references/api-examples/` to understand API calling methods
3. Check `references/api-documentation.md` for complete API documentation

### Q: How to understand API data structures?

**A**:
1. Check real API response examples in `references/api-examples/` directory
2. Read `references/api-documentation.md` to understand field meanings
3. Refer to `references/china-a-stock-examples.md` for practical cases

### Q: Which technical indicators are supported?

**A**: Technical analysis includes the following indicators (refer to `references/technical-analysis.md`):
- Trend indicators: SMA, EMA, MACD, ADX
- Momentum indicators: RSI, Stoch, CCI, Williams %R
- Volume indicators: Volume, MFI
- Support resistance: Pivot Points, Fibonacci
- Others: ATR, Beta, Bollinger Bands

### Q: How to get historical K-line data?

**A**: Refer to `references/api-examples/01-price-data.txt` for price data API format:
- Supported timeframes: 1/5/15/30/60/240/D/W/M
- Maximum 500 K-lines available
- Data fields: open, high, low, close, volume, time

### Q: Which languages are supported for news data?

**A**: Supports 19 languages (refer to `references/api-documentation.md`), commonly used are:
- `zh-Hans` - Simplified Chinese
- `en` - English
- `ja` - Japanese
- `ko` - Korean

## Directory Structure

```
openclaw-tradingview-quant/
├── README.md                    # English user guide
├── SKILL.md                     # AI skill description
├── SECURITY.md                  # Security policy and best practices
├── references/                  # Reference materials
│   ├── api-examples/            # Real API request/response examples (9 files)
│   │   ├── 01-price-data.txt    # Price/K-line data examples
│   │   ├── 02-quote-data.txt    # Real-time quote examples
│   │   ├── 03-market-search.txt # Market search examples
│   │   ├── 04-technical-analysis.txt # Technical analysis examples
│   │   ├── 05-leaderboards.txt  # Leaderboard examples
│   │   ├── 06-news.txt          # News data examples
│   │   ├── 07-metadata.txt      # Metadata examples
│   │   ├── 08-calendar.txt      # Calendar event examples
│   │   └── 09-logo.txt          # Logo image examples
│   ├── api-documentation.md     # Complete API documentation and metadata dictionary
│   ├── technical-analysis.md    # Technical analysis methodology
│   ├── pattern-library.md       # Pattern recognition library
│   ├── risk-management.md       # Risk management methods
│   └── china-a-stock-examples.md # China A-share practical cases
└── workflows/                   # Analysis workflows (15 total)
    ├── smart-screening.md       # Smart stock screening framework
    ├── pattern-recognition.md   # Pattern recognition methods
    ├── market-review.md         # Market review framework
    ├── risk-assessment.md       # Risk assessment methods
    ├── event-analysis.md        # Event analysis framework
    ├── deep-stock-analysis.md   # Deep individual stock analysis
    ├── fundamental-screening.md # Fundamental screening
    ├── sector-rotation.md       # Sector rotation analysis
    └── ...                      # Other workflows
```

## Advanced Usage

### Custom Screening Framework

Refer to `workflows/smart-screening.md` and `workflows/fundamental-screening.md` to build:
- Technical indicator screening frameworks (RSI, MACD, ADX, etc.)
- Fundamental screening frameworks (PE, PB, ROE, dividend yield, etc.)
- Market cap, volume screening strategies
- Industry sector screening methods

### Multi-Market Comparative Analysis

```
How to compare markets in China, US, and Japan? Please provide an analysis framework
```

### Strategy Backtesting Methods

Combining historical K-line data and technical indicators, methodology guidance for strategy validation can be provided.

## Technical Support

- **API Examples**: `references/api-examples/` - Real API request/response examples
- **API Documentation**: `references/api-documentation.md` - Complete API documentation
- **Analysis Methods**: `references/technical-analysis.md` - Technical analysis methodology
- **Practical Cases**: `references/china-a-stock-examples.md` - China A-share practical cases

## Get Real-Time Data (Optional)

To access real-time market data, you can:

1. **Visit RapidAPI**: https://rapidapi.com/hypier/api/tradingview-data1
2. **Refer to Examples**: Real API calling examples in `references/api-examples/` directory

## Disclaimer

The analysis frameworks and methodologies provided by this tool are for learning and research purposes only and do not constitute any investment advice. Investing involves risks; enter the market cautiously. Any investment decisions made using the analysis methods provided by this tool are at your own risk.

## License

MIT License
