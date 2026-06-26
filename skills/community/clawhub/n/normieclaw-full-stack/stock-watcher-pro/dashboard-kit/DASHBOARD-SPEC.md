# Stock Watcher Pro — Dashboard Companion Kit Specification

*For consumption by Dashboard Builder. This spec defines the complete visual command center for Stock Watcher Pro.*

---

## Overview

The Stock Watcher Dashboard transforms chat-based intelligence into a Bloomberg-style visual command center. Dark mode, data-dense, institutional teal and alert-orange accents. Maximum signal, zero noise.

---

## Stack

- **Framework:** Next.js (App Router)
- **Database:** Supabase (PostgreSQL) — Fallback: SQLite for zero-config local setups
- **Styling:** Tailwind CSS + shadcn/ui (customized terminal aesthetic)
- **Charting:** TradingView Lightweight Charts (Apache 2.0, canvas-based)
- **Chart Types:** Candlestick, Line, Area, Volume Histograms
- **Timeframes:** 1D, 1W, 1M, 3M, 1Y, 5Y, MAX

### Market Data Providers (Free Tiers)
- **Alpha Vantage:** Historical EOD data (25 calls/day free)
- **Financial Modeling Prep (FMP):** Intraday snapshots, company profiles (generous free tier)

---

## Database Schema (Supabase / PostgreSQL)

### `portfolios`
| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid | Primary key, default gen_random_uuid() |
| `name` | text | Portfolio name |
| `created_at` | timestamptz | Default now() |

### `holdings`
| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid | Primary key |
| `portfolio_id` | uuid | FK → portfolios.id |
| `ticker` | varchar(10) | Stock symbol |
| `company_name` | text | Full company name |
| `shares` | numeric | Share count |
| `avg_cost` | numeric | Average cost basis |
| `price_target` | numeric | User's price target (nullable) |
| `sector` | text | Sector classification |
| `thesis` | text | User's investment thesis |
| `thesis_status` | varchar(20) | bullish / neutral / bearish |
| `added_at` | timestamptz | Default now() |

### `briefings`
| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid | Primary key |
| `date` | date | Briefing date |
| `type` | text | CHECK: pre-market, mid-day, post-market, weekly-wrap |
| `content_md` | text | Full markdown content |
| `market_sentiment` | varchar(20) | Overall market read |
| `created_at` | timestamptz | Default now() |

### `filing_summaries`
| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid | Primary key |
| `ticker` | varchar(10) | Stock symbol |
| `form_type` | varchar(10) | 10-K, 10-Q, 8-K, 4, DEF 14A |
| `filing_date` | timestamptz | SEC filing timestamp |
| `edgar_url` | text | Direct EDGAR link |
| `items_reported` | text[] | Array of item descriptions |
| `ai_summary` | text | Agent-generated summary |
| `impact_score` | integer | 1-10 materiality scale |
| `thesis_alignment` | varchar(20) | bullish / neutral / bearish |
| `created_at` | timestamptz | Default now() |

### `news_links`
| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid | Primary key |
| `ticker` | varchar(10) | Stock symbol |
| `title` | text | Article headline |
| `source` | varchar(100) | Source name |
| `url` | text | Source URL |
| `published_at` | timestamptz | Original publish time |
| `relevance_score` | integer | 1-100 relevance scale |
| `type` | text | CHECK: news, press_release, sec_filing, earnings_transcript |
| `ai_summary` | text | 2-sentence agent summary |
| `created_at` | timestamptz | Default now() |

### `source_network`
| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid | Primary key |
| `ticker` | varchar(10) | Stock symbol |
| `source_name` | varchar(200) | Human-readable name |
| `feed_url` | text | URL being monitored |
| `source_type` | varchar(50) | ir_page, edgar, industry_blog, rss, etc. |
| `last_polled` | timestamptz | Last successful check |
| `health_status` | text | CHECK: active, stale, failing, unknown |
| `quality_score` | integer | 0-100 |
| `created_at` | timestamptz | Default now() |

