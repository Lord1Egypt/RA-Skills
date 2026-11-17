# Changelog — OpenClaw Memory Toolkit

All notable changes to the OpenClaw Memory Toolkit skill.

## v4.0.6 — Read-only memory access for the agent (2026-10-13)

### Added

- **`mcp-server.py`** — stdio MCP server exposing `memory_query`, `memory_facts`
  and `memory_stats` over the local hybrid search index. Read-only.
- **`memory-audit.py`** — read-only memory state report (`--json`, `--db`),
  SQLite opened with `mode=ro`.
- **`memory-dedup.py`** — content-hash deduplication, dry-run by default,
  marks duplicates with `superseded_by` + `status='superseded'` (never `DELETE`),
  guarded by `--max-rows`.

## v4.0.5 — Dates are validated before they reach the graph (2026-10-11)

### Real fix

**The extraction pipeline trusted the LLM's date and folded it into ids.**
`stable_id('tl', what, today)` concatenated the string blindly, and the
decision write took `dec.get('date')` verbatim. A model asked for `YYYY-MM-DD`
still returns `2026-05-31-0913` (date + time), `2026-05-26-roadmap-updates`
(date + free text) or `2026-04` (month only).

Blind concatenation produced the unmatchable nodes `day_202605310913` /
`day_20260526roadmapupdates` / `day_202604` — targets no edge can ever match.
That is the **dangling-target** defect the 10/10 backfill had to repair by hand
(158 edge targets pointing at nodes that did not exist). It is now fixed at
the source, so it cannot recur.

### Change

`normalize_date()` is the single gate every date passes before it is written
or folded into an id:

- **Parse first, build second.** A real calendar date is required —
  `datetime()` rejects `2026-13-01` and `2026-02-30`; a regex alone would not.
- A leading `YYYY-MM-DD` in a longer string is kept
  (`2026-05-31-0913` → `2026-05-31`), the trailing noise is dropped.
- Anything else falls back — the honest answer for "undated decision" is today,
  not a fabricated date.

It gates both the id builder (`stable_id`) and the decision-date write. 12 unit
cases cover the boundary.

### Note on the source of truth

`trace_extractor.py` is the one skill file whose **live copy leads**: the fix
was written against the running skill then ported live → repo. `release.sh`
section 2 asserts the two copies are identical.

## v4.0.4 — No decision enters the ontology as an orphan (2026-10-10)

### Real fix

**M6: every extracted decision now carries an edge.** The ontology held
**889 orphan entities out of 928, with only 34 relations** — a list of
disconnected blocks, not a graph. Root cause: `trace_extractor` created
Decision / TimelineEvent nodes with no relation at all.

Two changes, both at the source:

- The extraction prompt now REQUIRES a `related_to` on every item — the id of an
  existing entity it attaches to, grounded in the note text, never invented.
  When nothing fits, the item anchors to the catch-all root `daily_notes`.
- `write_ontology_entities()` appends a `relate` fact for every decision it
  writes, resolving the root via `_norm_related_to()` (grounded anchors only)
  then `_root_id_for()`. An invented anchor is refused, not wired.

Nothing is deleted: the graph stays append-only, and every auto-link is
reversible.

### New guard

`hybrid-search/test_orphan_link.py`, wired into `scripts/release.sh`. It asserts
both directions: a grounded anchor links, an ungrounded decision still links to
`daily_notes`, and an INVENTED anchor is refused. A gate that accepted invented
roots would silently wire the graph wrong.

## v4.0.3 — MEMORY.md can no longer grow unbounded (2026-10-10)

### Real fix

**Size guard in `consolidate_advisor.apply_promotions()`.** MEMORY.md is injected
into every main-session context and has a hard 5 KB budget, but the promotion
path appended entries without ever checking the running total. That is how the
file silently reached **19.6 KB (3.8x the limit)** before a manual audit caught
it. The writer now projects the post-write size and **refuses to write** when it
would exceed `MEMORY_MAX_SIZE` (env-overridable, default 5000):

```
❌ Size guard: refusing to write — projected MEMORY.md 18689 bytes
   > limit 5000 bytes (+13710 would be added).
   Trim/archive MEMORY.md first, or promote fewer entries.
```

The file is left byte-for-byte untouched on refusal. Promotions are suggestions,
not obligations: losing an overflow is strictly better than paying for it in
every future session's context.

Verified by direct test: a 2-entry lot applies, a 20-entry lot is refused and
the file stays intact.

## v4.0.2 — Ontology health check no longer cries wolf (2026-10-10)

### Real fix

**`memory-health.py` parser was blind to `op=state`.** The ontology graph is an
append-only log whose dominant record is now `op=state` (879 of 964 lines in the
current graph); `create`/`upsert` are the older forms. `check_ontology()` counted
an entity only for `op in ("create", "upsert")`, so it saw **50 entities** while
`ontology_compact.py`, which replays the full log, saw **927**. The 34 `relate`
records pointed at the real entities, so the check reported **68 orphan
relations on every run** — all of them false.

The parser now accepts `state` as an entity-bearing op. Both tools agree:

```
before:  50 entities,  68 orphan relations (🟡)
after : 928 entities,   0 orphan relations (🟢)
```

No false-positive suppression: the orphan count is still computed and still
reported when real orphan relations exist. Only the parse was wrong.

### Notes

- Discovered while triaging a health report (10/10): the "68 orphan relations"
  warning was the health check disagreeing with the compactor, not real drift.
- `ontology_compact.py` needed no change — it was already correct.

## v4.0.1 — Security hardening + static-analysis false positives (2026-10-10)

### Real fixes

**A. Loopback guard on `llm_resolution.py` (SSRF gap).** The v4.0 resolver read
`OLLAMA_URL` straight from the environment, while every other module routes it
through `get_safe_ollama_url()`. It was even *exempted* from the static scan in
`test_loopback_guard.py` (`if fn == "llm_resolution.py": continue`). A crafted
environment could therefore point the safety-net endpoint at a remote host. It
now uses the same loopback guard, and the exemption is removed —
`llm_resolution` is covered by the guard test like the other modules.

**B. Cloud transport is now opt-in.** `trace_extractor.py` used to send memory
and session excerpts to `ollama.com` whenever an API key was *present*. A memory
skill that ships notes off-machine just because a key happens to exist is a
consent surprise. Cloud is now used only when the operator explicitly sets
`TRACE_LLM_ALLOW_CLOUD=1` **in addition** to the key; otherwise extraction stays
on `127.0.0.1:11434`. `TRACE_LLM_LOCAL_ONLY=1` remains a hard local-only lock.
The disclosure banner reflects the real transport in all cases.

### Clearing a scanner false positive

ClawHub's static analysis flagged
`hybrid-search/test_ontology_key_parity.py:61` as
`suspicious.dynamic_code_execution` (critical). It is a false positive: the
flagged call is the standard Python import machinery loading a **fixed, literal**
path in the same repository (`migrate_ontology_subjects.py`) — no network, no
user input, no environment variable, no argv reaches it.

The loader was **not** removed to silence the scanner: the test deliberately
imports the real migrator module so it tracks the real code instead of a stale
copy. An inline explanation and a `noqa` marker were added instead.

Also ignores `hybrid-search/FULL_INDEX_REPORT.md` (a run artifact, like
`test_results.json`).

### Known false positives (documented, not fixed)

Further SkillSpector findings are scanner artefacts and are recorded here so a
future review does not waste time re-triaging them:

- **"Tainted flow … credential exfiltration" (Critical, ×5).** The flagged
  values are `OLLAMA_URL`, `GEN_TIMEOUT` and a `Content-Type` header — not
  secrets. The one genuine nugget was the missing loopback guard on
  `llm_resolution.py` (fixed above).
- **"Anti-Refusal Statement" (CHANGELOG).** Prose describing the
  `resolve --confirm` feature; the scanner matched the words "supersedes any
  rival claim". Not an instruction.
