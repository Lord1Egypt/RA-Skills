---
name: GitHub Workflow
description: "Professional GitHub workflow skill for AI agents. Covers full project lifecycle: repo setup, Git Flow branching, atomic commits, pull requests, code review, CI/CD monitoring, semantic versioning, releases, secrets management, and security rules. Includes mandatory agent behavior directives for skill installation, new projects, and returning to existing work. Features built-in work log system for task state and session continuity. Trigger on: GitHub, git, gh CLI, repo, PR, branch, merge, commit, issue, release, CI, GitHub Actions, tag, secret."
---

# GitHub Skill

## Agent Directives

These are mandatory behavioral rules. Follow them in every situation involving code, projects, or tasks.

### On skill installation
When this skill is first loaded, introduce it to the user:
- Explain that all project work will now follow a professional GitHub workflow
- Mention: branching strategy, work logs, CI checks, semantic versioning, security rules
- Ask: "Do you have an existing project, or are we starting a new one?"

### On new project
**If this is the user's first project ever:**
- Check `gh auth status` — if not authenticated, run `gh auth login --web` before anything else
- Offer to create a new repo: name, visibility (public/private), license, .gitignore
- Set up branch protection on `main` and `develop` right away
- Clone into `~/workspace/projects/<repo-name>/`
- Create initial `develop` branch
- Confirm setup is complete before starting any work

**If the user already has projects:**
- Ask which repo they want to work on, or detect from context
- Clone into `~/workspace/projects/<repo-name>/` if not already there
- Verify branch protection is in place — if not, offer to set it up
- Proceed directly to task workflow

### On continuing existing work
When the user returns to an already-cloned project — run the Session start checklist (see Agent Workflow below) before making any changes.

### On every task
- Assess task scale first (see Task scale table in Agent Workflow).
- Tiny tasks: branch → commit → quick-log → PR → confirm with user → merge.
- Normal/significant tasks: Issue and work log are mandatory before branching.
- Never commit directly to `main` or `develop`.
- Never skip the pre-PR checklist on normal/significant tasks.
- Never expose tokens, secrets, or credentials in any command or output.
- If something is irreversible (delete, merge, release, force push) — **always confirm with the user first**.

### On using this skill
- This file (SKILL.md) is always in context — use it for workflow, branching, work log rules.
- Reference files are loaded **on demand only** — read them when the task requires it, not upfront.
- Work log is not optional — it is part of every task from start to finish.
- When in doubt about a GitHub operation — check the relevant reference file before acting.

---

## Security (always)
- All operations via `gh` CLI. Always `--repo owner/repo` outside a git directory.
- Auth: `gh auth login --web` or `GITHUB_TOKEN` env var
- Secrets: `gh secret set NAME --repo owner/repo` (interactive, never `--body`)
- Never print/log tokens. `gh auth status` to verify.

## Quick Reference

Read-only lookup. All write operations require explicit user confirmation — see ⚠️ markers in reference files.

| Task | Command |
|------|---------|
| Auth check | `gh auth status` |
| List PRs | `gh pr list --repo o/r` |
| Create PR | `gh pr create --repo o/r --title "..." --base develop --head branch` |
| PR checks | `gh pr checks <n> --repo o/r` |
| Merge (squash) | `gh pr merge <n> --squash --delete-branch --repo o/r` |
| Failed CI logs | `gh run view <id> --log-failed --repo o/r` |
| Re-run failed | `gh run rerun <id> --failed-only --repo o/r` |
| Create issue | `gh issue create --repo o/r --title "..." --body "..."` |
| Create release | `gh release create vX.Y.Z --repo o/r --title "..." --notes "..."` |
| Set secret | `gh secret set KEY --repo o/r` |
| Branch protect | `gh api --method PUT repos/o/r/branches/main/protection ...` |

