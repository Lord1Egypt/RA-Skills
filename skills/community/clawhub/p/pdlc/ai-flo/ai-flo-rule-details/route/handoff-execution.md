<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 6: Handoff Execution

## Purpose

Execute an individual routing handoff — move a project from one package to the next. This is the atomic routing operation: produce the handoff instruction, log it, update state, and notify the operator.

---

## Trigger

This stage executes when:
- A routing decision is confirmed (from Stage 4 dispatch, Stage 5 fan-out/fan-in, or Stage 7 override)
- A package completion is detected and the route is unambiguous (single successor, no fan-in wait)

---

## Steps

### Step 1: Validate the Route

Before executing the handoff, verify:

| Check | Pass? | Action if Fail |
|-------|:-----:|----------------|
| Source package marker shows Complete | ✅/❌ | If ❌: cannot route — package isn't done |
| Target package exists in workspace | ✅/❌ | If ❌: alert — target not installed |
| Target package is not toggled OFF for this project | ✅/❌ | If ❌: skip → advance to next successor |
| No active conflict for this project/field | ✅/❌ | If ❌: hold — conflict must resolve first |
| No active hold on this project | ✅/❌ | If ❌: cannot route while held |

If all checks pass → proceed to handoff.

### Step 2: Produce Handoff Instruction

Surface to operator:

```
📨 Handoff: {Project ID} → {Target Package}

  From:        {Source Package} (completed {date})
  To:          {Target Package}
  Project ID:  {PRJ-ABBREV-YYYY-NNN}
  Priority:    #{N}
  
  Input for {Target Package}:
  • {Predecessor output path(s)}
  • Project ID: {ID}
  • Constraints: {from dispatch — budget, timeline, etc.}
  
  Profile notes:
  • {Any relevant skip/toggle info for context}
  
  Action required: Start {Target Package} session pointing at the above inputs.
  
  ⚠️ **IMPORTANT: Start {Target Package} in a NEW session.**
     Each AI-* package loads a full workflow into context;
     a fresh session keeps it fast and focused.
  
  Confirm handoff? [Y] Proceed | [O] Override target | [H] Hold | [S] Skip
```

### Step 3: Update State

On confirmation:
- Update `flo-state.md` for this project:
  - `Current Package` → {Target Package}
  - `Current Status` → Dispatched (will become In Progress when target starts)
  - `Next Hop` → recalculated from routing table
  - `Last Activity` → now
  - Append to Position History: `{date} | {From} | {To} | {Trigger}`

### Step 4: Log the Handoff

Append to `routing-log.md`:

```
| {seq} | {timestamp} | {project-id} | {from} | {to} | Hop | {trigger} | {operator/Auto} | {notes} |
```

This is a routine hop — **NOT** logged to the governance spine (only decisions/issues go there).

### Step 5: Check for Follow-On Actions

After the handoff, check if any immediate follow-on is needed:

| Situation | Follow-On |
|-----------|-----------|
| Target is a fan-in target (DWG) | Trigger Stage 5 readiness check |
| Source had multiple targets (fan-out) | Handoff each target independently |
| Target is AI-POLC and UXD personas are ready | Include persona handoff reference |
| Project now at AI-DLC v1 | Companion packages (GCE/TGE) also activate |

### Step 6: Completion Confirmation

```
✅ Handoff logged: {Project ID} → {Target Package}

  Routing log: #{sequence}
  State: flo-state.md updated
  Next hop after {Target}: {next successor or "end of chain"}
```

---

## Batch Handoffs

When multiple projects route simultaneously (e.g., after a readiness check clears):

```
📨 Batch Handoff: {N} projects ready to advance

  | # | Project | From | To | Priority |
  |---|---------|------|----|:--------:|
  | 1 | PRJ-ERP-2026-001 | AI-POLC | AI-DWG | #1 |
  | 2 | PRJ-MOB-2026-003 | AI-ADLC | AI-DWG | #3 |
  
  Confirm all? [Y] All | [S] Select individually | [H] Hold all
```

---

## Gate

Operator confirms every handoff before FLO commits it. The only exception: if the operator has configured "auto-route for routine hops" (v1.1 — not in v1.0). In v1.0, every handoff surfaces for acknowledgment.

---

*Part of AI-FLO v1.0.0*