- **"Credential Access" (CHANGELOG, ×4).** The quoted text is the *refusal* list
  (`/etc/passwd`, `.secrets/*`, `SOUL.md` … are rejected). The scanner matched the
  words, not the meaning. This is a security *proof* read as a crime.
- **"Referenced artifact was not completely inspected" (SKILL.md).** The skill
  documents modules (e.g. `hybrid_search.py`) that live outside the scanned
  bundle; the scanner cannot open what was not shipped.

## v4.0 — One resolver, one truth (2026-10-10)

**Breaking contract change.** Model selection is no longer copied into each
script: it is *resolved* once, at runtime, from the gateway configuration. Every
caller now goes through a single module, `hybrid-search/llm_resolution.py`, so a
catalogue rotation or a config change propagates everywhere at once instead of
silently breaking one script at a time.

### Why this release exists

v3.6.0 and v3.6.1 each fixed a *symptom*: a hard-coded model name that no longer
matched what the Ollama daemon served (`glm-5.2` vs `glm-5.2:cloud`). The fix
worked, but the *pattern* that caused it survived — model names were still
recopied in `PREFERRED_MODELS` lists, in `auto_capture.py`, and in the local
`trace-extractor` fallback. The next catalogue rotation would have re-broken it.
v4.0 removes the pattern.

### Added

- **`hybrid-search/llm_resolution.py`** — the single source of truth for the
effective LLM model. Resolution chain, in order:
  1. an explicit `*_LLM_MODEL` / `OLLAMA_MODEL` env var (**visible and logged**,
     never silent — the escape hatch that saved v3.6.0/v3.6.1 is kept);
  2. the gateway default, `agents.defaults.model.primary` from `openclaw.json`;
  3. the configured fallback, `agents.defaults.model.fallbacks[0]`;
  4. the local safety net (`qwen2.5:7b`), **presence-checked before use**.
  Exposes `resolve_llm_model()` and `explain_resolution() -> {model, source, chain}`
  for logging and tests. `@lru_cache`d, so a run resolves once.
- **No-silent-failure invariant (spec §6.1).** A missing local safety model
  raises a clear error instead of letting Ollama start a synchronous multi-GB
  pull that would hang an unattended nightly run.
- **`hybrid-search/test_model_resolution.py` (extended).** Pins the whole
  precedence chain (explicit > gateway:primary > gateway:fallback > local safety),
  the served-model guarantee, and the raise-on-missing-safety-model invariant.
- **`hybrid-search/test_extract_atomic.py` (new).** Covers `extract_atomic()`,
  a gap flagged in the spec: number protection (`Ubuntu 24.04`, `3.14`, `100%`,
  `12,5 %`) *and* real clause splitting (semicolons, conjunctions, sentence
  boundaries).
- **`hybrid-search/test_ontology_key_parity.py` (new).** Pins indexer/migrator
  display-key parity. Drift is a failure; a display-key collision (two ids, one
  key) is reported as data, not drift. It caught a real second issue on first run.

### Changed

- **4 callers migrated to the shared module**, no more hard-coded names:
  `consolidate_advisor.py`, `hybrid-search/auto_capture.py`,
  `hybrid-search/conflict_resolver.py`, and `trace_extractor.py` (which also
  serves the local `trace-extractor` fallback). `qwen2.5:7b` now survives *only*
  as the last link of the shared chain.
- **`PREFERRED_MODELS` lists are gone** from the arbiters — the chain replaces
  them.
- **`resolve_llm_model()` reads the gateway config** (`agents.defaults.model.*`),
  so the effective model follows the operator's real default instead of a copy.
- **`scripts/sync-skill.sh` ships `hybrid-search/llm_resolution.py`** and the new
  test files to the installed skill. (`llm_resolution.py` had been missing from
  its `FILES` list: post-sync, each caller's `try/except ImportError` fallback
  would have silently restored the *old* behaviour — the exact "silent failure"
  this release removes.)
- **`trace_extractor.py` imports the module via multi-candidate paths**, so it
  finds `llm_resolution` from both the repo and the installed skill.

### Fixed

- **Destructive detection bug in `migrate_ontology_subjects.py` (M4-B).**
  `load_graph()` rebuilt the display key as `name or type`, but the indexer
  (`hybrid_search.index_jsonl_file`) uses `name or entity.id or type`.
  `Decision` / `TimelineEvent` nodes carry no `name`, so the migrator produced
  `' (Decision)'`, matched nothing, and reported **2826 live facts as ghosts**.
  A single `--apply` would have marked **2406 valid facts `superseded`** and
  pulled them out of active retrieval. Fix: mirror the indexer exactly (add the
  id fallback). After the fix: survivors **3871** / ghosts **0** (was 1045 / 2826).

### Housekeeping

- `migrate_subject.py` / `migrate_ontology_subjects.py` marked **APPLIED**
  (one-shot, already run in production). Kept as re-auditable tools — a dry-run
  still answers "is anything left to migrate?" in seconds. Not merged.
- `docs/CHANGELOG-UNRELEASED-V3.6.1.md` was a superseded draft (content fully
  present in this CHANGELOG, verified line by line) → renamed `_ARCHIVED-*`.
- Dead orphan log `memory/nightly-extraction.log` (frozen 2026-07-22) archived to
  `.archive/retired-scripts/nightly-extraction.log.mort-2026-07-23`.

### Verified

- `scripts/release.sh check` green: syntax, frontmatter, loopback guard, and all
  five test suites pass.
- Both arbiters resolve to a model the local daemon actually serves.
- Migrator dry-run on the live DB: `survivors 3871 / ghosts 0`.

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
  correctly: the operator's first SQL draft referenced `superseded_at` before it
  existed, which is what surfaced the gap.
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
  atomic transaction (C2). The column is maintained by the real resolution path,
  not only by a one-off backfill.
- **`search_lexical()` / `search_vector()` / `search_hybrid()`** take an optional
  `as_of`; default (`None`) behaviour is byte-for-byte the previous "active only"
  query — verified by a regression run against the live database.

### Data maintenance (real database, 2026-10-05)
- **3 475 `superseded` rows backfilled** with
  `superseded_at = COALESCE(updated_at, created_at)`. Backup taken and
  `integrity_check` verified before the write; post-run `foreign_key_check`
  clean; zero active rows carry a `superseded_at`.
- _Note recorded for a future release:_ `--as-of` cannot reconstruct a state
  older than the first indexing date (`created_at` floor, here 2026-10-03), since
  no row predates it. Historical *world* time belongs to `valid_from`, a separate
  axis, not to row lifecycle.

## v3.3.0 — Referential Integrity, Transactional Writes, Ontology→DB Sync (2026-10-05)

Hardening release. An audit of the fact-lifecycle layer found that the schema
*declared* a state machine (status, confidence, superseded_by) the engine never
enforced, that the write paths were not atomic, and that subject arbitration was
dead in practice (100 % of indexed facts had `subject = NULL`). Every defect is
fixed at the source and verified against the real database.

### Fixed
- **Schema now enforces what it declared (C1).** `status` carries a `CHECK
  (status IN ('active','superseded','disputed'))`, `confidence` a range `CHECK`,
  and `superseded_by` a `FOREIGN KEY … ON DELETE SET NULL`. Previously an
  out-of-range status or a dangling referent was silently accepted. Verified by
  negative tests: invalid status, `confidence = 5` and a broken referent are all
  rejected by the engine.
- **`conflict_resolver.apply_resolution()` is atomic (C2).** It ran its UPDATE
  (supersede) and its INSERT (successor) as separate statements; a crash between
  them left a fact superseded by nothing — silently lost. The whole resolution is
  now one `BEGIN IMMEDIATE` … `COMMIT` with rollback.
