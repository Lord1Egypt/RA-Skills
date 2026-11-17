# Pattern: Progressive Activation

**Purpose:** Documents the reusable design pattern where capabilities are introduced in stages matched to readiness — tiers in governance, depth levels in workflows, and modes in generators — so users are never overwhelmed by full capability on day one.

---

## The Pattern

```
FULL CAPABILITY (everything the package can do)
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  PROGRESSIVE ACTIVATION                                              │
│                                                                      │
│  Level 1 (minimal/foundational)  → Active immediately                │
│  Level 2 (standard)              → Activated on readiness signal      │
│  Level 3 (comprehensive/advanced)→ Activated on maturity signal       │
│                                                                      │
│  Each level INCLUDES all previous levels (additive, never replacing) │
└─────────────────────────────────────────────────────────────────────┘
```

**One sentence:** Ship all capability but activate progressively — start with what's essential, graduate when ready, never force the full weight upfront.

---

## Where It's Used

| Package | Activation Mechanism | Levels | What Progresses |
|---------|---------------------|:------:|-----------------|
| **AI-GCE** | Governance Tiers | 3 | Rules enforced (Tier 1: 5-8 → Tier 2: +15 → Tier 3: +20) |
| **All lifecycle packages** | Depth Levels | 3 | Detail produced (Minimal → Standard → Comprehensive) |
| **AI-DWG** | Generation Modes | 4 | Scope of generation (Full → Delta → Brownfield → Extension) |
| **AI-ADLC** | Extension Opt-In | Per-extension | Constraints activated (core only → core + DDD → core + DDD + Resilience) |
| **AI-POLC** | Tier Activation | 2 | Capabilities active (Tier 1 gap-filling → Tier 2 full PO discipline) |
| **AI-TGE** | Phase Activation | 2 | Operations mode (Strategy derivation → continuous Observation) |

---

## Why This Pattern Exists

**The problem it solves:** Tools with full capability active from day one overwhelm users. The reaction is predictable: "this is too much" → disable/ignore/abandon. Progressive activation gives users the right amount at the right time.

**Three failure modes it prevents:**

| Failure Mode | Without Progressive Activation | With Progressive Activation |
|-------------|-------------------------------|------------------------------|
| **Overwhelm** | 45 rules day one → team rejects all governance | 5 rules day one → team accepts, graduates later |
| **Over-engineering** | Full comprehensive output for a simple project | Minimal output that's proportional to complexity |
| **Premature optimization** | Advanced patterns forced before basics are stable | Extensions activate only when architecture demands |

---

## The Readiness Signal Pattern

Every progressive activation uses measurable signals (not gut feel):

### Governance Tiers (AI-GCE)

| From → To | Signal | Threshold |
|-----------|--------|-----------|
| Tier 1 → Tier 2 | Compliance score sustained | ≥ 90% for 2+ weeks |
| Tier 2 → Tier 3 | Compliance score + infrastructure | ≥ 85% for 4+ weeks + production infra exists |

### Depth Levels (All Packages)

| Level | Signal (at selection time) | Indicators |
|-------|---------------------------|-----------|
| Minimal | Low complexity detected | Solo dev, internal tool, <2 week timeline, POC |
| Standard | Normal complexity (default) | 2-8 person team, production-bound, some integrations |
| Comprehensive | High complexity detected | Enterprise, regulated, multi-team, 5+ integrations |

### Extension Activation (AI-ADLC)

| Extension | Signal | Architectural Evidence |
|-----------|--------|----------------------|
| DDD Tactical | Complex domain | Multiple bounded contexts identified at Stage 4 |
| Microservices | Service decomposition | ≥3 independent services at Stage 5 |
| Resilience | Integration density | ≥3 external integrations at Stage 11 |

---

## Implementation Anatomy

### The Additive Guarantee

Each level INCLUDES everything from lower levels:

```
Tier 1: [GOV-01, GOV-02, SESSION-01, NAME-01, SEC-01, SEC-02]
Tier 2: [GOV-01, GOV-02, SESSION-01, NAME-01, SEC-01, SEC-02] + [ARCH-01..05, API-01..03, TEST-01..03]
Tier 3: [everything in Tier 1+2] + [PERF-01..03, A11Y-01..02, DEPLOY-01..03, OBS-01..04]
```

**Never:** "Tier 2 replaces Tier 1 rules" — levels are cumulative.

### The Grace Period Pattern

Every activation includes a transition period:

```
Readiness confirmed → Team approves → Grace period (advisory-only) → Full enforcement
```

During grace period:
- New rules fire but DON'T block
- Team sees what would be enforced
- Gives time to fix easy violations before blocking starts
- Duration: typically 3-7 days

### The Override Guarantee

Users can always:
- Stay at a lower level indefinitely (no forced graduation)
- Override depth per-package (downstream doesn't have to match upstream)
- Disable specific items within a level (with documented rationale)
- Roll back to a lower level if the current level isn't working

---

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Three levels (not two, not five) | Two is too coarse (no middle ground); five is too granular (analysis paralysis). Three maps to natural complexity bands. |
| Additive (not replacing) | Users never lose capability they've internalized. Downgrade means "fewer additional things," not "different things." |
| Signal-based (not time-based) | "4 weeks" doesn't mean ready. "90% compliance for 2 weeks" means demonstrated mastery. |
| Human-confirmed (not auto-activated) | Readiness signals suggest; humans decide. No surprise escalation. |
| Package-specific implementation | Depth, tiers, modes, and extensions are ALL progressive activation — but each package implements it in its domain-appropriate way. |

---

## When to Apply This Pattern

Apply when:
- [ ] A package has capability that varies in intensity/depth/scope
- [ ] Full capability from day one would overwhelm or slow users
- [ ] Natural progression exists (beginner → intermediate → advanced)
- [ ] Readiness can be measured (not just time-based)
- [ ] Users benefit from starting small and growing (not just from having everything)

Don't apply when:
- The capability is atomic (either you use it or you don't — no middle ground)
- All users need full capability immediately (e.g., core workflow file)
- Progressive disclosure would hide critical safety features

---

## Related Documents

| Document | Location |
|----------|----------|
| How Tiered Governance Works | `knowledge_docs/HOW_TIERED_GOVERNANCE_WORKS.md` |
| How Depth Levels Work | `knowledge_docs/HOW_DEPTH_LEVELS_WORK.md` |
| How ADLC Extensions Work | `knowledge_docs/HOW_ADLC_EXTENSIONS_WORK.md` |
| How to Scale Governance as Project Matures | `knowledge_docs/HOW_TO_SCALE_GOVERNANCE_AS_PROJECT_MATURES.md` |
| Why Progressive Governance Matters | `knowledge_docs/WHY_PROGRESSIVE_GOVERNANCE_MATTERS.md` |
| Why Depth Calibration Matters | `knowledge_docs/WHY_DEPTH_CALIBRATION_MATTERS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
