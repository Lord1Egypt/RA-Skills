# Source Categories

These are the types of sources the Stock Watcher Pro agent discovers and monitors for each ticker. Understanding these helps you evaluate the quality and breadth of your source network.

---

## Primary Sources (Highest Signal)

### SEC EDGAR Filings
- **What:** Official regulatory filings with the U.S. Securities and Exchange Commission.
- **Types:** 8-K (material events), 10-K (annual reports), 10-Q (quarterly reports), Form 4 (insider transactions), DEF 14A (proxy statements).
- **Why it matters:** This is legally required disclosure. It's the most reliable, least-spun information about a public company.
- **Quality score range:** 90-100

### Company Investor Relations (IR) Pages
- **What:** The company's own investor-facing content: press releases, earnings presentations, SEC filing archives, event calendars.
- **Why it matters:** First-party information. Earnings dates, guidance updates, and corporate announcements often appear here before mainstream news picks them up.
- **Quality score range:** 85-95

### Earnings Call Transcripts
- **What:** Word-for-word records of quarterly earnings calls between executives and analysts.
- **Why it matters:** Management tone, forward guidance nuances, and analyst questions reveal what the market is really focused on.
- **Sources:** Company IR pages, Seeking Alpha (free with delay), Motley Fool transcripts.
- **Quality score range:** 80-90

---

## Secondary Sources (Good Signal, Some Noise)

### Industry-Specific Publications
- **What:** Trade publications and specialist blogs that cover a specific sector deeply.
- **Examples:** 9to5Mac (Apple/tech), Electrek (EVs/energy), STAT News (biotech/pharma), The Information (enterprise tech).
- **Why it matters:** These catch stories before mainstream financial media. Deeper analysis, less hype.
- **Quality score range:** 60-85

### Financial News Wires
- **What:** Major financial news outlets.
- **Examples:** Reuters, Bloomberg (free articles), CNBC, MarketWatch, Financial Times.
- **Why it matters:** Speed. They break stories fast. But they also generate volume, so the agent filters by relevance.
- **Quality score range:** 50-75

### Competitor Press Rooms
- **What:** Press releases and announcements from competitor companies.
- **Why it matters:** A competitor's product launch, executive hire, or earnings miss directly impacts your holdings. Cross-referencing competitor moves against your thesis is a key Stock Watcher Pro feature.
- **Quality score range:** 70-85

---

## Tertiary Sources (Context & Sentiment)

### Analyst Research (Public Summaries)
- **What:** Publicly available summaries of Wall Street analyst reports (price target changes, rating changes).
- **Sources:** MarketBeat, TipRanks, Yahoo Finance analyst pages.
- **Why it matters:** Consensus shifts can move stocks. The agent tracks rating changes as data points, not recommendations.
- **Quality score range:** 40-65

### Social Sentiment
- **What:** Discussion on Reddit (relevant subreddits like r/stocks, r/investing, r/wallstreetbets), StockTwits, and financial Twitter/X.
- **Why it matters:** Retail sentiment can be a leading or contrarian indicator. The agent monitors but does NOT treat social media as investment advice.
- **Quality score range:** 20-50
- **Caution:** Highest noise source. The agent weighs these signals lowest and always cross-references with primary sources.

### RSS Feeds
- **What:** Automated content feeds from news sites, blogs, and corporate newsrooms.
- **Why it matters:** Efficient polling mechanism. The agent checks RSS feeds for new content without scraping entire websites.
- **Quality score range:** Varies (inherits the quality of the underlying source)

---

## Source Health Indicators

| Status | Meaning |
|--------|---------|
| 🟢 **Active** | Source is reachable, returning fresh content, and contributing to briefings. |
| 🟡 **Stale** | Source hasn't produced new relevant content in 14+ days. May need review. |
| 🔴 **Failing** | Source URL is broken, returning errors, or blocked. Will be removed if not fixed. |
| ⚪ **Unknown** | Newly discovered source not yet checked. Will be evaluated on next health check. |

The agent runs a weekly source health check (configurable in `watchlist-config.json`) and flags any degraded sources in your next briefing.
