<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 16: Package Assembly & UXP README

## Purpose

Assemble all artifacts into the final UX Design Package, generate the reading guide (UXP_README.md), finalize the state file, and present the complete package to the user.

---

## Steps

### Step 1: Verify Artifact Completeness

Cross-check all expected artifacts against the state file's Completed Stages:

```markdown
## Artifact Verification Checklist

### Always Produced
- [ ] `uxd-state.md` (Stage 1)
- [ ] Research Synthesis (Stage 2)
- [ ] Persona Documents — {N} files (Stage 3)
- [ ] Journey Maps — {N} files (Stage 4)
- [ ] Information Architecture (Stage 5)
- [ ] User Flows — {N} files (Stage 6)
- [ ] Screen Inventory + Wireframe Specs (Stage 7)
- [ ] Design System documents (Stage 8)
- [ ] Design Tokens specification (Stage 8)
- [ ] Voice & Tone Guidelines (Stage 8)
- [ ] Component Inventory + Specs (Stage 9)
- [ ] Accessibility Baseline (Stage 11)
- [ ] Usability Test Plan (Stage 12)
- [ ] Design QA Framework (Stage 13)

### Conditionally Produced
- [ ] Multi-Brand Theming (Stage 10) — {Active/Skipped}
- [ ] i18n/Localization section (Stage 8) — {Active/Skipped}
- [ ] Service Blueprints (Stage 4) — {Active/Skipped}
- [ ] Empathy Maps (Stage 3) — {Active/Skipped}
```

If any expected artifact is missing → flag and either produce it or explain why it was omitted.

### Step 2: Generate UXP README

Produce `UXP_README.md` — the reading guide for anyone consuming the package:

