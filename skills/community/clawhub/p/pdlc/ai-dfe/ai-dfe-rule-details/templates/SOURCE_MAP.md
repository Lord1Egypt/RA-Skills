# SOURCE_MAP — {AI-PKG}

> **Template.** Each package ships this file at `ai-{pkg}-rule-details/data-schema/SOURCE_MAP.md`. It declares where this package's raw data lives and how AI-DFE extracts it. Paths are relative to `{family}-ws/`. Replace every `{placeholder}`.

**Package:** {AI-PKG} — {full name}
**Schema:** `{pkg}-data.schema.json` (this folder)
**Schema version:** {semver}
**Scope:** {per-project | portfolio | family}

---

## Presence Check

How AI-DFE detects whether this package has been run:

| Check | Path | Meaning if absent |
|-------|------|-------------------|
| Marker exists | `{family}-ws/{…}/{pkg}-state.md` | `status: not-run` → all payload fields `null` |

## Source Files

Every file AI-DFE reads for this package:

| # | Source path (relative to `{family}-ws/`) | Holds |
|---|-------------------------------------------|-------|
| 1 | `{role-folder}/{pkg}-state.md` | state, projectId, status, phase |
| 2 | `{role-folder}/{artifact}.md` | {what} |
| 3 | `management_framework/{Register}.md` | {register rows} |

## Field Extraction

Maps each schema field to a source + extraction rule. A missing source → field = `null` (graceful degradation).

| Field path (in `data`) | Source (# above) | Extraction rule |
|------------------------|------------------|-----------------|
| `projectId` | 1 | front-matter `projectId` |
| `status` | 1 | front-matter `status` |
| `{field}` | 2 | {parse rule — e.g. heading value, list count, table column} |
| `{register}[].{f}` | 3 | one object per register row; map columns → fields |

## Retention Policy (optional)

| Policy | Value |
|--------|-------|
| History retention | {forever \| keep-last-N \| keep-days-T} |

## Notes

- AI-DFE reads these sources ONLY for this package's `{pkg}-data.json` (Layer 1). It never reaches into another package's sources.
- If this package adds/moves outputs, update this SOURCE_MAP and bump the schema version — that triggers DFE re-discovery.
- Declared sources that don't exist yet are allowed; they resolve to `null` until the package runs.
