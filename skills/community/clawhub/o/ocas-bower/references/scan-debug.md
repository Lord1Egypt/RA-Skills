# Bower Scan Debug & Resume

## Critical File Layout Facts

### folder_index.json — Single JSON Object (Not JSONL)
```json
{"scan_timestamp":"...","total_folders":73900,"folders":[{"id":"...","name":"..."}]}
```
Load with `json.load(f)`, NOT line-by-line.

### scans/ — Authoritative Source of Truth
Each `.json` file = one scanned folder. Count files directly:
```bash
ls {agent_root}/commons/data/ocas-bower/scans/ | wc -l
```

### scan_progress.json — Unreliable for Resume
The `scanned_folders` array is often stale/empty even when `scans/` has files. Always use `scans/` as ground truth.

## Diagnosis Commands

```python
# Count actual scanned folders
import json
from pathlib import Path
scanned = len(list(Path("{agent_root}/commons/data/ocas-bower/scans").glob("*.json")))

# Total folders
with open("{agent_root}/commons/data/ocas-bower/folder_index.json") as f:
    d = json.load(f)
total = d.get("total_folders")
remaining = total - scanned
```

## Resume Pattern

```python
from pathlib import Path
import json

scans_dir = Path("{agent_root}/commons/data/ocas-bower/scans")
folder_index = json.load(open("{agent_root}/commons/data/ocas-bower/folder_index.json"))

# Build scanned set from scans/ directory
scanned_ids = {f.stem for f in scans_dir.glob("*.json")}

# Find unscanned folders
unscanned = [fd for fd in folder_index["folders"] if fd["id"] not in scanned_ids]
```

## Two-Phase Deep Scan

**Phase 1**: Tree discovery → `folder_index.json`
**Phase 2**: Scan each folder → `scans/{folder_id}.json`
**Content enrichment**: `bower_read_contents.py` → `content_summaries.jsonl`

All three produce distinct outputs. Proposal generation requires Phase 2 + content.

## Scripts Location

- `bower_resume_scan.py` — resumable folder scanner
- `bower_read_contents.py` — content enrichment
- `bower_full_scan.py` — full scan with content reading

Run in background:
```bash
cd {agent_root}/commons/data/ocas-bower
nohup python3 bower_resume_scan.py > /tmp/bower_resume.log 2>&1 &
echo "PID: $!"
```

## Light Scan Lessons

### OAuth invalid_grant — Drive access permanently broken until re-auth

**Symptom:** Light scan (or any Drive API call) fails with `google.auth.exceptions.RefreshError: ('invalid_grant: Bad Request')` or `HTTP 401 UNAUTHENTICATED`. The `creds.valid` property may still return `True` even though the token is unusable — the library checks internal state, not the actual token expiry.

**Cause:** The OAuth refresh token has been revoked or expired at the Google side. This happens when:
- The user revokes app access in Google Account settings
- The refresh token expires (Google tokens can expire after 6+ months of inactivity)
- The OAuth client was deleted or regenerated in Google Cloud Console

**Diagnosis:**
```python
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import json, urllib.request

# Load token file
d = json.loads(Path("<gworkspace-creds>/credentials/<user-google-email>.json").read_text())
print(f"Token expiry: {d.get('expiry')}")  # If past, token is expired

# Test with direct REST API (bypasses library auto-refresh)
req = urllib.request.Request(
    "https://www.googleapis.com/drive/v3/about?fields=user",
    headers={"Authorization": f"Bearer {d['token']}"}
)
try:
    resp = urllib.request.urlopen(req, timeout=15)
    print("Token still valid")
except urllib.error.HTTPError as e:
    print(f"Token rejected: {e.code} {e.read().decode()[:200]}")
```

**Handling in Bower:**
1. Catch `RefreshError` and `HTTPError 401` at the scan entry point
2. Write `degraded: google_drive` to evidence.jsonl with the specific error
3. Write an aborted scan event to scan_events.jsonl
4. **Do NOT retry** — the refresh token will not recover without user interaction
5. Enter degraded mode: produce a partial Drive health report using last known state from `scan_progress.json` and `drive_digest.json`
6. The cron job will retry next cycle; if auth is restored by then, the scan will succeed automatically

