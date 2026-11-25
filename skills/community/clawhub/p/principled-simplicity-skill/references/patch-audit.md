# Principled Simplicity — Patch Audit

Load this when: the system already has accumulated patches and you need to assess the damage, find the worst hotspots, and plan a gradual cleanup without breaking things.

**Core premise:** You cannot refactor everything at once. A patch audit identifies where the abstraction debt is highest, so effort goes to the right place first.

---

## Audit Entry Points

Bring one or more of the following:
- System prompt (full text)
- Routing logic or tool-selection code
- If/else branch cluster from a specific file
- List of tools/agents with descriptions
- List of rules added in the last N weeks
- Badcase log or issue tracker export

---

## Phase 1: Density Scan

Score each of the following. Count instances, not severity.

```text
[ ] Prompt sentences that encode business rules or permissions
[ ] If/else or switch branches handling specific user inputs
[ ] Keyword lists used for intent detection or tool routing
[ ] Regex patterns applied to user text
[ ] Hard-coded examples or case references in prompt or code
[ ] Duplicate logic across files or modules
[ ] Tools or agents with overlapping descriptions
[ ] Prompt sentences added specifically to fix a previous badcase
```

**Density score:**

```text
0–3 total:  Low patch density. Monitor, no immediate action needed.
4–8 total:  Medium density. Identify the top 2 hotspots for mechanism design.
9–15 total: High density. System is fragile. Prioritize audit before adding features.
16+:        Critical. New features are likely making things worse, not better.
```

---

## Phase 2: Hotspot Identification

For each high-count area:

```text
Hotspot name: _______________
What class of user input triggers this cluster?
How many distinct cases does it handle?
Are the cases growing?  [ ] Yes  [ ] No
Do two or more cases share a root cause?
Is there a mechanism that could replace this cluster?
```

Rank hotspots by: **frequency × maintenance cost × reuse potential**.

---

## Phase 3: Dependency Map

Before touching anything, map:

```text
Callers:          What relies on this behavior?
Downstream:       What does this output feed into?
Test coverage:    Would a regression be caught?
Last modified:    When was this last touched?
Incident history: Has a bug here caused a production incident?
```

If test coverage is missing: **write tests before refactoring, not after.**

---

## Phase 4: Incremental Migration Plan

```text
Step 1: Freeze the hotspot
Step 2: Write regression tests for existing cases
Step 3: Design the replacement mechanism
Step 4: Build the mechanism alongside the patches
Step 5: Gate switch and remove patches incrementally
Step 6: Protect with eval
```

---

## Audit Output Format

```text
## Patch Density Score
Total signals: [N]
Level: [ ] Low  [ ] Medium  [ ] High  [ ] Critical

## Hotspot Map
#1: [name] — [N patches] — [class of problem]
    Replacement mechanism: [name or TBD]
    Dependency risk: [Low / Medium / High]
    Test coverage: [Yes / No]

## Decisions Required Before Refactoring
1. ...

## Migration Sequence
Phase 1: Freeze hotspot + regression tests
Phase 2: Build mechanism in parallel
Phase 3: Remove patches
Phase 4: Eval protection
```

---

## Signals That Refactoring Is Working

```text
✓ Prompt length decreasing
✓ New features don't require new if/else branches
✓ Badcase clusters shrinking
✓ Same mechanism handles cases that previously needed separate patches
✓ Regression suite grows with capability
```

## Signals That Refactoring Has Gone Wrong

```text
✗ New abstraction created more branches than it removed
✗ Mechanism is more complex than the patches it replaced
✗ Tests were written after refactoring
✗ Team moved new patches to adjacent areas
✗ Mechanism only works in one domain
```