- **Concurrent access is safe (C3).** Both connection paths (`HybridMemoryStore`
  and the resolver's `connect()`) now set `busy_timeout=5000`, `journal_mode=WAL`
  and `foreign_keys=ON`. The async capture hook, the resolver and RRF reads can
  now run in parallel instead of colliding on a locked DB.
- **`add_memory()` writes the hot row and its vector atomically (C4).** A failure
  between the two INSERTs used to leave a fact with no embedding — invisible to
  vector search, still visible to FTS5 (silent index drift). Both INSERTs now
  share one transaction and roll back together.
- **`compact.py` never archives a still-referenced fact (M2).** A terminal row
  that another hot row points at via `superseded_by` is now held back, so
  archiving cannot dangle a live reference. Verified on a `1←2←3` chain.
- **`ontology_compact.py` drops orphan relations (M3).** Relations touching a
  superseded/absent entity used to survive compaction as orphan edges. They are
  now dropped and reported (`relations: N kept, M orphan(s) dropped`).

### Added
- **`subject` is finally writable and populated (M4).** The column existed since
  v2.2.0 but no write path could set it, so **100 % of facts had `subject = NULL`**
  and conflict arbitration fell back to brittle lexical overlap. `add_memory()`
  now accepts `subject`; the indexer derives a **deterministic, never-invented**
  key from the source (`derive_subject()`), and ontology nodes use their own
  entity id. Arbitrable fact categories now sit at **100 % subject coverage**
  (daily notes and archives stay subjectless by design — they are episodic logs,
  not atomic assertions).
- **Ontology → DB synchronisation (v3.3 causality link).** `ontology_compact.py`
  now mirrors a compaction into the hot DB: every entity that leaves the reference
  nomenclature (`graph.jsonl`) has its facts marked `superseded` in the same run.
  The set is the **diff between the pre- and post-compaction live sets**, so
  entities that simply vanish are caught — not only explicit `supersede` ops.
  Best-effort: a missing/locked DB never aborts a successful graph compaction.
- **`migrate_subject.py` / `migrate_ontology_subjects.py`** — one-shot, idempotent
  backfill/audit tools, kept in the repo (not installed in the skill). They are
  what surfaced and repaired the two M4 defects below.
- **`docs/AUDIT-v3.2.md`** — the reference audit that catalogued C1–C4, M2–M4.

### Changed
- **Auto-capture subject anti-hallucination relaxed (M4).** The old rule dropped
  any subject whose tokens did not *all* appear in the fact (`« Serveur Prod »` →
  tokens `serveur`,`prod`; only `serveur` grounded, so the whole key was thrown
  away). It now keeps the subject if **any** token is grounded (preferring the
  grounded token) and falls back to the fact's first substantial word. A subject
  that grounds nothing is still dropped.

### Data maintenance (real database, 2026-10-05)
- **898 ontology rows relabelled.** The filename-derived migration had collapsed
  898 distinct entities under one generic `subject = 'graph'`, which would have
  made arbitration fetch an absurd mix. Re-mapped to each entity's real id: **209
  survivors** got their live id, **689 ghosts** (entities absent from the compacted
  ontology) were moved to `superseded`, then their stale `subject` cleared.
- **Backups verified before every write** (`integrity_check: ok`), and post-run
  `foreign_key_check` clean.

## v3.2.1 — Ontology Reindex, Number-Safe Splitting, Local Model Bump (2026-10-05)

Maintenance release. Two defects found during the first live Auto-Capture
session, both fixed and verified against the real database.

### Fixed
- **`hybrid-search/hybrid_search.py` — nested-schema ontology indexing.**
  `index_jsonl_file()` read `name`/`type` at the JSON root, but ontology lines
  are nested (`{"entity": {"properties": {"name": …}, "type": …}, "op": …}`).
  Every graph node was therefore indexed as the literal string `" ()"` —
  **2 786 junk rows, 69 % of the database**, which also polluted the FTS5 and
  vector indexes. The function now reads both flat and nested schemas, falls
  back to `id`, and applies a real minimum-length guard (`len(content) <= 4`);
  the previous `if not content.strip()` check let `" ()"` through because
  `"()"` is not the empty string. A `skipped` counter is now reported.
- **`hybrid-search/conflict_resolver.py` — number-safe punctuation split.**
  `extract_atomic()` split on every period, breaking version strings and
  percentages: `Ubuntu 24.04` became `Ubuntu 24` + `04`, and `… à 100% atteint`
  lost its tail. A period now splits only when not sandwiched between digits
  (`(?<![0-9])\.(?![0-9])`), and any purely-numeric orphan fragment is
  re-attached as a safety net. Semicolons and coordinating conjunctions still
  split as before.

### Changed
- **Default extraction model: `qwen2.5:3b` → `qwen2.5:7b`** (still local).
  The 3 b model returned empty `{}` extractions in ~20 s and split version
  numbers; the 7 b model extracts whole facts in ~44 s. Loopback-only
  guarantee preserved — no cloud model is used.
- **Database maintenance:** 2 786 empty ontology rows moved to
  `superseded` (reversible, not deleted) and the 898 clean nodes re-indexed
  (`0` errors, 34 `relate` lines correctly skipped). Backup taken before the
  operation.

## v3.2.0 — Auto-Capture: Session Dialogue → Arbitrated Facts (2026-10-04)

Feature release. Adds the write-behind half of the autonomous memory loop: a
post-turn pipeline that reads session dialogue, extracts atomic durable facts
with a local LLM, and arbitrates them against existing memory (superseding or
flagging contradictions). Complementary to the existing nightly indexer, which
only archives/indexes daily notes and never arbitrates.

### Added
- **`hybrid-search/auto_capture.py`** — post-turn fact extraction. Gating
  (regex/length) skips trivial exchanges before any LLM call; a local model
  (`qwen2.5:7b` by default) returns atomic facts; results are handed to
  `conflict_resolver.py`. Guards: local-only endpoint, user-anchored extraction
  (echo-loop guard drops assistant speculation), subject anti-hallucination
  (a subject must appear in the fact text or it is dropped), `--selftest`.
- **`hybrid-search/transcript_adapter.py`** — reads the OpenClaw per-agent
  session store (`agents/<agent>/agent/openclaw-agent.sqlite`,
  `session_transcript_fts`) and emits `{user, assistant}` turns. Snapshot-first
  (WAL-aware copy; the live DB is never touched), read-only, secret-redacting.
- **`--no-split`** flag on `conflict_resolver.py` `check`/`arbitrate`: treats an
  already-atomic fact as-is, avoiding a punctuation split that broke values
  like `Ubuntu 24.04` into two malformed facts.

### Why
- Legacy `sessions/*.jsonl` transcripts stopped being written (OpenClaw migrated
  session storage to SQLite). A cron reading them would run green nightly while
  capturing nothing. The adapter reads the authoritative store the CLI itself
  uses.
- `conflict_resolver.py` had 3100 facts all `active` with no subject: the
  lifecycle/arbitration path had never been exercised. Auto-Capture feeds it.

## v3.1.1 — README Split: Contributing Moved Out (2026-10-03)

Documentation-only release. No behaviour change to any script.

### Changed
- **The "Release Pipeline" section moved from `README.md` to a new
  `CONTRIBUTING.md`.** It documents the repo → skill → GitHub → ClawHub flow, the
  release gate, and the anti-drift invariants — that is maintainer material, not
  user material. Someone installing the skill from ClawHub has nothing to do with
  our internal pipeline; the README should not make them read it.
- **`README.md` now targets users only** and keeps a one-line pointer to
  `CONTRIBUTING.md`, plus the short "MUST go through `scripts/release.sh`" warning.

### Why
Standard GitHub split: `README` = what it is / how to use it;
`CONTRIBUTING` = how to maintain and release it. Keeping the maintenance detail
out of the user-facing README makes the ClawHub listing cleaner without losing
any of the release discipline.

## v3.1.0 — Recursive Archive Scan + Nightly Index Guard (2026-10-03)

Feature release. The hybrid search index was silently blind to every archived
note filed in a sub-folder, and the nightly job could index nothing at all
without anyone noticing. Both are fixed and both now fail loudly.

### Added
- **Recursive archive scanning.** `hybrid_search.py` now scans
  `memory/archive/**/*.md` instead of `memory/archive/*.md`. The non-recursive
  glob only saw top-level files and missed every month/themed sub-folder
  (`archive/2026-07/`, `archive/2026-08/`, `april-2026/`, `june-2026/`, …):
  **174 archived notes were invisible to search**, and the DB covered 28 days
  instead of ~6 months. Sources keep their relative path
  (`archive/2026-07/2026-07-15.md`) so `delete_by_source` stays unambiguous.
- **Hard verification in the nightly job.** The job now captures the chunk count
  before and after indexing and writes one timestamped line to
  `logs/nightly-index.log` **every night, success or failure**:
  `status=<ok|ERROR> files=<n> chunks=<before>-><after> indexed_delta=<d> msg=…`.
  `status=ok` requires the indexing to have run, `chunks > 0`, and `Last indexed`
  from the current night; anything else is an explicit `ERROR`.
- **Native failure alert to Telegram** on the nightly job (after 1 error,
  1h cooldown), covering crashes/timeouts that the internal check cannot see.

### Fixed
- **The nightly job ran with an interpreter that could not index.** The job
  called `python3` (system), which does **not** have `sqlite-vec`; the extraction
  step worked but the indexing step silently wrote nothing. Job status was `ok`
  while the index stayed frozen — a silent failure that had gone unnoticed.
  Both steps now run under `skills/memory-health/.venv/bin/python`.

### Verified
- Reindex: **68 → 239 files, 1238 → 2167 chunks** (three layers aligned:
  2167 memories = 2167 FTS = 2167 vec).
- End-to-end proof: a witness note was indexed by the nightly job and retrieved
  by the search (`ZORBLAX-7729`), then removed and the orphan chunk deleted
  (2168 → 2167).
- Old `scripts/nightly-extraction.py` (last executed 2026-07-22, no remaining
  caller) retired to `.archive/retired-scripts/`.

## v3.0.3 — trace_extractor Ported From the Local Skill (2026-10-03)

Behaviour fix, ported from the installed skill copy. The skill's
`trace-extractor.py` (891 lines, written 03/10 07:07) had moved ahead of the repo
(842 lines); the repo copy was stale and is now identical.

### Fixed
- **Strict truncation salvage in `parse_llm_output()`.** When the cloud model hits
  `done_reason=length`, the response is cut mid-JSON. The parser now salvages only
  the *fully-parsed elements* that appear before the cut, dropping an incomplete
  object entirely rather than keeping an amputated value — a truncated fact is
  worse than no fact in long-term memory. It never invents content.
- **Cloud model.** `deepseek-v4-flash` returned HTTP 410 Gone; switched to
  `deepseek-v4.1-flash:cloud`.

### Verified
- The installed version is a functional superset of the repo copy (21 replaced /
  70 added lines, no repo-only content lost).
- Repo and skill converge on the same 891-line file (md5-identical).

## v3.0.2 — Security: `OLLAMA_GEN_URL` Loopback Guard (2026-10-03)

Round 8 security scan of the published v3.0.0 returned 51 findings; one was real
and is fixed here, the rest are triaged in `docs/SECURITY-AUDIT-NOTES.md` §3.

### Fixed
- **`hybrid-search/conflict_resolver.py` bypassed the loopback guard.**
  `OLLAMA_GEN_URL` was read directly from `os.environ`, skipping
  `get_safe_ollama_url()`. `classify_relation()` POSTs the content of two memory
  facts to that URL on every arbitration, so a crafted environment could redirect
  memory content to a remote host while the docstring still claimed "fixed to
  localhost at import time". Routed through the same loopback allowlist as
  `OLLAMA_URL`; a non-loopback override now raises at import.

### Verified
- `OLLAMA_GEN_URL="http://evil.example.com/api/generate"` → `ValueError: Host
  'evil.example.com' not allowed for OLLAMA_GEN_URL. Only localhost is permitted.`
- `OLLAMA_GEN_URL="http://127.0.0.1:11434/api/generate"` → imports fine.
- No other `os.environ.get("OLLAMA…")` bypass remains (grep-verified).

## v3.0.1 — SKILL.md Actually Ships the v3.0.0 Content (2026-10-03)

Documentation-only fix. v3.0.0 shipped correct code, CHANGELOG and README, but
`SKILL.md` — the file ClawHub renders and users read first — was never actually
updated. The v3.0.0 commit message claimed "SKILL/README/CHANGELOG updated"; on
`SKILL.md` the edit was a silent no-op (an identical-replacement), and it was not
re-verified before commit. The published skill therefore advertised `v2.2.0` in
its lifecycle heading and documented none of the new commands.

### Fixed
- `SKILL.md` lifecycle heading is now `v3.0.0`.
- Added the two missing Scripts entries:
  - **8. `conflict_resolver.py`** — the four-step NLI pipeline, `check` /
    `arbitrate`, `pending` (surface unresolved disputes) and `resolve --confirm`
    / `--reject [--replacement]` (only `disputed` rows eligible; `--confirm`
    supersedes rivals on the same subject).
  - **9. `compact.py`** — cold-storage compaction: `--stats`, `--dry-run`
    default, `--apply --min-age-days N`, `--restore <id>`; archive table +
    JSONL audit, hot-table DELETE so FTS5/vector indexes drop the rows; requires
    `sqlite-vec`.
- `SKILL.md` grew 343 → 394 lines.

### Process lesson
An `edit` that reports "no changes made (replacement text is identical)" is a
**failure signal for that edit**, not a success. The version marker and the new
sections are now grep-verified against the file, both locally and against the
pushed remote, before claiming the docs are updated.

## v3.0.0 — Cold Storage & Interactive Dispute Resolution (2026-10-03)

Major version: the fact lifecycle introduced below is now complete end-to-end —
facts enter, get arbitrated, get resolved by a human when ambiguous, and are
finally compacted out of the hot index when terminal. The search DB becomes a
managed store with a hot/cold boundary rather than an append-only pile.

### Added
- **`hybrid-search/compact.py`** — cold-storage compaction of terminal facts.
  `superseded` (and optionally `disputed`) rows older than `--min-age-days` are
  copied verbatim into `memories_archive` in the same SQLite file and appended to
  a dated JSONL audit under `memory/audit/`, then `DELETE`d from the hot table —
  which fires the existing triggers and removes them from FTS5 and the vector
  index. That is the actual perf win: BM25 rank space and `memories_vec` no longer
  carry dead facts. Never a hard delete of data, only a move; `--restore <id>`
  rehydrates a single archived fact.
  - Backed up first via SQLite's own `backup()` API (a `copy2` on a live DB can
    capture a torn WAL), MD5-checked before any write; `--dry-run` is the default
    and mutation requires `--apply`; a retention guard refuses to sweep rows newer
    than `--min-age-days`, and rows whose age cannot be proven are kept.
  - Requires `sqlite-vec`: the `memories_vec_ad` trigger fires on `DELETE`, so
    without the extension the move would abort mid-transaction with "no such
    module: vec0". The extension is now loaded on every connection, and the script
    refuses loudly (instead of half-archiving) when it is missing but needed.
