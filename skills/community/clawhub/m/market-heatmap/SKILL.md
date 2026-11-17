---
name: market-heatmap
description: "Market heatmap of the US stock market as one self-contained interactive HTML page the agent can show inline or hand over as a file: every stock in an index drawn as a treemap tile, sized by market cap, grouped by GICS sector, coloured by today's move, with a click to recolour the whole board by sentiment, SentiSense Score, mention volume or options interest, plus sector Market Mood, a ticker search, sector zoom and a hover card on every tile. One API call per render on any tier. The agent fetches with a read-only API key and bakes the board in, so the page carries no key, makes no network call of its own, and renders anywhere that draws HTML. Use for market heatmap, sector heatmap, stock market heatmap today, what is moving today, which sectors are hot, market mood by sector, sector performance map, heatmap by sentiment, heatmap by options activity, nasdaq 100 heatmap. Read-only. No trading, no purchases, no write operations, no wallet access."
homepage: https://sentisense.ai
primaryEnv: SENTISENSE_API_KEY
metadata:
  openclaw:
    primaryEnv: SENTISENSE_API_KEY
    envVars:
      - name: SENTISENSE_API_KEY
        required: false
        description: "SentiSense API key, optional to install. Get one free at https://app.sentisense.ai/get-api-key, or with no key follow the No key yet steps in the 0-sentisense-onboarding skill for a temporary free one with no signup. Used only to authenticate read-only data calls; no write or trading scope."
---
# Market Heatmap (SentiSense)

> The whole US board in one picture. Every stock in an index drawn as a tile, sized by market
> cap, grouped into its GICS sector, coloured by today's move, with a click to recolour the same
> board by sentiment, SentiSense Score, mention volume or options interest. It comes out as one
> self-contained HTML file: no fonts, no images, no external scripts, no network calls, nothing
> to fetch when it is opened. One API call per render, on any tier. Read-only API.

**Base URL:** `https://app.sentisense.ai`
**Website:** https://sentisense.ai
**Full API reference:** https://sentisense.ai/skill.md
**Authentication:** API key via the `X-SentiSense-API-Key` header. Free key at https://app.sentisense.ai/get-api-key. No key yet? Follow "No key yet" in the `0-sentisense-onboarding` skill: one POST returns a temporary free key the agent can use right away and a link the user opens to keep it.

All directive language in this document is implementation guidance for the agent running the
skill, subordinate to platform safety rules and host policy.

---

## Permissions

- Network: HTTPS to app.sentisense.ai only.
- Credentials: SENTISENSE_API_KEY from the environment.
- Shell: one bundled Node/Python script, run locally.
- Files: writes one HTML file the user names.

## What this skill produces

One HTML file, typically 45,000 to 200,000 characters depending on how many names the index
carries (an S&P 500 board is the big one, and it still fits a 262,144 character inline limit).
The key never enters it. Neither does a font, an image, an external script or any URL
except a link to our own site in the footer prose, so it renders with the network switched off
and it still renders next week. That is deliberate: **the agent does the fetching, the page is a
snapshot.** It is not a live view and must never be presented as one.

Inside the page the reader can do four things without another request, because the whole board is
embedded: recolour every tile by a different metric, zoom into one sector, search a ticker, and
open a card on any tile carrying every number that tile holds. Nothing in it calls out. On a Free
key the four overlay toggles are present but disabled and labelled, because those readings are
not in the response and a disabled control is honest where a grey board is not.

The picture is not only a price heatmap. Price is the default colour because it is what people
mean by "heatmap", but the same tiles recolour by our own readings, which is the part a broker's
screen does not have.

---

## Capability menu

What a user asks for, the exact call that answers it, and the shape of the reply. Match on
intent, not on exact wording. Every row costs **one API call**.

