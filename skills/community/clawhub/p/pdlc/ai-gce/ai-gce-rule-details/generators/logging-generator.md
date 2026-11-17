<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Logging & Sensitive Data — Derivation Logic

## Purpose

Derives logging compliance (LOG-*) and sensitive data protection (SEC-PII-*) rules from `observability-logging.md` and `observability-sensitive.md`. 100% steering-derived for project-specific rules; built-in baseline covers "no secrets in code."

---

## MANDATORY: Stage Sub-Role — Automation Engineer

During THIS activity, ALSO adopt the mindset of an **Automation Engineer**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in data classification: what's safe to log (amounts, timestamps) vs. what's NEVER logged (passwords, tokens, SSNs)
- Treat sensitive-data-check as Tier A (immediate): PII in code is a compliance violation from the moment it's written
- Derive masking formats from steering — don't invent masking patterns
- Ensure correlation ID and structured logging rules are enforceable (specific field names, not vague "use structured logs")
- Consider the dual nature: logging rules improve observability, PII rules prevent regulatory violations

### Anti-Patterns for This Activity
- Do NOT defer sensitive-data-check to agentStop — secrets and PII in code are dangerous at every intermediate state
- Do NOT conflate logging format rules (LOG-*) with data protection rules (SEC-PII-*) — they serve different stakeholders
- Do NOT generate PII rules without specific categories from observability-sensitive.md

### Quality Check
A good output from this activity sounds like:
- "SEC-PII-01: NEVER log passwords, tokens, credit card numbers, SSN. Masking: email → `a***@domain.com`. Derived from observability-sensitive.md → PII Categories table."
- "sensitive-data-check.json fires on fileEdited (Tier A) with sessionDedup:true. Pattern: `**/*.ts`, `**/*.json`, `**/*.yaml`. Covers all files where PII could appear."

---

## Source Files

| File | Generated Rules |
|------|----------------|
| `observability-logging.md` | LOG-01: Structured logging format; LOG-02: Required logging points (entry/exit/error); LOG-03: Correlation ID in all log entries; LOG-04: Log levels used correctly |
| `observability-sensitive.md` | SEC-PII-01: Listed PII categories NEVER logged; SEC-PII-02: Masking format per data type; SEC-PII-03: Financial amounts OK, account numbers NEVER |

## Built-in Baseline

| Rule ID | Statement |
|---------|-----------|
| SEC-BASELINE-01 | No hardcoded secrets in source (also in security-compliance-gen) |

## Hook: `sensitive-data-check.json`

- **Event:** fileEdited (Tier A 🔴)
- **Pattern:** All code files (`**/*.{lang-ext}`, `**/*.json`, `**/*.yaml`)
- **Checks:** SEC-BASELINE-01, SEC-PII-01/02/03
- **sessionDedup:** true (only final state matters for log)

## Tier: 1 (logging and PII protection are foundational)
