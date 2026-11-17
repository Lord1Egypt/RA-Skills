<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "{upstream-steering-file}"
generatedOn: "{generation-date}"
ownership: generated
---
# Brownfield Baseline — Template

Generated into `.governance/brownfield-baseline.md` when Mode 3 (Brownfield Incremental Adoption) runs.

---

```markdown
# Brownfield Compliance Baseline — {project name}

**Established:** {date}
**Status:** Active (adoption period: 12 weeks from establishment)
**Acknowledgment:** Violations below are KNOWN TECHNICAL DEBT with a remediation plan.

---

## Baseline Summary

| Metric | Value |
|--------|-------|
| Overall compliance score at baseline | {x}% |
| Categories fully compliant | {n} |
| Categories with legacy violations | {m} |
| Security violations (2-week SLA) | {p} |
| General violations (12-week SLA) | {q} |

---

## Acknowledged Violations by Category

### {Category 1}

| Rule ID | Description | Count | Remediation SLA | Status |
|---------|-------------|:-----:|:--------------:|:------:|
| {ID} | {what's violated} | {n} | {date} | Open |

### {Category 2}
...

---

## Remediation Timeline

| Phase | Timeline | Target |
|-------|----------|--------|
| Immediate (Week 0) | New code MUST comply from today | All hooks enforce on new files |
| Early Wins (Weeks 1-4) | Security-critical violations | 2-week SLA items resolved |
| Steady Progress (Weeks 5-8) | High-priority violations | Blocking hooks extended |
| Convergence (Weeks 9-12) | All remaining violations | Full enforcement active |

---

## Sign-Off

This baseline is acknowledged as technical debt with a formal remediation plan.

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Tech Lead | ________ | ________ | ________ |
| PM | ________ | ________ | ________ |

---

*Established by AI-GCE Mode 3 (Brownfield Incremental Adoption) | {date}*
```
