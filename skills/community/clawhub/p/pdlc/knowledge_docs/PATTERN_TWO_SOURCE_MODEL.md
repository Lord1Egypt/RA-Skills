# Pattern: Two-Source Model

**Purpose:** Documents the reusable design pattern where a package derives output from TWO complementary sources — project-specific input (steering, architecture, configuration) plus a built-in universal baseline — ensuring coverage even when project-specific input is thin or absent.

---

## The Pattern

```
SOURCE 1: Project-Specific              SOURCE 2: Built-In Baseline
(from steering, AP, or config)          (universal minimums, always present)
        │                                       │
        └──────────── COMBINE ──────────────────┘
                         │
                         ▼
                  DERIVED OUTPUT
          (rules, requirements, scores)
```

**One sentence:** Always derive from what the project provides, but never leave gaps when the project provides nothing — the baseline fills the silence.

---

## Where It's Used

| Package | Source 1 (Project-Specific) | Source 2 (Baseline) | Output |
|---------|---------------------------|---------------------|--------|
| **AI-GCE** | `.kiro/steering/` files | 10 universal methodology rules | Compliance rules + hooks |
| **AI-TGE** | AP artifacts (API contracts, ADRs, security) | Universal test minimums (every function tested, error paths covered) | Test requirements register |
| **AI-ILC** | Configurable evaluation rubric (org-specific weights) | Universal thresholds (feasibility < 2/5 = auto-defer) | Evaluation scores |
| **AI-GCE Audit** | Project-specific rules (derived from steering) | Baseline violation tracking (brownfield) | Compliance score |

---

## The Resolution Logic

When both sources provide guidance on the same topic:

| Situation | Resolution |
|-----------|-----------|
| Source 1 provides specifics | Source 1 rules enriched; override baseline on that topic |
| Source 1 is silent | Baseline rules stand alone (still get governance) |
| Source 1 contradicts baseline | Source 1 WINS (project has authority over methodology) |
| No Source 1 at all (empty steering) | Baseline-only mode (minimum viable governance) |

**Key principle:** Project authority always wins over baseline. The baseline is a floor, not a ceiling. It prevents zero-governance gaps — it doesn't cap what the project can define.

---

## Why This Pattern Exists

**The problem it solves:** If rules are 100% derived from project-specific input, then "no input = no output." A workspace with empty steering gets zero governance. That's invisibly dangerous — the team doesn't know they're unprotected.

**The anti-pattern it prevents:** Making ALL rules derivation-only. This creates a "no steering = no governance" gap that's invisible until something goes wrong (security breach, unchecked merge, vibe-coded feature).

**The test:** "If I run this package against a workspace that has zero steering on [topic], does the user get ANY governance on that topic?" If the answer is "no" and the topic has universal best-practices → built-in baseline is missing.

---

## Implementation Anatomy

### AI-GCE Example

```
Built-in Baseline (10 universal rules):
├── GOV-01: Author ≠ approver
├── GOV-02: Spec before implementation
├── GOV-03: PR description required
├── SESSION-01: Structured session discipline
├── SEC-01: No secrets in source code
├── SEC-02: Input validation on public interfaces
├── NAME-01: Consistent naming (style from tech detection)
├── GOV-04: Change requires rationale
├── GOV-05: Decisions are recorded
└── GOV-06: No direct-to-main commits

Project-Specific (derived from steering):
├── ARCH-01: Module boundaries (from module-structure.md)
├── API-01: Contract-first (from api-standards.md)
├── API-02: Versioning required (from api-standards.md)
├── SEC-03: JWT validation (from security-rules.md)
├── TEST-01: 80% coverage threshold (from testing-strategy.md)
└── ... (as many as steering justifies)

Combined Output:
├── Baseline rules (always active, Tier 1)
├── Project-specific rules (active at appropriate tier)
└── No gaps on universal concerns regardless of steering depth
```

### AI-TGE Example

```
Built-in Baseline (universal test minimums):
├── Every public function has a test
├── Error paths are tested (not just happy path)
├── Regression test for every bug fix
├── New endpoints have input validation tests
├── Authentication flows are tested
└── Build must run tests (CI includes test execution)

Architecture-Derived (from AP):
├── TR-001: GET /users pagination test (from API Architecture §3.2)
├── TR-002: JWT expiry rejection (from Security Architecture §4.1)
├── TR-003: Order service → payment integration test (from Integration Map)
├── TR-004: Event immutability test (from ADR-005 Event Sourcing)
└── ... (one requirement per architectural commitment)

Combined Output:
├── Baseline ensures minimum test hygiene
├── Architecture-derived ensures design promises are verified
└── Both tracked in one unified register
```

---

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Baseline is ADDITIVE (never replaces project rules) | Project authority must always be respected |
| Baseline is small (10 rules, not 50) | Must be uncontroversial; "obviously right" rules only |
| Baseline is methodology-derived (not architecture-derived) | Architecture rules can't be universal (no two systems are alike); methodology rules can be |
| Resolution favors project on conflict | Teams know their context better than a generic baseline |
| Baseline is versioned with the package | Updates to baseline ship with package updates, not silently |

---

## When to Apply This Pattern (in new packages)

Apply the two-source model when:
- [ ] The package generates rules, requirements, or enforcement
- [ ] There's a realistic scenario where the input source is empty or thin
- [ ] Universal best-practices exist for the domain (not everything is project-specific)
- [ ] The cost of "no output when no input" is dangerous (governance gap, quality gap, test gap)

Don't apply when:
- The output is 100% project-specific by nature (e.g., architecture design can't have a "baseline architecture")
- There are no universal standards for the domain
- "No output" is an acceptable state (e.g., optional enrichment)

---

## Related Documents

| Document | Location |
|----------|----------|
| How GCE Derivation Pipeline Works | `knowledge_docs/HOW_GCE_DERIVATION_PIPELINE_WORKS.md` |
| How TGE Test Governance Works | `knowledge_docs/HOW_TGE_TEST_GOVERNANCE_WORKS.md` |
| How ILC Idea Lifecycle Works | `knowledge_docs/HOW_ILC_IDEA_LIFECYCLE_WORKS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
