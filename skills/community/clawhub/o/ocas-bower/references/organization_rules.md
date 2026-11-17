# Organization Rules

Rules Bower applies when analyzing Drive structure and generating proposals.

---

## Preference inference

During `bower.scan.deep`, Bower builds a preference profile from evidence in the existing structure. Written to `{agent_root}/commons/data/ocas-bower/preference_profile.json` and updated on every deep scan. Human-readable; the user may edit it directly. Any field marked `locked: true` is treated as immutable and never overwritten by inference.

The profile captures:

**Naming conventions** -- Examine filenames across each folder. Detect: date prefix format (YYYY-MM-DD, YYYY-Q#, MM-YYYY, none), capitalization style (Title Case, lowercase, UPPER), separator style (spaces, hyphens, underscores), whether version suffixes appear. Record dominant convention per folder and overall.

**Depth preference** -- Measure median folder depth across the Drive. Median 2 = flat preference; 4+ = deep hierarchy preference. Calibrate proposal aggressiveness accordingly: propose deeper nesting only when median depth supports it.

**Date handling** -- Detect whether dates appear in folder names (year-based folders common in Taxes, Finance, Archive) or filenames or both. Record date position preference (prefix vs. suffix).

**Folder density** -- Measure average file count per folder. Low average (< 10) = fine-grained preference; propose new folders more readily. High average (> 50) = coarse preference; prefer moving into existing broader folders over creating new ones.

**Sacred folders** -- Flag any folder unchanged (no new files, no moves) for 90+ days with 20+ files. Treat as stable archive; never propose moving files out without high confidence and explicit reasoning.

**Domain detection** -- Identify which domains are present. See `references/domains.md` for detection criteria and canonical structures.

The profile is rebuilt from scratch on every deep scan, then reconciled against user-locked fields. Locked fields are preserved; all others are updated from current evidence.

---

## Pattern promotion

Bower learns from your approval and execution history to auto-approve future proposals matching established patterns.

### Promotion threshold

A pattern is promoted to auto-approve when: 3 or more proposals sharing the same `pattern_key` (`'{outlier_class}:{source_folder_label}:{destination_folder_label}'`) have been executed with no subsequent undo within 30 days.

Promoted patterns are stored in `preference_profile.json` under `auto_approved_patterns`. Each entry records: `pattern_key`, `promoted_at`, `supporting_proposal_ids`, `confidence` (starts at `med`; upgrades to `high` after 6 executions with no undos).

### Auto-approve behavior

During `bower.analyze`, after generating proposals, check each proposal's `pattern_key` against `auto_approved_patterns`. If a match exists: set `status: approved` immediately rather than `pending`. Log `auto_approved: true` on the proposal record.

Auto-approved proposals still pass the staleness gate and permission check before execution. They do not bypass safety rules -- only the human approval step.

### Demotion

If a promoted pattern receives an undo or reject: demote confidence by one level. At two undos/rejects: remove the pattern from `auto_approved_patterns` and add it to `feedback_log.jsonl` with `feedback_type: demotion`. Bower will not re-promote the same pattern until it accumulates 5 new clean executions.

### User visibility

`bower.status` lists active auto-approved patterns and their confidence. `bower.feedback.clear --pattern key` removes a pattern from auto-approve immediately.

---

## Taxonomy inference

Bower infers taxonomy from the preference profile and existing folder structure. Generic logic applies to all folders not identified as a known domain.

1. Identify top-level folders. These define the primary taxonomy.
2. Identify second-level folders. These define subcategories.
3. Use the preference profile's naming conventions and depth preference to calibrate proposal style.
4. All proposals must place files into folders that already exist or are themselves proposed in the same analysis run (folder creation proposals always execute first).
5. For folders identified as a known domain, apply domain-specific logic from `references/domains.md` before generic outlier logic.

Never create more than two new folder levels in a single analysis run. If the needed hierarchy is deeper, propose the shallowest reasonable destination and flag the nesting gap.

Never propose a naming convention that contradicts the preference profile's dominant convention for that folder's parent.

---

## Outlier classification

A file is an outlier if any of the following is true:

**Location outlier** -- The file's parent folder does not match the file's apparent category based on name, mimeType, date, or content summary. Example: a PDF invoice living in a folder named "Photos".

**Content mismatch** -- The file's content summary places it in a different category than its current folder. This signal is only used when a content summary is available (see Content classification below). Content mismatch alone is never sufficient for a `high` confidence proposal; it must be corroborated by at least one structural signal (name, mimeType, or location).

**Depth outlier** -- The file is at Drive root level and is not a shared shortcut, a pinned reference doc, or a folder. Lone files at root are almost always misplaced.

**Name inconsistency** -- The file's name does not match the naming convention of its siblings by more than one standard deviation. Example: siblings are named `YYYY-MM-DD Report.docx` and this file is named `draft final v3 ACTUAL.docx`.

**Stale staging** -- The file is in a folder named "Inbox", "Unsorted", "Staging", "To Sort", or similar, and has not been modified in more than 30 days.

**Duplicate candidate** -- Two or more files share the same name and mimeType in different folders. Flag but do not automatically propose a merge. Propose consolidation to one folder only.

---

## Content classification

During `bower.scan.deep`, Bower reads and summarizes the content of non-folder files to improve placement accuracy.

### What to read

Read content for files with these mimeTypes: Google Docs (`application/vnd.google-apps.document`), Google Sheets (`application/vnd.google-apps.spreadsheet`), Google Slides (`application/vnd.google-apps.presentation`), plain text (`text/plain`), PDF (`application/pdf`), and common Office formats (`.docx`, `.xlsx`, `.pptx`).

Skip: folders, shortcuts, binary files without readable text (images, audio, video, archives), files larger than 5MB, files modified within the last 24 hours.

### What to extract

For each readable file, extract a content summary of no more than 150 words covering: apparent document type (invoice, contract, meeting notes, code, research, etc.), primary topic or subject, any named entities (people, companies, projects, dates) that suggest a home folder.

Store the summary in the structural model under the file record. See `analysis_schema.md` for the schema field.

### How to use content in proposals

Content summaries are one signal among several. Apply this weighting:

- Content alone: never sufficient to generate a proposal
- Content + name signal: sufficient for `med` confidence
- Content + structural signal (mimeType, location pattern, depth): sufficient for `high` confidence if destination is unambiguous
- Content contradicts other signals: downgrade confidence tier by one level and note the conflict in reasoning

Summarize content reading outcomes in the analysis event record (`content_read_count`, `content_skip_count`).

### Content privacy boundary

Bower reads file content only to extract placement signals. Content summaries stored in the structural model must be limited to the 150-word extract. Full file text must not be written to any log, journal, or output file.

---

## Confidence tier assignment

**High** (auto-approvable with `--tier high`, or auto-approved via pattern promotion):
- Destination is unambiguous given the existing taxonomy or domain logic
- File is a location or depth outlier with a single clear destination
- Content corroborates at least one structural signal pointing to the same destination
- Folder creation proposals (required preconditions)
- Stale staging files with a clear category match
- Domain-prescriptive proposals where the domain is clearly started (see `references/domains.md`)

**Med**:
- Destination is plausible but two or more reasonable candidates exist
- Content matches destination but structural signals are ambiguous
- Name inconsistency outliers (rename proposals always start at med before content corroboration)
- Duplicate candidate consolidation
- Domain-descriptive proposals (inferring within your existing variant)

**Low**:
- File is near a folder boundary (could belong in either of two sibling folders)
- File was recently modified (within 7 days) -- may be actively in use
- No clear destination exists; proposal is speculative
- Content contradicts structural signals (conflict noted in reasoning)

Domain-prescriptive proposals (domains clearly started) begin at `high`. Domain-descriptive proposals begin at `med`. Both are subject to the standard downgrade rules (content conflict, sacred folder, recent modification).

---

## Forbidden move categories

Never propose moving:
- Top-level folders (only their contents can move)
- Files or folders that are Shared Drives roots
- Files with `starred: true` unless confidence tier is `high` and reasoning is explicit
- Files in `Trash` (already excluded from structural model)
- Shortcuts (mimeType `application/vnd.google-apps.shortcut`)
- Files modified within the last 24 hours
- Any file where the move would change the effective permission set (see Permission safety below)

Never propose renaming:
- Folders at any depth (folder renames are out of scope)
- Files modified within the last 24 hours
- Files where the existing name follows a clear convention shared by siblings

---

## Description generation

During `bower.scan.deep`, after reading file content, generate a proposed Drive description for each readable file.

### What a good description contains

50-120 words covering: document type, primary subject or purpose, key named entities (people, companies, projects), date range if apparent, and any terms that would aid future search or classification. Written in plain prose, not bullet points. No internal file paths or system metadata.

### When to propose a description write

**Auto-write (no approval required):** the file's existing Drive description field is null or empty.

**Propose overwrite (approval required):** the file already has a description, and Bower's generated description is meaningfully better. Apply the "meaningfully better" test:
- Bower's description is at least 30% longer in substantive content (not padding)
- Bower's description includes named entities or dates absent from the existing description
- The existing description is a generic placeholder (e.g., "Untitled", "See file", a single word)

If none of these conditions are met, do not propose an overwrite. Preserve the existing description.

### Approval gate

Auto-writes execute in `bower.apply` without appearing in `proposals.jsonl`. They are logged to `move_log.jsonl` with `operation: describe_auto` and the previous value (null) preserved.

Overwrite proposals appear in `proposals.jsonl` with `proposal_type: describe_overwrite`, `confidence_tier: med`, and require explicit approval. The existing description is stored in `previous_value` at proposal generation time.

### Staleness check for overwrites

Before executing a description overwrite, fetch the file's current description from Google Drive. If it has changed since the proposal was generated, mark the proposal `skipped` with `skip_reason: description_changed`.

---

## Rename rules

Renames are high-risk: they can break external links, document references, scripts, and automations. Apply extreme conservatism.

### When to propose a rename

Propose a rename only when all of the following are true:
- Confidence tier is `high` (renames at `med` or `low` are forbidden)
- The existing name is objectively poor: contains "untitled", "copy of", "draft", "v2/v3/final/new" suffixes, or is a system-generated default (e.g., "Document", "Spreadsheet")
- A clearly better name can be derived unambiguously from file content and context
- The proposed name follows the naming convention of sibling files in the same folder
- The file has not been modified within the last 7 days

### Proposed name construction

Derive the proposed name from: document type, primary subject, date (YYYY-MM-DD format if a clear date is present), and file extension. Match sibling naming convention exactly if one exists. Keep names under 80 characters.

Example: `Copy of Q3 Financial Review final v2.xlsx` → `2026-Q3 Financial Review.xlsx` (if siblings follow date-prefixed convention).

### Rename forbidden categories (beyond the existing forbidden list)

Never propose renaming:
- Any file whose name is referenced by another file's content (detectable if the filename appears verbatim in any other file's content summary)
- Files in shared folders where others may depend on the name
- Folders at any depth

