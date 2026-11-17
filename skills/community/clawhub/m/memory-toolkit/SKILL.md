---
name: memory-health
description: Complete memory management pipeline for OpenClaw agents — extraction, archiving, scoring, consolidation, health monitoring, hygiene, and ontology. Local by default (Ollama over local HTTP). Use for memory health checks, hybrid search, fact arbitration, cold-storage compaction, and memory pipeline maintenance.
---

# Memory Pipeline Skill

Complete memory management pipeline for OpenClaw agents: extraction, archiving,
scoring, consolidation, health monitoring, and ontology — local by default
(Ollama runs locally via HTTP).

⚠️ **One opt-in exception**: `trace_extractor.py` can send memory/session excerpts
to **Ollama cloud** (`https://ollama.com`) when `OLLAMA_API_KEY` is configured.
With no key it stays local; `TRACE_LLM_LOCAL_ONLY=1` refuses every cloud call. The
destination is printed before each send. See the Security Notes below.

> **⛔ MUST — releasing this skill.** Every change to this skill goes through
> `scripts/release.sh`, without exception. A change is **not done** until
> `scripts/release.sh check` passes green. Then, and only then, sync to the
> installed skill and tag via `scripts/release.sh release vX.Y.Z "msg"`.
> Never edit the installed skill directly. Never tag or publish on a red gate —
> fix the drift or the invariant, never bypass the gate.
> Pipeline: **local repo → installed skill → GitHub → ClawHub (manual).**

## Pipeline Overview

```
Nightly Cron (23h)
  │
  ├─ 1. trace_extractor.py    # Extract decisions/errors/facts from sessions
  ├─ 2. auto_archive.py       # Archive daily notes >21 days
  ├─ 3. scoring.py            # Score all memories with temporal decay
  ├─ 4. consolidate_advisor.py # Suggest consolidations (agent reviews)
  ├─ 5. conflict_resolver.py   # Arbitrate contradictory facts (NLI lifecycle)
  ├─ 6. memory_health.py       # Periodic health check (weekly)
  └─ 7. hybrid_search.py      # Hybrid search: FTS5 + sqlite-vec + RRF
```

All scripts are standalone and composable. Run individually or as a pipeline.

## Fact lifecycle (introduced in v3.0.0) — current release v4.0.6

The search DB no longer just accumulates facts: every fact carries a lifecycle
(`active` / `superseded` / `disputed`) and only `active` facts are ever
retrieved. `conflict_resolver.py` runs the four-step consistency pipeline:
atomic extraction → targeted retrieval of concurrent active facts → NLI
classification (`CONTRADICTION` / `REDUNDANT` / `COMPATIBLE`) → traceable state
update. A weak contradiction is escalated to `disputed` rather than silently
destroying an established fact; `pending` surfaces the queue and `resolve
--confirm|--reject` lifts the ambiguity. `compact.py` moves terminal facts into a
cold archive (`memories_archive` + JSONL audit) so the hot FTS5/vector indexes
stay lean without losing traceability.

## Scripts

### 1. `trace_extractor.py` — Session extraction

Extracts decisions, errors, facts, and patterns from OpenClaw session
transcripts and daily notes. Updates daily notes with extracted items,
appends entities to the ontology graph.

```bash
# Nightly (pattern-based, fast ~5s)
python3 scripts/trace_extractor.py --days 1

# Deep extraction (LLM-powered, ~60-180s)
python3 scripts/trace_extractor.py --days 3 --llm

# With session transcripts
python3 scripts/trace_extractor.py --days 1 --llm --session-file /path/to/session.jsonl

# Preview only
python3 scripts/trace_extractor.py --days 1 --llm --dry-run
```

**Categories extracted:**
- 🟢 DECISIONS — new choices, config changes, migrations
- 🔴 ERRORS — bugs, failures, workarounds
- 🔵 FACTS — new versions, configs, status changes
- ⬆️ PROMOTIONS — items worth promoting to MEMORY.md

**Output:** Daily notes updated, ontology entities added, `.trace-extracted` flag.

### 2. `auto_archive.py` — Daily note archiving

Moves daily notes older than N days to `memory/archive/YYYY-MM/` subdirectories.

