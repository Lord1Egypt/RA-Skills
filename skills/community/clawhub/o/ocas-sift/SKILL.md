---
name: ocas-sift
source: https://github.com/indigokarasu/sift
install: openclaw skill install https://github.com/indigokarasu/sift
description: Use when searching the web, synthesizing research across multiple sources, verifying facts, summarizing documents, or extracting structured entities. The system's general research engine for topic research, web lookups, fact-checking, comparisons, and deep multi-source sessions. Trigger phrases: 'search for', 'look up', 'research this topic', 'fact check', 'compare', 'summarize this', 'what is', 'find information about', 'update sift'. Do not use for person-focused OSINT investigations (use Scout) or image processing (use Look).
metadata: {"openclaw":{"emoji":"🔬"}}
---

# Sift

Sift is the system's general research engine, retrieving and synthesizing information from the web across a tiered source hierarchy — internal knowledge first, then free web search, then rate-limited semantic research providers for deep work. It evaluates source reliability through cross-source agreement scoring, extracts structured entities from retrieved content, and emits enrichment candidates to Chronicle so researched knowledge accumulates over time.

## When to use

- Web search and research synthesis on any topic
- Fact verification across multiple sources with consensus scoring
- Document summarization and structured entity extraction
- Comparison research across products, technologies, or options
- Deep research sessions with multi-source threading

## When not to use

- OSINT investigations on individuals — use Scout
- Image-to-action processing — use Look
- Pattern analysis on the knowledge graph — use Corvus
- Communications and message drafting — use Dispatch

Sift never performs OSINT investigations on individuals. If the primary entity of a query is a person, Scout should be invoked.

## Responsibility boundary

Sift owns web research, fact verification, and structured entity extraction.

Sift does not own: person-focused OSINT (Scout), image processing (Look), knowledge graph writes (Elephas), pattern analysis (Corvus), social graph (Weave).

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

## Response modes

Sift classifies query depth automatically:

- **quick_answer** — simple factual lookups, single-source sufficient
- **comparison** — multi-source comparison with structured output
- **research** — deep multi-session investigation with threading
- **document_analysis** — URL or document-focused extraction

Users may override with phrases like "quick answer", "deep dive", "compare", or "summarize".

## Search tier selection

- **Tier 1 — Internal Knowledge**: LLM knowledge, conversation context, Chronicle if available.
- **Tier 2 — Free Web Search**: Brave Search API, SearXNG, DuckDuckGo. Default for all queries.
- **Tier 3 — Semantic Research**: Exa, Tavily. Deep research with sparse sources only. Quota-limited.

Read `references/search_tiers.md` for provider details and escalation criteria.

## Source reputation model

Sift maintains per-domain trust scores based on: cross-source agreement, contradiction frequency, historical accuracy, structured data quality, citation frequency.

## Structured extraction rules

When pages are retrieved, extract: entities (with type from shared ontology), claims, statistics, relationships, citations. Each extraction includes confidence level.

Extracted entities are emitted as enrichment candidates for Elephas.

## Run completion

After every Sift command that produces results:

1. Persist session, entities, sources, and decisions to local JSONL files
2. For each extracted entity or relationship with confidence >= `med`: write a Signal file to `~/openclaw/db/ocas-elephas/intake/{signal_id}.signal.json`. Use Signal schema from `spec-ocas-shared-schemas.md`.
3. Write journal via `sift.journal`

## Chronicle interaction

Sift never writes directly to Chronicle. It emits enrichment candidates via Signal files to `~/openclaw/db/ocas-elephas/intake/{signal_id}.signal.json`. Elephas decides promotion.

## Inter-skill interfaces

Sift writes Signal files to Elephas intake: `~/openclaw/db/ocas-elephas/intake/{signal_id}.signal.json`

Sift may read from Thread (when present) for recent browsing context to improve query rewriting. This is a cooperative read, not a dependency.

See `spec-ocas-interfaces.md` for signal format.

## Storage layout

