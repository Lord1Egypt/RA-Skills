# Elephas Pipeline Gotchas

Operational pitfalls discovered during elephas cron pipeline runs.

## List Entity Crash Bug

### `get_name` and helpers crash on list-type entities

**Symptom**: Pipeline crashes with `AttributeError: 'list' object has no attribute 'get'` during the entity processing loop.

**Root cause**: Some journals emit `entities_observed` entries that are nested lists instead of dicts. The `extract_entities()` function iterates and appends whatever is in the list — if it's a list instead of a dict, the helper functions `get_name()`, `get_type()`, `get_ur()`, and `get_conf()` crash because they call `.get()` on a list.

**Fix**: Add type guards at the top of each helper function in `elephas_cron_run.py`:

```python
def get_name(e):
    if isinstance(e, str):
        return e
    if isinstance(e, (int, float)):
        return str(e)
    if isinstance(e, list):       # ADD THIS
        return ""                 # ADD THIS
    if not isinstance(e, dict):   # ADD THIS
        return ""                 # ADD THIS
    # ... rest of function
```

Apply the same guard pattern to `get_type()`, `get_ur()`, and `get_conf()` — add `isinstance(e, list)` and `not isinstance(e, dict)` checks that return the function's default value.

**Fixed in**: `elephas_cron_run.py` (verified present 2026-06-18). Also present in the older `elephas_cron_pipeline.py` (patched 2026-06-17).

**Note**: If running the pipeline and encountering `AttributeError: 'list' object has no attribute 'get'`, re-apply the type guard pattern to the canonical script at `<fs-root>/indigo-repo/commons/db/ocas-elephas/elephas_cron_run.py`.

## Bridge Dependency

The elephas pipeline requires the LadybugDB bridge to be running on port 9192. Check with:
```bash
curl -s http://localhost:9192/health
```

If not running, the bridge must be started manually. The bridge requires `LBUG_C_API_LIB_PATH` to be set:
```bash
# Check if bridge is already running
ps aux | grep ladybug_bridge | grep -v grep

# If not running or unhealthy, restart:
pkill -f "ladybug_bridge" 2>/dev/null
sleep 2
LBUG_C_API_LIB_PATH=/tmp/liblbug-v0171/liblbug.so.0.17.1 \
  nohup python3 <hermes-home>/profiles/indigo/scripts/ladybug_bridge.py \
  --db <hermes-home>/commons/db/ocas-elephas/chronicle.lbug \
  --port 9192 \
  > /tmp/ladybug_bridge_elephas.log 2>&1 &
sleep 4
curl -s http://127.0.0.1:9192/health
```

**Root cause**: The `real_ladybug` v0.15.3 C extension needs `ArrowQueryResult` from `liblbug.so`, but the v0.17.1 library doesn't export it. The `ladybug` module from 3.13 site-packages works with `LBUG_C_API_LIB_PATH` set. See `ocas-custodian/references/elephas-bridge-recovery-2026-06-18.md` for full details.

As of 2026-06-18, the bridge does NOT run as a systemd service — it's a persistent process that must be restarted manually when it fails.

## Cursor Update After Manual/Cron Run

After running the elephas pipeline, update the lucid config cursor to include the new journal files. Add the new `cron_*.json` entries to both `cursor.ocas-elephas` AND `cursor.elephas` in `<hermes-home>/profiles/indigo/commons/data/ocas-lucid/config.json`. Without this, lucid will try to re-process elephas journals on the next dream cycle.

**Note**: This only applies to elephas journals that ARE in Lucid's scan path (`<hermes-home>/commons/journals/ocas-elephas/`). Journals written to `<commons>/journals/ocas-elephas/` by the canonical script do NOT need cursor updates (they're outside Lucid's scan scope).

## Dual Journal Output Paths

The canonical `elephas_cron_run.py` writes its run journals to:
```
<fs-root>/commons/journals/ocas-elephas/YYYY-MM-DD/cron_<hash>.json
```

Lucid scans journals under:
```
<hermes-home>/commons/journals/
```

These are **different directories**. Elephas cron journals are NOT in Lucid's scan path — this is intentional (elephas journals are self-contained run records, not Lucid input). Do NOT add `<commons>/journals/ocas-elephas/` to Lucid's scan roots.

The **ingestion log** at `<commons>/db/ocas-elephas/ingestion_log.jsonl` tracks what elephas has already processed, so re-runs are safe — the pipeline deduplicates via the ingestion log, not via Lucid's cursor.

## Script Path

The pipeline script is at:
```bash
<fs-root>/indigo-repo/commons/db/ocas-elephas/elephas_cron_run.py
```

Run with:
```bash
cd <fs-root>/indigo-repo/commons/db/ocas-elephas
python3 elephas_cron_run.py
```

Typical runtime: <30 seconds for a no-new-data run. With many unprocessed journals (100+), expect 60-120 seconds. Set `timeout=300` to be safe.

