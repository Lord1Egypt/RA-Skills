---
name: gi-valuesider-superinvestor-data
version: "1.0.0"
description: Fetches Superinvestors' 13F portfolio holdings and buy/sell activity from ValueSider (valuesider.com). Use when the user asks for guru portfolio, 13F holdings, superinvestor positions, ValueSider data, or which stocks a fund/manager is buying or selling.
tags: ["finance", "13f", "superinvestor", "portfolio", "valuesider", "holdings", "trading-activity"]
---

# ValueSider Superinvestor Data

Dynamically fetches portfolio and trading activity for value investors (Superinvestors) from ValueSider, based on SEC 13F filings. **Real-time flow**: fetch page with web_fetch → parse with script → return JSON.

## When to use

- User asks for a **Superinvestor / guru portfolio** (e.g. Warren Buffett, Mason Hawkins, Longleaf Partners).
- User asks for **13F holdings** or **what stocks does [manager/fund] own**.
- User asks for **buy/sell activity** (what is [guru] buying or selling).
- User mentions **ValueSider** or **valuesider.com** in the context of portfolio data.

## Real-time flow (recommended)

ValueSider often returns 403 for direct HTTP requests. Use **web fetch** to get page content, then **parse** with the script.

### Step 1: Resolve guru slug

- If the user gave a name (e.g. "Mason Hawkins"), use a known slug such as `mason-hawkins-longleaf-partners`, or fetch `https://valuesider.com/value-investors` with web_fetch and find the matching link (slug is the path between `/guru/` and `/portfolio`).
- Common slugs: `warren-buffett-berkshire-hathaway`, `mason-hawkins-longleaf-partners`, `seth-klarman-baupost-group`, `bill-ackman-pershing-square-capital-management`.

### Step 2: Fetch both pages with web_fetch

- **Portfolio**: `https://valuesider.com/guru/{guru_slug}/portfolio`
- **Activity**: `https://valuesider.com/guru/{guru_slug}/portfolio-activity`

Call web_fetch (or equivalent) for each URL and keep the returned text content.

### Step 3: Parse content to JSON

Save the portfolio response to a temp file (e.g. `_portfolio.txt`), activity to `_activity.txt`. Then run:

```bash
# From the skill directory (gi-valuesider-superinvestor-data/)
python scripts/parse_fetched_content.py --type portfolio --file _portfolio.txt --guru-slug <guru_slug> --source-url "https://valuesider.com/guru/<guru_slug>/portfolio"
python scripts/parse_fetched_content.py --type activity --file _activity.txt --guru-slug <guru_slug> --source-url "https://valuesider.com/guru/<guru_slug>/portfolio-activity"
```

Or pipe content from stdin (no `--file`):

```bash
python scripts/parse_fetched_content.py --type portfolio --guru-slug mason-hawkins-longleaf-partners < _portfolio.txt
```

Output is JSON: portfolio has `summary` + `holdings`; activity has `activities` (quarter, ticker, stock_name, activity_type, share_change, pct_change_to_portfolio, reported_price, pct_of_portfolio).

### Step 4: Present results

Summarize `summary` (period, portfolio value, number of holdings), list top holdings or recent buys/sells from the parsed JSON. Data is from ValueSider; do not present as financial advice.

---

## Alternative: direct fetch script (when not 403)

If the environment allows (e.g. no 403), you can use the request-based script:

```bash
# List gurus (may 403)
python scripts/fetch_valuesider.py --list-gurus --limit 100

# Fetch one guru (may 403)
python scripts/fetch_valuesider.py <guru_slug>
python scripts/fetch_valuesider.py <guru_slug> --portfolio-only
python scripts/fetch_valuesider.py <guru_slug> --activity-only
```

Requires: `pip install -r requirements.txt` (requests, beautifulsoup4). On 403, use the real-time flow above instead.

## Data source

- Portfolio: `https://valuesider.com/guru/{guru_slug}/portfolio`
- Activity: `https://valuesider.com/guru/{guru_slug}/portfolio-activity`
- Guru list: `https://valuesider.com/value-investors`