### `thesis_tracking`
| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid | Primary key |
| `ticker` | varchar(10) | Stock symbol |
| `date_logged` | timestamptz | When the evaluation happened |
| `thesis_state` | text | accelerating, holding, weakening |
| `catalyst_noted` | text | What triggered the evaluation |
| `source` | text | Where the signal came from |
| `reasoning` | text | Agent's reasoning |
| `price_at_time` | numeric | Stock price at evaluation time |
| `created_at` | timestamptz | Default now() |

### Indexes
```sql
CREATE INDEX idx_holdings_portfolio ON holdings(portfolio_id);
CREATE INDEX idx_holdings_ticker ON holdings(ticker);
CREATE INDEX idx_briefings_date_type ON briefings(date, type);
CREATE INDEX idx_filings_ticker_date ON filing_summaries(ticker, filing_date DESC);
CREATE INDEX idx_news_ticker_date ON news_links(ticker, published_at DESC);
CREATE INDEX idx_source_ticker ON source_network(ticker);
CREATE INDEX idx_thesis_ticker_date ON thesis_tracking(ticker, date_logged DESC);
```

### Row Level Security (RLS)
All tables should have RLS enabled with policies scoped to the authenticated user's portfolio. For local/single-user setups, a permissive policy is acceptable.

---

## Component Breakdown

### A. Portfolio Overview (Home — `/`)

**Layout:**
- Top bar: Global market status (S&P 500, NASDAQ, DOW — green/red), daily portfolio P&L snapshot
- Left column (60%): Holdings data table
- Right column (40%): Allocation donut chart + 1-month portfolio value line chart

**Holdings Table Columns:**
| Column | Content |
|--------|---------|
| Ticker | Symbol + company name (truncated) |
| Price | Current/latest price |
| 24h % | Daily change (teal = up, orange = down) |
| Shares | Position size |
| Cost Basis | Average cost |
| P&L | Unrealized gain/loss ($ and %) |
| Thesis | Status badge (🟢 Accelerating, 🟡 Holding, 🔴 Weakening) |

Clicking a row routes to `/ticker/[symbol]`.

**Allocation Donut:**
- Segments by ticker, sized by position value
- Teal palette with distinct shades
- Center shows total portfolio value

### B. Per-Stock Intelligence Hub (`/ticker/[symbol]`)

**Header:** Ticker, Company Name, Live Price, 24h Change, Thesis Status Badge

**Main Chart (Top 60%):**
TradingView Lightweight Candlestick chart with volume histogram overlay. Timeframe selector: 1D, 1W, 1M, 3M, 1Y, 5Y, MAX.

**Below Chart (Split View):**

*Left Panel — "AI Thesis" Card:*
- Current thesis status (Accelerating/Holding/Weakening) with colored indicator
- User's thesis text
- Most recent catalyst and reasoning
- Last 5 thesis log entries as a mini-timeline

*Right Panel — Recent Filings:*
- Expandable accordion list from `filing_summaries`
- Each shows: form type badge, date, impact score, 2-line summary
- Click to expand full summary + direct EDGAR link

### C. Briefing Archive (`/briefings`)

**Layout:** Dense list with filter controls

**Controls:**
- Filter by type: All / Pre-Market / Mid-Day / Post-Market / Weekly Wrap
- Date range picker
- Full-text search on `content_md`

**Cards:** Expandable markdown renderer. Shows date, type badge, market sentiment indicator. Click to expand full briefing text.

### D. SEC Filing Feed & News (`/intel`)

**Layout:** Chronological timeline feed

**Item Design:**
- Type badge: `[8-K]` `[10-K]` `[Press Release]` `[News]` — color-coded
- Title (linked to source)
- Source name + timestamp
- 2-sentence AI summary
- Impact/relevance score indicator
- Ticker tag

