# Trigger Keys — Quick Reference

> Two trigger classes exist in destination workspaces:
> - **Package activation keys:** **`_{PKG}_`** (package abbreviation, leading + trailing single underscore) — force-activate a family package's workflow.
> - **Agent shortcuts:** **`{3-LETTER-UPPERCASE}__`** (three capitals + double underscore) — invoke a governance agent.
>
> Type any trigger key in a Kiro chat prompt to invoke it instantly.

---

## Package Activation Keys (`_{PKG}_`)

Force-activate a family package's workflow, unambiguously, regardless of other installed packages. The explicit key is **deterministic** — it wins over all keyword matching and every sibling package, with no confirmation. Defined in each package's `core-workflow.md` / `core-generator.md` "Activation & Multi-Package Isolation" section.

| Key | Package | Activates |
|-----|---------|-----------|
| `_ILC_`  | AI-ILC  | Idea life cycle (capture → go/no-go) |
| `_PILC_` | AI-PILC | Project initiation (raw requirement → PIP) |
| `_ADLC_` | AI-ADLC | Architecture design (PIP → Architecture Package) |
| `_UXD_`  | AI-UXD  | UX design life cycle (→ UX Design Package) |
| `_POLC_` | AI-POLC | Product ownership (→ Product Backlog Package) |
| `_DWG_`  | AI-DWG  | Development-workspace generation |
| `_GCE_`  | AI-GCE  | Compliance/governance enforcement derivation |
| `_TGE_`  | AI-TGE  | Test governance & quality |
| `_PPM_`  | AI-PPM  | Portfolio management (cross-project) |
| `_FLO_`  | AI-FLO  | Routing / package-to-package handoff |
| `_DFE_`  | AI-DFE  | Data fabric (gather → shape → distribute `{family}-ws/data/`) |

**Status / utility keys (family-wide):**

