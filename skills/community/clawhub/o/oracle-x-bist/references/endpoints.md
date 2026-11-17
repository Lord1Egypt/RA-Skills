<!-- GENERATED FILE — do not edit by hand.
     Regenerate with: python scripts/build_agent_skill.py
     Source of truth: the FastAPI route definitions in backend/routers/. -->

# Oracle-X Borsa İstanbul endpoint reference

Every path below is relative to the instance base URL (`$ORACLE_X_URL`,
default `http://localhost:8000`). Nothing here is scoped to a person, so none of it needs a token.

Request and response bodies are described by their field names and types. When
a response shape is not declared on the route, the entry says so — call it once
and read the actual JSON rather than guessing.

Only the Turkish market is here. Crypto, US equities, macro, chains, derivatives, prediction markets and the vector memory are the sibling skill `oracle-x-api`, on the same instance and the same base URL.

## Borsa İstanbul (BIST)

The Turkish market: equities, TEFAS funds, KAP filings and the macro series they are measured against.

Two things about this surface differ from the rest of the API and will produce wrong answers if assumed away. **Every return is quoted three ways.** A lira figure over a year in which consumer prices rose ~32% is not a result, so `returns`/`framed_returns` carry `nominal`, `real` (inflation-adjusted) and `usd` side by side; a null `real` means the window could not be deflated, never that inflation was zero. **Prices are delayed at least 15 minutes** — `delay_minutes` says so on every board that carries a quote.

Symbols carry the venue: `BIST:THYAO`. A bare ticker never resolves to Borsa İstanbul unless the caller asks for it explicitly.

### `GET /api/bist/overview`

Get Overview

The realm's landing board: indices, sector heat, breadth and the macro strip.

Sector performance is derived from the constituents rather than read off the
sector indices — those are published by Borsa İstanbul but absent from the
quote source, and a capitalisation-weighted roll-up of the members is what a
heatmap is asking for anyway.


Response shape is not declared on the route — inspect one call.

### `GET /api/bist/market-note`

Get Market Note

What the equity board as a whole looks like, narrated.

Deliberately not scoped to the screener's index or sector filter. The read
is whether the index and the breadth agree, which is a property of the
whole board — recomputing it per filter would answer a question nobody on
the page asked and would multiply the note cache by every combination.

`facts` carries the deterministic aggregation and renders whether or not
the sentence arrives, which is what keeps an absent note from looking like
a broken panel.


Response shape is not declared on the route — inspect one call.

### `GET /api/bist/stocks`

Get Stocks

The equity screener, with each company's one-year return in three frames.

Parameters:
- `index` (query, string?, optional) — Index code, e.g. XU100
- `sector` (query, string?, optional)
- `search` (query, string?, optional)
- `sort_by` (query, string, optional, default `'market_cap'`) — One of ('market_cap', 'change_pct', 'volume', 'traded_value', 'pe', 'pb', 'ev_ebitda', 'perf_ytd', 'perf_1y', 'rsi', 'relative_volume')
- `descending` (query, boolean, optional, default `True`)
- `limit` (query, integer, optional, default `100`)

Response shape is not declared on the route — inspect one call.

### `GET /api/bist/stocks/{ticker}`

Get Stock

One company: quote, fundamentals, index membership and a price history.

Parameters:
- `ticker` (path, string, required)
- `range` (query, string, optional, default `'1y'`) — Yahoo chart range, e.g. 6mo, 1y, 5y

Response shape is not declared on the route — inspect one call.

### `GET /api/bist/heatmap`

Get Heatmap

One index as a treemap: area is market capitalisation, colour is the
reader's choice, and VİOP open interest rides along where it exists.

The futures board is fetched inside its own `try`. It is a scrape of a
broker page and it will break; when it does the answer is this board minus
one column, not a 503. `has_futures_data` says which of the two happened, so
a tile with no open interest can be drawn as unknown rather than as zero.

Deliberately not `_equity_row`: that payload carries valuation ratios and
framed real returns, none of which a tile draws, and at a thousand listings
the unused half is most of the response.

Parameters:
- `index` (query, string, optional, default `'XU100'`) — One of ('XU100', 'XU030', 'XU050', 'XUTUM', 'XBANK', 'XKTUM', 'XK100')
- `limit` (query, integer, optional, default `150`)

Response shape is not declared on the route — inspect one call.

### `GET /api/bist/funds`

Get Funds

The fund screener.

