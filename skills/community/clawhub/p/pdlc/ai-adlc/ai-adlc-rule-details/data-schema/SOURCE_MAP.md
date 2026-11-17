# SOURCE_MAP — AI-ADLC

> Declares where AI-ADLC's raw data lives and how AI-DFE extracts it. Paths relative to `pdlc-ws/`.

**Package:** AI-ADLC — AI-Driven Architecture Design Life Cycle
**Schema:** `adlc-data.schema.json` (this folder)
**Schema version:** 1.0.0
**Scope:** per-project

---

## Presence Check

| Check | Path | Meaning if absent |
|-------|------|-------------------|
| Marker exists | `projects/PRJ-{ABBREV}-{slug}/architecture/adlc-state.md` | `status: not-run` → all payload fields `null` |

## Source Files

| # | Source path (relative to `pdlc-ws/`) | Holds |
|---|-------------------------------------------|-------|
| 1 | `projects/PRJ-{ABBREV}-{slug}/architecture/adlc-state.md` | state, projectId, status, phase, containers, extensions, ADR register, progress |
| 2 | `projects/PRJ-{ABBREV}-{slug}/management_framework/Decision_Log.md` | architecture decisions (below-ADR threshold) |
| 3 | `projects/PRJ-{ABBREV}-{slug}/management_framework/Change_Log.md` | architecture scope changes |
| 4 | `projects/PRJ-{ABBREV}-{slug}/management_framework/Issue_Log.md` | design blockers |
| 5 | `projects/PRJ-{ABBREV}-{slug}/management_framework/Lessons_Learned.md` | architecture lessons |
| 6 | `projects/PRJ-{ABBREV}-{slug}/architecture/Architecture_Workbook.md` | open questions + decision backlog |
| 7 | `projects/PRJ-{ABBREV}-{slug}/architecture/01_Architecture_Vision.md` | vision statement, principles, constraints, quality priorities (→ `arch.vision`, `arch.principles`, `arch.constraints`) |
| 8 | `projects/PRJ-{ABBREV}-{slug}/architecture/` C4 docs — `02_System_Context*.md` (L1), `03_Container*.md` (L2), `11_Component*.md` (L3) | fenced ```mermaid blocks (→ `arch.c4Diagrams.l1/l2/l3`, `arch.c4Progress`, `arch.containers`) |
| 9 | `projects/PRJ-{ABBREV}-{slug}/architecture/` Technology Stack doc | Core/Supporting/Deployment stack tables (→ `arch.techStack` grouped object) |
| 10 | `projects/PRJ-{ABBREV}-{slug}/architecture/` Security / Data / API / Integration / Infrastructure docs | fenced ```mermaid (→ `arch.diagrams.{security,data,api,infrastructure}`), NFR tables (→ `arch.nfrs`), external systems (→ `arch.integrations`) |
| 11 | `projects/PRJ-{ABBREV}-{slug}/architecture/ADR/` | one file per ADR `ADR-NNN_*.md` (→ `arch.adrs` with path) |

## Field Extraction