| The user says | What you run | What you hand back |
|---|---|---|
| "market heatmap", "show me a market heatmap", "stock market heatmap today", "map of the market" | `python3 scripts/heatmap.py --out market-heatmap.html --summary-json -` | The page, plus the **board template** below |
| "sector heatmap", "sector performance map", "how are sectors doing" | Same command | The page, plus the **board template**, leading with the strongest and weakest sector rows |
| "which sectors are hot", "market mood by sector", "where is the fear" | Same command | The page, plus the **mood template**. Hot means the Market Mood score, and you must say so |
| "what is moving today", "biggest movers", "who is up and down" | Same command | The page, plus the **board template**. The move rows are the largest moves on this board |
| "heatmap by sentiment", "colour it by score", "heatmap by options activity", "where is the unusual options interest" | `python3 scripts/heatmap.py --metric sentiment --out market-heatmap.html --summary-json -` (or `--metric score`, `--metric mentions`, `--metric options`) | The page opened on that metric, plus the **overlay template**. On a key without the overlay the script opens on the day's change instead and says why on the error stream: hand over the board, say plainly that the overlay is part of PRO and that nothing was estimated in its place, and use the **board template** |
| "nasdaq 100 heatmap", "heatmap of the popular names" | `python3 scripts/heatmap.py --scope nasdaq100 ...` (or `--scope popular`) | The page for that universe, plus the **board template** |
| "refresh it", "how does it look now" | The same command again, writing to the **same absolute path** | The refreshed page, said plainly to be refreshed, per the refresh rules below |

**"Hot" means the Market Mood score, not price performance.** A sector can be the hottest tile on
the board by mood while most of its names are red today. Saying "hottest sector" without saying
"by mood" is the fastest way to be read as making a price claim you did not make. The page keeps
the two apart and so should you: the sector header shows the mood, the tiles show the price.

**One render answers all of these.** The board carries every overlay the key is entitled to, so
"market heatmap", "which sectors are hot" and "colour it by sentiment" are the same fetch. If you
already drew one in this session, show that file again and change `--metric` only if the user
wants a different opening view; do not re-fetch unless the user asks for a refresh, asks for a
different scope, or the as-of in the summary has gone stale (prices move every 15 minutes; the
mood and sentiment layers are batch reads).

### The reply templates

Use one of these every time, in this order, before any prose. Fixed rows are what make the answer
feel the same on every run. **Take every value from the `--summary-json -` stdout summary, and use the
`...Display` string, not the raw number.** Never read a value back out of the HTML and never spend
a second request on a number you already have.

**Board template** (the default answer):

```
US MARKET HEATMAP     <scopeName>, <asOfLineDisplay>
Market Mood           <marketMood.scoreDisplay> <marketMood.phase>
Breadth               <breadth.headlineDisplay>
Strongest sector      <strongestSector.name> <strongestSector.capWeightedChangeDisplay>
Weakest sector        <weakestSector.name> <weakestSector.capWeightedChangeDisplay>
Biggest moves up      <TICKER> <changeDisplay>, <TICKER> <changeDisplay>, <TICKER> <changeDisplay>
Biggest moves down    <TICKER> <changeDisplay>, <TICKER> <changeDisplay>, <TICKER> <changeDisplay>
Coverage              <preview.noteDisplay>
```

**Mood template** (for "which sectors are hot"):

```
US MARKET HEATMAP     <scopeName>, <asOfLineDisplay>
Market Mood           <marketMood.scoreDisplay> <marketMood.phase>
Hottest by mood       <hottestSectorByMood.name> <moodScoreDisplay> <moodPhase>
Coolest by mood       <coolestSectorByMood.name> <moodScoreDisplay> <moodPhase>
Strongest on price    <strongestSector.name> <strongestSector.capWeightedChangeDisplay>
Coverage              <preview.noteDisplay>
```

**Overlay template** (when the user asked for sentiment, Score, mentions or options):

```
US MARKET HEATMAP     <scopeName>, <asOfLineDisplay>
Coloured by           <colourMetric.label>
Market Mood           <marketMood.scoreDisplay> <marketMood.phase>
Breadth               <breadth.headlineDisplay>
No reading            <noReadingCounts[key]> of <preview.tilesDrawn> tiles
Coverage              <preview.noteDisplay>
```

