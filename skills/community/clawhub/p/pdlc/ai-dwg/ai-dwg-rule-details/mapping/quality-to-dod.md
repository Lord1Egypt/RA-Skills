<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Quality Attributes → backlog/DEFINITION_OF_DONE.md + backlog/DEFINITION_OF_READY.md

## Purpose

Transforms quality attributes and testing strategy from the Architecture Vision into a Definition of Done document that defines when work is "complete" — covering code quality, testing, documentation, and review gates. Also produces the paired Definition of Ready that defines when a story is ready to enter a sprint.

**Output:**
- `{workspace-root}/backlog/DEFINITION_OF_DONE.md` — quality gate: when work is "done"
- `{workspace-root}/backlog/DEFINITION_OF_READY.md` — entry gate: when a story is ready for sprint

**Condition:**
- `DEFINITION_OF_DONE.md` — Generate IF POLC or ADLC present (quality attrs from either)
- `DEFINITION_OF_READY.md` — Generate IF POLC present (sprint entry is a product concern)

---

## MANDATORY: Stage Sub-Role — Workspace Architect

During THIS activity, ALSO adopt the mindset of a **Workspace Architect**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Write DoD items as binary checkboxes — each must be verifiable as yes/no, never subjective quality judgment
- Trace every DoD section back to a specific steering file — "follows coding-standards.md" not "writes good code"
- Ensure security items are non-negotiable regardless of task type — no PR skips security verification
- Think about conditional sections (Database, API) — not every task touches every layer; make applicability clear
- Consider DoD as the quality gate contract between AI-DLC v1 and human reviewers — it defines "done" for both

### Anti-Patterns for This Activity
- Do NOT write aspirational quality statements ("code should be clean") — write enforceable checks
- Do NOT make the DoD so long it gets ignored — keep it to verifiable, high-impact items
- Do NOT skip observability requirements — logging is not optional for any feature work

### Quality Check
A good output from this activity sounds like:
- "Testing section: Unit tests pass (100%), integration tests for new API endpoints, coverage does not decrease, edge cases tested (null, empty, boundary)."
- "Security section: No secrets in code (DATA-06), input validated (SEC-01), authorization checked (AUTHZ-05), sensitive data not logged (SENS rules)."

---

## Source

**From:** Architecture Vision — Quality Attributes (all priorities)
**Also from:** Testing Strategy (from AP), Security Architecture (security review requirements), Git Workflow (PR process)

---

## Target: DEFINITION_OF_DONE.md

### Structure

```markdown
<!-- AI-DWG generated | source: Architecture Vision (Quality Attributes) + multiple AP sources | date: {generation-date} -->

# Definition of Done

## When Is a Task "Done"?

A task (user story, bug fix, feature) is DONE when ALL of the following are met. No exceptions — "almost done" is not done.

---

## Code Quality

- [ ] Code follows coding-standards.md conventions
- [ ] Code follows module-structure.md boundaries (no boundary violations)
- [ ] Domain terminology matches domain-context.md (no invented terms)
- [ ] Error handling follows error-handling.md patterns
- [ ] No new lint warnings introduced
- [ ] No `TODO` or `FIXME` left without a linked ticket

---

## Testing

- [ ] Unit tests written for new/changed logic
- [ ] Unit tests pass (100% of suite)
- [ ] Integration tests written for new API endpoints or service interactions
- [ ] Integration tests pass
- [ ] Test coverage: {from AP — e.g., does not decrease / meets module target}
- [ ] Edge cases tested (null, empty, boundary values, error paths)

---

## Security

- [ ] No secrets in code (security-rules.md DATA-06)
- [ ] Input validation on all new inputs (security-rules.md SEC-01)
- [ ] Authorization checked for new endpoints (security-rules.md AUTHZ-05)
- [ ] Sensitive data not logged (observability-sensitive.md)
- [ ] Tenant scoping verified (if multi-tenant — multi-tenancy.md)

---

## Observability

- [ ] Logging added for significant operations (observability-logging.md required points)
- [ ] Log level appropriate (INFO for business events, ERROR for failures)
- [ ] No sensitive data in log statements
- [ ] Metrics incremented where applicable

---

## Database (if schema changes)

- [ ] Migration created and tested (database-rules.md DB-MIG-01)
- [ ] Migration is reversible OR explicitly documented as forward-only
- [ ] Schema follows naming conventions (database-rules.md DB-SCHEMA)
- [ ] Indexes added for new query patterns
- [ ] Tenant scoping on new tables (if multi-tenant)

---

## API (if endpoint changes)

- [ ] Follows api-standards.md conventions (URL, methods, response format)
- [ ] Error responses use standard format (api-standards.md API-ERR)
- [ ] OpenAPI documentation updated
- [ ] Pagination applied for list endpoints
- [ ] Rate limiting considered

---

## Documentation

- [ ] Code comments for complex logic (WHY, not WHAT)
- [ ] README updated if setup/commands changed
- [ ] API documentation (OpenAPI) updated for new/changed endpoints
- [ ] ADR created if architectural decision was made

---

## Review & Merge

- [ ] PR follows template (all checklist items checked)
- [ ] Required approvals received ({n} reviewers)
- [ ] CI pipeline passes (lint + test + build + security)
- [ ] No merge conflicts
- [ ] Branch is up-to-date with target branch

---

## Post-Merge (if applicable)

- [ ] Staging deployment successful
- [ ] Smoke test on staging passed
- [ ] No error rate increase in monitoring
```

