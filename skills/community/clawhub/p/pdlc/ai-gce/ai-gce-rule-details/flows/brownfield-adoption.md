<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mode 3: Brownfield Incremental Adoption — Full Flow

## Purpose

This file holds the complete **Mode 3 (Brownfield Incremental Adoption)** flow: what brownfield means, the interaction model, and the 8-step overlay flow. Output skeletons live in `templates/compliance-log/brownfield-baseline.md` and `templates/compliance-log/incremental-adoption-plan.md`; the flow logic lives here.

The Mode 3 entry (purpose + trigger) lives in `core-generator.md` (the always-loaded dispatcher). Load this file when Mode 3 is detected.

---

## What Brownfield Means for Compliance

When a workspace has `brownfield-patterns.md` in its steering, it signals:
- The codebase predates AI-DWG governance
- Existing code may have violations of the rules that AI-GCE will derive
- Teams CANNOT be blocked on day 1 for violations that existed before governance was introduced

**Key principle:** The compliance engine enforces against NEW code immediately. It acknowledges existing violations as technical debt with a formal remediation SLA. Over time, the compliance score improves as legacy violations are resolved.

**Anti-pattern to avoid:** Generating the same hooks as Mode 1 but with looser thresholds. Brownfield mode is architecturally different — it operates with a baseline, a timeline, and a distinction between "new code violations" and "legacy violations."

## Interaction Model

1. **User invokes:** "Set up incremental compliance adoption" / "Brownfield baseline scan" / "Retrofit compliance"
2. **AI reads** workspace + `brownfield-patterns.md` for specific brownfield constraints
3. **AI runs** a baseline scan — identifies existing violations
4. **AI generates** the brownfield baseline document (acknowledged violations + SLAs)
5. **AI generates** the incremental adoption plan (enforcement timeline)
6. **AI generates** compliance rules and hooks configured for new-code-only enforcement
7. **AI generates** same artifacts as Mode 1, but with brownfield-adapted behavior
8. **AI presents** the baseline summary and adoption roadmap

## Brownfield Overlay Flow

