---
name: ocas-lucid
description: 'Nightly journal curator. Batch-processes OCAS skill journals via relevance
  classification and writes curated content to journal files for the configured memory
  provider to ingest. Classifies each journal for filing as a verbatim journal note,
  structured entity/relationship data, or skip. Features re-emergence detection,
  two-pass stale handling, change magnitude gates, hibernation protection,
  and incremental cursor-based resumption. NOT for real-time memory filing,
  skill evaluation, behavioral pattern detection, or entity identity resolution.'
license: MIT
source: https://github.com/<agent-handle>/lucid
includes:
- references/**
- scripts/**
metadata:
  author: Indigo Karasu (indigokarasu)
  version: "3.1.0"
---

# Lucid

Nightly journal curator. Batch-processes journals from all OCAS skills, classifies them
by relevance, and writes curated content to Lucid's journal files. The configured memory
provider reads these journals during its ingestion cycle and decides what to persist.

Lucid does NOT depend on any specific memory provider. It writes to
`{agent_root}/commons/journals/ocas-lucid/` and lets the memory provider handle ingestion.

## Interactive Menu

When invoked interactively, present a two-level menu. See `references/interactive-menu.md` for the full menu structure.

## When to Use

- Scheduled nightly cron at 3am (primary mode)
- Manual invocation via `lucid.dream` for immediate processing
- `lucid.status` to check last run, pending journals, filing stats

## When NOT to Use

- Real-time memory filing during active sessions
- Skill evaluation or improvement proposals (Mentor)
- Behavioral pattern detection (Corvus)
- Entity identity resolution (Elephas)

## Responsibility boundary

Lucid owns: nightly journal scanning, MemPalace filing (drawers + KG), relevance classification, weak signal recirculation, re-emergence detection.

Lucid does not own: Chronicle writes (use the elephas-chronicle bridge pattern from the memory-system-design skill), social graph updates (Weave only), real-time pattern analysis (Corvus), skill performance evaluation (Mentor).

## Adjacent boundaries**: Elephas also reads journals but for structured entity extraction and Chronicle promotion. Lucid reads journals for verbatim preservation and semantic searchability via MemPalace. When elephas is run manually (skill archived), update `config.json` cursor to include new elephas journal files to prevent lucid re-processing.

**Elephas pipeline as Lucid input source**: The canonical `elephas_cron_run.py` writes run journals to `<fs-root>/commons/journals/ocas-elephas/` which is NOT in Lucid's scan path. However, other OCAS skills' journals (mentor, vesper, scout) that Elephas reads from the shared `<fs-root>/commons/journals/` path ARE in Lucid's scope. When running elephas directly (not via the `ocas-elephas` skill), see `references/elephas-pipeline-gotchas.md` for the expected unprocessed residual pattern and the nested entity extraction gap.

**Elephas JSON parse errors**: The `elephas_cron_pipeline.py` skips ~43% of `mentor-light-*` files due to malformed JSON (trailing commas, unescaped newlines in `notes` fields). This is a producer-side bug in `ocas-mentor`, NOT an elephas pipeline bug. Lucid handles this gracefully via try/except. See `references/elephas-pipeline-json-errors.md` for the full error pattern, root cause, and recommended non-mitigation.

## Optional skill cooperation

- **Elephas**: Lucid queries Chronicle via `elephas.query` to check if an entity already exists before emitting a Signal. If Elephas is unavailable, Lucid emits the Signal anyway (Elephas deduplicates on ingestion).
- **MemPalace**: Required. Lucid uses MemPalace MCP tools for all filing operations. If MemPalace is unavailable, Lucid logs failures and skips filing for that run.

## Commands

- `lucid.dream` -- run the full dream cycle immediately, ignoring the time gate
- `lucid.status` -- last run timestamp, journals pending, cumulative filing stats, streak count
- `lucid.init` -- create storage directories, initialize config and logs, register cron jobs
- `lucid.update` -- pull latest from GitHub source; preserves journals and data

## Recovery Behavior

This skill implements the recovery contract from `spec-ocas-recovery.md`.

- **Evidence**: Every dream cycle writes an evidence record to `{agent_root}/commons/data/ocas-lucid/evidence.jsonl`, including skip/hibernation runs. The `not_activity_reason` field is mandatory when no side effects occur.
- **Gap detection**: On every wake, checks the evidence log. If gap exceeds 24h for dream cycle, logs `gap_detected` and runs a catch-up pass (capped at 40 journals).
- **Degraded mode**: When MemPalace MCP is unavailable, logs `degraded: mempalace` and queues filing for retry. When journal sources are missing, continues with available sources.
- **Log compaction**: Ingestion logs older than 30 days (no-op) or 90 days (error/gap) compacted. Last 7 days retained.

## Storage layout

```
{agent_root}/commons/data/ocas-lucid/
  config.json
  ingestion_log.jsonl
  decisions.jsonl
  recirculation_queue.jsonl
  removed_entries.jsonl
  staging/
  intents.jsonl
  evidence.jsonl

{agent_root}/commons/journals/ocas-lucid/
  YYYY-MM-DD/
    {run_id}.json
```

## Initialization

On `lucid.init` or first invocation:

1. Create `{agent_root}/commons/data/ocas-lucid/` and subdirectories (`staging/`)
2. Write default `config.json` with ConfigBase fields and skill-specific defaults
3. Create empty `ingestion_log.jsonl`, `decisions.jsonl`, `recirculation_queue.jsonl`, `removed_entries.jsonl`
4. Create `{agent_root}/commons/journals/ocas-lucid/`
5. Register cron jobs `lucid:dream` and `lucid:update` if not already present (check before registering)
6. Log initialization as a DecisionRecord

## Dream cycle

Four phases executed sequentially. Each journal is processed to completion (file + cursor advance) before moving to the next, ensuring mid-run termination loses no filed work.

See `references/dream-cycle.md` for the full phase-by-phase procedure (Orient, Gather, Classify, File), cursor tracking, and filing pitfalls.

### Incremental cursor

The ingestion log tracks each processed run_id. If the session terminates mid-run, the next cycle resumes from the first unprocessed journal. Filed content and cursor updates are durable — only the dream journal summary is lost on interruption.

## Re-emergence detection & stale handling

See `references/re-emergence.md` for the full re-emergence algorithm (3+ journal threshold, auto-promotion) and two-pass stale handling (mark on first contradiction, invalidate on second confirmation).

## Safety gates

See `references/safety-gates.md` for change magnitude gates (>30% warning, >50% staging hold) and hibernation protection (7-day no-new-journals → skip with zero IO).

## Dream journal output

Journal type: Action (writes to MemPalace are external side effects). Written to `{agent_root}/commons/journals/ocas-lucid/YYYY-MM-DD/{run_id}.json` using the standard JournalEntry schema with `journal_spec_version "1.3"`.

See `references/dream-journal.md` for the full journal schema (scan/file/skip counts, re-emergence events, Signal payload, skip path).

## OKR evaluation

Universal OKRs per `spec-ocas-journal.md`, plus skill-specific targets. See `references/okr.md` for the full OKR table (ingestion coverage, duplicate avoidance, recirculation, Signal precision, schedule adherence, data integrity).

## Inter-skill interfaces

**Reads (all read-only):**
- All skill journals from `{agent_root}/commons/journals/` (same access pattern as Mentor and Elephas)

**Writes:**
- MemPalace drawers and KG via MCP tools (external)
- Signal payload field in own dream journal (standard Signal schema from spec-ocas-shared-schemas.md)
- Own journal, data, and decisions files only

**Queries:**
- `mempalace_status`, `mempalace_search`, `mempalace_check_duplicate`, `mempalace_get_taxonomy` (read)
- `mempalace_add_drawer`, `mempalace_kg_add`, `mempalace_kg_invalidate` (write)
- `elephas.query` (optional, for pre-emission entity existence check)

## Background Tasks

| Job name | Mechanism | Schedule | Command |
|----------|-----------|----------|---------|
| `lucid:dream` | cron | `0 3 * * *` (3am local) | `lucid.dream` |
| `lucid:update` | cron | `0 0 * * *` (midnight daily) | `lucid.update` |

See `references/cron-execution.md` for cron-specific execution patterns (heredoc Python, two-pass classification, degraded mode).

**Schedule gap recovery:** If the system was asleep at the 3am `lucid:dream` run, the morning gap detector re-processes the missed run. On the next wake / morning invocation, check whether a dream cycle ran for the expected date (scan the run journal directory for the target `YYYY-MM-DD`); if absent, run `lucid.dream` once to catch up. Log the gap (schedule_gap=missed→recovered) and optionally batch with `lucid:update` so the missed nightly curation still lands the same day.

## Ontology mapping

Lucid extracts no entities from user data directly. It classifies and routes journal content produced by other skills. When it emits Signals to Elephas, the Signal's `payload.type` reflects the entity type found in the source journal (Person, Place, Concept, etc.) per spec-ocas-ontology.md.

## Self-Update

See `references/self-update-lucid.md`.

## Visibility

public

## Recirculation Queue `re_evaluations` Field

- **`re_evaluations` can be `null` (not 0)** in older queue entries. Always use `e.get('re_evaluations') or 0` when comparing. Direct `>= 3` comparison against `null` returns `False` in Python and silently skips cleanup.

## Scoring Traps

### Payload keys vs. narrative content

The `correction_or_lesson(+4)` signal must ONLY fire on narrative text fields (`summary`, `description`, `reasoning_summary`). Do NOT count payload dictionary **key names** (like `lessons_extracted`) as content — this causes routine operational journals to score 6+ and get filed as noise. Apply keyword checks to the extracted narrative text only, not to the full serialized JSON.

### MemPalace wing fallback

`mempalace_list_wings` may return only `root` even though the classification taxonomy defines wings like `wing_research`, `wing_knowledge`, etc. When this happens, file into `root/<room>` where `<room>` is the wing's topic slug (e.g., `root/preferences`, `root/operations`, `root/evolution`). Do not attempt to create custom wings via MCP — it is not supported.

### When interesting journals are buried under scan backlog

If the cursor is deep into a scan-heavy region (e.g., 2000+ unprocessed, mostly mentor light scans), the standard 40-journal batch will process zero interesting journals. **Mitigation**: Run a targeted pass that collects unprocessed journals only from high-signal skills (vesper, praxis, taste, custodian, dispatch) and processes those first. This ensures the cursor advances through scans *and* interesting signals get filed in the same session. See `references/classification.md` Pass 1 for the narrative extraction improvements needed to correctly score these journals.

### Narrative extraction must handle nested structures

The top-level-only narrative extraction in the original template misses ~80% of vesper content (`decision.reasoning_summary`, `decision.payload.entities_observed`, `run_identity.journal_type`) and ~60% of custodian findings (`findings[].diagnosis`). The classification reference (`references/classification.md`) now includes the correct multi-path extraction. **Always use the updated extraction, not the simplified top-level version.**

### Reference file resilience

`references/dream-cycle.md`, `references/re-emergence.md`, `references/safety-gates.md`, and `references/dream-journal.md` may not exist on disk even though the Support File Map references them. When a reference file is missing, fall back to the procedural instructions in the SKILL.md body itself. Do not block the run.

## Support File Map

| File | When to read |
|------|-------------|
| `references/cron-execution.md` | Before running any dream cycle in cron context. Contains the heredoc Python pattern, two-pass classification workflow, and degraded mode decision tree. |
| `references/classification.md` | Before classifying any journal entry. Contains the relevance scoring model, filing taxonomy, wing/room assignment rules, and skip criteria. |
| `references/dream-cycle.md` | Before executing the dream cycle. Phase-by-phase procedure (Orient, Gather, Classify, File), cursor tracking, and filing pitfalls. |
| `references/re-emergence.md` | During post-file cleanup. Re-emergence detection (3+ threshold, auto-promotion) and two-pass stale handling. |
| `references/safety-gates.md` | After classification, before filing. Change magnitude gates (>30% warning, >50% staging hold) and hibernation protection. |
| `references/dream-journal.md` | When writing the dream journal. Full output schema (counts, events, Signal payload, skip path). |
| `references/okr.md` | During OKR evaluation. Skill-specific targets for ingestion coverage, duplicate avoidance, recirculation, Signal precision, schedule adherence, data integrity. |
| `references/gotchas.md` | Before any dream cycle run. Operational pitfalls for journal discovery, KG triples, null fields, ingestion log formats, cursor resumption, and recirculation queue. |
| `references/elephas-pipeline-gotchas.md` | Before running the elephas cron pipeline directly (when the `ocas-elephas` skill is not found). Contains the list entity crash bug fix, bridge dependency, cursor update procedure, expected unprocessed residuals, nested entity extraction gap, and script path. |
| `references/elephas-pipeline-json-errors.md` | When elephas reports high JSON parse error rates on journal files. Contains the full error pattern, root cause (mentor malformed JSON), impact analysis, and recommended non-mitigation. |
| `references/bridge-health-check.md` | Before running any pipeline that depends on LadybugDB (elephas, deep scan). Health check, restart procedure for cron/terminal mode, and env var reference. |
| `scripts/lucid_dream_template.py` | Reference implementation of the dream cycle script. Copy to `/tmp/` and adapt rather than writing from scratch. Uses `pathlib`, skill-level scan exceptions, priority sorting, and produces `file`-key ingestion log entries compatible with cursor resumption. |

## Cron Execution Pattern

> **Critical**: `execute_code` is **blocked** in cron mode. Use `write_file` to write a Python script to `/tmp/`, then invoke it via `terminal(command="python3 /tmp/script.py")`.

### Multi-Batch Processing (for large backlogs)

When the journal backlog exceeds ~500 files (common), a single 40-journal batch will be entirely consumed by scan files. **Mitigation**: Set `BATCH_SIZE = 200` in the template script to process 5× more journals per run. This clears scan backlogs faster and reaches interesting signals (vesper, praxis, taste) sooner.

The template script (`scripts/lucid_dream_template.py`) now defaults to 200 journals per run.

### Two-Pass Classification Workflow

**First run (no cursor)**: Alphabetical sorting places scan/sweep journals (forge, finch, custodian) before interesting journals (mentor, praxis, dispatch, vesper, taste). A 40-journal cap means the first batch may be *entirely* scan files.

**Mitigation for first run**:
1. Separate journals into "interesting" and "scan" using `is_scan()` with **skill-level exceptions** (see `references/gotchas.md` — `mentor-light`, `vesper`, `taste`, `praxis-review`, `dispatch-triage` are NEVER scans)
2. Sort interesting journals by **skill priority** (mentor=0, vesper=1, praxis=2, taste=3, dispatch=4, spot=5, forge=6, custodian=7) — NOT alphabetically
3. Process interesting journals first (up to cap of 40)
4. Track both groups in the cursor — remaining scans are processed in subsequent runs

**Subsequent runs**: Resume from cursor, process next batch. Once all interesting journals are processed, move to scan batches.

### Journal Priority Heuristic

Skills with high-scan volume (forge, finch, custodian, spot) produce mostly operational noise. The interesting signals concentrate in:
- **ocas-mentor**: evaluation coverage, behavioral corrections in `notes` field
- **ocas-praxis**: `praxis-review-*` and `praxis-debrief*` filenames; `r_*` runs with `reasoning_summary` or `notes`
- **ocas-dispatch**: `dispatch-triage-*` and `dispatch-draft-*` filenames; `reasoning_summary` in decision block
- **ocas-vesper**: `*morning*` and `*evening*` briefings; `notes` field
- **ocas-taste**: consumption pattern records
- **ocas-custodian/light-***: Starting ~June 14, these contain lesson/blocker content (scores 6-7) — NOT pure scans

Skills with almost exclusively scan content (skip unless cap allows):
- ocas-forge (`journal-scan-*`, `r_*` numeric), ocas-finch (`scan-*`, `daily-*`, `weekly-*`), ocas-spot (`sweep-*`, `spot-watch-*`), ocas-custodian (`deep-scan-*`, `light-scan-*`)

### Degraded Mode Decision Tree

1. Check MemPalace availability via `mempalace_status`
2. **If unavailable**: Log `degraded: mempalace` in evidence, skip `mempalace_add_drawer`/`mempalace_kg_add` calls, write all other records (decisions, ingestion log, dream journal) normally
3. **If available but error on individual call**: Log the specific error, queue for retry in next run, continue with remaining journals
4. Never block the dream cycle on MemPalace — it is a write-side dependency, not a read-side one