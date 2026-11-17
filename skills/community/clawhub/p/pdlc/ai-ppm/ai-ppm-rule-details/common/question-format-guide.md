<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-PPM — Question Format Guide

**Purpose:** Define how AI-PPM asks questions and collects decisions from the user. Portfolio governance decisions are consequential — the format must ensure clarity, auditability, and traceability.

---

## Standard Question Format

When asking the user to make a decision at any stage:

```markdown
### Q-{NN}: {Question Title}

**Context:** {Why this question matters to the portfolio}

**Options:**
- (a) {Option A} — {one-line consequence}
- (b) {Option B} — {one-line consequence}
- (c) {Option C} — {one-line consequence}

**Recommended:** Option {x}
**Rationale:** {Why this is recommended — grounded in portfolio data}

**Impact:** {What changes in the portfolio if this decision is made}

**Your Decision:** _[awaiting input]_
```

---

## Rules

1. **Always provide a recommendation.** Portfolio managers expect advisory guidance, not just options.
2. **Always state rationale.** "Because it scores highest" is not enough — explain WHY it scores highest.
3. **Always state impact.** What changes downstream? Which projects are affected?
4. **Number sequentially** within the session (Q-01, Q-02, …). Reset per session.
5. **Log every decision** in the Governance Decision Record or Management Framework Decision Log immediately upon user confirmation.
6. **User can always override.** Recommendations are advisory — the user holds governance authority.

---

## Governance Gate Questions (Stage 5)

Governance gate decisions use an elevated format because they are consequential (admit/pause/retire):

```markdown
### GQ-{NN}: {Project Name} — Governance Decision

**Project:** {Project Name} (ID: {Project ID})
**Current State:** {Registered | Paused | Active}
**Priority Rank:** #{rank} of {total}
**Strategic Alignment:** {score}/25
**Health (if available):** {RAG}

**Decision Required:**
- (a) **Admit** — authorize execution via AI-FLO → Project layer activates
- (b) **Pause** — authorized but deferred (reason: {capacity/timing/dependency})
- (c) **Hold** — not yet authorized; needs more information
- (d) **Retire** — remove from active portfolio (reason: {completed/cancelled/superseded})

**Recommended:** {option}
**Rationale:** {Why — referencing prioritization score, capacity, strategic alignment}
**Conditions (if any):** {What must be true for this to proceed}
**Review Date:** {When to revisit this decision}

**Your Decision:** _[awaiting input]_
```

---

## Prioritization Questions (Stage 4)

When scoring projects:

```markdown
### PQ-{NN}: Score {Project Name} on {Dimension}

**Dimension:** {e.g., Strategic Alignment / Business Value / Urgency / Risk}
**Scale:** 1 (lowest) — 5 (highest)
**Scoring Guide:**
- 1 = {what 1 means for this dimension}
- 3 = {what 3 means}
- 5 = {what 5 means}

**Suggested Score:** {N}
**Rationale:** {Based on PIP data: "{specific evidence}"}

**Your Score:** _[awaiting input or accept recommendation]_
```

---

## Batch Questions

When multiple projects need the same decision (e.g., scoring all projects on one dimension):

```markdown
### BQ-{NN}: Score All Projects on {Dimension}

| # | Project | Suggested Score | Rationale | Your Score |
|---|---------|:---:|---|---|
| 1 | {Project A} | {3} | {evidence} | _[   ]_ |
| 2 | {Project B} | {4} | {evidence} | _[   ]_ |
| 3 | {Project C} | {2} | {evidence} | _[   ]_ |

**Accept all recommendations?** [Yes / Adjust specific items]
```

---

## Quick Decisions (Low Ceremony)

For non-consequential decisions (configuration, format preferences):

```markdown
**Q-{NN}:** {Question}
Options: (a) {A} / (b) {B} / (c) {C}
Recommended: {x}. Proceed? [Yes / Change]
```

---

## Decision Logging

Every decision (regardless of format) is logged:

| Logged Where | When | Format |
|---|---|---|
| `portfolio-decisions/PGD-{NNN}.md` | Governance gate decisions (Stage 5) | Full Governance Decision Record |
| `management_framework/Decision_Log.md` | All other decisions | PPM-D-{NNN} row |
| `ppm-state.md` → Session History | Summary per session | One-line entry |

---

## Anti-Patterns

- Do NOT ask open-ended questions without options ("What should we do?")
- Do NOT present decisions without impact analysis ("Pick one")
- Do NOT skip the recommendation ("I don't have enough information" — use available data)
- Do NOT batch governance gate decisions — each project gets its own explicit decision
- Do NOT accept "yes to all" for governance gates — confirm each project individually

---

*Use this format consistently across all stages. It ensures decisions are traceable, auditable, and defensible.*