**Recovery requires user interaction:** Re-run OAuth consent flow with `access_type=offline&prompt=consent` to obtain a fresh refresh token. This cannot be automated.

**Gotcha:** The `google_auth.py` helper's `get_service()` catches refresh failures and tries the next account, but if all accounts fail it raises `RuntimeError`. Bower's scan scripts should catch this at the top level and enter degraded mode rather than crashing with an unhandled exception.

### Drive is overwhelmingly automated
A typical light scan finds 2,000–4,000 recently modified items. Most are:
- **System agent files**: `session_*.json`, `decisions.jsonl`, `config.json`, `messages.jsonl`
- **Agent skill artifacts**: `SKILL.md`, `.pyc` bytecode, `outbound_ckpt.txt`, drafts
- **Automated backups**: Files inside timestamped folders like `2026-04-20_06-00-01/`

Only ~1-2% are actual user content. Filter aggressively:
```python
hermes_re = re.compile(r"^20\d{2}-\d{2}-\d{2}_\d{2}-\d{2}")
code_markers = {"node_modules", "dist", ".git", "build", "__pycache__", "vendor",
                "coverage", "compiled", "objects", "refs", "checkpoints"}
system_patterns = ["session_", "decisions.jsonl", "config.json", "messages.jsonl",
                   "issues.jsonl", "fixes.jsonl", "ingest_", "state.db", "agent.log",
                   "gateway.pid", ".lbug", "FETCH_HEAD", "SKILL.md", "draft-"]
```

### folder_index.json is incomplete for parent lookups
The `folder_index.json` only contains ~72K folders from the original deep scan. Many parent IDs from Shared Drives or newer folders are NOT in the index. Use the Drive API to look up parent folder names directly.

### Proposals JSONL field names
The `proposals.jsonl` uses `proposal_type` and `confidence_tier` (NOT `type` and `confidence`).

### Transient drift — Drive self-corrects between cycles

**Scenario**: A light scan detects massive drift (e.g., root level goes from 6 items to 314+), triggering `drift_detected` and `needs_deep_scan`. A subsequent light scan finds the Drive has returned to its previous baseline (e.g., 6 root items again).

**What happened**: The drift was temporary — likely a sync/migration artifact where files were briefly visible at root level before being moved to their correct folders by an external process (Google Drive sync, migration tool, or bulk move operation).

**Handling**:
1. If the current scan count matches the pre-drift baseline (from `drive_digest.json` `previous_scan_file_count`), classify the drift as **transient** rather than structural.
2. Update `scan_progress.json` back to `phase: complete`, `status: stable` — set `total_files` and `total_folders` to the current counts.
3. Add a `scan_notes` entry documenting the transient drift event (peak count, resolution).
4. Reset `drive_digest.json` `scan_notes` to remove the stale drift warning.
5. **Do NOT trigger a deep scan** — the baseline was never actually broken; the scan window caught a mid-migration snapshot.
6. Write evidence explaining the transient drift; include both the spike count and the resolved count.
7. Skip `bower.analyze` — no proposals should be generated for a Drive that is back to its known-good state.

**Note**: This is different from the "Stale data after major Drive changes" gotcha in the main SKILL.md. That gotcha addresses a *permanent* structural change that invalidates old proposals. Transient drift resolves itself and the old baseline remains valid.

### Critical: No bower_analyze.py script may exist
If no `bower_analyze.py` exists, create it based on `references/organization_rules.md`, `references/domains.md`, and `references/analysis_schema.md`.

### Small Drive light scan efficiency (under 500 total files)

**Observed pattern (2026-06-26):** On <operator>'s Drive (~147 total files), the modifiedTime query returned 100 results — but 97 were epub/pdf books batch-imported to Bookshelf at the same timestamp. Only 3 were actual user activity (new folder, new PDF, modified spreadsheet). The "Drive is overwhelmingly automated" section above describes a 10K+ file scenario; small Drives have the opposite problem — most modified files are *intentional batch imports*, not noise.

**Efficient triage for small Drives:**

