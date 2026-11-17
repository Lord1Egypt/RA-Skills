<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Compliance Log Governance — Derivation Logic

## Purpose

Derives compliance log governance rules (GOV-LOG-*). These rules govern the compliance logging infrastructure itself — ensuring the audit trail maintains integrity.

---

## MANDATORY: Stage Sub-Role — Audit & Compliance Specialist

During THIS activity, ALSO adopt the mindset of an **Audit & Compliance Specialist**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in audit trail integrity: the compliance log is the EVIDENCE that governance is working — corrupting it invalidates the entire system
- Enforce append-only semantics: editing or deleting log entries is equivalent to destroying evidence
- Ensure exception governance is rigorous: Critical rule bypasses need different-person approval, time-limited expiry, and escalation on expiry
- Treat log retention as regulatory: SOX = 7 years, GDPR = anonymize PII, default = project lifetime + 1 year
- Verify that every hook produces a log event — a hook without logging is an enforcement action without evidence

### Anti-Patterns for This Activity
- Do NOT allow self-approval of Critical rule exceptions (segregation of duties applies to bypass too)
- Do NOT allow exception expiry to exceed 30 days for Critical, 90 days for High (forces resolution)
- Do NOT treat compliance log governance as secondary to rule generation — the log IS the proof

### Quality Check
A good output from this activity sounds like:
- "GOV-LOG-002: Log files are append-only. NEVER edited or deleted. Any compliance-log file in .gitignore is a BLOCKING violation. Log files MUST be committed as compliance evidence."
- "GOV-LOG-004: Exceptions for 🔴 Critical rules require approval from a DIFFERENT person than the requester. Verified by exception-expiry-check.json (Tier 3, userTriggered)."

---

## Built-in Baseline (Primary Source — These Are Non-Negotiable)

| Rule ID | Statement | Rationale |
|---------|-----------|-----------|
| GOV-LOG-001 | `compliance-log/` folder MUST exist in project | Infrastructure for audit trail |
| GOV-LOG-002 | Log files are append-only — NEVER edited or deleted | Audit trail integrity |
| GOV-LOG-003 | Every hook fire produces a CHECK event in the log | Completeness of trail |
| GOV-LOG-004 | Exceptions for 🔴 Critical rules require approval from a DIFFERENT person | Segregation — self-bypass blocked |
| GOV-LOG-005 | Exceptions have expiry dates (max 30 days Critical, 90 days High) | Forces resolution |
| GOV-LOG-006 | Expired exceptions flagged in next audit | Accountability |
| GOV-LOG-007 | All 🔴 Critical violations have a remediation entry within 24 hours | Urgency enforcement |
| GOV-LOG-008 | Compliance dashboard updated after every audit | Visibility |
| GOV-LOG-009 | Log files committed to Git as compliance evidence (NOT in .gitignore) | Auditability |
| GOV-LOG-010 | Log retention: minimum per project's regulatory requirements | Compliance |

---

## Steering Enrichment

If `project-governance.md` or `scope-and-risks.md` mentions specific regulatory requirements:

| Regulatory Context | GOV-LOG-010 Becomes |
|-------------------|---------------------|
| SOX mentioned | "7-year retention for financial project logs" |
| GDPR mentioned | "Right to erasure applies to PII in logs — anonymize before retention" |
| No regulatory context | "Retain for project lifetime + 1 year" |

---

## Hook: `exception-expiry-check.json`

- **Event:** userTriggered (Tier 3)
- **Checks:** GOV-LOG-005/006 — finds expired exceptions, flags them

## Hook: Every hook (via mandatory logging block)

- **Checks:** GOV-LOG-003 is enforced by the mandatory compliance logging suffix in every hook prompt

## Tier: 2 (most rules) / 3 (exception-expiry-check hook activation)