| Key | Reports / Does |
|-----|----------------|
| `_ACTIVE_` | Which AI-* package is currently active + its state-marker status. Read-only — never triggers a package switch. |
| `_APROJ_` | **Active-project switch** (multi-project workspaces). Reports the current ★ active project from `projects/PROJECTS.md`, lists all projects, and switches the ★ pointer to a user-chosen project. Per-project producers (PILC/ADLC/UXD/POLC/DWG) then default to the newly active project. PPM/FLO are unaffected (registry-wide, §8). Updates only the `★`/`Active project:` pointer — never package state. (Specified as `APROJ__` in design OD#6; normalized to the `_X_` utility-key class alongside `_ACTIVE_`.) |

**Switching guarantees (enforced by every package's "Activation & Multi-Package Isolation" section):**
- A package switch NEVER happens without a **direct user order** (an explicit `_{PKG}_` key) or **explicit confirmation** (yes/no when a sibling is active).
- On any switch, the **first line of that response names the now-active package** (e.g. `Active package: AI-PILC`).

> **Optional runtime enforcement (opt-in):** the steering-level guarantees above are reinforced by an OPT-IN hook — `package-activation-guard.json` (a `promptSubmit` hook shipped **disabled** in `ai-gce/ai-gce-rule-details/templates/hooks/`). Set `"enabled": true` (or toggle it in the Kiro Hooks UI) to have the switch rule re-checked on every prompt. It is family-wide and works regardless of which packages are installed.

> **Distinct from agent shortcuts:** `_PILC_` (package, single underscores) ≠ `IQA__` (agent, trailing double underscore). No collision by construction.

---

## Destination Workspace Triggers (AI-GCE Generated)

| Key | Agent | Type | Owner | What It Does |
|-----|-------|------|-------|--------------|
| `SDC__` | session-discipline-agent | Process | AI-GCE | Spec-before-code enforcement, session methodology |
| `SGV__` | sprint-governance-agent | Process | AI-GCE | Sprint plan, goals, retro actions |
| `CRV__` | code-review-agent | Audit | AI-GCE | Reviewer separation, trust spectrum |
| `SQC__` | steering-quality-agent | Audit | AI-GCE | Steering file meta-governance (5 qualities) |
| `CMG__` | change-management-agent | Process | AI-GCE | Release governance, rollback criteria |
| `DOD__` | dod-gate-agent | Process | AI-GCE | Definition of Done validation |
| `IQA__` | initiation-quality-agent | Process | AI-PILC | PIP completeness, gate compliance |
| `ADA__` | architecture-decision-agent | Process | AI-ADLC | ADR quality, decision traceability |
| `WIA__` | workspace-integrity-agent | Audit | AI-DWG | Steering completeness, workspace structure |
| `TGV__` | test-governance-agent | Audit | AI-TGE | Test strategy, coverage, quality metrics |
| `CVR__` | coverage-review-agent | Audit | AI-TGE | Test coverage analysis |
| `SEC__` | session-end-compliance-agent | Audit | AI-GCE | Session-end sweep: module boundaries + domain purity + coverage + naming (manual or hook-triggered) |

## AI-DFE Data Fabric Triggers (ship with AI-DFE)

> Shipped by the AI-DFE package itself (not AI-GCE-generated). Available in any workspace where AI-DFE is installed. `DAT__` performs data operations (mutates `{family}-ws/data/`); `DFA__` and `DHC__` are report-only agents.

| Key | Agent / Mode | Type | Owner | What It Does |
|-----|--------------|------|-------|--------------|
| `DAT__` | _(engine operation — no agent)_ | Operation | AI-DFE | Data operations: gather → shape → distribute. Sub-commands: `all`, `full` (complete-set pass + pane-completeness readiness report), `{family}`, `{family}/{pkg}`, `aggregate`, `status`, `discover`, `validate`, `cleanup --before {epoch-ms}`, `master`, `master --set {family}`. Mutates `{family}-ws/data/`. |
| `DFA__` | data-fabric-agent (DFE-AG-01) | Audit | AI-DFE | Deep data-surface integrity assessment — 18 checks / 5 categories (schema, registry, manifest, freshness, territory). Report-only. Scopes: `schema`/`registry`/`manifest`/`freshness`/`territory`. |
| `DHC__` | data-fabric-health-check (DFE-AG-02) | Audit | AI-DFE | Bootstrap readiness — "can DFE run here?". `DHC__ fix` creates missing empty scaffolding only. Run first in a new workspace. |

## AI-FLO Fabric Triggers (ship with AI-FLO)

> Shipped by the AI-FLO package itself (not AI-GCE-generated). Available in any workspace where AI-FLO is installed. Both are report-only health/integrity agents.

| Key | Agent | Type | Owner | What It Does |
|-----|-------|------|-------|--------------|
| `FHC__` | flo-health-check (FLO-AG-02) | Audit | AI-FLO | Bootstrap readiness — "is this workspace ready for FLO?". Validates fabric trio, discovery, routing graph. `FHC__ fix` attempts simple resolutions. Run first in a new workspace. |
| `FIA__` | flow-integrity-agent (FLO-AG-01) | Audit | AI-FLO | Operational integrity — "is FLO's state correct?". Validates routing graph consistency, entity positions, marker freshness during active operation. |

## Future Triggers (Planned)

| Key | Agent | Type | Owner | What It Does |
|-----|-------|------|-------|--------------|
| `BLH__` | backlog-health-agent | Process | AI-POLC | Backlog quality, user story health |
| `PGA__` | portfolio-governance-agent | Audit | AI-PPM | Cross-project health, portfolio status |
| `UXC__` | ux-consistency-agent | Audit | AI-UXD | Design system adherence, accessibility |

---

## Tier Availability

| Tier | When Active | Available Triggers |
|------|-------------|--------------------|
| **1** (Day 0) | From first generation | `SDC__`, `TGV__`, `IQA__`, `ADA__`, `WIA__` |
| **2** (Sprint 2+) | After Tier 2 activation | + `SGV__`, `CRV__`, `SQC__`, `DOD__`, `CVR__` |
| **3** (Pre-Release) | After Tier 3 activation | + `CMG__` |

---

## Rules

- Each trigger must be **globally unique** per workspace — no collisions across either class.
- **Package activation keys** use `_{PKG}_` (single underscores either side); the abbreviation is the package name minus the `AI-` prefix.
- **Agent shortcuts** use `{3-LETTER}__` (trailing double underscore); the double underscore suffix is non-negotiable for this class.
- Letters must form a recognizable abbreviation of the package/agent's purpose.
- Triggers are registered in the workspace-rules steering file for the AI to recognize.
- Canonical sources: package activation keys → each package's `core-workflow.md`/`core-generator.md`; agent shortcuts → `contracts/AGENT_GOVERNANCE_CONTRACT.md`.