---

## Permission safety

Google Drive inherits permissions from parent folders. Moving a file changes its inherited permissions to match the destination folder. This can silently expand access (more people can see it) or reduce access (people lose visibility). Both outcomes are forbidden.

### Permission comparison rule

Before generating any move proposal, compare the effective permission set of the file's current parent folder against the effective permission set of the proposed destination folder.

A permission set is the union of: the folder's direct permissions plus all permissions inherited from its ancestors.

Represent each permission as a tuple: `(email_or_domain, role)` where role is one of `reader`, `commenter`, `writer`, `owner`.

**The move is forbidden if the destination permission set differs from the source permission set in any way** -- additions, removals, or role changes all block the proposal.

The only exception: if the file itself has explicit permissions that override inherited ones, compare only the inherited layers (the folder chain), not the file's own explicit grants.

### How to capture permission data during scan

During `bower.scan.deep` and `bower.scan.light`, fetch the `permissions` resource for every folder. Store each folder's effective permission set (direct + all inherited, deduplicated and flattened) in the structural model's `folder_index` keyed by folder ID. This index is the authority for permission comparison during analysis -- do not walk parent chains at analysis time, use the pre-built index.

Permission fetching adds latency. Fetch folder permissions only; skip files that are not folders. If permissions are unavailable, set `permissions_available: false` in the scan event record and suppress all move proposals for that scan. Do not generate proposals without permission data.

