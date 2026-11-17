<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "{upstream-steering-file}"
generatedOn: "{generation-date}"
ownership: generated
---
# Exception Workflow — Template

Generated into `.governance/compliance-log/exception-workflow.md` in the target workspace.

---

## What Is an Exception?

A **formal, approved bypass** of a compliance rule. It acknowledges an intentional violation, documents why, sets an expiry date, and ensures tracking until resolved.

---

## The 5-Step Process

```
1. ENCOUNTER → Developer hits a compliance violation
2. REQUEST  → Developer creates exception request with justification
3. APPROVE  → Approver reviews (different person for 🔴 Critical)
4. LOG      → Exception recorded in compliance-log/exceptions/
5. EXPIRE   → Expiry date forces resolution — flagged in next audit
```

---

## Approval Rules

| Rule Severity | Required Approver | Max Duration |
|:-------------:|:-----------------:|:------------:|
| 🔴 Critical | Architect or PM (MUST differ from requester) | 30 days |
| 🟠 High | Team lead (different person) | 90 days |
| 🟡 Medium | Self-document (requester logs it) | 180 days |

---

## Exception Request Fields

| Field | Required | Description |
|-------|:--------:|-------------|
| `ruleId` | ✅ | Which rule is bypassed |
| `justification` | ✅ | Specific reason — "we'll do it later" is NOT acceptable |
| `scope` | ✅ | What's covered (module, file pattern, or project-wide) |
| `requestedBy` | ✅ | Person requesting |
| `expiresAt` | ✅ | When the exception expires |
| `linkedTicket` | 🟠 | Ticket tracking the resolution |

---

## What Happens on Expiry

1. `exception-expiry-check` hook flags it as EXPIRED
2. Next audit includes it as a finding
3. If not resolved within one sprint after expiry → escalation
4. Resolution options: fix the issue, renew with fresh approval, or accept as ongoing risk (PM sign-off)

---

## Exceptions Are NOT

- Ignoring a rule because it's inconvenient
- A permanent waiver (every exception expires)
- A way to avoid fixing technical debt (it forces a deadline)
