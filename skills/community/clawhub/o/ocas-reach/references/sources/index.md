# Reach source index

This is the authoritative list of every data source registered in `scripts/sources.yml`. Each row links to a per-source reference file under `references/sources/<name>.md`.

## How to read this index

| Column | Meaning |
|---|---|
| **Source** | Slug to use as `<source>` argument: `python3 scripts/reach.py query <source> <action> [params_json]` |
| **Category** | knowledge / government / science / weather / geo / finance / health / media |
| **Auth** | `none` = public, `optional` = key recommended for higher rate, `required` = won't work without |
| **Account** | `null` = no account ever needed, `optional` = key improves limits, `required` = must register |
| **Daily / Monthly** | Hard caps on free tier when known. Empty = no documented hard cap (rate-limit instead). |

When the **Account** column says `required`, Reach is authorized to register at the source's signup URL using the OCAS persona and store the issued key in `~/.hermes/.env` under the registered env var. See [`account_provisioning.md`](../account_provisioning.md) for the full registration playbook and [`credential-files.md`](../credential-files.md) for the persona details.

---

## No key, no login

| Source | Category | Reference | Auth | Notes |
|---|---|---|---|---|
| `wikipedia` | knowledge | [wikipedia.md](wikipedia.md) | none | full text + summary; needs `User-Agent` |
| `wikidata` | knowledge | [wikidata.md](wikidata.md) | none | SPARQL + entity JSON; 5/sec, 60s timeout |
| `sec_edgar` | government | [sec_edgar.md](sec_edgar.md) | none | every US public-company filing; require `User-Agent` |
| `gdelt` | media | [gdelt.md](gdelt.md) | none | global news events + sentiment, deep history |
| `openalex` | science | [openalex.md](openalex.md) | none / polite-pool email | 240M+ scholarly works |
| `open_meteo` | weather | [open_meteo.md](open_meteo.md) | none | forecast + 80yr archive + marine + air + pollen + flood |
| `world_bank` | government | [world_bank.md](world_bank.md) | none | country-level macro indicators |
| `crossref` | science | [crossref.md](crossref.md) | none | DOI metadata, 50/sec polite |
| `pubmed` | health | [pubmed.md](pubmed.md) | none / optional NCBI key | biomedical literature |
| `arxiv` | science | [arxiv.md](arxiv.md) | none | preprint metadata, 1 req / 3 sec |
| `federal_register` | government | [federal_register.md](federal_register.md) | none | daily US rules / notices / proposed regs |
| `usaspending` | government | [usaspending.md](usaspending.md) | none | federal spending + awards |
| `overpass` | geo | [overpass.md](overpass.md) | none | OpenStreetMap via Overpass QL |
| `noaa_nws` | weather | [noaa_nws.md](noaa_nws.md) | none | official US forecasts + alerts |
| `usgs_earthquake` | weather | [usgs_earthquake.md](usgs_earthquake.md) | none | FDSN spec quake events |
| `nominatim` | geo | [nominatim.md](nominatim.md) | none | OSM geocoding, 1 req/sec absolute |
|| `open_library` | knowledge | [open_library.md](open_library.md) | none | books, authors, ISBN |
|| `scihub` | science | [scihub.md](scihub.md) | none | academic papers via Sci-Hub mirrors; ~85M papers |
|| `unpaywall` | science | [unpaywall.md](unpaywall.md) | none | open-access paper lookup; ~30M papers, legal OA copies |
|| `public_apis` | knowledge | [public_apis.md](public_apis.md) | none | collective directory of free public APIs |
|| `rest_countries` | geo | [rest_countries.md](rest_countries.md) | none | country metadata |
|| `open_food_facts` | knowledge | [open_food_facts.md](open_food_facts.md) | none | packaged food + barcodes |
|| `weather` | weather | [weather.md](weather.md) | none | unified US weather: conditions, forecast, alerts, metar, brief + global via Open-Meteo. Default for all weather queries. |
|| `welib` | knowledge | [welib.md](welib.md) | none | 43M books + 98M papers; Cloudflare-protected, may need browser |
|| `openaq` | weather | [openaq.md](openaq.md) | optional | global air-quality measurements |
| `photon` | geo | [photon.md](photon.md) | none | OSM geocoding, faster alt to Nominatim |
| `worldtime` | geo | [worldtime.md](worldtime.md) | none | timezone + DST |
| `nager_holidays` | knowledge | [nager_holidays.md](nager_holidays.md) | none | public holidays, ~100 countries |
| `ip_api` | geo | [ip_api.md](ip_api.md) | none | IP geolocation; non-commercial only |
| `themealdb` | knowledge | [themealdb.md](themealdb.md) | none | recipes — test endpoint |
| `thecocktaildb` | knowledge | [thecocktaildb.md](thecocktaildb.md) | none | cocktails — test endpoint |
| `census` | government | [census.md](census.md) | none | demographics, population, economic census |
| `epa_echo` | government | [epa_echo.md](epa_echo.md) | none | environmental compliance, facility violations |
| `hifld` | government | [hifld.md](hifld.md) | none | critical infrastructure (hospitals, power, dams) |
| `nonprofit_explorer` | government | [nonprofit_explorer.md](nonprofit_explorer.md) | none | IRS 990 data, nonprofit financials |
| `ncbi_datasets` | health | [ncbi_datasets.md](ncbi_datasets.md) | none | genomic data, gene function, taxonomy |
| `space_weather` | science | [space_weather.md](space_weather.md) | none | solar flares, geomagnetic storms, ISS location |
| `exchangerate` | finance | [exchangerate.md](exchangerate.md) | none | currency exchange rates, no key needed |
| `transit_land` | geo | [transit_land.md](transit_land.md) | none | transit routes, stops, schedules worldwide |
| `ev_charging` | geo | [ev_charging.md](ev_charging.md) | none | EV charging station locations worldwide |
| `manualslib` | knowledge | [manualslib.md](manualslib.md) | none | 3M+ product manuals, 140K+ brands. Vue.js SPA, direct access blocked. Wayback CDX + image OCR. |
| `gibs` | science | [gibs.md](gibs.md) | none | NASA satellite imagery tiles (MODIS, VIIRS, ~180+ layers). WMTS + WMS. No key. |