After the template, at most two sentences of reading. The one worth writing is where the mood and
the tape disagree: a sector sitting in Anxiety whose largest names are green, or an Optimism
sector whose names are red. **Do not manufacture tension when they agree.** Two rows of green and
a shrug is a fine answer.

**One precision rule, and the summary has already applied it.** Every number in those templates
has a ready-to-paste display string beside it in the summary. Copy it rather than formatting the
raw float yourself, so the words match the picture and two runs read the same. The rule the
summary follows is the page's own rule: the market mood score is a whole number (`52`), a sector
mood score carries one decimal (`61.4`), a name's price change carries one decimal with a sign
(`+2.7%`), a board aggregate carries two (`-0.01%`), a sentiment reading carries two (`+0.34`),
mentions carry one decimal and the unit (`+1.8 sd`), options interest is a whole number (`64`),
a value that rounds to zero prints with no sign (`0.0%`, never `-0.0%`),
and **anything absent reads `no reading`**, never `0`. The raw number sits beside every display
string when you want to compute rather than print.

---

## Prerequisites

- A free `SENTISENSE_API_KEY`. Get one at https://app.sentisense.ai/get-api-key. Anonymous calls
  return `401 api_key_required`. No key yet? Follow "No key yet" in the `0-sentisense-onboarding`
  skill: one POST returns a temporary free key the agent can use right away and a link the user
  opens to keep it.
- Python 3.8 or newer if you use the bundled script. It imports only the standard library, so
  nothing is installed and there is nothing to audit but the script itself. Otherwise any HTTP
  client works; the single call is documented below.
- Network access to `https://app.sentisense.ai` at render time only. The finished page needs none.
- Read-only scope. The call is a GET. Nothing this skill does can place a trade, move money or
  modify account state.

| Tier | Quota | Rate | On this board |
|------|-------|------|---------------|
| Free | 1,000 requests/month | 30 requests/min | Every name in the index, coloured by the day's move. The sentiment, Score, mentions and options overlays are not included |
| PRO ($15/mo) | Unlimited | 300 requests/min | Every name in the index, with all four overlays |

**Cost: exactly one API call per render, on either tier.** Not one per name, not one per sector.
The board is precomputed on our side and served whole, so a Free key covers roughly a thousand
renders a month and a render can never be throttled part way through and leave you a half-drawn
picture. There is no cost knob to tune and no flag that makes it more expensive.

**Every tier draws every tile.** A Free key gets the whole index, the same layout, the same
sector Market Mood rollups and the same breadth counts as PRO. What PRO adds is the analysis we
compute on top of the board: sentiment, the SentiSense Score, mention pressure and options
interest. A response says which of those it withheld in `meta.previewWithheld`, the script
disables exactly those colour toggles rather than painting a metric it has no data for, and the
footer says what is missing and that nothing was estimated in its place. **Say the same when you
hand the board over.**

---

## How to Run

**Identify your client.** Send a `User-Agent` naming your agent runtime and this skill, for
example `OpenClaw/2.0 (market-heatmap)` or `ClaudeCode/2.1 (market-heatmap)`. Substitute your own
runtime and version if neither matches. You can also volunteer what your agent is called by adding
an `agent/<your-agent-name>` token inside the same parentheses, as in
`OpenClaw/2.0 (market-heatmap; agent/research-desk)`. All of it is optional, and it is what tells
us this skill has real integrations behind it, so it gets prioritized and you get notice before it
changes. The bundled script already carries the skill slug and honors `SENTISENSE_AGENT_NAME` the
same way, so exporting that name is all it takes on the script path.

### 1. Render it

```bash
export SENTISENSE_API_KEY=...      # or however your host supplies secrets
python3 scripts/heatmap.py --out market-heatmap.html --summary-json -
```

