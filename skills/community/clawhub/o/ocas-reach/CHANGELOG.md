# Changelog

## [3.12.0] - 2026-09-16

### Changed
- **Actionable error envelopes** — `reach.py` wraps HTTP/network errors in JSON envelopes including `actionable_guidance` with retry-backoff rules (429/5xx → backoff; 401/403 → verify credential; 404 → verify path; network → retry+check connectivity) per `spec-ocas-scripts.md`.
- Fixed pre-existing syntax bug in `USER_AGENT` (nested quote string) breaking the script.


## [3.6.0] - 2026-05-28

### Added — Consolidated weather source

- **`weather` source** — Unified weather connector wrapping NWS, SPC, METAR (aviationweather.gov), and Open-Meteo behind a single 7-action interface: `conditions`, `forecast`, `alerts`, `metar`, `brief`, `global`, `severe`. Logic ported from the hermes-weather-plugin by FahrenheitResearch (MIT). Pure Python, no Rust/binary dependencies.
- **`scripts/sources/weather.py`** — Custom connector module. Handles multi-step NWS resolution (points → stations → observations), SPC GeoJSON parsing, and Open-Meteo unit selection.
- **Routing hints updated**: all weather queries now route to `weather` first; `noaa_nws` and `open_meteo` retained for raw API shapes and archival access.
- **Source count**: 53 → 54 registered sources.

### Changed

- SKILL.md version bumped 3.5.0 → 3.6.0.
- `references/sources/index.md`: added `weather` entry to source table; replaced `noaa_nws`/`open_meteo` weather routing hints with `weather`-primary entries.

## [3.5.0] - 2026-05-13

### Added — Web search, social, and Yahoo Finance MCP

- **`searxng` source** — Local SearXNG metasearch engine. Open web search + social media search (Reddit, Stocktwits, Twitter/X). No API key needed. Enables `social_heat` signal for Rally sentiment.
- **`yahoo_finance` source** — Yahoo Finance MCP server (`yahoo-finance-mcp` by Alex2Yang97). Provides historical prices, financial statements, news, analyst recommendations, holder info, options chain, and stock actions. No API key needed. Custom connector: `scripts/sources/yahoo_finance_mcp.py`.
- **Source count**: 51 → 53 registered sources.

### Architecture

- SearXNG is a direct HTTP source (no MCP needed — it has a clean JSON API).
- Yahoo Finance uses MCP stdio transport (same pattern as Reddit, Paper Search, LinkedIn).
- Rally's `rally_data_sources.py` updated to use SearXNG for `social_heat` and Yahoo Finance MCP as fallback for sentiment/news/recommendations.

## [3.4.0] - 2026-05-13

### Added — Media and academic sources via MCP

- **`reddit` source** — Reddit browser via `reddit-mcp-buddy` MCP server. Browse subreddits, search posts, get post details, analyze users. Anonymous mode (10 req/min) or OAuth (60-100 req/min). Custom connector: `scripts/sources/reddit_mcp_buddy.py`.
- **`paper_search` source** — Multi-source academic paper search via `paper-search-mcp` MCP server. Searches 20+ platforms (arXiv, PubMed, bioRxiv, Semantic Scholar, Crossref, OpenAlex, etc.) with unified deduplication. Custom connector: `scripts/sources/paper_search_mcp.py`.
- **`linkedin` source` — LinkedIn profiles, companies, jobs, and messaging via `linkedin-scraper-mcp` MCP server. Browser automation with saved session. 16 actions including person_profile, company_profile, search_people, search_jobs, feed, inbox. Requires login. Custom connector: `scripts/sources/linkedin_mcp.py`.
- **"Media and social sources" section** added to `references/sources/index.md`.
- **Routing hints** updated for Reddit, paper_search, and LinkedIn.
- **Out of scope** updated: Reddit and LinkedIn removed from excluded list.
- **Source count**: 48 → 51 registered sources.

### Architecture note

All three new sources use MCP stdio transport (subprocess JSON-RPC) rather than direct HTTP. This pattern is now the preferred integration method for complex APIs that have existing MCP server packages. The `_MCPClient` class in each connector handles the MCP handshake, tool invocation, and response parsing.

## [3.0.0] - 2026-04-26

### Added
- Unified source registry at `scripts/sources.yml` declaring 35 new sources across knowledge / government / science / weather / geo / finance / health / media categories
- `scripts/reach.py` orchestrator: generic HTTP dispatch, custom-module hooks, per-source daily/monthly quota enforcement, journal emission, env-var auth resolution
- Custom Python modules for multi-step sources: `scripts/sources/sec_edgar.py`, `scripts/sources/pubmed.py`, `scripts/sources/wikidata_sparql.py`, plus shared `scripts/sources/_http.py`
- `references/sources/index.md` — authoritative source index with category, auth, account, quota, and routing-hints tables
- Per-source reference files at `references/sources/<slug>.md` (37 sources) covering data scope, endpoints, response shape, pitfalls
- `references/account_provisioning.md` with explicit account-creation grant authorizing Reach to register accounts at `account: required` and `account: optional` sources using `<agent-email>`
- `references/usage_tracking.md` documenting the `usage.jsonl` log and quota derivation
- New CLI subcommands: `reach.py sources`, `reach.py source <name>`, `reach.py usage [--month YYYY-MM]`
- `_template.md` skeleton for adding new source references

### Changed
- Storage: `queries.jsonl` replaced by `usage.jsonl` (call log) and `accounts.json` (account ledger)
- SKILL.md: added Source registry section, Account-creation grant section, expanded routing description, and an explicit list of what Reach is not authorized to do during registration
- Generic HTTP dispatch now handles auth via path/query/body/header insertion declared per-action in the registry
- README rewritten to describe the registry, cite the index, and list the new commands

### Removed
- The single-source `sources` field in SKILL.md (replaced by the registry pointer)

## [2.0.0] - 2026-04-26

### Changed
- Restructured to OCAS architecture standard: scripts moved from `sources/<source>/connector.py` to top-level `scripts/<source>.py`; per-source READMEs moved to `references/<source>.md`
- SKILL.md rewritten with required system-skill sections (Trigger conditions, Responsibility Boundary, Optional Skill Cooperation, Decision model, Execution loop, Storage Layout, Journal Outputs, Background tasks, Visibility)
- Storage moved out of the skill package to `{agent_root}/commons/data/ocas-reach/` per spec-ocas-storage-conventions.md
- Author email and version metadata added to SKILL.md frontmatter
- Update mechanism switched from `git source update` reference to `reach.update` cron job
- README description rewritten as routing-aware text, not branding copy

### Added
- `scripts/property_lookup.py` — first connector implementation for the Redfin/Zillow/SF-assessor lookup chain (previously only documented)
- Observation Journal emission for every query
- `queries.jsonl` append-only query log
- README.md and CHANGELOG.md per spec-ocas-skill-publishing.md
- `reach:update` daily self-update cron job

### Fixed
- Removed hardcoded `RT_KEY` value from SKILL.md and per-source documentation; all auth via `~/.hermes/.env`

### Removed
- `sources/` directory layout (non-standard, conflicted with OCAS scripts/references separation)

## [1.0.0] - 2026-04-26

### Added
- Initial release with `sources/katzilla/katzilla.py` connector for US government data
- Documentation stub for `sources/property-lookup/`
