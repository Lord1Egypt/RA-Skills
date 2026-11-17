# PDLC Family — Command Dashboard

> **Purpose:** Single-page reference for operating the AI-* PDLC Family in your workspace. Copy any command and paste it directly into the Kiro chat prompt.

---

## Package Activation Keys

Force-activate any PDLC package's workflow. Deterministic — wins over keyword matching and sibling packages.

### Portfolio Layer

| Key | Package | What It Does |
|-----|---------|--------------|
| `_ILC_` | AI-ILC | Start the Idea Life Cycle — capture, shape, evaluate, and approve ideas |
| `_PILC_` | AI-PILC | Start Project Initiation — transform a raw requirement into a PIP |
| `_PPM_` | AI-PPM | Start Portfolio Management — cross-project prioritization & governance |

### Edge (Router)

| Key | Package | What It Does |
|-----|---------|--------------|
| `_FLO_` | AI-FLO | Activate routing — package-to-package handoff decisions |

### Project Layer

| Key | Package | What It Does |
|-----|---------|--------------|
| `_POLC_` | AI-POLC | Start Product Ownership — PIP → Product Backlog Package |
| `_UXD_` | AI-UXD | Start UX Design — PIP + PBP → UX Design Package |
| `_ADLC_` | AI-ADLC | Start Architecture Design — PIP + PBP + UXP → Architecture Package |
| `_DWG_` | AI-DWG | Generate Development Workspace — AP + PBP + UXP → ready-to-code workspace |
| `_GCE_` | AI-GCE | Derive Governance & Compliance — hooks, agents, enforcement layer |
| `_TGE_` | AI-TGE | Derive Test Governance — test strategy, coverage, quality layer |

### Utility Keys

| Key | What It Does |
|-----|--------------|
| `_ACTIVE_` | Report which AI-* package is currently active + its state |
| `_APROJ_` | Switch active project (multi-project workspaces) |

---

## Agent Shortcuts

Invoke a governance or quality agent instantly. Three capitals + double underscore.

### Always Available (Tier 1 — Day 0)

| Command | Agent | What It Does |
|---------|-------|--------------|
| `IQA__` | Initiation Quality Agent | PIP completeness, gate compliance |
| `ADA__` | Architecture Decision Agent | ADR quality, decision traceability |
| `WIA__` | Workspace Integrity Agent | Steering completeness, workspace structure |
| `TGV__` | Test Governance Agent | Test strategy, coverage, quality metrics |
| `SDC__` | Session Discipline Agent | Spec-before-code enforcement |

### Sprint 2+ (Tier 2)

| Command | Agent | What It Does |
|---------|-------|--------------|
| `SGV__` | Sprint Governance Agent | Sprint plan, goals, retro actions |
| `CRV__` | Code Review Agent | Reviewer separation, trust spectrum |
| `SQC__` | Steering Quality Agent | Steering file meta-governance (5 qualities) |
| `DOD__` | DoD Gate Agent | Definition of Done validation |
| `CVR__` | Coverage Review Agent | Test coverage analysis |

### Pre-Release (Tier 3)

| Command | Agent | What It Does |
|---------|-------|--------------|
| `CMG__` | Change Management Agent | Release governance, rollback criteria |

### Planned (Coming Soon)

| Command | Agent | What It Does |
|---------|-------|--------------|
| `BLH__` | Backlog Health Agent | Backlog quality, user story health |
| `PFH__` | Portfolio Health Agent | Cross-project health, portfolio status |
| `UXC__` | UX Consistency Agent | Design system adherence, accessibility |

---

## The Chain — Execution Sequence

The canonical forward flow. Each package feeds the next.

```
Portfolio:  _ILC_ → _PILC_ → _PPM_
                         │
Edge:                  _FLO_  (routes between layers)
                         │
Project:   _POLC_ → _UXD_ → _ADLC_ → _DWG_ → AI-DLC v1 (build)
                                                     ▲
           _GCE_ + _TGE_ ── alongside AI-DLC v1 ───────┘
```

### Common Sequences (Copy & Follow)

**Full greenfield project (portfolio → code):**
```
_ILC_        ← capture & approve the idea
_PILC_       ← initiate the project (raw requirement → PIP)
_PPM_        ← register in portfolio, prioritize, dispatch
_FLO_        ← route to project layer
_POLC_       ← build the product backlog (PIP → PBP)
_UXD_        ← design the UX (PIP + PBP → UXP)
_ADLC_       ← design the architecture (PIP + PBP + UXP → AP)
_DWG_        ← generate the development workspace
_GCE_        ← derive governance layer
_TGE_        ← derive test governance
```

