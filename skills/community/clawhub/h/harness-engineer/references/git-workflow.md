# GIT WORKFLOW

## STRATEGY: TRUNK-BASED DEVELOPMENT

- One main branch (main or trunk)
- Short-lived feature branches only -- max lifetime: CONFIG.yaml git.branch_max_lifetime
- No long-running feature branches. Decompose large features into shippable increments.

---

## CHECKPOINT COMMIT PROTOCOL

A checkpoint commit is made after every atomic task (T-NNN) is verified.

Rules:
  - Tests must pass BEFORE committing
  - Pre-commit hooks must pass BEFORE committing
  - Update PROGRESS.md (mark task complete) BEFORE committing
  - Never bundle two unverified tasks in one commit

Commit message format:
```
checkpoint(T-NNN): <short description>

Plan: PLAN-NNN.md
Tests: <pass count> passed, 0 failed
Coverage: <percent>%
```

Checkpoint commits are the recovery points. If context resets, the new agent
reads HANDOFF.md and resumes from the last checkpoint commit SHA.

---

## PR REQUIREMENTS (every PR must include)

- [ ] Reference to PLAN-NNN.md in PR description
- [ ] All tests passing (unit + integration + e2e)
- [ ] Pre-commit hooks passing
- [ ] Docs updated (spec, README, API docs as applicable)
- [ ] Security scan clean (scan_vulnerabilities)
- [ ] Coverage >= 90% on changed files
- [ ] All 3 reviewer layers approved (REVIEW-NNN-L1, L2, L3)
- [ ] Human approval (mandatory -- no auto-merge)

---

## MERGE REQUIREMENTS

PRs are merged by a human operator only, after:
  1. All CI checks pass
  2. All 3 reviewer layers have approved
  3. Human has reviewed the diff
  4. Human explicitly merges

There is no auto-merge. The harness creates PRs; humans merge them.

---

## FORBIDDEN ACTIONS

- Direct commits to main/trunk (use PRs)
- Merging with failing tests
- Merging without reviewer cycle completion
- Merging without docs updated
- Force-pushing to shared branches
- Bypassing the reviewer cycle
- Committing without checkpoint message format

---

## WORKTREE ISOLATION

For parallel ITR groups, each group works in an isolated git worktree.

### Protocol

1. Before dispatching an ITR group, create a worktree:
   git worktree add .worktrees/wu-{NNN}-{short-description} -b harness/wu-{NNN}

2. Implementer operates within the worktree:
   - All file reads/writes are scoped to the worktree
   - Tests run within the worktree environment
   - Commit checkpoints go to the worktree branch

3. After ITR cycle completes successfully:
   - All tests pass in the worktree
   - Reviewer approves the changes
   - Merge worktree branch back to trunk
   - Delete the worktree: git worktree remove .worktrees/wu-{NNN}

4. If ITR cycle fails:
   - Delete the worktree and branch (clean slate)
   - No partial state leaks into the main working tree

### Benefits
- True parallelism: multiple ITR groups can modify different files simultaneously
- Isolation: a failing group cannot corrupt the main working tree
- Clean rollback: failed work is deleted entirely, no merge conflicts to resolve

### Integration with Dispatcher

In agents/dispatcher.md, the dispatcher creates and manages worktrees as part
of the ITR group lifecycle. The worktree path is passed to the implementer
agent as the working directory.