- **Interactive dispute resolution** (`hybrid-search/conflict_resolver.py`):
  - `pending` — surfaces unresolved `disputed` facts cheaply and deterministically
    (`--json` for programmatic use), so an agent can raise the queue at the next
    relevant turn without a runtime hook. This is the tool half of "resolve at the
    next pertinent turn": the skill cannot decide relevance, but it can always
    answer "what is waiting for a human?".
  - `resolve <id> --confirm` — restores the wording to `active` **and supersedes
    any rival claim on the same subject**, so a contested pair can never both stay
    visible.
  - `resolve <id> --reject [--replacement "…"]` — supersedes the wrong wording and
    optionally inserts a corrected fact as the new `active` one, chaining
    `superseded_by`.
  - Only rows currently `disputed` are eligible; resolving an `active` or already
    `superseded` row is refused, so the command cannot rewrite lifecycle state by
    accident.

### Changed
- SKILL/README pipeline diagrams and the nightly cron block document the
  arbitration, cold-storage and dispute-resolution steps.
- Version moved to 3.0.0: this is the first release where the lifecycle is closed
  end-to-end (create → arbitrate → resolve → compact), and it introduces the
  hot/cold storage boundary — a schema/operational break worth a major bump.

### Verified (executed, not read)
- **Compaction**: a `superseded` fixture moved with `--apply --min-age-days 0` →
  hot 4→3, FTS rows 4→3, archive 1, JSONL audit written, DB backup taken. Retention
  guard: with `--min-age-days 30` on fresh rows, 0 eligible (correctly refused).
