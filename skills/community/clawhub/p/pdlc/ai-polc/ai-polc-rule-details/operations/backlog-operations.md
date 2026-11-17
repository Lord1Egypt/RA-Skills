<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 14: Backlog Operations

**Phase:** Operations (repeating)
**Purpose:** Ongoing backlog maintenance — refinement, splitting, tech-debt trade-offs, stale-item cleanup, and health monitoring. The discipline that keeps the backlog a living strategic instrument rather than an ever-growing pile.

---

## MANDATORY: Stage Sub-Role

During this stage, also adopt the **Business Analyst** sub-role:

### Behavioral Shifts
- Think in terms of backlog health: size, staleness, quality, and coherence
- Facilitate refinement conversations: challenge vague epics, split oversized ones
- Balance feature delivery against technical debt — make the trade-off explicit and governed
- Prune ruthlessly: items older than {N} sprints with no action → candidate for removal

### Anti-Patterns
- Do NOT let the backlog grow indefinitely without pruning
- Do NOT refine items that aren't in the next 2-3 sprints (waste)
- Do NOT split stories for the sake of splitting — only when they breach DoR size criteria
- Do NOT treat tech debt as "free" — it competes for capacity like any other work

### Quality Check
After every refinement session, the backlog should be SMALLER or the same size (not larger). New items added = old items removed or deprioritized.

---

## Behavior by Mode

| Mode | Stage 14 Behavior |
|------|------------------|
| **Standalone (no DLC)** | Part of a repeating cycle (14→15→16→14...). PO drives cadence. |
| **Chain with DLC** | Re-entry point. User opens POLC session for refinement when needed. |

---

## Steps

### Step 14.1: Backlog Health Assessment

At the start of every refinement session, assess:

| Metric | Healthy | Warning | Action |
|--------|:---:|:---:|---|
| Total items | <50 | >100 | Prune stale items |
| Items without AC | 0 | >5 | Refine or remove |
| Items older than 3 sprints untouched | <5 | >10 | Assess: still relevant? |
| Items without goal linkage | 0 | >3 | Link or remove |
| Size distribution | Mix of S/M/L | All XL | Split oversized items |

### Step 14.2: Refinement Cadence

Define (or re-confirm) the refinement rhythm:

| Methodology | Recommended Cadence |
|---|---|
| Scrum | Once per sprint (mid-sprint, prepare for next) |
| Kanban | Continuous (refine when WIP drops below threshold) |
| SAFe | PI Planning refinement + per-sprint refinement |
| Shape Up | Per-cycle: shape next bets |

### Step 14.3: Splitting Criteria (Not Patterns)

AI-POLC defines WHEN to split (criteria). AI-DLC v1 defines HOW to split (patterns).

**Split triggers:**
- Epic estimated as XL → must split before entering a sprint
- Epic has >8 acceptance criteria → likely multiple concerns bundled
- Epic crosses bounded context boundary (DDD) → split by context
- Epic has internal dependencies → split into dependency-free slices
- Epic serves multiple user segments → split by segment

**PO responsibility:** Decide IF the split is needed. Dev team decides HOW to split.

### Step 14.4: Tech Debt Trade-Off Framework

Define the feature-vs-debt ratio:

| Tech Debt Level | Recommended Allocation |
|---|---|
| Low | 10-15% of capacity for tech debt / improvement |
| Medium | 20-30% of capacity |
| High | 30-40% of capacity (with explicit paydown plan) |

**Governance:**
- Tech debt items are tracked in the backlog (not hidden in a separate list)
- Each tech debt item must state: "If we don't address this, {consequence}"
- PO decides priority of tech debt against features — not the dev team alone
- Log tech-debt allocation decision: `POLC-D-NNN`

### Step 14.5: Stale Item Cleanup

Items that haven't moved in >3 sprints:
1. **Reassess:** Is this still aligned with the vision/goals?
2. **If yes:** Why hasn't it moved? (blocked? deprioritized? forgotten?)
3. **If no:** Remove from backlog. Log in Change Log: `POLC-C-NNN: Removed EPIC-XXX — no longer serves product goals`

**Rule:** Every refinement session should result in at least as many items removed/archived as added.

### Step 14.6: Reprioritization (If Needed)

If new information changes priorities:
1. Re-score affected items using the declared model
2. Update `prioritization-register.md`
3. Update `release-plan.md` if release composition changes
4. Log: `POLC-C-NNN: Reprioritized — {reason}`
5. Update `polc-state.md` Backlog Summary

### Step 14.7: Persist Changes

Update affected files:
- `prioritization-register.md` (if ordering changed)
- `release-plan.md` (if release composition changed)
- `epics/` (if epics were split, added, or removed)
- `traceability-matrix.md` (if goal/epic links changed)
- `polc-state.md` (Backlog Summary numbers)

---

## Gate

**Gate 14 — Refinement Complete:**

Present to user:
```
Backlog operations complete:
• Items refined: {N}
• Items split: {N}
• Items removed: {N}
• Items added: {N}
• Net change: {+/-N}
• Tech debt allocation: {%}
• Backlog health: {healthy | warning | needs attention}

Continue to Acceptance (Stage 15), or end session here?
```

---

## Transition

→ **Stage 15: Acceptance & Feedback** (if continuing)
→ **Session end** (if user chooses; state persisted)

---

*Detail file for AI-POLC Stage 14 | Phase: Operations*
