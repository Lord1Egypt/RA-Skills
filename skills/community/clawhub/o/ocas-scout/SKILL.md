---
name: ocas-scout
description: 'Structured OSINT research on people, companies, and organizations. Use for provenance-backed briefs, entity resolution across public sources, background research with cited sources, or free-first research workflows that escalate to paid sources only with explicit permission. Do not use for topic research without a person/org focus (use Sift) or illegal data collection.'
license: MIT
source: https://github.com/<agent-handle>/scout
includes:
- references/**
- scripts/**
metadata:
  author: Indigo Karasu (indigokarasu)
  version: 4.1.0
  hermes:
    category: research
    tags:
    - OSINT
    - research
    - people
    - companies
    - investigation
    - OCAS-core
tags:
- OSINT
- research
- people
- companies
- investigation
triggers:
- osint research
- people research
- company research
- entity resolution
- provenance brief
---
## Interactive Menu

When invoked interactively, present a two-level menu. See `references/interactive-menu.md` for the full menu structure.

## When to Use

- OSINT research on people, companies, or topics
- Structured investigation with source tracking
- Due diligence and background research
- Competitive intelligence gathering
- When Sift needs deeper targeted research
## When NOT to Use

- General topic research (use Sift)
- Image processing (use Look)
- Knowledge graph writes (use Elephas)
- Social graph management (use Weave)

# Scout

Scout conducts lawful OSINT research on people, companies, and organizations, assembling provenance-backed briefs where every claim carries a source reference, retrieval timestamp, and direct quote. It works through a tiered source waterfall — public web first, then rate-limited registries, then paid databases only with explicit permission — collecting no more than the stated research goal requires. This tiered approach exists because paid sources require explicit consent and rate-limited registries need careful quota management to avoid service degradation.

Scout integrates curated person-specific OSINT tools (theHarvester, Maigret, Holehe, h8mail, PhoneInfoga, and others), a public-records investigation framework (SEC EDGAR, USAspending, Senate lobbying, OFAC sanctions, ICIJ offshore leaks, NYC property records, OpenCorporates, CourtListener, Wayback Machine, Wikipedia/Wikidata, GDELT), and dynamically discovers new MCP-wrapped OSINT servers at runtime.

## Responsibility boundary

Scout owns lawful OSINT research on people and organizations with provenance-backed output.

Scout does not own: general topic research (Sift), image processing (Look), knowledge graph writes (Elephas), social graph (Weave), communications (Dispatch).

## Ontology types

Scout works with these types from `spec-ocas-ontology.md`:

- **Entity/Person** — people and their public profiles. The primary entity type Scout extracts.
- **Entity/AI** — AI agents or organizations when relevant to research.
- **Thing/DigitalArtifact** — public documents, profiles, and digital records found during research.

Scout emits Signals to Elephas after each completed research request, for each extracted entity with confidence >= med. Signal `payload.type` is `"Person"` or `"AI"`. `source_journal_type` is `"Research"`. Every emitted Signal must include a `user_relevance` field.

### user_relevance field

Every Signal emitted by Scout carries a `user_relevance` field:

- `"user"` — the signal is relevant to the user's personal knowledge graph
- `"agent_only"` — agent-initiated research with no demonstrated user connection

**Default is `"agent_only"`**. A signal receives `user_relevance: "user"` only when: (1) the user explicitly requested the research, OR (2) the entity connects to a `user_relevance: "user"` Chronicle entry. When in doubt, default to `"agent_only"`.

Signal example:
```json
{
  "signal_id": "sig-scout-20260402-001",
  "source_skill": "ocas-scout",
  "source_journal_type": "Research",
  "emitted_at": "2026-04-02T14:30:00Z",
  "user_relevance": "agent_only",
  "payload": {
    "type": "Person",
    "name": "Jane Doe",
    "confidence": "high",
    "source_refs": ["https://example.com/profile"]
  }
}
```

## Commands

- `scout.research.start` — begin a new research request with subject and goal
- `scout.research.expand --tier <1|2|3>` — escalate to a higher source tier
- `scout.brief.render` — generate the final markdown brief with findings and sources
- `scout.brief.render_pdf` — optional PDF brief generation
- `scout.status` — return current research state
- `scout.journal` — write journal for the current run; called at end of every run
- `scout.update` — pull latest from GitHub source; preserves journals and data
- `scout.sources.discover` — discover new MCP servers relevant to current research
- `scout.sources.refresh` — refresh curated source lists from GitHub
- `scout.sources.status` — show state of dynamic source discovery

## Invariants

1. Legality-first — only publicly available sources without bypassing access controls
2. Minimization — collect only what the research goal requires
3. Provenance for every claim — at least one source reference with URL, retrieval timestamp, and quote
4. Paid sources require explicit permission — Tier 3 needs a recorded PermissionGrant
5. No doxxing by default — private details suppressed unless explicitly permitted
6. Uncertainty must be surfaced — incomplete identity resolution stated clearly
7. Identity gate — a profile is `verified` only when 2+ seed data points overlap (name + location, etc.). Username match alone = `unverified_lead`; exclude from synthesis
8. Tiered verification — Sherlock results: top 3 verified immediately, 2-3 sampled, remainder only on explicit request
9. Recursion cap — recursive handle discovery allowed for 1 additional pass; hard cap at 2 Sherlock passes per request
10. Person-first tooling — always run theHarvester and OpenSanctions for person research. Run Holehe, h8mail, PhoneInfoga, Ghunt when relevant input data is available.

## Input contract

ResearchRequest requires: request_id, as_of, subject (type, name, aliases, known_locations, known_handles, known_emails, known_phones), goal, constraints (time_budget_minutes, minimize_pii). Read `references/scout_schemas.md` for exact schema.

## Research workflow

Full step-by-step workflow with tool commands, handle expansion logic, identity gating, and verification tiers is in `references/scout_schemas.md`.

**Phase summary:**

- [ ] **Normalize** — parse request, validate subject identity inputs
- [ ] **Tier 1 collection** — run person-specific tools (theHarvester, OpenSanctions) and public web search in parallel
- [ ] **Handle expansion** — extract handles, run Sherlock/Maigret, apply identity gate (inv 7), tiered verification (inv 8), recursion cap at 2 passes (inv 9)
- [ ] **Email/phone tools** — run Holehe, h8mail, EmailRep, Ghunt (if Gmail), PhoneInfoga as data is available
- [ ] **Public records investigation** — for company/org research or when person research reveals corporate ties, run public-records fetch scripts (SEC EDGAR, USAspending, Senate lobbying, OFAC sanctions, ICIJ offshore leaks, OpenCorporates, CourtListener, NYC ACRIS, Wayback Machine, Wikipedia/Wikidata, GDELT). See `references/scout_public_records.md` for source selection, execution order, and cross-reference keys.
- [ ] **Entity resolution across sources** — normalize names, run `entity_resolution.py` to cross-link entities between public-records CSVs and person-tool findings. Three match tiers: exact (high), fuzzy (medium), token_overlap (low).
- [ ] **Timing correlation (optional)** — run `timing_analysis.py` to test whether event time series (e.g., lobbying filings vs contract awards) cluster suspiciously. Permutation test, one-tailed p-value.
- [ ] **Dynamic MCP discovery** — if Tier 1 + public records results are thin, discover and connect to MCP-wrapped OSINT servers
- [ ] **Compile** — record provenance, assign confidence, escalate to Tier 2/3 only as permitted
- [ ] **Brief** — render markdown brief (see Output requirements). Near-match profiles surfaced explicitly, not discarded.
- [ ] **Emit & journal** — store findings, emit Signal files per confirmed entity (with `user_relevance`), write journal via `scout.journal`

When `minimize_pii=true`, suppress unnecessary sensitive details in the final brief.

## Source waterfall

Read `references/scout_source_waterfall.md` for full tier logic.

- **Tier 1 — Person-specific tools** — theHarvester, OpenSanctions, Sherlock, Maigret, Holehe, h8mail, EmailRep, Ghunt, PhoneInfoga. See `references/scout_person_sources.md` for full list and execution order.
- **Web + platform search** — public web via SearchX (local SearXNG), including Twitter/X, Reddit, LinkedIn, GitHub. Always runs.
- **Tier 1.5 — Public records** — SEC EDGAR, USAspending, Senate lobbying (LD-1/LD-2), OFAC SDN sanctions, ICIJ offshore leaks, NYC property records (ACRIS), OpenCorporates, CourtListener, Wayback Machine, Wikipedia/Wikidata, GDELT. Python stdlib-only fetch scripts. Runs for company/org research or when person research reveals corporate ties. See `references/scout_public_records.md`.
- **Tier 2** — rate-limited sources, registries, MCP-discovered servers. Only if enabled and useful.
- **Tier 3** — paid OSINT providers, background databases. Requires explicit permission grant.

## Output requirements

Markdown brief: Executive Summary, Identity Resolution Notes, Findings, Social Graph (if handles found), Digital Footprint (if email/phone tools ran), Public Records (if public-records investigation ran), Risk and Uncertainty, Source Log. Every finding carries source-backed provenance.

- **Social Graph**: verified profiles (platform, URL, discovery method, verification evidence) + unverified leads separately. Omit if no handles found.
- **Digital Footprint**: email accounts (Holehe), breaches (h8mail/HIBP), Google data (Ghunt), phone metadata (PhoneInfoga), email risk (EmailRep), dark web (OnionClaw). Omit if no data available.
- **Public Records**: corporate filings (SEC EDGAR), government contracts (USAspending), lobbying disclosures (Senate LD-1/LD-2), sanctions (OFAC SDN), offshore leaks (ICIJ), property records (NYC ACRIS), corporate registry (OpenCorporates), court records (CourtListener), web archives (Wayback), knowledge base (Wikipedia/Wikidata), news monitoring (GDELT). Omit if no public-records investigation was run.

Read `references/scout_brief_template.md` for the full template.

## Inter-skill interfaces

Scout writes Signal files to Elephas (via journal signal payload). One Signal per confirmed entity or high-confidence relationship. Use schema from `spec-ocas-shared-schemas.md`. Every Signal must include `user_relevance`. See `spec-ocas-interfaces.md` for signal format.

## Recovery Behavior

This section defines error handling and recovery procedures for all scout jobs.

Implements the recovery contract from `spec-ocas-recovery.md`.

- **Evidence**: Every run writes to `{agent_root}/commons/data/ocas-scout/evidence.jsonl` (including no-op runs; `not_activity_reason` mandatory when no side effects).
- **Gap detection**: On wake, checks evidence log. If gap exceeds cadence (24h update, 7d research), logs `gap_detected`.
- **Degraded mode**: When tools unavailable, logs `degraded: <tool>` and continues with available sources.
- **Log compaction**: Logs older than 30 days (no-op) or 90 days (error/gap) compacted. Last 7 days retained.

## Storage layout

See `references/storage-layout.md` for directory structure. Read `references/scout_config.md` for default config.json and field descriptions.

## OKRs

See `references/okrs.md` for skill OKR definitions.

## Optional skill cooperation

- **Sherlock** — username-to-platform expansion during handle expansion. Falls back to `sift.search("site:<platform> '<handle>'")` if unavailable.
- **Sift** — web search during Tier 1; Sift-dork fallback when Sherlock unavailable
- **Look** — reverse image search for person identification when photo available
- **Weave** — read social graph for identity context before research (read-only)
- **Elephas** — emit Signal files for Chronicle promotion
- **native-mcp / mcporter** — connect to dynamically discovered MCP-wrapped OSINT servers
- **RapidAPI** — structured social media enrichment via `rapidapi_call` (see RapidAPI Enrichment Workflow below)

---
## RapidAPI Enrichment Workflow

During Phase 3 (Handle Expansion) and Phase 4 (Email/Phone Tools), use RapidAPI social media endpoints to enrich profiles with structured data that free tools (Sherlock/Maigret) can't provide. Full procedure including person/company enrichment pipelines, rate limiting, and tier integration: see `references/rapidapi-enrichment-workflow.md`.

## Journal outputs

- Observation Journal — research runs producing findings
- Research Journal — structured multi-source research sessions

Journals must include an `entities_observed` array (name, type, confidence, user_relevance). See `references/journal.md` for schema.

## Visibility

public

## Initialization

On first invocation, run `scout.init`: create data dirs + default config, create empty JSONL files, create journal dir, register cron jobs, log DecisionRecord, set up SearchX (SearXNG + nginx), verify person-specific tools (install missing via pip), check dark web tools (OnionClaw + Tor, non-blocking).

## Background tasks

| Job | Schedule | Command |
|---|---|---|
| `scout:update` | `0 0 * * *` (midnight daily) | `scout.update` |
| `scout:research` | `0 9 * * 1` (Monday 9am) | `scout.research` |
| `scout:sources-refresh` | `0 6 * * 0` (Sunday 6am) | `scout.sources.refresh` |

## Self-update

`scout.update` pulls the latest package from the `source:` URL in this file's frontmatter. Runs silently — no output unless the version changed or an error occurred.

Read `references/self_update.md` for the full self-update procedure.

## External Catalog Review

Monitors: [awesome-osint-mcp-servers](https://github.com/soxoj/awesome-osint-mcp-servers) (weekly), [awesome-osint](https://github.com/jivoi/awesome-osint) (monthly), [API-s-for-OSINT](https://github.com/cipher387/API-s-for-OSINT) (monthly). New tools classified by tier → added to `references/scout_person_sources.md`. See `references/scout_mcp_discovery.md` for dynamic discovery. See `references/sources-refresh.md` for the concrete refresh procedure that runs on the `scout:sources-refresh` cron.

## Gotchas

- **Tier 3 sources require explicit permission** — Paid OSINT providers and background databases (Tier 3) cannot be queried without a recorded PermissionGrant. The skill will silently skip Tier 3 even if credentials are configured.
- **User relevance defaults to `agent_only`** — Signals emitted to Elephas default to `user_relevance: "agent_only"` unless the user explicitly requested the research or the entity connects to a known `user` Chronicle entry. This means most Scout entities won't be promoted.
- **Hard cap at 2 Sherlock passes** — Recursive handle discovery is allowed for exactly 1 additional pass (2 total). Further recursion is silently blocked regardless of leads found.
- **Identity gate requires 2+ data points** — A username match alone produces only `unverified_lead` status. Profiles are `verified` only when 2+ seed data points overlap (name + location, etc.).
- **minimize_pii suppresses home addresses and personal details** — When the user sets `minimize_pii=true`, the final brief suppresses unnecessary sensitive details even if they were found during research. Re-run without the flag to see full data.
- **"Not subscribed" ≠ broken on RapidAPI.** Many APIs return tools on `tools/list` but "You are not subscribed to this API" on actual calls. These are tier-gated by the provider, not broken. 3 genuinely broken LinkedIn APIs (linkedin-data-api, linkedin-api8, li-data-scraper) — provider shut down. 4 new ones work: fresh-linkedin-scraper-api (primary), linkedinscraper, linkedin-email-finder5, linkedin-lead-enrichment.
- **`gh api` base64 content is unreliable for counting** — `gh api repos/<owner>/<repo>/readme --jq '.content' | base64 -d` can silently return truncated or empty results. For fetching raw GitHub README content, use `curl -s "https://raw.githubusercontent.com/<owner>/<repo>/<branch>/README.md"` instead. This returns clean text that `wc -l` and `grep` can process directly.
- **Branch names vary across repos** — `jivoi/awesome-osint` uses `master` (not `main`). Always verify branch name with a quick `curl -s -o /dev/null -w "%{http_code}"` probe before fetching content.
- **curl timeout for unreliable endpoints** — Some GitHub endpoints return 0 bytes under rate-limiting. Use `--max-time 15` and check HTTP status code before processing output.
- **Public-records scripts use stdlib only** — All fetch scripts in `scripts/fetch_*.py` use Python stdlib only (no pip installs required). They use `urllib.request` with retry logic and respect `Retry-After` headers. 429 responses surface immediately with the upstream's quota message.
- **Entity resolution is token-bag only** — `entity_resolution.py` does NOT use external fuzzy libraries (no rapidfuzz, no jellyfish). Token-bag matching is the upper bound. For Levenshtein, transliteration, or phonetic matching, pip-install separately.
- **ICIJ offshore leaks cache** — First run downloads ~70 MB bulk CSV. Cached for 30 days under `$HERMES_OSINT_CACHE/icij/` (default: `~/.cache/hermes-osint/icij/`). Subsequent runs search the local cache.
- **Statistical significance ≠ wrongdoing** — `timing_analysis.py` p < 0.05 means the timing pattern is unlikely under the null. It does not establish corruption. Always state this in the brief.

## Support File Map

| File | When to read |
|---|---|
| `references/scout_schemas.md` | Before requests/findings/briefs; full workflow steps |
| `references/scout_config.md` | Default config.json and field descriptions |
| `references/scout_source_waterfall.md` | Before tier selection or escalation |
| `references/scout_brief_template.md` | Before rendering briefs |
| `references/scout_person_sources.md` | At start of every person research run |
| `references/scout_public_records.md` | At start of every company/org research run; when person research reveals corporate ties; before Phase 5 |
| `references/scout_mcp_discovery.md` | Before `scout.sources.discover`; before Tier 2 escalation |
| `references/sources-refresh.md` | Before `scout.sources.refresh`; before weekly cron refresh runs |
| `references/rapidapi-osint-params.md` | Before RapidAPI enrichment; param patterns per platform |
| `references/rapidapi-enrichment-workflow.md` | During Phase 3/4 research; RapidAPI person/company enrichment pipelines |
| `references/journal.md` | Before scout.journal; at end of every run |
| `references/self_update.md` | Before running `scout.update`; when debugging self-update failures |

## Update command

This skill self-updates every 24 hours via:

```bash
scout.update
```

This pulls the latest version from GitHub and restarts the skill's background tasks if applicable.