```
STEP 1: READ WORKSPACE + BROWNFIELD SIGNALS
─────────────────────────────────────────────
Read all steering files (same as Mode 1 STEP 1)
ADDITIONALLY read:
• brownfield-patterns.md → understand characterization test requirements,
  strangler-fig boundaries, legacy API compatibility rules, data migration guardrails
• Existing codebase structure → identify which modules are LEGACY vs. NEW

From brownfield-patterns.md, determine:
• Which modules/folders are LEGACY (pre-governance code)
• Which modules/folders are NEW (post-governance code)
• Legacy API compatibility constraints
• Data migration guardrails in effect

STEP 2: RUN BASELINE SCAN
────────────────────────────
Perform a non-blocking catalog of current state:
For each rule category (that would be generated in Mode 1):
• Scan existing code patterns for rule violations
• Classify each violation: LEGACY (in existing code) vs. SCOPE UNKNOWN

Produce baseline catalog:

"📊 BROWNFIELD COMPLIANCE BASELINE

Scanned: {n} modules | {m} files
Project: {project name}

By rule category:
┌─────────────────────────┬──────────────┬─────────────────────────────────────┐
│ Rule Category           │ Status       │ Notes                               │
├─────────────────────────┼──────────────┼─────────────────────────────────────┤
│ Naming conventions      │ ⚠️ {n} gaps  │ {description of pattern variations} │
│ API contract-first      │ ✅ Compliant │ Existing endpoints documented        │
│ Module boundaries       │ ⚠️ {n} gaps  │ {description of cross-boundary deps} │
│ Security gates          │ ✅ Compliant │ Auth present on all routes           │
│ ...                     │ ...          │ ...                                 │
└─────────────────────────┴──────────────┴─────────────────────────────────────┘

Overall baseline score: {x}% compliant
New code will be enforced at: 100% from day 1
Legacy code remediation target: {date} (12-week default SLA)"

STEP 3: GENERATE BROWNFIELD BASELINE DOCUMENT
──────────────────────────────────────────────
Load: templates/compliance-log/brownfield-baseline.md

Generate .governance/brownfield-baseline.md:
• Summary of existing violations per category
• Designation: ACKNOWLEDGED LEGACY TECHNICAL DEBT
• Remediation SLA per category (default: 12 weeks from governance adoption date)
• Exception: security-critical violations get 2-week SLA regardless
• Sign-off line (team lead acknowledges the baseline)

This document transforms "violations" into "acknowledged technical debt with a plan."
Without it, the team would face hundreds of immediate blocks on day 1.

STEP 4: GENERATE INCREMENTAL ADOPTION PLAN
────────────────────────────────────────────
Load: templates/compliance-log/incremental-adoption-plan.md

Generate .governance/incremental-adoption-plan.md:

Phase 1 — Immediate (Week 0, day 1):
• New code MUST comply with all rules
• Hooks active for files CREATED after governance adoption
• Baseline violations documented and tracked

Phase 2 — Early Wins (Weeks 1-4):
• Resolve security-critical legacy violations (2-week SLA)
• Resolve naming convention violations in new modules
• Enable blocking mode for hooks on NEW code only

Phase 3 — Steady Progress (Weeks 5-8):
• Resolve high-priority legacy violations
• Extend blocking hooks to recently modified files
• First compliance score review

Phase 4 — Convergence (Weeks 9-12):
• Resolve remaining acknowledged violations
• Move all hooks to full enforcement
• Final compliance audit — target: 80%+ score
• Graduate from brownfield mode: full compliance engine active

STEP 5: GENERATE RULES WITH BROWNFIELD ANNOTATIONS
────────────────────────────────────────────────────
Same as Mode 1 STEP 3, with these additions:
• Each rule file includes a "Brownfield Note" section:
  "Existing violations acknowledged in .governance/brownfield-baseline.md.
   This rule enforces NEW code only until {remediation SLA date}."
• Rules reference the incremental-adoption-plan.md for timeline

STEP 6: GENERATE HOOKS WITH BROWNFIELD CONFIGURATION
──────────────────────────────────────────────────────
Same as Mode 1 STEP 4, with these critical differences:

For hooks watching CREATED files (fileCreated events):
→ Run at full enforcement immediately (new code = must comply)

For hooks watching EDITED files (fileEdited events):
→ Run in WARN mode for legacy module paths (don't block; inform)
→ Run in ENFORCE mode for new module paths (as defined by brownfield-patterns.md)

Brownfield hook configuration pattern:
Each hook prompt for legacy modules must include:
"[BROWNFIELD MODE] This file is in a legacy module. If this is a modification to
existing legacy code, note the violation in .governance/brownfield-baseline.md.
If this is new code added to a legacy module, it MUST comply with [rule reference]."

STEP 7: GENERATE REMAINING ARTIFACTS
──────────────────────────────────────
Same as Mode 1 STEPS 5-8 (audit agent, compliance log, COMPLIANCE_README)
Ensure COMPLIANCE_README includes a "Brownfield Adoption" section explaining:
• The baseline scan concept
• How the incremental adoption plan works
• How legacy violations are tracked
• How to graduate from brownfield mode to full enforcement

STEP 8: OUTPUT — Present Brownfield Summary
─────────────────────────────────────────────

"✅ AI-GCE BROWNFIELD ADOPTION INITIALIZED

📦 Compliance engine (incremental mode) for: {project name}
📁 Workspace: {workspace root}

📊 Baseline established:
   • Overall compliance score: {x}%
   • Categories fully compliant: {n}
   • Categories with legacy violations: {m}
   • Security violations (2-week SLA): {p}
   • General violations (12-week SLA): {q}

🔒 Immediate enforcement (new code):
   • {n} hooks active for newly created files
   • All rule categories enforced for NEW code from today

⏳ Incremental enforcement (legacy code):
   • Baseline documented: .governance/brownfield-baseline.md
   • Adoption plan: .governance/incremental-adoption-plan.md
   • Full compliance target: {date}

📋 Key files:
   • .governance/brownfield-baseline.md — acknowledged legacy violations
   • .governance/incremental-adoption-plan.md — enforcement timeline
   • .governance/COMPLIANCE_README.md — how to work with this compliance engine

🔗 Next steps:
   1. Review .governance/brownfield-baseline.md — acknowledge and sign off
   2. Read .governance/incremental-adoption-plan.md — understand the timeline
   3. Open this workspace as root in a NEW Kiro instance (or new IDE window)
   4. Install AI-DLC v1 (awslabs/aidlc-workflows) in the workspace — follow its install guide
   5. Begin development — new code is enforced from day 1; legacy follows the adoption plan
   6. Run weekly compliance audit (`CAA__`) to track improvement score

🔀 **Chain Navigation:**
   • Dashboard data: type `DAT__ pdlc/gce` to update the family dashboard

⚠️ **IMPORTANT: AI-DLC v1 runs in THIS workspace, but in a fresh IDE instance.**
   Close this planning session. Open the workspace folder as the ROOT
   of a fresh Kiro instance (or Cursor/Windsurf/Claude Code). AI-DLC v1
   is a separate product — install it yourself
   (github.com/awslabs/aidlc-workflows). The hooks, rules, and baseline
   AI-GCE produced are already in place for AI-DLC to operate within."
```
