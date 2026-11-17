# Reference Map: Built-In Baseline Rules

**Purpose:** Complete reference of all 10 universal baseline rules that AI-GCE enforces regardless of steering content — the methodology floor that every project gets even with zero steering files.

---

## All Baseline Rules

| # | Rule ID | Rule Statement | Category | Tier | Source |
|---|---------|---------------|----------|:----:|--------|
| 1 | GOV-B01 | The author of a change MUST NOT be the sole approver of that change | Governance | 1 | AI-DLC v1 methodology (separation of duties) |
| 2 | GOV-B02 | Implementation MUST be preceded by specification (spec-before-code) | Session | 1 | AI-DLC v1 methodology (structured sessions) |
| 3 | GOV-B03 | Every pull request MUST have a description explaining what and why | Governance | 1 | Professional engineering practice |
| 4 | GOV-B04 | Changes to established baselines MUST have documented rationale | Governance | 1 | Change management principle |
| 5 | GOV-B05 | Significant decisions MUST be recorded with context and rationale | Governance | 1 | Decision traceability |
| 6 | GOV-B06 | Direct pushes to main/master branch are PROHIBITED | Governance | 1 | Branch protection |
| 7 | SEC-B01 | Secrets (API keys, passwords, tokens) MUST NOT appear in source code | Security | 1 | Security baseline |
| 8 | SEC-B02 | User-provided input MUST be validated before processing | Security | 1 | Input safety (OWASP) |
| 9 | SESSION-B01 | AI-assisted development sessions MUST follow structured discipline (not vibe-coding) | Session | 1 | AI-DLC v1 methodology |
| 10 | NAME-B01 | File and symbol naming MUST follow a consistent, documented convention | Quality | 1 | Codebase readability |

---

## Resolution With Project-Specific Rules

| Situation | Behavior |
|-----------|----------|
| Steering provides MORE specific rule on same topic | Project rule ENRICHES baseline (both apply) |
| Steering CONTRADICTS baseline | Project rule WINS (project authority > baseline) |
| Steering is SILENT on baseline topic | Baseline stands alone (minimum governance) |
| No steering exists at all | All 10 baseline rules active (minimum viable governance) |

**Example:** Baseline says "naming MUST follow a consistent convention" (generic). If `naming-conventions.md` exists, it provides SPECIFICS ("files use kebab-case, classes use PascalCase"). The baseline's generic rule is satisfied by the specific steering. Both contribute — no conflict.

---

## What Each Rule Prevents

| Rule | Without This Rule | Real-World Failure |
|------|------------------|-------------------|
| GOV-B01 | Self-merged PRs bypass all review | Auth bypass ships, discovered in prod 3 weeks later |
| GOV-B02 | Vibe-coded features with no spec | "That's not what I meant" at demo time |
| GOV-B03 | PRs with no context ("fix stuff") | Reviewers can't assess impact; merge blindly |
| GOV-B04 | Scope changes without assessment | 300% scope growth, budget exhausted at 60% |
| GOV-B05 | Why decisions were made is lost | "Why is this PostgreSQL and not MongoDB?" — no one knows |
| GOV-B06 | Untested code in main | CI breaks, deployment fails, team blocked |
| SEC-B01 | Hardcoded secrets in repo | API key leaked, service compromised in hours |
| SEC-B02 | SQL injection, XSS, path traversal | Data breach, compliance failure |
| SESSION-B01 | Unstructured AI sessions produce inconsistent code | Technical debt accumulates without awareness |
| NAME-B01 | 5 naming patterns in one project | Search fails, merge conflicts, cognitive overhead |

---

## Baseline vs. Tier 1

Baseline rules ARE Tier 1 rules — but not all Tier 1 rules are baseline:

```
TIER 1 RULES
├── Baseline rules (10) ← Always present, even with zero steering
└── Steering-derived Tier 1 rules ← Only present if steering exists
    ├── From naming-conventions.md → specific naming rules
    ├── From security-rules.md → specific security patterns
    └── From session-governance.md → specific session rules
```

**Baseline = the FLOOR of Tier 1.** Even a workspace with no steering gets these 10 rules. Steering adds MORE Tier 1 rules on top.

---

## Enforcement Mechanism

Each baseline rule has a corresponding enforcement:

| Rule | Hook Type | Event |
|------|-----------|-------|
| GOV-B01 | `askAgent` | preToolUse (shell — git push/merge) |
| GOV-B02 | `askAgent` | promptSubmit |
| GOV-B03 | `askAgent` | preToolUse (shell — git push) |
| GOV-B04 | `askAgent` | preToolUse (write — config/steering files) |
| GOV-B05 | `askAgent` | postToolUse (write — when decisions detected) |
| GOV-B06 | `askAgent` | preToolUse (shell — git push to main) |
| SEC-B01 | `askAgent` | preToolUse (write) |
| SEC-B02 | `askAgent` | postToolUse (write — API handlers) |
| SESSION-B01 | `askAgent` | promptSubmit |
| NAME-B01 | `askAgent` | fileCreated |

---

## Versioning

Baseline rules are versioned with the AI-GCE package:

- AI-GCE v1.0.0: 10 baseline rules (current)
- Future versions may add baseline rules (additive only — never remove)
- Updates ship with package updates
- New baseline rules on existing projects: added to Tier 1, grace period applied

---

## Related Documents

| Document | Location |
|----------|----------|
| Pattern: Two-Source Model | `knowledge_docs/PATTERN_TWO_SOURCE_MODEL.md` |
| How GCE Derivation Pipeline Works | `knowledge_docs/HOW_GCE_DERIVATION_PIPELINE_WORKS.md` |
| How Tiered Governance Works | `knowledge_docs/HOW_TIERED_GOVERNANCE_WORKS.md` |
| Why Separation of Duties Matters | `knowledge_docs/WHY_SEPARATION_OF_DUTIES_MATTERS.md` |
| Why Spec Before Code Matters | `knowledge_docs/WHY_SPEC_BEFORE_CODE_MATTERS.md` |
| Why Security Gates Matter | `knowledge_docs/WHY_SECURITY_GATES_MATTER.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