- **Restore**: `--restore <id>` moved the row back (hot 4, archive 0, FTS 4); a
  second restore refused with `not in archive` (idempotent).
- **vec0 trigger bug caught by testing**: the first `--apply` failed with "no such
  module: vec0" because the vec trigger fires on delete; fixed by loading the
  extension on every connection, with an explicit refusal path when it is absent.
- **Resolve**: `--confirm` on a disputed row restored it to `active` and superseded
  its active rival (`superseded_rivals: [7]`), leaving one active fact per subject;
  `--reject --replacement` superseded the wrong fact and inserted the correction
  with a proper `superseded_by` chain; `pending` then reported none; resolving a
  non-disputed row was refused (`id 6 is 'active', not 'disputed'`).
- Syntax validated on all modules (`ast.parse`); CLI `--help` for both new command
  surfaces inspected.

### Files Modified (5)
Added `hybrid-search/compact.py`; modified `hybrid-search/conflict_resolver.py`,
`README.md`, `SKILL.md`, `CHANGELOG.md`.

## v2.2.0 — Fact Lifecycle, Conflict Arbitration & Tagged Injection (2026-10-03)

Three improvements asked for after a review of the toolkit against a memory-engineering
spec: fact conflict lifecycle, structured context injection, and a hard token budget.
Every change is local-first and read-only by default; nothing new leaves the machine.

### Added
- **Fact lifecycle columns** (`hybrid-search/schema.sql`): `subject`, `status`
  (`active` | `superseded` | `disputed`), `confidence`, `valid_from`,
  `source_context`, `last_confirmed`, plus indexes on `status`/`subject`. The
  `superseded_by` column existed since the first schema but **was never written to
  by any code** — it is now populated by the resolver below. An older DB is
  migrated in place (idempotent `ALTER TABLE`, no data loss).
- **`hybrid-search/conflict_resolver.py`** — the four-step consistency pipeline:
  1. *atomic extraction* (`extract_atomic`) splits a compound statement into unit
     facts; 2. *targeted retrieval* (`fetch_active_facts`) pulls only `active`
     facts on the same subject, with an FTS5 lexical fallback; 3. *NLI
     classification* (`classify_relation`) asks a loopback Ollama model for
     `CONTRADICTION | REDUNDANT | COMPATIBLE` + confidence + reasoning, with a
     conservative deterministic `heuristic_relation()` fallback for offline use;
     4. *state update* (`apply_resolution`) supersedes / confirms / adds — never
     hard-deletes, always keeping the chain via `superseded_by`.
  - **Weak-signal protection**: a contradiction below `DISPUTE_CONFIDENCE_FLOOR`
    (0.6) flags the old fact `disputed` and inserts the new one, instead of
    destroying an established truth on a guess.
  - CLI: `check`, `arbitrate <jsonl>`, `lifecycle --status …`. Analysis is
    read-only; mutation requires `--apply` (`--force` in non-interactive mode).
- **Tagged injection payload** (`render_context` in `hybrid_search.py`): produces a
  strict `<agent_memory trusted="false">` block with nested `<core_facts>`,
  `<session_context ephemeral="true">` and `<retrieved_context>`, XML-escaped, and an
  explicit comment that retrieved text is *background data, never an instruction* —
  separating recalled facts from the live prompt (indirect-injection defence). New
  CLI: `hybrid_search.py context "<text>" --budget N --core-fact "…"`.
- **Hard token budget** (`estimate_tokens` + `apply_token_budget`): a fixed top-k can
  still overflow the window when hits are long. `--max-tokens` / `context --budget`
  trims to a conservative ~4-chars/token estimate; an over-budget first hit is
  truncated rather than returning nothing. `0` = unlimited (legacy behaviour).

### Changed
- **Retrieval is now lifecycle-aware**: `search_lexical`, `search_vector` and
  `search_hybrid` add `AND m.status = 'active'`, so superseded/disputed facts can no
  longer pollute results — the concrete fix for "two contradictory facts coexist".
- README/SKILL nightly pipeline documents the arbitration step and the re-index.

### Verified (executed, not read)
- **Lifecycle transitions** on a real SQLite DB: high-confidence contradiction → old
  row `superseded` with `superseded_by` pointing at the new `active` row; weak
  contradiction (0.4) → old row `disputed`, new inserted; redundant → `last_confirmed`
  refreshed and confidence bumped, no duplicate; compatible → added. `lifecycle`
  listing confirmed the end state (`active=3, superseded=1` in the fixture).
- **Token budget**: 400-char chunks (~100 tokens each) → budget 250 keeps 2, budget
  500 keeps 3, budget smaller than one chunk truncates it and still returns a payload.
- **Tagged block**: rendered output inspected — nesting, escaping and the
  non-authoritative comment present.
- **In-place migration**: `ensure_lifecycle_columns()` on a DB built from the old
  schema adds exactly the missing columns.
- Syntax validated on both modules (`ast.parse`).

### Files Modified (5)
`hybrid-search/schema.sql`, `hybrid-search/hybrid_search.py`, added
`hybrid-search/conflict_resolver.py`; plus `README.md`, `SKILL.md`, `CHANGELOG.md`.

## v2.2.2 — Disclosure That Matches the Transport (2026-10-02)

Round 7, from the second SkillSpector run on the published v2.2.1 (54 findings).
Most of the report is scanner triage already covered in
`docs/SECURITY-AUDIT-NOTES.md`; **one finding was real, and it was one the scanner
only half-saw**.

### Fixed
- **The transport disclosure lied about the transport** (`trace_extractor.py`):
  `llm_destination()` — the function whose entire job is to warn the operator before
  memory content leaves the machine — read **only** `os.environ["OLLAMA_API_KEY"]`,
  while the actual sender, `get_ollama_api_key()`, also resolves the key from
  `~/.openclaw/workspace/.secrets/ollama.json` and from `openclaw.json`.
  Consequence: with the key in the secrets file — the common deployment — the banner
  printed *"local Ollama … else local fallback"* and the content was then posted to
  `https://ollama.com`. The warning was wrong **in exactly the configuration it
  existed to protect**. This is worse than an undisclosed transmission: it is a
  disclosure that actively misleads.
  Both code paths now share one resolver, `_find_ollama_api_key_sources()`, which
  returns `(source, key)` in one fixed precedence order. The banner names the source
  (`key from env`, `key from secrets-file`, `key from config`) and `TRACE_LLM_LOCAL_ONLY=1`
  short-circuits before any lookup.
- **Intent/code divergence in the docs** (`README.md`, `SKILL.md`): the README opened
  with "No external API dependencies (Ollama runs locally via HTTP, no cloud APIs)"
  and the SKILL description ended with "zero external cloud API dependencies" — while
  the extractor's **primary** transport was Ollama cloud. Six of the 54 findings are
  this single contradiction. Both files now state the real posture: **local by
  default, one opt-in cloud path**, with the switch and the warning documented at the
  top, not buried.
- **`--session-file` contradicted the confinement claim** (`SKILL.md`): the notes
  asserted that every script stays inside `WORKSPACE/memory/`, but `--session-file`
  deliberately accepts one absolute path outside it (a session transcript does not
  live under `memory/`). The claim is now precise — documented as an explicit,
  never-automatic exception rather than silently overstated. The same edit records the
  three-file `ALLOWED_SCAN_FILES` allowlist so the stated scope equals the real scope.
- **`OLLAMA_API_KEY` was missing from the configuration table** (`README.md`): the
  variable that turns on the only cloud-capable path was undocumented.