```
~/openclaw/data/ocas-sift/
  config.json
  sessions.jsonl
  threads.jsonl
  entities.jsonl
  sources.jsonl
  decisions.jsonl
  reports/

~/openclaw/journals/ocas-sift/
  YYYY-MM-DD/
    {run_id}.json
```


Default config.json:
```json
{
  "skill_id": "ocas-sift",
  "skill_version": "2.3.0",
  "config_version": "1",
  "created_at": "",
  "updated_at": "",
  "search": {
    "default_tier": 2,
    "tier3_daily_limit": 50
  },
  "retention": {
    "days": 30,
    "max_records": 10000
  }
}
```

## OKRs

Universal OKRs from spec-ocas-journal.md apply to all runs.

```yaml
skill_okrs:
  - name: source_accuracy
    metric: fraction of extracted facts confirmed by cross-source agreement
    direction: maximize
    target: 0.85
    evaluation_window: 30_runs
  - name: tier3_quota_compliance
    metric: fraction of days where Tier 3 usage stays within daily limit
    direction: maximize
    target: 1.0
    evaluation_window: 30_runs
  - name: entity_extraction_precision
    metric: fraction of extracted entities with valid source reference
    direction: maximize
    target: 0.90
    evaluation_window: 30_runs
```

## Optional skill cooperation

- Elephas — emit Signal files for Chronicle promotion after every extraction
- Thread — may read recent browsing context for query rewriting (cooperative, not required)
- Weave — may use Weave for entity disambiguation
- Chronicle — may read Chronicle (read-only) for entity context

## Journal outputs

- Observation Journal — search and extraction runs
- Research Journal — structured multi-source research sessions

## Initialization

On first invocation of any Sift command, run `sift.init`:

1. Create `~/openclaw/data/ocas-sift/` and subdirectories (`reports/`)
2. Write default `config.json` with ConfigBase fields if absent
3. Create empty JSONL files: `sessions.jsonl`, `threads.jsonl`, `entities.jsonl`, `sources.jsonl`, `decisions.jsonl`
4. Create `~/openclaw/journals/ocas-sift/`
5. Ensure `~/openclaw/db/ocas-elephas/intake/` exists (create if missing)
6. Register cron job `sift:update` if not already present (check `openclaw cron list` first)
7. Log initialization as a DecisionRecord in `decisions.jsonl`

## Background tasks

| Job name | Mechanism | Schedule | Command |
|---|---|---|---|
| `sift:update` | cron | `0 0 * * *` (midnight daily) | `sift.update` |

```
openclaw cron add --name sift:update --schedule "0 0 * * *" --command "sift.update" --sessionTarget isolated --lightContext true --timezone America/Los_Angeles
```


## Self-update

`sift.update` pulls the latest package from the `source:` URL in this file's frontmatter. Runs silently — no output unless the version changed or an error occurred.

1. Read `source:` from frontmatter → extract `{owner}/{repo}` from URL
2. Read local version from `skill.json`
3. Fetch remote version: `gh api "repos/{owner}/{repo}/contents/skill.json" --jq '.content' | base64 -d | python3 -c "import sys,json;print(json.load(sys.stdin)['version'])"`
4. If remote version equals local version → stop silently
5. Download and install:
   ```bash
   TMPDIR=$(mktemp -d)
   gh api "repos/{owner}/{repo}/tarball/main" > "$TMPDIR/archive.tar.gz"
   mkdir "$TMPDIR/extracted"
   tar xzf "$TMPDIR/archive.tar.gz" -C "$TMPDIR/extracted" --strip-components=1
   cp -R "$TMPDIR/extracted/"* ./
   rm -rf "$TMPDIR"
   ```
6. On failure → retry once. If second attempt fails, report the error and stop.
7. Output exactly: `I updated Sift from version {old} to {new}`

## Visibility

public

## Support file map

| File | When to read |
|---|---|
| `references/schemas.md` | Before creating sessions, threads, or extraction records |
| `references/search_tiers.md` | Before tier selection or escalation |
| `references/query_rewrite.md` | Before query rewriting |
| `references/journal.md` | Before sift.journal; at end of every run |
