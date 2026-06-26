---
name: pr-pilot
description: "Submit professional pull requests and manage their full lifecycle — from push to merge. Covers PR creation with structured descriptions, CI monitoring, review response patterns, code iteration, and progress tracking. Use when submitting PRs to any repository, responding to code reviews, or managing multiple open PRs across projects."
---

# PR Pilot — PR Submission & Lifecycle Management

## Overview

Submit professional-quality pull requests and manage them through the full review lifecycle until merge (or closure). Covers PR creation, CI monitoring, review response, iteration, and tracking.

**Use cases**: Open-source contributions, team code reviews, multi-repo PR management, any code submission workflow.

## Prerequisites

GitHub CLI must be authenticated — PR creation, review monitoring, and commenting all require it:

```bash
gh auth status   # Must show "Logged in"
```

If not configured, ask the user to provide:
1. **GitHub username** — used for `--head {username}:{branch}` and PR search
2. **GitHub token** — run `gh auth login` or set `export GH_TOKEN=<token>`

Token is required for: creating PRs, posting comments, checking review status, pushing iterations.

## Part 1: Submit the PR

### Step 1: Stage & Commit (if not done)

```bash
# Stage specific files — never use git add .
git add {specific files}
git diff --cached --stat   # Verify

# Commit with conventional message
git commit -m "{type}({scope}): {description}"
```

### Step 2: Push to Remote

```bash
git push origin {branch-name}

# If this is a new branch:
git push -u origin {branch-name}
```

### Step 3: Write PR Description

Use this structured template. Adapt sections based on PR type and scope.

```markdown
## Summary

{1-2 sentence overview of what this PR does and why}

Closes #{issue_number}.

## Problem

{Description of the bug/issue being fixed:}
- What users experience
- Root cause analysis
- Impact / severity

## Solution

{Technical description of the approach:}
- Architecture / design decisions
- Key abstractions introduced (if any)
- Why this approach over alternatives

## Changes

| File | Change |
|------|--------|
| `path/to/file.py` | **New** — Description |
| `path/to/other.py` | Modified — Description |
| `tests/test_file.py` | **New** — N tests for feature |

## Testing

```
{paste test output}
N passed in X.XXs
```

{Describe what was tested:}
- Unit tests for ...
- Edge cases covered: ...

## Backward Compatibility

- No breaking changes / Breaking changes in ...
```

#### Adaptation by PR type

| PR Type | Focus Sections | Skip/Minimize |
|---------|---------------|---------------|
| Bug fix | Problem + Solution + Testing | Design Decisions (unless non-obvious) |
| Feature | All sections + Extensibility Example | — |
| Security fix | Defense-in-depth, bypass scenarios, residual risk | — |
| Refactor | Motivation, before/after comparison | Problem (reframe as "improvement") |

### Step 4: Create the PR

```bash
# Save description to a temp file
cat > /tmp/pr_body.md << 'EOF'
{pr description}
EOF

# Create PR
gh pr create \
    --repo {owner}/{repo} \
    --head {username}:{branch} \
    --base {default-branch} \
    --title "{type}({scope}): {description}" \
    --body-file /tmp/pr_body.md
```

### Step 5: Verify

```bash
# Check PR was created
gh pr view {number} --repo {owner}/{repo} --json url,state,statusCheckRollup

# Verify CI is running
gh pr checks {number} --repo {owner}/{repo}
```

### PR Description Quality Checklist

- [ ] Links to the issue being fixed (with `Closes #N`)
- [ ] Explains root cause, not just symptom
- [ ] Describes solution approach and design decisions
- [ ] Includes test results
- [ ] Has file change summary table
- [ ] Addresses backward compatibility

---

## Part 2: Manage the PR Lifecycle

### 2a. Monitor PR Status

Check status periodically:

```bash
# Single PR
gh pr view {number} --repo {owner}/{repo} \
    --json state,reviews,comments,mergeable,statusCheckRollup

# All your open PRs
gh search prs --author={username} --state=open \
    --json repository,number,title,url,updatedAt
```