```bash
python3 scripts/auto_archive.py                 # Archive notes > 21 days
python3 scripts/auto_archive.py --days 30       # Custom threshold
python3 scripts/auto_archive.py --dry-run       # Preview only
python3 scripts/auto_archive.py --verbose       # Show each file
```

Idempotent. Only moves `YYYY-MM-DD*.md` files. Zero dependencies.

### 3. `scoring.py` — Temporal decay scoring

Scores all memory items using exponential recency decay, category weights,
frequency boost, entity boost, and completion penalty.

```bash
python3 scripts/scoring.py                      # Score all memories
python3 scripts/scoring.py --verbose            # Show top 20
python3 scripts/scoring.py --threshold 0.3      # Filter by min score
python3 scripts/scoring.py --dry-run            # Don't write output
```

**Scoring formula:**
```
score = weight_category × recency_decay × frequency_boost × entity_boost × completion_penalty

recency_decay = exp(-ln(2) × days_old / HALF_LIFE_DAYS)
```

**Category weights:** DECISIONS ×3, ERRORS ×2, FACTS ×1.5, PATTERNS ×1.2, TRANSIENT ×1

**Output:** `memory/scores.json` — full ranking with stats and promotion candidates.

### 4. `consolidate_advisor.py` — Consolidation suggestions

Analyzes recent daily notes + scores.json to identify clusters, promotions,
stale items, and duplicates. Writes consolidation_report.json by default.
Modifies MEMORY.md only with --apply-promotions flag (requires confirmation).

```bash
python3 scripts/consolidate_advisor.py                     # Last 7 days
python3 scripts/consolidate_advisor.py --days 14           # Custom window
python3 scripts/consolidate_advisor.py --verbose           # All suggestions
python3 scripts/consolidate_advisor.py --no-llm            # Skip LLM (fallback)
python3 scripts/consolidate_advisor.py --apply-promotions  # Write to MEMORY.md
```

**Output:** `memory/consolidation_report.json` — clusters, promotions, stale items, duplicates.

LLM optional (Ollama) for cluster summaries. Falls back to text-based with `--no-llm`.

### 5. `memory_health.py` — System health check

Comprehensive diagnostics: trace extraction, LoCoMo benchmark, MEMORY.md size,
ontology health, daily notes hygiene, index status, drift detection.

**READ-ONLY by default**: writes nothing to disk. Use `--output-dir <path>` to save
JSON reports and SVG trend charts.

```bash
python3 scripts/memory_health.py              # Full health check (read-only)
python3 scripts/memory_health.py --quick      # Skip benchmark & LLM (read-only)
python3 scripts/memory_health.py --benchmark  # Benchmark only (read-only)
python3 scripts/memory_health.py --deep       # LLM + sessions + benchmark (weekly)
python3 scripts/memory_health.py --output-dir results/  # Save reports to disk
python3 scripts/memory_health.py --fix        # Fix mode (DESTRUCTIVE)
```

**Output:** `results/YYYY-MM-DD.json` — only with `--output-dir`.

**Destructive actions (`--fix`)**: Moves daily notes >14 days old to `archive/`,
rewrites ontology file (dedup + clean). Creates timestamped backup in `memory/backup/`
before modifying. Requires interactive confirmation or `--force` flag.

### 6. `ontology_compact.py` — Ontology graph GC

Compacts `memory/ontology/graph.jsonl` (an append-only operation log) by replaying
it into a consolidated state: one line per active entity, superseded records dropped.

**Safe by design**: backs up first (MD5-verified), writes to a temp file, validates
that the entity set and contents are identical, and only then swaps in place.
Idempotent: skips when the gain is below `--min-gain` (default 5%).

```bash
python3 scripts/ontology_compact.py --dry-run      # Report only
python3 scripts/ontology_compact.py                # Compact (threshold 5%)
python3 scripts/ontology_compact.py --min-gain 10  # Skip unless >=10% smaller
```

Run weekly. Typical gain on a never-compacted log: **~60-65%**.

### 7. `hybrid_search.py` — Hybrid search (FTS5 + sqlite-vec + RRF)

Hybrid memory search combining lexical (BM25 via SQLite FTS5) and semantic
(vector via sqlite-vec) retrieval using Reciprocal Rank Fusion (RRF, k=60).

