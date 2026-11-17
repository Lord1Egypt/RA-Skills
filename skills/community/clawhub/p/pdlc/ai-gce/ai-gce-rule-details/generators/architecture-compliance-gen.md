<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Architecture Compliance — Derivation Logic

## Purpose

Derives architecture compliance rules from `workspace-rules.md` and `architecture-principles.md`. These are the "golden rules" — the non-negotiable principles every piece of code must respect.

---

## MANDATORY: Stage Sub-Role — Systems Engineer

During THIS activity, ALSO adopt the mindset of a **Systems Engineer**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in structural invariants: architecture rules define what MUST be true regardless of which module or feature is being built
- Evaluate each principle for mechanical enforceability — can a hook verify this without subjective judgment?
- Consider system-wide impact: one architecture violation can cascade into multiple downstream failures
- Derive rules at the right abstraction level — too specific and they break on edge cases, too vague and they're uncheckable
- Map every rule to observable file-level evidence (imports, folder placement, class structure)

### Anti-Patterns for This Activity
- Do NOT generate architecture rules from missing steering files — architecture is 100% project-specific
- Do NOT conflate style preferences with structural principles (naming is NC-*, not ARCH-*)
- Do NOT create rules that require runtime behavior observation — hooks check static artifacts

### Quality Check
A good output from this activity sounds like:
- "ARCH-03: No direct class references across module boundaries. Verification: import statements in module X reference only its own namespace or shared kernel. File pattern: `src/modules/*/application/**/*.ts`."
- "Architecture-principles.md has 6 numbered principles → 6 ARCH-P* rules generated, all Critical severity, all Foundation+ phase."

---

## Source Steering Files

| File | What to Extract |
|------|----------------|
| `workspace-rules.md` | Architecture identity, golden rules, DON'T rules, system-level constraints |
| `architecture-principles.md` | Numbered principles (P1-Pn) with statements and rationale |

---

## Extraction → Rule Transformation

### From `workspace-rules.md`

Every MUST/MUST NOT/NEVER/ALWAYS statement → one rule:

| Steering Content | Generated Rule |
|-----------------|---------------|
| "All modules MUST follow clean architecture layers" | ARCH-01: Clean architecture layers enforced per module |
| "NEVER bypass the domain layer for database access" | ARCH-02: No direct DB access from presentation/application |
| "All cross-module communication via events only" | ARCH-03: No direct class references across module boundaries |

### From `architecture-principles.md`

Every numbered principle → one compliance rule:

| Principle | Generated Rule |
|-----------|---------------|
| P1: "Single Responsibility — each module owns one bounded context" | ARCH-P01: Module ↔ bounded context 1:1 mapping enforced |
| P2: "Contract-First — API contracts defined before implementation" | ARCH-P02: OpenAPI spec precedes controller code |
| P3: "Fail-Safe — all failures handled gracefully with Result pattern" | ARCH-P03: No unhandled exceptions in application layer |

---

## Rule Format (Generated Output)

```markdown
### ARCH-{NN}: {Rule Title}

| Field | Value |
|-------|-------|
| **Severity** | 🔴 Critical |
| **Tier** | 1 |
| **Phase** | Foundation+ |
| **Derived From** | rules/architecture-principles.md → P{n}: "{principle statement}" |

**Requirement:** {One sentence — what MUST be true}

**Verification:**
- [ ] {Specific check 1}
- [ ] {Specific check 2}

**File Patterns:** `{technology-specific glob}` (if applicable)

**Anti-Pattern:** {What violation looks like — concrete example}
```

---

## Severity Assignment for Architecture Rules

| Principle Type | Default Severity | Override Condition |
|---------------|:----------------:|-------------------|
| Structural (layers, boundaries, isolation) | 🔴 Critical | — |
| Communication patterns (events, APIs) | 🔴 Critical | — |
| Technology constraints (what NOT to use) | 🟠 High | Upgrade to 🔴 if security-related |
| Quality attributes (performance, scalability) | 🟠 High | — |
| Style preferences (naming within arch) | 🟡 Medium | — |

---

## Hook Mapping

Architecture compliance rules are enforced by:

| Hook | When | What It Checks |
|------|------|----------------|
| `post-task-governance.json` | After task completion | All ARCH-* rules against the completed work |
| `domain-layer-purity.json` | agentStop | ARCH rules related to layer isolation |
| `module-boundary-check.json` | agentStop | ARCH rules related to cross-module communication |

---

## Built-in Baseline Integration

Architecture rules are 100% steering-derived — NO built-in baseline for this category. If `architecture-principles.md` is empty or missing, NO ARCH-* rules are generated (architecture is entirely project-specific).

Exception: The built-in baseline rule "spec before code" is classified under GOV-SESSION, not ARCH.