With `--summary-json -`, standard output is the summary JSON, including the HTML output path;
no JSON sidecar is written. Without that flag, standard output contains only the absolute HTML path.
Fetch progress and tile/character counts go to the error stream. Write into
a directory you control and can name out loud rather than wherever the shell happens to be.

| Flag | Default | What it does |
|---|---|---|
| `--out FILE` | `market-heatmap.html` | Where to write the page. Its absolute path is printed |
| `--summary-json -` | off | Print summary JSON to stdout, with a display string beside each value; write only the named HTML file |
| `--scope NAME` | `sp500` | `sp500`, `nasdaq100` or `popular`. An unknown scope is refused, never quietly swapped for the default |
| `--metric NAME` | `change` | Which metric the page opens on. Five metrics, and each answers to more than one name: `change` (also `move`, `price`, `changePercent`), `sentiment` (also `tone`, `sentiment7d`), `score` (also `sentisense`, `sentisenseScore`), `mentions` (also `attention`, `mentionsZ`), `options` (also `optionsInterestScore`). Anything else is a usage error listing the valid names. An overlay the key did not receive falls back to `change` with a line on the error stream, and still exits 0. The reader can switch inside the page either way |
| `--fixture FILE` | off | Render a saved response instead of calling the API. Used by the tests, and by anyone who wants to see the layout with no key: `scripts/fixtures/market-heatmap.nasdaq100.sample.json` is a Nasdaq-100 board on a free key, 101 tiles, with sample figures. A fixture render stamps a sample-data banner on the page |

**Use `--summary-json -` whenever you are going to write the reply**, which is every time. It
carries the as-of line, the mood, the breadth headline, every sector ranked both by price and by mood,
the largest moves up and down, the per-metric count of tiles with no reading, the preview note
with the layers this key did not receive, and the path and character count of the file it just
wrote. Sectors are ranked by price with the `Unclassified` bucket left out, because it is a
data-quality bucket rather than a sector and "weakest sector Unclassified" tells a reader
nothing; it is still drawn on the board and still counted in the tiles. Every value comes with
its display string, so the reply is a copy rather than a formatting decision.

**Exit codes are specific so a failure is legible.** `2` for usage: a missing key, an unknown
scope or metric, an unreadable fixture. `3` for auth: the key was rejected. `4` for a board that
is not there yet, which is a real state worth wording carefully: the board is rebuilt every 15
minutes during regular trading hours, so right after a release the first request can answer
`404 no_snapshot`. That is a warm-up, not an outage. Tell the user **the board has not been built
yet and to retry in 15 minutes**, and do not fall back to a different scope to manufacture an
answer. `5` for rate limited, `6` for a network or upstream failure. Nothing is written on a
failure, so a stale file never passes for a fresh one.

### 2. Hand it over

The page lands on the machine the agent runs on, which is not always the machine the user is
looking at, so decide the route before you announce anything. In order of preference:

1. **Give it to whatever the host uses to show a page.** Many hosts can put a self-contained HTML
   document in front of the user directly: a render surface, a widget, an inline panel, an
   attachment. That is the best fit, because the file is a static self-contained snapshot by
   design and it carries its own styles and behaviour. Check the capability is actually connected
   before promising it.
2. **Name the absolute path in prose either way**, in the same message, so the user can open it in
   a browser themselves. The script prints that path for you. Never present a bare relative path,
   and never present a path as if it were a link.
3. **If nothing on the host can display it**, use the host's file or attachment mechanism, or
   serve the file briefly over a local port you name explicitly, stating which machine "localhost"
   refers to.

**Do not hand a `file:` URL to a host's in-app browser.** Several runtimes refuse local file URLs
under their URL policy, and the refusal usually arrives as a security error rather than a
fallback, which burns a turn and looks like the skill is broken. For example, a terminal-style
coding agent typically cannot open `file:///.../market-heatmap.html` in its built-in browser but
can attach or embed the same absolute path; substitute whatever your own runtime does.

