---
name: ocas-reach
license: MIT
description: 'Live world-data query engine. Queries real-time external APIs for factual ground truth — no synthesis, no opinion, no research. Routes requests through a registry of ~55 registered sources covering US government data, scholarly literature, weather and hazards, geocoding, finance and macro indicators, court records, nutrition, news events, property records, land due-diligence, academic papers, satellite imagery, and product manuals (3M+). Do not use for web research (use Sift), entity investigations (use Scout), or pattern analysis over historical signals.'
source: https://github.com/<agent-handle>/reach
includes:
- references/**
- scripts/**
metadata:
  author: Indigo Karasu (indigokarasu)
  version: "3.12.0"
  hermes:
    category: data-science
    tags:
    - live-data
    - api
    - real-time
    - facts
    - OCAS-core
tags:
- live-data
- API
- real-time
- facts
- research
triggers:
- live data query
- real-time API
- fact check
- current data
- external API query
---

# ocas-reach: Live World-Data Query Engine

Reach is the system's **sensory layer** for verified ground truth. It answers "what *is*" — not "what was," not "what should be," not "what might be." Each registered source is a deterministic connector: structured query in, structured response with citation out. No synthesis. No interpretation. Reach returns the fact; downstream skills synthesize.

## When to Use

- The user asks about real-time external data with a known authoritative source (USGS, NOAA, FDA, FRED, Congress, Redfin, Open-Meteo, NASA, Wikidata, etc.)
- The user wants a factual lookup ("what's the current GDP figure," "any recent FDA recalls of <X>," "is 123 Main St for sale," "papers about transformers since 2022")
- The agent needs a citation-bearing fact to ground a downstream response
- The request is a specific entity, measurement, or list, not an open-ended exploration

For example, when the user asks "any recent FDA recalls of peanut butter," Reach queries the FDA API and returns the verbatim recall list with citations.

## When NOT to Use

- Open-ended research over many sources → use Sift
- Investigating a person → use Scout
- Detecting patterns in historical signals — query Chronicle directly
- Requests requiring summarization or synthesis (Reach returns the fact; the agent or another skill does the writing)

## Responsibility Boundary

Reach owns: real-time external API calls, source-specific connector logic, source registry, query/response logging, monthly quota tracking, account ledger.

Reach does not own:
- Web research over open content (Sift)
- Person investigations (Scout)
- Knowledge graph queries
- Pattern analysis over journals
- Long-form synthesis or briefing (Vesper)
- Inbox / messaging (Dispatch)

A query that needs synthesis after fetching is a two-step request: Reach returns the fact, the agent or downstream skill synthesizes.

## Optional Skill Cooperation

When present:
- **Vesper** may include Reach lookups in morning briefings (overnight USGS earthquake summary, weather, FRED indicator deltas).
- **Sift** may invoke Reach as one of many sources during deep research.
- **Scout** may invoke Reach for property records and SEC filings during contact enrichment.
- **Custodian** may verify a Reach quota state when triaging API rate-limit issues.

Reach functions normally when none of these are present.

## Source Registry

The authoritative source list lives in `scripts/sources.yml` (54 sources). Browsable index: `references/sources/index.md`. See `references/credential-files.md` for credential storage, `references/account_provisioning.md` for account registration.

## Account Creation

Reach is explicitly authorized to register accounts at sources requiring them. See `references/account_provisioning.md` for the registration playbook. Not authorized to: pay for tiers, use different identity, accept arbitration waivers, register outside `sources.yml`.

## Decision Model

8-step query pipeline: identify source → validate auth → check quota → build query → execute → log usage → write journal → return verbatim. No silent fall-through to alternative sources.

## Execution

CLI via `python3 scripts/reach.py`. See `references/sources/index.md` for command reference and `references/usage_tracking.md` for quota management.

## Adding a New Source

See `references/source-evaluation-framework.md` for the evaluation checklist and `references/sources/_template.md` for the source reference template.

## Legacy Sources

`katzilla` and `property_lookup` predate the v3 registry. References: `references/katzilla.md`, `references/property_lookup.md`.

## Methodology Notes

**Reach/Sift boundary (Jun 12, 2026)** — Reach owns: sources.yml, API connectors, MCP connections, quota tracking (CSAPI + all Reach-registered APIs), discovered APIs catalog (`references/discovered-apis.md`). Sift owns: research synthesis, web_search, entity extraction. NEVER manages own MCP/quota. Sift delegates to Reach for factual anchors via `reach.csapi_check/increment` and `reach.query rapidapi`.

**RapidAPI is general-purpose marketplace (Jun 12, 2026)** — 203 endpoints (finance, crypto, news, geo, weather, security, social, travel). NOT "local business search." Route via `reach.query rapidapi`. When one skill uses a narrow slice of a tool, don't let that define the tool for all skills. Always check canonical source/definition of a multi-skill shared tool.

**ExchangeRate source doc is STALE (2026-07-24)** — `sources.yml` declares `exchangerate:` with `auth: none`, but `https://api.exchangerate.host` now returns `code 101 missing_access_key` (requires `access_key`). Treat as effectively key-required until the source doc is updated to declare an `env_var`. Always live-verify a source's auth requirement rather than trusting the registry.

## Support File Map

| File | When to read |
|------|-------------|
| `references/sources/index.md` | Before picking which source to use for a query; when checking routing hints |
| `references/sources/<slug>.md` | Before building a query for a specific source; when you need actions, params, response shape, or pitfalls |
| `references/credential-files.md` | Credential storage, env_var names, **which `.env` the active profile actually loads** |
| `references/credential-files.md` | When auditing whether a source is accessible — start here; misplaced keys (global root vs active profile) are the #1 cause of "key not found" |
| `references/usage_tracking.md` | When checking quota status or usage counts; when debugging rate-limit issues |
| `references/source-evaluation-framework.md` | Before adding a new source to the registry; when evaluating candidate APIs |
| `references/storage-layout.md` | When inspecting or configuring the on-disk data and journal directories |
| `references/okrs.md` | When reviewing OKR definitions or scoring skill performance |
| `references/api-mine-cron-notes.md` | When debugging api-mine cron behavior; when "0 new APIs" result needs interpretation |

## Recovery Behavior

This skill implements the recovery contract from `spec-ocas-recovery.md`.

- **Evidence**: Every query run writes an evidence record to `{agent_root}/commons/data/ocas-reach/evidence.jsonl`, including no-op runs. The `not_activity_reason` field is mandatory when no side effects occur.
- **Gap detection**: On every wake, checks the evidence log. If gap exceeds 24h for update cron, logs `gap_detected`.
- **Degraded mode**: When external APIs are unavailable, logs `degraded: <api>` and returns partial results with error envelope.
- **Log compaction**: Evidence and usage logs older than 30 days compacted. Last 7 days retained.

## Storage Layout

See `references/storage-layout.md` for the full directory structure.

## Journal Outputs

Every `reach.query` run emits an **Observation Journal**. Account-registration runs (when Reach signs up at a new source) emit an **Action Journal** because side effects are involved (form submission, key storage).

Journal payload includes: `source`, `action`, `params`, `outcome` (`success` / `auth_missing` / `source_error` / `parse_error` / `quota_blocked`), and `result_meta` (extracted `meta` / `citation` / `quality` / `http_status` from the response — not the bulk payload).

## Background tasks

| Job | Mechanism | Schedule | Command |
|---|---|---|---|
| `reach:update` | cron | `0 0 * * *` | Self-update from GitHub source |
| `reach:api-mine` | cron | `0 4 * * *` | Scan sessions for sites with APIs → `references/discovered-apis.md` |

## Source Discovery (reach:api-mine)

The `reach:api-mine` cron job scans **all** session transcripts (not just research) for sites, services, databases, and archives that are used or needed by any skill. For each site found, it evaluates:

- [ ] **Does it have an API?** — Check for programmatic access (REST, GraphQL, etc.)
- [ ] **Can I access it?** — Free/freemium/paid? API key required? Account signup possible?
- [ ] **What data does it provide?** — What endpoints exist? What can you search/retrieve?
- [ ] **Does it belong as a preferred source?** — Is the API meaningfully better than the current access method (web scraping, SearXNG, browser) for the skill that found it?

A site is only cataloged if it has a **confirmed working API**, the data is useful to an active skill/workflow, and the API is better than the current approach. Deduplicate against both `sources.yml` and `references/discovered-apis.md`.

Catalog: `references/discovered-apis.md` — fully evaluated candidates ready for integration into `sources.yml`.

**Key principle:** Not a general search index. Only sites that specific skills already use or need, where an API would reduce friction vs. the current method.

`reach.init` registers `reach:update` on first invocation. No operational background tasks beyond self-update — Reach is purely reactive to user/agent queries.

**Session-retention limitation (Jun 18, 2026)** — The session database (via `session_search`) only retains recent sessions (typically 48-72h of FTS5-indexed content). Older research sessions — even those with significant API discoveries — become unsearchable once they age out. This means:
- The api-mine cron can only discover APIs from sessions that are still in the active session store
- If a session produced API discoveries but was compacted/aged out before the cron ran, those discoveries are lost
- **Mitigation**: When a session produces an API discovery, immediately write it to `references/discovered-apis.md` (don't rely on the cron to catch it later)
- A "0 new APIs" result from the cron is NORMAL and expected when sessions are current — it means the catalog is up-to-date, not that the cron is broken
- **Cron-skew (Jun 27, 2026)**: During periods when the agent runs primarily as cron jobs, there may be zero interactive sessions to mine. `[SILENT]` is correct — see `references/api-mine-cron-notes.md` § Cron-Skew.

## Self-Update

See `references/self-update-reach.md`.

## Validation rules

A query is valid when:
- `source` is registered in `sources.yml`
- The action is supported by the source
- Required env var is present (or `auth: optional`)
- The daily/monthly quota has remaining budget

Otherwise return an explicit error envelope and write the failure to `usage.jsonl` with the appropriate status. **Do not fall through to a different source silently** — the operator will not know which source actually answered.

## Gotchas

See `references/gotchas.md` for all operational pitfalls including quota exhaustion, User-Agent requirements, demo mode, rate-limit handling, account creation, non-commercial sources, and silent fall-through prevention.

## Ontology types

Reach does not extract entities or emit Signals to Chronicle. It is a query passthrough — entity extraction from returned data is the responsibility of the calling skill.

## OKRs

See `references/okrs.md`.

## Visibility

public
