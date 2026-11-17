# Discovered APIs

APIs, data sources, and endpoints found during research sessions but **not yet integrated** into `sources.yml`. Maintained by the `reach:api-mine` cron job (daily 4am PT).

For fully integrated sources, see `references/sources/index.md`.

---

## Data Index

_Lookup by what data you need. Cross-references the main source index._

### Prediction Markets
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Election odds | Kalshi API | Polymarket Gamma API | Real-time market prices via REST |
| Economic indicators (prediction) | Kalshi API | — | GDP, unemployment, inflation odds |
| Political event odds | Kalshi API | Polymarket Gamma API | Congressional votes, leadership |
| Climate/weather thresholds | Kalshi API | — | Temperature, emissions targets |

### Finance & Economics
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Stock prices (real-time) | `yahoo_finance` (main index) | Alpaca API, Finnhub | Alpaca: brokerage + market data |
| Trading/brokerage | Alpaca API | — | Paper + live trading, crypto, options |
| Company fundamentals | Finnhub | `alpha_vantage` (main index) | Financials, earnings, estimates |
| Alternative data | Massive API | — | Consumer sentiment, web scraping |
| Crypto podcast sentiment | AudioAlpha | — | Narrative sentiment, market themes |

### People & Social
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Social profiles | `linkedin` (main index) | `reddit` (main index) | |
| Tech/news social feed | Hacker News API | `reddit` (main index) | Top/New/Best stories, comments, users; Firebase JSON, no auth |
| Reverse image search | Yandex Images | Google Images | Via browser (Yandex) or residential IP (Google) |

### Geocoding & Places
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Places / local business | Google Places API | `photon` (main index) | Used by Styx, Taste, Sands for enrichment |
| Address geocoding | `photon` (main index) | `nominatim` (main index) | |

### Health & Nutrition
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Drug recalls | FDA open data | — | Not yet integrated |

### Archives & Newspapers
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Historic US newspapers | Chronicling America API | Newspapers.com (no API, subscription) | 23M+ pages, 1790-1963, free, no auth |
| Book metadata & search | Google Books API | OpenLibrary API | Both free; Google has better snippet previews |
| Book metadata (open) | OpenLibrary API | Google Books API | Internet Archive project, fully open data |

### Standards & RFC
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Internet standards / RFCs | IETF Datatracker API | — | 157K+ documents, drafts, groups, meetings; no auth |
| IETF working groups | IETF Datatracker API | — | WG charters, chairs, milestones |
| IETF meetings / agendas | IETF Datatracker API | — | Meeting materials, proceedings |

### Creative & Media
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Image generation | Pollinations.ai | — | Used by ocas-imagine |

### Museums & Cultural Heritage
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Museum open-data source discovery | Digital Art History Directory — Open Data Collections | `public_apis`, web search | Curated list of art/museum open datasets and APIs; WordPress JSON accessible |
| Metropolitan Museum of Art collections | The Met Collection API | Met Open Access CSV | 470k+ object records + public-domain images; no auth; CC0 dataset |
| Harvard Art Museums collections | Harvard Art Museums API | IIIF manifests | Object/person/exhibition/publication/gallery metadata + images; key required; non-commercial |
| Walters Art Museum collections | Walters static collections data | Online Collection / future API v2 | 10k+ object records + media CSVs; v1 API closed; CC0; static GitHub data now |

### Models & ML
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| ML model search | Hugging Face Hub API | — | 100K+ models, datasets, metadata |
| Dataset discovery | Hugging Face Hub API | — | Filter by task, language, license |

### Web Search
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| General web search | SearXNG (main index) | Google CSAPI | CSAPI: programmatic Google search |
| API discovery | RapidAPI marketplace | `public_apis` (main index) | 203 endpoints across all categories |
| Product manuals | `manualslib` (main index) | ManualZZ (mirror) | 3M+ manuals, 140K+ brands. Vue.js SPA, direct access blocked. Wayback CDX + image OCR. |

### Web Data Extraction
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| JS-rendered page content + unblocking | Zyte API | donsetch, sift.webwright | Paid API (usage-based); unblocking, browser rendering, auto-extraction (Product, Article, jobPosting, SERP). Not yet evaluated. |

### Banking & Transactions
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Bank transactions | Plaid API | — | Used by ocas-styx for financial sync |
| Account balances | Plaid API | — | Real-time balance checks |

---

## Registry

_Full details per API. Organized by category. Quality-ranked within each category._

### Prediction Markets

#### Kalshi Prediction Market API
- **Endpoint**: `https://api.elections.kalshi.com/trade-api/v2`
- **Data**: Real-time prediction market prices (0-1, representing implied probability) for economics, politics, climate, science/tech, financials, health events
- **Auth**: None required for public market data
- **Rate limits**: Not documented; reasonable use assumed
- **Quality**: Active markets with significant volume. Prices represent crowd-sourced probability estimates. USD-denominated contracts ($0-$1).
- **Discovered**: 2026-06-12 (bones:research cron via docs.kalshi.com)
- **Notes**: Old endpoint was `/v2/`, migrated to `/trade-api/v2/`. Frontend (kalshi.com/markets) is behind Vercel JS challenge — use API directly. Covers non-sports categories: Economics, Politics, Elections, Climate, Science/Tech, Financials, Health.
- **Source session**: `20260612_145529_92eac6`