Returns TEFAS's own published period returns rather than ones derived from
the price series: the price endpoint is per-fund, so deriving them for a
thousand funds would be a thousand round trips to reach the same figures.
Risk statistics are on the detail endpoint, where a reader has asked for one
fund.

Parameters:
- `fund_type` (query, string, optional, default `'YAT'`) — One of ('YAT', 'EMK', 'BYF')
- `umbrella` (query, string?, optional) — Şemsiye fon type, exact match
- `search` (query, string?, optional) — Substring of the code or title
- `tradable_only` (query, boolean, optional, default `True`)
- `max_risk` (query, integer?, optional)
- `sort_by` (query, string, optional, default `'1y'`) — One of ('1a', '3a', '6a', '1y', '3y', '5y', 'yb')
- `limit` (query, integer, optional, default `100`)

Response shape is not declared on the route — inspect one call.

### `GET /api/bist/funds/{code}`

Get Fund

One fund: its net asset value history and the statistics derived from it.

Parameters:
- `code` (path, string, required)
- `months` (query, integer, optional, default `12`)

Response shape is not declared on the route — inspect one call.

### `GET /api/bist/funds/{code}/holdings`

Get Fund Holdings

Which companies the fund actually owns, from its monthly KAP filing.

A separate route rather than a field on `/funds/{code}`, because the two
have nothing in common but the fund. This one costs up to four upstream
calls and a PDF parse on a cold cache, against a source that publishes once
a month; the detail page must not wait on it to draw its chart.

Always 200. An absent book is described by `reason` rather than by a status
code: "no report filed yet", "the fund holds no equity" and "this filing's
layout could not be read" are three different sentences, and a 404 would say
the same wrong thing for all three.

Parameters:
- `code` (path, string, required)
- `fund_type` (query, string, optional, default `'YAT'`) — One of ('YAT', 'EMK', 'BYF')

Response shape is not declared on the route — inspect one call.

### `GET /api/bist/funds/compare`

Get Fund Comparison

Several funds on one axis.

Declared before `/funds/{code}` on purpose: FastAPI matches in declaration
order, and the path parameter would otherwise swallow `compare` and go
looking for a fund by that name.

Parameters:
- `codes` (query, string, required) — Comma-separated fund codes, at most 8
- `months` (query, integer, optional, default `12`)

Response shape is not declared on the route — inspect one call.

### `GET /api/bist/funds/market-note`

Get Funds Market Note

What this whole fund universe looks like, narrated.

Declared above `/funds/{code}` deliberately: FastAPI matches in declaration
order, and behind it this path resolves as a fund whose code is
"market-note".

Keyed on the fund type rather than on the caller's filters. The medians and
the dispersion are computed across every fund of the type, because "half the
board lost purchasing power" is a fact about the market and the same count
over the page a reader happens to be looking at would invert it.

Never 503s. The screener beside this is already reporting whatever went
wrong from its own query, and a second error for a missing paragraph would
be reporting the same outage twice.

Parameters:
- `fund_type` (query, string, optional, default `'YAT'`) — One of ('YAT', 'EMK', 'BYF')

Response shape is not declared on the route — inspect one call.

### `GET /api/bist/macro`

Get Macro

The Turkish macro backdrop, and the deflators the rest of the realm uses.

`cpi_series` is empty without a `TCMB_EVDS_API_KEY`, which is a supported
state rather than a failure: the trailing-year deflator comes from the
published year-on-year rate and needs no key, and every longer window
reports nominal only rather than approximating.

Parameters:
- `fx_range` (query, string, optional, default `'5y'`) — Yahoo range for the USDTRY series

Response shape is not declared on the route — inspect one call.

### `GET /api/bist/macro-note`

Get Macro Note

What the backdrop as a whole says, narrated above the tiles that draw it.

Its own route rather than a field on `/macro`, for the reason every note
here is: the snapshot is cached for half an hour and the page refetches it
on demand, and a paragraph welded to the payload would either be recomputed
on every refresh or hold the tiles back to the model's cadence.

`facts` is null when the policy rate or the inflation print could not be
read — the two figures every other reading hangs off. The client renders
that as an absent panel rather than as a quiet backdrop.


Response shape is not declared on the route — inspect one call.

### `GET /api/bist/kap`

Get Kap

The most recent KAP filings.

The default view excludes `FON` — around nine filings in ten are a portfolio
manager reporting an overnight repo, forty of them stamped the same minute,
and they bury the company news a reader came for.

Parameters:
- `limit` (query, integer, optional, default `40`)
- `ticker` (query, string?, optional)
- `categories` (query, string?, optional) — Comma-separated KAP categories. Omit for the signal set (ODA, FR, DUY); pass 'all' to include fund housekeeping.

