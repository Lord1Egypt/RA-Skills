# AI-DFE — Session Continuity

> Loaded by `core-engine.md`. How DFE resumes work across sessions. State lives in `{family}-ws/data/dfe-state.md` (DFE's marker).

## State File

`dfe-state.md` is DFE's single source of truth for what it has discovered and produced. It holds:

- **`discovered`** — per package: `schemaVersion`, `discoveredOn`, `schemaPath`, cached `sourceFiles[]`, `outputFile`, `lastGenerated`.
- **`demands`** — per consumer: `consumer`, `demandFile`, `outputFile`, `lastGenerated`.
- **`master`** — (multi-family) which family's DFE is currently master.

See `templates/dfe-state.md` for the full schema.

## Resume Flow

On activation, DFE checks for `{family}-ws/data/dfe-state.md`:

| Found? | Action |
|--------|--------|
| No | First run — show welcome, run Phase 1 (Configure) in full. |
| Yes | Resume — load cached discovery + demand registries. Skip full discovery; go straight to monitoring (Phase 2.4): compare cached source timestamps vs. `$generatedOn` and refresh only stale files. |

## Re-Discovery Triggers

DFE re-runs Phase 1 for a package only when:
- its `SOURCE_MAP.md` or `{pkg}-data.schema.json` timestamp changed, OR
- a `$schemaVersion` mismatch is detected, OR
- the user issues `DAT__ discover`.

Otherwise the cached interface stands (discover-once).

## Edge Cases

| Situation | Behaviour |
|-----------|-----------|
| `dfe-state.md` missing but data files present | Treat as first run; rebuild state from discovery; existing data files are overwritten on next pass. |
| A package was uninstalled | Its cached entry is marked stale; its `{pkg}-data.json` is left in place but flagged in `DAT__ status` until a discovery pass removes it. |
| A new DEMAND appears mid-session | Picked up on the next `DAT__ aggregate` or `DAT__ all`. |
| Interrupted write | History snapshot is taken only after a successful write; a partial write is re-done on next pass (idempotent). |