1. **Group by modified timestamp.** If 90%+ of modified files share a timestamp within minutes of each other, it's a batch import. Skip content reading — just verify the destination folder makes sense.

2. **Identify user-authored files quickly.** After filtering batch imports, look at:
   - Files modified at *unique* timestamps (especially the most recent)
   - Newly created folders (check parents to determine if they follow existing domain patterns)
   - Modified files that are NOT in the usual import folder

3. **Check parent folders explicitly.** The Drive API search results don't include parent IDs in the `files.list` response from `search_drive_files`. Use `mcp_google_workspace_list_drive_items` with the parent folder ID to see where new content landed, or infer from the folder structure you already know.

4. **Domain pattern recognition on small Drives.** <operator>'s structure is: `Home/Taxes/YYYY/[Deductions, CA TAX, Tax temp]`. When a new "Deductions" subfolder appears under "2026", it's following the established prescriptive tax pattern — mark it as correct, not as an outlier. The domain detection threshold (5+ files / 2+ subfolders) may need to be lower for small Drives where the user has already established multi-year tax subfolders.

5. **Skip deep inspection for well-understood domains.** Books in Bookshelf = always correct. Tax docs in Home/Taxes/YYYY/ = always correct. Don't generate proposals for files that are clearly in their canonical location.

6. **Report succinctly.** For a small, well-organized Drive, a single paragraph summary is sufficient. No need for the full tier/type breakdown tables from `analysis_events.jsonl` when there are zero outliers.

**Cron optimization:** For small Drives (<500 files), you can often process the entire modifiedTime query result set in one page (100 items). If `nextPageToken` is present AND the Drive is known to be small, paginate once more — the second page will likely be empty or contain only a few items. Don't set up multi-page pagination infrastructure for a Drive that barely fills one page.

### Shared files in modifiedTime results — triage before action

**Observed pattern (2026-06-28):** The `modifiedTime` query in `bower.scan.light` returns files and folders that are **shared with the user** but not in their Drive tree. These appear with `parents: null` and `ownedByMe: False` on `.get()`. They may be:
- Files/folders from another user's Drive (shared directly)
- Folders inside "Shared with me" items (e.g., `My Mac/Documents/...`)
- Shared spreadsheets recently modified by their owner

**Why they appear:** The Drive API `files.list` with `modifiedTime` filter returns all files the user can see that were modified in the timeframe — including shared files. These are NOT part of the user's Drive structure.

**Triage rule:** For each file/folder returned by the modifiedTime query, check:
1. `parents: None` + `ownedByMe: False` → **shared file, skip.** Bower has no authority to organize files outside the user's Drive tree.
2. Parent folder not in user's Drive tree (not in `folder_index.json`, not visible in root listing) → **shared context, skip.**
3. File inside a folder like "My Mac" that doesn't appear in the user's root listing → **shared context, skip.**

**How to verify:** Query `service.files().get(fileId=..., fields='parents, ownedByMe, shared')`. If `ownedByMe` is `False` and `parents` is `None`/empty, the file is shared and outside scope. For folders, check if they appear in the root-level listing (`'root' in parents`) — if not, they're in a shared context.

**Reporting:** Count shared files in the scan results and report them as "not actionable — shared context" in the evidence log. Do NOT generate proposals for shared files. The structural baseline check (root count comparison) already filters these out since shared folders don't appear in `'root' in parents` queries.

**Example from June 28 scan:** 31 modified files returned. 28 were automated scripts in `My Mac/Documents/takeout-enrichment-2026-06-28/` (shared context folder), 2 were shared spreadsheets (Clayroom Sign-Up Sheet, SF Restaurants). All 31 correctly classified as non-actionable. Zero proposals generated.

### Identifying batch vs. user activity by timestamp clustering

**Rule:** If the modifiedTime values cluster tightly (within 5 minutes) and the files share a common parent folder and mime type pattern, classify as batch import. Real user activity typically has:
- Scattered modifiedTime values (hours/days apart)
- Different mime types or parent folders
- Or a single file/folder modified at a unique time

**Caveat:** The modifiedTime on imported books is the import time, not the original file creation date. All books imported in one session will share a modifiedTime cluster. This is expected and not a sign of automated system activity.
