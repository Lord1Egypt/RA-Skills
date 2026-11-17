# Polymarket API Reference

## Base URLs

| API | Base URL | Purpose |
|-----|----------|---------|
| Gamma API | `https://gamma-api.polymarket.com` | Markets, events, sports metadata, series, tournaments |
| CLOB API | `https://clob.polymarket.com` | Order book, prices, trading data |

## API Change Notes (July 2026)

The Polymarket Gamma API has changed significantly. Key changes:
- **REMOVED**: `/categories` endpoint (HTTP 404) — use `/sports` + `/tags` instead
- **REMOVED**: `/leagues`, `/countries`, `/competitions`, `/fixtures`, `/matches` endpoints
- **NEW**: `/sports` — sports metadata (306 entries: sport slug, image, resolution source, series ID, tag IDs)
- **NEW**: `/series` — series data (NFL, NBA, MLB, etc.) with nested events
- **NEW**: `/tournaments` — tournament data (March Madness, World Cup) with phases/sections/games
- **NEW**: `/tags` — tag list (player/team/topic tags)
- **CHANGED**: Event `tags` field is now an array of objects `{id, label, slug, forceShow, ...}` (was string)
- **CHANGED**: `gameStartTime` is now only present at the **market** level for game markets (not at the event level)
- **CHANGED**: The `category` query parameter on `/markets` still works but may return loosely-related markets (e.g., World Cup props appear under `category=sports` and `category=politics`). Tag-based filtering via `/markets?tag=<slug>` is more precise but returns smaller result sets.

## Key Endpoints

### Categories / Metadata (updated)
- `GET /sports?limit=N` — List sports metadata (replaces `/categories`)
- `GET /series?limit=N&active=true` — List series (NFL/NBA/etc.)
- `GET /tournaments?limit=N` — List tournaments (March Madness, World Cup)
- `GET /tags?limit=N` — List tags (players, teams, topics)

### Markets
- `GET /markets?limit=N&active=true&closed=false&order=volume24hr&ascending=false` — Active markets sorted by volume
- `GET /markets/{id}` — Single market details
- `GET /markets?category={slug}` — Markets by category (note: results may be loose)
- `GET /markets?tag={slug_or_id}` — Markets by tag (more precise than category)
- `GET /markets?event_id={id}` — Markets belonging to an event
- `GET /markets?slug={slug}` — Market by slug

### Events
- `GET /events?limit=N&active=true&closed=false` — List events
- `GET /events/{id}` — Event with sub-markets
- `GET /events?slug={slug}` — Event by slug

### CLOB (Order Book)
- `GET /book?token_id={tokenId}` — Order book for a token
- `GET /midpoint?token_id={tokenId}` — Midpoint price (requires valid token_id)
- `GET /spread?token_id={tokenId}` — Current spread
- `GET /price?token_id={tokenId}&side={buy|sell}` — Price for a side
- `GET /markets` — CLOB markets list

## Removed Endpoints (do not use)
- ~~`GET /categories`~~ — Returns HTTP 404
- ~~`GET /leagues`~~ — Returns HTTP 404
- ~~`GET /countries`~~ — Returns HTTP 404
- ~~`GET /competitions`~~ — Returns HTTP 404
- ~~`GET /fixtures`~~ — Returns HTTP 404
- ~~`GET /matches`~~ — Returns HTTP 404
- ~~`GET /tickers` (CLOB)~~ — Returns HTTP 404