### 2b. Respond to Reviews

When a reviewer provides feedback, classify and respond:

#### Pattern 1: Actionable Code Fix

> Reviewer: "This should handle the null case" / "Add error handling for X"

**Action**: Fix code → add test → push → reply.

```
Good catch — fixed in {commit_sha}. Added null check and a test case for this scenario.
```

#### Pattern 2: Architecture Concern

> Reviewer: "This approach is fundamentally flawed because..."

**Action**: If fundamental, consider full rearchitecture.

```
You're absolutely right — {acknowledge specific concern}. I've rearchitected this in #{new_pr_number}:

{Brief description of new approach}

Closing this PR in favor of the new approach.
```

**Steps for major rework**:
1. Create new branch from upstream
2. Reimplement with new approach
3. Create new PR referencing the old
4. Close old PR with comment pointing to new one
5. Reply to reviewer on new PR

#### Pattern 3: Style / Convention Nit

> Reviewer: "We use camelCase here" / "Please add docstring"

**Action**: Quick fix → push → reply.

```
Fixed in {commit_sha}, thanks for pointing out the convention.
```

#### Pattern 4: Question / Clarification

> Reviewer: "Why did you choose X over Y?"

**Action**: Explain clearly. If they suggest a better approach, adopt it.

```
{Direct answer}. {Trade-off explanation}.
```

#### Pattern 5: Request for Tests

> Reviewer: "Can you add a test for the edge case where...?"

**Action**: Write test → verify → push → reply.

```
Added in {commit_sha}. The new test covers:
- {scenario 1}
- {scenario 2}
```

### Iteration Workflow

```bash
cd ~/prs/{repo}
git checkout {branch}
git pull origin {branch}

# Make changes based on review
# ...

# Run tests
python -m pytest --tb=short

# Commit and push
git add {files}
git commit -m "address review: {description}"
git push origin {branch}
```

### 2c. Handle CI Failures

```bash
gh pr checks {number} --repo {owner}/{repo}
```

| CI Result | Action |
|-----------|--------|
| Failure in your code | Fix and push |
| Pre-existing/flaky failure | Comment on PR noting it |
| CI needs config | Check CONTRIBUTING.md |
| Merge conflicts | `git fetch upstream && git rebase upstream/main`, resolve, force push |

### 2d. Track Progress

Maintain `{workspace}/pr-tracker.md` for multi-PR management:

```markdown
# PR Campaign Tracker

> Last updated: {date}

| # | Repository | PR | Title | Status | Issue |
|---|------------|-----|-------|--------|-------|
| 1 | owner/repo | [#N](url) | fix(x): desc | 🟢 Open | #N |
| 2 | ... | ... | ... | 🟣 Merged | #N |
```

**Status icons**:
- 🟢 Open — Waiting for review
- 🟡 Changes Requested — Needs iteration
- 🔵 Approved — Ready to merge
- 🟣 Merged
- 🔴 Closed (not merged)

Update the tracker after each PR event (creation, review, iteration, merge, close).

---

## Review Response Principles

1. **Reply to every comment** — even if just "Done" or "Good point, fixed"
2. **Thank the reviewer** in your first response to a review round
3. **Never argue** — explain once, then defer to the maintainer
4. **Be specific** — reference commits, line numbers, test names
5. **Respond promptly** — within 24-48 hours keeps momentum
6. **Update PR description** if the approach changed significantly

## Output

- PR URL, CI status verified
- Review responses and iterations
- Updated `pr-tracker.md`

## Tips

- In a development pipeline, this follows **dev-test** and is the final delivery step.
- For managing a portfolio of PRs, run the status check periodically (or set up an automation).
- When responding to architecture concerns, creating a fresh PR (instead of force-pushing a rewrite) keeps the review history clean and makes reviewers' jobs easier.
- Always run tests locally before pushing review iterations.
