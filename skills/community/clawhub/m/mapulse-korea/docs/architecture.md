# Architecture — Mapulse v1.1.0

## System Overview

Mapulse is a Korean stock market AI analyst delivered as a Telegram Bot. It combines real-time market data from multiple sources with LLM analysis to provide instant, context-rich answers to stock market questions in Korean, Chinese, and English.

## Core Components

### 1. Telegram Bot (`bot/mapulse_bot.py`)

Entry point. Handles:
- 15 slash commands (see Bot Commands below)
- Natural language messages (routed to chat_query.py)
- Group chat support (responds to @mentions and replies)
- Billing v2 integration (pay-per-call, free trial, Infini Money checkout)

### 2. Query Engine (`scripts/chat_query.py`)

The brain. 2,000+ lines handling 22 intent types:

| Intent | Trigger Examples | Handler |
|--------|-----------------|---------|
| `STOCK_PRICE` | 삼성 / Samsung / 005930 | `handle_stock_price()` |
| `WHY_DROP` | 왜 빠졌어 / 为什么跌 / why drop | `handle_why_move()` |
| `WHY_RISE` | 왜 올랐어 / 为什么涨 / why up | `handle_why_move()` |
| `MARKET_OVERVIEW` | 시장 / 코스피 / 市场 | `handle_market_overview()` |
| `SECTOR_RANKING` | 업종 / 行业 / sector | `handle_sector_ranking()` |
| `HOT_RANK` | 인기 / 热门 / trending | `handle_hot_rank()` |
| `NEWS` | 뉴스 / 新闻 / news | `handle_news()` |
| `COMMUNITY` | 분위기 / 舆论 / sentiment | `handle_community()` |
| `RESEARCH` | 리서치 / 研报 / research | `handle_research()` |
| `SUPPLY_DEMAND` | 수급 / 外资 / foreign | `handle_supply_demand()` |
| `COMPARE` | 비교 / 对比 / compare | `handle_compare()` |
| `OUTLOOK` | 전망 / 怎么看 / outlook | `handle_outlook()` |
| `COMMODITY` | 금시세 / 黄金 / gold | `query_commodity()` |
| `CRYPTO` | 비트코인 / BTC / ETH | `fetch_price()` |
| `DISCLOSURE` | 공시 / 公告 | `fetch_disclosure()` |
| `FINANCIAL` | 재무 / 财务 | `fetch_financial_summary()` |
| `EXCHANGE_RATE` | 환율 / 汇率 / forex | `fetch_exchange_rates()` |
| `FEAR_GREED` | 공포 / VIX | `fetch_fear_greed()` |
| `CHAT` | 자유 대화 | LLM freeform |
| `UNKNOWN` | (unclassified) | fallback |

#### Ticker Resolution (v1.1 updated)

```
Input → resolve_ticker(text)
  ├─ 직접 티커 (6자리 숫자) → return
  ├─ 별명 매칭 (최장매칭 우선, 172개 별명)
  │   정렬: _ALIASES_SORTED = sorted by len(alias) desc
  │   삼성바이오로직스 → 207940 (삼성 보다 먼저 매칭)
  ├─ 정식 이름 매칭 (길이 내림차순)
  └─ KRX API fallback: krx.get_market_ticker_name(ticker)
```

Theme keywords (117개): 반도체, AI, 2차전지, 방산, 바이오, K-POP, etc.

#### Two-Phase Response

```
Phase 1: process_query_fast()  → 1-5 seconds, no LLM
  ├─ Intent classification (keyword match)
  ├─ Ticker resolution (longest-match first)
  ├─ Data fetch (Daum + Naver + pykrx)
  ├─ Format + enhanced data (market cap, PER, 52w)
  └─ Immediate send

Phase 2: process_query_deep()  → 5-20 seconds, LLM
  ├─ Collect: news + community + research + global news
  ├─ AI analysis with full context
  ├─ Trust badge (data source attribution)
  └─ Append send
```

### 3. Data Layer

#### Daum Finance (`scripts/daum_finance.py`)

7 API endpoints, all free, no key required:

| Function | API | Returns |
|----------|-----|---------|
| `fetch_daum_stock(ticker)` | `/api/quotes/A{ticker}` | 50+ fields |
| `fetch_daum_batch(tickers)` | `/api/quotesv4?codes=...` | Batch (max 20) |
| `fetch_daum_chart(ticker, days)` | `/api/charts/A{ticker}/days` | OHLCV candles |
| `fetch_daum_indices()` | `/api/domestic/trend/market/indexes` | KOSPI/KOSDAQ + investor flow |
| `fetch_daum_investors()` | `/api/domestic/trend/market/investors` | Market-wide net purchase |
| `fetch_daum_sectors()` | `/api/sector/wics` | WICS sectors + components |
| `fetch_daum_hot_ranks()` | `/api/search/ranks` | Trending stocks |

**Required header**: `Referer: https://finance.daum.net`

#### Naver Finance (`scripts/market_data.py` + `scripts/naver_extended.py`)

| Function | Returns |
|----------|---------|
| `fetch_naver_integration(ticker)` | Market cap, PER/est.PER, PBR, 52w, dividend, foreign exhaustion |
| `fetch_financial_summary(ticker)` | Annual revenue, profit, ROE |
| `fetch_disclosure(ticker)` | Corporate filings |
| `fetch_price_history(ticker)` | Historical OHLCV |
| `fetch_naver_ssr(ticker)` | OpenTalk, research, investor trends, peers |

Data priority: **Daum → Naver → pykrx → Yahoo Finance**

### 4. AI Layer