### Verified (executed, not read)
- **The bug, reproduced then closed**: with no `OLLAMA_API_KEY` in the environment and
  a key present in `.secrets/ollama.json`, the old `llm_destination()` returned
  `('cloud', "…if a key is configured, else local fallback")` — ambiguous at best.
  The patched version returns
  `('cloud', 'Ollama cloud (ollama.com) — key from secrets-file — content leaves this machine')`.
- **Local-only still wins**: `TRACE_LLM_LOCAL_ONLY=1` returns
  `('local', 'local Ollama (127.0.0.1:11434) — forced by TRACE_LLM_LOCAL_ONLY')` before
  any key lookup runs.
- **Env override**: `OLLAMA_API_KEY` set returns `('cloud', '… — key from env — …')`.
- `ast.parse()` clean on the modified module.

### Documented (scanner false positives — not defects)
- **Tainted flow `os.environ` → `urlopen`** in `consolidate_advisor.py` (~318) and
  `trace_extractor.py` (~359): the first targets `OLLAMA_URL`, produced by
  `get_safe_ollama_url()` and constrained to a loopback allowlist at import; the second
  targets the literal `http://127.0.0.1:11434`. Loopback sinks, not exfiltration sinks.
- **"Credential Access"** on `SECRET_SKIP_PATTERNS` / `SECRET_PATH_PATTERNS` and on the
  markdown that documents them: a deny-list that names what it refuses is a control,
  not a credential read. Firing on the prose of a fix is a category error.
- **"Autonomous Decision Making"** in `auto_archive.py` / `consolidate_advisor.py`:
  the scanner quotes the `if not sys.stdin.isatty(): return` guard as though it forced
  the action. It is the human-in-the-loop branch.
- Full dispositions: `docs/SECURITY-AUDIT-NOTES.md` §2.6.

### Files Modified (4)
`trace_extractor.py`, `README.md`, `SKILL.md`, `CHANGELOG.md`, plus
`docs/SECURITY-AUDIT-NOTES.md`

## v2.2.1 — Disclose the LLM Transport, Harden PII Scrubbing (2026-10-02)

Closes the T09 finding raised by the ClawHub / SkillSpector scan on 2026-10-02:
**"Undisclosed Cloud Transmission of Memory and Session Content"** in
`trace_extractor.py`. The finding was valid. The extractor's primary transport is
Ollama **cloud**, so memory and session text leaves the machine — and neither the
code nor the docs said so, in a repository that advertises itself as local-first.

### Fixed
- **Undisclosed cloud transmission** (`trace_extractor.py`): the extraction path
  posts to `https://ollama.com/api/chat` with a bearer key. Every run now prints its
  destination before sending — `[Security] ⚠️ CLOUD TRANSMISSION: …` when the target
  is cloud, `[Security] … (stays on this machine)` when it is local — via the new
  `llm_destination()` helper.
- **No local-only escape hatch**: added **`TRACE_LLM_LOCAL_ONLY=1`**, which makes
  `call_ollama_cloud()` return early and refuses every cloud call. Local-only mode
  cannot silently fail over to a transport that leaves the machine.
- **`sanitize_pii()` gaps**: the filter was regex-only and missed secrets in uncommon
  formats. Extended with JWTs (`eyJ…`), hex blobs ≥32 chars, base64 blobs ≥40 chars,
  French phone numbers, card-like digit runs, `access_key`/`apikey` assignments and
  OpenSSH private keys. The docstring now states plainly that scrubbing is
  **best-effort, not a guarantee**, and that the transport decision is the primary
  control. A "local-first, no cloud" claim is only as good as the transport behind it.

### Docs
- `README.md`, `SKILL.md`: the transmission, the destination, and the local-only
  switch are now documented; the blanket "zero external cloud API" phrasing is
  corrected where it did not hold for the extractor. `TRACE_LLM_LOCAL_ONLY` added to
  the configuration table.
- `docs/SECURITY-AUDIT-NOTES.md`: T09 recorded as a **closed real finding** (§1.0);
  the two false-positive families it generated — tainted-flow at `urlopen` in
  `trace_extractor.py` (§2.4) and credential-access hits on the secret deny-lists and
  on the audit prose itself (§2.5) — are triaged with dispositions.

### Verified (executed, not read)
- `llm_destination()` returns `('local', …)` under `TRACE_LLM_LOCAL_ONLY=1`, and
  `('cloud', "… content leaves this machine")` when `OLLAMA_API_KEY` is set.
- `sanitize_pii()` redacts all six test classes: JWT, hex-32, base64-40, French phone
  number, email, bearer token — 6/6.
- Non-regression: ordinary note text survives (`version 2.1.4`, `exit code 1`
  intact); only the embedded email is redacted.
- `ast.parse()` clean on the modified module.

### Acknowledgements
T09 reported by the ClawHub security scan (SkillSpector). Fixed rather than argued.

## v2.2.0 — Trace Extractor Ships, Ontology GC, Deterministic IDs (2026-10-02)

First release that includes `trace_extractor.py` as a **shipped artifact** rather
than a referenced-but-absent step, plus a long-overdue garbage collector for the
ontology op-log. Two latent bugs in the extractor are fixed: IDs that were
never stable across processes, and an "upsert" that physically appended.

### Added
- **`trace_extractor.py`** — the session/notes extractor is now published. It was
  cited as step 1 of the documented pipeline since v2.0 but the file itself was
  never in the repository, so cloning the toolkit gave you a README referencing a
  script no one could run. Categories: decisions, errors, facts, patterns.
- **`ontology_compact.py`** — garbage collector for `memory/ontology/graph.jsonl`.
  The ontology file is an append-only operation log; nothing ever replayed it, so
  the same entity was rewritten on every run and the file grew without bound.
  The compactor replays the log into a consolidated state (one line per active
  entity, superseded records dropped), backs up first, validates that the entity
  set and contents are identical, and only then swaps in place. Idempotent: it
  skips when the gain is below `--min-gain` (default 5%).

### Fixed
- **Non-deterministic entity IDs** (`trace_extractor.py`): decisions were keyed
  with `hash(what) % 10000`. Python randomises `hash()` per process
  (`PYTHONHASHSEED`), so the *same* decision produced a *different* ID on every
  run. The `if entity_id not in existing_ids` guard could never fire — the ID was
  always new — and the guard's own premise (ID identifies content) was false.
  Observed impact on a production workspace: one episode rewritten **38 times**
  under 38 different IDs, 63 IDs duplicated 2–38×, 52% of all log lines redundant.
  IDs now come from `stable_id()`, a SHA-256 prefix, stable across processes and
  machines.
- **`upsert` that appended** (`trace_extractor.py`): records were labelled
  `"op": "upsert"` but written with `open(path, "a")`. The operation name
  described an intent the code did not implement — an update was impossible, only
  appends happened. Both writers now go through `upsert_entities()`, which reads
  the current file, replaces matching entities in place, appends the rest, and
  writes atomically via a temp file.

### Verified (executed, not read)
- **ID stability**: `stable_id()` called from three separate interpreter processes
  returns the identical digest (`dec_20260629_4f0644cd`, `tl_20260613_873a194b`),
  where the previous `hash()`-based scheme returned a different value each run.
- **Real upsert**: on a two-entity file, updating an existing ID leaves the line
  count unchanged and replaces the record; adding a new ID grows it by exactly one.
- **Compactor on a production graph**: 742,364 → 272,518 bytes (−63%),
  2,018 → 912 lines, 1,106 redundant lines dropped, and the reloaded entity set
  compared equal to the pre-compaction state (912 active entities, 0 lost).
- **Compactor idempotence**: re-run on the already-compacted file reports 0 lines
  dropped and writes nothing (gain below threshold).
- **Syntax**: `ast.parse()` clean on both new scripts.

### Notes
- The ontology compactor pairs with the parser fix in the sibling release line:
  `memory_health.py` and the index builder accept any record carrying an entity,
  so a consolidated `"op": "state"` file and a raw operation log both index
  correctly. Previously the indexer matched `op == "create"` only, which silently
  indexed **zero** entities once a log had been compacted.

