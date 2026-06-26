---
name: coding-agent
description: Delegate coding tasks to Codex, Claude Code, Pi, or OpenCode from bash with safe launch modes, background monitoring, and repo-isolated review workflows.
metadata: { "openclaw": { "emoji": "🧩", "requires": { "anyBins": ["claude", "codex", "opencode", "pi"] } } }
---

# Coding Agent

Use this skill when you need another coding agent to implement or review changes in a repository.

## Use this for
- Building features that need multi-file edits.
- Large refactors where you want parallel workstreams.
- PR review or issue triage in an isolated checkout.
- Repeatable "run/fix/verify" loops that benefit from background execution.

## Do not use this for
- Tiny one-line edits you can apply directly.
- Read-only code lookup tasks.
- Work inside `~/.openclaw` for external repo reviews.

## Execution mode matrix
- `Codex`: use `pty:true`.
- `Pi`: use `pty:true`.
- `OpenCode`: use `pty:true`.
- `Claude Code`: use `--print --permission-mode bypassPermissions` (no PTY required).

Examples:

```bash
# Codex (PTY required)
bash pty:true workdir:~/project command:"codex exec --full-auto 'Add request timeout handling to API client and update tests.'"

# Claude Code (print mode, no PTY required)
bash workdir:~/project command:"claude --permission-mode bypassPermissions --print 'Refactor auth middleware and explain risk areas.'"

# OpenCode (PTY required)
bash pty:true workdir:~/project command:"opencode run 'Add retry/backoff for webhook delivery.'"

# Pi (PTY required)
bash pty:true workdir:~/project command:"pi 'Fix failing Vitest suite in src/api and keep behavior unchanged.'"
```

## Background session pattern

```bash
# Start
bash pty:true workdir:~/project background:true command:"codex exec --full-auto 'Implement issue #142 and run tests.'"

# Monitor output
process action:log sessionId:XXX

# Check running state
process action:poll sessionId:XXX

# Reply when prompted
process action:submit sessionId:XXX data:"yes"

# Stop session
process action:kill sessionId:XXX
```

## Safe review workflow
Never run PR review in your live OpenClaw repo. Use a temp clone or a worktree.

```bash
# Temp clone review
REVIEW_DIR=$(mktemp -d)
git clone https://github.com/org/repo.git "$REVIEW_DIR"
cd "$REVIEW_DIR" && gh pr checkout 130
bash pty:true workdir:"$REVIEW_DIR" command:"codex review --base origin/main"

# Worktree review
git worktree add /tmp/pr-130-review pr-130-branch
bash pty:true workdir:/tmp/pr-130-review command:"codex review --base main"
```

## Prompt template for long tasks

```text
Task:
- [clear scope]
- [constraints]
- [required checks]

When finished:
1) Summarize changed files and why.
2) Report test/lint commands and outcomes.
3) Run:
openclaw system event --text "Done: [brief result]" --mode now
```

## Failure recovery checklist
- If output stalls, poll once before killing.
- If agent asks for missing context, answer directly and continue the same session.
- If the session dies early, relaunch with a tighter prompt and explicit file scope.
- If multiple retries fail, switch to a fresh worktree to remove local state noise.

## Rules
1. Match the user-requested agent when explicitly specified.
2. Keep each session scoped to one repository and one objective.
3. Prefer `--full-auto` for implementation and conservative flags for review.
4. Send user updates at start, major milestones, blockers, and completion.
5. Do not silently take over coding work when orchestration mode was requested.
