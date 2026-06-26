# Stall Detection

Detect when a completed action requires follow-up steps that are not being executed, and invoke `/fix` to resolve.

## When to Activate

This topic runs as a **post-completion check** after `/next` suggests actions or after any skill completes.

### Stall Signals

| Signal | Example |
|--------|---------|
| Skill completed but pending tasks remain | ClawHub deploy done, but sync.sh not run |
| CodeRabbit review received but no action taken | PR has actionable comments, assistant is idle |
| Commit done but push not offered | `git commit` succeeded, no push prompt |
| Test failed but no diagnosis started | Test output shows failure, assistant reports "done" |
| CI triggered but result not checked | `gh run rerun` executed, no `gh run watch` follow-up |
| AskUserQuestion answered but action not executed | User selected an option, assistant acknowledged but didn't act |

### Detection Logic

After any task completion or skill execution:

1. **Check pending tasks**: Are there uncompleted tasks in the task list?
2. **Check workflow rules**: Does an active workflow rule mandate a follow-up step? (e.g., CI pass → verify unchecked Test Plan items)
3. **Check PR/issue body**: Are there unchecked `- [ ]` items in the PR Test plan or issue checklist?
4. **Check fix_plan.md**: Does the current item have incomplete sub-steps?
5. **Check skill procedure**: Did the skill's documented steps complete fully?
6. **Check user response**: Did the user answer an AskUserQuestion that implies an action?

If any of the above is true and no action is being taken → **invoke `/fix`**.

## Invocation

```
Skill("fix", "stall detected: <description of what's stalled>")
```

The fix skill will:
1. Identify the root cause (which step was skipped)
2. Execute the missing step
3. Record the pattern to prevent recurrence

## Examples

### Example 1: Deploy without sync

```
Completed: clawhub publish claude-session v0.1.2
Stall: sync.sh not run, es6kr/skills repo not updated
→ Skill("fix", "stall detected: ClawHub publish completed but es6kr/skills sync not executed")
```

### Example 2: User selection ignored

```
AskUserQuestion answer: "proceed" (proceed with publish)
Stall: No clawhub publish command executed after approval
→ Skill("fix", "stall detected: user approved publish but no action taken")
```

### Example 3: CI result not checked

```
Completed: git push origin develop
Stall: No gh run watch or CI status check initiated
→ Skill("fix", "stall detected: push completed but CI result not monitored")
```