**Refresh reuses the same absolute path.** Write the new render over the old file so a user who
already has it open reloads rather than hunting for a second copy. Where the host has a stable
artifact identity, a pinned widget or a named panel, replace it in place under the same name.
Where the surface is a conversation, show the refreshed page again and say plainly that this is
the refreshed board: a new message cannot literally replace an older one, so do not imply the
earlier picture is gone.

**Say what is interactive and what is not.** Inside the page the metric toggle, the sector zoom,
the search box and the hover cards all work with no network. Nothing in it updates on its own, and
no click fetches anything. If the host renders the page without running its scripts, the board,
the header, the legend and the footer still read correctly, but the toggle and the zoom will not
respond; say so rather than promising a control the reader cannot use.

For example, OpenClaw since 2026.8.1 offers exactly that route as a runtime tool. Call
`show_widget` with `widget_code` set to the contents of the HTML file (the tool takes
self-contained HTML) and a short `title` such as "US market heatmap". Add `pin: true` with the
stable `name` `market-heatmap` to place it on the session dashboard, where it survives `/new` and
`/reset`; a later call with the same `name` replaces it in place, which is how "refresh it"
updates the board instead of stacking a second one. Pick a large `size`, `xl` or `full`, since
this is a treemap of hundreds of tiles. Inline widgets are sandboxed with inline style and script
allowed and no external loads, which this file already satisfies, and the inline limit is 262,144
characters, which the script checks and warns about on the error stream.

**Never declare `capabilities.netOrigins` for this widget.** The agent fetches the board with the
key in its own environment and renders a snapshot, so the page needs no origin and no key. That is
the whole design: a widget that fetched for itself would have to carry the key in its source, and
declaring an origin would make the render depend on the session permission mode. With no origins
declared it draws identically under every mode, including the strictest. Check that the tool is
present before promising it; when it is not, the file route above still applies.

---

## The call, and how to do it without the script

The bundled script is a convenience. Everything it does starts from one plain GET, documented
here so this skill works with no script, no CLI and no SDK.

```bash
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/trackers/market-heatmap?scope=sp500"
```

**`GET /api/v1/trackers/market-heatmap?scope={sp500|nasdaq100|popular}`**, the whole board.
`scope` is optional and defaults to `sp500`; an unknown value returns `400 invalid_scope` listing
the valid ones. Unlike several other endpoints this one **does** use the preview envelope:

```
{ "isPreview": true, "previewReason": "PRO_REQUIRED", "totalCount": 500, "data": { ... } }
```

`isPreview` is `false` for a PRO key. `totalCount` is on every response and always equals the
number of rows in it, because no tier is served a shortened board. Everything else lives under
`data`:

- `asOf` is the price as-of, `generatedAt` is when the board was written.
- `rows[]` is one row per tile, sorted by market cap descending, and every tier receives all of
  them. Each row carries `ticker`, `name`, `sector`, `marketCap`, `price`, `previousClose`,
  `changePercent`, `volume`, `industry` when one is on file, sometimes `priceAsOf`, the generic
  tracker fields `rank`, `rowId`, `category`, `url` and `metrics[]`, and on a PRO key the
  overlays `sentiment7d`, `sentimentChange7d`, `sentisenseScore`, `mentionsZ` and
  `optionsInterestScore`. **A field with no reading is absent from the row, not set to zero.**
  That is the single most important thing to get right when you read this payload:
  `row.get("sentisenseScore")` returning nothing means there is no reading, and defaulting it to
  `0` invents a neutral that nobody measured. What a served Score of `0.0` does and does not
  prove is honesty rule 2 below.
- **`meta.previewWithheld` is what separates "no reading" from "not on your tier."** It lists the
  layer names a non-PRO key did not receive, `["sentiment", "options"]`, where the `sentiment`
  layer covers `sentiment7d`, `sentimentChange7d`, `sentisenseScore` and `mentionsZ`, and
  `options` covers `optionsInterestScore`. It is absent from a PRO response, and it names only
  layers this board actually has: a layer the writer could not build is missing from
  `meta.layers` and from this list, because PRO would see nothing for it either. Reading the row
  alone cannot tell you which case you are in, so read this field, disable those choices, and
  never colour a metric you have no data for.
