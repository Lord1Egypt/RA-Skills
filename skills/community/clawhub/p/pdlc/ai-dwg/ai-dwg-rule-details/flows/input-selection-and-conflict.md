<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Input Selection & Conflict Surfacing — Pre-Mode Gate

## Purpose

Defines the mandatory two-phase gate AI-DWG runs **after mode is determined but BEFORE any mode executes**. No mode (Full Generation, Delta Reconciliation, Brownfield Overlay) proceeds until this gate passes. It (a) selects the present peer inputs and discloses the quality impact of any absent input, (b) offers to complete installed-but-not-run packages, and (c) surfaces any cross-input conflict for the user to resolve.

This gate enforces the **Peer-Input Principle**: {ADLC, POLC, UXD} are equal-impact peers; any non-empty subset is valid; absence is acknowledged degradation, never silent degradation.

---

## Phase A: Peer-Input Selection

```
SCAN for marker files:
  adlc-state.md → ADLC peer (tech cluster)
  polc-state.md → POLC peer (product cluster)
  uxd-state.md  → UXD peer (UX cluster)

RESULT:
  IF zero found → BLOCK. Ask user: "No design packages detected. Point me to your input(s)."
  IF 1+ found  → record {present_inputs} set, proceed to quality-impact disclosure.

QUALITY-IMPACT DISCLOSURE (if <3 inputs):
  Present: [{list with paths}]
  Absent:  [{list}]

  Impact per absent input:
  • ADLC absent → tech steering (13+ files), src structure, technical-environment.md NOT produced.
                   AI-DLC v1 will lack: module layout, technology constraints, security rules, API standards.
  • POLC absent → vision.md, DEFINITION_OF_DONE.md, planning templates NOT produced.
                   AI-DLC v1 will lack: product context, success metrics, acceptance criteria.
  • UXD absent  → design-system.md, ui-implementation-spec.md, a11y baseline NOT produced.
                   AI-DLC v1 will lack: design tokens, component patterns, accessibility governance.

  "Proceed with {n}/3 inputs?" → USER MUST EXPLICITLY APPROVE.
  If user says no → ask which missing input to provide or point to.
```

### Quality-Impact Disclosure (Mandatory Before Proceeding)

When fewer than all three inputs are present, DWG MUST present:

```
⚠️ QUALITY-IMPACT DISCLOSURE

Present inputs: {list}
Absent inputs: {list}

Impact of absent inputs:
• {absent input}: Cannot produce {cluster list}. AI-DLC v1 will lack {what}.
• ...

Proceed with reduced coverage? (User must explicitly approve)
```

> **Detection + reduced-coverage default gate detail:** see `common/ap-reading-guide.md` ("Locate Peer Inputs"). The default start gate waits for all three peers; starting with fewer is a user-approved exception with acknowledged reduced coverage, never the silent default.

---

## Installed-Package Detection & Completion Offer (Mandatory Before Proceeding)

**Purpose:** When a peer package is *installed in the family* (its steering/rules exist in the workspace) but its *output marker is absent for the current project*, the user may have simply not run that package yet — not consciously decided to skip it. DWG MUST distinguish "package not available" from "package available but output not yet produced" and offer the user an informed choice.

**Detection logic:**

1. **Check package installation:** For each of {ADLC, POLC, UXD}, verify if the package's steering rules are installed in the workspace (i.e., the corresponding `ai-*-rules/` folder or setup exists).
2. **Check output presence:** For each installed package, check whether its output marker (`adlc-state.md`, `polc-state.md`, `uxd-state.md`) exists for the current project.
3. **Classify each peer:**
   - ✅ **Present** — marker found, output ready for consumption
   - ⚠️ **Installed but not run** — package exists in workspace but no marker/output for this project
   - ❌ **Not installed** — package not available in workspace (genuine absence)

**When at least one peer is classified "Installed but not run", DWG MUST present:**