## Market Data Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique market ID |
| `question` | string | Market question/title |
| `conditionId` | string | Condition ID (UMA) |
| `slug` | string | URL slug |
| `outcomes` | string (JSON array) | Outcome names, e.g. `["Yes", "No"]` |
| `outcomePrices` | string (JSON array) | Prices (0-1), e.g. `["0.65", "0.35"]` — multiply by 100 for percentage odds |
| `volumeNum` | number | Total trading volume in USD |
| `volume24hr` | number | 24-hour trading volume |
| `volume1wk` | number | Weekly trading volume |
| `volume1mo` | number | Monthly trading volume |
| `volume1yr` | number | Yearly trading volume (new) |
| `volumeClob` | number | CLOB volume (new) |
| `volume24hrClob` | number | 24h CLOB volume (new) |
| `liquidityNum` | number | Available liquidity in USD |
| `liquidityClob` | number | CLOB liquidity (new) |
| `openInterest` | number | Open interest in USD |
| `active` | boolean | Whether market is active |
| `closed` | boolean | Whether market is closed |
| `acceptingOrders` | boolean | Whether orders are being accepted |
| `acceptingOrdersTimestamp` | string | When orders started being accepted (new) |
| `endDate` / `endDateIso` | string | Market end date |
| `startDate` / `startDateIso` | string | Market start date |
| `gameStartTime` | string | For sports games: game start time (market-level only, not event-level) |
| `category` | string | Category name (legacy field) |
| `description` | string | Market description/rules |
| `negRisk` | boolean | Negative risk market |
| `negRiskRequestID` | string | Neg risk request ID (new) |
| `negRiskOther` | boolean | Neg risk other (new) |
| `clobTokenIds` | string (JSON array) | Token IDs for CLOB queries |
| `oneDayPriceChange` | number | 1-day price change (decimal) |
| `oneWeekPriceChange` | number | 1-week price change (decimal) |
| `oneMonthPriceChange` | number | 1-month price change (decimal) |
| `lastTradePrice` | number | Last trade price |
| `bestBid` | number | Best bid price |
| `bestAsk` | number | Best ask price |
| `spread` | number | Bid-ask spread (decimal) |
| `events` | array | Nested events list (new — markets now embed their events) |
| `comboStatus` | string | Combo market status (new) |
| `competitive` | number | Competitive score (new) |
| `cyom` | boolean | Check Your Own Markets flag (new) |
| `automaticallyActive` | boolean | Auto-active flag (new) |
| `rfqEnabled` | boolean | RFQ (Request for Quote) enabled (new) |
| `holdingRewardsEnabled` | boolean | Holding rewards enabled (new) |
| `feesEnabled` | boolean | Fees enabled (new) |
| `feeType` | string | Fee type (new) |
| `feeSchedule` | string | Fee schedule (new) |
| `makerBaseFee` | number | Maker base fee (new) |
| `takerBaseFee` | number | Taker base fee (new) |
| `requiresTranslation` | boolean | Translation required flag (new) |
| `pendingDeployment` | boolean | Pending deployment flag (new) |
| `deploying` | boolean | Currently deploying flag (new) |
| `deployingTimestamp` | string | Deployment timestamp (new) |
| `gmpChartMode` | string | GMP chart mode (new) |
| `showGmpSeries` | boolean | Show GMP series (new) |
| `showGmpOutcome` | boolean | Show GMP outcome (new) |
| `manualActivation` | boolean | Manual activation flag (new) |
| `clearBookOnStart` | boolean | Clear book on start flag (new) |
| `rewardsMinSize` | number | Rewards minimum size (new) |
| `rewardsMaxSpread` | number | Rewards maximum spread (new) |
| `approved` | boolean | Approved flag (new) |
| `pagerDutyNotificationEnabled` | boolean | PagerDuty notification flag (new) |

## Event Data Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique event ID |
| `ticker` | string | Event ticker (new) |
| `slug` | string | URL slug |
| `title` | string | Event title |
| `description` | string | Event description |
| `volume` | number | Total volume |
| `liquidity` | number | Total liquidity |
| `liquidityClob` | number | CLOB liquidity (new) |
| `openInterest` | number | Total open interest |
| `volume24hr` | number | 24h volume |
| `volume1wk` | number | Weekly volume (new) |
| `volume1mo` | number | Monthly volume (new) |
| `volume1yr` | number | Yearly volume (new) |
| `markets` | array | Array of sub-market objects |
| `tags` | array | **Array of tag objects** `{id, label, slug, forceShow, forceHide, ...}` (changed from string) |
| `competitive` | number | Competitive score |
| `commentCount` | number | Comment count (new) |
| `cyom` | boolean | Check Your Own Markets flag (new) |
| `enableNegRisk` | boolean | Enable neg risk flag (new) |
| `negRiskAugmented` | boolean | Neg risk augmented flag (new) |
| `showAllOutcomes` | boolean | Show all outcomes flag (new) |
| `showMarketImages` | boolean | Show market images flag (new) |
| `automaticallyActive` | boolean | Auto-active flag (new) |
| `eventMetadata` | object | Event metadata including `context_description` (new) |
| `requiresTranslation` | boolean | Translation required flag (new) |
| `pendingDeployment` | boolean | Pending deployment flag (new) |
| `deploying` | boolean | Currently deploying flag (new) |

## Sports Metadata Fields (`/sports`)

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique sport ID |
| `sport` | string | Sport slug (e.g., `nba`, `nfl`, `epl`, `lal`) |
| `image` | string | Image URL |
| `resolution` | string | Resolution source URL |
| `ordering` | string | Display ordering (`home`, etc.) |
| `tags` | string | Comma-separated tag IDs |
| `series` | string | Linked series ID |
| `createdAt` | string | Creation timestamp |

## Series Fields (`/series`)

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique series ID |
| `ticker` | string | Series ticker (e.g., `nfl`, `nba`) |
| `slug` | string | URL slug |
| `title` | string | Series title |
| `seriesType` | string | Series type (`single`, etc.) |
| `recurrence` | string | Recurrence pattern (`daily`, etc.) |
| `description` | string | Series description |
| `layout` | string | Layout type |
| `active` | boolean | Active flag |
| `closed` | boolean | Closed flag |
| `restricted` | boolean | Restricted flag |
| `volume24hr` | number | 24h volume |
| `startDate` | string | Start date |
| `events` | array | Nested events list |