| Field path (in `data`) | Source (#) | Extraction rule |
|------------------------|------------|-----------------|
| `projectId` | 1 | Configuration table → `Project ID` row value |
| `systemName` | 1 | Configuration table → `System Name` row value |
| `projectHandle` | 1 | Configuration table → `Project Handle` row value |
| `status` | 1 | Configuration table → `Status` row value |
| `currentPhase` | 1 | Configuration table → `Current Phase` row value |
| `currentStage` | 1 | Configuration table → `Current Stage` row value (integer) |
| `workflowDepth` | 1 | Configuration table → `Workflow Depth` row value |
| `inputMode` | 1 | Configuration table → `Input Mode` row value |
| `started` | 1 | Configuration table → `Started` row value (ISO 8601) |
| `lastUpdated` | 1 | Configuration table → `Last Updated` row value (ISO 8601) |
| `producerVersion` | 1 | Configuration table → `Producer Version` row value |
| `enabledExtensions[]` | 1 | Enabled Extensions section → list of extension names |
| `containers[]` | 1 | Containers table → one object per row: `{ name, technology, responsibility }` |
| `adrs[]` | 1 | ADR Register table → one object per row: `{ number, title, stage, status, summary }` |
| `principles[]` | 1 | Architecture Principles table → one object per row: `{ id, name, summary }` |
| `constraints[]` | 1 | Key Constraints table → one object per row: `{ constraint, source, impact }` |
| `openQuestions[]` | 1+6 | Open Questions from state (or Workbook) → `{ number, question, priority, raisedAt, targetStage }` |
| `progress[]` | 1 | Progress table → one object per row: `{ stage, name, status, completed, notes }` |
| `decisions[]` | 2 | One object per table row (prefixed `ADLC-{ABBREV}-D-*`): `{ id, date, summary, status }` |
| `changes[]` | 3 | One object per table row (prefixed `ADLC-{ABBREV}-C-*`): `{ id, date, description, status }` |
| `issues[]` | 4 | One object per table row (prefixed `ADLC-{ABBREV}-I-*`): `{ id, description, priority, status, owner }` |
| `lessons[]` | 5 | One object per table row (prefixed `ADLC-{ABBREV}-L-*`): `{ id, lesson, stage, captured }` |
| `arch.status` / `phase` / `stage` / `stageNum` | 1 | Configuration table → status / currentPhase / currentStage |
| `arch.c4Progress` | 1, 8 | `{ context, container, component, code }` — completion status of each C4 level (from progress table / presence of each C4 doc) |
| `arch.vision` | 7 | `{ status, statement, optimisesFor[], path }` — status/statement from the `dashboard-summary` block (Hybrid emit) or Vision doc heading; `optimisesFor` from quality-priorities list; `path` workspace-root-relative |
| `arch.principles[]` | 7, 1 | Architecture Principles table → `{ id, name, summary }` |
| `arch.constraints[]` | 7, 1 | Key Constraints table → `{ id, text, impact }` |
| `arch.nfrs` | 10 | **Object keyed by NFR name** → `{ defined, target, priority }` (from NFR tables; targets via `dashboard-summary` when prose-only) |
| `arch.integrations[]` | 10 | External systems / integration patterns → `{ name, type, direction, status }` |
| `arch.adrs[]` | 11, 1 | ADR Register + `ADR/` folder → `{ id, title, status, date, path }` |
| `arch.risks[]` | 4, 6 | Design blockers / architecture risks → `{ text, severity }` (may be `[]`) |
| `arch.techStack` | 9 | **Grouped object** → `{ languages[], frameworks[], databases[], infrastructure[], messaging[], observability[] }` from the stack tables (grouping via `dashboard-summary` when ambiguous) |
| `arch.containers[]` | 8, 1 | Containers table → `{ name, type, tech }` |
| `arch.c4Diagrams` | 8 | `{ l1, l2, l3 }` each `{ mermaid, path, status }` — extract the real fenced ```mermaid block from each C4 doc; generate L3 only where the source has none (ISS-037/039) |
| `arch.diagrams` | 10 | `{ security, data, api, infrastructure }` each `{ mermaid, path, label }` — extract fenced ```mermaid from each doc; generate where absent |

## Retention Policy

| Policy | Value |
|--------|-------|
| History retention | forever |

## Notes

- ADLC is per-project scoped: one `adlc-data.json` per project (keyed by `projectId`).
- Management_framework is shared with AI-PILC — DFE distinguishes entries by phase prefix (`ADLC-{ABBREV}-*`).
- ADLC produces 4 registers (not 6); Actions → tracked in Architecture_Workbook; Assumptions → resolved in Vision stage.
- Individual architecture documents (`01_*.md` through `11_*.md`) — DFE extracts their **structured sub-sections** for the dashboard `arch` pane: fenced ```mermaid blocks (C4 L1/L2/L3 + security/data/api/infrastructure diagrams), the technology-stack tables, NFR tables, the ADR register + `ADR/` folder, and the containers table. It does NOT parse free-form prose; the few free-form roll-ups (vision status/statement, NFR targets, techStack grouping) come from a small `dashboard-summary` block in `adlc-state.md` (Hybrid emit). (Supersedes the earlier "not read by DFE — too unstructured" stance — scoped to structured sub-sections per the Dashboard Data-Fidelity Plan.)
- The `containers[]` field is what AI-DWG consumes; DFE preserves it (top-level + mirrored under `arch.containers`) so dashboards can show system topology.