**Skip the portfolio layer (start at project):**
```
_PILC_       ← initiate directly from requirement
_POLC_ → _UXD_ → _ADLC_ → _DWG_ → _GCE_ → _TGE_
```

**Architecture-first (brownfield / existing backlog):**
```
_ADLC_       ← design architecture from existing PIP + PBP
_DWG_        ← generate workspace
_GCE_ → _TGE_
```

**Governance refresh on existing workspace:**
```
_GCE_        ← re-derive compliance layer
_TGE_        ← re-derive test governance
```

---

## Multi-Project Management

For workspaces with multiple projects under `projects/`:

| Command | What It Does |
|---------|--------------|
| `_APROJ_` | List all projects, switch the ★ active project |
| `_PPM_` | Portfolio-wide view — all projects, prioritization, governance decisions |
| `_FLO_` | Routing — check package positions across all projects |

After switching with `_APROJ_`, all per-project packages (PILC/ADLC/UXD/POLC/DWG) default to the newly active project.

---

## State & Status Checks

Quick read-only queries you can paste anytime:

| Prompt | What You Get |
|--------|--------------|
| `_ACTIVE_` | Current active package + state marker status |
| `What's the current project status?` | Summary from the active state marker |
| `Show me the chain position for this project` | Where the project is in the PDLC flow |
| `List all open items` | Outstanding work across active packages |

---

## Tier Model (Progressive Governance)

AI-GCE activates governance progressively. Higher tiers unlock as the project matures.

| Tier | When | What Activates |
|------|------|----------------|
| **Tier 1** | Day 0 — workspace generated | Foundational hooks + `IQA__`, `ADA__`, `WIA__`, `TGV__`, `SDC__` |
| **Tier 2** | Sprint 2+ (manual or auto) | Sprint governance + `SGV__`, `CRV__`, `SQC__`, `DOD__`, `CVR__` |
| **Tier 3** | Pre-release readiness | Release governance + `CMG__` |

To check current tier: `_GCE_` → ask "What tier is active?"

---

## Quick Reference — Key Outputs

Each package produces a named output that feeds downstream:

| Package | Output Name | Abbreviation | Consumed By |
|---------|-------------|:------------:|-------------|
| AI-ILC | Approved Idea Brief | — | AI-PILC, AI-PPM |
| AI-PILC | Project Initiation Package | **PIP** | AI-POLC, AI-UXD, AI-ADLC, AI-PPM |
| AI-PPM | Portfolio Register | — | AI-FLO (dispatch) |
| AI-FLO | Routing Decision | — | Next package in chain |
| AI-POLC | Product Backlog Package | **PBP** | AI-UXD, AI-ADLC, AI-DWG |
| AI-UXD | UX Design Package | **UXP** | AI-ADLC, AI-DWG, AI-GCE |
| AI-ADLC | Architecture Package | **AP** | AI-DWG |
| AI-DWG | Development Workspace | **DW** | AI-GCE, AI-TGE, AI-DLC v1 |
| AI-GCE | Compliance Layer | — | AI-DLC v1 (enforcement) |
| AI-TGE | Test Governance Layer | — | AI-DLC v1 (quality) |

---

## Tips

- **Package keys are deterministic** — `_PILC_` always activates AI-PILC, no ambiguity.
- **Agent shortcuts are audit-safe** — they never modify files, only report and advise.
- **You don't need to memorize the chain** — AI-FLO can route you to the right next package automatically.
- **Packages auto-resume** — if a state marker exists (e.g. `pilc-state.md`), the package picks up where you left off.
- **Tier upgrades are non-destructive** — Tier 2/3 adds governance; it never removes Tier 1 protections.

---

## See Also

| Document | What It Covers |
|----------|----------------|
| `TRIGGER_KEYS_REFERENCE.md` | Full trigger specification + rules |
| `FAMILY_STRUCTURE.md` | Package structure + output trees |
| `INSTALL_GUIDE_KIRO.md` | How to install the PDLC family |
| `contracts/AGENT_GOVERNANCE_CONTRACT.md` | Agent lifecycle, escalation, naming |
| `contracts/OUTPUT_AND_STATE_CONTRACT.md` | Multi-project layout + state markers |

---

*Part of the AI-* PDLC Family · AIFLC*