To compare permissions for a proposed move: look up `folder_index[source_parent_id].effective_permissions` and `folder_index[destination_id].effective_permissions`. Compare as sets of `(type, emailAddress|domain, role)` tuples. Any difference blocks the proposal.

### Blocked proposal handling

When a move is blocked by the permission rule, do not generate a proposal. Append a record to `analysis_events.jsonl` under `permission_blocked_count`. Do not surface blocked proposals to the user unless they run `bower.analyze --show-blocked`.

---

## Proposal ordering

Proposals in a single apply run execute in this order:
1. Folder creation (ensures destinations exist)
2. High-confidence moves
3. High-confidence renames
4. Med-confidence moves
5. Med-confidence description overwrites
6. Low-confidence moves

Description auto-writes (empty fields) execute before all of the above, outside the approval queue.

Within a tier, order by: depth outliers first, then location outliers, then stale staging, then name inconsistencies, then content mismatches.

---

## Proposal deduplication

Before appending new proposals to `proposals.jsonl`, check for existing proposals with:
- Same `source_id` and `status` in (`pending`, `approved`)

If a pending or approved proposal already targets this file, skip generating a new one. Do not create duplicate proposals for the same file.

---

## Proposal expiry

Proposals expire if not approved within `proposal_expiry_days` (default: 14 days, configurable). Expired proposals have their status set to `expired` during the next `bower.analyze` run. Expired proposals are never executed.

