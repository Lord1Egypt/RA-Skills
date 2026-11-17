<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 1: Portfolio Detection & Initialization

**Phase:** Intake
**Purpose:** Detect whether a Portfolio Register already exists, determine the operational mode and depth level, and establish the engine's working context for this session.

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | Small portfolio (≤3 projects). Lightweight register, simple state file. Skip extension scanning. |
| **Standard** | Medium portfolio (4-10). Full register structure, governance cadence established, extensions scanned. |
| **Comprehensive** | Large portfolio (10+). Full register + all applicable extensions activated. Detailed cadence. |

---

## Step-by-Step Execution

### Step 1.1: Scan for Existing Portfolio

> **Fixed location (install-lock).** AI-PPM does **not** scan arbitrary or user-specified paths and never asks where the portfolio lives. The portfolio area is always the family-workspace path `pdlc-ws/portfolio/`, created by the installer (`OUTPUT_AND_STATE_CONTRACT.md` §5).

Check for `ppm-state.md` at the fixed portfolio location:
- `pdlc-ws/portfolio/ppm-state.md`

**If found:** Load state and follow resume protocol (see `session-continuity.md`). Skip remaining steps.

**If not found:** This is a fresh portfolio. Continue to Step 1.2.

### Step 1.2: Scan for Available Upstream Sources (Same Layer — Direct)

Scan for Portfolio-layer siblings:

| Source | Marker | Detection |
|---|---|---|
| AI-PILC output(s) | `pilc-state.md` with Status: Complete | Scan `pdlc-ws/projects/*/pip/` |
| AI-ILC output(s) | `ilc-state.md` with Route: project + Status: Approved/Complete | Scan `pdlc-ws/ideas/` |

Report findings:
```
📂 Upstream scan results:
   • PILC PIPs found: {N} ({list project names})
   • ILC Approved Briefs found: {N} ({list idea names})
   • Total potential portfolio entries: {N}
```

### Step 1.3: Determine Portfolio Size & Depth

Ask user or infer from scan:

```
Q-01: Portfolio scope — how many projects will this portfolio govern?

Options:
(a) Small (1-3 projects) → Minimal depth
(b) Medium (4-10 projects) → Standard depth
(c) Large (10+ projects) → Comprehensive depth
(d) I'm not sure yet — start with what's available and adjust

Recommended: Based on {N} upstream sources detected, option {x}.
```

### Step 1.4: Confirm Output Location (No User Choice)

The output location is **fixed** by the install-lock design — the user has **no authority to select it**. All portfolio governance artifacts live at the family-workspace portfolio area `pdlc-ws/portfolio/`, created by the installer. Do **not** present a "where should this live?" question. State the location for transparency only:

```
📁 Portfolio governance artifacts will be written to: pdlc-ws/portfolio/
   (fixed family-workspace location — not configurable)
```

### Step 1.5: Check FLO Availability

Scan for AI-FLO installation indicators:
- Look for `flo-state.md` or FLO configuration markers
- If found: Cross-layer communication is automated
- If not found: Cross-layer communication will use manual fallback

Report:
```
🔗 Cross-layer communication:
   • AI-FLO: {Detected — automated roll-ups available | Not detected — manual updates mode}
```

### Step 1.6: Initialize State

Create `ppm-state.md` with:
- Engine Status: Phase 1, Stage 1 complete
- Depth Level: as determined
- FLO Status: connected or fallback-manual
- Portfolio Summary: all zeros (empty portfolio)
- Strategic Objectives: empty (established in Stage 3)
- Governance Cadence: defaults based on depth

Create output folder structure at the fixed location:
```
pdlc-ws/portfolio/
├── ppm-state.md
├── portfolio-register.md (empty template)
├── portfolio-decisions/
├── dispatch-authorizations/
├── dashboards/
└── management_framework/ (if spine not already present)
```

### Step 1.7: Present Confirmation

```
✅ Portfolio initialized
📁 Location: pdlc-ws/portfolio/ (fixed family-workspace location)
📊 Depth: {level}
🔗 FLO: {status}
📋 Upstream sources detected: {N} PIPs, {M} Idea Briefs

Ready to register projects into the portfolio.
Proceed to Project Registration? [Yes / Adjust configuration]
```

---

## Gate

User confirms initialization is correct → proceed to Stage 2.

---

## Outputs

| Artifact | Status |
|---|---|
| `ppm-state.md` | Created (initial state) |
| `portfolio-register.md` | Created (empty template) |
| Output folder structure | Created |

---

## Management Framework Contribution

If the shared governance spine (`management_framework/MANAGEMENT_FRAMEWORK.md`) does not exist at `pdlc-ws/portfolio/`, create it with PPM as the first contributor. If it exists, register PPM as a contributing phase.

Entry: `PPM-D-001: Portfolio initialized. Depth = {level}. Source: {N} PIPs + {M} briefs detected.`

---

*This stage runs once at portfolio creation. On subsequent sessions, the resume protocol in `session-continuity.md` handles re-entry.*
