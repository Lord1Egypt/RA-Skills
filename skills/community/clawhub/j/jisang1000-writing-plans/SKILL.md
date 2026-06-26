---
name: writing-plans
description: Break work into clear, ordered plans before execution. Use when a task is multi-step, long-running, easy to derail, or needs coordination across tools, files, or agents.
---

# Writing Plans

Write plans that are concrete enough to execute, review, and verify.

## Core Rule

Do not jump into a long task with only a vague idea.
Break it into explicit steps with outcomes.

## When to Use

Use for:
- multi-step setup work
- migrations
- skill installation and validation passes
- browser automation workflows
- refactors
- research + implementation tasks
- tasks that may require sub-agents

## Plan Shape

A good plan includes:
1. Goal
2. Constraints
3. Ordered steps
4. Verification points
5. Possible blockers

## Good Step Format

Each step should answer:
- what to do
- what tool/file it touches
- what counts as success

Example:
1. Inspect installed files and runtime requirements.
2. Install missing low-risk dependencies.
3. Run smoke tests.
4. Separate working / needs-auth / broken states.
5. Report results.

## Execution Rule

After writing the plan:
- execute in order
- update the plan if reality changes
- do not hide changed assumptions

## Lightweight vs Heavyweight

### Lightweight plan
Use for 3-5 step tasks.

### Heavyweight plan
Use when:
- many files or tools are involved
- external systems are involved
- the task may run long
- sub-agents may help

## Reporting

Summarize with:
- planned scope
- what completed
- what changed during execution
- what remains

## Practical Examples

### Example: Skill setup pass
1. Inspect files and dependencies
2. Install missing low-risk runtime tools
3. Run smoke tests
4. Split results into working / needs-auth / blocked
5. Report next steps

### Example: Browser automation task
1. Confirm target site and success condition
2. Test a minimal path first
3. Add login/session handling if needed
4. Re-test the actual target flow
5. Record blockers clearly
