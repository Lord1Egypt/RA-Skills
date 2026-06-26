# ⚔️ Presage Skill for OpenClaw

> AI-powered prediction market analysis for Solana

[![ClawHub](https://img.shields.io/badge/Available%20on-ClawHub-blue?style=flat-square)](https://clawhub.ai/Seenfinity/presage)
[![GitHub Repo](https://img.shields.io/badge/GitHub-seenfinity%2Fpresage--skill-blue?style=flat-square)](https://github.com/Seenfinity/presage-skill)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](https://opensource.org/licenses/MIT)

---

## What is Presage?

[Presage](https://presage.market) is an AI-powered prediction market terminal on Solana (powered by Kalshi). Analyze YES/NO outcomes on real-world events — sports, crypto, politics, economics, and more.

This skill integrates Presage with OpenClaw, giving your AI agent:
- 📊 Live market data analysis
- 🔍 Opportunity detection
- 📈 Portfolio insights
- 🧠 AI-powered recommendations

---

## Installation

### From ClawHub (recommended)

```bash
clawhub install presage
```

### Manual

```bash
cd /path/to/your/workspace/skills
git clone https://github.com/Seenfinity/presage-skill.git presage
```

---

## Features

### Market Analysis
- Real-time prices, volumes, and orderbooks
- Trend and liquidity analysis
- Identify trading opportunities

### Opportunity Detection
- Find mispriced markets automatically
- Spread analysis
- Volume-weighted recommendations

### Portfolio View
- Check account balances
- View open positions
- Track P&L

---

## Usage

Once installed, the skill provides these tools:

```
analyzeMarkets      → Overview of all available markets
analyzeMarket(ticker) → Deep dive into specific market
getPortfolio(agentId) → Your balance and positions
findOpportunities   → Scan for mispriced markets
```

---

## Example

```
> What markets have high volume today?
→ [Analysis of top markets by volume]

> Check my portfolio
→ [Your balance and positions]

> Find undervalued markets
→ [Markets where YES/NO prices seem off]
```

---

## Requirements

- OpenClaw or compatible agent platform
- Node.js 18+ (uses built-in fetch)

---

## Tech Stack

- **Runtime**: OpenClaw agent
- **API**: Presage REST API (public endpoints)
- **Language**: JavaScript

---

## Contributing

1. Fork the repo
2. Create a feature branch
3. Submit a PR

---

## License

MIT © 2026 Seenfinity

---

## Links

- 🌐 [Presage Market](https://presage.market)
- 🦞 [ClawHub Skill](https://clawhub.ai/Seenfinity/presage)
- 📂 [GitHub Repo](https://github.com/Seenfinity/presage-skill)
- 💬 [Colosseum](https://colosseum.com/agent-hackathon/projects/presage)
