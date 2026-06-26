# Mapulse 🇰🇷

Korean stock market AI analyst — Telegram bot.

Monitor KOSPI/KOSDAQ, track your watchlist, get AI briefings, and ask natural-language questions in Korean, Chinese, or English.

## Quick Start

```bash
pip install python-telegram-bot pykrx requests beautifulsoup4
export TELEGRAM_BOT_TOKEN=your_token_here
cd bot && python3 mapulse_bot.py
```

Open Telegram → find your bot → `/start`

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | ❌ | Enables Telegram bot integration (sending and receiving messages). If not provided, Telegram features will be disabled . |
| `OPENROUTER_API_KEY` | ❌ | AI deep analysis (OpenRouter) |
| `ANTHROPIC_API_KEY` | ❌ | AI deep analysis (Anthropic, alternative to OpenRouter) |
| `DART_API_KEY` | ❌ | DART corporate disclosure data (free at https://opendart.fss.or.kr) |
| `ALLOWED_GROUPS` | ❌ | Restrict to specific Telegram group IDs (comma-separated) |

## Features

**Stock Queries** — type naturally:
- 삼성전자 / NAVER / 005930
- 삼성 왜 빠졌어? (why analysis)
- 비교 삼성 하이닉스 (compare)

**Market Overview:**
- 시황 / 코스피 / 업종 (sector rankings)

**Global Assets:**
- 환율 / 비트코인 / 금 / 원유

**Alerts:**
- /alert 005930 3.0 (crash alert at -3%)

**DART Disclosures** (requires DART_API_KEY):
- 삼성 공시

## Data Sources (free, no keys)

- **pykrx** — KRX official KOSPI/KOSDAQ data
- **Yahoo Finance** — real-time quotes, FX, commodities
- **Daum Finance** — sector rankings, trending stocks
- **CoinGecko** — crypto prices

## AI Analysis (optional)

Set `OPENROUTER_API_KEY` or `ANTHROPIC_API_KEY` to enable:
- Cause analysis (why did X drop?)
- Stock comparisons
- Risk/opportunity assessment
- Multi-language responses

Without an AI key, the bot still works — just returns data without deep analysis.

## Project Structure

```
bot/
  mapulse_bot.py        # Telegram bot entry point
scripts/
  chat_query.py         # Query processing & intent classification
  db.py                 # SQLite database layer
  market_data.py        # KRX data via pykrx
  claude_ai.py          # AI analysis layer
  commodities.py        # Commodities & FX data
  crypto.py             # Crypto prices
  crash_alert.py        # Price alert monitoring
  fetch_briefing.py     # Daily briefing generator
  daum_finance.py       # Sector rankings
  cron_*.py             # Scheduled tasks
docs/
  TUTORIAL.md           # Setup tutorial
  architecture.md       # Technical architecture
```

## License

MIT
