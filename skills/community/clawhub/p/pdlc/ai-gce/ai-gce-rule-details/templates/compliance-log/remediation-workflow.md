<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "{upstream-steering-file}"
generatedOn: "{generation-date}"
ownership: generated
---
# Remediation Workflow — Template

Generated into `.governance/compliance-log/remediation-workflow.md` in the target workspace.

---

## What Is a Remediation?

A tracked violation fix. When a compliance rule fails, a remediation entry is created to track it from detection to resolution.

---

## Remediation Lifecycle

```
DETECTED → OPEN → IN-PROGRESS → RESOLVED
                      ↓
               (if past SLA) → ESCALATED
```

---

## SLAs by Severity

| Severity | Remediation SLA | Escalation If Missed |
|:--------:|:--------------:|---------------------|
| 🔴 Critical | 24 hours | PM + Architect notified; blocks phase transition |
| 🟠 High | 14 days (1 sprint) | Team lead notified; appears in retro |
| 🟡 Medium | 28 days (2 sprints) | Appears in audit report |

---

## How Remediations Are Created

| Trigger | Creation |
|---------|----------|
| Audit finds 🔴 Critical violation | AUTO — remediation entry created immediately |
| Audit finds 🟠 High violation | AUTO — remediation entry created |
| Audit finds 🟡 Medium violation | MANUAL — team decides whether to track |
| Hook fires with `fail` result | NOT auto-created — hooks warn only; audit creates remediations |

---

## Remediation Entry Fields

```json
{
  "ruleId": "{RULE-ID violated}",
  "status": "open",
  "violationDate": "{when first detected}",
  "assignedTo": "{responsible person}",
  "sla": "{24h|14d|28d}",
  "resolvedAt": null,
  "notes": ""
}
```

---

## Resolution Process

1. Developer fixes the underlying issue
2. Next audit (or hook re-run) confirms the rule now passes
3. Remediation status → `resolved` with timestamp
4. MTTR (mean time to remediate) calculated for metrics

---

## MTTR Tracking

The audit agent calculates MTTR per severity:
- `MTTR = average(resolvedAt - violationDate)` for resolved items in the period
- Tracked in the compliance dashboard
- Target: Critical < 24h, High < 14d, Medium < 28d