#### Polymarket Gamma API
- **Endpoint**: `https://gamma-api.polymarket.com`
- **Data**: Prediction market data from Polymarket (election odds, political events, sports-adjacent markets)
- **Auth**: None for public data
- **Rate limits**: Not documented
- **Quality**: Large volume on election/politics markets. Gamma API is the newer REST interface (replaces older CLOB API).
- **Discovered**: 2026-06-12 (bones skill references)
- **Notes**: Used alongside Kalshi in ocas-bones for cross-platform prediction market analysis.
- **Source session**: `20260612_145529_92eac6`

### Finance & Economics

#### Alpaca Trading API
- **Endpoint**: `https://paper-api.alpaca.markets` (paper) / `https://api.alpaca.markets` (live)
- **Data**: Stock/crypto prices, fundamentals, options chain, order execution, portfolio management, account balances
- **Auth**: API key + secret (free tier available)
- **Rate limits**: 200 req/min (free tier)
- **Quality**: Well-documented, reliable, supports paper trading. Used by ocas-rally for trade execution.
- **Discovered**: 2026-06-05 (ocas-rally skill audit)
- **Notes**: Brokerage API — can place real trades. Paper trading environment available for testing. Also provides market data (IEX feed on free tier, SIP on paid).
- **Source session**: `20260605_235610_02d858`

#### Finnhub
- **Endpoint**: `https://finnhub.io/api/v1`
- **Data**: Company fundamentals, earnings estimates, financial statements, news sentiment, insider transactions, crypto prices
- **Auth**: API key (free tier: 60 req/min)
- **Rate limits**: 60 req/min (free), higher on paid tiers
- **Quality**: Good fundamentals data, used by ocas-rally for company analysis.
- **Discovered**: 2026-06-05 (ocas-rally skill audit)
- **Notes**: Free tier sufficient for research. WebSocket available for real-time prices.
- **Source session**: `20260605_235610_02d858`

#### Massive API
- **Endpoint**: `https://api.massivedata.io` (approximate — verify current URL)
- **Data**: Alternative data: consumer sentiment, web scraping results, ESG scores, patent filings
- **Auth**: API key (paid)
- **Rate limits**: Varies by tier
- **Quality**: Used by ocas-rally for alternative signal generation. Paid service.
- **Discovered**: 2026-06-05 (ocas-rally skill audit)
- **Notes**: Niche alternative data provider. Verify current endpoint and pricing before integration.
- **Source session**: `20260605_235610_02d858`

#### AudioAlpha
- **Endpoint**: Not publicly documented — requires API key
- **Data**: Crypto podcast narrative sentiment, market themes, trending topics in crypto media
- **Auth**: `AUDIOALPHA_API_KEY` (optional but recommended)
- **Rate limits**: Not documented
- **Quality**: Niche signal source for crypto market sentiment. Used by ocas-rally.
- **Discovered**: 2026-06-11 (ocas-rally Yahoo Finance fix session)
- **Notes**: Small/indie API. May have limited uptime. Treat as supplementary signal only.
- **Source session**: `20260611_231040_0f9966`

### Banking & Transactions

#### Plaid API
- **Endpoint**: `https://production.plaid.com` (production) / `https://sandbox.plaid.com` (sandbox)
- **Data**: Bank transactions, account balances, institution metadata, auth (routing/account numbers), identity verification
- **Auth**: Client ID + secret + public key (OAuth 2.0)
- **Rate limits**: Varies by tier; sandbox is generous
- **Quality**: Industry standard for financial data aggregation. Used by ocas-styx for daily transaction sync.
- **Discovered**: 2026-06-05 (ocas-styx skill audit)
- **Notes**: Requires Plaid account and app registration. Sandbox available for testing. Production requires compliance review. Covers 12,000+ financial institutions in US/Canada/EU.
- **Source session**: `20260605_235610_02d858`

### Geocoding & Places

#### Google Places API
- **Endpoint**: `https://maps.googleapis.com/maps/api/place`
- **Data**: Place search (text/nearby), place details, photos, reviews, opening hours, price level
- **Auth**: API key (Google Cloud Console)
- **Rate limits**: 100 req/sec (with billing enabled)
- **Quality**: Best-in-class place data. Used by ocas-styx (merchant enrichment), ocas-taste (restaurant discovery), ocas-sands (travel time).
- **Discovered**: 2026-06-05 (ocas-styx, ocas-taste, ocas-sands skill audits)
- **Notes**: Requires billing enabled on Google Cloud. Not a Reach-registered source — accessed via MCP or direct API calls from consuming skills.
- **Source session**: `20260605_235610_02d858`

### Creative & Media

#### Pollinations.ai
- **Endpoint**: `https://image.pollinations.ai/prompt/{encoded_prompt}`
- **Data**: AI-generated images from text prompts (Stable Diffusion-based)
- **Auth**: None for basic use; API key for higher rate limits
- **Rate limits**: Generous free tier; no key required for low-volume use
- **Quality**: Good for concept art and illustration. Used by ocas-imagine for image generation.
- **Discovered**: 2026-06-05 (ocas-imagine skill audit)
- **Notes**: Free tier is sufficient for most use cases. Image quality comparable to basic Stable Diffusion. No account required.
- **Source session**: `20260605_235610_02d858`