```bash
# Initialize DB with schema
python3 scripts/hybrid_search.py init

# Index all memory files
python3 scripts/hybrid_search.py index

# Search
python3 scripts/hybrid_search.py query "project_alpha"
python3 scripts/hybrid_search.py query "roadmap EIIDP" --top 10

# Lexical only (BM25)
python3 scripts/hybrid_search.py query "2026-08-17" --lexical-only

# Vector only (semantic)
python3 scripts/hybrid_search.py query "memory decay scoring" --vector-only

# JSON output for programmatic use
python3 scripts/hybrid_search.py query "leadership coaching" --json

# Stats
python3 scripts/hybrid_search.py stats

# Index a single file
python3 scripts/hybrid_search.py add path/to/file.md --category skill
```

**How it works:**

```
query → ┬─ vector_search (nomic-embed-text, top 20) ──┐
        └─ lexical_search (FTS5/BM25, top 20) ────────┤
                                                        ↓
                                              RRF(k=60) fusion
                                                        ↓
                                        min_score filter (≥0.015)
                                                        ↓
                                        temporal boost (optional)
                                                        ↓
                                              source deduplication
                                                        ↓
                                                   top K results
```

RRF ignores raw scores and uses only ranks: `rrf(d) = Σ 1/(k + rank_m(d))`.
Source deduplication groups by file, returning the best chunk per source.

**Gemini vigilance #1 — min_rrf_score (noise threshold):**
Chunks appearing in neither top-20 list have RRF score ~0 = pure noise.
Filtered by default at `0.015`. Override with `--min-score 0` to disable.

**Gemini vigilance #3 — temporal_boost (decay weighting):**
RRF score is multiplied by `(1 + 0.1 * normalized_score)` where `normalized_score`
comes from the `score` column (populated by `scoring.py` temporal decay).
Gives slight priority to recent facts when context conflicts.
Disable with `--no-temporal-boost`.

**Schema:** Single SQLite file with three synchronized tables:
- `memories` — content, category, layer, source, score, timestamps
- `memories_fts` — FTS5 virtual table (external content, auto-synced via triggers)
- `memories_vec` — vec0 virtual table (float[768], nomic-embed-text)

**Layers:** episodic (daily notes), semantic (long-term facts, ontology), procedural (skills, config)

**Requirements:** `sqlite-vec` (pip install in venv), Ollama with `nomic-embed-text`

**Output:** `hybrid-search/agent_memory.db` — SQLite DB with FTS5 + vec0 indexes.

### 8. `conflict_resolver.py` — Fact lifecycle & dispute resolution

Four-step consistency pipeline over the search DB: **atomic extraction →
targeted retrieval of concurrent `active` facts → NLI classification → traceable
state update**. Only `active` facts are ever retrieved. A new fact that
contradicts an active one supersedes it (`superseded_by` now written); a weak
contradiction is escalated to `disputed` instead of silently destroying an
established fact.

```bash
# Analyse one candidate fact (read-only)
python3 hybrid-search/conflict_resolver.py check "On a migré la BDD sur MySQL 8" --subject serveur_prod

# Batch arbitration from JSONL (dry-run; --apply to persist)
python3 hybrid-search/conflict_resolver.py arbitrate facts.jsonl
python3 hybrid-search/conflict_resolver.py arbitrate facts.jsonl --apply --force

# What is waiting for a human? (cheap, deterministic)
python3 hybrid-search/conflict_resolver.py pending

# Lift the ambiguity explicitly
python3 hybrid-search/conflict_resolver.py resolve 42 --confirm
python3 hybrid-search/conflict_resolver.py resolve 42 --reject --replacement "corrected fact"
```

`--confirm` restores the wording to `active` **and supersedes any rival on the
same subject**; `--reject [--replacement]` supersedes it and optionally inserts a
corrected fact. Only `disputed` rows are eligible. `--no-llm` gives a
conservative lexical fallback; the LLM endpoint is loopback-only.

### 9. `compact.py` — Cold storage & lifecycle compaction

Moves terminal facts (`superseded`, optionally `disputed`) out of the hot tables
into a **cold archive** so FTS5/BM25 rank space and the vector index stop carrying
dead rows while full traceability is kept.

