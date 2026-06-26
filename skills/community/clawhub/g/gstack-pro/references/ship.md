# /ship — One-Command Ship

> **Role**: Release Engineer  
> **Activate**: `sessions_spawn(agentId="operator", task="...")`  
> **Goal**: sync main → run tests → push → PR — done in 6 steps

---

## Pre-flight Checklist

Must all be ✅ before running:

- [ ] Code review approved (at least 1 reviewer)
- [ ] All P0/P1 bugs fixed
- [ ] QA Health Score ≥ 70
- [ ] No unresolved merge conflicts
- [ ] Branch is rebased on latest main

If any item is ❌, STOP and report the blockers.

---

## Release Flow (6 Steps)

### Step 1: Sync Main

```bash
git fetch origin
git stash
git checkout main && git pull origin main
git checkout <feature-branch>
git rebase main
# If conflicts → resolve → git rebase --continue
```

### Step 2: Run Tests

```bash
npm run test && npm run build
# If fails → STOP and report error
```

### Step 3: Update Version

```bash
# Patch release (bug fixes)
npm version patch   # 1.0.0 → 1.0.1

# Minor release (new features)
npm version minor   # 1.0.0 → 1.1.0
```

### Step 4: Commit

```bash
git add -A
git commit -m "<type>(<scope>): <description>

BREAKING CHANGE: <if applicable>
Closes #<issue-number>"
```

### Step 5: Push

```bash
git push origin <feature-branch> --force-with-lease
# --force-with-lease: refuses push if remote has new commits
```

### Step 6: Open PR

```bash
gh pr create \
  --title "[Feature] <title>" \
  --body "## What Changed
- Change 1
- Change 2

## Test Results
Health Score: <score>/100

## QA Checklist
- [ ] Code review approved
- [ ] QA tests passed
- [ ] Functional tests passed

Closes #<issue-number>" \
  --base main
```

---

## Rollback Triggers

| Trigger | Action |
|---------|--------|
| Health Score < 50 | 🔴 Immediate rollback |
| Error rate > 1% | 🔴 Immediate rollback |
| P0 functionality broken | 🔴 Immediate rollback |
| Health Score 50-69 | 🟡 Evaluate |
| Console ERROR spam | 🟡 Evaluate |

**Rollback command:**
```bash
git revert <commit-hash>
git push origin main
```

---

## Output Format

```markdown
# /ship Release Report

## Pre-flight: ✅ All checks passed

## Release Details

| Item | Value |
|------|-------|
| Branch | `<branch-name>` |
| Commit | `<hash>` |
| PR | `#<number>` |
| Version | `<version>` |
| Build Time | `<timestamp>` |

## Next Steps
- [ ] Reviewer approves PR
- [ ] Merge to main
- [ ] Deploy to staging
- [ ] Monitor for 48 hours
- [ ] Deploy to production

## Rollback Plan
If issues detected, run:
\`\`\`bash
git revert <commit-hash>
git push origin main
\`\`\`
```
