# PR Code Review

Review a PR's code changes and post structured review comments.

## When to Use

- User says "post review comment", "PR review", "review PR", "code review"
- After reviewing code in a merged or open PR
- When fix_plan has a "PR #N review" item

## Scope

This topic covers **human-initiated code review** — reading diffs, analyzing code quality, and posting findings.

For **AI bot review consolidation** (CodeRabbit, Copilot) → use `/consolidate pr-review`.

## Procedure

### Step 1: Identify Target

```bash
gh pr view <NUMBER> --json title,state,url,changedFiles,additions,deletions,headRefName
```

If the user specifies a particular file, focus review on that file.

### Step 2: Read Changes

```bash
# Full diff
gh pr diff <NUMBER>

# Specific file diff within the PR
gh pr diff <NUMBER> -- <path/to/file>
```

For merged PRs, read from the merge commit or the default branch.

### Step 3: Analyze

Review criteria (apply relevant ones):

| Category | Check |
|----------|-------|
| Correctness | Logic errors, edge cases, error handling |
| Performance | N+1 queries, unnecessary allocations, missing indexes |
| Security | Input validation, SQL injection, XSS, secrets exposure |
| Architecture | Singleton patterns, connection management, resource cleanup |
| Conventions | Project conventions compliance (`.claude/rules/`) |
| Dependencies | New deps justified, version pinning, license |

### Step 4: Structure Review

Use this template:

```markdown
## <Title> Code Review (`<file-path>`)

<1-line overall assessment>

### Strengths

| Item | Assessment |
|------|------------|
| ... | ... |

### Areas for Improvement (<priority>)

<description and suggested fix with code snippet>
```

Priority levels:
- **Critical** — must fix (bug, security)
- **Major** — should fix (performance, architecture)
- **Minor** — nice to have (style, readability)

### Step 5: Check Milestone

Verify the PR has a milestone assigned:

```bash
gh pr view <NUMBER> --json milestone --jq '.milestone.title // "none"'
```

- **No milestone** → query open milestones and suggest one based on the PR's change scope:
  ```bash
  gh api repos/{owner}/{repo}/milestones --jq '.[] | select(.state=="open") | "\(.title)\t\(.description)"'
  ```
  Include the recommendation in the review comment (e.g., "Milestone unassigned — suggest assigning `v0.5.0`").
- **Has milestone** → no action needed

### Step 6: Post Comment

Write body to a temp file, then post:

```bash
Write("/tmp/pr-review.md", "<review content>")
gh pr comment <NUMBER> --body-file /tmp/pr-review.md
```

**Do NOT use `--body` with multiline content** — use `--body-file` always.

### Step 7: Update fix_plan (if applicable)

Mark the review item as `[x]` with review summary.

## Rules

- **Post via `--body-file`** — never inline multiline body in shell args
- **Language**: use the repo's team language for review comments (Korean for private team repos)
- **Include code suggestions** with fenced code blocks when recommending changes
- **Do not auto-fix merged PRs** — review is comment-only for merged PRs
- **Open PRs**: suggest changes via comment; fixes require separate approval