```bash
python3 hybrid-search/compact.py --stats              # hot vs cold sizes
python3 hybrid-search/compact.py --dry-run            # what would be archived
python3 hybrid-search/compact.py --apply --min-age-days 30
python3 hybrid-search/compact.py --restore 42         # rehydrate one fact
```

Rows are copied verbatim into `memories_archive` in the same SQLite file and
appended to a dated JSONL audit under `memory/audit/`, then `DELETE`d from the hot
table (fires the triggers → removed from FTS5 and `memories_vec`). **Never a hard
delete of data, only a move.** Dry-run is the default; mutation requires
`--apply`; a retention guard refuses rows newer than `--min-age-days`; the DB is
backed up via SQLite's `backup()` API and MD5-checked before any write. Requires
`sqlite-vec` (the vec0 delete trigger fires on `DELETE`).

## Ontology

The ontology graph stores entities and relations as JSONL. A YAML schema
defines allowed types and relations.

**Entity types:** Person, Organization, Project, Task, Document, Event,
Skill, Device, Service, Tool, Infrastructure, Concept, Location, Pet,
BugFix, SecurityEvent, Integration, Feature, Software, Configuration

**Relation types:** reports_to, has_owner, includes, depends_on, manages,
uses, integrated_with, located_at, fixes, monitors

**Files:**
- `memory/ontology/graph.jsonl` — entity and relation records
- `memory/ontology/schema.yaml` — type and relation definitions
- `memory/ontology/graph-index.json` — search index

## Configuration

Environment variables with defaults:

| Variable | Default | Description |
|----------|---------|-------------|
| `WORKSPACE` | `~/.openclaw/workspace` | OpenClaw workspace path |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama API URL |
| `OLLAMA_MODEL` | `glm-5.2` | Model for LLM extraction/summaries |

Scoring constants (top of `scoring.py`):

| Parameter | Default | Description |
|-----------|---------|-------------|
| `HALF_LIFE_DAYS` | 14 | Recency decay half-life |
| `MAX_SCORE` | 5.0 | Score cap |
| `PROMOTE_THRESHOLD` | 2.0 | Min score for promotion |
| `ARCHIVE_THRESHOLD` | 0.05 | Score below = archive candidate |

Memory health thresholds (top of `memory_health.py`):

| Parameter | Default | Description |
|-----------|---------|-------------|
| `MEMORY_MAX_SIZE` | 5000 | MEMORY.md max size in bytes |
| `DAILY_NOTES_MAX_AGE` | 14 | Days before archiving |

## Requirements

- Python 3.10+
- Ollama (optional — LLM extraction and cluster summaries)
- No pip packages required — pure stdlib (sqlite-vec optional for hybrid search)

## Nightly Cron Integration

Recommended nightly pipeline (after trace extraction):

```bash
# In nightly cron (23h):
python3 scripts/trace_extractor.py --days 1
python3 scripts/auto_archive.py
python3 scripts/scoring.py
python3 scripts/consolidate_advisor.py --no-llm  # quiet mode
```

Weekly health check (Monday, separate cron):

```bash
python3 scripts/memory_health.py --quick
```

Monthly deep check (manual):

```bash
python3 scripts/memory_health.py --deep
```

## Design Principles

1. **Local by default** — no cloud account, no paid dependency. `trace_extractor.py` is the only cloud-capable script, opt-in via `OLLAMA_API_KEY`, disclosed each run, cancellable via `TRACE_LLM_LOCAL_ONLY=1`
2. **Composable** — each script is standalone, can run independently
3. **Safe by default** — dry-run available for all analysis scripts; some nightly cron commands modify files by default (archive, scores, consolidation report). Review cron commands before deploying.
4. **Human-in-the-loop** — consolidation suggestions, not auto-merge
5. **Pipeline-friendly** — scripts chain naturally, outputs feed inputs
6. **Zero dependencies** — pure Python stdlib (except sqlite-vec for hybrid search)
7. **Strata-aware** — episodic, semantic, and procedural memory are separated

## License

MIT — free to use, modify, and share.

## Security Notes