## Needs key or login (free tier)

| Source | Category | Reference | Env var | Account URL | Daily | Monthly | Notes |
|---|---|---|---|---|---|---|---|
| `fred` | finance | [fred.md](fred.md) | `FRED_KEY` | https://fred.stlouisfed.org/docs/api/api_key.html | — | — | ~800k US/global econ time series |
| `nasa` | science | [nasa.md](nasa.md) | `NASA_KEY` | https://api.nasa.gov/ | 1000/hr | — | APOD/NEO/EPIC/EONET/Mars |
| `congress_gov` | government | [congress_gov.md](congress_gov.md) | `CONGRESS_KEY` | https://api.congress.gov/sign-up/ | — | — | bills, votes, members |
| `bls` | government | [bls.md](bls.md) | `BLS_KEY` | https://data.bls.gov/registrationEngine/ | 500 | — | US labor / CPI / employment |
| `govinfo` | government | [govinfo.md](govinfo.md) | `GOVINFO_KEY` | https://api.govinfo.gov/docs/ | — | — | Cong. Record, CFR, US Code |
| `alpha_vantage` | finance | [alpha_vantage.md](alpha_vantage.md) | `ALPHA_VANTAGE_KEY` | https://www.alphavantage.co/support/#api-key | **25** | **750** | stocks, forex, fundamentals |
| `semantic_scholar` | science | [semantic_scholar.md](semantic_scholar.md) | `SEMANTIC_SCHOLAR_KEY` | https://www.semanticscholar.org/product/api | — | — | 100M+ papers, citation graph |
| `usda_fooddata` | health | [usda_fooddata.md](usda_fooddata.md) | `USDA_KEY` | https://api.nal.usda.gov/fdc/ | — | — | authoritative US nutrition |
| `courtlistener` | government | [courtlistener.md](courtlistener.md) | `COURTLISTENER_KEY` | https://www.courtlistener.com/help/api/rest/ | — | — | federal + state case law |
| `fec` | government | [fec.md](fec.md) | `FEC_KEY` | https://api.open.fec.gov/developers/ | — | — | campaign finance |
| `geonames` | geo | [geonames.md](geonames.md) | `GEONAMES_USERNAME` | https://www.geonames.org/login | 20000 | — | populated places, elevation, timezone |
| `airnow` | weather | [airnow.md](airnow.md) | `AIRNOW_KEY` | https://docs.airnowapi.org/ | — | — | official US EPA Air Quality Index |

