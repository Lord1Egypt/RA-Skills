# Task Workflow — Full Lifecycle

This document covers everything about how you interact with tasks from the moment they're available to the moment they're done.

## Picking Up a Task

Tasks live in two source columns on the Asana board:
- **Features** — New functionality or enhancements from the SRS/Implementation Plan
- **Bugs** — Defects found during QA or reported by the client

### Pre-Start Checklist

Before moving any task to "In Progress," verify ALL of the following:

1. **Read the full task description.** Not just the title — the description, acceptance criteria, estimated effort, and any comments from the PM or Engineer.
2. **Locate the spec section.** Every task should reference a spec section from the Implementation Plan (e.g., "FE-003" or "BE-012"). Find it and read it. If no spec section is referenced, ask the PM or Engineer which section applies before starting.
3. **Check dependencies.** The task description should list any prerequisite tasks. Verify each dependency is in the "Completed" column. If any dependency is still open, do NOT start this task — pick another one or notify the PM that the task is blocked.
4. **Confirm you understand the acceptance criteria.** Can you describe, in concrete terms, what "done" looks like for each criterion? If not, escalate to the Engineer for clarification before starting.
5. **Check for relevant comments.** Other team members may have added context, warnings, or guidance in the task comments. Read them.

### Starting the Task

Once the pre-start checklist passes:
1. Move the task to **In Progress**
2. Add your start comment with the branch name (see `git_workflow.md` for naming)
3. Begin implementation

**Timing rule:** Move to "In Progress" the moment you begin active work — not when you plan to start, not after you've been working for an hour. The PM monitors the board for status reporting; inaccurate column placement means inaccurate reports.

## Working a Task

### The Acceptance Criteria Are Your Contract

The acceptance criteria in the task description are your definition of done. Implement against them exactly — not more, not less.

- If an acceptance criterion is ambiguous, escalate to the Engineer for clarification before implementing your interpretation
- If an acceptance criterion seems wrong or contradicts the spec section, the **spec section wins** — but notify the Engineer of the discrepancy so they can update the task or spec
- If you think an acceptance criterion is missing something important, raise it with the Engineer — don't add scope yourself

### Progress Communication

**When things are going well:** No news is fine news during normal progress. You don't need to post hourly updates. But if you're approaching the effort estimate for the task, post a progress note.

**When things are not going well:**

Add a comment to the Asana task immediately when:
- You hit a blocker that will delay completion
- You discover the task is significantly more complex than estimated
- You find a dependency that wasn't listed
- You need to deviate from the spec for a technical reason

Comment format for blockers:
```
BLOCKER: [Brief description of what's blocking you]
Impact: [None / delays completion by ~X days]
Action: [What you're doing about it — researching, escalating to Engineer, waiting on dependency]
```

### Approaching the Estimate

If the task was estimated at N days/hours and you're at 75% of that estimate without being close to done:

1. Assess honestly: how much more effort is needed?
2. Post a comment to the Asana task BEFORE the estimate expires:
   ```
   ESTIMATE UPDATE: Originally estimated at [X]. Current progress: [summary]. 
   Revised estimate: [Y]. Reason: [why it's taking longer — complexity, unexpected issues, spec gaps].
   ```
3. The PM uses these updates for client reporting — surprising them with a missed deadline damages the team's credibility

## The Blocker Decision Tree (Detailed)

When you're stuck, work through this decision tree in order:

### Level 1: Self-Help (30-minute rule)

- Is this a language/framework question? → Consult your stack skills and documentation first
- Is this a pattern you've seen before? → Check existing codebase for examples
- Is this a common error? → Research the error message
- **Time limit: 30 minutes.** If you haven't made meaningful progress in 30 minutes of self-help, move to Level 2.

### Level 2: Classify the Blocker

After 30 minutes of self-help, classify what you're dealing with:

| Classification | What It Means | Action |
|---|---|---|
| **Spec gap** | The spec doesn't cover this scenario | Escalate to Engineer with spec section ID |
| **Spec conflict** | The spec says one thing but existing code or another spec section says something else | Escalate to Engineer with both references |
| **Technical wall** | You understand what to build but can't figure out how | Escalate to Engineer with what you tried |
| **Dependency block** | You need another task completed first | Comment in Asana, notify PM, switch tasks |
| **Environment issue** | Config, access, tooling, or infrastructure problem | Attempt 30 min, then escalate to Engineer |
| **Scope question** | "Should this task include X?" — it's not clear from the task or spec | Ask the Engineer (technical) or PM (scope/priority) |

### Level 3: Escalate

Follow the format in `escalation_to_engineer.md`. Include what you tried so the Engineer doesn't re-tread the same ground.

## Completing a Task

### Pre-Completion Checklist

Before creating a PR, walk through every acceptance criterion:

```
For each acceptance criterion in the task:
  [ ] Implemented? 
  [ ] Tested locally?
  [ ] Matches the spec section description?
```

If any criterion is not met:
- If it's unfinished work → finish it
- If it's blocked by something outside your control → document it in the PR under "Known Limitations"
- If the criterion itself seems wrong → escalate to Engineer before submitting PR

### PR and QA Engagement

Once the pre-completion checklist passes:
1. Create the PR following the template in `pr_and_qa_handoff.md`
2. Notify QA with the PR link and task ID
3. Add the Asana comment noting the PR is open
4. **Do not move the task to the QA column** — QA moves it when they begin their review

### After QA Approval and Merge

1. Confirm the merge landed on main
2. Move the Asana task to **Completed**
3. Add the completion comment:
   ```
   PR merged. Task complete.
   ```
4. If there are follow-up items (tech debt notes, things to revisit, related future work), mention them in the completion comment so the PM can capture them

## Task Rejection / Reassignment

Sometimes a task gets reassigned or de-prioritized after you've started:
- If the PM moves your task back to Features or deprioritizes it: stop work, push your current branch (even if incomplete), add a comment noting where you left off, and pick up the next task
- If the Engineer restructures the spec section your task references: stop, re-read the updated spec, and confirm with the Engineer whether your current work is still valid
- In either case, keep your branch — don't delete it. It may be picked up again later.