### Museums & Cultural Heritage

#### Digital Art History Directory — Open Data Collections
- **Endpoint**: `https://dahd.hcommons.org/open-data-collections/`
- **Machine-readable endpoint**: `https://dahd.hcommons.org/wp-json/wp/v2/pages?slug=open-data-collections`
- **Data**: Curated directory of open digital art history / museum collection datasets and APIs. Entries currently include Artsy Art Genome Project, Art Institute of Chicago API, Biodiversity Heritage Library, Carnegie Museum of Art dataset, Cleveland Museum of Art Open Access API, Getty Vocabularies LOD, Harvard Art Museums API, Library of Congress Prints & Photographs API, Smithsonian American Art Museum LOD/SPARQL, Met Collection API + CSV, MoMA datasets, National Gallery of Art open data, Nationalmuseum Sweden Wikidata collection, Cooper Hewitt open data/API, Tate dataset, Wikidata Sum of All Paintings, Yale Center for British Art IIIF resources.
- **Auth**: None for the WordPress JSON endpoint.
- **Rate limits**: Not documented; treat as low-volume source-discovery endpoint.
- **Quality**: Curated domain-specific source directory from the Digital Art History Directory / Art Libraries Society of North America context. Useful for discovering candidate Reach sources, not for answering object-level factual queries directly.
- **Cost/terms**: Open web page; individual linked datasets have their own licenses/terms.
- **Discovered**: 2026-07-11 (<operator> suggested DAHD Open Data Collections as an ocas-reach source)
- **Verified**: Browser-like page request redirects through HCommons silent login with HTTP 202, but WordPress REST API returns the published page JSON without login. Extracted 26 links from the page content.
- **Notes**: Register, if integrated, as a `source_directory` / discovery source rather than a primary factual source. Initial Reach actions should be `list_sources` (parse page content into name, URL, description), `get_source` by normalized name, and maybe `refresh_catalog`. Deduplicate against `sources.yml` and this discovered catalog before adding linked APIs. Do not treat directory summaries as authoritative for the linked API's current terms; verify each linked source directly before integration.
- **Source session**: current

#### The Metropolitan Museum of Art Collection API
- **Endpoint**: `https://collectionapi.metmuseum.org/public/collection/v1`
- **Docs**: `https://metmuseum.github.io/`; GitHub/Open Access page: `https://github.com/metmuseum/openaccess`
- **Data**: Open Access metadata for 470,000+ artworks in The Met collection plus high-resolution public-domain JPEGs where available. Endpoints cover all object IDs, single object records, departments, and search. Object records include accession data, public-domain/image flags and URLs, constituents/artist metadata, department, title, culture/period/dynasty, dates, medium, dimensions/measurements, credit line, geography fields, classification, rights, metadata date, repository, object URL, tags with AAT/Wikidata links, object Wikidata URL, Timeline flag, and gallery number.
- **Auth**: None. No API key or registration required.
- **Rate limits**: 80 requests/second. No documented daily/monthly cap.
- **Quality**: Primary source maintained by The Metropolitan Museum of Art; REST JSON API; unrestricted Open Access dataset; direct public-domain image URLs. Stronger immediate Reach candidate than Harvard because no key is needed and commercial/noncommercial use is allowed under CC0 where applicable.
- **Cost/terms**: Free. The Met states it has waived copyright/neighboring rights to the selected dataset using Creative Commons Zero to the extent possible under law; API use remains subject to The Met terms and conditions. Images returned are high-resolution public-domain JPEGs when available.
- **Discovered**: 2026-07-11 (<operator> suggested docs as an ocas-reach source)
- **Verified**: Live API calls succeeded for `/departments`, `/search?q=sunflowers&hasImages=true`, and `/objects/436524`.
- **Notes**: Initial Reach actions should be `list_objects` (with `metadataDate` and `departmentIds` filters), `get_object`, `departments`, and `search_objects` with supported search filters (`q`, `isHighlight`, `title`, `tags`, `departmentId`, `isOnView`, `artistOrCulture`, `medium`, `hasImages`, `geoLocation`, `dateBegin`, `dateEnd`). Citation should prefer `objectURL` for object records and docs URL for aggregate endpoints. Because search returns object IDs only, a higher-level helper may optionally fetch first N object details after search, but should preserve raw IDs/result counts.
- **Source session**: current