- Some rows carry `classes`, the other spellings the index list uses for that company: GOOGL's
  tile carries `["GOOG", "GOOGL"]` because both classes are listed and the vendor reports the
  whole company's market cap against each, so the board collapses them onto one tile rather than
  counting Alphabet twice. `meta.collapsedClasses` names every class that folded, and
  `meta.universeSize` still counts listed classes while `meta.tileCount` counts drawn tiles.
- `meta.sectors[]` is the per-sector rollup: `sector`, `marketMoodScore`, `marketMoodPhase`,
  `marketMoodWeeklyChange`, `count`, `capWeightedChangePct`, `equalWeightedChangePct`, `capUsd`,
  `up`, `down`. The price fields (`count`, the two changes, `capUsd`, `up`, `down`) are computed
  over this board's names, which is also what you were served, so they and the rows describe the
  same set. The three `marketMood...` fields are not: they are the market-wide Market Mood reading
  for that GICS sector, identical in every scope, so a Nasdaq-100 board carries the same sector
  mood as the S&P 500 board. Print the rollup rather than recomputing a sector's size from the rows.
- `meta.layers` names the layers that ran, each with its own `asOf`. On `sentiment` that is a date,
  and `computedAt` beside it is the instant the read was computed: the read is rewritten a few
  times a day, far slower than the board, so quote `computedAt` when you say how fresh a Score is.
  `prices` carries
  `delayMinutes: 15` and `asOfSource`: `vendor` when the quotes carry their own time, or
  `lastRegularClose` when they do not and the as-of is the previous regular session's close,
  which is the case outside regular hours. On `lastRegularClose`, "today's change" is the last
  session's move, so say "as of the last close" rather than "today". A layer that is absent from
  this map did not run today, which is a different fact from a ticker having no reading. `meta.breadthUp`, `meta.breadthDown`,
  `meta.capWeightedChangePct`, `meta.equalWeightedChangePct`, `meta.marketMoodScore` and
  `meta.marketMoodPhase` are the same numbers the human-labelled `headline[]` carries, in
  machine-readable keys.
- `meta.missingPrice[]` lists names in the index that had no quote and therefore have no tile.

**Sectors arrive canonical, and that is new.** Every row's `sector` is one of the eleven GICS
names or the bucket `Unclassified`; the endpoint normalises before it writes, and a build gate
holds our curated sectors to the index provider's own GICS column. `Unclassified` is a
data-quality bucket, not a sector: draw it, count it, and keep it out of any "strongest" or
"weakest sector" sentence. You do not need an alias map for this payload. **You do need one the
moment you join anything else**, because the per-ticker profile endpoint and the sector
vocabularies elsewhere still disagree with each other
(`Information Technology` against `Technology`, `Healthcare` against `Health Care`, `Financials`
against `Financial Services`, `Consumer Discretionary` against `Consumer Cyclical`). Join two
sector fields without normalising and roughly a sixth of your names land in a sector that does not
exist and vanish, which reads as a quiet sector rather than as a broken join.

---

## Reading the picture

- **Tile area is market cap**, so the board is what a cap-weighted index actually looks like: a
  handful of names carry most of the surface. That is the point of the shape, not a distortion of
  it. A tile with no market cap on file is drawn at the smallest area and the footer counts it.
- **Colour is one metric at a time**, and the legend prints the scale's real edges. The scale is
  **fitted to the board in front of you**, with a floor, so a quiet day is not painted as a
  crisis; two boards from different days are not on the same scale and should not be compared by
  colour. Compare the numbers.