---

## Transformation Rules

| AP Content | Output |
|-----------|--------|
| Quality attribute: Security (Critical/High) | Security section items |
| Quality attribute: Reliability | Testing rigor requirements |
| Quality attribute: Performance | Performance-related items (if targets exist) |
| Testing strategy from AP | Testing section requirements |
| Security Architecture review requirements | Security section |
| Git workflow (review process) | Review & Merge section |
| Observability requirements | Observability section |

---

## Key Rules

1. **Every section traces to a steering file** — DoD items reference specific rules
2. **All checkboxes are binary** — can verify yes/no, not subjective quality
3. **Security is non-negotiable** — security section is present regardless of depth
4. **Conditional sections** — Database and API sections only apply when those areas are touched
5. **DoD is a gate** — work that doesn't pass ALL applicable items is not done


---

## Target: backlog/DEFINITION_OF_READY.md (Paired Output)

### Purpose

The Definition of Ready (DoR) is the **sprint entry gate** — it defines when a story is sufficiently prepared to be worked on. It is the natural pair to DoD: DoR gates entry, DoD gates exit.

### Source

**From:** AI-POLC → PBP governance (`governance/definition-of-ready-done.md`) if present, else DWG derives from the story format and team standards.

### Structure

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-POLC — governance/definition-of-ready-done.md"
generatedOn: "{generation-date}"
ownership: hybrid
projectId: "{project-id}"
---

<!-- AI-DWG generated | source: AI-POLC DoR + AI-DWG derivation | date: {generation-date} -->

# Definition of Ready

## When Is a Story "Ready" for Sprint?

A user story is READY to enter a sprint when ALL of the following are met. Unready stories MUST NOT be pulled into a sprint — they create waste and block flow.

---

## Story Completeness

- [ ] Story follows INVEST format (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- [ ] "As a / I want / So that" narrative is complete and specific
- [ ] Acceptance criteria are written in Given/When/Then format
- [ ] At least 2 acceptance criteria per story (covers happy path + one edge case minimum)
- [ ] Story is small enough for one sprint (≤ {team story point cap, e.g., 8 points})

---

## Dependencies Resolved

- [ ] No unresolved blockers or dependencies on other stories in same sprint
- [ ] External dependencies (APIs, third-party services) confirmed available
- [ ] Design/UX assets available (wireframes, specs) if UI work
- [ ] Test data or environment requirements identified

---

## Acceptance & Validation

- [ ] Acceptance criteria are testable (can write a test for each G/W/T clause)
- [ ] PO has confirmed acceptance criteria represent business intent
- [ ] Story has been estimated by the team
- [ ] Edge cases and error scenarios identified

---

## Technical Readiness

- [ ] Architecture approach clear (no open design questions)
- [ ] Relevant steering files identified (which rules apply to this story)
- [ ] No ambiguity that would require mid-sprint PO consultation

---

## Traceability

- [ ] Story links to parent epic
- [ ] Story appears in traceability matrix (backlog/traceability-matrix.md)
```

### Transformation Rules (DoR-specific)

1. **DoR is POLC-gated** — only generate when POLC is present (sprint readiness is a product concern)
2. **Source POLC's DoR if available** — if `governance/definition-of-ready-done.md` exists in PBP, use it as primary source (copy relevant criteria verbatim)
3. **Derive from story format** — if no explicit DoR in PBP, derive from the INVEST/G-W-T format the stories use
4. **Keep it short** — DoR should be quick to verify (< 20 items); long DoRs create ceremony overhead
5. **Binary checkboxes only** — same rule as DoD: every item is verifiable yes/no