```
📋 UPSTREAM PACKAGE STATUS

| Package | Status | What It Produces for DWG |
|---------|--------|--------------------------|
| AI-ADLC | {✅ Ready / ⚠️ Installed but not run / ❌ Not installed} | Architecture Package → tech steering + src structure |
| AI-POLC | {✅ Ready / ⚠️ Installed but not run / ❌ Not installed} | Product Backlog Package → vision, DoD, backlog scaffold |
| AI-UXD  | {✅ Ready / ⚠️ Installed but not run / ❌ Not installed} | UX Design Package → design system, frontend standards, accessibility |

⚠️ The following packages are installed but have not produced output for this project:
• {package list}

You have two options:
  [A] Go back and complete {package(s)} first, then return to AI-DWG
      → Richer workspace, more clusters generated, better AI-DLC v1 readiness
  [B] Skip and proceed with what's available now
      → DWG generates only the clusters for present inputs (reduced coverage)

Which do you prefer? (A / B / or specify which packages to complete)
```

**Rules:**
- This check runs AFTER peer-input scanning and BEFORE the Quality-Impact Disclosure.
- If the user chooses **[A]**, DWG MUST name the activation key(s) for the package(s) to complete (e.g., "Type `_ADLC_` to start your Architecture Package") and pause — it does NOT proceed with generation.
- If the user chooses **[B]**, DWG proceeds to the Quality-Impact Disclosure (which the user must still approve) and then generates with reduced coverage.
- If ALL three are "Present" (✅), this section is skipped entirely and DWG proceeds to generation.
- If a package is "Not installed" (❌), it is treated as genuinely absent — no completion offer for that package.

---

## Phase B: Cross-Input Conflict Surfacing

ADLC, POLC, and UXD are **designed not to overlap** — each owns a distinct domain (tech / product / UX). Conflict between them is an **anomaly** (an upstream error), not a normal operating case.

**When to check:** Only when 2+ inputs are present. A single input cannot conflict with itself.

**What to check (overlap detection):**

| Overlap Zone | How to Detect | Example Conflict |
|---|---|---|
| **Frontend framework** | ADLC Technology Stack specifies one framework; UXD design-system references a different component library | ADLC says "React 18"; UXD design tokens are built for Vue 3 |
| **Quality bar** | ADLC quality attributes vs. POLC Definition of Done define different coverage/performance thresholds | ADLC says "p99 < 200ms"; POLC DoD says "page load < 3s" (inconsistent granularity, not necessarily wrong) |
| **Accessibility level** | UXD accessibility baseline vs. ADLC Security/Compliance constraints specify different WCAG levels | UXD targets WCAG 2.1 AA; ADLC constraint says "WCAG 2.2 AAA required by regulation" |
| **User model** | UXD personas vs. POLC user segments describe different user populations | UXD personas are B2C end-users; POLC defines B2B admin-only user stories |
| **Naming/terminology** | ADLC bounded contexts use different domain terms than POLC product vocabulary | ADLC calls it "Tenant"; POLC calls it "Organization" for the same concept |

**Conflict surfacing protocol:**

```
IF overlap detected between two present inputs:

  ⚠️ CROSS-INPUT CONFLICT DETECTED

  Conflict: {description}
  Source A: {input} → {document} → {section/value}
  Source B: {input} → {document} → {section/value}

  Root cause analysis:
    {Why this likely happened — e.g., "UXD workflow ran against an outdated AP version",
     "POLC acceptance criteria were written before ADLC quality attributes were finalized"}

  Suggested correction:
    {Specific fix — e.g., "Re-run UXD Stage 9 with current AP tech-stack as input",
     "Align POLC DoD coverage threshold with ADLC quality attribute P3"}

  Options:
    (a) Fix upstream — go back and correct the source input, then re-run DWG
    (b) Override — record as ADR and proceed (DWG uses value from {recommended source})
    (c) Cancel — stop generation until resolved

  DWG does NOT proceed until user selects (a), (b), or (c).
  If (b): Record override as ADR in generated workspace. Provenance marks the override.
```

**Rules:**
1. DWG does **NOT** resolve conflicts. It surfaces them with analysis.
2. DWG does **NOT** apply a default or offer a "pick one" without explanation.
3. DWG does **NOT** proceed with a conflict unresolved — this is a hard gate.
4. If no conflicts detected → proceed silently (don't report "no conflicts found" — that's noise).
5. Multiple conflicts are surfaced one at a time. Each must be resolved before the next.

**Conflict vs. complementary content:**
Not all shared topics are conflicts. UXD providing frontend patterns alongside ADLC-defined frontend technology is **complementary** (UXD fills in design tokens; ADLC provides the framework). Only flag when values **contradict** (different answers to the same question).

---

*Pre-mode gate — runs before Mode 1 / Mode 2 / Mode 3. Loaded by `core-generator.md` after mode detection.*