## Branching Model
```
main       ← production, protected
develop    ← integration
feature/*  ← from develop
fix/*      ← from develop (reference issue: fix/123-desc)
hotfix/*   ← from main (emergency)
release/*  ← from develop (prep)
chore/*    ← from develop (deps, tooling, CI — no product change)
```
Commit convention: `feat: description (#42)` / `fix: description (#42)`
PR merge: `--squash` for features, `--merge` for releases.
Semver: `MAJOR.MINOR.PATCH` — breaking/feature/fix.

## Agent Workflow

### Workspace layout
Always clone into `~/workspace/projects/<repo-name>/`. Never work in `/tmp` — it doesn't persist between sessions.

```bash
mkdir -p ~/workspace/projects
gh repo clone owner/repo ~/workspace/projects/repo-name
cd ~/workspace/projects/repo-name
```

### Session start (every time)
```bash
gh auth status                   # 1. verify auth
git checkout develop && git pull # 2. sync before any work
git branch                       # 3. confirm you're on the right branch
# 4. open work/<issue>-<desc>.md and read Status.next
```

### Task scale
Before starting any task, assess its scale — this determines the workflow level.

| Scale | Signals | What to skip |
|-------|---------|--------------|
| **tiny** | ≤2 files, no backend/auth/infra, cosmetic or config change | Issue, PR, full work log → use `quick-log.md` instead |
| **normal** | 3–10 files, one area of the codebase | Issue optional if obvious, PR only if risky |
| **significant** | backend, auth, infra, API, DB, multi-component, deploy | Nothing — full workflow mandatory |

When in doubt — treat as significant.

### Clarification (significant tasks only)
Before creating an Issue or branching, ask until requirements are clear:
- What exactly needs to change and why?
- Are there affected components, APIs, or dependencies?
- Any constraints — performance, backward compatibility, deadlines?
- What does "done" look like?

**Do not start implementation until answers are clear.** For tiny/normal tasks — skip this, infer from context.

### Task process

**Tiny task:**
```
1. Branch from develop          → git checkout -b fix/short-desc
2. Atomic commit                → "fix: description"
3. Append to quick-log.md       → date + one line what changed
4. ⚠️ CONFIRM WITH USER — merge via PR → gh pr merge --squash --delete-branch
```

**Normal/significant task:**
```
1. Create or find the Issue                → gh issue create / gh issue list
2. Create work log file                    → work/<issue>-<desc>.md (see Work Log section below)
3. Branch from develop                     → git checkout -b feature/42-short-desc
4. Make small atomic commits               → one change per commit
5. Commit message references Issue         → "feat: description (#42)"
6. Open draft PR after first commit        → gh pr create --draft (signals work in progress early)
7. Monitor CI                              → gh run watch
   If CI fails:
   - Download failed logs                  → gh run view <id> --log-failed
   - Record cause in work log              → Status.blocked or Notes
   - Fix, commit ("fix: resolve CI failure"), push
   - Wait for green before proceeding
8. Pre-PR checklist (see below)
9. Mark ready + request review             → gh pr ready / gh pr review
10. Merge after approval                   → gh pr merge --squash --delete-branch
11. Close Issue + compact work log         → gh issue close 42
```

### Pre-PR checklist
Before marking PR ready:
- Run tests locally
- `git diff origin/develop` — no debug code, credentials, or temp files
- CI is green (`gh pr checks <n>`)
- PR description follows the template below
- **Self-review:** read your own diff one more time — check for hardcoded values, leftover debug statements, missing error handling. Only after this request human review.

**PR description template:**
```markdown
## What
Brief description of the change.

## Why
Closes #<issue>

## Changes
- Change 1
- Change 2

## Testing
- [ ] Tests pass locally
- [ ] CI green
- [ ] Manual check done (if UI)
```

### Between sessions
If a task is unfinished at end of session:
```bash
git stash push -m "wip: description of what's in progress"
```
Update `Status` and `next` in the work log, then stop. On next session: read `next`, then `git stash pop`.