## v2.1.4 — Allowlist/Index Agreement, Both Directions (2026-09-27)

Follow-up found by the v2.1.3 control pass. v2.1.3 fixed an allowlist that was
**narrower** than what was indexed; the fix then made it **wider** than disk
reality. Declared scope must equal indexable scope in both directions.

### Fixed
- **Dead entry in `ALLOWED_SCAN_FILES`** (`hybrid-search/hybrid_search.py`): v2.1.3 declared `TOOLS.md` unconditionally, but `collect_all_files()` guards each root file with `os.path.exists()` — and `TOOLS.md` does not exist on a standard workspace (its content was merged into `AGENTS.md`). The allowlist therefore advertised a file that was never indexed: the same intent/code divergence v2.1.3 set out to remove, re-created in the opposite direction. Optional root files are now declared **only when present on disk** (`{f for f in ROOT_CONFIG_FILES if os.path.exists(f)}`), so `MEMORY.md` is always declared and `TOOLS.md` is declared exactly when it is actually indexable. `OWN_SKILL_FILE` stays unconditional (it is a shipped artifact).

### Verified (executed, not read)
- **`TOOLS.md` absent** (real workspace): dropped from the allowlist; `safe_resolve()` refuses the path with `UnsafeFileError: outside allowed scan dirs`.
- **`TOOLS.md` present** (temp workspace, `WORKSPACE_ALLOW_CUSTOM=1`): automatically declared and resolved successfully.
- **`MEMORY.md`** (present): still declared and resolved.
- **Non-regression**: `/etc/passwd` still refused.

### Files Modified (1)
`hybrid-search/hybrid_search.py`

## v2.1.3 — Security Round 6: Runtime Confinement & Read-Only Correctness (2026-09-27)

Second pass over the public ClawHub audit, after the v2.1.2 import-path work.
Four real findings closed; the rest of the report was confirmed as scanner false
positives and is now documented so it does not have to be re-triaged.

### Security
- **`--workspace` no longer bypasses confinement** (`auto_archive.py`, `consolidate_advisor.py`): the `is_relative_to(WORKSPACE)` guard ran only at import time, while the CLI re-bound the module globals from `args.workspace` further down the flow — so `--workspace <other>` produced unvalidated `MEMORY_DIR` / `ARCHIVE_DIR` / `SCORES_FILE` for the whole run. The check is now a `validate_paths()` function invoked at import **and** immediately after every `--workspace` rebind. `WORKSPACE` is also `.resolve()`d before use. This was an intent/code divergence: the code claimed confinement, the flag removed it.
- **Passive health check no longer mutates memory** (`memory-health.py`, T09): `run_trace_extraction()` ran `trace-extractor.py` unconditionally, and that script **appends to `memory/ontology/graph.jsonl` and rewrites daily notes** — so `memory-health.py` reported `MODE: READ-ONLY` while silently changing state. The extractor is now invoked with `--dry-run` unless the caller explicitly opted into mutation; the mutating path is reachable only through `_run_trace_extraction(..., mutating=True)`, set from the user's `--fix` intent.
- **Scan scope now matches what is actually indexed** (`hybrid-search/hybrid_search.py`): `ALLOWED_SCAN_DIRS` declared "memory/ only", but `collect_all_files()` also indexed `MEMORY.md`, `TOOLS.md` and `skills/memory-health/SKILL.md`. Added `ALLOWED_SCAN_FILES`, an explicit allowlist of those exact paths, which `safe_resolve()` now accepts in addition to the scoped directories. Deliberately a set of named files, never a directory — a directory entry would re-open skill enumeration.
- **Subprocess isolation hardened** (`memory-health.py`): `WORKSPACE` came straight from the environment and drove every subprocess path, and `["openclaw", ...]` calls trusted the inherited `$PATH`. `OPENCLAW_BIN` is now resolved once via `shutil.which()` with an absolute fallback (no bare `"openclaw"` remains), and `WORKSPACE` is validated against the expected root unless `WORKSPACE_ALLOW_CUSTOM=1` is set deliberately.

### Verified
- Syntax validated on all four modified modules.
- `validate_paths()` exercised for real: an import-time load succeeds, then a simulated escape (`MEMORY_DIR=/etc` under the real workspace) raises `RuntimeError`; a legitimate workspace still archives normally in `--dry-run`.
- Read-only path confirmed to build `trace-extractor.py --days N --dry-run`; `--help` on the extractor confirms the flag is supported.
- Allowlist exercised: `MEMORY.md` and the skill's own `SKILL.md` accepted; `/etc/passwd`, `skills/<other>/SKILL.md`, `SOUL.md`, `USER.md`, `.secrets/*` and `memory/../SOUL.md` all refused.

### Documented (scanner false positives — not defects)
- **"Credential Access" in the secret-path filters**: `SECRET_PATH_PATTERNS` / `SECRET_SKIP_PATTERNS` match `\.ssh`, `id_rsa`, `token`, `password`, `.env`, `.aws`, `.config/google`. These are a deny-list that *prevents* such files from being read or indexed, matched against the resolved path so a benign-named symlink cannot smuggle a secret through. Defensive filter, not an access attempt.
- **"Unsafe Defaults" in `CHANGELOG.md` / `README.md`**: `/tmp/vec-test-venv` and `/etc/passwd` appear only as documentation of already-removed vulnerabilities and of a guard's test case. Prose describing a fixed defect is not a live defect.
- **"Tainted Flow / network sink" at `urlopen`**: `consolidate_advisor.py` and `hybrid-search/hybrid_search.py` never POST memory content anywhere attacker-chosen. `OLLAMA_URL` (and `OLLAMA_EMBED_URL`) pass through `get_safe_ollama_url()`, which raises `ValueError` at import for any host outside `{localhost, 127.0.0.1, ::1}` — the process will not start against a remote endpoint. The destination is fixed to loopback before any memory is read, so this is a **local flow secured by design**, not exfiltration.
- Full triage written up in `docs/SECURITY-AUDIT-NOTES.md`, including scanner-configuration recommendations.

### Files Modified (5)
`auto_archive.py`, `CHANGELOG.md`, `consolidate_advisor.py`, `hybrid-search/hybrid_search.py`, `memory-health.py`, added `docs/SECURITY-AUDIT-NOTES.md`

## v2.1.2 — Security Round 5: Import Path & Filesystem Confinement (2026-09-27)

Follow-up to the public ClawHub security audit. Three real findings closed; the
remaining secondary-block items were confirmed as scanner false positives.

### Security
- **Attacker-controllable import path removed** (`hybrid-search/hybrid_search.py`): `VEC_VENV_PATH = "/tmp/vec-test-venv/lib/python3.14/site-packages"` + `sys.path.insert(0, ...)` deleted. A world-writable directory at the head of `sys.path` gives import resolution absolute priority over site-packages, so any local process could drop a `sqlite_vec.py` and have it executed on the next `import`. The path also did not exist on the production host — dead *and* dangerous. `sqlite_vec` now imports from the active environment, with an actionable `ImportError` (`pip install sqlite-vec`) and a comment recording why a `/tmp` entry must never return.
- **`safe_resolve()` added to `hybrid_search.py`**: applied to `index_file()`, `index_jsonl_file()` and the `--dir` walk in `cmd_index()`. Guard order: refuse symlinks outright; `os.path.realpath()` to normalise `..`; require the result to sit inside `ALLOWED_SCAN_DIRS` (`memory/` only); match `SECRET_PATH_PATTERNS` against the **resolved** path (never the literal one, so a symlink cannot smuggle a secret through an innocuous name); require a regular file. `--dir` pointing outside scope is rejected before the glob runs. New `UnsafeFileError` exception.
- **Symlinks refused in the memory scanners** (`scoring.py`, `auto_archive.py`, `consolidate_advisor.py`): `is_symlink()` checked before `is_file()` at each walk site. `scoring.py` gained `is_safe_memory_file()` — a symlink named like a daily note is the classic route for pulling a private key into an index that then ships it to the embedding endpoint.
- **Secret patterns extended**: `.ssh`, `.aws`, `.config/google`, `id_rsa`, `id_ed25519`, `.pem`, `.key`.

