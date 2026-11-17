# When to Use Brownfield vs. Greenfield Mode

**Decision:** Do I treat my project as a fresh start (greenfield) or as extending something that already exists (brownfield)?

**Derived from:** Pattern: Non-Destructive Reconciliation + Pattern: Adaptive Intake

---

## The Decision at a Glance

| Your Situation | Mode | What Packages Do Differently |
|---------------|------|------------------------------|
| No code exists yet, building from scratch | **Greenfield** | Full generation, complete architecture, all artifacts new |
| Existing codebase, adding governance/structure | **Brownfield** | Overlay only, non-destructive, adapt to what exists |
| Existing system being extended with new capability | **Brownfield** | Focus on delta, preserve existing, design only the new parts |
| Rewriting from scratch (existing system being replaced) | **Greenfield** | Even though old system exists, the new one starts fresh |
| Migrating (existing system being moved, not changed) | **Brownfield** | Preserve behavior, change infrastructure/platform |

---

## Greenfield Mode

### Choose Greenfield When

- No codebase exists (or the existing one is being scrapped)
- You're building something entirely new
- The team starts with a blank IDE and empty repo
- No existing conventions to respect (you're establishing them)
- No existing tests, CI, or governance to preserve

### What Packages Do in Greenfield

| Package | Greenfield Behavior |
|---------|-------------------|
| AI-PILC | "What do you want to build?" — full requirements capture from zero |
| AI-ADLC | Design from blank slate — all C4 levels, all decisions fresh |
| AI-DWG | Mode 1 (Full Generation) — generate everything: folders, steering, configs, CI |
| AI-GCE | Full derivation, no baseline scan — all rules are new |
| AI-TGE | Strategy derivation only — no existing tests to map |

---

## Brownfield Mode

### Choose Brownfield When

- A codebase already exists (any size, any age)
- The team has existing conventions (even if undocumented)
- CI/CD, tests, configs already exist and must be preserved
- You're adding capability to an existing system
- You're adding governance to a team that's already delivering
- An external system constrains your choices (dependencies, APIs, data formats)

### What Packages Do in Brownfield

| Package | Brownfield Behavior |
|---------|-------------------|
| AI-PILC | "What exists? What's changing? Extend vs. replace?" — delta-focused initiation |
| AI-ADLC | Load existing architecture, identify ONLY the delta (new components, changed integrations) |
| AI-DWG | Mode 3 (Brownfield Overlay) — add governance WITHOUT touching existing code |
| AI-GCE | Baseline existing violations, enforce only on NEW code, track improvement |
| AI-TGE | Brownfield assessment (Stage 4) — scan existing tests, map coverage, find gaps |

---

## The Key Differences

| Dimension | Greenfield | Brownfield |
|-----------|-----------|-----------|
| **Questions asked** | "What should we build?" | "What exists? What's changing?" |
| **Output scope** | Everything generated from scratch | Only delta/overlay generated |
| **Existing files** | None (or ignored) | Preserved, never modified |
| **Conventions** | Defined by architecture | Detected from existing code |
| **Governance** | Clean enforcement from day one | Baseline + enforce-forward |
| **Risk profile** | Design risk (wrong decisions) | Integration risk (breaking what works) |
| **Steering files** | Reference idealized architecture | Reference actual folder structure |

---

## The Gray Areas

### "We have some code but it's small/experimental"

**Ask:** "Would I lose anything valuable if I started over?"
- Yes → Brownfield (preserve it)
- No → Greenfield (start fresh, it's faster)

### "We have architecture docs but no code yet"

**This is greenfield.** Architecture docs are INPUT, not existing system. Use them as structured input to AI-ADLC or AI-DWG.

### "We're rewriting from scratch but the old system still runs"

**Greenfield for the new system.** The old system is reference material, not something to preserve. You might read it for requirements (adaptive intake), but you're not overlaying governance onto it.

### "We're splitting a monolith into services"

**Brownfield.** The monolith exists, has conventions, has tests. You're extending the system's architecture while preserving its codebase (until migration is complete).

### "We're adding a new microservice to an existing platform"

**Hybrid:** Brownfield for governance (overlay onto existing platform governance). Greenfield for the new service itself (fresh architecture for that container).

---

## The Brownfield Signal Through the Chain

When brownfield is selected at AI-PILC, it propagates:

```
AI-PILC: Project Type = "Brownfield Extension"
    → pilc-state.md carries the signal
    → AI-ADLC: Input Mode = "Brownfield" (design the delta)
    → AI-DWG: Mode 3 (overlay, don't generate structure)
    → AI-GCE: Baseline pattern (enforce forward, not backward)
    → AI-TGE: Brownfield assessment (map existing tests)
```

Every downstream package adapts automatically. You declare "brownfield" once; the whole chain adjusts.

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Greenfield mode on existing codebase | AI-DWG generates folder structure that conflicts with existing | Use Mode 3 (Brownfield Overlay) |
| Brownfield mode on truly new project | Unnecessary scanning, questions about "what exists" (nothing does) | Use Mode 1 (Full Generation) |
| Not declaring brownfield at PILC | Downstream packages don't adapt; governance doesn't baseline | Set brownfield signal early |
| Treating "rewrite" as brownfield | Preserves patterns from the old system that you're trying to escape | Use greenfield — the old system is reference, not constraint |

---

## Related Documents

| Document | Location |
|----------|----------|
| Pattern: Non-Destructive Reconciliation | `knowledge_docs/PATTERN_NON_DESTRUCTIVE_RECONCILIATION.md` |
| Pattern: Adaptive Intake | `knowledge_docs/PATTERN_ADAPTIVE_INTAKE.md` |
| How DWG Brownfield Detection Works | `knowledge_docs/HOW_DWG_BROWNFIELD_DETECTION_WORKS.md` |
| How to Retrofit Governance on Existing Code | `knowledge_docs/HOW_TO_RETROFIT_GOVERNANCE_ON_EXISTING_CODE.md` |
| Why Brownfield Awareness Matters | `knowledge_docs/WHY_BROWNFIELD_AWARENESS_MATTERS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
