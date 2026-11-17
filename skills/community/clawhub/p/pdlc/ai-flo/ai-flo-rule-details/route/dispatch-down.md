<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 4: Dispatch (Down)

## Purpose

Receive AI-PPM's dispatch authorization and route it across the layer boundary to the correct Project-layer packages. This is the primary "downward" flow — portfolio decisions becoming project actions.

---

## Trigger

This stage executes when:
- A new `dispatch-authorizations/DA-*.md` file is detected from AI-PPM
- OR the operator issues a `dispatch` command
- OR FLO detects a `ppm-state.md` change indicating new authorizations

---

## Steps

### Step 1: Read Dispatch Authorization

Load the dispatch authorization document and extract:

| Field | Value | Used For |
|-------|-------|----------|
| Project ID | `{PRJ-ABBREV-YYYY-NNN}` | Correlation key for all routing |
| Project Name | `{name}` | Display |
| Priority | `#{N}` | Ordering when multiple dispatches |
| Scope | `Full / Design-only / Custom` | Project profile |
| Constraints | Budget, timeline, team, dependencies | Passed to Project layer |
| Entry Point | `{which packages to start}` | Routing target(s) |

### Step 2: Build Project Profile

From the dispatch scope, determine which packages this project will use:

| Scope | Profile | Packages Active |
|-------|---------|-----------------|
| Full | All canonical packages (sequential) | POLC → UXD → ADLC → DWG → DLC |
| Design-only | Architecture only (skip product/UX) | ADLC → DWG → DLC (skip POLC, UXD) |
| Custom | Operator specifies | As declared in authorization |

```
📨 New Dispatch: {Project Name}

  Project ID:  {ID}
  Priority:    #{N}
  Scope:       {Full / Design-only / Custom}
  Constraints: Budget ${X}, Timeline {Y}, Team {Z}
  
  Routing profile:
  {✅/🚫} AI-POLC  {✅/🚫} AI-UXD  {✅/🚫} AI-ADLC  ✅ AI-DWG  ✅ AI-DLC v1
  
  Entry point: AI-POLC (sequential chain starts here)
  Sequence: AI-POLC → AI-UXD → AI-ADLC → AI-DWG → AI-DLC v1
  
  Confirm dispatch? [Y] Proceed | [N] Hold | [E] Edit profile
```

### Step 3: Check for Conflicts

Before committing the dispatch:
- Does this Project ID already exist in `flo-state.md`? → conflict (duplicate dispatch)
- Are there dependency constraints that aren't met? → block
- Does the priority conflict with existing projects? → warning (contention)

If conflict detected → surface as alert (don't auto-dispatch).

### Step 4: Create Project Entry

Add the project to `flo-state.md`:
- Position: entry point package(s)
- Status: Dispatched (not yet In Progress — packages haven't started)
- Profile: from dispatch scope
- Priority: from authorization
- Workspace ref: local (`./`) or remote (ask operator for Mode 2/3)

### Step 5: Produce Dispatch Record

Create `dispatch-records/DR-{project-id}.md`:

```markdown
# Dispatch Record: DR-{Project-ID}

| Field | Value |
|-------|-------|
| Project ID | {ID} |
| Project Name | {name} |
| Dispatched | {ISO date} |
| Source | AI-PPM DA-{ID} |
| Priority | #{N} |
| Scope | {Full / Design-only / Custom} |
| Profile | {active packages list} |
| Entry Point | {first package(s)} |
| Constraints | Budget: ${X}, Timeline: {Y} |

## Routing Instructions

| Target Package | Action | Input Path |
|----------------|--------|-----------|
| AI-POLC | Start product ownership (first in sequence) | {PIP location} |

> Sequential flow: POLC → UXD → ADLC → DWG. Each package starts when its predecessor completes.
> FLO will route each handoff automatically via marker detection.

## Operator Action Required

Start a session for AI-POLC, pointing it at the PIP.
FLO will track progress via marker detection and route to AI-UXD when POLC completes,
then to AI-ADLC when UXD completes, then to AI-DWG when ADLC completes.

⚠️ **IMPORTANT: Start each package in a NEW session.**
   Each AI-* package loads a full workflow into context;
   a fresh session keeps it fast and focused.
```

### Step 6: Log and Notify

- Append to routing log: Type=Dispatch, From=AI-PPM, To={entry points}
- Append to spine: `FLO-D-{NNN}: Dispatch issued for {Project Name} ({ID}). Scope: {scope}. Priority: #{N}.`
- Update `flo-state.md` with new project entry

### Step 7: Handle Multiple Dispatches

If multiple projects are dispatched simultaneously:
- Process in priority order (highest priority first)
- Each gets its own dispatch record
- If contention warning exists (C2), surface it but don't block

```
✅ Dispatch complete: {N} project(s) routed

  | # | Project | ID | Priority | Entry Point | Status |
  |---|---------|-----|:--------:|-------------|--------|
  | 1 | {name} | {ID} | #1 | AI-POLC (sequential) | 📨 Dispatched |
  | 2 | {name} | {ID} | #2 | AI-ADLC (design-only) | 📨 Dispatched |
  
  Action: Start the entry-point package session. FLO routes each successor automatically.

  ⚠️ IMPORTANT: Start each package in a NEW session.
     Each AI-* package loads a full workflow into context;
     a fresh session keeps it fast and focused.
```

---

## Gate

Operator confirms dispatch targets and profiles before FLO commits. No dispatch executes without explicit confirmation.

---

## Transition

After dispatch, FLO returns to hybrid mode (monitoring). Next routing event triggers Stage 5 (fan-out/fan-in) or Stage 6 (handoff) when markers change.

---

*Part of AI-FLO v1.0.0*
