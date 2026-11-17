<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Project Retirement Record: {Project Name}

---
generatedBy: AI-PPM
generatedVersion: {version}
source: portfolio-governance
generatedOn: {ISO-date}
ownership: generated
---

## Retirement Summary

| Field | Value |
|-------|-------|
| **Project ID** | {PRJ-XXX-YYYY-NNN} |
| **Project Name** | {name} |
| **Retirement Reason** | {Completed / Cancelled / Superseded / Merged / Failed} |
| **Retirement Date** | {ISO-date} |
| **Active Duration** | {months from admission to retirement} |
| **Governance Decision** | PGD-{NNN} |
| **Final Priority Rank** | #{rank} at retirement |

---

## Actuals vs. Planned

| Metric | Planned (at admission) | Actual (at retirement) | Variance |
|--------|:----------------------:|:---------------------:|:--------:|
| **Duration** | {N months} | {M months} | {+/- difference} ({pct}%) |
| **Budget** | ${planned} | ${actual} | {+/-}${amount} ({pct}%) |
| **Scope** | {planned scope summary} | {delivered scope summary} | {Full / Partial / Exceeded} |
| **Team Size (peak)** | {N FTE} | {M FTE} | {+/- N} |

---

## Benefits Status

| # | Benefit (from Business Case) | Status | Evidence | Timeline |
|---|------------------------------|:------:|----------|----------|
| 1 | {benefit description} | {✅ Realized / ⏳ Pending / ❌ Not realized} | {measurement or "pending"} | {when measurable} |
| 2 | {benefit description} | {status} | {evidence} | {timeline} |
| 3 | {benefit description} | {status} | {evidence} | {timeline} |

**Overall benefit realization:** {Fully realized / Partially realized / Not realized / Too early to measure}

---

## Capacity Released

| Resource | Allocation Released | Available From | Candidate for Reallocation |
|----------|:-------------------:|:--------------:|---------------------------|
| {Team/role} | {N FTE} | {date} | {which paused projects could use this} |
| {Budget} | ${amount} | Immediate | {portfolio reserve or specific project} |

---

## Portfolio Lessons

| # | Lesson | Impact on Future Governance |
|---|--------|----------------------------|
| 1 | {lesson learned} | {how this changes future scoring/estimation/governance} |
| 2 | {lesson learned} | {impact} |

> These are PORTFOLIO-level lessons (not project-level). They improve how we govern the portfolio, not how we run projects.

---

## Retirement Context

### Why This Reason?

{Explanation of why this project is being retired with this specific reason. For cancellations/failures: what went wrong? For completions: confirmation that objectives were met.}

### Impact of Retirement

- **On other projects:** {freed capacity enables X; removed dependency for Y; etc.}
- **On portfolio balance:** {changes distribution of investment themes/horizons}
- **On strategic alignment:** {remaining portfolio still covers objectives? Any gap?}

---

## Final Health Snapshot (at retirement)

| Metric | Value |
|--------|-------|
| RAG at retirement | {🟢🟡🔴} |
| Compliance score | {score}/100 |
| Test coverage | {pct}% |
| Open issues | {N} |
| Open risks | {N} |

---

## Cross-References

| Type | Reference |
|------|-----------|
| Original PIP | {path to pilc-state.md} |
| Admission decision | PGD-{NNN} |
| Retirement decision | PGD-{NNN} |
| Dispatch authorization | DA-{project-id}.md |
| Portfolio Register | Row updated to Retired |
| Management Framework | PPM-D-{NNN}, PPM-L-{NNN} |

---

*This record closes the portfolio lifecycle for this project. It is archived in the Portfolio Register's Retired section.*