- **Market Mood is 0 to 100, fear to greed.** Bands: 0-15 Extreme Fear, 16-30 Fear, 31-45 Anxiety,
  46-55 Neutral, 56-70 Optimism, 71-85 Greed, 86-100 Extreme Greed. It sits on the sector headers
  and in the masthead, never on a tile, because it is a sector-level and market-level reading.
- **A weekly change on a sector is a mood change, not a return.** `-6.7` means the sector's
  fear-to-greed reading fell by 6.7 points, not that it lost 6.7 percent.
- **Sentiment is a mean daily tone from -1 to +1 over seven days.** The **SentiSense Score** is
  how bullish or bearish today's news and social coverage reads, weighted by how much a name is
  discussed. Above zero leans bullish, below zero leans bearish. It reads what people write, not
  what the price did, so it can stay positive on a down day. **Mentions** are today's
  volume in standard deviations of that name's own 30-day baseline, so it says "unusually busy",
  not "bullish". **Options interest** is a 0 to 100 composite of how unusual the options activity
  is, and it has no direction either.
- **Breadth counts and cap-weighted change cover the whole board**, which is every name in the
  index on every tier. What changes by tier is the overlays, not the names. The page says which
  overlays it is missing; so should you.

---

## Honesty rules, all five load-bearing

**1. Label freshness per layer, because it varies inside one picture.** Prices are 15-minute
delayed, not live. Market Mood, sentiment and options interest are analytical batches with their
own as-of dates, and the options layer is typically a day behind. The footer carries all four
stamps and the masthead carries the render time. Outside regular hours the price layer is the
last regular session's close (`asOfSource: lastRegularClose`); before the open that is the
previous day, so answer "what is moving today" with that session's moves and say which session.
Never describe any of it as real time, and never diff a delayed price against a batch reading
and call the gap a finding.

**2. Absent is not zero, and on the Score a zero is a measurement.** An
overlay with no reading for a ticker is missing from the row, and the page draws it in the neutral
no-reading tone with the words "no reading", never as a zero that would read as the middle of the
scale. A served zero gets its own flat tone, which is a different thing and is drawn differently.
This matters most on the **SentiSense Score**, which is centred on zero. The board decides from
the day's own sample:

```
no bullish or bearish analyses today   ->  omitted, no field at all
bullish or bearish analyses today      ->  served, and 0.0 means they balanced
```

So a served `0.0` is a measured neutral, and an omitted Score means nothing directional was
measured today, including for a name that has an older reading. The overlay template's "No
reading" row counts the tiles served without a Score; word it that way. To see one name's counts,
read that day's point on `GET /api/v2/metrics/entity/{ticker}/metric/sentisense`, whose
`metricValue.properties` carry `bull`, `bear` and `directional` (their sum). If you read the
payload yourself, do not default a missing reading to zero and do not count an absent field as a
bearish one.

**3. Mood and sentiment are nowcasts, not forecasts.** They read how fearful or greedy the market
currently is and how a name is currently discussed, weighted by how actively. They do not predict
price. A green tile is not a buy list and a red tile is not a sell list. Never label the board a
signal, a target or a prediction, and do not build a "top picks" answer out of it.

**4. Do not narrate more than the board holds.** The tiles are one index, not the market, on
every tier. Report what the picture shows and stop.
The tell that you have crossed the line is a clause where a partial sample acquires a motive:
"money is rotating out of energy", "the market is repricing healthcare". **Direction is reportable
from a partial sample. Magnitude and intent are not.** This is the easiest way to turn a correct
picture into a wrong sentence, because the numbers stay right while the words underneath them go
wrong.

**5. Every board carries a disclaimer.** It is written into the footer, and it is not optional:

> Not investment advice. Generated from public and licensed market data for research and
> educational purposes only. Not a recommendation to buy or sell any security.

---

## Design, if you render it yourself

The script is the reference implementation and the reviewed one. If you draw your own board from
the same payload, these are the rules that keep it looking like a research instrument rather than
a demo mock.

