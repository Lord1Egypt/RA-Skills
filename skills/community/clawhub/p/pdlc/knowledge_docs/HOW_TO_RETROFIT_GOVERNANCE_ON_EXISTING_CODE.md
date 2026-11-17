# How to Retrofit Governance on Existing Code

**Purpose:** Practical guide for bringing AI-GCE governance to a brownfield codebase — an existing project that was built without the AI-* Family chain. Covers: how to overlay governance non-destructively, how to baseline existing violations, and how to enforce progressively on NEW code without drowning in legacy debt.

---

## Who This Is For

Teams with an existing codebase (months or years old) that want automated governance without rewriting anything. You have working software, a team already delivering, and you want to introduce structure without disrupting flow.

---

## The Core Principle: Govern Forward, Baseline Backward

Retrofitting governance does NOT mean fixing everything that's wrong today. It means:
- **Baseline** existing violations (acknowledge them without blocking)
- **Enforce** rules on all NEW code from this point forward
- **Track** improvement over time (violations should decrease, never increase)

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                    │
│   EXISTING CODE          │        NEW CODE                         │
│   (pre-governance)       │        (post-governance)                │
│                          │                                         │
│   Baseline: 47 violations│        Enforce: zero tolerance          │
│   Track: improvement     │        Block: violations at commit      │
│   Fix: as you touch it   │        Audit: continuous                │
│                          │                                         │
│   "Fix when you're       │        "Never introduce new             │
│    in the neighborhood"  │         violations"                     │
│                          │                                         │
└──────────────────────────────────────────────────────────────────┘
```

---

## Before You Start

**You need:**
- AI-GCE installed in your workspace
- An existing codebase with SOME form of structure (any language, any framework)
- Willingness to create a few steering files (minimum: `workspace-rules.md`)

**You do NOT need:**
- AI-DWG to have generated the workspace
- AI-ADLC architecture documents (helpful but not required)
- The entire team to agree upfront (start small, demonstrate value)

---

## Step-by-Step Retrofit

### Step 1: Create Minimal Steering

AI-GCE needs at least one steering file to detect the workspace. Create:

```
.kiro/steering/
├── workspace-rules.md       ← REQUIRED: describes your project context
├── tech-stack.md            ← What technologies you use
└── naming-conventions.md    ← Your existing naming patterns
```

**Tip:** Write steering files that describe what you ALREADY DO (current conventions), not what you aspire to. Governance should codify reality first, then raise the bar incrementally.

**workspace-rules.md minimum:**
```markdown
# Workspace Rules
- Project: {your project name}
- Language: {primary language}
- Framework: {primary framework}
- Architecture: {monolith / microservices / modular monolith}
- Team size: {number}
```

### Step 2: Run AI-DWG in Brownfield Overlay Mode (Optional)

If you have architecture documents (formal or informal), AI-DWG Mode 3 can generate richer steering:

1. Point AI-DWG at your existing codebase
2. Provide whatever architecture docs exist
3. AI-DWG scans the codebase, generates steering files that match your ACTUAL structure
4. Review and approve — steering is added alongside your code, nothing is modified

**Skip this if:** You prefer to write steering files manually or don't have architecture docs.

### Step 3: Run Initial AI-GCE Derivation

1. Point AI-GCE at the workspace
2. Select **Tier 1 only** (critical: do NOT start at Tier 2 or 3 on brownfield)
3. AI-GCE derives rules from:
   - Your steering files (project-specific)
   - Built-in baseline (universal methodology rules)
4. Review generated rules and hooks

### Step 4: Run Baseline Scan

Before activating enforcement, capture the current state:

1. AI-GCE scans existing code against generated rules
2. Produces a **baseline report**: violation count per rule category
3. Records baseline in `.compliance-state.json`

```json
{
  "complianceTier": 1,
  "baselineDate": "2026-06-12",
  "baselineViolations": {
    "ARCH-01": 12,
    "SEC-01": 3,
    "NAME-01": 47,
    "GOV-01": 0
  },
  "enforceFrom": "2026-06-12",
  "score": 62
}
```

**Key field: `enforceFrom`** — violations in code committed BEFORE this date are baselined (tracked but not blocking). Violations in code committed AFTER this date are enforced (blocking).

### Step 5: Activate Enforcement (New Code Only)

With the baseline recorded:
- Hooks fire on NEW file edits, NEW commits, NEW PRs
- Existing violations are tracked but don't block
- New violations in new code are blocked immediately
- Existing files: enforce when MODIFIED (you touched it, you fix it)

### Step 6: Progressive Improvement

Over time:
- Pick one rule category per sprint to address in existing code
- Fix baselined violations as you naturally touch those files
- Track declining violation count (celebrate improvement)
- When Tier 1 baseline drops below threshold → consider Tier 2

---

## The "Fix When Touched" Rule

The most practical approach to legacy violations:

| Developer Action | Governance Behavior |
|-----------------|-------------------|
| Creates new file | Full enforcement — zero violations allowed |
| Modifies existing file | Enforce on changed lines + adjacent (new violations blocked, existing tracked) |
| Reads existing file (no changes) | No enforcement (you didn't touch it) |
| Refactors a module | Full enforcement on refactored code (you're already rewriting, fix violations) |

This prevents governance from becoming a blocker while ensuring every human touch improves the codebase.

---

## Steering Files for Brownfield

Write steering that reflects reality, then evolve it:

**Phase 1 — Codify current practice (week 1):**
- Document what naming conventions exist (even if inconsistent)
- Document what test expectations exist (even if not met)
- Document what architecture boundaries exist (even if violated)

**Phase 2 — Tighten standards (week 3-4):**
- Update naming-conventions.md to the desired standard (new code must follow)
- Add API standards for any new endpoints
- Add security rules you want enforced going forward

**Phase 3 — Expand scope (month 2+):**
- Add module-structure.md with boundary rules
- Add testing-strategy.md with coverage thresholds
- Consider Tier 2 activation

Each steering file addition triggers AI-GCE re-derivation — new rules generated automatically.

---

## Common Brownfield Scenarios

### "We have no tests"

- Start with: testing-strategy.md that requires tests on NEW code only
- AI-GCE derives: "any new file must have corresponding test file"
- Existing code: baselined at 0% coverage, tracked but not blocked
- Over time: coverage rises as new code (tested) replaces old code (untested)

### "Our naming is inconsistent"

- Start with: naming-conventions.md that defines the TARGET standard
- AI-GCE derives: naming enforcement hook on new files + modified files
- Existing violations: baselined, tracked
- Fix strategy: rename when refactoring (not as standalone cleanup sprints)

### "We have no API contracts"

- Start with: api-standards.md requiring OpenAPI spec for NEW endpoints
- AI-GCE derives: "no new endpoint without contract" rule
- Existing endpoints: baselined as undocumented
- Fix strategy: document existing APIs when you modify them

### "Architecture boundaries are violated everywhere"

- Start with: module-structure.md defining DESIRED boundaries
- AI-GCE derives: boundary enforcement on new imports/dependencies
- Existing violations: baselined (12 cross-boundary imports)
- Fix strategy: resolve when refactoring the involved modules

---

## What NOT to Do

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| Start at Tier 3 | Team rejects governance immediately — too much friction on day one |
| Require fixing all baseline violations first | Blocks all delivery for weeks; team resents governance |
| Enforce on existing code without baseline | Every build fails; no one can merge; governance gets disabled |
| Write aspirational steering (not reflecting reality) | Rules don't match codebase; false positives everywhere |
| Apply governance to one developer only | Creates resentment; governance must be universal to be respected |

---

## Measuring Success

Track these metrics weekly:

| Metric | Target Trajectory |
|--------|-------------------|
| Baseline violation count | Decreasing (as files are touched and fixed) |
| New violations introduced | Zero (enforcement catches them) |
| Compliance score | Increasing over time |
| Team friction reports | Decreasing (as team adapts) |
| Time to merge | Stable (governance shouldn't slow delivery significantly) |

---

## Related Documents

| Document | Location |
|----------|----------|
| How GCE Derivation Pipeline Works | `knowledge_docs/HOW_GCE_DERIVATION_PIPELINE_WORKS.md` |
| How GCE Rederivation Works | `knowledge_docs/HOW_GCE_REDERIVATION_WORKS.md` |
| How to Adopt Governance on a Project | `knowledge_docs/HOW_TO_ADOPT_GOVERNANCE_ON_A_PROJECT.md` |
| Why Governance Automation Matters | `knowledge_docs/WHY_GOVERNANCE_AUTOMATION_MATTERS.md` |
| Why Brownfield Awareness Matters | `knowledge_docs/WHY_BROWNFIELD_AWARENESS_MATTERS.md` (planned) |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
