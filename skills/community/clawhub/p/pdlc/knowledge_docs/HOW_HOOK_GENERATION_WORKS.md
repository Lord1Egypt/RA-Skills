# How Hook Generation Works

**Purpose:** Explains how AI-GCE reads steering files and generates automated enforcement hooks — the derivation logic, hook anatomy, event-to-rule mapping, and how hooks compose into a coherent governance layer.

---

## What Hook Generation Is

Hooks are the automated enforcement mechanism of AI-GCE. They fire on IDE events (file edits, pre-commit, PR submission, session start) and either remind the AI of a rule (askAgent) or run a validation command (runCommand). AI-GCE DERIVES hooks from steering files — it doesn't require manual hook authoring.

```
STEERING FILES (.kiro/steering/)
├── api-standards.md
├── naming-conventions.md
├── security-rules.md
└── session-governance.md
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  AI-GCE HOOK DERIVATION                                              │
│                                                                      │
│  For each steering file:                                             │
│  1. Extract enforceable rules (MUST/MUST NOT/NEVER)                  │
│  2. Determine trigger event (when should this fire?)                 │
│  3. Determine action (askAgent vs. runCommand)                       │
│  4. Generate hook JSON                                               │
└─────────────────────────────────────────────────────────────────────┘
        │
        ▼
.kiro/hooks/
├── api-contract-check.json
├── naming-enforcement.json
├── security-gate-check.json
└── session-discipline.json
```

---

## Hook Anatomy

Every generated hook follows the schema:

```json
{
  "name": "API Contract Compliance",
  "version": "1.0.0",
  "description": "Ensures new endpoints have corresponding OpenAPI spec entries",
  "when": {
    "type": "fileEdited",
    "patterns": ["src/**/*.controller.ts", "src/**/*.route.ts"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Verify this endpoint change has a corresponding OpenAPI spec entry in api-spec.yaml. If no spec exists for this endpoint, remind the developer to add one before committing."
  }
}
```

**Key fields:**
- `when.type` — the IDE event that triggers the hook
- `when.patterns` — file patterns that scope the trigger (for file events)
- `when.toolTypes` — tool categories that scope the trigger (for preToolUse/postToolUse)
- `then.type` — what happens when triggered (askAgent or runCommand)
- `then.prompt` / `then.command` — the action content

---

## Event-to-Rule Mapping

AI-GCE maps steering rules to the most appropriate trigger event:

| Steering Rule Type | Trigger Event | Rationale |
|-------------------|---------------|-----------|
| Naming conventions | `fileCreated`, `fileEdited` | Check names when files are created/modified |
| API contract requirements | `fileEdited` (on route/controller files) | Catch endpoint changes at edit time |
| Security patterns | `preToolUse` (write operations) | Intercept before code is written |
| Session governance | `promptSubmit` | Check every AI interaction for spec-first compliance |
| PR requirements | `preToolUse` (shell — git push) | Enforce before code leaves local |
| Module boundaries | `fileEdited` (on source files) | Catch import violations at edit time |
| Test requirements | `fileCreated` (on source files) | Remind about tests when new code is created |
| Architecture compliance | `postToolUse` (write operations) | Review after code is written |

---

## Derivation Rules (Steering → Hook)

### Rule 1: One Hook Per Enforcement Concern

Each hook addresses ONE concern. A steering file with 5 rules may produce 1-3 hooks (grouping related rules):

| Steering File | Rules | Hooks Generated |
|--------------|:-----:|:---------------:|
| `naming-conventions.md` | 8 rules | 1 hook (naming-enforcement) |
| `api-standards.md` | 12 rules | 2 hooks (contract-check + versioning-check) |
| `security-rules.md` | 10 rules | 3 hooks (secrets-scan + auth-check + input-validation) |
| `session-governance.md` | 5 rules | 1 hook (session-discipline) |
| `module-structure.md` | 6 rules | 2 hooks (boundary-check + dependency-direction) |

### Rule 2: Minimal-Friction Trigger Selection

AI-GCE selects the LEAST disruptive trigger that still catches violations early:

```
Preference order (most to least preferred):
1. postToolUse (review after action — non-blocking information)
2. fileEdited/fileCreated (catch at creation — immediate feedback)
3. preToolUse (intercept before action — blocking but early)
4. promptSubmit (check every interaction — most intrusive)
```

### Rule 3: Prompt Engineering for askAgent

Generated prompts follow a template:
```
[RULE]: {the specific rule being enforced}
[CONTEXT]: {what the developer was doing when this fired}
[CHECK]: {what to verify}
[IF VIOLATION]: {what to tell the developer}
[IF COMPLIANT]: {proceed silently — say nothing}
```

---

## Hook Categories (by Governance Domain)

| Category | Hooks | Tier |
|----------|:-----:|:----:|
| Session governance | 1-2 | Tier 1 |
| Naming enforcement | 1 | Tier 1 |
| Basic security (secrets, validation) | 1-2 | Tier 1 |
| Separation of duties | 1 | Tier 1 |
| Architecture boundaries | 2-3 | Tier 2 |
| API contract compliance | 1-2 | Tier 2 |
| PR governance | 1-2 | Tier 2 |
| Test requirements | 1-2 | Tier 2 |
| Performance budgets | 1 | Tier 3 |
| Accessibility checks | 1 | Tier 3 |
| Deployment governance | 1-2 | Tier 3 |

**Typical total:** 14-18 hooks across all three tiers.

---

## Tier-Aware Generation

AI-GCE generates hooks for ALL tiers but activates them progressively:

```json
{
  "name": "Performance Budget Check",
  "version": "1.0.0",
  "description": "Validates bundle size stays within budget",
  "tier": 3,
  "when": {
    "type": "postToolUse",
    "toolTypes": ["shell"]
  },
  "then": {
    "type": "runCommand",
    "command": "npm run check-bundle-size"
  }
}
```

Hooks at tiers above the current active tier are generated but dormant — activated when the team graduates.

---

## Hook Composition (Multiple Hooks on Same Event)

When multiple hooks trigger on the same event:

1. All applicable hooks fire (no short-circuit)
2. Each provides independent feedback
3. The AI aggregates findings into one response
4. Conflicting hook outputs → more specific hook wins (file-match scoped > global)

---

## Re-Derivation Impact on Hooks

When steering changes and AI-GCE re-derives:

| Hook Status | Behavior |
|-------------|----------|
| Generated, no modifications | Overwritten with new derivation |
| Generated, user added custom logic | Custom parts preserved (if `<!-- custom -->` marked) |
| Manually created (user-authored) | NEVER touched — AI-GCE only manages its own hooks |
| Obsolete (steering source removed) | Flagged for removal, not auto-deleted |

---

## Related Documents

| Document | Location |
|----------|----------|
| How GCE Derivation Pipeline Works | `knowledge_docs/HOW_GCE_DERIVATION_PIPELINE_WORKS.md` |
| How GCE Rederivation Works | `knowledge_docs/HOW_GCE_REDERIVATION_WORKS.md` |
| How Tiered Governance Works | `knowledge_docs/HOW_TIERED_GOVERNANCE_WORKS.md` |
| How Steering File Loading Works | `knowledge_docs/HOW_STEERING_FILE_LOADING_WORKS.md` |
| How to Adopt Governance on a Project | `knowledge_docs/HOW_TO_ADOPT_GOVERNANCE_ON_A_PROJECT.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
