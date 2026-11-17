# Changelog — OpenClaw Memory Toolkit

## v3.6.1 → v3.2.1 — Consolidated release notes (2026-10-05 → 2026-10-06)

> Bloc fusionné pour la publication ClawHub, du `v3.2.1` à la dernière version `v3.6.1`.
> Ordre anti-chronologique (le plus récent en tête), comme dans le CHANGELOG officiel.

---

## v3.6.1 — Arbiter follows the operator's real default (2026-10-06)

Follow-up to v3.6.0. That release restored conflict arbitration but still listed
`glm-5.2:cloud` first in `PREFERRED_MODELS` — a name inherited from the v2.2.0
hard-code, not a deliberate choice. It is installed on the daemon (so the fix
worked), but it is not the model this deployment actually runs on.

### Changed
- **`PREFERRED_MODELS` now follows the operator's real default**, `deepseek-v4-pro:cloud`
  (the configured `agents.defaults.compaction.model`), ahead of
  `deepseek-v4.1-flash:cloud`, `glm-5.2:cloud` and the offline `qwen2.5:7b`. Both
  `conflict_resolver` and `consolidate_advisor` are aligned.
- An explicit `CONFLICT_LLM_MODEL` / `TRACE_LLM_MODEL` / `OLLAMA_MODEL` still
  overrides the list, so pinning a model stays a visible, one-line decision.

### Verified
- `deepseek-v4-pro:cloud` returns `CONTRADICTION` (confidence 0.85) with a correct
  rationale on the same backup-broken/repaired probe that v3.6.0 used — the model
  swap does not weaken the arbiter.
- Both modules resolve to `deepseek-v4-pro:cloud` on this host.

## v3.6.0 — Conflict arbitration was dead on arrival (2026-10-06)

Fix release. Closes the finding that the `superseded` / `disputed` lifecycle paths
had **never executed once**. The cause was not the subject fidelity work of v3.5.0
nor the source echo guard: it was a missing model tag.

### Fixed
- **The arbiter asked Ollama for a model that does not exist.** `conflict_resolver`
  sent the bare name `glm-5.2`, while the daemon serves `glm-5.2:cloud`. Ollama
  answered **HTTP 404**, `classify_relation()` fell through to the conservative
  heuristic, and *every* fact came back `COMPATIBLE / no confident relation detected`.
  Conflict arbitration had therefore never fired: `superseded` and `disputed` were
  unreachable code paths. Verified against a real contradiction (backup broken →
  repaired): the LLM now returns `CONTRADICTION` with a correct rationale, and
  `--apply` writes `status=superseded` + the `superseded_by` link.
- **`consolidate_advisor.py` carried the identical defect** (`OLLAMA_MODEL` default
  `"glm-5.2"`), so the advisor was silently producing nothing for the same reason.
  Both modules now resolve their model the same way.

### Changed
- **Model resolution is no longer hard-coded.** A hard-coded name — even one with
  the correct tag — rots on the next model swap. Both modules now resolve against
  the models the daemon actually serves (`GET /api/tags`): an explicit
  `CONFLICT_LLM_MODEL` / `TRACE_LLM_MODEL` / `OLLAMA_MODEL` still wins, otherwise
  the first served model from a preference list is used, and an unreachable daemon
  falls back to a tagged preference instead of crashing or sending a bare name.
- **New regression test `hybrid-search/test_model_resolution.py`** pins the three
  behaviours (explicit env wins / resolves to a served model / offline fallback is
  tagged). Wired into `scripts/sync-skill.sh` and the `release.sh check` gate.
- **Source filter (M4 follow-up):** trivially short user turns (`go`, `ok`, `top`, …)
  are skipped by the trace extractor instead of being mined for durable facts — the
  76-turn dry-run contained 18% such turns feeding ~80% operational noise.

### Verified
- Real contradiction on a DB copy: `[contradiction] Le backup nightly est repare`
  → `--apply` → `id=5134 status=superseded superseded_by=5135`.
