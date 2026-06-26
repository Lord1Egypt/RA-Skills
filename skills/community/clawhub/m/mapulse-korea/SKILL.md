---
name: mapulse
description: >
  한국주식 analyst Telegram bot. Monitors KOSPI/KOSDAQ,
  tracks watchlist, delivers AI briefings, answers natural-language questions
  in Korean/Chinese/English. Covers stock prices, sector rankings, DART
  disclosures, crash alerts, crypto, commodities, and market news.
metadata:
  openclaw:
    env:
      - name: TELEGRAM_BOT_TOKEN
        required: false
        description: Enables Telegram bot integration (sending and receiving messages). If not provided, Telegram features will be disabled .
      - name: OPENROUTER_API_KEY
        required: false
        description: OpenRouter API key for AI deep analysis
      - name: ANTHROPIC_API_KEY
        required: false
        description: Anthropic API key (alternative to OpenRouter)
      - name: DART_API_KEY
        required: false
        description: DART API key for Korean corporate disclosures
      - name: ALLOWED_GROUPS
        required: false
        description: Comma-separated Telegram group IDs to restrict bot access
      - name: MAPULSE_DB
        required: false
        description: "SQLite database path (default: data/mapulse.db)"
      - name: MAPULSE_CLAUDE_MODEL
        required: false
        description: "LLM model override (default: claude-sonnet-4)"
      - name: KOREA_STOCK_WATCHLIST
        required: false
        description: "Default watchlist tickers, comma-separated"
      - name: RATE_LIMIT_PER_MIN
        required: false
        description: "Max requests per user per minute (default: 10)"
      - name: RATE_LIMIT_COOLDOWN
        required: false
        description: "Min seconds between requests (default: 3)"
      - name: OPS_CHAT_IDS
        required: false
        description: "Comma-separated Telegram user IDs for daily stats reports"
      - name: MAPULSE_CHANNEL_ID
        required: false
        description: "Telegram channel ID for public briefing pushes"
      - name: OPENNEWS_TOKEN
        required: false
        description: "6551.io news API token"
      - name: TWITTER_TOKEN
        required: false
        description: "6551.io Twitter API token"
---

# Mapulse 🇰🇷

Korean stock market AI analyst Telegram bot. Free, no billing — just set your bot token and go 한국 주식, 시장 분위기, 해외 변수까지 분석해주는 AI .

## Quick Start

```bash
# 1. Install dependencies
pip install python-telegram-bot pykrx requests beautifulsoup4

# 2. Set your bot token
export TELEGRAM_BOT_TOKEN=your_token_here

# 3. Start the bot
cd bot && python3 mapulse_bot.py
```

All configuration is via environment variables. No `.env` files are loaded automatically.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | ✅ | Telegram bot token from @BotFather |
| `OPENROUTER_API_KEY` | ❌ | AI deep analysis (OpenRouter) |
| `ANTHROPIC_API_KEY` | ❌ | AI deep analysis (Anthropic, alternative) |
| `DART_API_KEY` | ❌ | Korean corporate disclosure data |
| `ALLOWED_GROUPS` | ❌ | Restrict to specific Telegram group IDs |
| `MAPULSE_DB` | ❌ | SQLite path (default: `data/mapulse.db`) |
| `MAPULSE_CLAUDE_MODEL` | ❌ | LLM model override (default: `claude-sonnet-4`) |
| `KOREA_STOCK_WATCHLIST` | ❌ | Default tickers, comma-separated |
| `RATE_LIMIT_PER_MIN` | ❌ | Max requests per user per minute (default: 10) |
| `RATE_LIMIT_COOLDOWN` | ❌ | Min seconds between requests (default: 3) |
| `OPS_CHAT_IDS` | ❌ | Your Telegram user ID for daily stats |
| `MAPULSE_CHANNEL_ID` | ❌ | Telegram channel ID for public pushes |
| `OPENNEWS_TOKEN` | ❌ | 6551.io news API token |
| `TWITTER_TOKEN` | ❌ | 6551.io Twitter API token |

## What Users Can Do

Type naturally in Telegram (Korean / Chinese / English):

- **Stock query:** 삼성전자, NAVER, 005930
- **Why analysis:** 삼성 왜 빠졌어?
- **Compare:** 비교 삼성 하이닉스
- **Market:** 시황, 코스피, sector, 업종
- **FX/Crypto/Commodity:** 환율, 비트코인, 금, 원유
- **DART disclosures:** 삼성 공시
- **Alerts:** /alert 005930 3.0

Mapulse는 한국 주식 시장에 특화된 분석 AI입니다.
종목명이나 질문만 입력하면 종목 분석, 시장 요약, 투자자 심리, 해외 변수 해석까지 빠르게 정리해드립니다.

단순히 뉴스를 나열하는 것이 아니라,
지금 무엇을 봐야 하는지와 어떤 리스크를 체크해야 하는지를
판단 중심으로 정리해주는 것이 특징입니다.

## Cron Scripts (optional)

The skill includes cron scripts that send scheduled briefings to **your bot's own users** (people who have interacted with your bot). These only run if you explicitly schedule them:

| Script | Purpose | Suggested schedule |
|---|---|---|
| `cron_briefing.py` | Evening briefing with watchlist | `0 13 * * 1-5` (UTC) |
| `cron_platform_push.py morning` | Pre-market briefing | `30 7 * * 1-5` (CST) |
| `cron_platform_push.py midday` | Midday recap | `20 11 * * 1-5` (CST) |
| `cron_platform_push.py evening` | Overnight briefing | `50 19 * * 1-5` (CST) |
| `cron_news_scan.py` | Breaking news alerts | `*/30 0-6 * * 1-5` (UTC) |
| `cron_daily_metrics.py` | Usage stats to OPS_CHAT_IDS | `0 8 * * *` (CST) |
| `cron_news_aggregate.py` | News digest | 3x daily |

**None of these run automatically.** You opt in by adding them to your crontab.

## Data Sources (free, no keys needed)

- **pykrx** — KRX official KOSPI/KOSDAQ data
- **Yahoo Finance** — real-time quotes, FX, commodities
- **Daum Finance** — sector rankings, trending stocks
- **CoinGecko** — crypto prices

## Persistence

The bot stores a local SQLite database (default: `data/mapulse.db`) containing:
- User records (Telegram user ID, username, call count)
- Watchlists and alerts
- Push logs and seen news hashes
- User profiles (focus stocks, push preferences)

No payment data, no billing, no external credentials are stored.

An AI product within the MAP Protocol ecosystem