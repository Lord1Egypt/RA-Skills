<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Assumptions & Dependencies

| Field | Value |
|-------|-------|
| **Document** | Assumptions & Dependencies Register |
| **Project** | {project_name} |
| **Version** | {version} |
| **Date** | {date} |
| **Status** | _[Draft / Active / Closed]_ |
| **Owner** | {pm_name} |

---

## Assumptions Register

| ID | Date | Assumption | Impact if Wrong | Owner | Validate By | Status |
|:--:|:----:|-----------|-----------------|:-----:|:-----------:|:------:|
| ASM-001 | {date} | {what is assumed true} | {consequence if assumption is false} | {role} | {date/phase} | ☐ Unvalidated |

---

## Dependencies Register

| ID | Date | Dependency | Required By | Provider/Owner | Status | Risk if Unmet |
|:--:|:----:|-----------|:-----------:|:--------------:|:------:|--------------|
| DEP-001 | {date} | {what is needed from external source} | {milestone/phase} | {who provides it} | ☐ Unconfirmed | {consequence} |

---

## Constraints Register

| ID | Constraint | Type | Source | Non-Negotiable? |
|:--:|-----------|:----:|--------|:---------------:|
| CON-001 | {hard limit or boundary} | {Technical/Budget/Schedule/Regulatory/Resource} | {where this comes from} | {Yes/No} |

---

## Status Legend

### Assumptions
| Status | Meaning |
|--------|---------|
| ☐ Unvalidated | Not yet confirmed; proceeding on faith |
| ✅ Validated | Confirmed true |
| ❌ Invalidated | Proven false — mitigation required |
| 🔄 Under Review | Being checked |

### Dependencies
| Status | Meaning |
|--------|---------|
| ☐ Unconfirmed | Dependency identified but not yet secured |
| ✅ Confirmed | Provider committed; timeline agreed |
| ⚠️ At Risk | Provider indicates potential issue |
| ❌ Failed | Dependency will not be met — escalation required |

---

## Governance Rules

1. Every assumption is a risk in disguise — if unvalidated, it may trigger a risk
2. Dependencies should be confirmed as early as possible
3. Reviewed at every phase gate
4. Invalidated assumptions trigger immediate risk assessment
5. Failed dependencies escalate per project escalation criteria

---

*Last Updated: {date}*
