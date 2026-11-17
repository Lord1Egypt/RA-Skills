# AI-ADLC Extensions — How They Work

## Overview

Extensions are optional rule sets that add specialized architectural pattern guidance on top of the core AI-ADLC workflow. They activate via user opt-in during the workflow — only when your system needs a specific pattern.

---

## The Pattern

Each extension has **two files**:

```
extensions/{name}/
├── {name}.opt-in.md       ← Lightweight prompt (always scanned at workflow start)
└── {name}.md              ← Full rules (loaded ONLY if user opts in)
```

| File | Size | Loaded When | Purpose |
|------|:----:|-------------|---------|
| `*.opt-in.md` | Small | Always (at workflow start) | Presents the opt-in question to the user |
| `*.md` (rules) | Large | Only if user says "Yes" | Provides detailed design rules, verification criteria, and templates |

---

## The Flow

```
Workflow Start
    │
    ▼
[Scan extensions/ folder — load ONLY *.opt-in.md files]
    │
    ▼ (During relevant stage — Stage 5, 6, or 12)
    │
[Present opt-in questions to user]
    │
    ├── User says "Yes" ──► Load {name}.md (full rules)
    │                         └──► Enforce in subsequent stages
    │                         └──► Verify compliance at stage completion
    │
    └── User says "No"  ──► Never load full rules
                              └──► Zero overhead; workflow proceeds normally
```

---

## Example Walkthrough: DDD Tactical Patterns

**Step 1 — Workflow Start:**
AI scans `extensions/` directory. Finds `ddd-tactical/ddd-tactical.opt-in.md`. Reads it (lightweight — just a question prompt and applicability criteria).

**Step 2 — During Stage 12 (Component Design):**
The workflow presents the opt-in question:

> "Would you like to apply DDD Tactical Patterns?
> This adds: Aggregate design rules, Domain Events catalog, Anti-Corruption Layers, Value Objects.
> (a) Yes (b) No"

**Step 3a — User says Yes:**
- AI loads `ddd-tactical/ddd-tactical.md` (the full rules file)
- Those rules become **enforced constraints** for the current and remaining stages
- Example rule: "Every aggregate must define its consistency boundary explicitly"
- At stage completion, the AI verifies compliance and reports findings
- Non-compliance is a blocking finding — stage cannot complete until resolved

**Step 3b — User says No:**
- `ddd-tactical.md` is NEVER loaded into context
- No context/token budget consumed
- Workflow proceeds with standard component design from core rules
- No enforcement, no compliance check for DDD patterns

---

## Why This Design?

| Benefit | Explanation |
|---------|-------------|
| **Context-efficient** | Only load heavy rule files when actually needed — saves AI context budget |
| **Non-intrusive** | Core workflow works perfectly without any extensions activated |
| **User-controlled** | User decides which advanced patterns to apply — never forced |
| **Additive** | Extensions ADD rules on top of core workflow — never replace or conflict with core |
| **Blocking when active** | Once opted in, extension rules are hard constraints — not optional suggestions |
| **Composable** | Multiple extensions can be active simultaneously (DDD + Microservices + Resilience) |

---

## When Are Opt-In Questions Presented?

Extensions are presented at the stage where their pattern becomes relevant:

| Extension | Presented During | Why |
|-----------|-----------------|-----|
| Microservices | Stage 5 (Container Design) | Service decomposition is decided here |
| BFF Pattern | Stage 5 (Container Design) | BFF is a container-level decision |
| Resilience Patterns | Stage 5 or 11 (Integration/Infrastructure) | Resilience applies to distributed communication |
| DDD Tactical | Stage 12 (Component Design) | DDD patterns apply to internal module structure |
| Event Sourcing / CQRS | Stage 9 (Data Architecture) | Fundamentally changes data model approach |
| Feature Flags | Stage 6 (Technology Stack) or Stage 12 | Architectural decision about delivery mechanism |

---

## What a Full Rules File Contains

When activated, the rules file provides:

