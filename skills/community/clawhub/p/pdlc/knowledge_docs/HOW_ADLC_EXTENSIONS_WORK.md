# How AI-ADLC Extensions Work

**Purpose:** Explains the opt-in extension system that lets AI-ADLC enforce specialized architectural patterns (DDD, Microservices, BFF, Event Sourcing, Resilience, Feature Flags) — how they load, activate, compose, and propagate downstream.

---

## What Extensions Are

Extensions are optional rule sets that add specialized architectural pattern guidance on top of AI-ADLC's core workflow. They activate only when the user opts in — and once active, their rules become hard, blocking constraints (not suggestions).

```
CORE WORKFLOW (covers 80% of all architectures)
├── 5 phases, 13 stages
├── Always active for every project
└── Produces complete AP without extensions
        │
        ▼  (user opts in during relevant stage)
EXTENSIONS (cover the 20% specialized patterns)
├── DDD Tactical Patterns
├── Microservices
├── BFF Pattern
├── Event Sourcing / CQRS
├── Resilience Patterns
└── Feature Flags

Each extension ADDS rules — never replaces or conflicts with core.
```

---

## The Two-File Pattern

Every extension uses exactly two files:

| File | Loaded When | Purpose |
|------|-------------|---------|
| `{name}.opt-in.md` | Always (scanned at workflow start) | Lightweight prompt — presents the opt-in question |
| `{name}.md` | Only if user says "Yes" | Full rules — numbered constraints, verification, ADR triggers |

**Why two files:** Context efficiency. The opt-in file is tiny (saves AI context budget). The full rules file is large (10-12 rules with verification criteria). Loading rules that aren't needed wastes tokens and creates noise.

---

## The Activation Flow

```
Workflow Start
    │
    ▼
Scan extensions/ folder → load ONLY *.opt-in.md files
    │
    ▼ (During the relevant stage)
    │
Present opt-in question:
"Would you like to apply {Pattern Name}?
 This adds: {list of what it enforces}
 (a) Yes  (b) No"
    │
    ├── YES → Load {name}.md (full rules)
    │         Rules become BLOCKING constraints
    │         Verification required at stage completion
    │         Extension tracked in adlc-state.md
    │
    └── NO  → Full rules NEVER loaded
              Zero context overhead
              Workflow proceeds with core rules only
```

---

## When Each Extension Is Presented

Extensions are presented at the stage where their pattern becomes architecturally relevant:

| Extension | Presented At | Why This Stage |
|-----------|-------------|----------------|
| Microservices | Stage 5 (Container Design) | Service decomposition is a container-level decision |
| BFF Pattern | Stage 5 (Container Design) | BFF is a container added to the system |
| Event Sourcing/CQRS | Stage 9 (Data Architecture) | Fundamentally changes data model approach |
| Resilience Patterns | Stage 11 (Integration/Infra) | Resilience applies to distributed communication |
| DDD Tactical | Stage 12 (Component Design) | DDD patterns apply to internal module structure |
| Feature Flags | Stage 6 or 12 (Tech Stack/Components) | Delivery mechanism decision |

---

## What a Full Rules File Contains

Once activated, the rules file provides:

1. **Activation point** — Which stages the rules apply to (primary + secondary)
2. **Rules** — 10-12 numbered, verifiable constraints (e.g., `DDD-01: Aggregate Boundary Definition`)
3. **Verification criteria** — Checkboxes that must pass before stage completes
4. **ADR triggers** — Which decisions produce formal ADRs
5. **Templates** — Document templates the extension requires
6. **Anti-patterns** — What NOT to do when applying this pattern

### Rule Format (Consistent Across All Extensions)

```markdown
### Rule {PREFIX}-{NN}: {Title}

**Statement:** {What must be true — binary, testable}

**Verification:**
- [ ] {Check 1}
- [ ] {Check 2}

**Anti-Pattern:** {What violation looks like}

**ADR Trigger:** {Condition that produces an ADR}
```

---

## Enforcement Model

| Behavior | Description |
|----------|-------------|
| Rules are blocking | Stage cannot complete if extension rules are violated |
| Compliance summary at stage end | Extension compliance reported alongside core compliance |
| N/A is acceptable | Rules that don't apply to the current stage are marked N/A |
| Non-compliance = fix first | Must be resolved before proceeding |
| Tracked in state file | `adlc-state.md` records which extensions are active |

---

## Composability (Multiple Extensions Active)

Extensions are designed to compose without conflict. Multiple can be active simultaneously:

```
Active: DDD Tactical + Microservices + Resilience

At Stage 11 (Integration):
  Core checks: ✅ All pass
  Microservices checks: ✅ Service mesh, distributed tracing
  Resilience checks: ✅ Circuit breakers on all inter-service calls
  DDD checks: N/A (applies at Stage 12)

At Stage 12 (Component Design):
  Core checks: ✅ Module decomposition complete
  DDD checks: ✅ Aggregates defined, domain events cataloged
  Microservices checks: N/A (already verified at Stage 11)
  Resilience checks: N/A (already verified at Stage 11)
```

---

## Downstream Propagation

Extensions activated in AI-ADLC affect the entire downstream chain:

### AI-DWG reads `adlc-state.md` → "Enabled Extensions" field

| Active Extension | AI-DWG Generates |
|-----------------|------------------|
| DDD Tactical | Enriches `domain-context.md`, `module-structure.md`, `naming-conventions.md` |
| Microservices | Forces `resilience-standards.md` + `observability-tracing.md` (regardless of normal triggers) |
| BFF Pattern | Forces `frontend-standards.md`; enriches `api-standards.md` |
| Event Sourcing/CQRS | Generates `event-sourcing.md` steering file |
| Resilience Patterns | Forces `resilience-standards.md` with full detail |
| Feature Flags | Generates `feature-flags.md` steering file |

### AI-GCE reads workspace → conditional steering files

Extensions that caused AI-DWG to generate conditional steering files are then read by AI-GCE, which derives specialized compliance rules and hooks for those patterns.

**The chain:** AI-ADLC extension active → AI-DWG generates conditional steering → AI-GCE derives enforcement rules/hooks.

---

## The Six Extensions (v1.1)

| Extension | Prefix | Rules | Primary Stage |
|-----------|:------:|:-----:|:-------------:|
| DDD Tactical | `DDD-` | 10-12 | Stage 12 |
| Microservices | `MS-` | 10-12 | Stage 5 |
| BFF Pattern | `BFF-` | 10-12 | Stage 5 |
| Event Sourcing/CQRS | `ES-` | 10-12 | Stage 9 |
| Resilience Patterns | `RES-` | 10-12 | Stage 11 |
| Feature Flags | `FF-` | 10-12 | Stage 6/12 |

All six are complete and enforceable as of AI-ADLC v1.1.

---

## Runtime Controls

| Action | How |
|--------|-----|
| Activate mid-workflow | Say "Enable {extension}" — rules apply from that point forward |
| Deactivate | Say "Disable {extension}" — state updated, enforcement stops |
| Check what's active | Read `adlc-state.md` → "Enabled Extensions" section |

---

## Related Documents

| Document | Location |
|----------|----------|
| Extensions README (source) | `ai-adlc/ai-adlc-rule-details/extensions/README.md` |
| Extension folders (6) | `ai-adlc/ai-adlc-rule-details/extensions/` |
| AI-DWG extension detection | `ai-dwg/ai-dwg-rules/core-generator.md` (§ Extension-Aware Reading) |
| AI-DWG enrichment mappings | `ai-dwg/ai-dwg-rule-details/mapping/extension-*.md` |

*Knowledge Document | Created: 2026-06-11 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
