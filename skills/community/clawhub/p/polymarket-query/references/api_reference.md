# Polymarket API Reference

## Base URLs

| API | Base URL | Purpose |
|-----|----------|---------|
| Gamma API | `https://gamma-api.polymarket.com` | Markets, events, categories metadata |
| CLOB API | `https://clob.polymarket.com` | Order book, prices, trading data |

## Key Endpoints

### Categories
- `GET /categories?limit=100` — List all categories

### Markets
- `GET /markets?limit=N&active=true&closed=false&order=volume24hr&ascending=false` — Active markets sorted by volume
- `GET /markets/{id}` — Single market details
- `GET /markets?category={slug}` — Markets by category
- `GET /markets?tag={keyword}` — Search by tag

### Events
- `GET /events?limit=N&active=true&closed=false` — List events
- `GET /events/{id}` — Event with sub-markets

### CLOB (Order Book)
- `GET /book?token_id={tokenId}` — Order book for a token
- `GET /midpoint?token_id={tokenId}` — Midpoint price
- `GET /spread?token_id={tokenId}` — Current spread

## Market Data Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique market ID |
| `question` | string | Market question/title |
| `outcomes` | string (JSON array) | Outcome names, e.g. `["Yes", "No"]` |
| `outcomePrices` | string (JSON array) | Prices (0-1), e.g. `["0.65", "0.35"]` — multiply by 100 for percentage odds |
| `volumeNum` | number | Total trading volume in USD |
| `volume24hr` | number | 24-hour trading volume |
| `volume1wk` | number | Weekly trading volume |
| `liquidityNum` | number | Available liquidity in USD |
| `openInterest` | number | Open interest in USD |
| `active` | boolean | Whether market is active |
| `closed` | boolean | Whether market is closed |
| `acceptingOrders` | boolean | Whether orders are being accepted |
| `endDate` / `endDateIso` | string | Market end date |
| `startDate` / `startDateIso` | string | Market start date |
| `gameStartTime` | string | For sports: game start time |
| `category` | string | Category name |
| `description` | string | Market description/rules |
| `slug` | string | URL slug |
| `negRisk` | boolean | Negative risk market |
| `clobTokenIds` | string (JSON array) | Token IDs for CLOB queries |
| `oneDayPriceChange` | number | 1-day price change (decimal) |
| `oneWeekPriceChange` | number | 1-week price change (decimal) |
| `oneMonthPriceChange` | number | 1-month price change (decimal) |
| `lastTradePrice` | number | Last trade price |
| `bestBid` | number | Best bid price |
| `bestAsk` | number | Best ask price |
| `spread` | number | Bid-ask spread (decimal) |

## Event Data Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique event ID |
| `title` | string | Event title |
| `slug` | string | URL slug |
| `description` | string | Event description |
| `volume` | number | Total volume |
| `liquidity` | number | Total liquidity |
| `openInterest` | number | Total open interest |
| `volume24hr` | number | 24h volume |
| `markets` | array | Array of sub-market objects |
| `competitive` | number | Competitive score |

## Category Slugs

### Top-level categories:
- `sports` — Sports
- `politics` — Politics
- `crypto` — Crypto
- `business` — Business
- `coronavirus` — Coronavirus
- `entertainment` — Entertainment
- `science` — Science
- `tech` — Tech

### Sports sub-categories:
- `basketball`, `soccer`, `baseball`, `hockey`, `racing`, `olympics`, `poker`, `mma`, `tennis`, `golf`, `boxing`, `football`

### Crypto sub-categories:
- `prices`, `defi`, `nfts`, `exploits`, `exchanges`

### Business sub-categories:
- `inflation`, `fed-interest-rates`, `commodity-prices`, `forex`, `unemployment`, `finance`, `travel`

### Politics sub-categories:
- `us-politics`, `world-politics`, `elections`

## Query Parameters

| Param | Values | Description |
|-------|--------|-------------|
| `limit` | integer | Number of results (default varies) |
| `active` | `true/false` | Filter by active status |
| `closed` | `true/false` | Filter by closed status |
| `order` | field name | Sort field |
| `ascending` | `true/false` | Sort direction |
| `category` | slug string | Filter by category |
| `tag` | keyword | Search by tag |
