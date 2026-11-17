# google-finance-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**20 endpoints across 1 platform group(s).**

## Google (20)

### `google_finance_analyst_articles`

- **HTTP:** `GET /google/finance/analyst-articles/{quote}`
- **What:** Google Finance analyst articles. Returns the analyst articles Google Finance shows for a quote such as `AAPL:NASDAQ`. Each article has its title, source, URL, publication time (ISO and Unix), thumbnail and the related instruments with price, change and exchange. Articles come back only when Google Finance has them for that quote.
- **Params:** `quote` (string, **required**) — Quote identifier such as AAPL:NASDAQ

### `google_finance_chart`

- **HTTP:** `GET /google/finance/chart/{quote}`
- **What:** Google Finance chart data. Returns the price chart for a Google Finance quote such as `AAPL:NASDAQ` or `BTC-USD` over a window from `1d` to `max` (default `1d`). Each point has a time, price and volume; the response also carries the instrument's name, exchange, currency, current price, change and previous close.
- **Params:** `quote` (string, **required**) — Quote identifier such as AAPL:NASDAQ; `window` (string, optional) — Window: 1d, 5d, 1m, 6m, ytd, 1y, 5y, max

### `google_finance_classification`

- **HTTP:** `GET /google/finance/classification/{quote}`
- **What:** Google Finance classification data. Returns the category labels Google Finance assigns to a quote such as `AAPL:NASDAQ`, for example Technology, in `categories`. The response also carries the instrument itself: ticker, exchange, name, current price, change, previous close, currency and after-hours data.
- **Params:** `quote` (string, **required**) — Quote identifier such as AAPL:NASDAQ

### `google_finance_company`

- **HTTP:** `GET /google/finance/company/{quote}`
- **What:** Google Finance company data. Returns Google Finance company details for a quote such as `AAPL:NASDAQ`: description, CEO, employee count, headquarters, sector, market capitalisation, P/E ratio, open, day high and low, 52-week high and low, and volume.
- **Params:** `quote` (string, **required**) — Quote identifier such as AAPL:NASDAQ

### `google_finance_context`

- **HTTP:** `GET /google/finance/context`
- **What:** Find Google Finance instruments by query. Searches Google Finance for instruments matching a company name or ticker query and returns results with ticker, exchange, name, price, currency, and change data. Use a returned ticker with quote, company, chart, or news endpoints.
- **Params:** `q` (string, **required**) — Search query

### `google_finance_financials`

- **HTTP:** `GET /google/finance/financials/{quote}`
- **What:** Google Finance financial statements. Returns the financial statements Google Finance holds for a quote such as `AAPL:NASDAQ`, as `annual` and `quarterly` rows plus a `currency`. Each row has revenue, net income, EBITDA, EPS, margins, cash flow, assets, liabilities and equity. The rows are empty when Google Finance has no statement data for the quote.
- **Params:** `quote` (string, **required**) — Quote identifier such as AAPL:NASDAQ

### `google_finance_markets_category_news`

- **HTTP:** `GET /google/finance/markets/categories/{category}/news`
- **What:** Google Finance category news. Returns Google Finance news for one market category, identified by the `category` path id. Use `offset` to page through results. Each item has its title, URL and publication time (ISO and Unix), plus the source, a thumbnail and any related quotes with price, change and percent change when Google provides them. The response also echoes `category` and `offset`.
- **Params:** `category` (string, **required**) — Google Finance category id; `offset` (integer, optional) — Result offset

### `google_finance_markets_category_stocks`

- **HTTP:** `GET /google/finance/markets/categories/{category}/stocks`
- **What:** Google Finance category stocks. Lists the instruments in one Google Finance market category, chosen by the required `category` id and paged with `offset`. Each item has its ticker, exchange, name, price, change and change percent, previous close, currency, country and after-hours data.
- **Params:** `category` (string, **required**) — Google Finance category id; `offset` (integer, optional) — Result offset

### `google_finance_markets_earnings`

- **HTTP:** `GET /google/finance/markets/earnings`
- **What:** Google Finance earnings calendar. Returns the Google Finance earnings calendar. Each item has the company name, fiscal period, event time (including a Unix timestamp), conference call phone and URL when listed, and the instrument with its ticker, exchange, price and change.
- **Params:** _none_

### `google_finance_markets_featured`

- **HTTP:** `GET /google/finance/markets/featured`
- **What:** Google Finance featured stocks. Returns the stocks Google Finance features on its markets page. Each instrument has its ticker, exchange, name, price, change and change percent, previous close, currency, country, time zone and after-hours data.
- **Params:** _none_

