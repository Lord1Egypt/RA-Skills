<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Conditional Architecture — Derivation Logic

## Purpose

Derives rules from CONDITIONAL steering files (those that only exist if the architecture uses specific patterns). Each conditional file is self-contained — if the file exists, its rules are generated; if absent, nothing happens.

---

## MANDATORY: Stage Sub-Role — Systems Engineer

During THIS activity, ALSO adopt the mindset of a **Systems Engineer**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in conditional system boundaries: each conditional pattern (multi-tenancy, event-sourcing, resilience) is a discrete subsystem with its own invariants
- Respect the presence/absence signal — a missing steering file means the system does NOT use that pattern, period
- Evaluate each conditional for security criticality: tenant isolation is Tier A (immediate), resilience is Tier B (advisory)
- Consider interaction effects: activating multi-tenancy affects query patterns across ALL modules
- Ensure conditional hooks have technology-specific patterns derived from the actual stack

### Anti-Patterns for This Activity
- Do NOT generate rules for patterns the architecture doesn't use (no steering file = zero rules)
- Do NOT assume a conditional is "probably needed" — explicit signal only
- Do NOT mix conditional rule severity — tenant isolation is always 🔴 Critical regardless of tier gating

### Quality Check
A good output from this activity sounds like:
- "multi-tenancy.md exists → generating TENANT-* rules (3 rules) + tenant-isolation-check.json (fileEdited, Tier A). Pattern: `src/modules/*/domain/entities/**/*.ts`."
- "resilience-standards.md absent → zero RES-* rules generated, no resilience-gate.json created. Knowledge map shows: 'Resilience: N/A'."

---

## Conditional Derivation Table

| IF This File Exists | Generate These Rules | Rule Prefix | Hook |
|--------------------|--------------------|:-----------:|------|
| `multi-tenancy.md` | Tenant scoping on all queries, cross-tenant access prevention, tenant entity inheritance | TENANT-* | `tenant-isolation-check.json` (fileEdited Tier A 🔴) |
| `resilience-standards.md` | Retry policies enforced, circuit breaker configured per integration, timeout budgets | RES-* | `resilience-gate.json` (agentStop) |
| `observability-tracing.md` | Span naming per convention, required instrumentation points, trace context propagation | TRACE-* | `tracing-check.json` (agentStop) |
| `performance-standards.md` | Response time budgets per operation type (p95/p99), no N+1 queries, pagination required | PERF-* | (checked in `periodic-audit.json`) |
| `workflow-engine.md` | State machine patterns, workflow lifecycle rules, no direct state mutation | WF-* | (checked in `periodic-audit.json`) |
| `frontend-standards.md` | Component patterns, accessibility requirements (WCAG), state management rules | FE-* | `frontend-a11y-check.json` (agentStop) |
| `event-sourcing.md` | Event store patterns, projection rules, CQRS read/write separation, snapshot strategy | ES-* | `event-sourcing-check.json` (agentStop) |
| `feature-flags.md` | Flag lifecycle (create → rollout → permanent → retire), no stale flags, flag naming | FF-* | (checked in `periodic-audit.json`) |

---

## Extraction Pattern (Same for All Conditional Files)

For each conditional steering file that EXISTS:
1. Read ALL MUST/NEVER/ALWAYS statements → one rule per statement
2. Read all table entries → one rule per row (threshold, pattern, or constraint)
3. Assign severity based on security/data risk (🔴) vs. architectural drift (🟠) vs. quality (🟡)
4. Derive file patterns from tech-stack.md + module-structure.md
5. Generate hook if the conditional has a dedicated hook (see table above)

---

## Conditional NOT Generated = Zero Rules for That Category

If `multi-tenancy.md` does not exist:
- ZERO TENANT-* rules generated
- `tenant-isolation-check.json` NOT created
- Audit agent does not check for tenant isolation
- Knowledge map shows: "Tenant isolation: N/A (no multi-tenancy.md in workspace)"

This is correct behavior — don't enforce patterns the architecture doesn't use.

---

## Tier Assignment

All conditional rules: **Tier 2** (conditional patterns are activated once the team has basic governance in place).

Exception: `tenant-isolation-check.json` is Tier A 🔴 Essential (security-critical) even though the rule category itself is conditional.
