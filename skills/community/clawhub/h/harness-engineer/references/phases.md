# SYSTEM PHASES

The harness runtime operates in one of three phases. Agents adapt their behavior accordingly.

---

## PHASE 1: ACTIVE DEVELOPMENT
**Trigger:** Tasks exist in the backlog with specs and plans.

**Behavior:**
- Full loop runs: UNDERSTAND => DOCUMENT => PLAN => BUILD => VERIFY => REFLECT => IMPROVE
- All agents active.
- GC runs on schedule.
- Prioritization engine drives task selection.

---

## PHASE 2: MAINTENANCE MODE
**Trigger:** No new features. Only bug fixes, security patches, and dependency updates.

**Behavior:**
- Loop runs in reduced form: UNDERSTAND => VERIFY => REFLECT => IMPROVE
- `implementer_agent` only activated for confirmed bugs.
- `tester_agent` runs full suite every cycle.
- `garbage_collector_agent` runs every cycle (not on schedule).
- Security scans run every cycle.

---

## PHASE 3: OPTIMIZATION MODE
**Trigger:** No bugs. No failing tests. Only performance and maintainability improvements.

**Behavior:**
- `optimizer_agent` leads.
- All changes require baseline profiling before and after.
- No new features introduced.
- Docs must reflect current (not future) state.

---

## PHASE TRANSITIONS
Transitions are automatic based on task queue state.
Manual override requires a human decision logged in `docs/exec-plans/`.

```
Active Development
  v (no more features, tests green)
Maintenance Mode
  v (no bugs, security clean)
Optimization Mode
  v (new feature requested)
Active Development
```