1. **Activation point** — Which stage(s) the rules apply to
2. **Rules** — Numbered, specific, verifiable constraints (e.g., "DDD-01: Aggregate Boundary Definition")
3. **Verification criteria** — Checklist that must pass before stage can complete
4. **ADR triggers** — Which decisions within the extension produce ADRs
5. **Templates** — Any additional document templates the extension requires
6. **Anti-patterns** — What NOT to do when applying this pattern

### Example Rule Structure:

```markdown
### Rule {PREFIX}-{NN}: {Title}

**Statement:** {What must be true — clear, testable}

**Verification:**
- [ ] {Check 1}
- [ ] {Check 2}

**Anti-Pattern:** {What to avoid}

**ADR Trigger:** {Yes/No — does this rule generate an ADR?}
```

---

## Enforcement Model

Once an extension is activated:

| Behavior | Description |
|----------|-------------|
| **Rules are blocking** | Stage cannot complete if extension rules are violated |
| **Compliance summary** | At each stage completion, extension compliance is reported |
| **N/A is acceptable** | If a rule doesn't apply to the current stage, mark as N/A (not a violation) |
| **Non-compliance = fix first** | If a rule IS applicable and not met → must be resolved before proceeding |
| **Logged in state** | Enabled extensions are tracked in `adlc-state.md` |

---

## Multiple Extensions Active

Extensions compose — they don't conflict:

```
Active Extensions:
  ✅ DDD Tactical (Stage 12 rules)
  ✅ Microservices (Stage 5, 11 rules)
  ✅ Resilience Patterns (Stage 11 rules)

At Stage 11 completion:
  - Core workflow checks: ✅ All pass
  - Microservices extension checks: ✅ Service mesh defined, distributed tracing designed
  - Resilience extension checks: ✅ Circuit breakers on all inter-service calls
  - DDD extension checks: N/A (applies to Stage 12, not 11)
```

---

## Creating Your Own Extension

To create a custom extension:

1. Create folder: `extensions/{your-pattern-name}/`
2. Create opt-in file: `{your-pattern-name}.opt-in.md`
   - Include: when it applies, what it adds, the opt-in question
3. Create rules file: `{your-pattern-name}.md`
   - Include: activation point, numbered rules, verification criteria, anti-patterns
4. Keep it general — no project-specific content
5. Rules should be verifiable (yes/no pass criteria)

### Naming Convention

- Folder name: `kebab-case` (e.g., `event-sourcing-cqrs`)
- Opt-in file: `{folder-name}.opt-in.md`
- Rules file: `{folder-name}.md`
- Rule IDs: `{PREFIX}-{NN}` (e.g., `DDD-01`, `MS-03`, `RES-05`)

---

## Extension Status (v1.1)

All six high-priority extensions are **complete and enforceable**:

| Extension | Rules File | Status |
|-----------|-----------|:------:|
| `ddd-tactical/` | `ddd-tactical.md` | ✅ Complete |
| `microservices/` | `microservices.md` | ✅ Complete |
| `bff-pattern/` | `bff-pattern.md` | ✅ Complete |
| `event-sourcing-cqrs/` | `event-sourcing-cqrs.md` | ✅ Complete |
| `resilience-patterns/` | `resilience-patterns.md` | ✅ Complete |
| `feature-flags/` | `feature-flags.md` | ✅ Complete |

**Behavior when user opts in:**
- Full rules file is loaded
- Structured enforcement is active (numbered rules, checklists, blocking verification)
- ADR triggers produce formal Architecture Decision Records
- Stage cannot complete if extension rules are violated

---

## FAQ

| Question | Answer |
|----------|--------|
| Are extensions loaded automatically? | No — only opt-in prompts are scanned; full rules require explicit "Yes" |
| What if I say yes but later want to disable? | Tell the AI: "Disable {extension} extension" — it updates state and stops enforcing |
| Can I activate an extension mid-workflow? | Yes — say "Enable {extension}" at any point; rules apply from that point forward |
| Do extensions add stages? | No — they add RULES to existing stages, not new stages |
| Can extensions conflict with each other? | Designed not to. If conflict detected, AI flags it for user resolution |
| Can I use AI-ADLC without any extensions? | Yes — core workflow is 100% functional standalone |
| Who maintains extensions? | Community-contributed or self-authored; follow the structure above |