During `bower.analyze`, before generating new proposals, scan `proposals.jsonl` for any `pending` proposals older than `proposal_expiry_days` and mark them `expired`. Log the count in the analysis event record under `expired_count`.

---

## Pre-apply staleness gate

Before executing any proposal in `bower.apply`, verify the source file is still at its scanned location:

1. Fetch the file's current parent from Google Drive using its `source_id`.
2. Compare the current parent path to `source_path` in the proposal.
3. If they differ, mark the proposal `skipped` with `skip_reason: source_moved` and log the discrepancy. Do not execute the move.
4. Continue with remaining proposals.

This check runs per-proposal immediately before each move, not once at the start of the apply run.

---

## Proposal cap

A single `bower.apply` run executes at most `apply_cap` proposals (default: 25, configurable in `config.json`). If more approved proposals exist than the cap allows, execute the highest-confidence proposals first (folder creations, then high, then med, then low) and leave the remainder in `approved` status for the next run.

Notify the user how many proposals were held back and how many remain.

---

## Scan drift detection

At the start of `bower.scan.light`, compare the current Drive state to the existing structural model:

1. Sample up to 200 previously-scanned files by fetching their current parent from Google Drive.
2. Count how many have a parent that differs from the structural model.
3. If the drift rate exceeds 15%, abort the light scan. Log `drift_rate` and `abort_reason: drift_threshold_exceeded` to `scan_events.jsonl`. Do not generate proposals.
4. Notify the user that a deep scan is required before analysis can continue.

If the structural model does not exist (first run or deleted), always require a deep scan.

---

## Confidence recalibration

Bower tracks proposal precision per outlier class over rolling 30-run windows. After every `bower.apply`, update `preference_profile.json` under `class_precision`:

```
class_precision[outlier_class] = executed_count / (executed_count + undone_count)
```

At analysis time, apply recalibration adjustments before assigning confidence tiers:

- If `class_precision` for an outlier class falls below 0.60: downgrade all proposals of that class by one tier
- If `class_precision` falls below 0.40: suppress that class entirely until precision recovers above 0.50 over 10+ executions
- If `class_precision` exceeds 0.90 for 20+ executions: eligible for pattern promotion regardless of the standard 3-execution threshold

Log recalibration adjustments in the analysis event record under `recalibration_adjustments`.

---

## Reversibility note

Every executed operation is logged in `move_log.jsonl` with `previous_value` preserved. Use `bower.undo` to reverse programmatically. Pattern promotion undos also trigger demotion in `preference_profile.json`.

---

## Feedback learning and proposal suppression

Bower learns from user undos and explicit rejections to avoid repeating proposals the user has rejected.

### Recording feedback

Every `bower.undo` call and every `bower.proposals.reject` call appends a record to `feedback_log.jsonl`. The record captures `pattern_key` as a composite: `'{outlier_class}:{source_folder_label}:{destination_folder_label}'` where folder labels are the normalized folder name tokens (lowercase, no special characters).

Example: a user undoes moving a file from "Projects/Active" to "Archive" → `pattern_key: "location:projects_active:archive"`.

### Suppression at analysis time

At the start of `bower.analyze`, load `feedback_log.jsonl` and build a suppression map: for each `pattern_key`, count feedback events. Apply suppression tiers:

- 1 feedback event: downgrade proposed confidence by one tier for this pattern
- 2 feedback events: suppress `low` and `med` proposals matching this pattern
- 3+ feedback events: suppress all proposals matching this pattern (do not generate)

Suppression applies only to the specific source→destination folder combination, not globally. Bower may still propose moving a file from a different source to the same destination.

