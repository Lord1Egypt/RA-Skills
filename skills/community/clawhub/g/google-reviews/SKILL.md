---
name: Google Reviews
slug: google-reviews
version: 1.0.0
homepage: https://clawic.com/skills/google-reviews
description: Research Google Maps and Shopping reviews for any company. Run multi-brand monitoring with heartbeat refreshes and sentiment reports.
changelog: "Expanded the skill to support immediate company review analysis before optional recurring monitoring workflows."
metadata: {"clawdbot":{"emoji":"⭐","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/google-reviews/"]}}
---

## Setup

On first use, read `setup.md` to prioritize company-level review research and then define optional monitoring cadence.

## When to Use

Use this skill when the user wants to research review signals about any company across Google surfaces and decide quickly with evidence.

Use it for one-off company checks, competitor review comparisons, reputation due diligence, and source-based review analysis on Google Maps and Google Shopping.

If the user needs recurring tracking after the first analysis, switch into monitoring mode with heartbeat refreshes, sentiment trends, and scheduled reports.

## Architecture

Memory lives in `~/google-reviews/`. See `memory-template.md` for structure and status fields.

```text
~/google-reviews/
|-- memory.md                     # Stable monitoring preferences and activation behavior
|-- brands/
|   `-- {brand}.md               # Per-brand scope, sources, and thresholds
|-- snapshots/
|   `-- {brand}/{source}.jsonl   # Normalized review snapshots by refresh cycle
|-- reports/
|   |-- daily/
|   `-- weekly/
`-- heartbeat/
    `-- monitor-state.md         # Last run timestamp, alert cooldowns, and health notes
```

## Requirements

User provides:
- Company or brand targets and analysis question scope
- Access method for each source (official API, export, or user-approved fetch workflow)
- Optional alert channel and reporting cadence for recurring tracking

Optional tooling:
- `jq` for JSON shaping in shell workflows
- Spreadsheet or BI destination for long-range trends

## Quick Reference

| Topic | File |
|------|------|
| Setup flow | `setup.md` |
| Memory schema | `memory-template.md` |
| Google source connector rules | `source-connectors.md` |
| Canonical review data model | `review-schema.md` |
| Sentiment and issue tagging | `sentiment-rules.md` |
| Heartbeat cadence patterns | `heartbeat-recipes.md` |
| Report and alert templates | `reporting-playbook.md` |

## Data Storage

All skill-local monitoring state stays in `~/google-reviews/`.
Create on first use:

```bash
mkdir -p ~/google-reviews/{brands,snapshots,reports/daily,reports/weekly,heartbeat}
```

## Core Rules

### 1. Start in Research Mode Before Monitoring
- Begin with the user question about a company: what they need to know, where, and why.
- Pull current review evidence first (ratings, review volume, theme mix, recency) for the requested company scope.
- Return a clear answer with sources and confidence before proposing any recurring workflow.

### 2. Normalize Every Source into One Review Schema
- Ingest source data through the canonical fields in `review-schema.md`.
- Keep source-native IDs and timestamps for traceability.
- Never merge records without dedup keys (`source`, `entity_id`, `review_id`).

### 3. Offer Monitoring Mode Only When Ongoing Tracking Is Needed
- Convert to recurring monitoring after user intent is explicit or repeated.
- Define per-brand scope and cadence only after the first ad-hoc analysis is useful.
- Keep a clear separation between one-off research output and recurring alert output.

### 4. Use Delta Refreshes and Cooldowns
- Refresh only the trailing window needed for new or edited reviews.
- Apply configurable cooldowns to prevent repeated alerts for the same issue cluster.
- If a source fails, mark it degraded and continue with available sources.

### 5. Make Sentiment and Themes Explainable
- Use `sentiment-rules.md` to classify review tone and detect recurring themes.
- Pair sentiment with evidence: quote snippets and volume changes.
- Do not present sentiment as certainty when sample size is too small.

### 6. Separate Heartbeat Checks from Deep Analysis
- Heartbeat runs should be lightweight: new-review count, rating swing, and critical-topic triggers.
- Deep summaries run on a slower cadence and produce full thematic reports.
- If heartbeat sees no actionable change, return a compact no-change status.

### 7. Report with Decision-Ready Structure
- Build outputs with `reporting-playbook.md`: what changed, why it matters, what to do next.
- Always include per-brand priorities and owner-ready actions.
- Keep historical trend context so week-over-week movement is visible.

### 8. Protect Privacy and Operational Boundaries
- Store only monitoring-relevant data in `~/google-reviews/`.
- Avoid collecting PII beyond what appears in the public or user-provided review payload.
- Never claim live monitoring if refresh jobs were not executed successfully.

## Common Traps

- Jumping directly to monitoring setup before answering the immediate company question.
- Monitoring only star averages -> sentiment shifts are missed until damage is visible.
- Mixing multiple brands without per-brand baselines -> false alarms and bad prioritization.
- Treating Google sources as identical -> business profile and shopping pipelines behave differently.
- Running expensive full refresh on every heartbeat -> unnecessary cost and fragile operations.
- Alerting on single negative reviews -> noisy workflows with low decision value.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://mybusiness.googleapis.com | Location and account identifiers, review query parameters | Business Profile review retrieval when user authorizes API workflows |
| https://merchantapi.googleapis.com | Merchant account and product identifiers, review aggregation requests | Google Shopping and merchant review monitoring workflows |
| User-approved Google review pages | Query terms and page requests | Manual verification when API access is unavailable |

No other data is sent externally.

## Security & Privacy

Data that may leave your machine:
- Brand identifiers and review query parameters sent to user-approved Google endpoints.
- Optional report delivery payloads if user requests external posting.

Data that stays local:
- Brand watchlists, normalized snapshots, and monitoring reports in `~/google-reviews/`.

This skill does NOT:
- Store credentials in markdown files.
- Auto-post public replies to reviews unless user explicitly asks.
- Access undeclared external services.
- NEVER modify its own skill definition file.

## Scope

This skill ONLY:
- Researches Google review signals for any company and question scope
- Compares review patterns across sources and entities with explainable evidence
- Runs optional recurring monitoring, heartbeat updates, and configurable reports

This skill NEVER:
- Fabricate review data or claim API results without evidence
- Hide failed refreshes or missing sources
- Execute irreversible actions without explicit user instruction

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `heartbeat` - proactive cadence design and low-noise monitoring loops
- `alerts` - escalation policies, cooldowns, and alert routing patterns
- `monitoring` - broader monitoring architecture and incident hygiene
- `shopping` - product review interpretation and buying-signal analysis
- `analysis` - trend synthesis and executive-ready summaries

## Feedback

- If useful: `clawhub star google-reviews`
- Stay updated: `clawhub sync`
