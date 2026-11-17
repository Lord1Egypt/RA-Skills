# Large Drive Scanning Strategy

## Problem
Founding deep scans on Drives with 10K+ items (50K+ in this case) exceed the 10-minute cron timeout when attempting full enumeration.

## Symptoms
- `bower.scan.deep` runs for 5+ minutes just listing items
- Background process killed at 10-minute timeout
- Google Drive API returns 500 Internal Errors under load
- Folder-only queries still paginate through thousands of folders

## Solution: Sampled Deep Scan

For Drives with >10K estimated items, use a **sampled deep scan** instead of full enumeration:

### Sampling Strategy
1. **Root level**: Full enumeration (files + folders at Drive root)
2. **Per root folder**: Sample up to 300 files (3 pages × 100) per top-level folder
3. **Subfolders**: Count only (no file enumeration)
4. **Content reading**: Only for sampled Google Docs/Sheets/Slides

### Time Budget
- Root listing: ~15 seconds
- 19 root folders × 3 pages × 100 files: ~3-5 minutes
- Content reading (371 files): ~1-2 minutes
- Analysis & proposals: ~30 seconds
- **Total: ~5-7 minutes** (within 10-min cron limit)

### Trade-offs
| Aspect | Full Enumeration | Sampled Scan |
|--------|------------------|--------------|
| File coverage | 100% | ~20-50% |
| Domain detection | Complete | Root-level only |
| Proposal depth | All files | Root-level + sampled |
| Scan coverage field | 1.0 | 0.5 |
| Follow-up | None needed | Weekly deep scan STAYS sampled (never full enumeration) |

> **Correction (2026-07-19):** the original note said "Weekly deep scan fills gaps" (implying later full enumeration). On a Drive with ~24K total folders (a giant nested backup/Takeout tree), full enumeration times out the cron job and risks 500s. The weekly `bower:weekly-deep` run ALSO uses the sampled strategy — `scan_coverage` stays `0.5` every week by design. The "fills gaps" language has been removed from `deep_scan_sampled.py`'s docstring accordingly.

### Implementation Notes
- Set `scan_coverage: 0.5` in `drive_digest.json`
- Add `scan_notes` documenting the sampling approach
- Weekly deep scan (`bower:weekly-deep`) will run full enumeration
- Proposals focus on root-level outliers and domain-prescriptive moves

## 500 Error Handling
Google Drive API returns 500 Internal Errors intermittently during heavy pagination. Always wrap list calls with exponential backoff:

```python
for attempt in range(3):
    try:
        r = drive.files().list(...).execute()
        break
    except HttpError as e:
        if e.resp.status in (500, 503) and attempt < 2:
            time.sleep(2 ** attempt)
        else:
            raise
```

## When to Use Sampled Scan
- Founding run on Drive with >10K items (check via `about.get` storage or quick root count)
- Any deep scan that exceeds 5 minutes on folder enumeration
- Cron jobs with strict time limits
- **Weekly `bower:weekly-deep` on this Drive — always sampled** (the Drive has ~24K folders; full enum is not viable)

## Current implementation on this Drive (2026-07-14 → )
The maintained, runnable entrypoint is **`commons/data/ocas-bower/deep_scan_sampled.py`** (NOT the skill's own `scripts/bower_full_scan.py`, which does full enumeration + uses the broken hardcoded-credential auth path). What it does:
1. `get_service("drive", ...)` auth (correct per-account client + auto-refresh — never hand-built `Credentials`).
2. Phase 1: enumerate ALL folders once, cache to `folder_full_cache.json` (reused on subsequent runs → fast). Gives the true folder count + topology.
3. Root-level structural baseline: confirm 6 curated roots, 0 loose root files.
4. Phase 2: sample up to **300 direct children** per curated root (`ROOT_IDS`: Bookshelf, Archive, Home, Projects, Professional, Authenticator Backups). Writes `scans/{id}.json` (analyze-compatible) + `folder_index.json`.
5. Stale-data reconciliation, `drive_digest.json` update (`scan_coverage: 0.5`), `scan_progress.json`, scan event, evidence, Observation Journal, Vesper health signal.
- The curated roots hold ~516 direct files; the other ~23.7K folders are the auto-generated backup/Takeout tree and are out of scope (Bower organizes, never deletes).
- After the sampled deep scan, run the analyzer (`scripts/bower_analyze.py`, which reads the canonical `commons/data/ocas-bower` dir) to refresh `preference_profile.json` and proposals. The analyzer is pure-local (no Drive auth needed).

## Future Enhancement
A `--sample` flag on `bower.scan.deep` would formalize the auto-switch, but until then the sampled script IS the weekly-deep implementation.