Log `suppressed_by_feedback_count` in the analysis event record.

### Surfacing suppression to the user

When `bower.status` is called, include a "Learned suppressions" count. When `bower.proposals.review` is called, note at the bottom how many potential proposals were suppressed due to feedback. The user can clear suppressions with `bower.feedback.clear [--pattern key] [--all]`.

---

## Incremental scanning (deep scan)

Large Drives (50k+ files) cannot be scanned in a single session. Deep scans work in three phases, with progress saved to disk after each folder. Scanning can span multiple sessions — kill the process at any point and resume later.

### Phase 1: Tree discovery

List all folders in Drive (`mimeType = 'application/vnd.google-apps.folder'`, paginated). Build `folder_index.json` with the full folder tree — paths, depths, permissions. This is fast even for huge Drives because folder count is a small fraction of file count.

Write `scan_progress.json` with `phase: folder_scanning` and all top-level folders listed in `pending_folders`, sorted largest first (folders with the most descendants processed first for maximum organizational signal early).

### Phase 2: Folder scanning

Process one top-level folder tree at a time:
1. Pop the next folder from `pending_folders` in `scan_progress.json`.
2. Set `current_folder` to that folder ID.
3. List all files in that folder tree (Drive API `parents` query, paginated).
4. For each file: read content if applicable, build file record.
5. Write completed results to `scans/{folder_id}.json`.
6. **Update `drive_digest.json`** with this folder's contribution (see Drive Digest below).
7. Move the folder ID from `pending_folders` to `scanned_folders`.
8. Update `total_files_scanned` and `last_checkpoint_at`.

**Within-folder checkpointing:** For large individual folders (thousands of files), save `current_folder_page_token` in `scan_progress.json` periodically. On resume, the folder scan continues from the saved page token and appends to the existing `scans/{folder_id}.json`.

**Session time awareness:** Before starting each folder, estimate remaining session time. If insufficient for the next folder, stop gracefully and report progress.

Files at the Drive root (no parent folder) are collected in `scans/_root.json`.

### Phase 3: Completion

When all folders are scanned, set `phase: complete` in `scan_progress.json`. The `drive_digest.json` now represents the full Drive. Run `bower.analyze` using the digest for holistic decisions and individual scan files for per-file proposal generation.

---

## Drive digest (drive_digest.json)

The drive digest is a lightweight summary of the entire Drive's organizational state, built incrementally as each folder is scanned. It is small enough to hold in memory at all times and contains everything needed for holistic analysis — without any individual file records.

The digest is updated after each folder scan completes. It is never built from scratch by reading all scan files; instead, each folder's contribution is merged in as it finishes. This means the digest is always current with whatever has been scanned so far.

### What the digest captures

**Per-folder statistics** (one entry per folder in the Drive, not just top-level):
```json
{
  "folder_id": "string",
  "path": "string",
  "depth": "number",
  "file_count": "number",
  "subfolder_count": "number",
  "last_modified": "ISO 8601 -- most recent modifiedTime of any file in this folder",
  "mime_type_distribution": {"application/pdf": 3, "application/vnd.google-apps.document": 12},
  "naming_pattern": "YYYY-MM-DD prefix | title-case | mixed | null",
  "date_convention": "prefix | suffix | folder-name | none",
  "detected_domain": "taxes | finance | projects | null",
  "domain_confidence": "high | med | low | null",
  "has_year_subfolders": "boolean",
  "sacred": "boolean -- unchanged 90+ days with 20+ files",
  "outlier_count": "number -- files that don't match the folder's dominant pattern",
  "root_files_count": "number -- files directly in this folder (not in subfolders)"
}
```

**Drive-wide aggregates:**
```json
{
  "total_files": "number",
  "total_folders": "number",
  "median_depth": "number",
  "median_files_per_folder": "number",
  "dominant_naming": "YYYY-MM-DD prefix | title-case | mixed",
  "dominant_date_convention": "prefix | suffix | folder-name | none",
  "domains_detected": [
    {"domain": "taxes", "root_path": "Finance/Taxes", "mode": "prescriptive", "confidence": "high"},
    {"domain": "projects", "root_path": "Projects", "mode": "descriptive", "confidence": "high"}
  ],
  "sacred_folders": ["folder_id_1", "folder_id_2"],
  "root_level_file_count": "number -- files at Drive root with no parent",
  "stale_staging_count": "number -- files in staging-like folders >30 days old",
  "description_coverage": "number -- fraction of readable files with non-empty description",
  "cross_folder_patterns": [
    {"pattern": "tax documents in 3+ locations", "folders": ["folder_id_a", "folder_id_b", "folder_id_c"]},
    {"pattern": "duplicate filenames across folders", "count": 14}
  ],
  "scan_coverage": "number -- fraction of top-level folders scanned (0.0 to 1.0)",
  "last_updated": "ISO 8601"
}
```