Response shape is not declared on the route — inspect one call.

### `GET /api/bist/kap/{index}/note`

Get Kap Note

What one filing means, narrated.

Written on demand rather than with the tape: the board prints six hundred
rows and a reader opens one, so generating a note per row would run a local
model continuously to write text nobody asked for.

The share behind the filing is looked up but never required. Around a fifth
of the tape carries no ticker — the exchange files its own notices this way
— and the equity board is a separate upstream that can be down, so a missing
session is a stated gap in the prompt rather than a failed request.

Parameters:
- `index` (path, integer, required)

Response shape is not declared on the route — inspect one call.

### `GET /api/bist/restrictions`

Get Restrictions

Exchange measures: circuit breakers, gross settlement, short-selling bans.

Filtered out of the KAP tape rather than fetched separately — Borsa
İstanbul files these as ordinary disclosures with fixed titles, and there is
no feed of measures on its own.

Parameters:
- `limit` (query, integer, optional, default `30`)

Response shape is not declared on the route — inspect one call.

### `GET /api/bist/calendar`

Get Calendar

Results announcements and ex-dividend dates.

Rights and bonus issues are absent on purpose: they are announced through
KAP as prose with no structured date anywhere, so they appear on the
disclosure tape as filings rather than here as calendar rows. A partial
calendar that looked complete would be worse than one that says what it
covers.

Parameters:
- `days_ahead` (query, integer, optional, default `90`)
- `days_back` (query, integer, optional, default `14`)
- `kinds` (query, string?, optional) — Comma-separated: earnings, dividend

Response shape is not declared on the route — inspect one call.

### `GET /api/bist/viop`

Get Viop

Futures and options, with the open interest behind each contract.

Parameters:
- `underlying` (query, string?, optional)

Response shape is not declared on the route — inspect one call.

### `GET /api/bist/viop-note`

Get Viop Note

What the derivatives board says as a whole, above the panels that draw it.

Its own endpoint rather than a field on `/viop`, for the reason
`positioning-note` records: that board is cached for five minutes and the
page polls it, and a note welded to the payload would either be recomputed
on every poll or hold the board back to the note's cadence. Split, each
keeps its own.

`facts` is null when the board could not be read or came back too thin to
describe. The client must render that as an absent panel rather than as a
quiet session — this source is a scrape, and silence here is far more often
an outage than a market.


Response shape is not declared on the route — inspect one call.

### `GET /api/bist/viop-map/underlyings`

Get Viop Map Underlyings

The single-stock futures universe, ranked by the newest session's turnover.

Derived rather than listed: which names carry futures, and which of them are
worth opening first, both change without notice, and a hardcoded list is a
list that silently goes stale. `default` is what the picker starts with.


Response shape is not declared on the route — inspect one call.

### `GET /api/bist/viop-map/{ticker}`

Get Viop Map

One underlying's positioning, and the scan band each cohort sits behind.

Two layers on one price axis: the VİOP book, modelled only in its direction,
and the spot volume profile, modelled not at all. They share a grid because
they are read against each other.

The failure modes are deliberately unequal. Without the bulletin there is no
book and without Takasbank's scan range there is no band, so either missing
is a 503 — the distance is a published number and this endpoint will not
substitute one. Losing Yahoo's intraday history costs the second layer only,
and the map still answers.

Parameters:
- `ticker` (path, string, required)
- `sessions` (query, integer, optional, default `120`)
- `bins` (query, integer, optional, default `120`)

Response shape is not declared on the route — inspect one call.

### `GET /api/bist/viop-map/{ticker}/note`

Get Viop Map Note

Where this underlying's book stands against its scan range, narrated.

Scoped the way the map is — one underlying, one window — and fingerprinted
on both plus the newest session day, so a note about one name over one
window is never served for another. Split from `/viop-map/{ticker}` for
the reason every note here is: the field is polled at the equity cadence
and the paragraph is written once a session.

`facts` is null when the book is too thin to draw or one of its three
upstreams did not answer. Never a 404 or a 503: the page has already drawn
or declined the field on its own, and a note's absence is a paragraph.

Parameters:
- `ticker` (path, string, required)
- `sessions` (query, integer, optional, default `120`)

Response shape is not declared on the route — inspect one call.

### `GET /api/bist/positioning`

Get Positioning

Where the crowd is: free float, unusual volume, range position, futures OI.

