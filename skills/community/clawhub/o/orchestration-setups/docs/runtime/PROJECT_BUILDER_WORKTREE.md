# Project Builder — Git Worktree Protocol

## Goal
Run `project-builder` against a real git repository/worktree so another agent can resume from concrete project state, not only chat state.

## Layout
- canonical repo root: existing git repository
- worktree base: `<worktree-root>/<repo>/<run-id>/`
- branch naming: `orch/<run-id>/<slot>`
- one worktree per active builder slot when parallel module work is needed

## Stable shared context
At each worktree root, expect:
- `README.md`
- `CLAUDE.md`

These are the first files a replacement agent should read.

## Shared temporary context
Per-run temporary context remains in:
- `agent/orchestration/runs/<run-id>/working-memory/`

Use it for:
- partial notes
- failed approaches
- unresolved questions
- integration concerns
- reviewer follow-up items

## Directed communication
Directed handoffs remain in:
- `agent/orchestration/runs/<run-id>/handoffs/`

## Resume protocol after agent failure
Replacement agent reads, in order:
1. worktree `README.md`
2. worktree `CLAUDE.md`
3. latest run handoff
4. run `working-memory/`
5. `git status`
6. latest relevant diff / branch history

## GitHub requirement
For GitHub-backed projects, a GitHub remote should exist before production use of `project-builder`.

The V1 helper validates whether a GitHub remote is configured. Pushing remains an explicit action, not an implicit side effect.