## Tournament Fields (`/tournaments`)

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique tournament ID |
| `name` | string | Tournament name (e.g., "March Madness 2026", "World Cup") |
| `numEntrants` | integer | Number of entrants |
| `phases` | array | Array of tournament phases |
| `phases[].id` | integer | Phase ID |
| `phases[].tournamentId` | integer | Tournament ID |
| `phases[].roundSize` | integer | Round size (64, 32, 16, 8, 4, 2) |
| `phases[].phaseType` | string | Phase type (`knockout`, `placement`) |
| `phases[].displayName` | string | Display name (e.g., "First Round", "Final") |
| `phases[].sortOrder` | integer | Sort order |
| `phases[].sections` | array | Sections (e.g., regions like "East") |
| `phases[].sections[].games` | array | Games in the section |
| `phases[].sections[].games[].startTime` | string | Game start time |
| `phases[].sections[].games[].teamA` | object | Team A data |
| `phases[].sections[].games[].teamB` | object | Team B data |
| `phases[].sections[].games[].eventSlug` | string | Linked event slug |
| `phases[].sections[].games[].seedA` / `seedB` | integer | Team seeds |

## Tag Fields (`/tags`)

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique tag ID |
| `label` | string | Tag label (e.g., "Caitlin Clark", "Sports") |
| `slug` | string | URL slug |
| `forceShow` | boolean | Force show flag |
| `forceHide` | boolean | Force hide flag |
| `publishedAt` | string | Publication timestamp |
| `createdAt` | string | Creation timestamp |
| `updatedAt` | string | Last update timestamp |
| `requiresTranslation` | boolean | Translation required flag |

## Known Category Slugs (legacy, may still work as `category` query param)

### Top-level categories (legacy):
- `sports` — Sports
- `politics` — Politics
- `crypto` — Crypto
- `business` — Business
- `coronavirus` — Coronavirus
- `entertainment` — Entertainment
- `science` — Science
- `tech` — Tech

> ⚠️ Note: The `category` parameter still works but may return loosely-related markets. For precise sport filtering, use the slug-prefix approach (e.g., iterate `/events` and filter by slug prefix `nba-`, `nfl-`, etc.).

### Sport slugs (from `/sports` endpoint, 306 entries as of July 2026):
Popular ones: `nba`, `nfl`, `mlb`, `nhl`, `epl`, `lal` (La Liga), `bun` (Bundesliga), `fl1` (Ligue 1), `sea` (Serie A), `ucl` (Champions League), `uel` (Europa League), `ueu` (Conference League), `wnba`, `cfb` (College Football), `ncaab` (March Madness), `ipl` (Cricket), `atp`, `wta`, `ufc`, `f1`, `pga`, `boxing`, `mls`, `acn` (Africa Cup of Nations), `afcf` (AFC Asian Cup), `con` (CONCACAF), `lib` (Copa Libertadores), `sud` (Copa Sudamericana)

### Game event slug prefixes (used by `schedule` command):
The `schedule` command filters events by slug prefix. Key prefixes:
- `nba-` — NBA games (e.g., `nba-lal-okc-2026-05-05`)
- `nfl-` — NFL games
- `mlb-` — MLB games
- `nhl-` — NHL games
- `epl-` — English Premier League
- `lal-` — La Liga
- `serie-` — Serie A
- `bundes-` — Bundesliga
- `ligue-` — Ligue 1
- `fifwc-` — **FIFA World Cup** (e.g., `fifwc-esp-bel-2026-07-10`)
- `ucl-` — UEFA Champions League
- `uel-` — UEFA Europa League
- `ueu-` — UEFA Conference League
- `ufc-` — UFC fights
- `atp-` — ATP Tennis
- `wta-` — WTA Tennis
- `f1-` — Formula 1
- `pga-` — PGA Golf
- `boxing-` — Boxing (uses `-vs-` pattern)

> **Soccer prefix note**: The `soccer` keyword in the script maps to all major soccer prefixes (`epl`, `lal`, `serie`, `bundes`, `ligue`, `fifwc`, `ucl`, `uel`, `ueu`). Use `worldcup`/`fifawc`/`fifa`/`wc` for World Cup matches only.

## Query Parameters

| Param | Values | Description |
|-------|--------|-------------|
| `limit` | integer | Number of results (default varies) |
| `offset` | integer | Pagination offset |
| `active` | `true/false` | Filter by active status |
| `closed` | `true/false` | Filter by closed status |
| `order` | field name | Sort field |
| `ascending` | `true/false` | Sort direction |
| `category` | slug string | Filter by category (loose matching) |
| `tag` | slug or ID | Filter by tag (more precise) |
| `event_id` | event ID | Filter markets by event |
| `slug` | slug string | Filter by exact slug |

## Workflow Tips

1. **For sport schedules**: Use the slug-prefix approach — iterate `/events?order=volume24hr` and filter client-side by slug prefix (e.g., `nba-`, `nfl-`). This is what the `schedule` command does.
2. **For live games**: Look for markets where `gameStartTime` is within ±1 hour of current UTC time. The `live` command does this.
3. **For tournament brackets**: Query `/tournaments` to get phases/sections/games with team seeds and event slugs.
4. **For series data**: Query `/series` to get series metadata and nested events.
5. **For sports metadata**: Query `/sports` to map sport slugs to series IDs and tag IDs.