- ⚠️ **Nightly cron modifies files by default**: `auto_archive.py` moves files, `scoring.py` writes scores.json, `consolidate_advisor.py` writes consolidation_report.json. Review cron commands before deploying.
- ⚠️ **`--fix` mode is destructive**: `memory-health.py --fix` moves daily notes to archive/ and rewrites ontology. Requires interactive confirmation or `--force` flag. Creates timestamped backups in `memory/backup/` before modifying.
- ⚠️ **`--force` flag**: The `--force` flag exists on `consolidate_advisor.py` and `memory-health.py` for non-interactive/cron use. It skips confirmation prompts. Only use in trusted automation with backups in place.
- ⚠️ **`--apply-promotions` modifies MEMORY.md**: `consolidate_advisor.py --apply-promotions` appends entries to MEMORY.md. Requires interactive confirmation or `--force` flag.
- ⚠️ **Memory and session content IS transmitted to an LLM** (`trace_extractor.py`): extraction sends an excerpt of daily notes (and, with `--session-file`, session transcript text) to a language model. **Primary transport is Ollama cloud** (`https://ollama.com`, `POST /api/chat`) when `OLLAMA_API_KEY` is configured — **content leaves this machine**. Local fallback is Ollama at `127.0.0.1:11434`. Set **`TRACE_LLM_LOCAL_ONLY=1`** to refuse every cloud call and force local-only. The destination is printed on each run (`[Security] ⚠️ CLOUD TRANSMISSION: …`).
- ⚠️ **PII sanitization is best-effort, not a guarantee**: `sanitize_pii()` removes API keys, tokens, JWTs, emails, passwords, PEM keys, French phone numbers and long opaque blobs before any LLM submission — but regex scrubbing cannot catch every secret format. **The transport decision is the primary control, not the filter.**
- ⚠️ **OLLAMA_URL should stay localhost**: local LLM calls (cluster summaries, embeddings) send memory text to Ollama. Keep `OLLAMA_URL=http://localhost:11434` to prevent data from leaving the machine.
- ⚠️ **Subprocess and urlopen are intentional local calls**: Scripts use `subprocess.run` to call other local Python scripts (trace_extractor, locomo_test) and `urllib.request.urlopen` to call the local Ollama HTTP API. These are intentional local-only calls. Keep `OLLAMA_URL` on localhost to prevent data from leaving the machine.
- ⚠️ **Memory files may contain sensitive data**: Review all files before indexing with hybrid search. The `scoring.py` script skips files matching secret patterns (`.secrets/`, `*.env`, `credentials*`, `*token*`, `*password*`, `.git/`).
- ⚠️ **Hybrid search consent warnings**: `hybrid_search.py` `index` command displays a consent warning before batch embedding. Use `--yes` to skip in automation. `add` command prints a one-line embedding notice (use `--quiet` to suppress).
- ⚠️ **`memory-health.py` is READ-ONLY by default**: No files or charts are written to disk without `--output-dir <path>`. SVG trend charts and JSON reports require this flag.
- ⚠️ **Scope confinement**: All scripts restrict file scanning to the designated memory directory (`WORKSPACE/memory/`), plus an explicit allowlist of three root config files that the indexer legitimately reads (`MEMORY.md`, `TOOLS.md`, the skill's own `SKILL.md`). No parent traversal (`../`) and no sibling skill enumeration (`skills/*/SKILL.md`). Paths are validated with `Path.resolve().is_relative_to(WORKSPACE)`.
- ⚠️ **`--session-file` is a deliberate, explicit exception**: `trace_extractor.py --session-file <path>` accepts one absolute path outside the workspace, because a session transcript does not live under `memory/`. It is never scanned automatically — no global session directory walk exists. Only pass paths you own and accept sending to the configured LLM transport.
- ⚠️ **Subprocess calls use fixed argument lists**: All `subprocess.run` calls use hardcoded `[sys.executable, ...]` argument lists — no environment variable injection possible. Script paths are validated against workspace confinement.
- ⚠️ **No PII in test fixtures**: `run_tests.py` uses anonymized query terms (`project_alpha`, `sample_note_01`) — no real project names, personal names, or sensitive references.
- ⚠️ **`--fix` mode is destructive**: `memory-health.py --fix` moves daily notes to archive/ and rewrites ontology. Requires interactive confirmation or `--force` flag. Creates timestamped backups in `memory/backup/` before modifying.
> **Security & audit triage:** see [`docs/SECURITY-AUDIT-NOTES.md`](docs/SECURITY-AUDIT-NOTES.md) for
> which scanner findings are closed in code and which are accepted false positives.