#### Harvard Art Museums API
- **Endpoint**: `https://api.harvardartmuseums.org`
- **Docs**: `https://github.com/harvardartmuseums/api-docs`
- **Data**: Harvard Art Museums collections metadata and media: objects, people, exhibitions, publications, galleries, classifications, centuries, colors, cultures, groups, media/technique/support/worktype vocabularies, places, activities, sites, video, image, audio, annotations. Object records include provenance, credit line, dates, culture/classification/medium, people, publications, exhibitions, gallery, colors, images, and IIIF links.
- **Auth**: API key required via Google Form request. Key passed as `apikey` query parameter.
- **Rate limits**: 2,500 requests/day. Default page size 10; max `size=100`.
- **Quality**: Primary source maintained by Harvard Art Museums; data powers the public museum website; refreshed daily around 6am. JSON REST API plus IIIF Image/Presentation services. Strong fit for factual cultural-heritage lookups and collection/image/provenance queries.
- **Cost/terms**: Free, non-commercial only. Do not cache/store content for more than two weeks without written permission. Must identify/link Harvard Art Museums content; use returned image URLs rather than local copies; logo/name hostname restrictions.
- **Discovered**: 2026-07-11 (<operator> suggested GitHub API docs as an ocas-reach source)
- **Notes**: Better than scraping the collection website. Initial Reach actions should likely be `search_objects`, `get_object`, `search_people`, `get_person`, `search_exhibitions`, `get_exhibition`, `search_publications`, `get_publication`, `list_vocab`/resource passthrough, and `iiif_manifest`. Generic resource passthrough may cover the long tail, but object/person/exhibition deserve typed helpers. Citation should include `url` field for object/person records and docs URL otherwise. Requires account provisioning before full integration/testing.
- **Source session**: current

#### Walters Art Museum Collections Data
- **Endpoint**: `https://github.com/WaltersArtMuseum/api-thewalters-org` (static CSV data files); API homepage `https://api.thewalters.org/`
- **Docs**: GitHub wiki linked from repository: objects, images/media, collections, geographies, exhibitions.
- **Data**: Static data files for the Walters Art Museum collections. `art.csv` contains 10,000+ digital object records with fields including object ID/number/name, date begin/end/text, title, dimensions, medium, style, culture, inscriptions, classification, period, canonical resource URL, description, credit line, keywords, provenance, dynasty/reign, geography ID, related objects, image filenames, collection IDs, museum location note, creators, and exhibitions. Related CSVs cover media/images, relationships between objects, collections/categories, geographies, and exhibitions.
- **Auth**: None for GitHub/static files.
- **Rate limits**: GitHub raw/API rate limits apply; no museum API rate limit currently relevant because live v1 API closed in 2023.
- **Quality**: Primary institutional collection data from Walters Art Museum; CC0 and commercial reuse allowed. Good for offline/static factual lookups over Walters collection records and media, but not a live API until v2 comes online.
- **Cost/terms**: Free; repository README states data and images are CC0 for reuse, including commercial purposes. Verify image URL construction/media terms from `media.csv`/wiki before exposing image URLs.
- **Discovered**: 2026-07-11 (<operator> suggested GitHub repo as an ocas-reach source)
- **Verified**: Repository is active/unarchived; README states v1 closed in 2023 and static data files are available until v2. `art.csv` was readable via GitHub API and contains object records with canonical `https://purl.thewalters.org/art/...` citation URLs.
- **Notes**: Register, if integrated, as a static dataset/custom connector rather than a REST API. Initial Reach actions should be `search_objects` (CSV scan/filter), `get_object` by ObjectID/ObjectNumber, `list_collections`, `list_exhibitions`, `get_media` by ObjectID/ObjectNumber, and possibly `download_snapshot`/`refresh_snapshot`. Citation should use `ResourceURL` for object records and repository/docs URL for aggregate queries. Lower immediate priority than The Met for live REST behavior, but valuable because it is CC0 and adds Baltimore/Walters coverage.
- **Source session**: current

### Standards & RFC

