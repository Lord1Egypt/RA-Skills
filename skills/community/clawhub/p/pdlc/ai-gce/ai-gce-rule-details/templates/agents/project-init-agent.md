<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "{upstream-steering-file}"
generatedOn: "{generation-date}"
ownership: generated
---
# Project Init Agent — Template

## Purpose

A custom agent that scaffolds a new project with compliance-ready structure from 5 questions. Activates Tier 1 automatically and initializes the compliance tracking infrastructure.

---

## Trigger

User says: "Init project" / "Scaffold project" / triggers project-kickoff hook.

---

## Questions (5 Only — Everything Else Derived)

| # | Question | Used For |
|---|----------|---------|
| 1 | Project name? | README, state file, dashboard |
| 2 | Modules in scope? | Folder structure, CODEOWNERS stubs, steering selection |
| 3 | Team size? | Role isolation depth, cognitive load rules |
| 4 | Project sponsor? | Governance artifacts |
| 5 | Target go-live date? | Phase timeline, tier progression estimate |

---

## Behavior

### Step 1: Derive Defaults
From the 5 answers, derive:
- Technology: from workspace `tech-stack.md` (already exists)
- Architecture: from workspace `module-structure.md` (already exists)
- Team topology: from team size (scaling rules)
- Phase durations: from module count + team size

### Step 2: Generate Governance Artifacts
- Project Charter (filled with answers)
- RACI Matrix (roles from team size rules)
- Definition of Done (from DoD steering)
- Risk Register (top 5 standard risks pre-filled)

### Step 3: Generate Steering (If Not Already Present)
If `rules/` is sparse or missing domain-specific files:
- Use `steering-templates/` to generate per-module domain steering
- Phase-context steering for current phase awareness

### Step 4: Install Tier 1 Hooks
Copy Tier 1 hook set into `.governance/hooks/`

### Step 5: Initialize State
Generate `.compliance-state.json` with Tier 1 active

### Step 6: Run Initial Audit
Trigger periodic-audit to establish baseline score

---

## Output

Complete project scaffold with:
- Governance artifacts (filled, not stubs)
- Tier 1 hooks active
- Compliance state initialized
- Initial audit score recorded
- Next actions checklist for the PM