```markdown
# UX Design Package — {Project Name}

## Overview
This package contains the complete UX design governance for {project}.
It was produced by AI-UXD v1.0.0 on {date}.

## Quick Reference
| Field | Value |
|-------|-------|
| Personas defined | {N} |
| Journeys mapped | {N} |
| Components specified | {N} |
| Design tokens defined | {N} |
| WCAG conformance target | Level {AA/AAA} |
| Depth level | {Minimal/Standard/Comprehensive} |

## Reading Order
For a first-time reader, read in this order:
1. This README (you're here)
2. Research Synthesis → understand the evidence base
3. Personas → understand who we're designing for
4. Journey Maps → understand what they experience
5. Information Architecture → understand how content is organized
6. User Flows → understand task-level interaction
7. Design System → understand the visual/verbal system
8. Component Library → understand the building blocks
9. Accessibility Baseline → understand compliance requirements
10. Design QA Framework → understand how to maintain quality

## Artifact Index

### Research & Users
| Artifact | Path | Produced by Stage |
|----------|------|-------------------|
| Research Synthesis | `01_Research_Synthesis.md` | 2 |
| Personas | `02_Personas/Persona_*.md` | 3 |
| {Empathy Maps} | `Empathy_Maps/*.md` | 3 (Comprehensive) |

### Structure & Flows
| Artifact | Path | Produced by Stage |
|----------|------|-------------------|
| Journey Maps | `03_Journey_Maps/Journey_*.md` | 4 |
| {Service Blueprints} | `Service_Blueprints/*.md` | 4 (Comprehensive) |
| Information Architecture | `04_Information_Architecture.md` | 5 |
| User Flows | `05_User_Flows/Flow_*.md` | 6 |

### Design System
| Artifact | Path | Produced by Stage |
|----------|------|-------------------|
| Screen Inventory | `06_Wireframe_Specifications/Screen_Inventory.md` | 7 |
| Wireframes | `06_Wireframe_Specifications/Wireframe_*.md` | 7 |
| Design System Foundation | `07_Design_System/*.md` | 8 |
| Design Tokens | `07_Design_System/Design_Tokens.md` | 8 |
| Voice & Tone | `07_Design_System/Voice_Tone_Guidelines.md` | 8 |
| Component Library | `08_Component_Library/*.md` | 9 |
| {Multi-Brand Theming} | `09_Multi_Brand_Theming.md` | 10 |

### Validation & Governance
| Artifact | Path | Produced by Stage |
|----------|------|-------------------|
| Accessibility Baseline | `10_Accessibility_Baseline.md` | 11 |
| Usability Test Plan | `11_Usability_Test_Plan.md` | 12 |
| Design QA Framework | `12_Design_QA_Framework.md` | 13 |

## Traceability Map
```
Persona → Journey → Flow → Screen → Component → Token → Principle
   ↓         ↓        ↓       ↓         ↓         ↓
 POLC      POLC    Wireframe  Inv.    Library    System
```

Every artifact traces forward and backward through this chain.
To verify traceability: pick any token → trace back to the principle
it serves → forward to the component that uses it → to the screen
it appears on → to the flow that contains it → to the journey stage
it serves → to the persona whose goal it enables.

## Downstream Consumers
| Package | What They Receive | Artifacts |
|---------|------------------|-----------|
| AI-POLC | Personas + Journeys | `02_Personas/`, `03_Journey_Maps/` |
| AI-DWG | Design System + Tokens + Components | `07_Design_System/`, `08_Component_Library/` |
| AI-GCE | Accessibility Baseline + Design Rules | `10_Accessibility_Baseline.md`, token spec |

## How to Update This Package
1. Identify what changed (new research, revised design decision, implementation feedback)
2. Update the affected artifact(s)
3. Check traceability (does the change ripple to connected artifacts?)
4. Log the change in `management_framework/Change_Log.md` as `UXD-C-NNN`
5. Signal downstream consumers if their handoff artifacts are affected
```

### Step 3: Finalize State File

Update `uxd-state.md`:
- Status: Complete
- All stages in Completed Stages table
- All downstream signals updated
- Final `last_updated` timestamp

### Step 4: Present Completion Summary

```
╔══════════════════════════════════════════════════════════════╗
║         AI-UXD — UX Design Package Complete ✅               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Package: {Project Name}                                     ║
║  Completed: {date}                                           ║
║  Depth: {level}                                              ║
║                                                              ║
║  Produced:                                                   ║
║  • {N} personas                                              ║
║  • {N} journey maps                                          ║
║  • {N} user flows                                            ║
║  • {N} component specifications                              ║
║  • {N} design tokens                                         ║
║  • WCAG {level} accessibility baseline                       ║
║  • Design QA framework                                       ║
║                                                              ║
║  Handed off to:                                              ║
║  • AI-POLC ✅ (personas + journeys)                           ║
║  • AI-DWG ✅ (design system + tokens)                         ║
║  • AI-GCE ✅ (accessibility baseline)                         ║
║                                                              ║
║  Next steps:                                                 ║
║  • Run AI-ADLC to design the system architecture             ║
║  • Run AI-DWG to generate workspace with design steering     ║
║  • Run AI-GCE to enforce accessibility + design compliance   ║
║  • Use UXC__ agent for ongoing design quality governance      ║
║                                                              ║
║  🔀 Chain Navigation:                                         ║
║  • Sequential next: AI-ADLC (_ADLC_) — Architecture Design  ║
║  • Or ask AI-FLO: type _FLO_ for routing guidance            ║
║  • Dashboard data: type DAT__ pdlc/uxd to update dashboard   ║
║                                                              ║
║  ⚠️ IMPORTANT: Start the next package (AI-ADLC) in a NEW    ║
║  session. Each AI-* package loads a full workflow into        ║
║  context; a fresh session keeps it fast and focused.          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Gate

**Final approval — confirms the UXP is complete.**

User confirms:
- All expected artifacts are present
- UXP README is accurate
- Handoffs are complete
- Package is ready for downstream consumption

---

## Log

Update `uxd-state.md`:
- Status: Complete
- Current Stage: 16 (final)

Log completion in `management_framework/Decision_Log.md`:
`UXD-D-NNN: UX Design Package v1.0 declared complete. {artifact count} artifacts produced.`

---

## Post-Completion

After the UXP is complete, the package enters **maintenance mode**:
- Feedback from AI-DLC v1 (usability signals) triggers targeted revisions
- Design QA reports trigger component spec updates
- New features trigger persona/journey/flow additions
- The UXC__ agent governs ongoing consistency

No full re-run is needed for incremental changes — update affected artifacts, maintain traceability, signal downstream.
