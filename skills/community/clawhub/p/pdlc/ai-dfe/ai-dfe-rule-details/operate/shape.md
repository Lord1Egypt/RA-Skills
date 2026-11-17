# Stage 2.2 — Shape (Layer 2)

> Phase 2 (Operate). Per-package JSON → one `{consumer-output}.json` per DEMAND. The consumer-tailored view.

## Purpose

Assemble each consumer's demanded output by cherry-picking, aggregating, and transforming data drawn from per-package JSON (Layer 1) — never from raw sources.

## Inputs

- `dfe-state.md` `demands.{name}` (the DEMAND spec).
- The relevant `{pkg}-data.json` files produced by gather (2.1).

## Logic

For each DEMAND in the `demands` registry:
1. For each demanded field, read its value from the declared source domain's `{pkg}-data.json`.
2. Apply the DEMAND's transform (pick, rename, aggregate across projects, compute a roll-up, etc.).
3. A missing source-domain value → field = `null` (graceful).
4. Wrap in the metadata envelope with `$package: "AI-DFE"` (demand outputs are DFE-owned aggregations) and `$schema` pointing at the DFE-owned demand/aggregation schema.
5. Validate against the DFE-owned schema (3.1). On failure → block, report, keep prior version.

## Output

One `{consumer-output}.json` per DEMAND, staged for distribution (2.3).

## Hard Rule

Layer 2 NEVER re-reads raw sources. If a needed value isn't in any `{pkg}-data.json`, it is `null` — DFE does not reach back into the source files to "fix" it. This guarantees exactly one extraction point per fact (Layer 1).

## Dashboard pane assembly (the AIFLC-PDLC-Dashboard demand)

The dashboard output (`dashboard-data.json`) is assembled entirely from Layer-1 `{pkg}-data.json` files per the demand's field map:

| Output (`data`) | From Layer-1 |
|-----------------|--------------|
| `projects[].packages[]` | each `{pkg}-data` state-derived `{ status, phase, progress, stage, blockers, artifacts }` |
| `projects[].mgmt` / `mgmtDetail` | `pilc/adlc/polc-data` register counts + detail |
| `projects[].po` | **`polc-data.data.po`** (copy 1:1 — POLC now emits the full pane) |
| `projects[].arch` | **`adlc-data.data.arch`** (copy 1:1) |
| `projects[].ux` | **`uxd-data.data.ux`** (copy 1:1) |
| `projects[].edges[]` | `flo-data.routes` (else canonical chain order) |
| `ideas[]` | **`ilc-data.data.ideas`** (enriched: lowercase `stage`, `brief`, `routeTarget`, `files[]`) |
| `ppm` | `ppm-data` summary (mapped to `{ totalProjects, dispatched, pending, strategicFit, topPriority }`) |
| `health` | aggregate over packages (`totalBlockers`, `stalledProjects`, `overallProgress`) |

- The `po`/`arch`/`ux` panes are a **direct copy** of the producing package's pane object — the rich shape was already built at gather (Layer 1). If a producer is absent/unrun, its pane is `null` (graceful; the renderer guards it).
- **Serialize with depth ≥ 20** so nested arrays/objects are not truncated to `@{…}` strings (ISS-014).

## MANDATORY: Artifact Object Transform

The `packages[].artifacts` array in `dashboard-data.json` MUST contain **objects**, never plain strings. The dashboard renderer (`renderPM()`) accesses `.name`, `.status`, and `.path` on each item — plain strings produce `undefined` across the board.

### Required object shape per artifact:

```json
{
  "name": "01_Architecture_Vision.md",
  "status": "produced",
  "path": "projects/PRJ-FLT-fleet-tracking/architecture/01_Architecture_Vision.md"
}
```

### Transform rules (during Shape):

For each package in each project:

1. Read the `artifacts` field from the package's Layer-1 `{pkg}-data.json`.
2. **If items are already objects** with `name` and `status` → pass through (add `path` if missing using the output-root resolution below).
3. **If items are plain strings** (file names only) → transform each to an object:
   - `name` = the string value
   - `status` = derive from context:
     - File name matches a deliverable the package has produced (package status is `complete`, or the artifact's stage is marked done in `progress[]`) → `"produced"`
     - Package is `active` and artifact belongs to the current stage → `"in-progress"`
     - Otherwise → `"pending"`
   - `path` = resolve from the package's known output root (see table below) + the file name

### Package output-root resolution:

| Package code | Output root pattern (relative to `pdlc-ws/`) |
|---|---|
| AI-ILC | `ideas/{idea-folder}/` |
| AI-PILC | `projects/{project}/pip/` |
| AI-PPM | `portfolio/` |
| AI-POLC | `projects/{project}/backlog/` |
| AI-UXD | `projects/{project}/ux/` |
| AI-ADLC | `projects/{project}/architecture/` |
| AI-DWG | `projects/{project}/` (workspace root) |
| AI-GCE | `.governance/` |
| AI-TGE | `.governance/testing/` |
| AI-FLO | `routing/` |

When a package's output root or project context cannot be resolved → `path` = `null` (graceful; link won't work but name/status still display).

### Non-negotiable rule:

A plain-string artifact array is a **shape bug**. The schema (`dashboard-data.schema.json`) requires each item to be an object with at minimum `name` and `status`. DFE validation (3.1) will block the write if this contract is violated.

## `DAT__ aggregate`

`DAT__ aggregate` runs ONLY this stage (plus distribute), assuming per-package data is already fresh — a cheap way to refresh consumer views without re-gathering.
