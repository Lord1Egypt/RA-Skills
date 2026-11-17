# Interaction Between Depth Levels and Governance

**Purpose:** Maps how the depth level chosen at workflow start affects what governance is available, what tiers are accessible, and how thin vs. rich steering shapes the governance layer.

---

## The Interaction

Depth affects governance through a causal chain:

```
DEPTH LEVEL (chosen at AI-PILC or entry point)
    │
    ├── Affects AI-PILC output richness (thin vs. detailed PIP)
    │       │
    │       └── Affects AI-ADLC input (how many constraints visible)
    │               │
    │               └── Affects AP richness (how many ADRs, how detailed)
    │                       │
    │                       └── Affects AI-DWG output (how many steering files)
    │                               │
    │                               └── Affects AI-GCE derivation (how many rules derivable)
    │
    └── NET EFFECT: Depth determines the CEILING of governance achievable
```

---

## Depth → Steering → Governance Matrix

| Depth | Steering Files Generated | Rules Derivable | Max Practical Tier |
|-------|:------------------------:|:---------------:|:------------------:|
| **Minimal** | 6-8 essential files | 10-15 rules | Tier 1 (maybe partial Tier 2) |
| **Standard** | 14-19 files | 25-35 rules | Tier 2 (Tier 3 possible) |
| **Comprehensive** | 19+ files + conditionals | 35-50+ rules | Full Tier 3 |

---

## Minimal Depth + Governance

### What You Get

| AI-DWG Output | Governance Derivable |
|--------------|---------------------|
| `workspace-rules.md` | Basic project context rules |
| `tech-stack.md` | Language/framework naming rules |
| `security-rules.md` | Basic security (secrets, validation) |
| `naming-conventions.md` | Naming enforcement |
| `session-governance.md` | Session discipline |
| `testing-strategy.md` (lightweight) | Basic test presence rules |

### What You Don't Get

- No `api-standards.md` (API not detailed at Minimal depth) → No API-* rules
- No `module-structure.md` (L3 components not designed) → No ARCH boundary rules
- No conditional files (extensions not evaluated) → No extension-specific governance
- Limited `testing-strategy.md` → Minimal test governance

### Governance Ceiling

- **Tier 1:** Fully achievable (baseline + minimal steering covers all Tier 1 rules)
- **Tier 2:** Partially achievable (some Tier 2 rules can't be derived without richer steering)
- **Tier 3:** Not practical (insufficient steering for performance/deployment rules)

### When This Is Fine

Minimal depth + Tier 1 governance is appropriate for: POCs, internal tools, solo developers, <2 week projects. The governance matches the project weight.

---

## Standard Depth + Governance

### What You Get

Full steering set (14-19 files) covering:
- Architecture boundaries (from L2-L3 decomposition)
- API contracts (from API architecture stage)
- Security model (from security stage)
- Test strategy (from quality planning)
- All conditional files triggered by architecture

### Governance Ceiling

- **Tier 1:** Fully achievable
- **Tier 2:** Fully achievable (all Tier 2 rules derivable from standard steering)
- **Tier 3:** Mostly achievable (depends on whether performance/accessibility NFRs were captured)

### The Sweet Spot

Standard depth produces enough steering for full Tier 2 governance — which is appropriate for most production projects. Tier 3 is achievable if the project has production infrastructure.

---

## Comprehensive Depth + Governance

### What You Get

Maximum steering (19+ files + all conditionals) including:
- Detailed performance requirements (from extended NFR analysis)
- Accessibility requirements (from comprehensive quality planning)
- Deployment patterns (from operational architecture)
- Every extension evaluated (maximum conditional generation)

### Governance Ceiling

- **Tier 1:** Fully achievable
- **Tier 2:** Fully achievable
- **Tier 3:** Fully achievable (all advanced rules have sufficient steering to derive from)

---

## Upgrading Depth to Unlock Governance

If you're at Tier 1 and want Tier 2, but your steering is too thin:

```
Current: Minimal depth → 8 steering files → Tier 1 only

Problem: Want Tier 2 but API-* and ARCH-* rules can't be derived (no api-standards.md, no module-structure.md)

Solution:
1. Return to AI-ADLC → run Stages 10-12 (API, integration, components)
2. Re-run AI-DWG → generates api-standards.md, module-structure.md
3. Re-run AI-GCE → derives API-* and ARCH-* rules
4. Tier 2 now achievable

OR (faster):
1. Manually create api-standards.md and module-structure.md
2. Re-run AI-GCE → derives rules from manual steering
3. Less traceability but same enforcement
```

---

## The Baseline Safety Net

Regardless of depth, the built-in baseline ensures minimum governance:

| Depth | Steering-Derived Rules | Baseline Rules | Total Minimum |
|-------|:---------------------:|:--------------:|:-------------:|
| Minimal | ~5 | 10 | 15 |
| Standard | ~20 | 10 | 30 |
| Comprehensive | ~35+ | 10 | 45+ |

**The baseline protects Minimal depth projects.** Even with thin steering, you get: author≠approver, spec-first, no secrets, naming basics, session discipline. These are non-negotiable regardless of depth.

---

## Related Documents

| Document | Location |
|----------|----------|
| How Depth Levels Work | `knowledge_docs/HOW_DEPTH_LEVELS_WORK.md` |
| How Tiered Governance Works | `knowledge_docs/HOW_TIERED_GOVERNANCE_WORKS.md` |
| Pattern: Progressive Activation | `knowledge_docs/PATTERN_PROGRESSIVE_ACTIVATION.md` |
| Pattern: Two-Source Model | `knowledge_docs/PATTERN_TWO_SOURCE_MODEL.md` |
| When to Use Minimal vs Comprehensive | `knowledge_docs/WHEN_TO_USE_MINIMAL_VS_COMPREHENSIVE.md` |
| When to Activate Next Governance Tier | `knowledge_docs/WHEN_TO_ACTIVATE_NEXT_GOVERNANCE_TIER.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
