# Light Scan Triage — turning arrivals into a disorganization report

`bower.scan.light` writes `light_scan_latest.json` but its `owned_files` /
`shared_files` arrays record only each item's **parent folder ID** (first element
of `parents`), not the folder name. To produce a human-readable "what arrived and
where" report (the deliverable for a cron-driven light scan), you must resolve
those parent IDs to names and group the arrivals.

This is a read-only, post-scan step. It makes no changes — `bower.apply` is the
only writer.

## Auth
Use the only known-good path (see `references/cron-drive-fallback.md`):
```python
import sys
sys.path.insert(0, "$HERMES_HOME/../indigo/scripts")
from google_auth import get_service
svc = get_service("drive", "v3",
                  ["https://www.googleapis.com/auth/drive"],
                  account="<user-google-email>")
```

## Triage recipe
1. Load `light_scan_latest.json`; note `query_since` (the cutoff) and the
   `owned_count` / `shared_count` split.
2. Collect distinct parent IDs from `owned_files[*].parents[0]` (and shared, if
   surfacing them).
3. `svc.files().get(fileId=pid, fields="id,name,mimeType").execute()` for each.
4. Group arrivals by resolved parent name; count; list contents.
5. Flag disorganization signals:
   - **timestamp-named folder piles** (`2026-05-07_12-00-01` style) — likely
     auto-generated export/checkpoint trees needing a dated-archive convention.
   - **scatter** — assets that belong under a sibling folder (e.g. `Life101.*`
     assets loose in a person's folder while a dedicated `Life 101` folder exists).
   - **naming inconsistency** — a person's name used as a top-level project root
     alongside theme-based roots.

Shared arrivals are correctly excluded from action; just name the owner so the
cron report can say "N shared, non-actionable (owner: x)".

## PITFALL — Drive IDs are 33 chars; never truncate them
A Google Drive file/folder ID looks like
`1uBwL8OJ-XrXaBo4Uv9niZ_Qdx3JaqWHS` (33 chars). If you print/echo/copy an ID
and it gets **truncated to 24** (a common terminal/display wrap), a later
`get()` returns `HttpError 404 File not found`. The file is fine — your truncated
ID is wrong. Always copy the full 33-char ID verbatim. In the 2026-07-17 run,
five parent lookups 404'd purely because the printed IDs were truncated; the real
IDs resolved all 21 arrivals correctly.

## What a light scan does NOT do
- It never writes proposals. `bower.analyze` (run on the Sunday deep scan, or on
  request) converts arrivals into ranked, reviewable proposals.
- Detection-only even when `quiet_mode` is off. No auto-apply outside the
  `quiet_mode + promoted-pattern` path.
- Owned arrivals can legitimately be **zero** between runs (e.g. the 2026-07-16
  light scan saw 0 owned arrivals; the next day's saw 21, all timestamped that
  same day). Zero is not a failure — it means no new owned content arrived.
