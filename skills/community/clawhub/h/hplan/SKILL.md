---
name: hplan
description: >
  Hierarchical persistent planning for complex multi-phase tasks. Use when the user
  asks to plan, break down, or execute a task involving multiple steps, deliverables,
  or coordinated work streams. Creates a .plan/ directory with overview.md (global
  summary) and per-phase directories (specs, checklists). Integrates with OpenClaw's
  memory system for cross-session continuity. Trigger phrases: plan, break down task,
  create plan, phased plan, multi-step task, start planning.
version: 1.0.0
metadata:
  openclaw:
    emoji: "📋"
    homepage: https://github.com/Noirewinter/hplan
    files:
      - "templates/*"
---

# hplan — Hierarchical Persistent Planning

Use the file system as persistent working memory for complex multi-phase tasks. This skill solves two problems that arise in long task executions:

- **Goal drift** — the agent gradually forgets the original objective as the work progresses
- **Spec loss** — detailed requirements, deliverables, and dependencies vanish from context

## Core Idea

```
Context window = RAM (volatile, limited)
File system    = Disk (persistent, unlimited)
Memory system  = Long-term recall (cross-session, searchable)
→ Task structure and specs go to .plan/ (file system)
→ Key milestones and decisions go to memory (MEMORY.md / daily notes)
→ The overview stays concise for quick re-reading
→ All three layers work together to prevent drift and loss
```

## .plan/ Directory Structure

All plan files are stored in the `.plan/` directory under the current workspace:

```
.plan/
├── overview.md              ← Global summary (≤25 lines, re-read frequently)
├── decisions.md             ← Decision log
├── errors.md                ← Error log
└── phases/
    ├── phase1_xxx/
    │   ├── spec.md          ← Detailed spec for this phase
    │   └── checklist.md     ← Item-by-item completion status
    ├── phase2_xxx/
    │   └── ...
    └── ...
```

Use the templates in `templates/` as starting points for each file. Always use relative paths (`.plan/...`) when reading and writing plan files.

## Integration with OpenClaw Memory

hplan uses the file system for structured task data (.plan/ directory) and OpenClaw's memory system for cross-session awareness. They serve different purposes:

| Layer | What it stores | Why |
|-------|---------------|-----|
| `.plan/` files | Full specs, checklists, detailed plans | Structured, complete, not subject to compaction |
| MEMORY.md | Task goal, current phase, key decisions | Survives session restarts, loaded automatically |
| Daily notes | Progress snapshots, phase completions | Searchable history, compaction-safe via memory |

### When to write to memory

- **Plan creation**: Save the task goal and phase list to memory (`"Active hplan: [goal], phases: [list], plan at .plan/"`)
- **Phase completion**: Save a progress snapshot (`"hplan progress: completed phase2_xxx, now on phase3_xxx, 2/4 phases done"`)
- **Important decisions**: When recording in `decisions.md`, also save a one-line summary to memory
- **Session ending with incomplete work**: Save current state (`"hplan paused: phase2_xxx in_progress (3/5), next step: [description]"`)

### When to search memory

- **New session**: Use `memory_search("hplan")` to quickly find if there's an active plan and what state it was in
- **Resuming after interruption**: Search for the latest progress snapshot to orient quickly
- **Cross-referencing past decisions**: Search memory for decision context from earlier sessions

## Mandatory Behaviors

Since this environment does not have automatic hook injection, you must follow these behaviors manually to maintain plan awareness:

### 1. Check .plan/ before any action

**This is the first thing to do in every conversation, before any file writes.**

Check if `.plan/overview.md` already exists:
- **Exists with incomplete phases**: Show the user the current goal and progress, then ask: "There is an unfinished plan. Would you like to continue it, or discard it and start a new plan?" Wait for the user's answer before doing anything else.
- **Exists with all phases complete**: Silently delete the entire `.plan/` directory and proceed normally.
- **Does not exist**: Proceed normally.

Never overwrite or modify an existing `.plan/` without checking its status first.

### 2. Re-read overview.md frequently

Before every significant action (producing deliverables, making decisions, starting a new step), re-read `.plan/overview.md` to stay aligned with the goal and current phase. This is the most important behavior — it prevents goal drift.

### 3. Re-read the current phase spec before working

When starting work on any phase, always read the full `spec.md` and `checklist.md` for that phase first. Do not skip this step.

### 4. Update progress after each subtask

After completing a subtask, immediately update:
- The phase's `checklist.md` (`[ ]` → `[x]`)
- The progress count in `overview.md` (e.g., `in_progress (3/6)`)

### 5. Context recovery on new conversations