- Non-contradictions still classified `COMPATIBLE` (Kavita `0.9.0 → 0.9.1.4`; Dovato
  morning vs evening "plus le matin") — the arbiter discriminates, it does not cry
  conflict.
- `test_model_resolution.py`: 3/3 hold. `test_loopback_guard.py`: all guards hold
  (run under the skill venv, which has `sqlite_vec`).

## v3.5.0 — Subject fidelity (M4) + source echo guard (2026-10-06)

Fix release. Closes the M4 audit finding — the one that made conflict arbitration
structurally unable to fire. Three independent defects, one shared root: facts
reached the ledger with a subject that did not discriminate, so the resolver's
"is this the same entity?" test could never return a confident match.

### Fixed
- **Multi-word subjects were truncated to their first word** (`auto_capture._normalise_facts`,
  mirrored in the new `trace_extractor._norm_subject`). `'\w'` includes `_`, so
  `re.split(r"[^\w]+", "kavita_home")` yielded a SINGLE token, grounding failed,
  and the fallback took the fact's first substantial word. `kavita_home` became
  `kavita`, `backup_cron` became `backup` — so `kavita_home` and `kavita_index`
  (different entities) collided under one key. Grounding now compares against the
  tokenised text and splits on underscore too.
- **`trace_extractor.py` produced no subject at all.** Its prompt never requested
  one and its writer never emitted one, so every trace item reached the ledger as
  `subject=NULL`. The prompt now requires a grounded `subject` per item, and the
  writer emits it as `[subject:key]` on the note line for the downstream indexer.
- **Machine-generated assistant turns were mined for user facts** (echo guard).
  The only gate was `should_capture(user_msg)`; an assistant turn carrying a tool
  completion (`... executed from ...`) or a cron report (`Summary: {'added': 0, ...}`)
  was handed to the extractor and returned as a "durable fact". `assistant_turn_is_echo()`
  now drops such turns — the user half is kept, the machine half is discarded.

### Verified
- Echo guard: 8/8 cases (tool logs, cron summaries, `=== END ===` markers gated;
  real conversational turns kept).
- Subject normalisation: `kavita_home`/`backup_cron`/`ubuntu_24_04` keep their full
  key; v3.3 anti-hallucination behaviour (`Serveur Prod` → `serveur`) preserved.

### Notes
- `--apply` remains gated behind a real dialogued conflict batch: the
  `superseded`/`disputed` paths are still unproven on live data.

## v3.4.0 — Point-in-Time Retrieval (`--as-of`) (2026-10-05)

Feature release. Turns the fact-lifecycle ledger into a time machine: the search
can now reconstruct the exact cognitive state the agent had **on a past date**,
not just what it believes today. In PLM terms, this is the step from a single
"As-Maintained" configuration to a retrievable "As-Built" baseline. Born from
the operator's observation (2026-10-05) that the v3.3 ledger — which marks rows
`superseded` instead of deleting them — already held the history; what was
missing was a timestamp for *when* a fact stopped being current.

### Added
- **`superseded_at` column** (`schema.sql`). The ISO timestamp at which a row
  STOPPED being active (`NULL` while it is). This is the axis the earlier schema
  lacked: `valid_from` records when the fact became *true in the world*, while
  `superseded_at` records the *lifecycle of the row* — and `updated_at` cannot
  serve, because a REDUNDANT confirmation rewrites it without ending anything.
  Without a dedicated column, point-in-time retrieval is impossible to express
  correctly.
- **`--as-of YYYY-MM-DD`** on `query`, `search` and `context`. Reconstructs the
  facts visible on that date instead of the current set. A bare date means *end
  of that day* (`2026-07-01` → `T23:59:59`), so a row created at 10:00 on that
  day is visible; a full timestamp is used verbatim. Verified against a
  MySQL→PostgreSQL switch: the pre-switch fact is returned for a date before it
  and the successor for a date after, with no overlap.
- **`_as_of_clause()`** — one helper builds the visibility predicate shared by
  the lexical and vector paths, so both halves of the hybrid search agree on
  what "visible on date D" means.

