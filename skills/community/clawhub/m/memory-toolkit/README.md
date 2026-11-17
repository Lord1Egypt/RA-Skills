# 🧠 OpenClaw Memory Pipeline

**Complete memory management pipeline for OpenClaw agents: extraction, archiving,
scoring, consolidation, health monitoring, and hybrid search — local by default.**

Seven standalone Python scripts that form a complete memory lifecycle pipeline for
[OpenClaw](https://github.com/openclaw/openclaw) agents. Everything runs on this
machine out of the box: Ollama over local HTTP, no cloud account, no paid dependency
— works with any local LLM (Ollama, LM Studio, etc.) or fully without LLM in fallback
mode.

> **One exception, and it is opt-in:** `trace_extractor.py` can use **Ollama cloud**
> (`https://ollama.com`) when an API key is configured, because that content leaves
> the machine. With **no key configured it stays local**, and
> **`TRACE_LLM_LOCAL_ONLY=1` refuses every cloud call outright**. Every run prints its
> destination first (`[Security] ⚠️ CLOUD TRANSMISSION: …`). See
> [Security Notes](#security-notes).

Built for local-first OpenClaw setups (Ollama/GLM, nomic-embed-text).

## Pipeline

```
Nightly Cron (23h)
  │
  ├─ 1. trace_extractor.py     # Extract decisions/errors/facts from sessions
  ├─ 2. auto_archive.py        # Archive daily notes >21 days
  ├─ 3. scoring.py             # Score all memories with temporal decay
  ├─ 4. consolidate_advisor.py # Suggest consolidations (agent reviews)
  ├─ 5. conflict_resolver.py   # Arbitrate contradictory facts (NLI lifecycle)
  ├─ 6. memory_health.py       # Periodic health check (weekly)
  └─ 7. ontology_compact.py    # GC the ontology op-log (weekly)
```

All scripts are standalone and composable. Run individually or as a pipeline.

## Benchmark — LoCoMo (v4.0)

Most AI memory benchmarks publish cherry-picked configurations: `top-200` context
windows, excluded failure modes, or proprietary cloud pipelines. This project
publishes a **reproducible, glass-box** result — including when it sits below the
state of the art.

We evaluated the toolkit (100 % local indexing via **SQLite FTS5 BM25 +
`sqlite-vec` cosine similarity + Reciprocal Rank Fusion at `k=15`**, zero LLM
calls during ingestion) against the **LoCoMo** long-term conversational memory
benchmark (`snap-research/locomo`, SHA256 `79fa87e9…ea698ff4`).

### 1. Official Protocol (Categories 1–4)

Standard academic/industry protocol, Category 5 adversarial traps excluded.
Deterministic retrieval across all 10 conversations (`n = 1,536`) and end-to-end
QA across 9 validated conversations (`n = 1,386`), using `deepseek-v4.1-flash`
as both Reader and Judge.

| System | Architecture | LLM Calls at Index Time | Reader / Judge | QA Accuracy (Cat. 1–4) | Execution Scope |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **LangMem** | Agentic Memory | Yes (every turn) | GPT-4o-mini | 48.4% | Cloud API |
| **OpenClaw Memory Toolkit** | **BM25 + `sqlite-vec` + RRF (`k=15`)** | **None (0 LLM calls)** | **`deepseek-v4.1-flash`** | **49.6%** *(41.4% strict)* | **100% Local-First** |
| **OpenAI Memory** | Proprietary Assistant Memory | Yes | GPT-4o-mini | 52.9% | Cloud (Closed) |
| **Mem0** | Fact Extraction + Vector/Graph | Yes (every turn) | GPT-4o-mini | 66.9% – 68.4% | Cloud / Managed |
| **Letta (MemGPT)** | Agent OS / Multi-step File Search | Agent loops | GPT-4o-mini | 74.0% | High-latency loops |
| **Zep (Graphiti)** | Bi-temporal Knowledge Graph | Yes (every turn) | GPT-4o-mini | 75.1% | Cloud Graph DB |

### 2. Retrieval vs. QA — Why Retrieval Is the Ceiling

The deterministic retrieval engine (zero LLM cost) achieves:

* **`hit@15`** (at least one gold evidence chunk in top-15): **`65.1%`** (`n = 1,536`)
* **`all_evidence`** (all required gold chunks in top-15): **`51.6%`**
* **`MRR`** (mean reciprocal rank): **`0.449`**

| Category | Question Type | Questions (`n`) | Strict (Full Match) | Standard (Partial = ½) | Coverage | Engineering Diagnosis |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cat. 2** | Temporal Reasoning | 284 | **50.7%** | 54.6% | 58.5% | Strong chronological retention without a heavy temporal graph. |
| **Cat. 4** | Single-Hop Factual | 768 | **48.2%** | 55.3% | 62.5% | Tracks the `65.1%` `hit@15` retrieval ceiling almost 1:1. |
| **Cat. 1** | Multi-Hop Synthesis | 250 | **18.8%** | 36.6% | 54.4% | **89 partial hits**: `hit@15` is `65.1%`, but `all_evidence` drops to `51.6%`. The retriever finds pieces of the answer, not the full set. |
| **Cat. 3** | Open-Domain Inference | 83 | **15.7%** | 19.3% | 22.9% | By design, the reader prompt outputs `INSUFFICIENT` rather than guessing when facts are not explicitly grounded. |
| **Total** | **Official Protocol (Cat. 1–4)** | **1,386** | **41.4%** | **49.6%** | **57.8%** | **Reader efficiency is 76% of the `hit@15` ceiling (`49.6% / 65.1%`).** |

### 3. Full "Hardcore" Protocol (Categories 1–5, Adversarial Traps Included)

Evaluated on the complete LoCoMo dataset (`n = 1,946` QA / `n = 1,982` retrieval),
which includes **406 Adversarial questions (Category 5)** designed to trick agents
into hallucinating false premises:

* **Overall Hardcore Accuracy (Cat. 1–5):** **`57.6%`** (`n = 1,946`)
* **Category 5 (Adversarial Hallucination Resistance):** **`88.7%`** (`360 / 406` false premises successfully rejected)
* **Full-Dataset Retrieval (`n = 1,982`):** `hit@15 = 58.2%` · `all_evidence = 47.5%` · `MRR = 0.391`

> **The Hallucination Trade-off (Cat. 3 vs. Cat. 5):** the exact same strictness
> that penalizes speculative inference in Category 3 (`15.7%` strict) provides an
> **`88.7%` shield against adversarial traps in Category 5**. For production
> personal and enterprise agents, we prioritize factual grounding over speculation.

### 4. Next Engineering Milestones (Closing the Retrieval Gap)

Because the reader model is not the bottleneck, the v4.x roadmap focuses strictly
on lifting the `65.1%` retrieval ceiling and the `51.6%` multi-hop evidence assembly:

1. **Semantic & Dialog-Aware Chunking:** refining turn boundaries and entity anchoring at index time so multi-session facts aren't split across low-ranked chunks.
2. **Two-Stage Local Reranking:** expanding initial RRF candidate retrieval (`k=40`) followed by a lightweight local cross-encoder to boost `all_evidence` into the final `top-15` window.
3. **Dual Date Formatting:** preserving both relative conversational expressions ("the Sunday before May 25") and resolved ISO dates to eliminate false negatives in temporal judging.

> **Scope note:** Categories 1–5 figures come from the "hardcore" run (`n = 1,946`);
the comparable table uses the official Cat. 1–4 protocol (`n = 1,386`). Both are
measured on the same harness. Raw result files: `locomo-official-2026-10-11-FINAL.json`
and `locomo-hardcore-2026-10-11-FINAL.json`.

## Contributing

This README is written for **users**. If you are **maintaining this repository**
(working on the release pipeline, the gate, or the repo↔skill sync), read
[CONTRIBUTING.md](CONTRIBUTING.md) instead — it documents the full
repo → skill → GitHub → ClawHub flow and the invariants the release gate enforces.

> **MUST — every memory-skill change goes through `scripts/release.sh`.**
> A change to `skills/memory-health/**` is not "done" until
> `scripts/release.sh check` passes green. Never edit the installed skill
> directly; never let the repo and the skill drift. Full detail in
> [CONTRIBUTING.md](CONTRIBUTING.md).

## Scripts

### 1. `trace_extractor.py` — Session extraction

Extracts decisions, errors, facts, and patterns from OpenClaw session transcripts
and daily notes. Updates daily notes, appends entities to the ontology graph.

```bash
# Nightly (pattern-based, fast ~5s)
python3 scripts/trace_extractor.py --days 1

# Deep extraction (LLM-powered, ~60-180s)
python3 scripts/trace_extractor.py --days 3 --llm

# With a specific session transcript file (opt-in, explicit)
python3 scripts/trace_extractor.py --days 1 --llm --session-file /path/to/session.jsonl

# Preview only
python3 scripts/trace_extractor.py --days 1 --llm --dry-run
```

**Categories:** 🟢 DECISIONS, 🔴 ERRORS, 🔵 FACTS, ⬆️ PROMOTIONS

### 2. `auto_archive.py` — Daily note archiving

Moves daily notes older than N days to `memory/archive/YYYY-MM/`.

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

**Formula:** `score = weight_category × recency_decay × frequency_boost × entity_boost × completion_penalty`

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

Comprehensive diagnostics: trace extraction, benchmark, MEMORY.md size, ontology
health, daily notes hygiene, index status, drift detection.

**READ-ONLY by default**: writes nothing to disk. Use `--output-dir <path>` to save
JSON reports and SVG trend charts.

```bash
python3 scripts/memory_health.py              # Full health check (read-only)
python3 scripts/memory_health.py --quick      # Skip benchmark & LLM (read-only)
python3 scripts/memory_health.py --benchmark  # Benchmark only (read-only)
python3 scripts/memory_health.py --deep       # LLM + sessions + benchmark
python3 scripts/memory_health.py --output-dir results/  # Save reports to disk
python3 scripts/memory_health.py --fix        # Fix mode (DESTRUCTIVE)
```

**Output:** `results/YYYY-MM-DD.json` — only with `--output-dir`.

**Destructive actions (`--fix`)**: Moves daily notes >14 days old to `archive/`,
rewrites ontology file. Creates timestamped backup before modifying. Requires
interactive confirmation or `--force` flag.

### 6. `ontology_compact.py` — Ontology graph GC

Compacts `memory/ontology/graph.jsonl` (an append-only operation log) by replaying
it into a consolidated state: one line per active entity, superseded records dropped.

**Safe by design**: backs up first (MD5-verified), writes to a temp file, validates
that the entity set and contents are identical, and only then swaps in place. Skips
entirely when the gain is below a threshold, so it is idempotent.

```bash
python3 scripts/ontology_compact.py --dry-run      # Report only
python3 scripts/ontology_compact.py                # Compact (default threshold 5%)
python3 scripts/ontology_compact.py --min-gain 10  # Skip unless >=10% smaller
```

**Output:** rewrites `memory/ontology/graph.jsonl` + a timestamped backup in
`memory/ontology/backups/`.

Typical gain on an op-log that has never been compacted: **~60-65%**.
Run it weekly; between runs the file only grows by genuinely new operations.

### 7. `hybrid-search/hybrid_search.py` — Hybrid search engine

FTS5 (BM25) + sqlite-vec (cosine similarity) + Reciprocal Rank Fusion (k=60).

```bash
python3 hybrid-search/hybrid_search.py init                    # Create index DB
python3 hybrid-search/hybrid_search.py index                   # Batch index memory files
python3 hybrid-search/hybrid_search.py add path/to/file.md     # Add single file
python3 hybrid-search/hybrid_search.py search "project alpha"  # Hybrid search
python3 hybrid-search/hybrid_search.py status                  # Index stats
```

**Point-in-time retrieval (v3.4):** pass `--as-of YYYY-MM-DD` to `query`,
`search` or `context` to reconstruct the facts visible on that **past** date —
not what the index believes today. This is the difference between an
As-Maintained view and a retrievable As-Built baseline: the ledger marks rows
`superseded` (with a `superseded_at` timestamp) instead of deleting them, so the
history is already there to replay.

```bash
# What did the agent know on 1 July? (bare date = end of that day)
python3 hybrid-search/hybrid_search.py query "database backend" --as-of 2026-07-01

# Reconstruct context as of a precise instant
python3 hybrid-search/hybrid_search.py context "backup script" --as-of 2026-06-15T08:00:00
```

A fact created **after** the requested date is invisible; a fact still active on
that date stays visible even if it was superseded later. Without `--as-of` the
behaviour is unchanged (active facts only). _Limitation:_ `--as-of` cannot go
back before the first indexing date, since no row predates it (`valid_from`
carries historical *world* time, a separate axis).

**Scope:** Only indexes files within `WORKSPACE/memory/` + `MEMORY.md` + `TOOLS.md` + self `SKILL.md`.
Personal files (`USER.md`, `IDENTITY.md`, `AGENTS.md`, `SOUL.md`, `HEARTBEAT.md`) are excluded.
No sibling skill enumeration (`skills/*/SKILL.md` glob removed).

### 7. `hybrid-search/conflict_resolver.py` — Fact lifecycle & conflict arbitration

Implements the four-step consistency pipeline: **atomic extraction → targeted
retrieval of concurrent `active` facts → NLI classification → traceable state
update**. A new fact that contradicts an active one marks the old row
`superseded` (`superseded_by` finally populated) and inserts the new one as
`active`; a redundant fact refreshes `last_confirmed` instead of duplicating; a
compatible fact is added. A **weak** contradiction (confidence below the floor)
flags the old fact `disputed` and asks for confirmation rather than destroying a
truth.

```bash
# Analyse one fact against active memory (read-only)
python3 hybrid-search/conflict_resolver.py check "On a migré la BDD sur MySQL 8" --subject serveur_prod

# Batch arbitration from a JSONL of {content, subject?} (dry-run)
python3 hybrid-search/conflict_resolver.py arbitrate facts.jsonl

# Persist resolutions (mutates DB)
python3 hybrid-search/conflict_resolver.py arbitrate facts.jsonl --apply --force

# Inspect lifecycle states
python3 hybrid-search/conflict_resolver.py lifecycle --status superseded

# Heuristic-only (no LLM, offline)
python3 hybrid-search/conflict_resolver.py check "..." --subject x --no-llm
```

**Interactive resolution of blocked facts** — a `disputed` fact is a *suspended*
state waiting for a human. `pending` surfaces the queue (cheap, deterministic) so
the agent can raise it at the next relevant turn; `resolve` lifts the ambiguity
explicitly. `--confirm` restores the wording to `active` **and supersedes any
rival claim on the same subject**, so the pair can never both stay visible;
`--reject` supersedes it and optionally inserts a corrected `--replacement`.
Only rows currently `disputed` are eligible — resolving an `active` or already
`superseded` row is refused.

```bash
# What is waiting for adjudication?
python3 hybrid-search/conflict_resolver.py pending
python3 hybrid-search/conflict_resolver.py pending --json

# The wording stands -> active (rivals superseded)
python3 hybrid-search/conflict_resolver.py resolve 42 --confirm

# The wording was wrong -> superseded, with a corrected fact
python3 hybrid-search/conflict_resolver.py resolve 42 --reject \
    --replacement "The internal DNS is 10.0.0.99"
```

**Safety:** the LLM endpoint is loopback-only (same guard as `hybrid_search.py`);
`--no-llm` gives a conservative lexical fallback that never auto-supersedes on a
weak signal; analysis is read-only unless `--apply` is passed. Migrates an older
DB in place (adds the lifecycle columns idempotently).

### 8. `hybrid-search/compact.py` — Cold storage & lifecycle compaction

The lifecycle work keeps `superseded`/`disputed` facts out of *retrieval*, but
they still occupy the hot tables and their FTS5/vector indexes. Over months that
inflates BM25 rank space, the `memories_vec` table and the stats. This compactor
moves terminal facts into a **cold store** while keeping full traceability.

```bash
# Hot vs cold sizes
python3 hybrid-search/compact.py --stats

# What would be archived (superseded older than 30 days)
python3 hybrid-search/compact.py --dry-run

# Actually archive (MD5-verified backup + JSONL audit, then delete from hot)
python3 hybrid-search/compact.py --apply --min-age-days 30
python3 hybrid-search/compact.py --apply --include-disputed

# Resurrect one archived fact
python3 hybrid-search/compact.py --restore 42
```

**How "cold" works:** rows are copied verbatim into `memories_archive` in the
same SQLite file (transactional, no cross-file join) and appended to a dated
JSONL audit under `memory/audit/`; the hot rows are then `DELETE`d, which fires
the existing triggers and removes them from FTS5 and the vector index — the
actual perf win. **Never a hard delete of data, only a move.**

**Safety:** mutation requires `--apply` (dry-run is the default); the whole DB is
backed up via SQLite's backup API (a `copy2` on a live DB can capture a torn WAL)
and checked before any write; a retention guard refuses to archive rows newer
than `--min-age-days`; rows whose age cannot be proven are kept. Requires
`sqlite-vec` (the vec0 trigger fires on delete) and refuses loudly rather than
half-archiving if it is missing.

### 9. `hybrid-search/run_tests.py` — Search validation

Runs anonymized test queries against the hybrid search index.

```bash
python3 hybrid-search/run_tests.py          # Run all test queries
python3 hybrid-search/run_tests.py --verbose # Show scores and metadata
```

**Test fixtures use anonymized terms** (`project_alpha`, `sample_note_01`, etc.) — no real project names or personal data.

The same directory ships the regression guards run by the release gate:

| Guard | Pins |
|-------|------|
| `test_model_resolution.py` | the full model-resolution chain + raise-on-missing-safety-model |
| `test_extract_atomic.py` | `extract_atomic()` number protection and clause splitting |
| `test_loopback_guard.py` | cloud calls never leave except through the opt-in path |
| `test_meta_gate.py` | meta/pipeline chatter is never captured as a fact |
| `test_ontology_key_parity.py` | indexer and ontology migrator build the same display key |

### 10. Model resolution — `hybrid-search/llm_resolution.py` (v4.0)

**Single source of truth for the effective LLM model.** No script hard-codes a
model name any more; every caller asks this module, which resolves at runtime and
reports *where the answer came from*.

Resolution chain, in order (first hit wins):

1. an explicit `*_LLM_MODEL` / `OLLAMA_MODEL` env var — **visible and logged**,
   never silent (the escape hatch is kept on purpose);
2. the gateway default, `agents.defaults.model.primary` from `openclaw.json`;
3. the configured fallback, `agents.defaults.model.fallbacks[0]`;
4. the local safety net (`qwen2.5:7b`), **presence-checked before use** — if the
   model is absent the module **raises** rather than letting Ollama start a
   synchronous multi-GB pull that would hang an unattended nightly run.

```python
from llm_resolution import resolve_llm_model, explain_resolution

resolve_llm_model()   # -> "deepseek-v4.1-flash:cloud" (a name the daemon serves)
explain_resolution()  # -> {"model": ..., "source": "gateway:primary", "chain": [...]}
```

**Callers:** `trace_extractor.py`, `hybrid-search/auto_capture.py`,
`hybrid-search/conflict_resolver.py`, `consolidate_advisor.py`. The model is
resolved once per run (`@lru_cache`).

### 11. `mcp-server.py` — Read-only memory access for any agent

Exposes the local hybrid-search index over the Model Context Protocol (stdio),
so any MCP-capable agent can query the memory **without shell access** and
without writing to it. Three tools, all read-only:

| Tool | Purpose |
|------|---------|
| `memory_query(query, top=5)` | Hybrid search (FTS5 BM25 + vector + RRF) over memory |
| `memory_facts(topic=None, limit=20)` | Current facts, filterable by topic |
| `memory_stats()` | Row counts, active facts, statuses, last insert |

```json
{
  "mcpServers": {
    "memory": {
      "command": "python3",
      "args": ["/path/to/memory-health/mcp-server.py"],
      "transport": "stdio"
    }
  }
}
```

**Read-only by construction.** The server opens the index and never issues a
write; the nightly pipeline keeps the monopoly on mutation. Diagnostics go to
`stderr`, never to `stdout` — the JSON-RPC stream stays clean.

```bash
# smoke test without a gateway
printf '%s\n%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"t","version":"1"}}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' | python3 mcp-server.py
```

## Ontology

JSONL-based entity and relation graph with YAML schema.

**Entity types:** Person, Organization, Project, Task, Document, Event, Skill,
Device, Service, Tool, Infrastructure, Concept, Location, Pet, BugFix,
SecurityEvent, Integration, Feature, Software, Configuration

**Relation types:** reports_to, has_owner, includes, depends_on, manages, uses,
integrated_with, located_at, fixes, monitors

**Files:**
- `ontology/schema.yaml` — type and relation definitions
- `memory/ontology/graph.jsonl` — entity and relation records (generated)
- `memory/ontology/graph-index.json` — search index (generated)

## Configuration

Environment variables with defaults:

| Variable | Default | Description |
|----------|---------|-------------|
| `WORKSPACE` | `~/.openclaw/workspace` | OpenClaw workspace path |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama API URL (localhost only) |
| `OLLAMA_MODEL` | _(from gateway config)_ | **Explicit override** for LLM extraction/summaries. Unset = follow the gateway |
| `TRACE_LLM_MODEL` | _(from gateway config)_ | **Explicit override** for trace-extractor LLM calls. Unset = follow the gateway |
| `CONFLICT_LLM_MODEL` | _(from gateway config)_ | **Explicit override** for conflict arbitration (NLI). Unset = follow the gateway |
| `OPENCLAW_CONFIG` | `~/.openclaw/openclaw.json` | Gateway config read by the model resolver (v4.0) |
| `MEMORY_DB` | `hybrid-search/agent_memory.db` | Path to the search/lifecycle DB |
| `TRACE_LLM_LOCAL_ONLY` | _(unset)_ | Set to `1` to refuse cloud LLM calls and force local-only. **Recommended for any privacy-sensitive deployment.** |
| `OLLAMA_API_KEY` | _(unset)_ | Enables **Ollama cloud** (`ollama.com`) in `trace_extractor.py`. Unset = local only |

## Requirements

- Python 3.10+
- Ollama (optional — LLM extraction and cluster summaries)
- No pip packages required for core pipeline. Hybrid search requires sqlite-vec (optional).

> **Recommended local model:** `qwen2.5:7b` for Auto-Capture and conflict
> arbitration. The smaller `qwen2.5:3b` was found to return empty extractions and
> to split numeric values (`Ubuntu 24.04`); 7 b extracts whole facts reliably.
> Both are local — the loopback-only guarantee is unchanged.

## Nightly Cron

```bash
# Nightly (23h):
python3 scripts/trace_extractor.py --days 1
python3 scripts/auto_archive.py
python3 scripts/scoring.py
python3 scripts/consolidate_advisor.py --no-llm
python3 hybrid-search/hybrid_search.py index --yes   # refresh the search index

# Conflict arbitration (batch, after indexing; dry-run first):
#   emit candidate facts as JSONL, review the dry-run, then --apply
python3 hybrid-search/conflict_resolver.py arbitrate facts.jsonl           # analyse
python3 hybrid-search/conflict_resolver.py arbitrate facts.jsonl --apply --force

# Weekly health check (Monday):
python3 scripts/memory_health.py --quick
python3 scripts/ontology_compact.py

# Monthly cold-storage compaction (terminal facts out of the hot index):
python3 hybrid-search/compact.py --dry-run
python3 hybrid-search/compact.py --apply --min-age-days 30

# Monthly deep check (manual):
python3 scripts/memory_health.py --deep
```

## Design Principles

1. **Local by default** — no cloud account, no paid dependency. The single cloud-capable path is `trace_extractor.py` and it is opt-in via `OLLAMA_API_KEY`, disclosed on every run, and cancellable with `TRACE_LLM_LOCAL_ONLY=1`
2. **Composable** — each script is standalone, can run independently
3. **Safe by default** — dry-run available for all analysis scripts; `memory-health.py` is read-only by default. Some nightly cron commands modify files by default (archive, scores, consolidation report). Review cron commands before deploying.
4. **Human-in-the-loop** — consolidation suggestions, not auto-merge
5. **Pipeline-friendly** — scripts chain naturally, outputs feed inputs

## License

MIT — free to use, modify, and share.

## Acknowledgments

- [OpenClaw](https://github.com/openclaw/openclaw) — the agent framework this was built for

## Security Notes

- 🔒 **v2.1.4 — allowlist/index agreement, both directions**: v2.1.3 declared `TOOLS.md` in `ALLOWED_SCAN_FILES` even though `collect_all_files()` only indexes it when present — advertising a file that was never read. Optional root files are now declared only when they exist on disk, so the allowlist is neither narrower nor wider than what the indexer actually scans.
- 🔒 **v2.1.3 — runtime confinement, read-only correctness**: the `--workspace` flag no longer bypasses the confinement guard (`validate_paths()` re-runs after the rebind in `auto_archive.py` and `consolidate_advisor.py`); `memory-health.py` passes `--dry-run` to the trace extractor so a passive health check stops appending to the ontology graph; `ALLOWED_SCAN_FILES` declares the root config files the indexer legitimately reads, so the documented scan scope and the actual scan scope agree; `openclaw` subprocesses use a resolved absolute binary instead of trusting `$PATH`.
- 🔒 **v2.1.3 — scanner false positives documented**: "credential access" alerts on the secret deny-lists and "unsafe defaults" alerts on this file's own changelog prose are triaged in [`docs/SECURITY-AUDIT-NOTES.md`](docs/SECURITY-AUDIT-NOTES.md). Do not re-report them.
- 🔒 **v2.1.2 — no attacker-controllable import path**: `hybrid-search/hybrid_search.py` no longer inserts a `/tmp` directory at the head of `sys.path`. A world-writable directory in first position lets any local process shadow a module and get code executed on import. `sqlite_vec` is now imported from the active environment, with an actionable `ImportError` when it is missing (`pip install sqlite-vec`).
- 🔒 **v2.1.2 — symlinks refused, resolved paths confined**: indexing and scanning validate paths through `safe_resolve()` / `is_safe_memory_file()`, which refuse symlinks outright, normalise the path with `realpath()` (so `..` cannot escape), confine it to the allowed scan directory, and match secret patterns against the **resolved** path — a symlink with an innocuous name cannot smuggle `~/.ssh/id_rsa` into the vector index. `--dir` arguments outside scope are rejected before any file is listed.
- 🔒 **v2.1.2 — secret patterns extended**: added `.ssh`, `.aws`, `.config/google`, `id_rsa`, `id_ed25519`, `.pem`, `.key` to the skip list.
- ⚠️ **`memory-health.py` is READ-ONLY by default**: No files, SVG charts, or JSON reports are written to disk without `--output-dir <path>`. `check_drift()` does not auto-create the results directory.
- ⚠️ **`--fix` mode is destructive**: `memory-health.py --fix` moves daily notes to `archive/` and rewrites ontology. Requires interactive confirmation or `--force` flag. Creates timestamped backups in `memory/backup/` before modifying.
- ⚠️ **`--force` flag**: Skips confirmation prompts on destructive operations. Only use in trusted automation with backups in place.
- ⚠️ **`--apply-promotions` modifies MEMORY.md**: `consolidate_advisor.py --apply-promotions` appends entries to MEMORY.md. Requires interactive confirmation or `--force` flag.
- ⚠️ **Nightly cron modifies files by default**: `auto_archive.py` moves files, `scoring.py` writes `scores.json`, `consolidate_advisor.py` writes `consolidation_report.json`. Review cron commands before deploying.
- ⚠️ **OLLAMA_URL restricted to localhost**: LLM calls send memory text to Ollama. URL validated to be `localhost`, `127.0.0.1`, or `::1` only — no remote hosts.
- ⚠️ **Memory and session content IS transmitted to an LLM** (`trace_extractor.py`): extraction sends an excerpt of daily notes (and, with `--session-file`, session transcript text) to a language model. The **primary transport is Ollama cloud** (`https://ollama.com`) when an API key is configured — **content leaves this machine**. The local fallback is Ollama at `127.0.0.1:11434`, which keeps content on the machine. Set **`TRACE_LLM_LOCAL_ONLY=1`** to refuse every cloud call and force local-only operation. The destination is printed on each run (`[Security] ⚠️ CLOUD TRANSMISSION: …`).
- ⚠️ **PII sanitization before LLM calls is best-effort, not a guarantee**: `trace_extractor.py` and `consolidate_advisor.py` sanitize text with `sanitize_pii()` — regex-based removal of API keys, tokens, JWTs, emails, passwords, PEM keys, French phone numbers and long opaque blobs — before any LLM submission. Regex scrubbing cannot catch every secret in an arbitrary format. **The transport decision is the primary control, not the filter.**
- ⚠️ **Session transcripts are opt-in only**: `trace-extractor.py` no longer scans `~/.openclaw/agents/` globally. Use `--session-file <path>` to explicitly provide a single transcript file.
- ⚠️ **`scores.json` stores hashes, not raw text**: `scoring.py` replaces note text with SHA256 hashes (first 16 chars) in all JSON output. File permissions set to `0o600`.
- ⚠️ **Subprocess calls use fixed argument lists**: All `subprocess.run` calls use hardcoded `[sys.executable, ...]` argument lists — no environment variable injection. Script paths validated with `Path.resolve().is_relative_to(WORKSPACE)`.
- ⚠️ **Scope confinement**: All scripts restrict file scanning to `WORKSPACE/memory/`. No parent traversal (`../`) or sibling skill enumeration (`skills/*/SKILL.md`). Paths validated with `Path.resolve().is_relative_to(WORKSPACE)`.
- ⚠️ **Personal files excluded from search index**: `hybrid_search.py` does not index `USER.md`, `IDENTITY.md`, `AGENTS.md`, `SOUL.md`, `HEARTBEAT.md` — only `MEMORY.md`, `TOOLS.md`, and self `SKILL.md` are indexed.
- ⚠️ **No PII in test fixtures**: `run_tests.py` uses anonymized query terms (`project_alpha`, `sample_note_01`) — no real project names, personal names, or sensitive references.
- ⚠️ **Secret file filtering**: `scoring.py` skips files matching `.secrets/`, `*.env`, `credentials*`, `*token*`, `*password*`, `.git/`.
- ⚠️ **Hybrid search consent warnings**: `hybrid_search.py index` displays a consent warning before batch embedding. Use `--yes` to skip in automation. `add` prints a one-line notice (use `--quiet` to suppress).
- ⚠️ **`EXTRACTION_PROMPT` excludes secrets**: The LLM extraction prompt explicitly instructs the model to never extract credentials, API keys, tokens, passwords, personal data, or session IDs.