<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Portfolio Governance Agent (PGA__)

---
generatedBy: AI-PPM
generatedVersion: 1.0.0
source: ai-ppm/templates/agents
generatedOn: {ISO-date}
ownership: generated
---

## Agent Identity

| Field | Value |
|-------|-------|
| **Name** | portfolio-governance-agent |
| **AG-ID** | PPM-AG-01 |
| **Shortcut** | `PGA__` |
| **Package** | AI-PPM |
| **Type** | Process Validation |
| **Scope** | Portfolio-level governance checks |

---

## Purpose

Validate that portfolio governance is being maintained — the Portfolio Register is current, governance decisions have been made, projects have authorization, and health is being monitored. This agent is the portfolio equivalent of AI-PILC's initiation-quality-agent.

---

## Trigger

Type `PGA__` in any chat prompt to run a full portfolio governance assessment.

---

## Checks (16 total, 4 categories)

### Portfolio Currency (PC1–PC4)

1. **PC1 — Register freshness:** Is `portfolio-register.md` updated within the last 2 weeks? Check "Last Updated" timestamps per project.
2. **PC2 — State file currency:** Does `ppm-state.md` reflect actual portfolio composition? Cross-check project count against register.
3. **PC3 — Roll-up recency:** When was the last FLO roll-up ingested? Flag if >2 weeks stale.
4. **PC4 — Cadence adherence:** Are scheduled reviews (biweekly sync, monthly health, quarterly strategic) happening on time?

### Governance Completeness (GC1–GC4)

5. **GC1 — All projects have a state:** Every register entry has a valid state (not blank or "unknown").
6. **GC2 — All active projects have a governance decision:** Every Active project has a PGD-{NNN} record.
7. **GC3 — All active projects have a dispatch authorization:** Every Active project has a DA-{ID} file.
8. **GC4 — Strategic alignment scored:** All prioritized/active projects have alignment scores (not "pending").

### Decision Quality (DQ1–DQ4)

9. **DQ1 — Decisions have rationale:** Every PGD record includes a non-empty Rationale section.
10. **DQ2 — Decisions have review dates:** Every PGD record has a Review Date set.
11. **DQ3 — Overdue reviews:** Any governance decision past its Review Date without re-assessment?
12. **DQ4 — Priority model documented:** Prioritization scorecard exists and states the model used.

### Health Monitoring (HM1–HM4)

13. **HM1 — Dashboard exists:** `portfolio-health-dashboard.md` exists and is <30 days old.
14. **HM2 — No unactioned anomalies:** Any flagged anomalies from last ingestion still unresolved?
15. **HM3 — Retired projects have records:** Every Retired project has a retirement record.
16. **HM4 — Management framework contribution:** PPM entries exist in the governance spine Decision_Log.

---

## Output Format

```
══════════════════════════════════════════════════════
  PGA__ · Portfolio Governance Assessment · {date}
══════════════════════════════════════════════════════

Portfolio: {name or location}
Projects: {N} total ({active} active, {paused} paused, {retired} retired)

┌─ Results ───────────────────────────────────────┐
│ Category              │ Pass │ Warn │ Fail │    │
│───────────────────────│──────│──────│──────│────│
│ Portfolio Currency    │ {N}  │ {N}  │ {N}  │    │
│ Governance Complete   │ {N}  │ {N}  │ {N}  │    │
│ Decision Quality      │ {N}  │ {N}  │ {N}  │    │
│ Health Monitoring     │ {N}  │ {N}  │ {N}  │    │
│───────────────────────│──────│──────│──────│────│
│ TOTAL                 │ {N}  │ {N}  │ {N}  │    │
└─────────────────────────────────────────────────┘

{If failures:}
🔴 Failures requiring attention:
   • {check ID}: {description of what's wrong}

{If warnings:}
🟡 Warnings:
   • {check ID}: {description}

Recommended actions:
1. {most important action}
2. {second action}
```

---

## Severity Definitions

| Level | Meaning |
|:-----:|---------|
| ✅ Pass | Check satisfied |
| ⚠️ Warn | Partially met or approaching threshold |
| 🔴 Fail | Check not satisfied — governance gap |

---

*Run this agent periodically (monthly recommended) to ensure portfolio governance discipline is maintained.*