### Changed
- **`ensure_lifecycle_columns()`** now also adds `superseded_at` (and its index)
  to an older DB, so the migration is idempotent for existing installations.
- **`apply_resolution()` and `resolve`/`--confirm`/`--reject`** stamp
  `superseded_at` at each `active → superseded` transition, inside the existing
  atomic transaction (C2).
- **`search_lexical()` / `search_vector()` / `search_hybrid()`** take an optional
  `as_of`; default (`None`) behaviour is byte-for-byte the previous "active only"
  query — verified by a regression run against the live database.

### Data maintenance (real database, 2026-10-05)
- **3 475 `superseded` rows backfilled** with
  `superseded_at = COALESCE(updated_at, created_at)`. Backup taken and
  `integrity_check` verified before the write; post-run `foreign_key_check`
  clean; zero active rows carry a `superseded_at`.

## v3.3.0 — Referential Integrity, Transactional Writes, Ontology→DB Sync (2026-10-05)

Hardening release. An audit of the fact-lifecycle layer found that the schema
*declared* a state machine (status, confidence, superseded_by) the engine never
enforced, that the write paths were not atomic, and that subject arbitration was
dead in practice (100 % of indexed facts had `subject = NULL`). Every defect is
fixed at the source and verified against the real database.

### Fixed
- **Schema now enforces what it declared (C1).** `status` carries a `CHECK
  (status IN ('active','superseded','disputed'))`, `confidence` a range `CHECK`,
  and `superseded_by` a `FOREIGN KEY … ON DELETE SET NULL`.
- **`conflict_resolver.apply_resolution()` is atomic (C2).** The whole resolution
  is now one `BEGIN IMMEDIATE` … `COMMIT` with rollback.
- **Concurrent access is safe (C3).** Both connection paths now set
  `busy_timeout=5000`, `journal_mode=WAL` and `foreign_keys=ON`.
- **`add_memory()` writes the hot row and its vector atomically (C4).**
- **`compact.py` never archives a still-referenced fact (M2).**
- **`ontology_compact.py` drops orphan relations (M3).**

### Added
- **`subject` is finally writable and populated (M4).** Arbitrable fact categories
  now sit at **100 % subject coverage**.
- **Ontology → DB synchronisation.** Every entity that leaves the reference
  nomenclature has its facts marked `superseded` in the same run.
- **`migrate_subject.py` / `migrate_ontology_subjects.py`** — one-shot, idempotent
  backfill/audit tools.

## v3.2.1 — Ontology Reindex, Number-Safe Splitting, Local Model Bump (2026-10-05)

Maintenance release. Two defects found during the first live Auto-Capture
session, both fixed and verified against the real database.

### Fixed
- **Nested-schema ontology indexing.** `index_jsonl_file()` read `name`/`type` at
  the JSON root, but ontology lines are nested — every graph node was indexed as
  the literal string `" ()"`: **2 786 junk rows, 69 % of the database**.
- **Number-safe punctuation split.** `extract_atomic()` split on every period:
  `Ubuntu 24.04` became `Ubuntu 24` + `04`. A period now splits only when not
  sandwiched between digits (`(?<![0-9])\.(?![0-9])`).

### Changed
- **Default extraction model: `qwen2.5:3b` → `qwen2.5:7b`** (still local, loopback-only).
- **Database maintenance:** 2 786 empty ontology rows moved to `superseded`
  (reversible) and the 898 clean nodes re-indexed.

## v3.2.0 — Auto-Capture: Session Dialogue → Arbitrated Facts (2026-10-04)

Feature release. Adds the write-behind half of the autonomous memory loop: a
post-turn pipeline that reads session dialogue, extracts atomic durable facts
with a local LLM, and arbitrates them against existing memory.

### Added
- **`hybrid-search/auto_capture.py`** — post-turn fact extraction.
- **`hybrid-search/transcript_adapter.py`** — reads the OpenClaw per-agent session
  store (`session_transcript_fts`), snapshot-first, read-only, secret-redacting.
- **`--no-split`** flag on `conflict_resolver.py` `check`/`arbitrate`.
