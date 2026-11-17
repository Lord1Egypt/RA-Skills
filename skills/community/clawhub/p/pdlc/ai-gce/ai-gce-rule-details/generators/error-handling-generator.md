<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Error Handling Compliance — Derivation Logic

## Purpose

Derives error handling rules (ERR-*) from `error-handling.md`. 100% steering-derived.

---

## MANDATORY: Stage Sub-Role — Workspace Architect

During THIS activity, ALSO adopt the mindset of a **Workspace Architect**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in failure paths: every code path has a happy path AND an error path — both must be governed
- Enforce the Result pattern at the correct layer: application layer returns results, domain validates invariants, presentation formats errors
- Ensure error propagation rules prevent silent swallowing — every failure must surface somewhere
- Derive the API error format (RFC 7807, custom envelope) from error-handling.md, not from assumption
- Treat error handling as foundational (Tier 1): wrong error patterns early become expensive to refactor

### Anti-Patterns for This Activity
- Do NOT allow thrown exceptions for expected business failures (Result pattern exists for this)
- Do NOT conflate error HANDLING rules (ERR-*) with error LOGGING rules (LOG-*)
- Do NOT generate error format rules without verifying they align with api-standards.md error section

### Quality Check
A good output from this activity sounds like:
- "ERR-01: Application layer returns Result<T> — no thrown exceptions for expected failures. Tier 1. Enforced by post-task-governance.json after task completion."
- "ERR-03: HTTP responses use RFC 7807 Problem Details format. Cross-validated with GOV-API-005 from api-standards.md (consistent error format across both rule categories)."

---

## Source: `error-handling.md`

| Section | Generated Rules |
|---------|----------------|
| Result pattern usage | ERR-01: Application layer returns Result<T> — no thrown exceptions for expected failures |
| Exception usage | ERR-02: Exceptions reserved for truly unexpected failures only |
| API error format | ERR-03: HTTP responses use stated error envelope (RFC 7807 or custom) |
| Domain validation | ERR-04: Domain validates invariants — returns failure result, never throws |
| Error propagation | ERR-05: Errors propagate through result chain — no silent swallowing |

## Hook Mapping

Enforced by `post-task-governance.json` (checks ERR-* compliance on completed code).

## Tier: 1 (error handling is foundational)