| Module | Model | Usage |
|--------|-------|-------|
| `llm.py` | `claude-3.5-haiku` | Intent fallback, quick summaries, translation |
| `llm.py` | `claude-opus-4` | Deep stock analysis |
| `cron_platform_push.py` | configurable via `LLM_MODEL` | Platform push generation |

All routed via **OpenRouter** (`OPENROUTER_API_KEY`).

### 5. Billing v2 (`scripts/billing.py` + `scripts/infini_pay.py`) — NEW in v1.1

```
User Message → billing.charge(user_id, intent)
  ├─ Trial active? → free (7 days / 50 calls)
  ├─ Balance > 0? → deduct ($0.08 normal / $0.16 deep)
  └─ Insufficient → show top-up prompt with Infini checkout link

Top-up flow:
  /topup → create_order($10+) → Infini hosted checkout → webhook → balance credited

Referral:
  /invite → ref_XXXXXX link → referred user pays → 15% commission to referrer
```

### 6. Platform Push System — NEW in v1.1

4 daily pushes via `cron_platform_push.py`:

| Time (KST) | Type | Content |
|------------|------|---------|
| 08:30 | 🌅 Morning | Pre-market brief: overnight US/EU/Asia, today's variables |
| 12:20 | 📊 Midday | Morning session recap, investor flow, afternoon outlook |
| 14:00 | ⚡ Afternoon | Key variable spotlight + engagement prompt |
| 20:50 | 🌙 Evening | US market, FX, commodities, BTC, tomorrow preview |

All pushes include:
- 🚨 **한 줄 요약** (one-line summary) at the top
- 📌 **행동 지침** (action guidance) at the bottom
- Channel broadcast + individual user delivery

### 7. News Intelligence — NEW in v1.1

| Module | Schedule | Function |
|--------|----------|----------|
| `cron_news_aggregate.py` | 2x daily | Collect + score news into `news_digest` table |
| `cron_news_scan.py` | Every 30min (pre-market) | Real-time scan, push on high-impact |

### 8. Push Performance Tracker — NEW in v1.1

`scripts/push_tracker.py` tracks recommended stock performance:
- Records price at push time
- Backfills D+1, D+3, D+5 closing prices
- Calculates directional accuracy and return statistics
- `/track` command for stats dashboard

### 9. Engagement & Metrics — NEW in v1.1

| Module | Function |
|--------|----------|
| `cron_day2_survey.py` | Day-2 user profiling (investment style, sectors) |
| `cron_daily_metrics.py` | Daily ops report (DAU, messages, conversion) |
| `trust_badge.py` | Data source attribution per intent |

### 10. Storage

SQLite (`mapulse.db`):

```sql
-- Core
users (user_id, username, first_name, trial_start, ...)
watchlist (user_id, ticker, added_at)
alerts (id, user_id, ticker, threshold, active)

-- Billing v2
billing_usage (user_id, msg_type, cost_units, is_free, created_at)
transactions (id, user_id, type, amount, balance_after, tx_hash)
infini_orders (order_id, user_id, amount, status, ...)

-- Referral
referrals (referrer_id, referred_id, ref_code)
referral_earnings (referrer_id, earned_usd, ...)

-- Content
news_digest (title_hash, source, title, score, impact_direction, created_at)
news_seen (hash, source, title, seen_at)
push_log (user_id, push_type, content, created_at)
push_tracking (push_id, ticker, push_price, d1_price, d3_price, d5_price, ...)
```

## Bot Commands

| Command | Function |
|---------|----------|
| `/start` | Onboarding + trial activation |
| `/help` | Command reference |
| `/pulse` | Today's market briefing |
| `/stock [name]` | Stock lookup |
| `/sector` | Sector ranking |
| `/hot` | Trending stocks |
| `/dart` | DART disclosures |
| `/alert [ticker] [%]` | Price alert |
| `/notify` | Push notification settings |
| `/track` | Push performance stats |
| `/stats` | Usage statistics |
| `/topup` | Top up balance (Infini Money) |
| `/balance` | Check balance + trial status |
| `/invite` | Referral link |
| `/referrals` | Referral earnings |

## Extended Coverage (`scripts/extended_aliases.py`)

- **172 aliases** (Korean/Chinese/English) → 59 stocks
- **117 theme keywords**: 반도체, AI/인공지능, 2차전지, 방산, 바이오, K-POP, 로봇, 자동차, etc.
- Longest-match-first resolution prevents ambiguity (삼성바이오로직스 ≠ 삼성전자)

## Cron Schedule (12 jobs)

| Schedule (KST) | Script | Function |
|----------------|--------|----------|
| 07:30 | `push_tracker.py backfill` | Backfill push tracking prices |
| 07:30 | `cron_news_aggregate.py` | Morning news collection |
| 08:00 | `cron_platform_push.py morning` | Morning brief |
| 08:00 | `cron_daily_metrics.py` | Daily metrics report |
| 09:00 | `cron_day2_survey.py` | Day-2 user surveys |
| 10:50 | `run_briefing.sh` | Personal briefing |
| 11:20 | `cron_platform_push.py midday` | Midday report |
| 12:30 | `cron_news_aggregate.py` | Midday news collection |
| 13:00 | `cron_platform_push.py afternoon` | Afternoon variable |
| 19:00 | `cron_news_aggregate.py` | Evening news collection |
| 19:50 | `cron_platform_push.py evening` | Night brief |
| */1min | `payment_monitor.py` | Payment status monitor |

## Infrastructure

- **Runtime**: systemd `mapulse-bot.service` (auto-restart)
- **Language**: Python 3.12
- **DB**: SQLite (single file)
- **LLM**: OpenRouter (multi-model)
- **Payment**: Infini Money hosted checkout
- **Hosting**: Linux VPS