### `google_finance_markets_headline`

- **HTTP:** `GET /google/finance/markets/headline`
- **What:** Google Finance top headline. Returns the top headline on Google Finance markets as one article: title, source, URL, publication time (ISO and Unix), thumbnail and the related instruments with price and change. The article is present only when Google Finance shows a headline.
- **Params:** _none_

### `google_finance_markets_indices`

- **HTTP:** `GET /google/finance/markets/indices`
- **What:** Google Finance market indices. Returns the market indices Google Finance lists, such as the Dow Jones Industrial Average. Each index has its ticker, exchange, name, current value, change and change percent, previous close and last update time.
- **Params:** _none_

### `google_finance_markets_movers`

- **HTTP:** `GET /google/finance/markets/movers`
- **What:** Google Finance market movers. Lists Google Finance market movers. `categories` takes comma-separated numeric categories, `count` sets how many items to return (default 20) and `offset` skips ahead. Each item has its ticker, exchange, name, price, change and change percent, and previous close.
- **Params:** `categories` (string, optional) — Comma-separated numeric categories; `count` (integer, optional) — Result count; `offset` (integer, optional) — Result offset

### `google_finance_markets_top`

- **HTTP:** `GET /google/finance/markets/top`
- **What:** Google Finance top stocks by metric. Lists the top Google Finance instruments for a ranking metric. `metric` is a Google Finance metric id (default 6) and `page` is the page number (default 1). Each item has its ticker, exchange, name, price, change and change percent, and previous close.
- **Params:** `metric` (integer, optional) — Google Finance metric id; `page` (integer, optional) — Page number

### `google_finance_markets_trending`

- **HTTP:** `GET /google/finance/markets/trending`
- **What:** Google Finance trending stocks. Returns the instruments currently trending on Google Finance, up to `limit` items (default 18). Each has its ticker, exchange, name, price, change and change percent, previous close, currency and after-hours data.
- **Params:** `limit` (integer, optional) — Result limit

### `google_finance_news`

- **HTTP:** `GET /google/finance/news/{quote}`
- **What:** Google Finance quote news. Returns recent Google Finance news for one quote, such as `AAPL:NASDAQ`, given in the `quote` path parameter. `limit` caps the number of articles and defaults to 6. Each article has its title, source, URL, publication time (ISO and Unix), thumbnail, and related quotes with price and change data.
- **Params:** `limit` (integer, optional) — Article limit; `quote` (string, **required**) — Quote identifier such as AAPL:NASDAQ

### `google_finance_quote`

- **HTTP:** `GET /google/finance/quote/{quote}`
- **What:** Google Finance Quote API. Returns the Google Finance quote page for a symbol such as `AAPL:NASDAQ` or `BTC-USD`. The response carries key stats, an about section (CEO, employees, founded, headquarters, website), news, and investment tables for the income statement, balance sheet and cash flow by quarter and year.
- **Params:** `quote` (string, **required**) — Stock symbol to fetch the latest quote for (e.g., AAPL:NASDAQ, BTC-USD)

### `google_finance_related`

- **HTTP:** `GET /google/finance/related/{quote}`
- **What:** Google Finance related instruments. Returns the instruments Google Finance lists as related to a quote such as `AAPL:NASDAQ`. The response gives the queried `instrument` and an `items` list, each with ticker, exchange, name, price, change and change percent, and previous close.
- **Params:** `quote` (string, **required**) — Quote identifier such as AAPL:NASDAQ

### `google_finance_search`

- **HTTP:** `GET /google/finance/search`
- **What:** Google Finance Search API. Searches Google Finance for instruments matching `q`, such as a company name. Each match has its ticker, exchange, company name, currency, price, change and percentage change.
- **Params:** `q` (string, **required**) — Keyword to search for (e.g., Apple)

### `google_finance_ticker`

- **HTTP:** `GET /google/finance/ticker/{ticker}`
- **What:** Google Finance Ticker API. Returns the price series Google Finance charts for a ticker such as `AAPL:NASDAQ` or `BTC-USD`. `window` sets the range: `1d` (default), `5d`, `1m`, `6m`, `ytd`, `1y`, `5y` or `max`. Each point has a `time`, `price` and `volume`.
- **Params:** `ticker` (string, **required**) — Ticker symbol to fetch data for example:AAPL:NASDAQ, BTC-USD; `window` (string, optional) — Time window for the ticker data (default: 1d), options: 1d, 5d, 1m, 6m, 1y, 5y, max