Not the fund-to-stock cross index this board was originally meant to be.
TEFAS publishes a fund's split by asset class — the fund board draws it —
but nothing public names the securities behind it, and KAP publishes
holdings only as prose attachments. `positioning_service` documents what was
tried. What is here is published positioning rather than inferred, which is
a narrower claim honestly made.

Parameters:
- `limit` (query, integer, optional, default `50`)

Response shape is not declared on the route — inspect one call.

### `GET /api/bist/positioning-note`

Get Positioning Note

What the positioning board as a whole looks like, narrated.

Its own route rather than a field on `/positioning`, for the reason every
note here is: the board polls every two minutes and the paragraph is written
once, so folding them together would either hold the board behind a model
run or refuse the note a cadence of its own.

Deliberately not scoped to the caller's `limit`. `/positioning` returns rows
ranked by crowding, so any limit is a biased sample by construction — the
facts are computed across every listing instead, because "the board is at the
top of its year" answered over the busiest hundred names is a wrong answer
rather than a narrower one.


Response shape is not declared on the route — inspect one call.

### `GET /api/bist/ownership/board`

Get Bist Ownership Board

Every tracked holder with its XU100 stakes, valued at the latest market cap.


Returns `models__bist_ownership__OwnershipBoard`: `entities`, `latest_moves`, `latest_stake_moves`, `tracking_since`, `category_counts`, `sources`, `universe`, `tickers_covered`, `tickers_total`, `as_of`, `last_refresh_at`, `stale`

### `GET /api/bist/ownership/entities/{entity_id}`

Get Bist Ownership Entity

One holder: every stake, the filings on those companies, and the sources.

Parameters:
- `entity_id` (path, string, required)

Returns `models__bist_ownership__EntityDetail`: `entity`, `positions`, `moves`, `stake_moves`, `sources`, `tracking_since`

### `GET /api/bist/ownership/assets/{ticker}`

Get Bist Asset Owners

Who holds one company.

Every ≥5% holder from the card, tracked or not; the registry funds whose
latest report names the ticker; and the ownership-shaped filings on the
KAP tape. 404 outside the XU100 rather than an empty holder list.

Parameters:
- `ticker` (path, string, required)

Returns `AssetOwners`: `ticker`, `name`, `market_cap`, `free_float_pct`, `foreign_ratio_pct`, `holders`, `funds`, `moves`, `stake_moves`, `tracking_since`, `as_of`, `stale`, …

### `GET /api/bist/ownership/moves`

Get Bist Ownership Moves

Ownership-shaped KAP filings, newest first. The one route allowed to be empty.

Parameters:
- `limit` (query, integer, optional, default `20`)
- `ticker` (query, string?, optional) — Bare code or BIST:CODE

Returns `models__bist_ownership__Move[]`.

### `GET /api/bist/ownership/note`

Get Bist Ownership Note

What the whole board says, narrated.

Its own route rather than a field on `/board`, for the reason every note on
this realm is: the board is read on every visit and the paragraph is written
once a day, so folding them together would hold the grid behind a model run.
`facts` is null when the board is missing or too thin, and the note then
says `insufficient_data` rather than describing an index nobody holds.


Response shape is not declared on the route — inspect one call.

### `POST /api/bist/radar/scan`

Start Radar Scan

Scan the XU100 for pullbacks inside uptrends, in the background.

Returns the job to poll. A scan already running for this horizon is joined
rather than duplicated; a scan that just finished is returned with a 200 so
the client can read its result straight away.

Parameters:
- `horizon` (query, string, optional, default `'swing'`)

Response shape is not declared on the route — inspect one call.

### `GET /api/bist/radar/jobs/{job_id}`

Get Radar Job

Poll a scan for its stage, its progress and — once done — its result.

Parameters:
- `job_id` (path, string, required)

Response shape is not declared on the route — inspect one call.

### `DELETE /api/bist/radar/jobs/{job_id}`

Cancel Radar Scan

Stop a running scan.

A scan started on the wrong horizon, or by a stray click, should not have to
run its minute out. The settled job is returned so the button that asked
sees the outcome without another poll; the last persisted result is left
untouched, since a cancelled scan wrote nothing.

Parameters:
- `job_id` (path, string, required)

Response shape is not declared on the route — inspect one call.

### `GET /api/bist/radar`

Get Radar

The last finished scan for a horizon.

404 rather than an empty board when none has ever run: the page then shows
the button and says so, instead of a result that reads as "nothing passed".

Parameters:
- `horizon` (query, string, optional, default `'swing'`)

Response shape is not declared on the route — inspect one call.