When a user says "continue" or references an existing plan:
1. First, use `memory_search("hplan")` to find the latest plan state
2. Then check if `.plan/overview.md` exists and read it
3. Read the current phase's `spec.md` and `checklist.md`
4. Confirm the current state with the user before proceeding

### 6. Save progress before session ends

When the conversation is ending with incomplete phases:
- Save the current state to memory: goal, current phase, progress count, and next action
- This ensures the next session can pick up quickly even before reading .plan/ files

### 7. Check completion before finishing

Before ending your response on a planning task, verify whether all phases in `overview.md` are marked `[x]`. If incomplete phases remain, continue working or inform the user about remaining tasks. The user can exit the plan at any time by deleting the `.plan/` directory.

## Workflow

### Step 1: Create the Plan

After receiving a complex task:

1. Check `.plan/` status as described in Mandatory Behavior #1
2. Create the `.plan/` directory structure
3. Write `overview.md` using the template (≤25 lines)
4. Create phase directories with `spec.md` (≤60 lines each) and `checklist.md`
5. Create `decisions.md` and `errors.md`
6. **Save the task goal and phase list to memory** for cross-session recall

### Step 2: User Confirmation (cannot be skipped)

Present the plan to the user and wait for explicit confirmation before executing.

**What to show:**
- The full `overview.md` content (goal and phase breakdown)
- A summary of each phase's `spec.md` (key deliverables and scope)
- Total number of phases

**What to ask:**
- Is the phase breakdown reasonable? Need to add, remove, or split phases?
- Is the scope for each phase correct? Anything missing?
- Ready to start execution?

**Iterating on the plan:**
- If the user suggests changes, update the plan files accordingly
- Present the updated plan and ask for confirmation again
- Repeat until the user explicitly agrees
- Keep `overview.md` and phase directories in sync during any modifications: adding a phase means both an overview entry AND a new directory; removing a phase means both are deleted

**Only proceed to execution after the user explicitly confirms.**

### Step 3: Execute Phase by Phase

1. Read the current phase's `spec.md` and `checklist.md` in full
2. Work through checklist items one by one
3. Update `checklist.md` after each completed item
4. When a phase is complete:
   - Update `overview.md` and move to the next phase
   - **Save a progress snapshot to memory**

### Step 4: Phase Switching

When moving to the next phase:
1. Mark the completed phase as `[x] ... → complete` in `overview.md`
2. Update `current_phase` to the next phase ID
3. Read the new phase's `spec.md` and `checklist.md` before starting work
4. Save the phase transition to memory

### Step 5: Error Handling

```
1st failure: Diagnose and fix → record in errors.md
2nd failure: Try a different approach → record in errors.md
3rd failure: Re-examine assumptions → update spec.md
Still failing: Explain the situation to user, request guidance
```

## Plan Lifecycle

### New conversation with existing .plan/

When a new conversation starts, check if `.plan/overview.md` exists:

- **Has incomplete phases**: Ask the user whether to continue the existing plan or discard it and start fresh. Wait for the user's decision before proceeding.
- **All phases complete**: Delete the entire `.plan/` directory automatically, then proceed with the new task.

### After plan completion

When all phases are marked `[x]`:
1. Save a completion summary to memory: `"hplan completed: [goal], all N phases done"`
2. Inform the user that all tasks are complete

## overview.md Format (≤25 lines)

```markdown
# [Project Name]
current_phase: phase2_xxx

## Goal
[One sentence describing the final objective]

## Phases
- [x] phase1_xxx: [Phase description] → complete
- [ ] phase2_xxx: [Phase description] → in_progress (2/4)
- [ ] phase3_xxx: [Phase description] → pending

## Blockers
None

## Last Decision
[One-sentence summary]

## Last Error
None
```

Never put detailed task descriptions, lengthy requirements, or step-by-step procedures in `overview.md`. Those belong in the phase directories.

## Key Constraints

- `overview.md` ≤ 25 lines (re-read it frequently to prevent goal drift)
- `spec.md` ≤ 60 lines per phase (split into multiple phases if longer)
- Always read phase spec before starting work on it
- Update checklist immediately after completing each item
- Record decisions in `decisions.md`, errors in `errors.md`
- Save key milestones to memory for cross-session continuity
- You should aim to execute all checklist items yourself rather than handing them off to the user

## When to Use

- Multi-phase tasks (3+ phases)
- Complex projects with multiple deliverables or work streams
- Tasks requiring coordination across many steps or dependencies
- Long-running projects spanning multiple sessions

## When NOT to Use

- Simple questions or short tasks
- Single-step work that needs no tracking
