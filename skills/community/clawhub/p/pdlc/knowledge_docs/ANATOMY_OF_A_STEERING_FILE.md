# Anatomy of a Steering File

**Purpose:** Field-by-field breakdown of AI-* Family steering files — front-matter schema, rule language conventions, structure patterns, and how steering files connect to hooks and governance.

**Derived from:** Pattern: Two-Source Model + Pattern: Conditional Generation + Pattern: Custom Preservation

---

## What a Steering File Is

A steering file is a markdown document in `.kiro/steering/` that provides rules, conventions, and constraints to AI sessions. It's the RUNTIME expression of architecture decisions — what the AI must follow when writing code in this workspace.

```markdown
---
generatedBy: AI-DWG
generatedVersion: 1.0.0
source: adlc-output/07_API_Architecture.md
generatedOn: 2026-06-12
ownership: hybrid
inclusion: always
---

# API Standards

## Context
These rules derive from the API Architecture decisions in the Architecture Package.
All endpoints in this project MUST follow these standards.

## Rules
1. Every endpoint MUST have a corresponding OpenAPI spec entry
2. API versioning MUST use header-based strategy (Accept-Version header)
3. Error responses MUST follow RFC 7807 (Problem Details) format
...

<!-- custom -->
## Team Additions
- Internal-only endpoints (prefixed /internal/) are exempt from versioning
<!-- /custom -->
```

---

## Front-Matter Fields

```yaml
---
generatedBy: AI-DWG           # Which package generated this file
generatedVersion: 1.0.0       # Package version at generation time
source: adlc-output/07_API_Architecture.md  # Which upstream doc produced this
generatedOn: 2026-06-12       # When generated (ISO date)
ownership: hybrid              # generated | hybrid | user
inclusion: always              # always | fileMatch | manual
fileMatchPattern: "src/api/**" # Only for fileMatch inclusion
---
```

| Field | Required | Purpose |
|-------|:--------:|---------|
| `generatedBy` | ✅ (generated files) | Provenance: who created this |
| `generatedVersion` | ✅ (generated files) | Version tracking for updates |
| `source` | ✅ (generated files) | Traceability: which AP doc justified this |
| `generatedOn` | ✅ (generated files) | When last generated/re-derived |
| `ownership` | ✅ | Controls re-derivation behavior |
| `inclusion` | ⚪ | Loading mode (defaults to `always` if absent) |
| `fileMatchPattern` | Conditional | Required only when `inclusion: fileMatch` |

**Note:** User-created steering files don't need provenance fields (no `generatedBy`, etc.) — they just need `inclusion` if not always-loaded.

---

## Body Structure

### Section 1: Context (Why This File Exists)

```markdown
## Context
These rules derive from {AP document name} and enforce {what domain}.
They apply to {scope — all code / specific modules / specific file types}.
```

**Purpose:** When a developer sees a rule violation, they can read the context to understand WHY the rule exists without tracing back to the AP.

### Section 2: Rules (The Enforceable Constraints)

```markdown
## Rules
1. {Subject} MUST {action}
2. {Subject} MUST NOT {action}
3. {Subject} NEVER {action}
4. All {category} MUST {standard}
```

**Rule language (AI-DWG Rule 1: Prescriptive Output):**
- ✅ `MUST` / `MUST NOT` / `NEVER` — binary, enforceable
- ❌ `should` / `consider` / `prefer` — ambiguous, not enforceable

Every rule is binary: pass or fail. No judgment calls. If a rule requires judgment, it's not specific enough.

### Section 3: Examples (Optional but Valuable)

```markdown
## Examples

### ✅ Compliant
```typescript
// Correct: endpoint has OpenAPI spec entry
router.get('/users', handler); // spec: paths./users.get
```

### ❌ Non-Compliant
```typescript
// Wrong: no OpenAPI spec entry exists for this endpoint
router.get('/admin/metrics', handler); // NO SPEC ENTRY
```
```

**When to include examples:** When a rule might be ambiguous or when the "wrong" way is a common pattern developers might not recognize as wrong.

### Section 4: Custom Block (Team Additions)

```markdown
<!-- custom -->
## Team-Specific Rules
{Team additions that survive re-derivation}
<!-- /custom -->
```

Only present in `ownership: hybrid` files. Everything between markers is sacred.

---

## Inclusion Modes Explained

### `always` (Default)

```yaml
inclusion: always
```

Loaded into EVERY AI session. Use for rules that apply regardless of what file is being edited.

**Examples:** `workspace-rules.md`, `tech-stack.md`, `security-rules.md`, `naming-conventions.md`

### `fileMatch`