```
--bg:#0d1117    --panel:#161d28   --line:rgba(255,255,255,.13)
--ink:#e8edf4   --ink2:#9daaba    --ink3:#66738a
--bull:#2e9d75  --bear:#e05c4a    --flat:#6b7280   --data:#3182ce
--gold:#D4A843  (brand chrome only, never a data mark)
```

That bull, bear and neutral trio is validated for colorblind separation against this dark ground,
so substitute at your own risk. The usual finance red-green pairing is one of the worst possible
choices for deuteranopia; the green here is pushed toward teal specifically to survive it.

- **Directional metrics get the bull and bear pair. Attention metrics do not.** Colouring mention
  volume or options interest red and green tells the reader a busy name is a falling one. Use a
  single-hue ramp on the data blue for anything that has no sign.
- **Step the fill, do not blend it.** Discrete bands the reader can count and match against a
  legend beat a continuous ramp nobody can read a value off. No gradients on anything a reader
  compares, and no glow, no badges, no stamps, no drop shadows.
- **No arrow glyph next to a price change.** The sign and the colour already carry direction; an
  arrow is a third encoding of the same bit.
- **Never encode by colour alone.** Every tile large enough prints its own number, and every
  reading appears as text in the card.
- **Give a tile a visible minimum, and say what it means.** A name with no market cap drawn at
  zero area is indistinguishable from a name that is not there. Draw it at the smallest area and
  count it in the footer.
- **Leave ground between sectors.** Two sectors that touch read as one shape. A gap plus a header
  is enough; a border around everything is not.
- **A block too small to label is a hole the reader cannot check.** When a sector is too small to
  carry its name, give the room back to its tiles and say in the footer which sector lost its
  label, rather than spending the whole rectangle on a clipped word.
- **Let type carry hierarchy.** A serif masthead against a sans with tabular numerals for every
  figure. Two weights is enough.
- **Keep it self-contained.** No external fonts, no images, no external scripts, no `url()`, no
  `fetch`. If a grep for `http` finds anything but a link to our site in the footer prose, it is
  not a snapshot any more.

---

## Going further

Free draws the whole board, every tile, every sector rollup. **PRO ($15/mo)** lifts the monthly
request cap (no monthly limit, just a 300/min rate) and adds the four overlays we compute on top
of the tiles, sentiment, the SentiSense Score, mention pressure and options interest, so the same
board recolours by our own analysis, plus depth across the rest of the SentiSense API. Apply
coupon `AGENTS` at checkout for a builder launch discount: https://app.sentisense.ai/pricing?coupon=AGENTS

For "make this my morning brief", hand off to the `stock-market-dashboard` skill when available. Pass user-chosen tickers and notable anomalies. Return a dated watchlist artifact; never infer a portfolio from the market universe. Hand off only when the user changes the question; do not automatically route back. If the sibling is unavailable, answer the supported part here using a connected tool or the inline REST workflow, state any remaining gap, and never require an install.

For
building your own filtered lists of names instead of a fixed index, install `stock-screener`. For
the sentiment and Score numbers behind the overlays, install `stock-sentiment`. For the full REST
reference on this and every other endpoint, install the `sentisense` skill; for the command-line
equivalent, install `sentisense-cli`.

## Use & Disclaimer

This skill reads public market data from the SentiSense API over HTTPS with one GET request and
writes one HTML file locally. It performs no writes, no trades, no purchases and no wallet
operations, and it sends nothing anywhere except that documented request. The rendered page
contains no key, no external resource and no network call.

Output is a snapshot for research and education only. Prices are delayed, not live, and the mood,
sentiment and options readings come from analytical batches with their own as-of dates. It is not
investment advice, not a recommendation and not a forecast.

**ClawHub Skill:** [clawhub.ai/TheSentiTrader/market-heatmap](https://clawhub.ai/TheSentiTrader/market-heatmap)

---

*SentiSense is a read-only financial intelligence API. This data is for informational and educational purposes only, not investment advice.*
