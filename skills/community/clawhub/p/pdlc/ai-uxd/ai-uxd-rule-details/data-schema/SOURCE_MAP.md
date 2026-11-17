# SOURCE_MAP — AI-UXD

> Declares where AI-UXD's raw data lives and how AI-DFE extracts it. Paths relative to `pdlc-ws/`.

**Package:** AI-UXD — AI-Driven UX Design
**Schema:** `uxd-data.schema.json` (this folder)
**Schema version:** 1.0.0
**Scope:** per-project

---

## Presence Check

| Check | Path | Meaning if absent |
|-------|------|-------------------|
| Marker exists | `projects/PRJ-{ABBREV}-{slug}/ux/uxd-state.md` | `status: not-run` → all payload fields `null` |

## Source Files

| # | Source path (relative to `pdlc-ws/`) | Holds |
|---|-------------------------------------------|-------|
| 1 | `projects/PRJ-{ABBREV}-{slug}/ux/uxd-state.md` | YAML front-matter + workflow state, progress (16 stages), downstream signals, metrics, extensions, optional `dashboard-summary` block |
| 2 | `projects/PRJ-{ABBREV}-{slug}/ux/10_Accessibility_Baseline.md` (or working `accessibility-baseline.md`) | WCAG target + a11y status + criteria counts |
| 3 | `projects/PRJ-{ABBREV}-{slug}/ux/02_Personas/` | persona files `Persona_NN_{Name}.md` (→ `ux.personas`) |
| 4 | `projects/PRJ-{ABBREV}-{slug}/ux/03_Journey_Maps/` | journey files `Journey_NN_{desc}.md` with metadata (→ `ux.journeys`) |
| 5 | `projects/PRJ-{ABBREV}-{slug}/ux/05_User_Flows/` | flow files `Flow_NN_{task}.md` with fenced ```mermaid (→ `ux.flows`, `ux.userFlows`) |
| 6 | `projects/PRJ-{ABBREV}-{slug}/ux/06_Wireframe_Specifications/Screen_Inventory.md` | screen inventory (→ `ux.wireframes`) |
| 7 | `projects/PRJ-{ABBREV}-{slug}/ux/07_Design_System/` | `Design_Tokens.md`, `Voice_Tone_Guidelines.md`, etc. (→ `ux.designSystem`, `ux.designSystemFiles`) |
| 8 | `projects/PRJ-{ABBREV}-{slug}/ux/08_Component_Library/Component_Inventory.md` | component inventory (→ `ux.componentLibrary`) |
| 9 | `projects/PRJ-{ABBREV}-{slug}/ux/04_Information_Architecture.md` | IA / sitemap (→ `ux.informationArchitecture`) |

## Field Extraction

| Field path (in `data`) | Source (#) | Extraction rule |
|------------------------|------------|-----------------|
| `projectId` | 1 | Front-matter `projectId` |
| `projectHandle` | 1 | Front-matter `projectHandle` |
| `outputRoot` | 1 | Front-matter `outputRoot` |
| `created` | 1 | Front-matter `created` |
| `lastUpdated` | 1 | Front-matter `last_updated` |
| `mode` | 1 | Workflow State table → `Mode` (A/B/C/D) |
| `depth` | 1 | Workflow State table → `Depth` |
| `currentPhase` | 1 | Workflow State table → `Current Phase` (Discover/Define/Design/Validate/Assemble) |
| `currentStage` | 1 | Workflow State table → `Current Stage` (1-16) |
| `status` | 1 | Workflow State table → `Status` (In Progress/Complete) |
| `progress[]` | 1 | Progress table → one object per row: `{ stage, name, status, completed, artifacts }` |
| `enabledExtensions[]` | 1 | Enabled Extensions section → list |
| `downstreamSignals` | 1 | Downstream Signals section → object (what UXD signals to POLC/DWG/GCE) |
| `keyMetrics` | 1 | Key Metrics section → object (personas count, journeys count, flows count, components count) |
| `accessibility.wcagTarget` | 2 | Accessibility baseline → WCAG level (e.g. 2.2 AA) |
| `accessibility.status` | 2 | Accessibility baseline → overall status |
| `ux.status` / `ux.phase` / `ux.stage` | 1 | Workflow State → status / currentPhase / currentStage name |
| `ux.personas[]` | 3 | Scan `02_Personas/*.md` → `{ name, status, path }` (name from H1/front-matter; status from front-matter `validated`/`in-progress`; path workspace-root-relative) |
| `ux.journeys[]` | 4 | Scan `03_Journey_Maps/*.md` → `{ name, status, persona, path, steps, goal, trigger, endStateSuccess, endStateFailure, duration, frequency }` from each journey's metadata table |
| `ux.flows[]` | 5 | Scan `05_User_Flows/*.md` → `{ name, status, path, persona, journey, mermaid }`; `mermaid` = the file's fenced ```mermaid block (or `null`) |
| `ux.userFlows` | 5 | `{ total, mapped }` — count of flow files / those with a mermaid block |
| `ux.wireframes` | 6 | `Screen_Inventory.md` → `{ total, approved, inReview, pending, path, experiences[], screens[] }` from the inventory table |
| `ux.designSystem` | 7 | `{ tokens:{total,defined}, components:{total,specified} }` from `Design_Tokens.md` + component inventory counts |
| `ux.designSystemFiles[]` | 7 | One `{ name, path, status, description }` per file in `07_Design_System/` |
| `ux.componentLibrary` | 8 | `Component_Inventory.md` → `{ path, total, atoms, molecules, organisms, components[] }` (classify by level) |
| `ux.informationArchitecture` | 9 | `{ status, pages }` from `04_Information_Architecture.md` (pages = sitemap node count) |
| `ux.accessibility` | 2 | `{ target, wcagLevel, criteria, met, baselineDefined }` — `baselineDefined` true if file exists; `criteria`/`met` from the SC table |

## Retention Policy

| Policy | Value |
|--------|-------|
| History retention | forever |

## Notes

- UXD is per-project scoped: one `uxd-data.json` per project (keyed by `projectId`).
- Uses the shared `management_framework/` spine (sibling of `ux/`).
- **Rich `ux` pane (dashboard UX tab):** DFE scans the numbered `ux/` deliverable folders and extracts the **structured sub-sections** — persona/journey/flow files (metadata tables + fenced ```mermaid), `Screen_Inventory.md`, design-system files, component inventory, IA sitemap, and the accessibility SC table. It does NOT parse free-form prose. The few free-form roll-ups (overall ux status phrasing, design-token/component totals when not tabulated) come from a small `dashboard-summary` block in `uxd-state.md` (Hybrid emit). (Supersedes the earlier "counts only / not machine-extracted" stance — scoped to structured sub-sections per the Dashboard Data-Fidelity Plan.)
