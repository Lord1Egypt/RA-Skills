# Full Implementation (End-to-End)

Default operation for implementing an RFC. Orchestrates: Spec Analysis → Impl Guide → Coding Plan → Coding + Tests.

```
Spec Analysis → Impl Guide → Coding Plan → Coding + Tests
                    ▲              ▲
              [confirm gate] [confirm gate]
```

## Prerequisites

- RFC exists (Draft or Frozen)
- Target module specified
- Language/framework known or detectable

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| RFC Document | Yes | Path to source RFC |
| Target Module | Yes | Module/crate/package name |
| Language | Yes | Target language |
| Framework | No | If applicable |
| Auto Mode | No | Skip gates (default: false) |

## Sub-Workflow

### Step 1: Spec Analysis
Extract from RFC: core concepts, requirements (MUST/SHALL), constraints, interfaces, data structures, behaviors, dependencies. Create requirements checklist.

### Step 2: Impl Guide Design
Create implementation guide (follow `create-guide.md`). Output: module structure, type definitions, interface signatures, error handling, testing strategy.

**Confirmation Gate**: Present summary (module structure, key types, design decisions). Skip if auto-mode or "no confirmations".

### Step 3: Coding Plan
Break into ordered tasks: one file per task, dependency order, test pairing. Use `assets/coding-plan-template.md`.

**Confirmation Gate**: Present plan. Skip if auto-mode or trivial scope (single file, <50 lines).

### Step 4: Coding
Execute plan: follow guide as law, no speculative design, use language idioms, integrate with existing code, write unit + integration tests, verify build.

If guide is incomplete: document gap, suggest update—don't invent behavior.

## Output

- Implementation guide (`IG-NNN-<name>.md`)
- Source code
- Unit + integration tests
