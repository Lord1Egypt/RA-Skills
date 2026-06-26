---
name: verification-before-completion
description: Verify real outcomes before saying work is complete. Use when implementing, fixing, configuring, or automating something where behavior must be confirmed, not just command success or edited text.
---

# Verification Before Completion

Before reporting that work is done, confirm the real outcome the user cares about.

## Core Rule

A successful command is not proof that the task is complete.
Always verify the user-visible result, system behavior, or intended effect.

## When to Apply

Use this skill when:
- code was changed
- config was edited
- automation was updated
- a bug was supposedly fixed
- a reminder/job was created or changed
- a browser/script flow was updated
- a migration or setup task was performed

## Workflow

1. Identify the actual outcome to verify.
2. Choose the cheapest realistic verification method.
3. Run the verification.
4. Report completion only if the real outcome is confirmed.
5. If partially verified, explicitly say what was verified and what was not.

## Verification Order

Prefer evidence in this order:
1. Actual behavior observed
2. Tool output proving the behavior
3. State inspection that strongly implies behavior
4. Text/config inspection only when no stronger method exists

## Examples

### Good
- Not just “calendar event created” → confirm returned event fields match date/title
- Not just “script updated” → run a smoke test
- Not just “page changed” → open page and inspect result

### Bad
- “Done” because file was edited
- “Fixed” because command exited 0
- “Configured” because text now looks correct

## Reporting Style

Prefer:
- what was changed
- how it was verified
- what remains uncertain, if anything

Example:
- "수정했고, dry-run으로 실제 동작 확인했어. 실 API 호출은 키가 없어서 아직 미검증이야."

## Common Traps

- confusing command success with task success
- verifying text instead of behavior
- skipping verification because result seems obvious
- claiming full completion when only partial verification happened

## Practical Examples

### Example: Reminder setup
- Weak: "리마인드 등록했어" because the add command returned success
- Strong: confirm the scheduled timestamp, payload text, and next run time

### Example: Script fix
- Weak: "수정했어" because the file changed
- Strong: run the script in dry-run or smoke-test mode and confirm output

### Example: Browser automation
- Weak: "페이지 열리게 했어" because navigation command ran
- Strong: confirm the target page title, key visible text, or expected element state
