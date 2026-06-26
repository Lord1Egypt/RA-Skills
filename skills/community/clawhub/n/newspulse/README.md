# 📰 NewsPulse

**Crypto News Aggregator** - Real-time news from 10+ sources with sentiment analysis!

[![Version](https://img.shields.io/github/v/release/gztanht/newspulse)](https://github.com/gztanht/newspulse/releases)
[![License](https://img.shields.io/github/license/gztanht/newspulse)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-newspulse-blue)](https://clawhub.com/skills/newspulse)

> **Stay Ahead of the Market** - Never miss important crypto news! 📰

---

## 🌟 Features

- **News Aggregation** - 10+ major crypto media sources
- **Smart Filtering** - Filter by coin/topic/importance
- **Sentiment Analysis** - Positive/Neutral/Negative scoring
- **Importance Levels** - Major/Minor/General news
- **Real-Time Updates** - RSS feed integration
- **Multi-Language** - English/Chinese support
- **Topic Tags** - BTC, ETH, Regulation, DeFi, NFT, Hacks

---

## 🚀 Quick Start

```bash
# Install
npx @gztanht/newspulse

# Latest 10 news
node scripts/news.mjs --limit 10

# Bitcoin news only
node scripts/news.mjs --tag btc

# Major events only
node scripts/news.mjs --importance high

# Negative news alert
node scripts/news.mjs --sentiment negative
```

---

## 📊 Example Output

```bash
$ node scripts/news.mjs --limit 8

📰 NewsPulse - Crypto News

Time     Importance  Sentiment  Title                           Source
─────────────────────────────────────────────────────────────────────────
2h ago   🔴 Major    🟢 Positive  Bitcoin Surges Past $71,000...   CoinDesk
3h ago   🔴 Major    🟢 Positive  Ethereum Foundation Announces...  Cointelegraph
4h ago   🔴 Major    🟡 Neutral   SEC Delays Decision on Spot...   The Block
6h ago   🔴 Major    🔴 Negative  Major Exchange Reports $100M...  CoinDesk

💡 Tip: node scripts/news.mjs --tag btc for Bitcoin news only
```

---

## 💰 Pricing - Free First!

| Plan | Price | Limit |
|------|-------|-------|
| **Free** | $0 | **5 queries/day** |
| **Sponsor Unlock** | 0.5 USDT or 0.5 USDC | Unlimited |

### Sponsorship Addresses

- **USDT (ERC20)**: `0x33f943e71c7b7c4e88802a68e62cca91dab65ad9`
- **USDC (ERC20)**: `0xcb5173e3f5c2e32265fbbcaec8d26d49bf290e44`

---

## 🏷️ News Tags

| Tag | Description | Examples |
|-----|-------------|----------|
| `btc` | Bitcoin | BTC price, ETF approval |
| `eth` | Ethereum | Protocol upgrade, Gas fees |
| `sol` | Solana | Ecosystem, TVL |
| `regulation` | Regulatory | SEC decisions, Lawsuits |
| `defi` | DeFi | Yields, Hacks |
| `nft` | NFT | Market trends |
| `hack` | Security | Exchange hacks, Exploits |

---

## 📊 Importance Levels

- 🔴 **Major** - Market-moving (regulation, major hacks, adoption)
- 🟡 **Minor** - Coin/protocol specific news
- 🟢 **General** - Daily news flow

---

## 📈 Sentiment Analysis

- 🟢 **Positive** - Good news (adoption, upgrades, partnerships)
- 🟡 **Neutral** - Factual reporting, delays
- 🔴 **Negative** - Bad news (hacks, regulatory crackdowns)

---

## 📰 News Sources

- CoinDesk
- Cointelegraph
- The Block
- Decrypt
- Bitcoin Magazine
- Ethereum World News
- CryptoSlate
- U.Today
- NewsBTC
- AMBCrypto

---

## 🔧 API Reference

**Data Source**: RSS Feeds + Public APIs

- **Update Frequency**: Every 5-15 minutes
- **Cache**: 1 hour local cache
- **Sources**: 10+ major crypto media

---

## ⚠️ Disclaimer

- News is aggregated from third-party sources
- Accuracy depends on original sources
- This tool provides information only, not financial advice
- Always verify news from multiple sources

---

## 📞 Support

- **ClawHub**: https://clawhub.com/skills/newspulse
- **Email**: support@newspulse.shark
- **Telegram**: @NewsPulseBot

---

## 📄 License

MIT © 2026 gztanht

---

**Made with 📰 by [@gztanht](https://github.com/gztanht)**

*Stay Ahead of the Market!*
