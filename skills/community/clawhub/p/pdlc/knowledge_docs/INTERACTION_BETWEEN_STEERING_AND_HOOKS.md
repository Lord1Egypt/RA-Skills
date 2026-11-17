# Interaction Between Steering Files and Hooks

**Purpose:** Maps the precise relationship between steering files and governance hooks — which steering produces which hooks, how changes in one affect the other, and how they work together at runtime.

---

## The Relationship

```
STEERING FILE (the source of truth)
    │
    ├── AI session READS it directly (advisory enforcement)
    │
    └── AI-GCE DERIVES hooks from it (automated enforcement)
            │
            └── HOOK fires on IDE events (blocking/advisory enforcement)
```

**Dual enforcement:** Steering works TWO ways simultaneously:
1. **Direct** — AI reads steering at session start, follows rules
2. **Derived** — AI-GCE generates hooks that enforce automatically

---

## Steering-to-Hook Mapping

| Steering File | Derived Hooks | Event Type |
|--------------|---------------|-----------|
| `naming-conventions.md` | `naming-enforcement.json` | fileCreated, fileEdited |
| `api-standards.md` | `api-contract-check.json`, `api-versioning-check.json` | fileEdited (routes/controllers) |
| `security-rules.md` | `secrets-detection.json`, `input-validation-check.json` | preToolUse (write) |
| `session-governance.md` | `session-discipline.json` | promptSubmit |
| `module-structure.md` | `module-boundary-check.json`, `dependency-direction.json` | fileEdited (source files) |
| `testing-strategy.md` | `test-companion-check.json` | fileCreated (source files) |
| `role-isolation.md` | `segregation-check.json` | preToolUse (shell — git push) |
| `project-governance.md` | `pre-pr-checklist.json` | preToolUse (shell — git push) |
| `logging-observability.md` | (no hook — advisory only via steering) | — |
| `error-handling.md` | (no hook — advisory only via steering) | — |

**Not all steering generates hooks.** Some steering is advisory-only (AI follows it when read, but no automated check fires). Hooks are generated only when enforcement is automatable and binary.

---

## How Changes Propagate

### Steering Edited → Hooks Updated

```
1. Developer edits .kiro/steering/api-standards.md
   (adds: "All responses MUST include request-id header")

2. AI-GCE re-derivation triggered (manual or signal-based)

3. AI-GCE reads updated api-standards.md

4. api-contract-check.json regenerated:
   - Prompt now includes new rule about request-id header
   - Hook fires on same events as before (no event change)

5. Next time a route file is edited:
   - Hook fires → AI checks for request-id header compliance
```

### Steering Deleted → Hooks Orphaned

```
1. multi-tenancy.md deleted (architecture no longer includes tenancy)

2. AI-GCE re-derivation runs

3. Hooks derived from multi-tenancy.md flagged as orphaned:
   - tenant-isolation-check.json → status: deprecated
   - Hook stops firing

4. Audit report shows: "1 orphaned hook (source removed)"

5. Human confirms removal → hook file deleted
```

### New Steering Added → New Hooks Created

```
1. Team creates .kiro/steering/performance-budgets.md (new file)

2. AI-GCE re-derivation triggered

3. New hooks derived:
   - bundle-size-check.json (fires on build output)
   - response-time-check.json (fires on API handler files)

4. New hooks assigned to Tier 3 (performance = advanced governance)

5. If team is at Tier 3 → hooks active immediately
   If team is at Tier 1-2 → hooks dormant until tier graduation
```

---

## Runtime Interaction

During a developer's session, steering and hooks interact:

```
Developer opens API route file
    │
    ├── Steering: AI reads api-standards.md (knows the rules contextually)
    │   └── AI's responses naturally follow API conventions
    │
    └── Hook: api-contract-check.json fires (fileEdited event)
        └── Hook prompt: "Verify this endpoint has OpenAPI spec entry"
            └── AI checks → either passes silently or warns developer
```

**Both fire independently.** Steering shapes the AI's DEFAULT behavior. Hooks add EXPLICIT verification on top. A well-steered AI might never trigger a hook violation (steering prevented it). Hooks catch what steering missed.

---

## When They Disagree

| Scenario | What Happens | Resolution |
|----------|-------------|-----------|
| Steering says "MUST use kebab-case" but hook checks PascalCase | Hook is derived incorrectly | Fix: re-derive hook from current steering |
| Steering updated but hook not re-derived | Hook enforces OLD rule | Fix: trigger re-derivation |
| Hook fires but steering doesn't mention the rule | Hook was manually created (not derived) | Acceptable — manual hooks complement derived ones |
| Custom block in steering contradicts generated hook | Custom steering takes precedence | Human-authored > generated (resolve conflict in next re-derivation) |

---

## Related Documents

| Document | Location |
|----------|----------|
| How Hook Generation Works | `knowledge_docs/HOW_HOOK_GENERATION_WORKS.md` |
| How Steering File Loading Works | `knowledge_docs/HOW_STEERING_FILE_LOADING_WORKS.md` |
| Anatomy of a Hook | `knowledge_docs/ANATOMY_OF_A_HOOK.md` |
| Anatomy of a Steering File | `knowledge_docs/ANATOMY_OF_A_STEERING_FILE.md` |
| When to Trigger Re-Derivation | `knowledge_docs/WHEN_TO_TRIGGER_REDERIVATION.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