### How the digest enables holistic analysis

Without the digest, `bower.analyze` would need to load all scan files to answer questions like "what naming convention dominates across the Drive?" or "are there tax documents scattered across multiple folders?" The digest pre-computes these cross-cutting summaries.

Analysis uses the digest for:
- **Preference inference**: naming conventions, depth preference, folder density, date handling — all derived from the digest's aggregates and per-folder stats.
- **Domain detection**: the digest tracks detected domains per folder; cross-folder patterns surface domain fragmentation (e.g., tax files in 3 places).
- **Sacred folder identification**: the digest flags folders unchanged for 90+ days.
- **Outlier context**: when evaluating a file in a specific folder, the digest provides the folder's dominant pattern, the Drive-wide dominant pattern, and whether the file's folder is part of a recognized domain.
- **Cross-folder duplicate detection**: the digest tracks filename collisions across folders.

Analysis uses individual `scans/{folder_id}.json` files for:
- **Per-file proposal generation**: the actual file records with content summaries, permissions, and metadata needed to generate specific move/rename/describe proposals.
- **Permission comparison**: file-level and folder-level permission sets for move safety checks.
- **Staleness checks**: individual file `modifiedTime` values.

This two-layer approach means `bower.analyze` loads one small digest file for holistic reasoning, then loads individual scan files one at a time for per-folder proposal generation. Memory usage stays bounded.

### Digest updates during light scan

`bower.scan.light` updates the digest for any folder containing recently modified files. It adjusts the per-folder stats and recalculates Drive-wide aggregates. The digest stays current without a full deep scan.

### Partial digest

When not all folders have been scanned, `scan_coverage < 1.0` in the digest. Analysis can still run — it uses whatever data is available and notes the coverage gap. As more folders are scanned in subsequent sessions, the digest fills in and analysis improves.

### Resume behavior

On `bower.scan.deep` start:
1. Check for existing `scan_progress.json`.
2. If found with `phase != complete` and less than 7 days old: resume. Report "Resuming scan: {N} of {M} folders scanned ({files_scanned} files). Continuing..."
3. If found but older than 7 days: delete `scans/` contents and start fresh.
4. If not found: start fresh with Phase 1.

### Partial analysis

`bower.scan.deep --analyze-now` runs `bower.analyze` on whatever folders have been scanned so far, without waiting for all folders to complete. The analysis notes which folders are not yet included. Useful for large Drives where the user wants early results.

---

## Apply cap clarification

The `apply_cap` (default: 25) applies to approved proposals only. Description auto-writes are subject to a separate cap: `describe_auto_cap` (default: 50, configurable). Both caps are independent and both enforce limits within a single `bower.apply` run.

If either cap is hit, notify the user with the exact counts: "Applied N moves/renames, M description writes. X approved proposals and Y auto-writes held for next run."

---

## Apply digest

After every `bower.apply` run, produce a human-readable digest summarizing what was done. The digest is printed to the user and appended to `{agent_root}/commons/data/ocas-bower/reports/` as a dated Markdown file.

### Digest format

```
Bower applied {date}
─────────────────────────────────────────────
Moved:       N files
Renamed:     N files
Described:   N files (auto), N files (approved overwrites)
Skipped:     N proposals (source moved since scan)
Held back:   N approved proposals (cap reached)
─────────────────────────────────────────────
Highlights:
  • Moved 8 invoices from root to Finance/Invoices/2026
  • Renamed 2 files: "Copy of Budget final v3" → "2026-Q1 Budget"
  • Wrote descriptions to 14 files in Projects/Active
─────────────────────────────────────────────
To undo the last apply: bower.undo --last {N}
```

Generate highlights by grouping executed proposals by destination folder and summarizing in plain language. Maximum 5 highlight lines. Lead with the most impactful group (highest file count).

---

## Review narrative

`bower.proposals.review` does not just list proposals. It opens with a one-paragraph Drive health narrative before the proposal list:

