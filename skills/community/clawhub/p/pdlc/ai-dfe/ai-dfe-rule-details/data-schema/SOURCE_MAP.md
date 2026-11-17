# SOURCE_MAP — AI-DFE

> AI-DFE's own data interface. DFE reports on itself by reading its own state file. This lets a dashboard or `DFA__` see the health of the data layer as just another data file (`dfe-data.json`). Paths relative to `{family}-ws/`.

**Package:** AI-DFE — AI-Driven Data Fabric
**Schema:** `dfe-data.schema.json` (this folder)
**Schema version:** 1.0.0
**Scope:** family

---

## Presence Check

| Check | Path | Meaning if absent |
|-------|------|-------------------|
| Marker exists | `data/dfe-state.md` | `status: not-run` → DFE hasn't run yet; payload `null`/zeroed |

## Source Files

| # | Source path (relative to `{family}-ws/`) | Holds |
|---|-------------------------------------------|-------|
| 1 | `data/dfe-state.md` | family block, master block, `discovered` registry, `demands` registry |
| 2 | `data/REGISTRY.json` | current file list (for counts) |
| 3 | `data/history/` | snapshot count |

## Field Extraction

| Field path (in `data`) | Source (#) | Extraction rule |
|------------------------|------------|-----------------|
| `status` | 1 | `dfe-state.md` status header |
| `isMaster` / `masterFamily` | 1 | `master.isMaster` / `master.masterFamily` |
| `lastFullPass` | 1 | last full pass timestamp |
| `packages[]` | 1 | one object per `discovered.{pkg}` (package, schemaVersion, outputFile, lastGenerated, status) |
| `demands[]` | 1 | one object per `demands.{name}` |
| `counts.packagesDiscovered` | 1 | count of `discovered.*` |
| `counts.dataFiles` | 2 | count of `files` in REGISTRY.json |
| `counts.demands` | 1 | count of `demands.*` |
| `counts.historySnapshots` | 3 | count of files in `history/` |

## Retention Policy

| Policy | Value |
|--------|-------|
| History retention | forever |

## Notes

- DFE reading its own state is not self-referential recursion: `dfe-data.json` is produced from `dfe-state.md` (a marker file), exactly as any package's data is produced from its marker.
- Counts are derived at gather time and are advisory (they reflect the moment of the pass).
