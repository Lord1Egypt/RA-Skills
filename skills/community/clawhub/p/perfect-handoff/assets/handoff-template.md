# Compact project handoff

## Goal and acceptance
State the current objective, completion conditions, explicit non-goals, and actual project root.

## Current state and evidence
Separate implemented, verified, unverified, and blocked. Include the check time and source. A historical snapshot is not a current external status.

## Workspace and change ownership
Record the project root, branch/HEAD when applicable, relevant uncommitted changes, their owner (user, this task, or unknown), and protected files.

## Decisions and boundaries
Keep decisions that affect the next step, with a short reason; the authorization scope, prohibited actions, and stop conditions. Mark undecided choices.

## Next step and validation
Give one primary action, prerequisites, success check, and failure stop condition. Keep secondary open items in a precise index.

## On-demand references
For each item, write: question; file/directory relative to the project root; section/symbol/search term; when to read. Do not enumerate every document or rely on line numbers alone. For a Markdown link, use a path relative to this handoff's directory or an absolute path; wrap paths containing spaces in angle brackets. Check anchors semantically.

## Coverage and gaps
State what was examined, unknown, or out of scope. List gaps that affect recovery; do not write “all done” without evidence.

## New-session handoff prompt
Fill in the actual absolute paths below, save this prompt in the handoff, and print it in full in the original conversation. Do not leave template instructions in the final project handoff.

```text
Resume the project at <project-root>. This first turn is for read-only recovery and a report; do not implement changes.
Follow the active project rules. Read <compact-handoff> first. Do not read old chats, long historical handoffs, the full specification/goal plan, or logs. Do not recursively open links or run perfect-handoff closeout again.
Keep proactive first-turn reads of the handoff and supplemental material within 12,000 characters. If needed, read one located excerpt and record its path/section and size. Never skip required rules. If a key prerequisite exceeds this budget, state the gap without dropping its constraint.
Verify the project identity, workspace, and relevant uncommitted changes. Treat tests, deployment, and runtime statements in the handoff as dated snapshots. Preserve user changes. Do not perform the recorded next task or external actions.
Briefly report the goal, verified state, blockers/conflicts, and the first recommended task with its acceptance condition. Then wait for my next instruction.
```