**Controls:** Filter by ticker, type, date range, minimum impact score.

### E. Thesis Tracker Timeline (`/thesis`)

**Layout:** Per-ticker dual-axis chart

**Function:**
- TradingView Lightweight price chart for the ticker
- Overlay `thesis_tracking` entries as markers on the price line
- Bull markers (📈 teal triangle up) for accelerating signals
- Bear markers (📉 orange triangle down) for weakening signals
- Neutral markers (➡️ gray dot) for holding signals
- Hover/click a marker: tooltip shows `catalyst_noted`, `reasoning`, `source`, and `price_at_time`

**Selector:** Dropdown to pick which ticker's thesis timeline to view.

### F. Source Health Monitor (`/sources`)

**Layout:** Admin-style data table

**Columns:**
| Column | Content |
|--------|---------|
| Source Name | Human-readable |
| Ticker | Which holding it covers |
| Type | RSS, EDGAR, IR Page, Blog, etc. |
| Last Polled | Timestamp |
| Status | 🟢 Active / 🟡 Stale / 🔴 Failing / ⚪ Unknown |
| Quality | Score bar (0-100) |

**Controls:** Filter by ticker, status, type. Sort by any column.

---

## Design System

### Colors
| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#0f172a` | Main background |
| `--bg-secondary` | `#1e293b` | Cards, panels |
| `--bg-tertiary` | `#020617` | Deepest background |
| `--border` | `#334155` | Subtle borders (1px) |
| `--accent-bullish` | `#14b8a6` | Teal — positive, primary actions |
| `--accent-bearish` | `#f97316` | Orange — negative, alerts |
| `--text-primary` | `#f1f5f9` | Main text |
| `--text-secondary` | `#94a3b8` | Muted/label text |
| `--text-muted` | `#64748b` | Timestamps, minor details |

### Typography
- **Headings:** Inter (semibold)
- **Body:** Inter (regular)
- **Numbers/Tickers:** Roboto Mono (monospace) — high density
- **Size scale:** text-xs through text-lg. Favor text-sm and text-xs for data-dense views.

### Component Patterns
- **Cards:** `bg-secondary` with 1px `border` and `rounded-lg`
- **Badges:** Small pills with colored backgrounds (e.g., `bg-teal-500/20 text-teal-400`)
- **Tables:** Striped rows with `hover:bg-slate-800/50`
- **Charts:** Dark background, teal for bullish, orange for bearish, slate grid lines

---

## Data Flow & Agent Integration

### Ingestion Path
1. Stock Watcher Pro agent runs its scheduled checks (EDGAR, news, briefings).
2. Agent writes results to local JSON files (the standard Stock Watcher Pro data structure).
3. A sync script (or agent-triggered API call) pushes data from JSON files to Supabase tables.

### API Routes (Next.js)
```
POST /api/holdings      — Upsert holding
POST /api/briefings     — Store new briefing
POST /api/filings       — Store filing summary
POST /api/news          — Store news link
POST /api/thesis        — Log thesis evaluation
POST /api/sources       — Update source network
GET  /api/portfolio     — Fetch portfolio overview
GET  /api/ticker/[sym]  — Fetch per-ticker data
GET  /api/briefings     — List briefings (with filters)
```

### Authentication
- For local single-user setups: no auth required (localhost only)
- For hosted setups: Supabase Auth with RLS policies

### Real-Time Updates
- Supabase real-time subscriptions for live filing alerts
- SWR polling (30s interval) for price updates and briefing status

---

## Responsive Behavior

- **Desktop (1200px+):** Full multi-column layouts as described
- **Tablet (768-1199px):** Stack columns vertically, maintain chart sizes
- **Mobile (< 768px):** Single column, simplified tables (hide less critical columns), charts full-width

---

*This spec is designed for the NormieClaw Dashboard Builder skill to consume and produce a complete, deployable Next.js application.*
