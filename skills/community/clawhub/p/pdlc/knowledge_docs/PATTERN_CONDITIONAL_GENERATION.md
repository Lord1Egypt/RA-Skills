# Pattern: Conditional Generation

**Purpose:** Documents the reusable design pattern where output files are generated ONLY when the input justifies their existence — preventing bloat from unnecessary artifacts that no one reads.

---

## The Pattern

```
INPUT (Architecture Package, steering, config)
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  CONDITIONAL TRIGGER EVALUATION                                      │
│                                                                      │
│  For each potential output file:                                     │
│    IF trigger condition is met → GENERATE                            │
│    IF trigger condition is NOT met → SKIP (file never created)       │
└─────────────────────────────────────────────────────────────────────┘
        │
        ▼
OUTPUT (only files justified by input — no unnecessary artifacts)
```

**One sentence:** Generate a file only if the architecture demands it — if there's no multi-tenancy in the design, there's no multi-tenancy steering file in the output.

---

## Where It's Used

| Package | Conditional Output | Trigger Condition |
|---------|-------------------|-------------------|
| **AI-DWG** | `multi-tenancy.md` steering | AP contains multi-tenancy architecture |
| **AI-DWG** | `event-sourcing.md` steering | Event Sourcing extension is active in `adlc-state.md` |
| **AI-DWG** | `resilience-standards.md` steering | ≥3 external integrations OR Resilience extension active |
| **AI-DWG** | `feature-flags.md` steering | Feature Flags extension is active |
| **AI-DWG** | `frontend-standards.md` steering | AP contains frontend containers |
| **AI-DWG** | `microservices.md` steering | Microservices extension is active |
| **AI-GCE** | Performance budget hooks | Tier 3 active AND performance NFRs exist in AP |
| **AI-GCE** | Accessibility hooks | Tier 3 active AND frontend exists |
| **AI-TGE** | Contract test requirements | ≥2 services with explicit API contracts |
| **AI-ADLC** | Extension rule loading | User opts in during relevant stage |

---

## The Trigger Table Pattern

Every conditional output is documented in a trigger table:

```markdown
## Conditional Generation Table

| Output File | Trigger Condition | Source Check |
|------------|-------------------|-------------|
| `multi-tenancy.md` | AP contains "Multi-Tenancy" or "Tenant" | Scan AP §5 or §10 |
| `resilience-standards.md` | integration_count ≥ 3 OR Resilience extension | Count in AP §11 + check adlc-state |
| `event-sourcing.md` | Event Sourcing extension active | Check adlc-state.md → Enabled Extensions |
| `frontend-standards.md` | AP contains frontend container | Scan AP §3 containers |
```

This table is the contract — it defines exactly WHEN each file appears. No ambiguity.

---

## Why This Pattern Exists

**The problem it solves:** Without conditional generation, a workspace generator produces ALL possible files for ALL possible architectures. A simple 3-endpoint REST API gets multi-tenancy rules, event sourcing patterns, microservice governance, and feature flag policies — none of which apply.

**The anti-pattern it prevents:** Generating unnecessary files that:
- Confuse developers ("why do I have microservices rules for a monolith?")
- Waste AI context (steering files loaded into every session)
- Create false governance (rules enforcing patterns that don't exist in the architecture)
- Undermine trust ("this tool doesn't understand my project")

**The test:** "Is there a valid project where this file would be generated but never read?" If yes → make it conditional.

---

## Extension Overrides

Extensions can FORCE conditional generation regardless of normal triggers:

```
Normal trigger: resilience-standards.md generated IF ≥3 integrations
Extension override: Resilience extension active → ALWAYS generate resilience-standards.md
```

**Why:** An extension represents an explicit architectural commitment. If you activated Resilience Patterns, you want the steering even if you currently have only 2 integrations (you're designing for resilience proactively).

---

## Implementation Rules

1. **Every conditional file has exactly one trigger condition** — no ambiguous "maybe" generation.

2. **Triggers are evaluable from input** — they reference specific fields, counts, or patterns that can be checked programmatically.

3. **Skipped files leave no trace** — no empty placeholder, no "this section intentionally blank." If the trigger isn't met, the file doesn't exist.

4. **Triggers are documented in a table** — future maintainers can understand what causes each file to appear or not appear.

5. **Extension overrides are explicit** — documented as "extension X forces file Y regardless of normal trigger."

---

## Conditional Generation vs. Depth Levels

These are different mechanisms:

| Mechanism | Controls | Example |
|-----------|----------|---------|
| **Conditional generation** | WHETHER a file exists at all | No tenancy → no `multi-tenancy.md` |
| **Depth levels** | HOW DETAILED a file's content is | Minimal depth → shorter `api-standards.md` with fewer rules |

A file can be conditionally generated AND depth-adapted:
- Trigger met + Minimal depth → file exists with essential rules
- Trigger met + Comprehensive depth → file exists with detailed rules
- Trigger NOT met + any depth → file doesn't exist

---

## When to Apply This Pattern

Apply when:
- [ ] A package generates multiple output files
- [ ] Some outputs apply only to certain architectures/configurations
- [ ] Generating everything always would create noise or false enforcement
- [ ] The trigger condition is objectively evaluable (not judgment-based)

Don't apply when:
- The output is always needed regardless of input (core files, state files)
- The trigger would be too complex to evaluate reliably
- The file is small enough that its presence causes no harm

---

## Related Documents

| Document | Location |
|----------|----------|
| How DWG Generation Engine Works | `knowledge_docs/HOW_DWG_GENERATION_ENGINE_WORKS.md` |
| How ADLC Extensions Work | `knowledge_docs/HOW_ADLC_EXTENSIONS_WORK.md` |
| How Hook Generation Works | `knowledge_docs/HOW_HOOK_GENERATION_WORKS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