---

## Media and social sources

| Source | Category | Reference | Auth | Account | Notes |
|--------|----------|-----------|------|---------|-------|
| `reddit` | media | [reddit.md](reddit.md) | optional | optional | Reddit browser via MCP. Anonymous (10/min) or OAuth (60-100/min). |
| `linkedin` | media | [linkedin.md](linkedin.md) | required | required | LinkedIn profiles, companies, jobs via browser automation. Requires login. |
| `paper_search` | science | [paper_search.md](paper_search.md) | optional | null | Multi-source academic paper search (arXiv, PubMed, Semantic Scholar, etc.). |
|| `searxng` | media | [searxng.md](searxng.md) | none | null | Local SearXNG metasearch. Open web + social media search. No key needed. ||
|| `yahoo_finance` | finance | [yahoo_finance.md](yahoo_finance.md) | none | null | Yahoo Finance MCP. Prices, financials, news, recommendations, options. No key. ||
|| `rapidapi` | other | [rapidapi.md](rapidapi.md) | rapidapi_key | varies | 203+ APIs via MCP multiplexer. Finance, crypto, news, geo, weather, security, social, travel. General-purpose marketplace — NOT "local business search." ||
|| `acre_lens` | geo | [acre-lens.md](acre-lens.md) | none | null | AcreLens MCP. US land due-diligence: solar, groundwater, flood zones, building codes, county regulations. No key. ||
|| `metricduck` | finance | [metricduck.md](metricduck.md) | required | required | MetricDuck MCP. Company fundamentals, screening, comparison. Bearer token via METRICDUCK_API_KEY. Rally Quality/Safety fallback. ||

---

## Routing hints (which source for which question)

