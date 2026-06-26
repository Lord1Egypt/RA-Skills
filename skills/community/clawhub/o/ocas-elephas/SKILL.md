---
name: ocas-elephas
source: https://github.com/indigokarasu/elephas
install: openclaw skill install https://github.com/indigokarasu/elephas
description: Use when querying Chronicle (the system's long-term knowledge graph), ingesting signals from skill journals, running consolidation passes, resolving entity duplicates, or promoting candidates to confirmed facts. Trigger phrases: 'what does Chronicle know about', 'query the knowledge graph', 'ingest journals', 'consolidate', 'resolve entity', 'Chronicle status', 'update elephas'. Do not use for social relationship queries (use Weave), web research (use Sift), or person-focused OSINT (use Scout).
metadata: {"openclaw":{"emoji":"🐘"}}
---

# Elephas

Elephas is the system's long-term memory — the sole writer to Chronicle, the authoritative knowledge graph where entities, relationships, events, and inferences live permanently once confirmed. It ingests structured signals from every skill's journals, scores candidate facts for confidence, resolves identity across possible duplicates, and promotes what survives into durable Chronicle facts with full provenance. The Chronicle database initializes automatically on first use — no manual setup required.


## When to use

- Query Chronicle for entities, relationships, events, or inferences
- Ingest new signals from skill journals
- Run consolidation passes on pending candidates
- Resolve entity identity (possible duplicates)
- Promote or reject candidates
- Check Chronicle health and pending queue


## When not to use

- Social relationship queries — use Weave
- Web research — use Sift
- Person-focused OSINT — use Scout
- Direct user communication — use Dispatch


## Responsibility boundary

Elephas owns Chronicle: the authoritative long-term knowledge graph for entities, places, concepts, things, and their relationships.

Only Elephas writes to Chronicle. All other skills are read-only consumers.

Elephas does not own the social graph (Weave), OSINT briefs (Scout), or web research (Sift).

Elephas and Mentor are parallel journal consumers. Elephas reads journals to extract entity knowledge. Mentor reads journals to evaluate skill performance. Neither blocks the other.


## Storage layout

```
~/openclaw/db/ocas-elephas/
  chronicle.lbug      — Chronicle graph database (auto-created on first use)
  config.json         — consolidation and inference configuration
  staging/            — temporary files during ingestion passes
  intake/             — incoming signals from other skills
    {signal_id}.signal.json
    processed/        — moved here after ingestion

~/openclaw/journals/ocas-elephas/
  YYYY-MM-DD/
    {run_id}.json     — one Action Journal per consolidation or promotion run
```


Default config.json:
```json
{
  "skill_id": "ocas-elephas",
  "skill_version": "2.3.0",
  "config_version": "1",
  "created_at": "",
  "updated_at": "",
  "consolidation": {
    "immediate_interval_minutes": 15,
    "deep_interval_hours": 24
  },
  "identity": {
    "auto_merge_threshold": 0.90,
    "flag_review_threshold": 0.70
  },
  "inference": {
    "enabled": true,
    "min_supporting_nodes": 3
  },
  "retention": {
    "days": 0
  }
}
```


## Database rules

LadybugDB is an embedded single-file database. One `READ_WRITE` process at a time. Other skills open `chronicle.lbug` as `READ_ONLY` only — Elephas holds the `READ_WRITE` connection during active passes.

Surface lock errors immediately. Do not retry silently.


## Auto-initialization

Every command that opens the database runs `_ensure_init()` first. No manual init needed on first use.

Read `references/init_pattern.md` for the `_open_db` implementation pattern. Full DDL is in `references/schemas.md`.


## Commands

**elephas.ingest.journals** -- Ingest structured signals from skill journal files and signal intake directory. Read `references/ingestion_pipeline.md`. Auto-inits on first call. Writes Action Journal.

**elephas.consolidate.immediate** -- Immediate consolidation pass. Score candidate confidence, promote above threshold, flag possible matches. Writes Action Journal.

**elephas.consolidate.deep** -- Deep pass: full identity reconciliation, inference generation, graph cleanup. Writes Action Journal.

**elephas.identity.resolve** -- Attempt to resolve whether two Entity records refer to the same real-world entity. Read `references/ingestion_pipeline.md` → Deduplication. Never silently collapse records. Writes Action Journal.

**elephas.identity.merge** -- Merge two confirmed-same Entity records. Always reversible. Append to merge_history. Writes Action Journal.

**elephas.candidates.list** -- List pending candidates by confidence tier and age.

**elephas.candidates.promote** -- Manually promote a candidate to a confirmed Chronicle fact. Requires at least one supporting signal. Writes Action Journal.

**elephas.candidates.reject** -- Reject a candidate with stated reason. Writes Action Journal.

**elephas.query** -- Query Chronicle for entities, relationships, events, or inferences. Read `references/schemas.md` for node types and Cypher patterns. All queries are read-only. Returns only confirmed facts unless `include_candidates=true` specified.

**elephas.init** -- Diagnostic and repair command. Checks schema, creates missing tables, verifies indexes. Use when troubleshooting — the database initializes automatically on first use.

**elephas.status** -- Report Chronicle health.

```cypher
CALL show_tables() RETURN *;
MATCH (e:Entity) RETURN count(e) AS entities;
MATCH (p:Place) RETURN count(p) AS places;
MATCH (c:Concept) RETURN count(c) AS concepts;
MATCH (s:Signal {status: 'active'}) RETURN count(s) AS pending_signals;
MATCH (c:Candidate {status: 'pending'}) RETURN count(c) AS pending_candidates;
MATCH ()-[r]->() RETURN count(r) AS relationships;
CALL show_warnings() RETURN *;
```

Also report: last consolidation timestamps, pending identity reviews, inference count, intake queue depth.

**elephas.journal** -- Write Action Journal for the current run. Read `references/journal.md`. Called at end of every consolidation, promotion, merge, or rejection run.

**elephas.update** -- Pull latest skill package from GitHub source. Preserves journals and data.


## Run completion

After every Elephas command that modifies Chronicle or processes signals:

1. Process all files in `~/openclaw/db/ocas-elephas/intake/`; move processed files to `intake/processed/`
2. Persist ingestion results, promotion decisions, and merge records
3. Log material decisions to `decisions.jsonl` (if data directory exists)
4. Write journal via `elephas.journal`

## Memory lifecycle

```
Skill Journal / Signal Intake
  → Signal (immutable after creation)
    → Candidate (pending until confirmed, rejected, or merged)
      → Chronicle Fact (persists indefinitely)
      → Inference (separate, never overwrites facts)
```


## Consolidation passes

Immediate (every 15 min) -- creates candidates, scores confidence, promotes high-confidence. Scheduled -- promotes remaining, deduplicates.
Deep (every 24 hr) -- full identity reconciliation, inference generation, graph cleanup.


## Identity resolution rules

States: `distinct` (default), `possible_match`, `confirmed_same`. Merges are always reversible.

Resolution precedence: exact identifier match → name+location with corroboration → behavioral pattern match.

Ambiguous cases preserve separation. Never silently collapse records.


## Write authority

Only Elephas writes to Chronicle. Other skills open `chronicle.lbug` as `READ_ONLY` only.

Elephas does not write to any other skill's database.


## OKRs

Universal OKRs from spec-ocas-journal.md apply. Elephas-specific:

```yaml
skill_okrs:
  - name: promotion_precision
    metric: fraction of promoted candidates uncontradicted after 30 days
    direction: maximize
    target: 0.90
    evaluation_window: 30_runs
  - name: identity_merge_accuracy
    metric: fraction of auto-merges not subsequently reversed by human review
    direction: maximize
    target: 0.95
    evaluation_window: 30_runs
  - name: candidate_queue_age
    metric: median age of pending candidates in hours
    direction: minimize
    target: 24
    evaluation_window: 30_runs
  - name: ingestion_coverage
    metric: fraction of journal files ingested within one consolidation cycle
    direction: maximize
    target: 0.99
    evaluation_window: 30_runs
```


## Optional skill cooperation

- All skills — ingest structured signals from skill journals and signal intake
- Weave — read-only cross-DB queries for social graph enrichment
- Mentor — Mentor reads Chronicle (read-only) for evaluation context


## Journal outputs

Action Journal — every consolidation, promotion, merge, rejection, and ingestion run.


## Initialization

On first invocation of any Elephas command, run `elephas.init`:

1. Create `~/openclaw/db/ocas-elephas/` and subdirectories (`staging/`, `intake/`, `intake/processed/`)
2. Write default `config.json` with ConfigBase fields if absent
3. Create `~/openclaw/journals/ocas-elephas/`
4. Open database with `_open_db()` which auto-creates `chronicle.lbug` and runs DDL if needed
5. Register cron jobs `elephas:ingest`, `elephas:deep`, and `elephas:update` if not already present (check `openclaw cron list` first)
6. Log initialization as a DecisionRecord


## Background tasks

| Job name | Mechanism | Schedule | Command |
|---|---|---|---|
| `elephas:ingest` | cron | `*/15 * * * *` (every 15 min) | `elephas.ingest.journals` then `elephas.consolidate.immediate` |
| `elephas:deep` | cron | `0 4 * * *` (daily 4am) | `elephas.consolidate.deep` — full identity reconciliation, inference, cleanup |
| `elephas:update` | cron | `0 0 * * *` (midnight daily) | `elephas.update` |

Cron options: `sessionTarget: isolated`, `lightContext: true`, `wakeMode: next-heartbeat`.

Registration during `elephas.init`:
```
openclaw cron list
# If elephas:ingest absent:
openclaw cron add --name elephas:ingest --schedule "*/15 * * * *" --command "elephas.ingest.journals && elephas.consolidate.immediate" --sessionTarget isolated --lightContext true --wakeMode next-heartbeat --timezone America/Los_Angeles
# If elephas:deep absent:
openclaw cron add --name elephas:deep --schedule "0 4 * * *" --command "elephas.consolidate.deep" --sessionTarget isolated --lightContext true --wakeMode next-heartbeat --timezone America/Los_Angeles
# If elephas:update absent:
openclaw cron add --name elephas:update --schedule "0 0 * * *" --command "elephas.update" --sessionTarget isolated --lightContext true --timezone America/Los_Angeles
```


## Self-update

`elephas.update` pulls the latest package from the `source:` URL in this file's frontmatter. Runs silently — no output unless the version changed or an error occurred.

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
7. Output exactly: `I updated Elephas from version {old} to {new}`


## Visibility

public


## Support file map

| File | When to read |
|---|---|
| `references/schemas.md` | Before any DDL, query, or data write; before elephas.init |
| `references/init_pattern.md` | When implementing _open_db or troubleshooting initialization |
| `references/ontology.md` | When evaluating entity types, relationship types, or identity rules |
| `references/ingestion_pipeline.md` | Before elephas.ingest.journals or any consolidation pass |
| `references/journal.md` | Before elephas.journal; at end of every run |