#### IETF Datatracker API
- **Endpoint**: `https://datatracker.ietf.org/api/v1`
- **Data**: Machine-readable metadata for IETF/IRTF standards documents — RFCs, Internet-Drafts, working-group charters, groups, persons, meetings, IPR disclosures, liaisons, and more. The `/doc/document/` endpoint alone indexes 157,549 records (drafts, RFCs, reviews, slides). Resource list (from API root): community, dbtemplate, doc, group, iesg, ipr, liaisons, mailinglists, mailtrigger, meeting, message, name, nomcom, person.
- **Auth**: None required for read access (anonymous GET returns 200).
- **Rate limits**: Not published; throttle conservatively (Datatracker is a shared community resource — <2/sec recommended).
- **Quality**: Primary source maintained by the IETF Secretariat. REST JSON (Tastypie-style: `?format=json`, `?limit=`, `?offset=`, filter params per resource). Each record carries a `resource_uri` and grouped `meta` block (total_count, next, previous). Strong structured alternative to scraping Datatracker HTML pages.
- **Cost/terms**: Free, open. IETF community content; attribute appropriately.
- **Discovered**: 2026-07-14 (reach:api-mine — surfaced from interactive sessions referencing `datatracker.ietf.org` during dashboard/MCP-cookie work)
- **Verified**: Live API calls confirmed: `/api/v1/?format=json` (resource list, 200), `/api/v1/doc/document/?limit=1&format=json` (200, total_count 157549), `/api/v1/group/group/?limit=1&format=json` (200), `/api/v1/person/person/?limit=1&format=json` (200), `/api/v1/meeting/meeting/?limit=1&format=json` (200). Anonymous requests succeed without auth. (`/doc/docalias/` 404'd — use `/doc/document/` and filter by `name` for RFC lookup.)
- **Notes**: Initial Reach actions should be `list_resources` (API root), `get_document` (by name, e.g. `rfc9000`), `search_documents`, `get_group`, `get_person`, `get_meeting`. Deduplicate against `sources.yml` and this catalog before integration — not currently present. Better than scraping Datatracker HTML for RFC/WG/meeting metadata. Potential consumer skills: ocas-sift (technical research), ocas-reach (standards fact lookup), ocas-scout.
- **Source session**: `20260713_001806_387698` (and related dashboard-cookie sessions)

### Web Search

#### Google Custom Search API (CSAPI)
- **Endpoint**: `https://www.googleapis.com/customsearch/v1`
- **Data**: Programmatic Google search results (title, URL, snippet, paginated)
- **Auth**: API key + Custom Search Engine ID
- **Rate limits**: 100 queries/day free; 5000/day per $5 (paid)
- **Quality**: Google-quality results via API. Used by ocas-sift as fallback search tier.
- **Discovered**: 2026-06-12 (ocas-sift CSAPI quota management)
- **Notes**: Quota tracking managed by Reach (CSAPI quota). Free tier is limited (100/day). Requires Google Cloud billing for higher volumes.
- **Source session**: `20260612_145529_92eac6`

#### RapidAPI Marketplace
- **Endpoint**: `https://rapidapi.com/hub` (marketplace); individual API endpoints vary
- **Data**: 203+ APIs across finance, crypto, news, geo, weather, security, social, travel, etc.
- **Auth**: RapidAPI key (single key for all APIs); individual APIs may have additional auth
- **Rate limits**: Varies by API; RapidAPI free tier: 500 req/month total
- **Quality**: Mixed — marketplace aggregates many APIs of varying quality. Useful for discovery, not primary sourcing.
- **Discovered**: 2026-06-12 (RapidAPI skill review)
- **Notes**: General-purpose marketplace, NOT "local business search." The `rapidapi` skill is the canonical reference for all 203 endpoints. Use for discovery, then integrate best APIs individually into Reach.
- **Source session**: `20260612_145529_92eac6`

### Models & ML

#### Hugging Face Hub API
- **Endpoint**: `https://huggingface.co/api/` (REST API); also `huggingface_hub` Python library
- **Data**: Search and browse 100K+ ML models, datasets, and Spaces. Returns model metadata (downloads, tags, pipeline type, license), dataset metadata, file listings. Supports filtering by task, language, license, size.
- **Auth**: None for public data; HF token for private repos and higher rate limits
- **Rate limits**: Generous for public data; authenticated users get higher limits
- **Quality**: Largest ML model hub. Useful for finding models for specific tasks (image generation, text classification, etc.), checking model licenses, and discovering datasets.
- **Discovered**: 2026-06-19 (backpopulate scan — sessions reference huggingface.co for model/dataset discovery)
- **Notes**: Not a traditional "data source" but a meta-source for ML capabilities. Could be useful for ocas-imagine (finding image generation models), ocas-finch (finding models for self-improvement experiments), or any skill that needs to programmatically discover ML resources.
- **Source session**: `20260618_215154_7efa2e` (subagent sessions)

### Archives & Newspapers

#### Chronicling America API (Library of Congress)
- **Endpoint**: `https://www.loc.gov/collections/chronicling-america/` (base URL for JSON API queries)
- **Data**: 23+ million digitized historic US newspaper pages (1790-1963). Search by keyword, date range, state, newspaper title (LCCN), language. Returns OCR text, page images, issue metadata, newspaper title directory.
- **Auth**: None required
- **Rate limits**: Undocumented but reasonable; queries returning 100K+ results should be narrowed with facets. Add `&fo=json` for JSON format.
- **Quality**: Primary source for historical newspaper research. Complements Newspapers.com (which has later coverage but no API). Covers African American newspapers (Chicago Defender, Pittsburgh Courier, Baltimore Afro-American, etc.) that are critical for underrepresented subjects.
- **Discovered**: 2026-06-19 (util-wiki skill review — sessions search Chronicling America via browser when researching biographical subjects)
- **Notes**: Preferred over Newspapers.com for programmatic access because: (1) no API, (2) requires subscription, (3) browser-only access. Chronicling America covers the same titles for the 1790-1963 period. Beginning in 2025, Chronicling America is accessible exclusively via the loc.gov API.
- **Source session**: `20260615_180741_fc0c7ced` (util-wiki article research)

#### Google Books API
- **Endpoint**: `https://www.googleapis.com/books/v1/volumes`
- **Data**: Search books by author, title, ISBN, subject. Returns metadata (title, authors, publisher, date, description, page count), snippet previews, cover thumbnails, embeddable viewer links. Supports full-text snippet search within books.
- **Auth**: Google API key (free tier: 1,000 queries/day). No billing required for basic use.
- **Rate limits**: 1,000 queries/day (free); higher with billing
- **Quality**: Best-in-class book metadata and snippet previews. Used by ocas-sift as a source finder. More reliable than OpenLibrary for ISBN and edition data.
- **Discovered**: 2026-06-19 (util-wiki Phase 2 source verification — finding books by/about biographical subjects)
- **Notes**: Preferred over scraping Google Books web pages. The API returns structured metadata that can be used to verify publication details, find related editions, and check whether a book covers a specific subject.
- **Source session**: `20260615_180741_fc0c7ced` (util-wiki article research)

#### OpenLibrary API (Internet Archive)
- **Endpoint**: `https://openlibrary.org/search.json` (search); `https://openlibrary.org/works/{OLID}.json` (work details); `https://openlibrary.org/books/{ISBN}.json` (edition by ISBN)
- **Data**: Search books, authors, subjects. Returns work-level and edition-level metadata, author data, cover images, subject tags, reading logs. Data dumps available for bulk access.
- **Auth**: None for search/lookup. Optional account for higher rate limits.
- **Rate limits**: 1 req/sec (anonymous); 3 req/sec (identified with User-Agent + email header)
- **Quality**: Fully open data (CC0). Internet Archive project with strong coverage of older and public-domain works. Complements Google Books — when Google lacks a preview, OpenLibrary often has the full text.
- **Discovered**: 2026-06-19 (util-wiki source verification — cross-referencing book sources for biographical articles)
- **Notes**: Preferred over scraping. The search API supports structured queries (author, title, subject, ISBN) with faceted results. For Wikipedia editing, useful for verifying book citations and finding open-access full-text sources.
- **Source session**: `20260615_180741_fc0c7ced` (util-wiki article research)

---

## Quality Rankings

_Force-ranked within each data type. Only populated when 2+ discovered APIs compete._

### Prediction Market Data

| Rank | API | Why |
|------|-----|-----|
| 1 | Kalshi API | Free REST API, structured JSON, covers multiple categories, no auth required, active markets with volume |
| 2 | Polymarket Gamma API | Good for elections/politics, but narrower category coverage than Kalshi |

### Brokerage & Trading

| Rank | API | Why |
|------|-----|-----|
| 1 | Alpaca API | Full brokerage (paper + live), well-documented, free tier, supports stocks/crypto/options |
| 2 | Finnhub | Good for fundamentals/market data, but no trading capability |

### Financial Fundamentals

| Rank | API | Why |
|------|-----|-----|
| 1 | Finnhub | Free tier sufficient, comprehensive fundamentals, WebSocket for real-time |
| 2 | Massive API | Alternative/ESG data, but paid and niche |

### General Web Search

| Rank | API | Why |
|------|-----|-----|
| 1 | SearXNG (self-hosted, in main index) | Metasearch 70+ engines, no key, no CAPTCHA from VPS |
| 2 | Google CSAPI | Google-quality results, but 100/day free limit is restrictive |
| 3 | RapidAPI Marketplace | Useful for discovery, but mixed quality and 500 req/month free limit |

### Image Generation

| Rank | API | Why |
|------|-----|-----|
| 1 | Pollinations.ai | Free, no key required, good quality for concept art |

### Museums & Cultural Heritage

| Rank | API | Why |
|------|-----|-----|
| 1 | The Met Collection API | Primary museum source, 470k+ objects, no auth, 80 req/sec, CC0/Open Access, direct public-domain image URLs |
| 2 | Harvard Art Museums API | Richer/more varied museum metadata and IIIF support, but requires key and is non-commercial with stricter caching/attribution terms |

### Archives & Newspapers

| Rank | API | Why |
|------|-----|-----|
| 1 | Chronicling America API | Free, no auth, 23M+ pages, covers 1790-1963, preferred over Newspapers.com (no API) |
| 2 | Google Books API | Free tier sufficient, best snippet previews, structured metadata |
| 3 | OpenLibrary API | Fully open data, good for older/public-domain works, but lower rate limits |

---

## Recently Discovered

_Newest additions go here first. When fully categorized and indexed, move to Registry._

### Web Data Extraction

#### Zyte API
- **Endpoint**: `https://api.zyte.com/v1/extract` (POST); docs `https://docs.zyte.com/`
- **Data**: Web page content extraction with three capabilities in one call: (1) **unblocking** — anti-bot bypass (proxy rotation, fingerprint matching, challenge solving) via `httpResponseBody` field; (2) **JS rendering** — headless browser load with optional actions (click, scroll, wait, screenshot, geolocation) via `browserHtml` field; (3) **automatic structured extraction** — named data types (Product, Article, ArticleList, productList, jobPosting, forumThread, SERP) extracted by model, no CSS/XPath selectors required. Each result includes a confidence score (`extractionProbability`) and typed/named fields.
- **Auth**: HTTP Basic Auth — API key as user name, empty password.
- **Rate limits**: Usage-based (paid); no published hard limit. Pay-per-request pricing on Zyte's website. Free trial available.
- **Quality**: Commercial-grade extraction maintained by Zyte (same company behind Scrapy). Extraction models are site-adaptive — layout changes don't break selectors. 0.997 extraction probability demonstrated on test page.
- **Cost**: Paid (usage-based). Requires credit card/billing account. Not currently budgeted.
- **Discovered**: 2026-09-16 (web research — efoss article "Web Scraping With A Single API" by Ayan Pahwa, Open Source For Us)
- **Source session**: current
- **Notes**: Integrates natively with Scrapy via `scrapy-zyte-api` addon and `scrapy-poet` DI. Zyte also publishes a Claude Code plugin for AI-assisted scraper generation. Not yet live-verified from this host. Candidate for sift.fetch tier 3.5 if budget permits and donsetch proves insufficient for anti-bot. For now, catalog only — requires account provisioning + billing authorization before integration.

### Satellite & Earth Observation

#### NASA GIBS (Global Imagery Browse Services)
- **Endpoint**: `https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/` (WMTS REST/KVP); also WMS, TWMS, XYZ/TMS
- **Data**: ~180+ satellite imagery layers — MODIS, VIIRS, Landsat, Sentinel-2 (best available), MERRA-2 climate reanalysis, GEDI biomass, sea surface temperature, fire detection, aerosols, vegetation indices, and more. Global coverage, daily cadence for many layers, some near-real-time. Time dimension: YYYY-MM-DD per tile, with date ranges per layer (some back to 1980).
- **Auth**: None required
- **Rate limits**: No documented hard cap; be reasonable
- **Quality**: Authoritative NASA source. WMTS standard (OGC). Tiles are pre-rendered PNG at fixed zoom levels (250m to 16km). GetCapabilities XML lists all layers with identifiers, date ranges, projections, tile matrix sets. Massive GetCapabilities response (~5MB).
- **Discovered**: 2026-06-24 (evaluating Earth View github.com/colincode0/earth-view as source reference)
- **Notes**: Different from existing `nasa` source (which covers api.nasa.gov query APIs like APOD/NEO/EONET). GIBS is a tile imagery service — complementary, not overlapping. The `nasa` source's `eonet` action covers natural events; GIBS covers the underlying imagery. Earth View (colincode0/earth-view) uses GIBS as its primary globe renderer. Also used by VEDA, OpenStreetMap, and many scientific visualization tools.
- **Integration plan**: Add as `gibs` source with actions: `get_capabilities` (parse layer list from WMTS GetCapabilities XML), `get_tile` (construct tile URL from layer/zoom/row/col/date params), `list_layers` (filtered search across capabilities). Custom connector needed because WMTS is not a simple REST query pattern.
- **Source session**: current

### News & Social

#### Hacker News API
- **Endpoint**: `https://hacker-news.firebaseio.com/v0` (Firebase REST)
- **Data**: Tech-news / social aggregator. `topstories.json`, `newstories.json`, `beststories.json` return arrays of item IDs; `item/<id>.json` returns a story/job/poll/comment object (`by`, `title`, `url`, `text`, `score`, `time`, `descendants`/comment count, `kids`/comment IDs, `parent`); `user/<id>.json` returns a user profile (`id`, `about`, `karma`, `created`, `submitted[]`); `updates.json` returns recently changed items/users. All JSON.
- **Auth**: None required (public Firebase API)
- **Rate limits**: Not published; Firebase-backed, generous. Throttle to <1-2/sec to be safe.
- **Quality**: Primary source maintained by Y Combinator. Real-time community-curated tech/news stories and discussion. Structured, no scraping needed.
- **Discovered**: 2026-07-23 (reach:api-mine — surfaced from ocas-haiku content-queue workflow that already fetches HN top stories via curl)
- **Verified**: Live calls confirmed: `/v0/topstories.json` (returns ID array), `/v0/item/<id>.json` (returns full story object with `by`/`descendants`/`kids`/`score` fields).
- **Notes**: Complements `reddit` (main index) as a social/news signal source. Candidate consumer skills: ocas-haiku (content queue already pulls HN top stories), ocas-sift (tech-news research), ocas-vesper (daily briefing top stories). Better than scraping HN web pages or relying on ad-hoc curl scattered across skills. Initial Reach actions: `top_stories` (fetch + resolve N items), `get_item`, `get_user`, `updates`. Deduplicate against `sources.yml` and this catalog before integration — not currently present.
- **Source session**: `20260716_175117_de5bb7` (and HN-referencing sessions in the 7d window)

_All other discovered APIs have been moved to the Registry above. This section will populate with new discoveries from future cron runs._

### Music & Audio

#### MusicBrainz API
- **Endpoint**: `https://musicbrainz.org/ws/2/` (REST); docs `https://musicbrainz.org/doc/MusicBrainz_API`; also `https://beta.musicbrainz.org/ws/2/` (beta)
- **Data**: Authoritative music metadata database — artists, releases/albums, release-groups, recordings (songs), works, labels, places, events, instruments, series, URLs. Each entity carries stable UUID (**MBID**) identifiers, artist-credit, dates, barcodes, ASIN, label/catalog info, track/medium counts, country, lyrics/relations via linked entities. Supports structured search (`?query=artist:"X" AND release:"Y"`) per entity type plus direct MBID lookups, browse (`?inc=`), and linked entity `inc` includes (release-groups, recordings, etc.).
- **Auth**: None required for public read (must send a descriptive `User-Agent` identifying the client; the API `403`s or `503`s bare/HTTP-client defaults).
- **Rate limits**: Public pool ~1 request/sec / 100 req/min; extremely strict. Self-host the data (MusicBrainz data is CC0, released under the Open Data license; monthly data dumps + `brainz-musicbrainz-docker` replication available) for heavier use.
- **Quality**: Community-curated primary source (the de-facto canonical music identifier system, used as the identifier backbone by Spotify, Wikipedia, and music fingerprinting). CC0/Open Data licensed.
- **Discovered**: 2026-09-11 (reach:api-mine — surfaced from the DroppedNeedle music-library session, which resolved 2021 albums / 897 artists from Google Drive to MBIDs via this API)
- **Verified**: Live `release` search (`query=artist:"Lykke Li" AND release:"Wounded Rhymes"`) returned real structured release JSON including MBID, artist-credit, barcode, label-info, track-count (HTTP 200). One subsequent rapid artist lookup returned `503 busy` — confirming the aggressive 1 req/sec limit; throttle strictly.
- **Notes**: Complements existing `openalex`/`arxiv` scholarly sources for a factual music-metadata domain. Candidate consumer skills: ocas-haiku (music content), ocas-sift (music research), ocas-reach (music fact lookup), ocas-voyage (venue/event context). No existing source in `sources.yml` covers music metadata. Initial Reach actions: `search` (per entity type: artist/release/release-group/recording/work/label), `get_entity` by MBID, `browse` with `inc` links. Mandatory descriptive User-Agent; throttle to ~1/sec.
- **Source session**: `20260911_020506_ebd047` (and `20260911_004332_793d948d` DroppedNeedle setup)

#### DroppedNeedle REST API (self-hosted service)
- **Endpoint**: `/api/v1` on the deployed instance (`tunes.indigokarasu.com`); OpenAPI spec at `/openapi.json` on the same instance
- **Access**: Self-hosted Docker service (port 8688), behind nginx basic-auth + app login on `tunes.indigokarasu.com`; has an API key for the slskd backend integration. Uri is instance-specific — not a public shared API.
- **Data**: Music search/download via the slskd (Soulseek) backend — search artists/albums/tracks, queue downloads (FLAC preference), resolve albums to MusicBrainz IDs. Exposes song files through the shared storage mount.
- **Verdict**: Confirmed working + deployed and health-checked 2026-09-11 (container healthy, reaches slskd API 200). Integrated into the personal music-library workflow (GDrive album list → MBID resolve → queue FLAC downloads). Self-hosted/instance-scoped, so it belongs as a skill-integrated connector (like LetsFG/HotelsByDay) rather than a shared Reach world-data source.
- **Source session**: `20260911_004332_793d948d`, `20260911_020506_ebd047`

### Travel & Lodging
| Data | Best Source | Alternatives | Notes |
|------|-------------|--------------|-------|
| Flight search + real booking | LetsFG API | `fli` lib (Google Flights data) | Agent-native CLI/SDK/MCP; booking requires card-on-file auth |
| Day-use hotel rates | HotelsByDay API | browser scrape | Internal JSON API at api.hotelsbyday.com; integrated in Voyage script |
| Overnight hotel rates + compare | HotelOracle MCP (SerpAPI backend) | Google Hotels (browser) | 8 research-only tools |
| Hotel booking w/ identity-verified tools | 1Stay MCP (mcp.stayker.com) | — | 8 tools incl. lookup/cancel/resend; Bearer auth |

#### LetsFG API
- **Endpoint**: CLI (`letsfg`), Python SDK, MCP (`npx letsfg-mcp`); docs https://letsfg.co/for-agents
- **Access**: Freemium search AFTER one-time `letsfg auth` (zero-amount Stripe card-on-file → 90-day Bearer token). NEVER use `/developers/api/v1/agents/register` or `setup-payment` (paid Developer billing).
- **Data**: Flight search/book across airlines+OTAs incl. budget carriers; hotel search/book (free-cancellation pay-later rates, 5% non-refundable reservation fee).
- **Verdict**: Confirmed working; already integrated into ocas-voyage (`references/letsfg.md`). Better than scraping for actual booking without OTA redirect.

#### HotelsByDay API
- **Endpoint**: `https://api.hotelsbyday.com` (internal JSON API discovered from site JS)
- **Access**: No public key required for autocomplete/search/hotel-detail flows used by the site.
- **Data**: Day-use (daytime) hotel availability, rates, room detail.
- **Verdict**: Confirmed working; integrated into ocas-voyage as `scripts/hotelsbyday_search.py`. Better than browser scraping.

#### HotelOracle MCP
- **Endpoint**: Via Glama connector (io.tooloracle/hoteloracle); SerpAPI-backed
- **Access**: MCP tools: search_hotels, hotel_details, price_calendar, price_compare, area_guide, best_deals, nearby_attractions, health_check.
- **Data**: Multi-site hotel rate comparison.
- **Verdict**: Research-only (no booking); known failure mode: SerpAPI empty responses with auto-refunded credits. Integrated in ocas-voyage lodging-sources.md.

#### 1Stay MCP (stayker)
- **Endpoint**: `https://mcp.stayker.com/mcp`, Bearer auth (sandbox vs production key scopes)
- **Access**: 8 tools: search, details, lookup_booking, get_booking, cancel_booking (two-step), resend_confirmation, search_tools; chain_code brand filter.
- **Verdict**: Documented live 2026-08-08; integrated in ocas-voyage lodging-sources.md. Rate codes expire in 15 min; checkout URLs in 30 min.
