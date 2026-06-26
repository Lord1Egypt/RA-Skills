---
name: issue-to-pr
description: "issue-to-pr — Automatically fix GitHub issues end-to-end: reads the issue, analyzes repository code, implements a fix, and submits a pull request. Use when the user provides a GitHub issue URL, mentions fixing a GitHub issue, or uses the /fix-issue command. Supports URLs in the format https://github.com/{owner}/{repo}/issues/{number}."
version: "1.3.0"
author: "4yDX3906"
tags: ["git", "github", "automation", "issue-fix", "pull-request"]
homepage: "https://github.com/4yDX3906/issue-to-pr"
metadata:
  clawdbot:
    emoji: "🔧"
requires:
  env: []
files: ["scripts/install.sh"]
---

# issue-to-pr — Agent Skill

You are an autonomous agent that reads a GitHub issue, understands the problem, locates the relevant code, implements a fix, and prepares everything for review. Follow the phases below **in order**, using the checklist to track progress.

---

## Progress Checklist

Use this checklist to track your progress through the workflow:

- [ ] Phase 1: Parse Issue Reference
- [ ] Phase 2: Fetch Issue Details
- [ ] Phase 3: Clone or Locate Repository
- [ ] Phase 4: Analyze the Issue
- [ ] Phase 5: Implement the Fix
- [ ] Phase 6: Verify the Fix
- [ ] Phase 7: Present Changes & Get Confirmation
- [ ] Phase 8: Submit Pull Request (User-Approved)

---

## Phase 1: Parse Issue Reference

Extract the GitHub issue reference from the user's input.

**Supported input formats:**

| Format | Example |
|---|---|
| Full URL | `https://github.com/owner/repo/issues/123` |
| Shorthand | `owner/repo#123` |
| Issue number only | `#123` or `123` (requires being in a git repo) |

### Parsing logic

1. **Full URL:** Scan for `https://github.com/{owner}/{repo}/issues/{number}` and extract components directly.
2. **Shorthand:** Match `{owner}/{repo}#{number}` pattern.
3. **Issue number only:** If only a number (or `#number`) is provided:
   - Run `git remote -v` to detect the current repository's GitHub remote.
   - Parse `owner` and `repo` from the remote URL (supports both HTTPS and SSH formats).
   - If not in a git repo or no GitHub remote is found, ask the user for the full URL.
4. If no valid reference is found, ask the user to provide a valid GitHub issue URL.
5. Confirm the parsed values before proceeding:
   > Parsed issue: **{owner}/{repo}#{number}**

---

## Phase 2: Fetch Issue Details

Retrieve the full issue content including title, body, labels, and comments.

### Strategy A: Use `gh` CLI (preferred)

Run in the terminal:

```bash
gh issue view {number} --repo {owner}/{repo} --comments
```

If the command succeeds, extract from the output:
- **Title**
- **Body / Description**
- **Labels**
- **Comments** (may contain important context, reproductions, or workarounds)

### Strategy B: Fallback to `fetch_content`

If `gh` is not installed or the command fails:

1. Use the `fetch_content` tool with the issue URL: `https://github.com/{owner}/{repo}/issues/{number}`
2. Parse the fetched page content to extract:
   - Issue title and body
   - Any referenced file paths, error messages, or stack traces
   - Comments from maintainers or the reporter

### Extract Key Information

From the issue content, identify and note:

| Field | Description |
|---|---|
| **Problem summary** | One-sentence description of the bug or feature gap |
| **Reproduction steps** | How to trigger the issue |
| **Expected behavior** | What should happen |
| **Actual behavior** | What actually happens |
| **Error messages** | Stack traces, log output, error codes |
| **File path hints** | Any files, modules, or functions mentioned |
| **Related issues/PRs** | Cross-references that provide context |

---

## Phase 3: Clone or Locate Repository

Ensure you have local access to the repository source code.

### Step 1: Check current workspace

```bash
git remote -v 2>/dev/null
```

- If the output contains `github.com/{owner}/{repo}` (or `github.com:{owner}/{repo}`), you are already in the correct repo. Skip to Step 3.

### Step 2: Clone if needed

If the current workspace is not the target repository, clone it:

```bash
gh repo clone {owner}/{repo} /tmp/{repo} 2>/dev/null || git clone https://github.com/{owner}/{repo}.git /tmp/{repo}
```

Then inform the user about the clone location.

### Step 2.5: Change into the repository directory

After locating or cloning the repository, `cd` into the repository directory before running any git commands:

```bash
cd {repo_path}
```

### Step 2.7: Check push permission and prepare fork if needed

Determine if you have push access to the repository:

```bash
gh api repos/{owner}/{repo}/collaborators/$(gh api user --jq '.login') --silent 2>/dev/null
has_push=$?
```

If `has_push` is non-zero (no write access), fork the repository now:

```bash
gh repo fork {owner}/{repo} --remote-name fork --clone=false
```

This ensures the fork is ready before creating the fix branch. Note which remote to push to:
- If you have write access: push to `origin`
- If you forked: push to `fork`