### Merge conflicts
When a conflict occurs during merge or rebase:
```bash
git status                         # see conflicted files
# Open each file — resolve manually, keep correct code
git add <resolved-file>
git rebase --continue              # or git merge --continue

# If too complex — abort and ask the user
git rebase --abort
git merge --abort
```
Rules:
- Never blindly accept `--ours` or `--theirs` without understanding the diff
- If unsure which change is correct — **stop and ask the user**
- After resolving, re-run tests before pushing

### Scope creep
If during implementation something additional is discovered that wasn't in the original Issue:
- Do **not** expand the current task
- Complete current task as originally scoped
- Create a new Issue for the additional work
- Add a note in the current work log under `Notes`

### Hotfix workflow
Hotfixes are emergency fixes branched from `main`. After merging into `main`, the same fix **must** be merged back into `develop` — otherwise the bug returns in the next release.

```
1. Branch from main                        → git checkout main && git pull
                                             git checkout -b hotfix/short-desc
2. Fix, commit                             → "fix: description"
3. Open PR → main                          → gh pr create --base main --head hotfix/...
4. Merge into main after approval          → gh pr merge --squash --delete-branch
5. ⚠️ CONFIRM WITH USER — merge into develop too → git checkout develop && git pull
                                                    git merge main
                                                    git push origin develop
6. Tag the release                         → gh release create vX.Y.Z --target main
7. Record in work log                      → what broke, what was fixed, why
```

Never skip step 5 — an unsynced `develop` will reintroduce the bug on next release.

---

## Work Log

Every task gets a log entry. Format depends on scale.

### Quick log (tiny tasks only)
One shared file per project: `work/quick-log.md`

```markdown
## 2026-05-08
- fixed listing card spacing (components/Card.css)
- updated parser timeout (config/parser.yml)
- corrected Georgian translation (locales/ka.json)
```

Append one line per tiny task. No structure, no status, no decisions. Created once, never compacted.

### Full log (normal / significant tasks)
Every significant task gets its own log file. It is the agent's memory — orientation, decisions, state.

### Setup
```bash
mkdir -p work
# Add to .gitignore once per project
echo "work/" >> .gitignore
```
File: `work/<issue-number>-<short-desc>.md`

### Structure
```markdown
# Task: <title> (#<issue>)
Goal: <one sentence — what "done" means>

## Status
current: <what agent is doing right now>
next: <planned next action>
blocked: <blocker or —>

## Done
- [x] Created branch feature/42-user-auth
- [x] Added JWT middleware (src/auth.js)
- [ ] PR review pending

## Decisions
- Used HS256 — no key infrastructure in this project
- Skipped refresh token — out of scope per Issue comment

## Notes
- src/auth.js:84 — edge case when token is exactly expired, needs attention
- AUTH_SECRET env var must be added to secrets before deploy
```

### When to write

| Event | Action |
|-------|--------|
| Session start | Read `next`, update `current` |
| File or module created | Add to `Done` |
| Decision made | Add to `Decisions` with reason |
| Unexpected finding | Add to `Notes` |
| Step completed | Check off `Done`, update `next` |
| Session end | Update `Status`, write `next` explicitly |
| Task complete | Compact, then archive |

### Compacting
Compact when file exceeds ~80 lines **or** when task is complete.
- `Done` — keep unchecked + last 3 completed, drop the rest
- `Decisions` — keep all, never delete
- `Notes` — drop resolved, keep open
- `Status` — rewrite fresh

### Rules
- Always update `next` before ending a session — it is the re-entry point
- Never delete `Decisions` — they prevent re-debating solved problems
- Never store secrets, tokens, or credentials in work logs
- Compact proactively — a bloated log defeats the purpose

---

## When to read reference files

Load only what you need for the current task:

| Task | Read |
|------|------|
| Setting up a new repo, branch protection | `references/repo-setup.md` |
| PRs, reviews, merge strategies | `references/pull-requests.md` |
| CI runs, GitHub Actions | `references/ci-actions.md` |
| Releases, versioning, tags | `references/releases.md` |
| Secrets, environments | `references/secrets-envs.md` |
| JSON queries, audit, search | `references/api-queries.md` |