**Pre-flight check** — always verify the bridge is healthy before running:
```bash
curl -s http://localhost:9192/health
```
If the bridge is unhealthy, the script will print `BRIDGE ERROR` for every query and produce an empty run. See "Bridge Dependency" section above for restart procedure.

Note: An older path (`<hermes-home>/profiles/indigo/commons/db/ocas-elephas/elephas_cron_pipeline.py`) existed in a previous deployment. The current canonical path is under `<repo-root>/`.

## Self-Referential Journal Accumulation (Known Behavior)

The elephas cron writes its run journals to `<commons>/journals/ocas-elephas/YYYY-MM-DD/cron_*.json` (via `JOURNALS_OUTPUT` where `AGENT_ROOT = Path("/root")`). These same files are then scanned on the next run because `load_processed()` path matching fails for them — the ingestion log stores the path as written by the script, but the filesystem scan discovers them under a slightly different path representation.

**Result**: Each run re-scans ~135 accumulated cron journals, finds 0 entities in all of them, and logs them with `reason: "no_entities"`. This is harmless but adds ~5-10 seconds per run.

**Do NOT attempt to fix** by adding the elephas output directory to an exclude list — the path mismatch is in the ingestion log matching, not the scan. Excluding the directory would require changing `JOURNALS_OUTPUT` in the script, which would break the journal output. The current behavior is acceptable.

**Verified**: 2026-06-19 — pipeline completes successfully despite 135 "unprocessed" self-referential journals. All phases complete, 0 errors.

## Expected Unprocessed Residuals (2026-06-19)

After a full pipeline run, ~135 journals may remain "unprocessed" in the ingestion log. This is **expected and correct** — not a bug. The residual files are:

1. **Pure operational scans** (no entities): `ocas-forge/journal-scan-*`, `ocas-sands/briefing-*`, `ocas-scout/scout-update-*`, `ocas-dispatch/r_draft_*`, `ocas-haiku/r_*`
2. **Self-referential cron journals**: `ocas-elephas/cron_*.json` (the pipeline's own run records)
3. **Legacy nested-entity journals**: `ocas-mentor/r_deep_*`, `ocas-scout/scout-research-*` — these DO have entities but nested under `decision.payload` in a structure `extract_entities()` doesn't traverse
4. **`.jsonl` files (JSON Lines)**: `ocas-mentor/mentor-light-*.jsonl` — high-value evaluation journals written in JSON Lines format. The pipeline's `find_unprocessed()` only scans `*.json`, so these are silently skipped every run. See `memory-system-design/references/pipeline-scripts.md` section ".jsonl Blind Spot" for details and fix options.
5. **Unrendered templates**: Some `ocas-mentor/mentor-light-*.json` files contain literal template variables (`${TS}`, `$(python3 -c "...")`) that were never interpolated. These fail JSON parsing and are correctly skipped. This indicates a bug in the mentor skill's journal writing path — the template is being written instead of the rendered output.

**How to distinguish expected residuals from a real ingestion gap:**

| Signal | Expected residual | Real ingestion gap |
|--------|-------------------|-------------------|
| `entities_observed` at top level | Absent | Present |
| Journal is a scan/sweep file | Yes | No |
| `extract_entities()` returns empty | Yes (correct) | No (bug) |
| Count after full run | ~135 (and growing — elephas cron journals accumulate) | Growing unbounded |

The residual count grows over time because elephas's own cron output journals (`<fs-root>/commons/journals/ocas-elephas/cron_*.json`) are re-scanned each run. The ingestion log path matching fails for these because the log stores the path as written by the script, but the scan discovers them under a slightly different path format. This is harmless — they have no entities and are logged with `reason: "no_entities"` each time.

**Action**: If residual count is stable (not growing unboundedly) and all are scan/cron/self-referential files, the pipeline completed successfully. Do NOT re-run the pipeline to "catch" these — they have no extractable entities by design.

## Nested Entity Extraction Gap (Known Limitation)

The canonical `extract_entities()` function in `elephas_cron_run.py` checks three paths:
1. Top-level `data["entities_observed"]`
2. `data["decision"]["entities_observed"]`
3. `data["decision"]["payload"]["entities_observed"]`

**Missing paths** (found in older journals from ~April 2026):
- `data["decision"]["payload"]["entities_observed"]` — present but sometimes the payload is a JSON string, not a dict (requires `json.loads()` first)
- `data["action"]["entities_observed"]` — used in some scout/mentor journals
- Entity names embedded in `data["decision"]["payload"]["name"]` as a standalone string (not wrapped in an entity dict)

**Affected skills**: `ocas-mentor` (deep runs), `ocas-scout` (research runs). These are older journals from before the current schema stabilized.

**Fix** (if deep extraction is needed): Expand `extract_entities()` to also check `action.entities_observed` and to handle payload-as-string by attempting `json.loads()` on the payload value before traversal.

**Priority**: Low. These are historical journals. New journals (May 2026+) use the standard top-level `entities_observed` array and are ingested correctly.