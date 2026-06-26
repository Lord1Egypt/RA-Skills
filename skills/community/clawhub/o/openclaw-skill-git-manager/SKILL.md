---
name: git-manager
description: Advanced Git operations support for bisecting regressions, cleaning up branches, managing stash workflows, and analyzing commit/history state. Use when users ask for "git bisect", branch cleanup, stash recovery/organization, reflog or log analysis, or safe handling of destructive/history-rewriting commands.
---

# git-manager

## Summary
`git-manager` orchestrates advanced repository maintenance by combining bisecting, branch cleanup, stash handling, and log analysis into a cohesive guidance skill. It keeps teams safe by pairing every destructive recommendation with an explicit verification or rollback prompt before running commands that rewrite history.

## Triggers
- `git manager`
- `bisect issue`
- `cleanup branches`
- `stash help`
- `analyze git log`
- `safe git ops`

## Workflow
1. **Assess repository health** – start with `git status`, review `git fetch --all`, and record the current branch/tag. Prompt the user: _"Are we on the branch that should move forward, or is a temporary diagnostic branch mounted?"_
2. **Bisect troubleshooting** – when isolating regressions, run `git bisect start` with the known good/bad commits and iteratively test. After each reproduce attempt, ask for confirmation before `git bisect good/bad`. Offer the safety reminder: _"Bisect rewrites HEAD; stash or commit open work first."_
3. **Branch cleanup** – use `git branch --merged` versus `git branch --no-merged` to find stale branches. Recommend `git branch -d <branch>` for merged work and `git branch -D` only after re-confirming the target branch via a safety prompt to avoid deleting active work.
4. **Stash management** – suggest `git stash list`/`git stash show` to catalogue hidden work. Encourage naming stashes with `git stash push -m "description"` and verify the exact entries before `git stash drop`/`pop`, reminding the user to keep a copy (`git stash branch <name>`) if they need extra safety.
5. **Log analysis** – guide through `git log --oneline --graph --decorate`, `git reflog`, and `git log @{u}` to understand recent operations. Offer commands like `git show <commit>` for inspection and highlight the importance of reviewing commit messages before reverting or cherry-picking.
6. **Safety prompts** – before destructive commands (e.g., `reset --hard`, `git clean -fd`, branch deletion, `rebase`, `push --force`), run the two-step destructive confirmation protocol: (1) display the current branch name and HEAD commit hash or tag, verify the target commit, and remind the user to take a backup action (tag, temporary branch, stash, export patch, etc.); (2) require an explicit textual `YES` reply before running the command. Always pair the recommendation with `git status`, `git log -1`, or a `git tag` snapshot so the user can see exactly what would change, and prefer `git push --force-with-lease` over `--force` unless the situation explicitly warrants the risk.

## Deliverables
- Provide step-by-step command sets for diagnostics (bisect, log review, stash recovery).
- Keep a safety checklist in every response: check HEAD, stash status, remote tracking state, and backup plan (tag or branch) before rewriting history.
- Offer follow-up summary: what was touched, what is stashed, and what commands to run next for cleanup.
