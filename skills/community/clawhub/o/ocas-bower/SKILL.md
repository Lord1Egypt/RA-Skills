---
warning: 'FALSE TRIGGER RISK: Has had 50% false trigger rate on interactive loads (1/2). Do NOT load for Google Drive organization when the user has not explicitly requested it or when the task is simple folder cleanup — load only when Drive organization is the primary intent and there is clear evidence of organizational mess. Added automatically on 2026-09-21.'
name: ocas-bower
license: MIT
source: https://github.com/<agent-handle>/bower
description: Automatic Google Drive organizer. Scans Drive structure and file contents,
  builds a personalized preference profile, applies domain-specific logic (taxes by
  year, projects by name, home by system, finance by institution), and executes non-destructive
  moves, renames, and description writes. Learns organizational style over time and
  auto-approves consistently accepted patterns. Never deletes files. NOT for web research,
  document analysis, or Chronicle ingestion.
includes:
- references/**
- scripts/**
metadata:
  author: Indigo Karasu (indigokarasu)
  version: "1.5.0"
  hermes:
    category: utilities
    tags:
    - google-drive
    - file-organization
    - auto-organize
    - ocas-core
triggers:
- google drive
- drive organizer
- file organization
- drive cleanup
- auto-organize
---

## Interactive Menu

When invoked interactively, present a two-level menu. See `references/interactive-menu.md` for the full menu structure.

## When to Use

- Google Drive cleanup and organization
- Duplicate file detection and merging
- Folder structure optimization
- Preference-based auto-organization rules
- Drive health monitoring and reporting

# Bower

Bower keeps Google Drive organized without ever deleting anything. It learns your organizational style from your existing structure, applies domain-native logic where it detects known domains, builds a personalized preference profile, and over time auto-approves patterns you consistently accept. The goal: you go to sleep and wake up to a Drive that looks the way you would have organized it yourself.

**Current status (2026-07-19):** Weekly deep-scan cadence established. Drive has ~23,699 total folders; 6 curated root folders (Bookshelf, Archive, Home, Projects, Professional, Authenticator Backups) holding ~516 direct files. The ~23.7K folders are a large nested backup/Takeout tree (dominant subtree `Archive` with 9,692 descendant folders) — out of Bower's reorganization scope (Bower organizes, never deletes). Deep scans are **sampled** (`scan_coverage: 0.5`): enumerate all folders once (cached), sample 300 direct children per curated root. 2 prescriptive domains detected (projects, home). Auto-approval has not yet triggered — needs proposal review/approval. 16 pending move proposals remain from 2026-07-14, most of which are title-keyword false positives (see Gotchas). Drive root clean (0 loose files). Main value: monitoring drift, confirming health, and executing reviewed proposals.

## Trigger conditions

- "Organize my Drive"
- "Clean up my Google Drive"
- "What's disorganized in my Drive?"
- "Show me what Bower found" / "Run a Drive scan"
- "Apply the pending Bower proposals"
- "What has Bower learned about my preferences?"
- "What would you do to this folder?" / "Simulate Bower on my Projects folder"
- "Turn on quiet mode" / "Run silently"
- Bower's background scan job fires on schedule

## When NOT to Use

- Deleting files — Bower never deletes
- Managing sharing permissions — Bower doesn't touch permissions
- Creating top-level taxonomy from scratch — Bower infers from existing structure
- Interacting with non-Drive storage — Bower is Drive-only
- Applying domain logic to undetected domains — needs 5+ files or 2+ subfolders to activate
- Web research or document analysis — use Sift
- Chronicle ingestion

## Responsibility boundary

Bower does: scan Drive structure and file contents, build a preference profile from evidence, detect and apply domain-specific organization logic, identify outliers, propose folder moves, renames, and description writes, auto-approve promoted patterns, apply approved changes using the system's Google Drive access, maintain a full audit trail.

Adjacent responsibility: Sift handles web research and document analysis. Bower emits entity signals in journal payloads for Chronicle ingestion for all Drive artifacts and entities encountered during scans.

## Ontology types

- **Thing/DigitalArtifact** — Drive files and folders that Bower scans, classifies, and organizes. Bower includes signals in journal payloads for all discovered Drive artifacts.
- **Entity/Person** — People referenced in documents, shared-with metadata, and collaborators encountered during scans.
- **Place** — Locations found in documents (travel documents, address lists, venue information).
- **Concept/Event** — Events, projects, or topics that documents are about (e.g., a folder of wedding planning docs, a project kickoff deck).
- **Concept/Idea** — Themes and topics reflected by folder structure and document content (e.g., recurring interest in machine learning across multiple folders).

## Signal emission

Bower includes structured signals in journal payloads for all entities and artifacts encountered during scans. All signals carry `user_relevance: "user"`. Five signal types are emitted: Thing/DigitalArtifact, Entity/Person, Place, Concept/Event, Concept/Idea. One signal per unique artifact/entity, deduplicated by `file_id` (artifacts) or email (persons). Signals are written to the `signal` payload field during `bower.scan.deep` and `bower.scan.light`.

For full JSON schema examples, see `references/signal_examples.md`.

## Commands

| Command | Summary |
|---------|---------|
| `bower.scan.deep` | Full Drive crawl, folder-by-folder. `--founding` for first use. `--analyze-now` for early results. |
| `bower.scan.light` | Incremental scan of recent changes. Arrival detection + auto-apply if quiet mode. |
| `bower.analyze` | Domain logic + generic rules → ranked proposals. Read-only. |
| `bower.simulate` | Read-only scan of a folder. Shows what Bower would do. |
| `bower.proposals.review` | List pending proposals by folder, confidence, domain. |
| `bower.proposals.approve` | Approve a subset. Requires explicit scope. |
| `bower.proposals.reject` | Reject proposals. Suppresses patterns. |
| `bower.apply` | Execute approved proposals. `--dry-run` to preview. |
| `bower.undo` | Reverse moves, renames, description writes. |
| `bower.preferences.show` | Display preference profile. |
| `bower.preferences.lock` | Mark a preference field or pattern as fixed (prevents auto-inference from overwriting it). |
| `bower.preferences.quiet` | Toggle quiet mode (suppresses digest only). |
| `bower.feedback.clear` | Clear suppression patterns or demotions. |
| `bower.status` | SkillStatus summary. `--trend` for 8-week health. |
| `bower.init` | First-use initialization. |

Full flag descriptions and semantics: `references/command_reference.md`

## Workflow

The Bower organization pipeline: **scan → analyze → propose → apply → learn**.

1. Scan Drive structure and file contents
2. Analyze with domain-specific logic (taxes by year, projects by name, etc.)
3. Propose non-destructive moves/renames
4. Apply approved changes
5. Learn from accepted patterns for auto-approval

## Execution flow

### First use (founding run)
`bower.init` → `bower.scan.deep --founding` (Phase 1: tree discovery; Phase 2: scan folders one at a time, resume across sessions) → `bower.analyze` → present high-confidence proposals as batch → if accepted: `bower.apply`. Founding run batch approval grants immediate pattern promotion credit. Use `--analyze-now` for early results before all folders scanned.

### Steady state
Daily light scan at 02:00 PT: `bower.scan.light` → arrival detection → auto-apply promoted high-confidence matches if quiet mode on. Weekly deep scan Sunday 01:00 PT: run the **sampled** deep scan (`commons/data/ocas-bower/deep_scan_sampled.py` — NOT full enumeration) → `bower.analyze` (run `scripts/bower_analyze.py`, which reads the canonical data dir) → emit Drive health signal to Vesper. Silent unless something needs attention. On this ~24K-folder Drive the weekly deep scan stays sampled; it never attempts full enumeration.

### Running scans on this host (verified recipe)

The canonical scan scripts live under the indigo profile data dir, NOT the skill's own `scripts/`. Use these exact commands (verified 2026-07-24):

- **Light scan:** `/usr/bin/python3 $HERMES_HOME/../indigo/commons/data/ocas-bower/run_light_scan.py`
  - Interpreter: `/usr/bin/python3` (3.14) — has BOTH `googleapiclient` and `requests`. A stray `python3` on PATH (a project `.venv`, 3.13) lacks `requests` and produces a false `auth_or_build_failed` (see Gotchas).
  - Credentials: `<gworkspace-creds>/credentials/<user-google-email>.json`, read by `scripts/google_auth.py` → `get_service`. The script inserts `$HERMES_HOME/../indigo/scripts` onto `sys.path` itself, so run it from any cwd.
  - Exit 0 + JSON `"status": "OK"` = success. Artifacts: `light_scan_latest.json`, appended `scan_events.jsonl` / `evidence.jsonl`, and an Observation Journal under `commons/journals/ocas-bower/YYYY-MM-DD/`.
- **Deep scan (weekly, sampled):** `/usr/bin/python3 $HERMES_HOME/../indigo/commons/data/ocas-bower/deep_scan_sampled.py` (use the sampled script, never `scripts/bower_full_scan.py`).

Never trust a `search_files` `0 results` for `google_auth.py` — the ripgrep-backed index has returned phantom relative paths and missed real files under the profile tree. If a dependency check fails, confirm with `find ~/.hermes -name 'google_auth*'` and absolute `ls` before concluding auth is broken (see Gotchas).

### Arrival detection
After every light scan, for each new/modified file: classify → check `pattern_key` against `auto_approved_patterns`. High-confidence match: generate `approved` proposal (auto-apply if quiet mode). Medium-confidence: `pending`. No match: normal `pending`.

### Simulation
Read-only scan of specified folder → apply full analysis pipeline → print narrative report. No proposals, logs, journals, or state changes written. See `references/organization_rules.md` for simulation output format.

### Apply run
Description auto-writes first → sort by confidence tier → apply `apply_cap` → per-proposal staleness check → execute via Google Drive → log to `move_log.jsonl` → produce digest (suppressed in quiet mode if all succeeded) → write Action Journal.

**Verification after apply**: After `bower.apply` completes, read back applied proposal IDs from `move_log.jsonl` and confirm each file exists at its new destination via Google Drive list. Report any mismatches (file not found at destination) as failed moves. Verify the move log entry count matches the number of executed proposals.

### Undo run
Read move log records → staleness check → restore `previous_value` → execute reversal → log to `undo_log.jsonl` → record feedback → trigger pattern demotion if auto-approved → write Action Journal.

## Decision model

Read these reference files before the operations they govern:

| File | When to read |
|------|-------------|
| `references/organization_rules.md` | Before every `bower.analyze` run; defines preference inference, pattern promotion, taxonomy inference, all proposal generation rules, permission lookup, feedback suppression, recalibration, scan resume, cap behavior, digest format, and review narrative |
| `references/domains.md` | Before every `bower.analyze` run; defines domain detection, prescriptive/descriptive mode, canonical structures, and per-domain filing rules for Taxes, Projects, Home, Finance, Legal, Medical, Archive, Education |
| `references/analysis_schema.md` | Before `bower.scan.deep` or `bower.analyze`; defines all data schemas including preference profile, folder_index, scan_progress, proposals, move log, undo log, feedback log, and config |

See `references/decision-invariants.md` for the full list of safety invariants.

**Light scan structural baseline check (MANDATORY):**

Before running the `modifiedTime` query in `bower.scan.light`, ALWAYS perform a structural baseline comparison:

- [ ] Query root-level items: `GOOGLEDRIVE_FIND_FILE` with `q="'root' in parents and trashed = false"`, `pageSize=10`
- [ ] Compare counts against `drive_digest.json` → `root_level_file_count` and `root_level_folder_count`
- [ ] If root-level counts differ by more than 15% from the stored baseline, **flag structural drift immediately** — before processing the `modifiedTime` query results
- [ ] If drift exceeds threshold, abort the light scan, write `drift_detected` to `scan_events.jsonl`, and request a deep scan

**Why this matters (2026-06-14 incident):** A Drive restructuring placed 89+ files and 12+ folders at root level. All files had `modifiedTime` dates before the last scan's cutoff, so the `modifiedTime` query returned 0 results. The drift was invisible to the light scan. Only a root-level count comparison caught it. Without this check, the light scan would have reported "no new files" while the Drive was completely restructured.

**Cron implementation:** The `pageSize=10` query is fast (~2s). If `nextPageToken` is present, root has 100+ items — immediately compare against baseline. Do not wait for full pagination.

## Scan output

`bower.scan.deep` produces: `folder_index.json` (Phase 1), `scans/{folder_id}.json` per folder tree (Phase 2), `drive_digest.json` (updated per folder), `scan_progress.json`, scan event in `scan_events.jsonl`.

`bower.scan.light` produces: updated `scans/{folder_id}.json` files, scan event with drift_rate (aborts if drift exceeds threshold).

`bower.analyze` produces: outlier report in `analysis_events.jsonl`, expired proposals marked in `proposals.jsonl`, new proposals appended with `status: pending` and `expires_at`.

## Google Drive access

Bower uses Google Drive access for: list files/folders, read file content, move file to folder, rename file/folder, create folder, update file description. Bower never calls delete operations. Phase 1 lists all folders (fast metadata query). Phase 2 processes one folder tree at a time, capturing: id, name, mimeType, parents, modifiedTime, starred, size, trashed, description. Exclude trashed files. Fetch permissions for each folder; if unavailable, set `permissions_available: false` and suppress all move proposals.

**Workspace MCP fallback:** Drive operations prefer the Workspace MCP toolset (`workspace_mcp`) when present. If the Workspace MCP is **absent / unavailable**, fall back gracefully to `google_api.py` (the direct Google API python client that reads credentials via `google_auth.py` → `get_service`). The fallback is seamless: same list/move/rename/create operations, no delete, same `permissions_available` suppression rule. Prefer the python-client fallback over failing the run; log which backend was used in the scan journal.

## Background tasks

| Job | Schedule | Action |
|-----|----------|--------|
| `bower:scan` | Daily 02:00 PT | `bower.scan.light` → arrival detection → auto-apply promoted matches if quiet mode on |
| `bower:weekly-deep` | Sunday 01:00 PT | `bower.scan.deep` → `bower.analyze` → emit Drive health signal to Vesper |

Register during `bower.init`. Check for existing scheduled tasks before registering to avoid duplicates. All cron jobs use `sessionTarget: isolated`, `lightContext: true`, `wakeMode: next-heartbeat`.

### Vesper Drive health signal

Emitted weekly after Sunday deep scan as an InsightProposal with `proposal_type: routine_prediction` containing: Drive health score delta, files organized in past 7 days, active auto-approved patterns, domains that gained/lost structure, suppressed outlier classes worth surfacing. Vesper decides whether to include it in the weekly briefing.

## Optional skill cooperation

- **Vesper** — Bower emits a weekly Drive health InsightProposal after each Sunday deep scan. If Vesper is absent, the signal is dropped silently.
- **Chronicle** — Bower emits structured signals in journal payloads for all Drive artifacts and entities encountered during scans.
- **Mentor** — Bower's journals are evaluated by Mentor for OKR scoring. No action required from Bower.

## Inter-skill interfaces

Bower emits to:
- the `briefing` payload field — weekly Drive health InsightProposal (Sunday deep scan only)
- the `signal` payload field — entity and artifact signals for all Drive content (every scan)

Bower receives from: none.

## Journal outputs

Scan commands (`bower.scan.deep`, `bower.scan.light`) and `bower.analyze` emit **Observation Journals**. `bower.apply` and `bower.undo` emit **Action Journals**.

All Observation Journals from scan commands include `entities_observed`, `relationships_observed`, and `preferences_observed` in `decision.payload`. Journal path: `{agent_root}/commons/journals/ocas-bower/YYYY-MM-DD/{run_id}.json`.

## Recovery Behavior

Implements the recovery contract from `spec-ocas-recovery.md`.

- **Evidence**: Every scheduled run writes to `evidence.jsonl`, including no-op runs. `not_activity_reason` is mandatory when no side effects occur.
- **Gap detection**: On every wake, checks evidence log for most recent completed run. If gap exceeds cadence (24h light, 7d deep), logs `gap_detected` and runs a compact remedial pass.
- **Degraded mode**: When Google Drive access fails, enters degraded mode and produces a partial Drive health report. Evidence log records `degraded: google_drive`.
- **Log compaction**: Evidence and decision logs older than 30 days (no-op) or 90 days (error/gap) compacted to weekly summaries. Escalation records never auto-deleted. Last 7 days of raw entries always retained.

## Storage layout

See `references/storage-layout.md` for the full directory structure.

## OKRs

See `references/okrs.md` for all targets (folder coverage, proposal accuracy, user preference learning, schedule adherence, data integrity).

Tracked metrics: `proposal_precision` (≥0.80), `apply_success_rate` (≥0.95), `staleness_skip_rate` (≤0.05), `auto_approve_precision` (≥0.90), `false_positive_rate` (≤0.10), `scan_coverage` (1.0), `proposal_expiry_rate` (≤0.20), plus tracking-only: `content_influence_rate`, `description_coverage_rate`, `domain_proposal_rate`, `feedback_suppression_rate`.

## Initialization

`bower.init`: creates data/journal directories, writes `config.json` with defaults, registers cron jobs `bower:scan` and `bower:weekly-deep` (check platform registry first to avoid duplicates).

## Self-update

`bower.update` pulls the latest package from the `source:` URL in frontmatter. Compares local vs. remote version via GitHub API. If different: downloads tarball, extracts, replaces. Retries once on failure. Output: `I updated Bower from version {old} to {new}`. Silent if already current.

## Visibility

public

## Gotchas

- **Stale data after major Drive changes** — Between scans, the Drive may be cleaned up, migrated, or restructured catastrophically (e.g., 381K files → 17). When a deep scan detects a >50% change in total file/folder count compared to `scan_progress.json` or `drive_digest.json`, treat the previous scan data as stale: reset `scan_progress.json` to `phase: complete` with the new counts, update `drive_digest.json` with new totals, and add a `scan_notes` field documenting the change. Do NOT carry forward old proposals — the old `proposals.jsonl` records reference file/folders that may no longer exist. Let the new scan drive fresh proposals. Optionally archive old scan data (`scans/`, `proposals.jsonl`) to a dated archive directory.
- **Cron jobs cannot use `execute_code`** — Scheduled cron runs (light and deep scans on this profile) execute in an isolated context where `execute_code` is blocked. All scan logic must use native Hermes tools (List Google Drive files, Search Google Drive, `write_file`, `terminal` with `>>` for `.jsonl` append). Do not write Python scripts that expect to be run via `execute_code` for scheduled work. The `scripts/` directory is for interactive/scripted runs only.
- **Small Drive efficiency** — On Drives with <500 total files, the modifiedTime query may return mostly batch-imported content (e.g., 97 books imported at once). Group by timestamp to identify batch imports vs. real user activity. See `references/scan-debug.md` → "Small Drive light scan efficiency" for the triage pattern.
- **Drift threshold aborts light scans** — If the light scan detects significant structural drift, it aborts entirely rather than producing partial results. A subsequent deep scan is needed to re-establish the baseline.
- **Staleness checks execute per-proposal** — Even auto-approved, high-confidence proposals pass through a staleness check immediately before execution. A file moved between scan and apply can cause a proposal to quietly skip.
- **Permission fetch suppresses all move proposals** — If folder permissions are unavailable (API error or scope missing), Bower suppresses *all* move proposals for that folder—not just the affected files—and falls back to description-only suggestions.
- **Simulation writes absolutely nothing** — `bower.simulate` produces no proposals, logs, journals, or state changes. It is safe to run repeatedly but provides no persistent output.
- **Medical file redaction** — Medical folder contents are never logged, journaled, or surfaced by filename. Only folder paths and file counts appear in apply digests and simulation output.
- **Quiet mode suppresses only the digest** — Enabling quiet mode hides the apply digest output but does not bypass approval requirements, staleness checks, or any safety gate.
- **Small Drive below domain thresholds** — When the Drive has fewer than 5 files or 2 subfolders total, no domain logic activates. Analysis falls entirely on generic outlier rules (depth outliers, name inconsistencies). This is expected — report the Drive as "too small for domain detection" and focus proposals on obvious misplacements (files at root that belong in named folders, duplicate filenames).

- **Shared files appear in modifiedTime queries** — The Drive API `modifiedTime` filter returns shared files/folders that were recently modified by their owners, even though they're outside the user's Drive tree. These appear with `parents: null` and `ownedByMe: False`. Always check `ownedByMe` and parent location before generating proposals. Shared files are never actionable by Bower. See `references/scan-debug.md` → "Shared files in modifiedTime results" for the full triage pattern.

- **Light scan misses bulk-moved files** — The `bower.scan.light` queries by `modifiedTime`, which only catches files *modified* since the last scan. Files that were bulk-moved or bulk-created without recent modification timestamps are invisible to this query. The mandatory structural baseline check (root-level count comparison) before the `modifiedTime` query catches this. Without it, a completely restructured Drive can be reported as "no new files." See the "Light scan structural baseline check" section above.

- **write_file overwrites — use terminal >> for .jsonl append** — The `write_file` tool always overwrites the entire file. For append-only logs (`scan_events.jsonl`, `evidence.jsonl`, `move_log.jsonl`, `undo_log.jsonl`, `feedback_log.jsonl`, `proposals.jsonl`, `health_history.jsonl`, `decisions.jsonl`, `intents.jsonl`, `analysis_events.jsonl`), use `terminal` with `>>` to append, or build the full content and write once. Accidentally overwriting these files destroys history. When appending scan events or evidence entries, prefer: `terminal` > `command: "cat >> path.jsonl << 'EOF'\n{...}\nEOF"` . Never use `write_file` on a `.jsonl` unless you intend to replace the entire file.

- **Drive file/folder IDs are 33 chars — never truncate** — A valid Drive ID looks like `1uBwL8OJ-XrXaBo4Uv9niZ_Qdx3JaqWHS` (33 chars). If you print/echo/copy an ID and it gets truncated to ~24 (a common terminal wrap or manual copy slip), a later `files().get()` returns `HttpError 404 File not found`. The file is **not** missing — your truncated ID is wrong. Always copy the full 33-char ID verbatim. Confirmed 2026-07-17: five parent lookups 404'd solely due to truncated IDs; the real IDs resolved all 21 arrivals correctly. See `references/light-scan-triage.md` for the full triage recipe (resolving `light_scan_latest.json` parent IDs to folder names + grouping arrivals).
- **OAuth invalid_grant — two distinct causes, only one is fatal** — `invalid_grant: Bad Request` surfaces as either (a) a *permanently* dead/revoked refresh token (no recovery short of user re-auth), OR (b) a *recoverable* client_id/refresh-token mismatch: a script loads a cached token file whose embedded `client_id` differs from the `client_id` it passes when constructing `Credentials`. Google rejects the token as issued for another client. Symptom of (b): the *deep* scan works but the *light* scan fails — because deep uses `get_service` (which always pairs the right client secret with the right client_id from `_CLIENTS[account]`), while the broken light-scan script hand-builds `Credentials` with a hardcoded, mismatched `client_id`. Confirmed 2026-06-29 → 2026-07-14: light scans died nightly for 16 days while deep scans succeeded. **Fix for (b):** route the scan through `get_service`; never construct `Credentials` from a token file plus a separate hardcoded client_id. See `references/cron-drive-fallback.md` (ALWAYS-use-get_service note). For (a), handle at the scan entry point: catch `RefreshError`/`HTTPError 401`, write `degraded: google_drive` to `evidence.jsonl`, write an aborted scan event to `scan_events.jsonl`, enter degraded mode, report, and do NOT retry within the same run. If `get_service()` raises `RuntimeError` ("No valid Google credentials found"), that is condition (a) through a different path — handle identically.
- **Interpretter / `requests` missing looks like `invalid_grant`** — `run_light_scan.py` imports `get_service` from `$HERMES_HOME/../indigo/scripts/google_auth.py`, which does `import requests` at module load. If the `python3` the cron/shell invokes lacks `requests` (e.g. it resolves to a project `.venv` whose site-packages only has `googleapiclient`), the scan logs `auth_or_build_failed` with `No module named 'requests'` — which looks EXACTLY like an OAuth failure but is NOT. Tell them apart: the error string is `No module named 'requests'` and no HTTP 400 `invalid_grant: Bad Request` appears. Fix: invoke the script with an interpreter that has BOTH `googleapiclient` and `requests`. On this host the working interpreter is `/usr/bin/python3` (3.14); a stray `python3` on PATH (a project `.venv`, 3.13) did not. Always confirm `python3 -c "import googleapiclient, requests"` succeeds before trusting a cron run. A `auth_or_build_failed` that recurs nightly is the classic signature of this mismatch (cf. the 16-day June 2026 `invalid_grant` episode — same degraded output, different root cause). See `references/cron-drive-fallback.md` → "Operational pitfalls".
- **`search_files` can return phantom paths and miss real files under the profile tree** — During the 2026-07-24 light scan, `search_files` returned relative phantom paths (`<fs-root>/commons/...` that didn't exist from cwd) AND a literal `0 results` for `google_auth.py` under `~/.hermes`, even though `find ~/.hermes -name 'google_auth*'` proved the file at `$HERMES_HOME/../indigo/scripts/google_auth.py` (the `ls`/`find` were truncated or symlink-indexed). This almost caused a false "DEGRADED: auth module missing" conclusion. When a dependency/locator check returns empty or suspicious, DO NOT trust `search_files` alone: confirm with `find ~/.hermes -name '<file>'` and an absolute-path `ls` before concluding anything is missing. The ripgrep-backed index appears to miss files under nested profile dirs and to emit cwd-relative paths.
- **Light-scan query window repeats until the next deep scan** — `run_light_scan.py` sets `cutoff = drive_digest.json["last_updated"]`, which is updated ONLY by `bower.scan.deep` (weekly Sunday run). It is NOT "since the last light scan" or "since yesterday." Consequence: between deep scans, the SAME set of arrivals recurs on every light scan. Identical owned/shared counts day-to-day = "no NEW activity since the last deep scan," NOT a stuck or duplicating scan. Do not conclude the scan is broken when consecutive days return the same owned arrivals — the window simply never advanced. New activity only surfaces after the next deep scan resets `last_updated`. (This is also why a light scan is the wrong tool to detect "what arrived today" — use it for drift-safety + the standing disorganization among already-known arrivals. Run `scripts/bower_light_triage.py` to turn those arrivals into a report.)
- **Timestamp-folder false positives in triage** — when flagging `YYYY-MM-DD_HH-MM-SS`-style export/checkpoint folder piles, use the strict regex `^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$`. A naive `name[:4].isdigit()` test false-positives on legitimately-named folders like `2442 Kuhio Avenue 702` (a Real Estate subfolder). `scripts/bower_light_triage.py` already uses the strict regex.

- **Large Drive founding scans timeout** — On Drives with 10K+ items, a full founding deep scan can exceed the 10-minute cron timeout during folder/file enumeration, and the Drive API may return 500 Internal Errors under heavy pagination. Solution: use the **sampled deep scan** (`commons/data/ocas-bower/deep_scan_sampled.py`): enumerate all folders once (cached to `folder_full_cache.json` for reuse), then sample up to 300 direct children per curated root. Set `scan_coverage: 0.5` in `drive_digest.json`. See `references/large-drive-scanning.md`. **The weekly `bower:weekly-deep` run ALSO uses the sampled strategy** — it never attempts full enumeration on this ~24K-folder Drive. Always wrap Drive API list calls with exponential backoff for 500/503 errors.

- **Bundled `scripts/` scan scripts are unsafe for this Drive** — `scripts/bower_full_scan.py` (the skill's own deep-scan script) does a FULL file enumeration (times out on ~24K folders) AND builds its Drive service via the hardcoded-credential `get_drive_service()` path that triggers `invalid_grant` (see cron-drive-fallback). For real scans, run the maintained scripts in the canonical data dir: `commons/data/ocas-bower/deep_scan_sampled.py` (deep) and `run_light_scan.py` (light). These use `get_service`, honor drift/stale-data handling, and write analyze-compatible artifacts. `scripts/bower_analyze.py` is usable (it reads the canonical `commons/data/ocas-bower` dir) but is stale — prefer it over `bower_full_scan.py`, and never use `bower_full_scan.py` for scan runs.

- **location_outlier move proposals are title-keyword false-positive prone** — `bower.analyze` flags a file as `location_outlier` when its *name* contains a domain keyword (home/work/project/house) and it sits outside that domain's root. For books in **Bookshelf** this is almost always WRONG: e.g. *"Learn Hawaiian at Home"*, *"American House Styles"*, *"Work Like A Spy"*, *"Project Hail Mary"* are ebooks, not Home/Projects documents. Do NOT auto-apply such proposals. Rule of thumb: never move contents of an already-curated semantic root (Bookshelf, Archive) to another domain based on title-substring matches alone — require file *content/type* or explicit domain-folder membership. (Also seen: duplicate proposals — the same file listed twice, e.g. *Project Hail Mary*. The analyzer should dedupe by `source_id`.) Review the pending queue (`bower.proposals.review`) and reject the false positives before any `bower.apply`.

- **Weekly deep scan yields 0 NEW proposals when prior ones persist** — `bower_analyze.py` dedupes against existing `pending`/`approved` proposals, so a routine weekly deep scan legitimately produces 0 new proposals even when 16 are still pending. That is NOT a sign the scan failed. The deliverable of a weekly deep scan is the refreshed `folder_index.json` + `drive_digest.json` (which advances the light-scan `modifiedTime` cutoff) + the still-pending queue — not new proposals. Report "0 new, N pending" as healthy.

- **Stale digest causes permanent drift abort loop** — `drive_digest.json` can get a wrong baseline if a light scan incorrectly concludes that a large-drift event "reverted to baseline." Subsequent scans compare against the wrong baseline and permanently detect 95%+ drift, aborting every run and generating no proposals. Diagnosis: `root_level_file_count` and `root_level_folder_count` in `drive_digest.json` don't match what the Drive API actually returns. Fix: query the Drive API directly (`mimeType = 'application/vnd.google-apps.folder' and parentId = 'root'` for folders; `parentId = 'root' and mimeType != 'application/vnd.google-apps.folder'` for files), then update `drive_digest.json` with the real counts, clear `scan_progress.json`'s `drift_detected: true` flag, and update `folder_index.json` with the actual folder IDs. **Never write a digest update concluding drift has "reverted" unless you verified the root-level counts match the previous baseline.** Confirmed June 2026.

## Support File Map

| File | When to read |
|------|-------------|
| `references/organization_rules.md` | Before every `bower.analyze` run; defines preference inference, pattern promotion, taxonomy inference, all proposal generation rules, permission lookup, feedback suppression, recalibration, scan resume, cap behavior, digest format, and review narrative |
| `references/domains.md` | Before every `bower.analyze` run; defines domain detection, prescriptive/descriptive mode, canonical structures, and per-domain filing rules for Taxes, Projects, Home, Finance, Legal, Medical, Archive, Education |
| `references/analysis_schema.md` | Before `bower.scan.deep` or `bower.analyze`; defines all data schemas including preference profile, folder_index, scan_progress, proposals, move log, undo log, feedback log, and config |
| `references/signal_examples.md` | Before emitting signals; JSON schema examples for all five signal types |
| `references/scan-debug.md` | When debugging scan issues, resume failures, or light scan anomalies |
| `references/command_reference.md` | When you need full command flag descriptions and semantics |
| `references/decision-invariants.md` | Before every `bower.analyze` or `bower.apply` run; safety invariants that govern all operations |
| `references/large-drive-scanning.md` | When founding deep scan on Drive with >10K items or cron timeout; sampled scan strategy, 500 error handling, trade-offs |
| `commons/data/ocas-bower/*.py` (canonical data dir) | The RUNNABLE scan/analyze scripts: `deep_scan_sampled.py` (weekly deep, sampled), `run_light_scan.py` (light), plus artifacts (`folder_index.json`, `scans/`, `proposals.jsonl`, `drive_digest.json`, `evidence.jsonl`). Skill `scripts/` holds stale/unsafe equivalents — see Gotchas. |
| `references/drift-incident-2026-06-14.md` | When light scan detects major drift; lessons from 2026-06-14 restructuring incident, why modifiedTime-only queries miss bulk moves |
| `references/light-scan-triage.md` | After a light scan — resolving parent IDs to folder names and grouping arrivals into a disorganization report (the cron deliverable); includes the 33-char-ID truncation 404 pitfall |
| `references/interactive-menu.md` | When invoked interactively; the full two-level menu structure |
| `references/cron-drive-fallback.md` | When a scheduled scan hits OAuth/auth failures or you're wiring cron Drive access; ALWAYS-use-get_service note and operational pitfalls |
| `references/mcp-drive-tooling.md` | When driving Drive operations through MCP tooling instead of the python client |
| `references/spec-ocas-recovery.md` | Before implementing or auditing Recovery Behavior; the shared OCAS recovery contract (evidence, gap detection, degraded mode, compaction) |
| `references/okrs.md` | When reporting status/trend or reviewing targets; full OKR definitions |

## Scan Debug & Operational Notes

Debug procedures, resume patterns, file layout facts, and light scan lessons.
Full documentation: `references/scan-debug.md`