### Step 3: Ensure correct branch

First, detect the default branch:

```bash
# Detect the default branch (prefer GitHub API, fallback to git)
default_branch=$(gh api repos/{owner}/{repo} --jq '.default_branch' 2>/dev/null)
if [ -z "$default_branch" ]; then
  default_branch=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||')
fi
if [ -z "$default_branch" ]; then
  default_branch="main"
fi
```

Then check out the default branch and pull latest changes:

```bash
git checkout $default_branch
git pull --ff-only
```

Check if the fix branch already exists:

```bash
if git show-ref --verify --quiet refs/heads/fix/issue-{number} 2>/dev/null || \
   git show-ref --verify --quiet refs/remotes/origin/fix/issue-{number} 2>/dev/null; then
  echo "Branch fix/issue-{number} already exists"
fi
```

If the branch already exists, ask the user whether to:
- **Reuse** the existing branch and continue from where it left off
- **Recreate** the branch from the latest default branch (deletes existing work)
- **Rename** to `fix/issue-{number}-v2` (or incrementing suffix)

Create the fix branch:

```bash
git checkout -b fix/issue-{number}
```

---

## Phase 4: Analyze the Issue

Systematically locate the problem in the codebase.

### 4.1 Keyword Search

Use the error messages, file paths, and function names from the issue to search:

- Use `grep_code` to search for error strings, function names, or variable names mentioned in the issue.
- Use `search_codebase` for semantic searches when the issue describes behavior rather than specific code.
- Use `search_file` to find files by name if the issue mentions specific filenames.

### 4.2 Understand the Context

Once you find candidate files:

1. Read the relevant files to understand the current implementation.
2. Trace the code path that leads to the reported bug.
3. Check related tests to understand expected behavior.
4. Review recent git history for the affected files if useful:
   ```bash
   git log --oneline -10 -- {file_path}
   ```

### 4.3 Root Cause Analysis

Before writing any code, produce a structured analysis:

```
### Analysis Result
- **Root Cause:** {Why the bug occurs}
- **Affected Files:** {file1 (function_name), file2 (function_name)}
- **Fix Strategy:** {What the minimal change should be}
- **Risk Assessment:** Low / Medium / High
- **Estimated Changes:** {N files, ~M lines}
```

This structured output will be referenced in Phase 5 (implementation) and Phase 7 (summary).

### 4.4 Scope Assessment

Before proceeding to implementation, assess the scope:

- **Multiple sub-problems:** If the issue describes multiple distinct problems, focus on the most critical one first. Note remaining items for follow-up issues or separate PRs.
- **Monorepo detection:** Check for `workspaces` in `package.json`, `pnpm-workspace.yaml`, `lerna.json`, or similar workspace config files. If found, narrow your search scope to the relevant package/workspace.

---

## Phase 5: Implement the Fix

Apply the minimal code change to resolve the issue.

### Guidelines

- **Minimal diff:** Change only what is necessary to fix the issue. Do not refactor unrelated code.
- **Consistency:** Follow the existing code style, naming conventions, and patterns in the project.
- **No new dependencies** unless absolutely required and justified.
- Use the `search_replace` tool to make precise edits.

### If Multiple Files Need Changes

1. Plan the full set of changes before starting.
2. Apply changes one file at a time.
3. After each file change, verify there are no syntax errors using `get_problems`.

---

## Phase 6: Verify the Fix

Validate that the fix works and doesn't break anything.

### 6.1 Detect Project Type and Test Runner

Look for common indicators:

| File | Likely runner |
|---|---|
| `package.json` | `npm test` or `npx jest` or `npx vitest` |
| `Cargo.toml` | `cargo test` |
| `go.mod` | `go test ./...` |
| `pyproject.toml` / `setup.py` | `pytest` |
| `Makefile` | `make test` |
| `pom.xml` | `mvn test` |
| `build.gradle` | `./gradlew test` |

### 6.2 Run Tests

```bash
# Run the full test suite or scoped tests related to the changed files
{test_command}
```

- If tests **pass**, proceed to Phase 7.
- If tests **fail**, analyze the failure, adjust the fix, and re-run.

### 6.2.1 No Test Framework Detected

If no test runner or test files are found:

1. Run static analysis using `get_problems` on all changed files to catch syntax errors and type issues.
2. Manually verify the fix by reading through the changed code paths.
3. Note in the PR that automated tests were not available:
   > No automated test framework was detected in this project. The fix was verified via static analysis and manual code review.

### 6.3 Lint / Format Check (if available)

Check if the project has lint or format tools configured, and run them:

```bash
# Examples
npm run lint 2>/dev/null
cargo clippy 2>/dev/null
go vet ./... 2>/dev/null
```

Fix any lint issues introduced by your changes.

---

## Phase 7: Present Changes & Get Confirmation

Present the fix to the user and wait for explicit approval before proceeding.

### 7.1 Show Fix Summary