| If the user asks… | Try first |
|---|---|
| "What is X" / general factual lookup | `wikipedia` summary, then `wikidata` for structured facts |
| "What's filed by company X" | `sec_edgar` |
| "Recent news about X" | `gdelt` |
|| "Papers about X" | `openalex` (breadth) → `semantic_scholar` (curation) |
|| "Is paper X open access?" | `unpaywall` (check OA status by DOI) |
|| "Download paper PDF by DOI" | `unpaywall` (legal OA first) → `scihub` (mirror fallback) |
|| "Get paper PDF" / "sci-hub" | `scihub` |
|| "Find textbooks on X" | `welib` (books + papers) |
|| "Biomedical evidence about X" | `pubmed` |
| "What's the weather / will rain / forecast" | `weather` (brief, conditions, forecast) — US; `weather global` — international |
| "Any weather alerts / warnings" | `weather alerts` |
| "Severe weather risk / SPC outlook" | `weather severe` |
| "Current weather worldwide" | `weather global` |
| "METAR for airport X" | `weather metar` |
| "Recent earthquakes" | `usgs_earthquake` |
| "Where is / coordinates of" | `nominatim` (1 req/sec) or `photon` |
| "OSM features near X" | `overpass` |
| "US economic data" (GDP, CPI, unemployment) | `fred` (most comprehensive) or `bls` (labor only) |
| "Global development indicators" | `world_bank` |
| "Stock price / fundamentals" | `alpha_vantage` (mind 25/day cap) |
| "Federal regulation / rule" | `federal_register` (recent) or `govinfo` (CFR/USC) |
| "Bill / vote / member of Congress" | `congress_gov` |
| "Federal contract / grant" | `usaspending` |
| "Court opinion / case law" | `courtlistener` |
| "Campaign finance" | `fec` |
| "Nutrition / barcode" | `usda_fooddata` (nutrition) or `open_food_facts` (barcode) |
| "Holidays / time zone / IP location" | `nager_holidays`, `worldtime`, `ip_api` |
| "Country facts" | `rest_countries` (basics) or `world_bank` (indicators) |
| "Book / ISBN" | `open_library` |
| "NASA / asteroid / rover photo / disaster" | `nasa` |
| "Satellite imagery layers" / "Earth observation data" | `gibs` (planned -- see discovered-apis.md) |
| "Solar flare / geomagnetic storm / ISS location" | `space_weather` |
| "US demographics / population / income by area" | `census` |
| "Environmental compliance / facility violations" | `epa_echo` |
| "Hospitals / power plants / critical infrastructure near X" | `hifld` |
| "Nonprofit financials / IRS 990 data" | `nonprofit_explorer` |
| "Gene info / genome / taxonomy" | `ncbi_datasets` |
| "US air quality index (official EPA)" | `airnow` |
| "Currency exchange rates / convert currency" | `exchangerate` |
| "Transit routes / stops / schedules" | `transit_land` |
| "EV charging stations near X" | `ev_charging` |
| "Product manual for X" / "How to use X" / "X user manual" | `manualslib` search → read_page |
| "Random manual page" | `manualslib` read_random |
| "Satellite imagery of X" / "What does X look like from space" / "Recent imagery of location" | `gibs` layers → tile_url or wms_bbox |
| "Analyze this land"
|| "Solar potential for this address" | `acre_lens get_solar_potential` |
|| "Compare these two parcels" / "which property is better" | `acre_lens compare_properties` |
|| "How suitable is this land" / "quick land score" | `acre_lens get_land_quick_score` |
|| "Land regulations in state X" / "state land profile" | `acre_lens get_state_land_profile` |
|| "What are people saying about X on Reddit" | `reddit` search |
| "Find papers about X" | `paper_search` search (multi-source) |
| "Look up person on LinkedIn" | `linkedin` person_profile |
| "Find employees at company X" | `linkedin` company_employees |
| "Search jobs for X" | `linkedin` search_jobs |
| "Company X posts on LinkedIn" | `linkedin` company_posts |

When in doubt, fall back to `wikipedia` → `wikidata` chain — it's the universal fallback and requires no auth.

## Adding a new source

1. Append the entry to `scripts/sources.yml` following the existing schema. Validate any URL templates and parameter names against the source's docs.
2. Write `references/sources/<name>.md` using `_template.md` as the skeleton.
3. Add a row to this index in the appropriate section.
4. If the source needs custom multi-step logic, write `scripts/sources/<name>.py` exporting `query(action, params, auth)`.
5. **MCP connector sources:** Set `custom: <name>_mcp` and `mcp: true` in sources.yml. Add `mcp_url` and `transport` fields. No `base_url` needed for pure MCP servers. The MCP client handles tool invocation; Reach routes to it via the custom module.
6. Bump version in SKILL.md (MINOR — new source = new behavior). Update README + CHANGELOG.

## Out of scope (intentionally excluded)

- Crypto market data, decentralized data sources
- Social platforms not yet added: Twitter/X, Mastodon, Bluesky (Reddit and LinkedIn now supported)
- Generic web search (SearXNG now covers open web search; for deep research, use Sift)
- Anything requiring paid tier for first call
- MCP wrappers around APIs already registered as sources (prefer direct API integration)
- Generic web scraping proxies (belongs in Sift)
- Dark web / Tor access tools (belongs in Scout)
- MCP infrastructure/platform services (not data sources)

For the full evaluation framework including decision tree and rejection categories, see [`references/source-evaluation-framework.md`](../source-evaluation-framework.md).
