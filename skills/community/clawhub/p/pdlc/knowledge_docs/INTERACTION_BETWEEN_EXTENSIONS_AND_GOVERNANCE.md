# Interaction Between Extensions and Governance

**Purpose:** Maps how activating an AI-ADLC extension (DDD, Microservices, etc.) affects what AI-DWG generates and what AI-GCE enforces — the full cascade from opt-in to enforcement.

---

## The Interaction Chain

```
EXTENSION ACTIVATED (AI-ADLC Stage X)
    │
    ├── adlc-state.md updated: Enabled Extensions: [DDD Tactical]
    │
    ├── AP enriched with extension-specific artifacts
    │       │
    │       └── AI-DWG reads enabled extensions
    │               │
    │               ├── CONDITIONAL GENERATION triggered (new steering files)
    │               │
    │               └── EXISTING steering ENRICHED (rules added to existing files)
    │                       │
    │                       └── AI-GCE derives ADDITIONAL rules + hooks
    │                               │
    │                               └── ENFORCEMENT includes extension constraints
    │
    └── NET EFFECT: Extension adds steering → steering adds rules → rules add enforcement
```

---

## Extension → Steering → Rules Mapping

| Extension | Steering Generated/Enriched | Rules Derived | Hooks Added |
|-----------|---------------------------|:-------------:|:-----------:|
| **DDD Tactical** | `module-structure.md` (enriched: bounded context rules), `ddd-patterns.md` (new) | DDD-01..05 (aggregate boundaries, domain events, anti-corruption layer) | `domain-layer-purity.json`, `aggregate-boundary-check.json` |
| **Microservices** | `microservices.md` (new), `resilience-standards.md` (forced generation) | MICRO-01..05 (service independence, distributed tracing, contract testing) | `service-boundary-check.json`, `distributed-trace-check.json` |
| **BFF Pattern** | `api-standards.md` (enriched: BFF routing rules), `bff-patterns.md` (new) | BFF-01..03 (per-client APIs, no backend logic in BFF) | `bff-layer-check.json` |
| **Event Sourcing / CQRS** | `event-sourcing.md` (new), `data-standards.md` (enriched: event immutability) | ES-01..04 (event immutability, projection consistency, command/query separation) | `event-immutability-check.json`, `cqrs-separation-check.json` |
| **Resilience Patterns** | `resilience-standards.md` (generated or enriched) | RES-01..05 (circuit breakers, bulkheads, retry policies, fallback required) | `resilience-pattern-check.json` |
| **Feature Flags** | `feature-flags.md` (new) | FF-01..04 (flag lifecycle, no stale flags, testing with flags) | `flag-hygiene-check.json` |

---

## Conditional Generation Overrides

Extensions can FORCE generation of steering files that would otherwise be conditional:

| Normal Trigger | Extension Override |
|---------------|-------------------|
| `resilience-standards.md` generated if ≥3 integrations | Microservices extension → ALWAYS generate (regardless of integration count) |
| `module-structure.md` includes basic boundaries | DDD extension → enriches with bounded context rules (deeper boundaries) |
| Performance hooks at Tier 3 only | Resilience extension → resilience hooks at Tier 2 (earlier activation) |

---

## Impact on Governance Tiers

Extensions don't change WHICH tier a rule belongs to, but they ADD rules within tiers:

| Without Extensions | With DDD + Resilience |
|:--:|:--:|
| Tier 1: 5-8 rules | Tier 1: 5-8 rules (unchanged) |
| Tier 2: 15-20 rules | Tier 2: 20-28 rules (+DDD + Resilience rules) |
| Tier 3: 30-35 rules | Tier 3: 38-45 rules (+extension-specific advanced rules) |

**Key:** Extensions add rules to Tier 2 and 3 (not Tier 1). Extension rules require architecture maturity to enforce — they don't belong in the foundational tier.

---

## Activating an Extension Mid-Project

If an extension is activated AFTER AI-DWG already generated the workspace:

```
1. AI-ADLC: extension activated, adlc-state.md updated

2. AI-DWG Mode 4 (Extension Enrichment):
   ├── Reads updated adlc-state.md → sees new extension
   ├── Generates new conditional steering files
   ├── Enriches existing steering files (adds extension rules)
   └── Signals AI-GCE: steering-files-updated

3. AI-GCE re-derivation:
   ├── Reads new/enriched steering
   ├── Derives new extension rules
   ├── Generates new hooks
   └── Activates at appropriate tier

4. Team experiences new enforcement
   (grace period recommended for new extension rules)
```

---

## Deactivating an Extension

If an extension is removed after being active:

```
1. AI-ADLC: extension deactivated, moved to "Declined Extensions"

2. AI-DWG reconciliation:
   ├── Conditional steering files for that extension → flagged obsolete
   ├── Enrichment content in shared steering → proposed for removal
   └── Signal to AI-GCE

3. AI-GCE re-derivation:
   ├── Rules derived from extension steering → deprecated
   ├── Hooks for extension → stop firing
   └── Score recalculated (fewer rules = different denominator)

4. Human confirms removal of obsolete steering/rules
```

---

## Multiple Extensions Composing

When multiple extensions are active simultaneously:

| Composition | Effect |
|-------------|--------|
| DDD + Microservices | Bounded contexts map to services; both boundary types enforced |
| Microservices + Resilience | Service communication rules + fault tolerance rules (natural pair) |
| Event Sourcing + DDD | Domain events as the primary data model (deep synergy) |
| Feature Flags + any | Flag lifecycle rules layer on top of any architecture (purely additive) |

**No conflicts by design:** Extensions use separate rule namespaces (DDD-*, MICRO-*, RES-*, ES-*, BFF-*, FF-*). They compose additively without contradiction.

---

## Related Documents

| Document | Location |
|----------|----------|
| How ADLC Extensions Work | `knowledge_docs/HOW_ADLC_EXTENSIONS_WORK.md` |
| How to Choose Architecture Extensions | `knowledge_docs/HOW_TO_CHOOSE_ARCHITECTURE_EXTENSIONS.md` |
| How Hook Generation Works | `knowledge_docs/HOW_HOOK_GENERATION_WORKS.md` |
| Pattern: Conditional Generation | `knowledge_docs/PATTERN_CONDITIONAL_GENERATION.md` |
| Pattern: Downstream Signaling | `knowledge_docs/PATTERN_DOWNSTREAM_SIGNALING.md` |
| How to Handle Architecture Changes Mid-Project | `knowledge_docs/HOW_TO_HANDLE_ARCHITECTURE_CHANGES_MID_PROJECT.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