```yaml
inclusion: fileMatch
fileMatchPattern: "src/frontend/**"
```

Loaded ONLY when a file matching the pattern is open. Saves context budget.

**Examples:** `frontend-standards.md` (only when editing frontend), `ai-adlc-rules.md` (only when working in AI-ADLC package)

### `manual`

```yaml
inclusion: manual
```

Loaded ONLY when user invokes via `#filename` in chat. For heavy reference material.

**Examples:** `persona-cto-architect.md`, `package-builder-rules.md`

---

## How Steering Connects to Governance

```
STEERING FILE (source of truth for rules)
    │
    ├── AI-GCE reads → derives RULES (.governance/rules/*)
    │                 → derives HOOKS (.kiro/hooks/*)
    │                 → derives AGENTS (.kiro/agents/*)
    │
    └── AI session reads → follows rules directly (before hooks even fire)
```

**Dual enforcement:** Steering files work in TWO ways:
1. **Direct** — the AI reads them at session start and follows the rules
2. **Derived** — AI-GCE generates automated enforcement (hooks) from them

Even without AI-GCE, steering files provide governance via the direct read mechanism. AI-GCE adds AUTOMATED enforcement on top.

---

## Steering File Lifecycle

```
1. AI-DWG GENERATES steering from Architecture Package
   └── ownership: generated or hybrid

2. TEAM CUSTOMIZES (if hybrid)
   └── Adds content inside <!-- custom --> blocks

3. ARCHITECTURE CHANGES
   └── AI-DWG Mode 2 reconciles → updates generated sections
   └── Custom sections preserved

4. AI-GCE READS steering
   └── Derives rules + hooks → automated enforcement

5. AI-GCE RE-DERIVES (when steering changes)
   └── Updates rules/hooks to match current steering
```

---

## Common Steering Files (Generated by AI-DWG)

| File | Always/Conditional | Rules About |
|------|:------------------:|-------------|
| `workspace-rules.md` | Always | Project-wide context and conventions |
| `tech-stack.md` | Always | Technology choices and constraints |
| `api-standards.md` | Always | API design, versioning, error handling |
| `security-rules.md` | Always | Security patterns and requirements |
| `module-structure.md` | Always | Module boundaries and dependencies |
| `naming-conventions.md` | Always | File, variable, class, API naming |
| `testing-strategy.md` | Always | Test types, coverage, requirements |
| `session-governance.md` | Always | Session discipline, spec-first |
| `error-handling.md` | Always | Error propagation patterns |
| `logging-observability.md` | Always | Logging and monitoring standards |
| `role-isolation.md` | Always | Team topology and ownership |
| `project-governance.md` | Always | PR process, review requirements |
| `multi-tenancy.md` | Conditional | Tenant isolation (if AP includes tenancy) |
| `event-sourcing.md` | Conditional | Event patterns (if extension active) |
| `resilience-standards.md` | Conditional | Fault tolerance (if ≥3 integrations or extension) |
| `feature-flags.md` | Conditional | Flag lifecycle (if extension active) |
| `frontend-standards.md` | Conditional | UI patterns (if frontend containers exist) |
| `microservices.md` | Conditional | Service mesh rules (if extension active) |

---

## Writing Effective Steering Rules

| Principle | Good | Bad |
|-----------|------|-----|
| Binary | "MUST use kebab-case" | "Should prefer kebab-case" |
| Specific | "Files in src/api/ MUST have .controller.ts suffix" | "Use appropriate naming" |
| Verifiable | "Every endpoint MUST have OpenAPI entry" | "APIs should be documented" |
| Scoped | "Integration tests MUST mock external services" | "Tests should be reliable" |
| Actionable | "Error responses MUST include error_code field" | "Handle errors properly" |

---

## Related Documents

| Document | Location |
|----------|----------|
| How Steering File Loading Works | `knowledge_docs/HOW_STEERING_FILE_LOADING_WORKS.md` |
| How DWG Generation Engine Works | `knowledge_docs/HOW_DWG_GENERATION_ENGINE_WORKS.md` |
| How GCE Derivation Pipeline Works | `knowledge_docs/HOW_GCE_DERIVATION_PIPELINE_WORKS.md` |
| How Provenance Tracking Works | `knowledge_docs/HOW_PROVENANCE_TRACKING_WORKS.md` |
| Pattern: Custom Preservation | `knowledge_docs/PATTERN_CUSTOM_PRESERVATION.md` |
| Pattern: Conditional Generation | `knowledge_docs/PATTERN_CONDITIONAL_GENERATION.md` |
| When to Customize vs Use Steering | `knowledge_docs/WHEN_TO_CUSTOMIZE_VS_USE_STEERING.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