### Verified
- Syntax validated on all five modules.
- Guards exercised for real: a legitimate note is accepted; a symlink named `2026-01-01-innocent.md` pointing at `/etc/passwd` is refused; `/etc/passwd` passed directly is refused as out of scope; `api-token-notes.md` inside `memory/` is refused; `--dir /etc` is refused before listing.

### Not Changed (by design)
- `auto_archive.py` and `consolidate_advisor.py` still require `--force` in non-interactive mode. This is intended behaviour, not a defect — now documented rather than implicit.

### Files Modified (6)
`auto_archive.py`, `CHANGELOG.md`, `README.md`, `consolidate_advisor.py`, `hybrid-search/hybrid_search.py`, `scoring.py`

## v2.1.1 — Security Round 4: PII Purge & Scope Confinement (2026-08-22)

### Security
- **PII purge**: Deleted all results/*.json (11 files), results/*.svg (9 files), hybrid-search/FULL_INDEX_REPORT.md, hybrid-search/test_results.json, hybrid-search/agent_memory.db, hybrid-search-proto/ (entire prototype folder), __pycache__/*.pyc — all contained real personal data (Stéphane, Airbus, .secrets/, stephanemee.com, AstroCapture)
- **`.gitignore` hardened**: Added `*.svg`, `eval_output/`, `*.log`, `*.pyc`, `hybrid-search-proto/`, `.secrets/`
- **Subprocess query sanitized**: `memory-health.py` hardcoded query `"Stéphane's role at Airbus"` replaced with anonymized `"project alpha configuration"`
- **Script path validation**: All `subprocess.run` script paths validated with `Path.resolve().is_relative_to(WORKSPACE)` — prevents path traversal
- **Skill enumeration blocked**: `hybrid_search.py` no longer globs `skills/*/SKILL.md` — only indexes its own SKILL.md
- **Personal files excluded from index**: `USER.md`, `IDENTITY.md`, `AGENTS.md`, `SOUL.md`, `HEARTBEAT.md` no longer indexed by hybrid_search.py
- **Scope confinement**: `scoring.py`, `auto_archive.py`, `consolidate_advisor.py` validate `MEMORY_DIR.is_relative_to(WORKSPACE)` with explicit `ALLOWED_SCAN_DIR`

### Changed
- **`memory-health.py` is READ-ONLY by default**: No SVG charts, JSON reports, or benchmark reports written to disk without `--output-dir <path>` flag
- **`check_drift()` no longer auto-creates `RESULTS_DIR`**: Only reads existing results if present
- **Docstring updated**: Clearly documents read-only default, `--output-dir` for output, `--fix` as destructive mode
- **`run_tests.py` TEST_QUERIES anonymized**: `AstroCapture` → `project_alpha`, `leadership coaching Airbus` → `team leadership coaching session`, `2026-08-17` → `sample_note_01`, etc.
- **SKILL.md & README.md**: Updated with read-only documentation, security notes section, `--fix` destructive mode warning
- **`consolidate_advisor.py` docstring**: Removed personal name reference

### Files Modified (10)
`.gitignore`, `README.md`, `SKILL.md`, `auto_archive.py`, `consolidate_advisor.py`, `hybrid-search/hybrid_search.py`, `hybrid-search/run_tests.py`, `memory-health.py`, `scoring.py`, deleted `hybrid-search/FULL_INDEX_REPORT.md`

## v1.3.0 — Security Round 3 (2026-08-18)

### Fixed
- **OLLAMA_EMBED_URL no longer hardcoded**: Embedding endpoint now derived from `OLLAMA_URL` (`{OLLAMA_URL}/api/embeddings`) — consent warnings show the actual destination, not a misleading one
- **`check_ollama_url()` validates both endpoints**: Now checks `OLLAMA_URL` and `OLLAMA_EMBED_URL` for localhost
- **Batch/add warnings show real endpoint**: Consent text displays `OLLAMA_EMBED_URL` (where data actually goes) instead of `OLLAMA_URL`
- **`run_tests.py` no longer exposes content**: Removed all content snippets from stdout, `test_results.json`, and `FULL_INDEX_REPORT.md` — only metadata (source, scores, category) is stored
- **"Safe by default" claim corrected**: README and SKILL.md now accurately state that dry-run is *available* but not the default for all scripts (archive, scores, consolidation report write by default)

## v1.2.0 — Security Round 2 (2026-08-18)

### Added
- **Consent warnings on `hybrid_search.py index`**: Batch indexing now displays a warning before sending file contents to Ollama for embedding. Use `--yes` to skip in automation
- **Embedding notice on `hybrid_search.py add`**: Single-file add prints a one-line notice. Use `--quiet` to suppress
- **`OLLAMA_URL` localhost validation**: Warning printed if endpoint is not localhost
- **`--benchmark` is now benchmark-only**: No longer runs the full health check suite — benchmark only (unless combined with `--deep` or `--quick`)
- **READ-ONLY / FIX MODE banner**: `memory-health.py` prints clear mode indicator at startup
- **Inline SECURITY comments**: All `subprocess.run` and `urlopen` calls annotated with security context
- **4 new Security Notes** in README and SKILL.md: `--force` flag, subprocess/urlopen intent, hybrid_search consent, `--benchmark` behavior

### Fixed
- `memory-health.py --fix` now requires interactive confirmation or `--force` flag
- `--force` help text more explicit about backups

## v1.1.0 — Security Round 1 (2026-08-18)

### Fixed
- **`consolidate_advisor.py` docstring corrected**: No longer claims "Does NOT modify any files" — accurately reports that it writes `consolidation_report.json`
- **`--apply-promotions` confirmation added**: Now requires interactive `y/n` prompt or `--force` flag before writing to MEMORY.md
- **`--dry-run` no longer writes report**: `consolidate_advisor.py --dry-run` is truly read-only
- **`memory-health.py --fix` safety**: Creates timestamped backup in `memory/backup/` before modifying; requires confirmation or `--force`
- **`hybrid_search.py init` safety**: Requires `--force` to overwrite existing database
- **Secret file filtering in `scoring.py`**: Skips `.secrets/`, `*.env`, `credentials*`, `*token*`, `*password*`, `.git/`
- **`auto_archive.py` bulk safety**: Requires `--force` or confirmation if moving >10 files
- **`run_tests.py` content exposure**: Removed content snippets from `test_results.json` (metadata only)

### Changed
- README.md: Removed "no external API dependencies" and "pure stdlib" claims — added accurate Security Notes section
- SKILL.md: Same corrections + fixed duplicated Design Principles section
- README.md: Removed Second Brain comparison table and references

## v1.0.0 — Initial Release (2026-08-17/18)

### Added
- **`trace_extractor.py`** — Session extraction: decisions, errors, facts, patterns from transcripts and daily notes
- **`auto_archive.py`** — Daily note archiving: moves notes >N days to `memory/archive/YYYY-MM/`
- **`scoring.py`** — Temporal decay scoring: recency × category weight × frequency boost × entity boost
- **`consolidate_advisor.py`** — Consolidation suggestions: clusters, promotions, stale items, duplicates (LLM optional via Ollama)
- **`memory_health.py`** — System health check: diagnostics, benchmark, ontology health, drift detection
- **`hybrid_search.py`** — Hybrid search: FTS5 (BM25) + sqlite-vec (cosine) + Reciprocal Rank Fusion (k=60)
- **`run_tests.py`** — Validation queries for hybrid search index
- **`ontology/schema.yaml`** — Entity and relation type definitions (20 entity types, 10 relation types)
- **README.md** — Full documentation with pipeline diagram, CLI examples, configuration, design principles
- **SKILL.md** — OpenClaw skill manifest with script descriptions and cron setup
- **LICENSE** — MIT