```
## Fix Summary for {owner}/{repo}#{number}

**Issue:** {issue_title}
**Root Cause:** {brief explanation}
**Changes:**
- `{file_path_1}`: {what was changed and why}
- `{file_path_2}`: {what was changed and why}
```

### 7.2 Show Diff

Display the actual code changes so the user can review them:

```bash
git diff
```

Highlight the key modifications and explain their impact.

### 7.3 Wait for User Confirmation

Ask the user:
> Would you like me to submit these changes as a Pull Request? If anything needs adjustment, let me know.

- If the user **approves**, proceed to Phase 8.
- If the user **requests changes**, revise the fix (return to Phase 5) and re-present.

---

## Phase 8: Submit Pull Request (User-Approved)

Only execute this phase after the user has approved the changes in Phase 7.

### Step 1: Stage and Commit

```bash
git add -A
git commit -m "fix: {short description} (#{number})

{Detailed explanation of what was wrong and how this commit fixes it.}

Closes #{number}"
```

### Step 2: Push the branch

Push to the appropriate remote based on the permission check from Phase 3:

```bash
# If you have write access (push succeeded in Phase 3 check):
git push origin fix/issue-{number}

# If you forked the repository in Phase 3:
git push fork fix/issue-{number}
```

### Step 2.5: Check for repository PR template

```bash
pr_template=""
for f in .github/PULL_REQUEST_TEMPLATE.md .github/pull_request_template.md docs/pull_request_template.md PULL_REQUEST_TEMPLATE.md; do
  if [ -f "$f" ]; then
    pr_template="$f"
    break
  fi
done
```

If a PR template is found, use it as the base for the PR body and fill in the relevant sections. Otherwise, use the default template below.

### Step 3: Create Pull Request

#### Default PR Body Template

```
## Summary

Fixes #{number}.

### Problem
{Brief problem description from issue analysis}

### Solution
{Brief solution description from fix implementation}

### Changes
- {change 1}
- {change 2}

### Testing
- [x] Existing tests pass
- [x] {Any additional verification performed}

---
<sub>🔧 Generated by [issue-to-pr](https://github.com/4yDX3906/issue-to-pr)</sub>
```

```bash
gh pr create \
  --repo {owner}/{repo} \
  --title "fix: {short description}" \
  --body "$pr_body" \
  --base {default_branch} \
  --head {head_ref}
```

> `{head_ref}` is `fix/issue-{number}` for direct push or `{your_username}:fix/issue-{number}` for fork push.

> **Tip:** Add the `--draft` flag to create a draft PR if the fix needs further review before marking as ready.

### Step 4: Verify & Report

- Capture the PR URL from the `gh pr create` output.
- Report to the user:
  > ✅ PR created successfully: {PR_URL}
  > Please review the PR page for any CI checks or reviewer feedback.
- If creation **fails**, show the full error and provide the manual command as a fallback.

### Fallback: Manual Instructions

If the user declines auto-submission or any step fails, present:

1. **Suggested commit message:**
   ```
   fix: {short description} (#{number})

   {Detailed explanation}

   Closes #{number}
   ```
2. **PR creation command:**
   ```bash
   gh pr create \
     --title "fix: {short description}" \
     --body "..." \
     --base {default_branch}
   ```
3. **Recommend next steps:**
   - Review the diff: `git diff {default_branch}`
   - Commit and push the changes
   - Create the PR and verify CI passes

---

## Error Handling

Handle these common failure scenarios gracefully:

| Scenario | Action |
|---|---|
| `gh` CLI not installed | Fall back to `git clone` and `fetch_content`. Suggest installing gh: `brew install gh` or see https://cli.github.com |
| `gh auth` not configured | Prompt user to run `gh auth login` and retry |
| Repository is private / 403 | Inform the user that authentication is required and guide them to authenticate |
| Issue not found / 404 | Double-check the URL and ask the user to verify |
| No write access to `/tmp` | Clone to the workspace directory instead |
| Tests fail after fix | Analyze failure output, revise the fix, and re-verify |
| Cannot determine root cause | Present findings so far and ask the user for guidance |
| Large / complex issue | Break the issue into sub-tasks, fix the most critical part first, and note remaining work |
| `git push` permission denied | Auto-fork the repository and push to fork |
| `gh pr create` fails | Show error details and provide manual command |
| User's `gh` not authenticated | Prompt user to run `gh auth login` first |
| Branch already exists on remote | Ask user whether to force-push or create a new branch name |
| PR already exists for this branch | Show existing PR URL and ask whether to update |
| No test framework found | Run static analysis with `get_problems`, verify manually, and note in PR |
| Issue contains multiple problems | Fix the most critical problem first; note remaining items as follow-up |
| Fix branch already exists | Ask user to reuse, recreate, or rename the branch |

---

## Notes

- **Local operations:** All code analysis and modification happens locally. Only standard Git and GitHub API operations (clone, push, PR creation) send data to GitHub.
- **Authentication:** Uses your existing `gh` CLI credentials. No additional credentials are stored.
- **User consent required:** The agent will not push code or create PRs without explicit user approval in Phase 7.
