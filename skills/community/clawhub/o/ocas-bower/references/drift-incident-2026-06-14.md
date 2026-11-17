# Light Scan Drift Detection — 2026-06-14 Incident

## What happened

The Drive underwent a massive structural restructuring between the 2026-06-06 deep scan and the 2026-06-14 light scan:

- **Before:** 9 files, 7 folders (total Drive)
- **After:** 89+ files, 12+ folders at ROOT LEVEL ALONE (nextPageToken indicated more beyond first 100)
- **Trigger:** Light scan on 2026-06-14 queried `'root' in parents` as a baseline check and found 101 items vs. the expected ~6

## Root cause

The previous light scan (2026-06-13) only queried `modifiedTime > '2026-06-06T17:00:00Z'`. All 89+ files at root had modification dates *before* that cutoff (many from April 2026), so the query returned 0 results. The scan reported "no new files" while the Drive was completely restructured.

The files were likely moved to root level by an external process (Google Drive sync, migration tool, or bulk move) without updating their `modifiedTime`.

## Detection method that worked

The 2026-06-14 scan performed a **structural baseline check** as its first step:
1. Query `'root' in parents and trashed = false` with `pageSize=10`
2. Found 101 items with `nextPageToken` present
3. Compared against `drive_digest.json` → `root_level_file_count: 3`
4. Drift rate: 95% — exceeded 15% threshold → scan aborted, deep scan requested

## Lesson encoded

Added mandatory structural baseline check to `bower.scan.light` execution flow in SKILL.md. Every light scan must compare root-level counts against `drive_digest.json` baseline before processing `modifiedTime` queries.

## Files involved

Key folders now at root (previously nested or nonexistent):
- `CA TAX`, `Tax temp` — tax documents scattered
- `2026 Open Enrollment` — benefits
- `Hermes` — agent-related
- `Opal`, `Prime Meridian` — project folders
- `Post IPO` — financial planning
- `Scans` — document scans
- `Archive`, `Bookshelf`, `Home`, `Photobooth` — existing folders

Files needing organization:
- 10 untitled files (7 docs, 3 sheets)
- 3× duplicate "the agent Container Test" spreadsheets
- 11 medical/health files at root with no medical folder
- 18 agent/dev files mixed with personal documents
