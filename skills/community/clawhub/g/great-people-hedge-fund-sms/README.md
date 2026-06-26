# Great People Hedge Fund - AI Investment Analyst

> Multi-agent AI system inspired by [ai-hedge-fund](https://github.com/virattt/ai-hedge-fund), implementing the investment philosophies of legendary investors to analyze stocks.

## 🎯 Overview

This project creates a team of AI agents, each representing a legendary investor or analyst methodology, working together to provide comprehensive stock analysis and investment signals.

## 📊 Investor Personas

### Value Investing Legends
| Agent | Philosophy | Key Focus |
|-------|------------|-----------|
| **Warren Buffett** | Oracle of Omaha | Wonderful companies at fair prices, moats, long-term holding |
| **Charlie Munger** | Buffett's Partner | Mental models, rational decision making, quality at fair price |
| **Ben Graham** | Godfather of Value | Margin of safety, net-net stocks, deep value |
| **Mohnish Pabrai** | Dhandho Investor | Low risk, high certainty, cloning proven strategies |

### Growth Investing Masters
| Agent | Philosophy | Key Focus |
|-------|------------|-----------|
| **Peter Lynch** | Tenbagger Hunter | Growth in everyday businesses, know what you own |
| **Cathie Wood** | Innovation Queen | Disruption, exponential technologies, ARK Invest style |

### Contrarian & Risk Experts
| Agent | Philosophy | Key Focus |
|-------|------------|-----------|
| **Michael Burry** | Big Short Contrarian | Deep value, short candidates, contrarian bets |
| **Nassim Taleb** | Black Swan Analyst | Tail risk, antifragility, asymmetric payoffs |

### Macro & Special Situations
| Agent | Philosophy | Key Focus |
|-------|------------|-----------|
| **Stanley Druckenmiller** | Macro Legend | Asymmetric opportunities, big bets |
| **Rakesh Jhunjhunwala** | Big Bull of India | Emerging markets, contrarian conviction |

### Analytical Agents
| Agent | Function |
|-------|----------|
| **Sentiment Agent** | Market情绪分析, news sentiment, social media signals |
| **Fundamentals Agent** | Financial metrics, ratios, earnings analysis |
| **Technicals Agent** | Chart patterns, indicators, support/resistance |
| **Risk Manager** | Position sizing, risk metrics, drawdown analysis |
| **Portfolio Manager** | Final decision synthesis, signal generation |

## 🏗️ Architecture

```
User Input (Stock Ticker)
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    ANALYSIS PHASE (Parallel)                │
├──────────────┬──────────────┬──────────────┬────────────────┤
│  @buffett    │   @lynch    │   @taleb     │  @sentiment    │
│  @munger     │   @wood     │   @burry     │  @technicals   │
│  @graham     │   @druck    │   @pabraí    │  @fundamentals │
└──────────────┴──────────────┴──────────────┴────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    SYNTHESIS PHASE                          │
├─────────────────────────────┬───────────────────────────────┤
│      Risk Manager           │     Portfolio Manager           │
│  - Position limits          │  - Signal: BUY/HOLD/SELL       │
│  - Risk score               │  - Conviction level           │
│  - Tail risk assessment     │  - Key insights summary       │
└─────────────────────────────┴───────────────────────────────┘
         │
         ▼
              ┌─────────────────────────┐
              │   INVESTMENT REPORT    │
              │   - Signal + Rating     │
              │   - Agent viewpoints    │
              │   - Risk assessment     │
              │   - Position sizing     │
              └─────────────────────────┘
```

## 📈 Signal System

| Signal | Meaning | Conviction |
|--------|---------|------------|
| 🟢 **STRONG BUY** | Exceptional opportunity | 5/5 |
| 🟢 **BUY** | Favorable risk/reward | 4/5 |
| 🟡 **HOLD** | Wait for better entry | 3/5 |
| 🔴 **SELL** | Risk outweighs reward | 2/5 |
| 🔴 **STRONG SELL** | Avoid or close position | 1/5 |

## 🚀 Usage

### Quick Analysis
```
analyze AAPL
analyze NVDA,MSFT,GOOGL
```

### With Date Range (Backtest)
```
analyze TSLA --start 2024-01-01 --end 2024-12-31
```

### CLI Options
```bash
--ticker <symbols>    # Comma-separated stock symbols
--start <date>        # Start date (YYYY-MM-DD)
--end <date>          # End date (YYYY-MM-DD)
--agents <list>        # Specific agents to use
--format <type>        # Output format: markdown, json, table
```

## 📁 Project Structure

```
great-people-hedge-fund/
├── SKILL.md                          # Main skill definition
├── README.md                         # This file
├── _meta.json                        # Skill metadata
├── _skills/
│   ├── buffett/                      # Warren Buffett agent
│   │   └── PROMPT.md
│   ├── munger/                       # Charlie Munger agent
│   │   └── PROMPT.md
│   ├── lynch/                        # Peter Lynch agent
│   │   └── PROMPT.md
│   ├── taleb/                        # Nassim Taleb agent
│   │   └── PROMPT.md
│   ├── burry/                        # Michael Burry agent
│   │   └── PROMPT.md
│   ├── sentiment/                    # Market sentiment agent
│   │   └── PROMPT.md
│   ├── fundamentals/                 # Fundamental analysis agent
│   │   └── PROMPT.md
│   ├── technicals/                   # Technical analysis agent
│   │   └── PROMPT.md
│   ├── risk-manager/                 # Risk management agent
│   │   └── PROMPT.md
│   └── portfolio/                    # Portfolio manager agent
│       └── PROMPT.md
└── prompts/
    ├── INVESTOR_PERSONAS.md          # Full persona definitions
    ├── ANALYSIS_TEMPLATE.md          # Report template
    └── MARKET_DATA_REQUIREMENTS.md  # Data requirements
```

## 🔧 Installation

```bash
# Via OpenClaw
openclaw install great-people-hedge-fund

# Via ClawHub
npx --yes clawhub@latest install great-people-hedge-fund-sms
```

## ⚠️ Disclaimer

This project is for **educational and research purposes only**.

- NOT intended for real trading or investment
- NO investment advice or guarantees provided
- Past performance does not indicate future results
- Consult a financial advisor for investment decisions

## 📜 License

MIT License - See LICENSE file for details.

## 🙏 Credits

- Inspired by [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund)
- Investment philosophies of legendary investors
- Built on [Nanobot](https://github.com/HKUDS/nanobot) framework