"Your Drive has {N} outliers across {M} folders. The most common issues are {top 3 outlier classes}. {N} files have been sitting in staging folders for over 30 days. {N} files at root level have no folder home. Confidence breakdown: {high} high, {med} med, {low} low proposals ready for your review."

Then list proposals grouped by destination folder (not by confidence tier), so the user can see "here is everything Bower wants to move into Finance/Invoices" as a coherent group rather than scattered individual proposals. Within each group, show confidence tier as an indicator.

---

## Quiet mode

When `quiet_mode: true` in config:
- `bower.apply` executes without printing a digest unless at least one proposal failed, was skipped, or a cap was hit.
- Arrival detection auto-applies high-confidence pattern matches within the light scan session without prompting.
- No behavioral change to what requires approval -- only output is suppressed for clean runs.

Quiet mode is off by default. Enable with `bower.preferences.quiet --on`.

---

## Founding run

The founding run is a one-time bootstrap triggered by `bower.scan.deep --founding`. It runs only once; `founding_run_complete: true` is set in config on completion. Large Drives may require multiple sessions to complete — progress is saved automatically.

### Multi-session founding flow

1. First invocation: tree discovery (fast), then begin scanning folders largest-first.
2. After each folder: results written to `scans/{folder_id}.json`, progress saved to `scan_progress.json`.
3. If session time runs low, stop gracefully and report:
   "Scanned {N} of {M} top-level folders ({files} files). Run `bower.scan.deep --founding` again to continue."
4. Subsequent invocations: resume from `scan_progress.json`. No work is repeated.
5. When all folders are scanned: run `bower.analyze`, proceed to batch approval.

### Batch approval (after scan completes)

1. Group all high-confidence proposals by domain (and "General" for non-domain proposals).
2. Present to the user as a single batch grouped by domain. Show counts and a 3-5 item sample per group.
3. Accept options: "Accept all", "Review by domain" (approve/reject per group), "Reject all".
4. Execute the accepted subset immediately.
5. Grant pattern promotion credit for all executed proposals as if each had 3 prior clean executions. Set `execution_count: 3` on each promoted pattern entry in `preference_profile.json`.
6. This means Bower arrives at steady-state auto-approval behavior after a single founding run rather than needing 3 cycles per pattern.

If the founding run is rejected entirely, Bower falls back to normal first-use flow without promotion credit.

### Early analysis

`bower.scan.deep --founding --analyze-now` runs analysis on whatever folders have been scanned so far, without waiting for all folders. The analysis notes which top-level folders are not yet included. This lets the user see early results and start approving patterns while remaining folders are scanned in future sessions.

---

## Arrival detection rules

Arrival detection runs after every `bower.scan.light`. It evaluates only files that are new or modified since the previous scan (determined by `modifiedTime` delta vs. structural model).

For each arriving file:
1. Classify using domain logic first, then generic rules.
2. Derive `pattern_key`.
3. Check against `auto_approved_patterns` in preference profile.
4. If match found with `confidence: high`: create proposal with `status: approved` and `auto_approved: true`. If quiet mode is on, apply immediately within the current session (subject to `apply_cap`).
5. If match found with `confidence: med`: create proposal with `status: pending`. Do not auto-apply.
6. If no match: create proposal with `status: pending` as normal.

Arrival detection does not run analysis on the entire Drive -- only on the arriving files. It uses the existing structural model for context (folder taxonomy, permission index, sacred folder list).

Files arriving in a sacred folder: skip arrival detection. Do not disturb sacred folders based on arrival alone.

---

## Simulation rules

`bower.simulate` is a pure read operation. These rules are absolute:

- No writes to any file under `{agent_root}/commons/`.
- No journal written.
- No proposals appended to `proposals.jsonl`.
- No analysis events appended.
- The structural model and preference profile are read but never updated.

Simulation uses the same analysis pipeline as `bower.analyze` with one difference: the output is a narrative report rather than persisted proposals. Apply the same domain logic, generic rules, confidence tiers, permission checks, and forbidden categories. The simulation report must accurately reflect what `bower.analyze` would actually produce for the specified folder.

If no structural model exists: note in the report header that preferences could not be applied and results are based on domain logic and generic rules only. Do not block simulation -- proceed with reduced confidence.

If the specified path does not exist in Drive: return an error immediately without reading anything else.

Simulation depth: default is full recursive depth within the specified folder. `--depth N` limits recursion to N levels below the specified path.
