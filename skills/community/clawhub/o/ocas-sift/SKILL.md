---
name: ocas-sift
source: https://github.com/indigokarasu/sift
description: >-
  Sift: web search, research synthesis, fact verification, entity extraction,
  and URL content extraction. The system's general research engine. Use for ANY
  task requiring web information: search, research, look up, investigate, find
  out, check if, fact check, compare, summarize, what is, how to, product
  recommendations, price checks, current events, or reading a specific URL.
  TRIGGER ON: any question requiring current web data, any "investigate/find
  out/check/look into" request, any product/price/recommendation query. Do NOT
  use browser for search (CAPTCHA'd on VPS). The `web_search` and `web_extract`
  MCP tools route to SearXNG automatically — for deep research, load this skill
  directly. Do not use for person-focused OSINT (use Scout) or image
  processing (use Look).
license: MIT
includes:
- references/**
- scripts/**
metadata:
  author: Indigo Karasu (indigokarasu)
  version: "2.10.0"
triggers:
- web search
- research synthesis
- fact verification
- extract URL content
- search the web
- investigate
- find out
- check if
- look into
- product research
- price check
- recommendation
- current events
- how to
- what is
- compare products
---

# Sift

Sift is the system's general research engine, retrieving and synthesizing information from the web across a tiered source hierarchy — internal knowledge first, then free web search, then rate-limited semantic research providers for deep work. It evaluates source reliability through cross-source agreement scoring, extracts structured entities from retrieved content, and emits enrichment candidates to Chronicle so researched knowledge accumulates over time.

## Load-First Rule for Web-Adjacent Queries

**When the user asks about products, prices, reviews, how-to advice, or any information that requires current web data, load Sift FIRST before answering from domain knowledge.** This applies even if you think you already know the answer from training data.

**Why this matters:** On VPS/cloud environments, browser-based search (Google, Bing, DuckDuckGo) is almost entirely blocked by CAPTCHA from datacenter IPs. The `web_search` and `web_extract` MCP tools handle basic searches automatically via SearXNG. Load this skill directly for deep research, fact-checking, comparisons, or when the MCP tools' results are insufficient.

If you answer from domain knowledge without checking current sources, you may miss: product availability changes, new products on the market, updated formulations, price changes, or critical caveats (e.g., fabric-specific limitations like synthetic vs. cotton).

**Pattern to follow:**
1. User asks about a product/recommendation/how-to → load Sift
2. Run SearXNG: `curl -s "http://localhost:8888/search?q=QUERY&format=json"`
3. Fetch top result URLs with `curl -sL` or `sift.fetch`
4. THEN synthesize answer with citations

**Exception:** Pure factual lookups ("what is the capital of France") that don't require web data can be answered from internal knowledge.

## When to use

**LOAD SIFT FIRST — before any other action — when:**
- The user asks ANY question requiring current web data (not in your training data)
- The user says "search for", "look up", "research", "investigate", "find out", "check if", "look into"
- The user asks about products, prices, reviews, recommendations
- The user asks "what is", "how to", "why does", "when did" about current topics
- The user asks about current events, news, or recent developments
- You need to verify a fact or claim against current sources
- You need to compare products, technologies, or options using current data
- You need to fetch/extract content from a specific URL
- You're about to use the browser for ANY information-seeking purpose
- You're about to use `execute_code` to scrape a search engine

**In short: if you need information you don't already have loaded Sift first.**

Specific use cases:
- Web search and research synthesis on any topic
- Fact verification across multiple sources with consensus scoring
- Document summarization and structured entity extraction
- Comparison research across products, technologies, or options
- Deep research sessions with multi-source threading
- Product/price/recommendation research
- Current events and news research

## When not to use

- OSINT investigations on individuals — use Scout
- Image-to-action processing — use Look
- Pattern analysis on the knowledge graph — use Corvus
- Communications and message drafting — use Dispatch

Sift never performs OSINT investigations on individuals. If the primary entity of a query is a person, Scout should be invoked.

## Responsibility boundary

Sift owns web research, fact verification, and structured entity extraction.

Sift does not own: person-focused OSINT (Scout), image processing (Look), knowledge graph writes (Elephas), pattern analysis (Corvus), social graph (Weave).

## Ontology types

Sift works with these types from `spec-ocas-ontology.md`:

- **Entity/Person, Entity/AI** — people and agents identified during research.
- **Place** — locations, venues, and organizations.
- **Concept/Event, Concept/Idea** — events, topics, and themes extracted from research.
- **Thing/DigitalArtifact** — documents, articles, and digital records.

Sift emits Signals to Elephas for entities and relationships extracted with confidence >= med. Signal `payload.type` is the ontology type of the primary entity. `source_journal_type` is `"Research"`. Every emitted Signal must include a `user_relevance` field.

### user_relevance field

Every Signal emitted by Sift carries a `user_relevance` field with one of two values:

- `"user"` — the signal is relevant to the user's personal knowledge graph
- `"agent_only"` — the signal is agent-initiated research with no demonstrated user connection

**Default is `"agent_only"`** because much of Sift's research may be agent-initiated (scheduled runs, background enrichment, cooperative queries from other skills). A signal receives `user_relevance: "user"` only when:

Signal example:
```json
{
  "signal_id": "sig-sift-20260402-001",
  "source_skill": "ocas-sift",
  "source_journal_type": "Research",
  "emitted_at": "2026-04-02T14:30:00Z",
  "user_relevance": "agent_only",
  "payload": {
    "type": "Concept/Event",
    "name": "2026 Solar Eclipse",
    "confidence": "high",
    "source_refs": ["https://example.com/eclipse"]
  }
}
```

Sift may read Thread's active context for query rewriting and Weave's database for entity disambiguation (both cooperative read-only; see `spec-ocas-interfaces.md` Cooperative Query Interfaces).

## Commands

- `sift.search` — execute a search query with automatic tier selection and query rewriting
- `sift.research` — run a multi-source research session producing a structured research journal
- `sift.verify` — fact-check a specific claim across multiple sources with consensus scoring
- `sift.summarize` — summarize a document or URL with structured entity extraction
- `sift.extract` — extract entities, claims, statistics, and relationships from content
- `sift.thread.list` — list active research threads with entity overlap detection
- `sift.status` — return current state: active threads, quota usage, source reputation summary
- `sift.journal` — write journal for the current run; called at end of every run
- `sift.update` — pull latest from GitHub source; preserves journals and data
- `sift.fetch [url]` — extract clean Markdown content from a URL. Runs Scrapling first (fast HTTP for static sites, headless browser mode for JS-heavy sites); falls back to Jina Reader (`r.jina.ai/<url>`) if Scrapling output is below content threshold. Returns Markdown with structure preserved. Use for summarizing a specific page or document the user provides. **Exit codes:** `0` success · `1` permanent error (escalate to `donsetch fetch`) · `2` transient (retry) · `3` walled (escalate to `donsetch fetch` or `sift.webwright`). See `references/donsetch-integration.md` for the full anti-bot escalation chain.
- `donsetch fetch [url]` — anti-bot / Cloudflare-blocked fetch via the locally installed `donsetch` binary (v3.2.3, AGPL, `/usr/local/bin/donsetch`). Uses real Chrome TLS, solve-and-bounce, and headless escalation. Use when `sift.fetch` returns exit 1/3, bot-wall / 403 / empty / CAPTCHA on CF, Akamai, DataDome, Imperva. See `references/donsetch-integration.md`.
- `sift.webwright` — execute an interactive web task using browser automation (Playwright driving the system Chrome). **Requires the `playwright` package** (`pip install playwright`); it uses the already-installed Chrome via `channel="chrome"`, so no browser download is needed. Write the plan, exploration screenshots, instrumented final_script.py, execution log, and self-verification into `{agent_root}/commons/data/ocas-sift/webwright/`. For form filling, multi-step flows, JS-heavy sites, interactive filtering, or any task where the browser is the workspace. Read `references/webwright-integration.md` before first use.

## Response modes

Sift classifies query depth automatically:

- **quick_answer** — simple factual lookups, single-source sufficient
- **comparison** — multi-source comparison with structured output
- **research** — deep multi-session investigation with threading
- **document_analysis** — URL or document-focused extraction

Users may override with phrases like "quick answer", "deep dive", "compare", or "summarize".

## Search tier selection

All configured search sources fire in parallel. Results are deduplicated by URL and content hash.

- **Internal knowledge** — LLM knowledge, conversation context, Chronicle if available. Always runs first as a pre-check.
- **Free web search (parallel fan-out)** — all of the following fire simultaneously:
  - **N2 MCP** (`n2_web_search`) — SearXNG-backed, no API key required. Registered during `sift.init`. Also provides `n2_news_search` for recency-focused queries. See `references/searxng-diagnostics.md` for engine-health diagnostics.
  - **Brave Search API** — structured web results. See `references/search_tiers.md` for provider configuration and API keys.
  - **SearXNG** — self-hosted instance on `http://localhost:8888`. **This is the primary search source on VPS environments.** Always returns results when browser-based search is CAPTCHA-blocked. **Fallback cascade**: when a primary web-search API hits a rate limit / 429 (Brave, N2 MCP outage, etc.), escalate to the local SearXNG instance (`http://localhost:8888/search?q=...&format=json&limit=10`) before attempting paid/CSAPI tiers.
  - **Platform search** — agent-reach on Twitter/X (via Mirror Rotator → Search Bridge), Reddit, LinkedIn, GitHub, etc.
- **Google Custom Search API (CSAPI)** — fallback when free web search returns insufficient results. Uses `mcp_google_workspace_search_custom`. Quota-limited: 1,000 queries/month free tier. Check quota before calling (`csapi_quota.py check`), increment after (`csapi_quota.py increment`).

**Output format:** Helper scripts (`scripts/*.py`) support `--format=concise` (default — high-signal fields only, ~60–80% token savings or `--format=detailed` (full envelope/UUIDs/fields for downstream programmatic chaining). Every script failure path returns a JSON envelope with human-actionable `actionable_guidance`.

**Extraction tooling:** `get-md` (`indigokarasu/get-md`) is the default HTML-to-Markdown extraction engine — use it over ad-hoc extraction scripts. `sift.fetch` routes clean Markdown via Scrapling → Jina Reader → Wayback fallback → get-md.

For detailed tier-by-tier workflow, API curl examples,and cloud environment fallbacks, read `references/research-workflow.md` and `references/vps-search-cheat-sheet.md`.

## Source reputation model

Sift maintains per-domain trust scores based on: cross-source agreement, contradiction frequency, historical accuracy, structured data quality, citation frequency.

## Structured extraction rules

When pages are retrieved, extract: entities (with type from shared ontology), claims, statistics, relationships, citations. Each extraction includes confidence level.

Extracted entities are emitted as enrichment candidates for Elephas.

## Run completion

After every Sift command that produces results:

1. Persist session, entities, sources, and decisions to local JSONL files
2. For each extracted entity or relationship with confidence >= `med`: write a Signal file to the `signal` payload field in the journal entry. Use Signal schema from `spec-ocas-shared-schemas.md`. Every Signal must include `user_relevance` (see Ontology types section). Set `"user"` if the run was user-initiated or the entity connects to a `user_relevance: "user"` Chronicle entry; otherwise `"agent_only"`.
3. Write journal via `sift.journal`

## sift.fetch behavior

`sift.fetch [url]` extracts clean Markdown from a specific URL.

Do not use `sift.fetch` for general search — it fetches a specific known URL only.

## Chronicle interaction

Sift never writes directly to Chronicle. It emits enrichment candidates via Signal files.

## Inter-skill interfaces

Sift writes Signal files to Elephas (via journal signal payload): the `signal` payload field in the journal entry.

## Pitfalls & Tips

Read `references/pitfalls.md` for the full list. Key highlights:

- **Answer-from-knowledge trap:** Don't answer product/how-to questions from training data alone. Use SearXNG + fetch. (See Load-First Rule above.)
- **CAPTCHA cascade:** From cloud environments most search engines block automated browsers, but not uniformly — measured from this host through the system Chrome, Google's results page serves an "unusual traffic" reCAPTCHA with zero results while Bing answers normally. Prefer SearXNG (`localhost:8888`) or CSAPI, and if you do drive a browser, check the page for CAPTCHA markers rather than assuming an empty result set means the subject is unfindable.
- **Credential sanitizer blocks API key writes:** The Hermes output sanitizer intercepts API keys. If CSAPI fails with missing key, the owner must add it manually.

## Support file map

| File | When to read |
|---|---|
| `references/dye-transfer-fabric-guide.md` | When researching dye transfer, color run, or stain removal from clothes — fabric-specific product recommendations |
| `references/pitfalls.md` | Before research runs; CAPTCHA cascade, answer-from-knowledge trap |
| `references/search_tiers.md` | Before tier selection or escalation |
| `references/research-workflow.md` | When executing research sessions from cloud environments |
| `references/csapi-quota.md` | Before calling `search_custom` — quota tracking |
| `references/schemas.md` | Before creating sessions, threads, or extraction records |
| `references/query_rewrite.md` | Before query rewriting |
| `references/journal.md` | Before sift.journal; at end of every run |
| `references/mcp-redirect-pattern.md` | The MCP redirect pattern — how phantom tool calls (web_search, web_extract) are intercepted and routed to SearXNG via MCP servers |
|| `references/webwright-integration.md` | Before `sift.webwright` |
|| `references/local-business-search.md` | When searching for local businesses, services, or venues — RapidAPI Places workflow |
|| `references/donsetch-integration.md` | When `sift.fetch` fails with bot-wall / 403 / empty / CAPTCHA — anti-bot tier-3 fallback |
|| `references/fetch-behavior.md` | Before using `sift.fetch` — fetch pipeline behavior, thresholds, and fallback logic |
|| `references/vps-search-cheat-sheet.md` | When running searches from VPS/cloud — quick SearXNG + CSAPI + donsetch commands |
|| `references/searxng-diagnostics.md` | When SearXNG returns poor coverage — engine health check + N2 MCP notes |

## Background tasks

| Job name | Mechanism | Schedule | Command |
|---|---|---|---|
| `sift:update` | cron | `0 0 * * *` (midnight daily) | `sift.update` |

## Self-update

`sift.update` pulls the latest package from GitHub. Runs silently.

## Visibility

public

## Optional skill cooperation

- Elephas — emit Signal files for Chronicle promotion
- Thread — may read recent browsing context for query rewriting
- Weave — may use for entity disambiguation
- Chronicle — may read for entity context
- Look — reverse image search capability
