# Asana Standards — Task Management and Communication

This document defines how you interact with the Asana project board. Your Asana skill handles the API calls — this document tells you what to do, when to do it, and what to write.

## Board Structure

> **Column names are defined per project.** The names below reflect the standard dev team setup from the build-dev-team skill. Always confirm the exact column names for your project from `PROJECT.md` and `project.json` in the project folder — do not assume these names are universal.

Every project board in the standard dev team setup has these columns:

| Column | Contains | Who Puts Tasks Here |
|---|---|---|
| **Backlog** | Tasks ready to be worked, not yet started | PM (from Implementation Guide) |
| **In Progress** | Tasks actively being worked on | Developer (you) |
| **In Review** | PR submitted, awaiting QA pickup | Developer (you) — move here after PR is open |
| **QA** | Tasks under active QA review | QA agent — moves task here when they begin |
| **Completed** | QA passed, awaiting operator merge | QA (after passing) |
| **Blocked** | Waiting on client, operator, or external dependency | PM owns |

### Column Movement Rules — What You Can and Cannot Do

**You move tasks:**
- **Backlog → In Progress**: When you begin active work on the task
- **In Progress → In Review**: When your PR is open (push complete, PR created or updated)
- **In Review → Completed**: Only after QA has approved and the PR has been merged to main

**You do NOT move tasks:**
- **In Review → QA**: QA moves the task themselves when they begin their review
- **Anything → Blocked**: Only PM or QA create and place tasks in Blocked
- **Completed → anywhere**: If a completed task needs rework, PM or QA will reassign it

**Why this matters:** The PM monitors column counts and movement patterns for status reporting. If you move tasks to QA yourself, it inflates the QA queue and misrepresents where work actually is.

## Comment Standards

Comments on Asana tasks are the project's communication backbone. The PM uses them for status reports. The Engineer reads them when reviewing your escalations. QA reads them for context before testing. Write them clearly and consistently.

### Required Comments — When and What to Write

#### When You Start a Task
```
Beginning work. Branch: feature/{task-id}-{role}-{slug}
```
This tells the PM the task is active and gives the Engineer the branch name for reference.

#### When You Hit a Blocker
```
BLOCKER: [Brief description]
Impact: [None / delays completion by ~X days]
Action: [Researching / Escalating to Engineer / Waiting on {dependency task-id}]
```
Post this immediately when blocked — not after spinning for a day. The PM needs to know about delays as they happen.

#### When You Need to Update the Estimate
```
ESTIMATE UPDATE: Originally estimated at [X]. Current progress: [summary].
Revised estimate: [Y]. 
Reason: [Why — more complex than expected / spec gap discovered / dependency delay].
```
Post this BEFORE the original estimate expires, not after. Proactive communication builds trust; surprises erode it.

#### When You Submit a PR
```
PR open: [PR link]
Spec section: [FE-XXX / BE-XXX]
Notifying QA for review.
```
This signals to the PM that the task is moving toward QA, and gives QA a starting point.

#### When You're Addressing QA Feedback
```
Addressing QA feedback. Items: [brief list or count].
Fixes pushed to branch. Re-review requested.
ETA: [date if significant rework needed].
```
This keeps the PM aware that the task is in the QA feedback loop, not stalled.

#### When an Escalation Is Resolved
```
Escalation resolved: [brief summary of what was decided].
[If spec was updated, note that here.]
Continuing implementation.
```
This closes the loop — the PM and Engineer can see the resolution without digging through other channels.

#### When the Task Is Complete
```
PR merged. Task complete.
[Optional: Any follow-up items or tech debt notes.]
```
This is the final status marker. Keep it clean and definitive.

### Comment Quality Guidelines

**Good comments are:**
- **Specific:** "Blocked by BE-015 — need the auth middleware endpoint available before FE can integrate" not "Blocked by backend work"
- **Actionable:** "Escalating to Engineer for spec clarification on error handling" not "Need to figure out error handling"
- **Timely:** Posted when the event happens, not retroactively at the end of the day
- **Self-contained:** Someone reading just the comments should understand the task's journey without needing to ask you

**Bad comments are:**
- Vague: "Working on it" or "Almost done"
- Late: Posting a blocker comment after you've already been stuck for two days
- Missing: No comment at all between start and PR submission — the PM assumes the task is on track and reports accordingly

## Task Description Expectations

When you pick up a task, expect the following fields to be present (the PM creates tasks with this structure):

- **Title**: Brief, descriptive
- **Description**: What to build, referencing the spec section
- **Acceptance Criteria**: Checkboxed list of "done" conditions
- **Spec Section Reference**: The Implementation Plan section ID (e.g., FE-003, BE-012)
- **SRS Requirement(s)**: The upstream SRS requirement IDs this task fulfills
- **Estimated Effort**: How long this should take (from the Engineer's estimate)
- **Dependencies**: Other tasks that must complete before this one can start
- **Assigned Role**: FE or BE

If any of these are missing from a task you pick up, ask the PM or Engineer before starting. Don't guess at missing acceptance criteria or dependencies.

## Working with Multiple Tasks

If you're working on more than one task (e.g., you were blocked on Task A and picked up Task B):

- Each task's Asana status must independently reflect reality
- If Task A is blocked, its status should show "In Progress" with a blocker comment — don't leave it in Features while you secretly work on Task B
- If you switch between tasks, add a comment to the paused task noting it's temporarily paused and why:
  ```
  Pausing — blocked by [reason]. Switching to [Task B ID] in the meantime. 
  Will resume when [blocker is resolved].
  ```

## Finding a Bug Outside Your Task Scope

If during your work you discover a bug in existing code that's unrelated to your current task:

1. **Do NOT fix it on your feature branch.** This is scope creep — it makes your PR bigger, harder to review, and mixes unrelated changes.
2. **Report it to the PM** with enough detail for them to decide whether to create a bug task:
   ```
   Found potential bug outside task scope:
   Location: [file/component/endpoint]
   Behavior: [what happens]
   Expected: [what should happen]
   Severity: [Cosmetic / Functional / Critical]
   Discovered while working on: [your task ID]
   ```
3. The PM will decide whether to create a Bugs column task for it. You may or may not be assigned that bug — either way, keep it out of your current feature branch.

## Sprint/Cycle Boundaries

If your team works in sprints or cycles:

- At the start of a sprint, review the tasks assigned to you and confirm you understand each one before beginning
- If you can't finish a task within the current sprint, add an estimate update comment early — the PM needs to know for sprint reporting
- At the end of a sprint, any task still "In Progress" should have a clear comment explaining where it stands and what remains
- Do not rush to close tasks at sprint boundaries by cutting corners — QA will catch it, and the rework will take longer than doing it right
