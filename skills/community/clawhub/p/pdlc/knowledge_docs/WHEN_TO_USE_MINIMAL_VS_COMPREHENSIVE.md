# When to Use Minimal vs. Standard vs. Comprehensive Depth

**Decision:** Which depth level matches my project? How do I avoid over-engineering simple projects or under-specifying complex ones?

**Derived from:** Pattern: Progressive Activation + Pattern: Adaptive Intake

---

## The Decision at a Glance

| Depth | Choose When | Time Investment | Output Volume |
|-------|------------|:---------------:|:-------------:|
| **Minimal** | Simple, low-risk, solo/small team, POC | 1-2 sessions per package | Core artifacts only |
| **Standard** | Most projects (recommended default) | 2-4 sessions per package | Full stage output |
| **Comprehensive** | Enterprise, regulated, high-risk, multi-team | 4-8 sessions per package | Extended analysis |

**When in doubt → Standard.** It's the default because it serves the widest range of projects well.

---

## Minimal Depth

### Choose Minimal When

- Solo developer or 2-person team
- Internal tool or proof-of-concept
- Timeline < 2 weeks
- No external integrations (or just 1)
- No regulatory/compliance requirements
- Familiar domain (team has done this before)
- Throwaway / experimental (might discard)

### What You Get

| Package | Minimal Behavior |
|---------|-----------------|
| AI-PILC | Core artifacts only (requirements, charter, risk register). Skips deep feasibility, detailed stakeholder maps. |
| AI-ADLC | L1-L2 architecture only. Skips detailed design stages (9-12). Fewer ADRs. |
| AI-DWG | Essential steering files only. Fewer conditional files generated. |
| AI-GCE | Tier 1 governance only. Minimal hook set. |
| AI-TGE | Baseline test requirements only. No architecture-derived register. |

### What You Risk

- Missing constraints discovered mid-delivery
- Architecture gaps at integration points
- Less context for AI-DLC v1 sessions (thinner steering)
- Harder to upgrade later if project grows in complexity

---

## Standard Depth (Default)

### Choose Standard When

- Team of 2-8 people
- Production-bound software
- 1-5 external integrations
- Normal business requirements
- Some compliance considerations
- Timeline 1-6 months
- **When you're not sure** (this is the safe default)

### What You Get

| Package | Standard Behavior |
|---------|-------------------|
| AI-PILC | Full 13-stage output. All registers, all assessments. |
| AI-ADLC | Full L1-L3 decomposition. All ADRs. Extension evaluation. |
| AI-DWG | All relevant steering files. Full template generation. |
| AI-GCE | Tier 1-2 governance available. Full hook coverage for active tier. |
| AI-TGE | Architecture-derived + baseline requirements. Full register. |

### What You Risk

- Very little. Standard is calibrated for the 80% case.
- Slightly more ceremony than strictly necessary for very simple projects.

---

## Comprehensive Depth

### Choose Comprehensive When

- Enterprise initiative (budget > $500K)
- Multi-team (5+ teams / 20+ people)
- Regulated industry (healthcare, finance, government)
- 5+ external integrations
- High security sensitivity (PII, financial data, critical infrastructure)
- Long-term system (3+ year maintenance horizon)
- Certification required (SOC 2, ISO 27001, HIPAA)
- **Multiple stakeholders with conflicting interests**

### What You Get

| Package | Comprehensive Behavior |
|---------|----------------------|
| AI-PILC | Extended analysis at every stage. Deep stakeholder power maps. Full communication strategy. |
| AI-ADLC | Full L1-L3 + all extensions evaluated. Deep security threat modeling. Migration path analysis in ADRs. |
| AI-DWG | All steering + operational docs + advanced templates. |
| AI-GCE | All three tiers available immediately. Extended rule sets. |
| AI-TGE | Full architecture-derived + baseline + NFR-specific requirements. Detailed risk scoring. |

### What You Risk

- Over-engineering if project doesn't warrant it
- Team frustration if depth feels disproportionate to actual complexity
- More time invested upfront (but prevents more time lost to rework)

---

## Depth Selection Signals

### Complexity Indicators (Scan Your Project)

| Signal | Score |
|--------|:-----:|
| Team size > 5 | +1 |
| External integrations > 3 | +1 |
| Regulatory requirements exist | +1 |
| Multi-tenancy required | +1 |
| Timeline > 6 months | +1 |
| Budget > $200K | +1 |
| Security-sensitive data | +1 |
| Multiple frontend channels | +1 |
| Existing system being extended | +1 |
| Cross-organizational stakeholders | +1 |

**Score → Depth:**
- 0-2: Minimal
- 3-5: Standard
- 6+: Comprehensive

---

## Can I Change Depth Mid-Workflow?

**Yes.** Depth is not a permanent commitment:

| Change | How | Impact |
|--------|-----|--------|
| Minimal → Standard | Update state file, re-run skipped stages | Adds missed artifacts (time investment) |
| Standard → Comprehensive | Update state file, deepen remaining stages | Richer analysis going forward |
| Comprehensive → Standard | Update state file, lighter remaining stages | Faster completion |
| Any → Minimal | Update state file, skip detailed stages | Faster but thinner output |

**Best practice:** If you realize mid-workflow that depth is wrong, change it NOW rather than completing at the wrong level.

---

## Depth Cascading

Depth chosen at entry cascades forward through the chain:

```
AI-PILC (Standard) → AI-ADLC inherits Standard → AI-DWG inherits Standard → AI-GCE inherits Standard
```

Each successor CAN override (choose different depth) but defaults to inheriting. This ensures proportional effort across the chain.

---

## Related Documents

| Document | Location |
|----------|----------|
| Pattern: Progressive Activation | `knowledge_docs/PATTERN_PROGRESSIVE_ACTIVATION.md` |
| How Depth Levels Work | `knowledge_docs/HOW_DEPTH_LEVELS_WORK.md` |
| Why Depth Calibration Matters | `knowledge_docs/WHY_DEPTH_CALIBRATION_MATTERS.md` |
| What If Wrong Depth Was Chosen | `knowledge_docs/WHAT_IF_WRONG_DEPTH_WAS_CHOSEN.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
