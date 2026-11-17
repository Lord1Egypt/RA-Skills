# Scoring Rubric

How to rank discovered resources. Each result is scored on four axes, weighted and summed to a 0.0-1.0 composite score.

## Axes

### Relevance (weight: 0.40)

Does this resource solve the stated need?

| Score | Criteria |
|-------|----------|
| 1.0 | Exact match: resource description directly addresses the capability need |
| 0.7 | Strong match: covers the core need, may include extra scope |
| 0.4 | Partial match: handles a related capability that could be adapted |
| 0.1 | Tangential: shares keywords but serves a different purpose |
| 0.0 | Irrelevant |

Relevance is the primary filter. A resource scoring below 0.4 on relevance is discarded regardless of other scores.

### Trust (weight: 0.25)

How safe and reliable is this resource?

| Score | Criteria |
|-------|----------|
| 1.0 | Official/verified: maintained by the protocol org, a major company, or passes all security scans |
| 0.8 | Well-established: 500+ stars, active maintenance, permissive license, clean security scan |
| 0.6 | Community-trusted: 50+ stars, recent updates, no security flags |
| 0.4 | New or lightly used: <50 stars, limited history, but no red flags |
| 0.2 | Unvetted: no stars, no scan data, unknown author |
| 0.0 | Flagged: security scan flagged as suspicious or malicious |

**Hard disqualify at 0.0.** Never recommend a resource with a malicious security flag.
**Warn at 0.2.** If included, prominently flag as unvetted.

### Cost (weight: 0.20)

What does it cost to use?

| Score | Criteria |
|-------|----------|
| 1.0 | Completely free: no API key, no signup, no rate limits that matter |
| 0.8 | Free with key: requires a free API key but no payment |
| 0.6 | Generous free tier: free tier covers typical personal use |
| 0.4 | Limited free tier: free tier exists but is restrictive |
| 0.2 | Freemium: meaningful features behind paywall |
| 0.0 | Paid only: no free option |

When `--free-only` is set (default), discard results scoring below 0.6 on cost.

### Effort (weight: 0.15)

How much work to start using it?

| Score | Criteria |
|-------|----------|
| 1.0 | Drop-in: install/connect and use immediately (e.g., `npx clawhub install`, add MCP URL) |
| 0.7 | Config required: needs env vars, API keys, or minor setup |
| 0.4 | Build required: needs wrapper code, custom integration, or significant configuration |
| 0.2 | Major effort: requires infrastructure, database setup, or complex auth flows |
| 0.0 | Impractical: would take more effort than building from scratch |

## Composite score

```
score = (relevance * 0.40) + (trust * 0.25) + (cost * 0.20) + (effort * 0.15)
```

## Discard threshold

Discard any result with composite score below 0.3.

## Presentation order

Within each surface, sort by composite score descending. Across surfaces, present in surface priority order (MCP > ClawHub > GitHub > APIs) but let the per-surface ranking speak for itself.

## Tie-breaking

When two results have the same composite score:
1. Prefer higher trust
2. Prefer lower cost
3. Prefer lower effort

## Example scoring

**Query:** "calendar event management"

| Resource | Relevance | Trust | Cost | Effort | Composite |
|----------|-----------|-------|------|--------|-----------|
| Google Calendar MCP (official) | 1.0 | 1.0 | 0.8 | 1.0 | 0.96 |
| ical-parser skill (ClawHub, 200 stars) | 0.7 | 0.6 | 1.0 | 1.0 | 0.76 |
| CalDAV API wrapper (GitHub, 30 stars) | 0.7 | 0.4 | 1.0 | 0.4 | 0.64 |
| Calendly API (official) | 0.4 | 0.8 | 0.4 | 0.7 | 0.50 |

Recommendation: Google Calendar MCP is the clear winner -- official, free, drop-in.

## Known high-quality resources

Check these first for common capability gaps before running a full search:

| Category | Resource | Type | Notes |
|----------|----------|------|-------|
| MCP bridge | steipete/mcporter | skill | Official MCP CLI, 51k downloads |
| API reference | ivangdavila/api | skill | 147 services: auth, endpoints, rate limits, gotchas |
| Browser automation | TheSethRose/agent-browser | skill | Headless browser with a11y tree |
| GitHub | steipete/github | skill | PR, CI, issues via gh CLI |
| Database | gitgoodordietrying/sql-toolkit | skill | SQLite, Postgres, MySQL |
| Google Calendar | official | MCP | google-calendar MCP server |

## Known zero-auth free APIs

These APIs require no signup and no API key. Use them directly via web_fetch when the capability matches:

| API | URL | Capability |
|-----|-----|------------|
| Open-Meteo | `https://api.open-meteo.com/v1/forecast?latitude=X&longitude=Y&current_weather=true` | Weather data |
| JSONPlaceholder | `https://jsonplaceholder.typicode.com/` | Test/mock REST data |
| Puter.js | `https://developer.puter.com/` | Free AI inference + image generation (client-side JS) |
| public-apis list | `https://api.publicapis.org/entries?category={cat}` | Meta-API: search 1400+ public APIs |
| IP geolocation | `https://ipapi.co/json/` | IP-based location |
| Exchange rates | `https://open.er-api.com/v6/latest/{base}` | Currency exchange rates |

## Red flags (disqualify or warn)

- Description says "no X" but SKILL.md uses X (e.g., "no curl" + curl fallback)
- References env vars not declared in requires metadata
- Cross-promotes other skills in SKILL.md body
- Instructs arbitrary shell execution without clear justification
- Uses `npx <package>@latest` to execute unvetted npm code at runtime
- ClawHub or VirusTotal scan flagged as suspicious

## Green flags (trust boosters)

- Instruction-only (no binary install)
- Clean VirusTotal + platform security scan
- Author has other well-rated skills (e.g., steipete, gitgoodordietrying)
- Active maintenance (commits within 3 months)
- Permissive license (MIT, MIT-0, Apache-2.0)
