---
name: git-mender
description: "git-mender — Automatically fix GitHub issues end-to-end: reads the issue, analyzes repository code, implements a fix, and submits a pull request. Use when the user provides a GitHub issue URL, mentions fixing a GitHub issue, or uses the /fix-issue command. Supports URLs in the format https://github.com/{owner}/{repo}/issues/{number}."
version: "1.1.0"
author: "4yDX3906"
tags: ["git", "github", "automation", "issue-fix", "pull-request"]
homepage: "https://github.com/4yDX3906/git-mender"
metadata:
  clawdbot:
    emoji: "🔧"
requires:
  env: []
files: ["scripts/install.sh"]
---

# git-mender — Agent Skill

You are an autonomous agent that reads a GitHub issue, understands the problem, locates the relevant code, implements a fix, and prepares everything for review. Follow the phases below **in order**, using the checklist to track progress.

---

## Progress Checklist

Use this checklist to track your progress through the workflow:

- [ ] Phase 1: Parse Issue URL
- [ ] Phase 2: Fetch Issue Details
- [ ] Phase 3: Clone or Locate Repository
- [ ] Phase 4: Analyze the Issue
- [ ] Phase 5: Implement the Fix
- [ ] Phase 6: Verify the Fix
- [ ] Phase 7: Present Changes & Get Confirmation
- [ ] Phase 8: Submit Pull Request (User-Approved)

---

## Phase 1: Parse Issue URL

Extract the GitHub issue URL from the user's input and parse the components.

**Expected URL format:** `https://github.com/{owner}/{repo}/issues/{number}`

1. Scan the user message for a URL matching the pattern above.
2. Extract three values:
   - `owner` — the GitHub organization or user
   - `repo` — the repository name
   - `number` — the issue number
3. If no valid URL is found, ask the user to provide a valid GitHub issue URL.
4. Confirm the parsed values before proceeding:
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

Check if the repo exists locally in a common location:

```bash
ls -d ~/Desktop/{repo} ~/projects/{repo} ~/repos/{repo} /tmp/{repo} 2>/dev/null
```

If not found, clone it:

```bash
gh repo clone {owner}/{repo} /tmp/{repo}
```

If `gh` is not available:

```bash
git clone https://github.com/{owner}/{repo}.git /tmp/{repo}
```

Then inform the user about the clone location.

### Step 2.5: Change into the repository directory

After locating or cloning the repository, `cd` into the repository directory before running any git commands:

```bash
cd {repo_path}
```

### Step 3: Ensure correct branch

First, detect the default branch:

```bash
# Detect the default branch
default_branch=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||')
if [ -z "$default_branch" ]; then
  default_branch="main"
fi
```

Then check out the default branch and pull latest changes:

```bash
git checkout $default_branch
git pull --ff-only
```

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

Before writing any code, clearly state:

1. **Root cause:** Why the bug occurs.
2. **Affected code:** Which file(s) and function(s) need changes.
3. **Fix approach:** What the minimal change should be.

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
> Do you want to adopt these changes? If anything needs adjustment, let me know.

- If the user **approves**, proceed to Phase 8.
- If the user **requests changes**, revise the fix (return to Phase 5) and re-present.

---

## Phase 8: Submit Pull Request (User-Approved)

Only execute this phase after the user has confirmed the changes in Phase 7.

First, ask the user:
> Would you like me to automatically commit and submit a PR to the repository?

- If the user **declines**, show the suggested commit message and `gh pr create` command for manual execution (see Fallback below).
- If the user **agrees**, execute Steps 1–4 automatically.

### Step 1: Stage and Commit

```bash
git add -A
git commit -m "fix: {short description} (#{number})

{Detailed explanation of what was wrong and how this commit fixes it.}

Closes #{number}"
```

### Step 2: Check Push Permission & Handle Fork

Attempt to push to the origin repository:

```bash
git push origin fix/issue-{number}
```

- If the push **succeeds**, continue to Step 3 with `--head fix/issue-{number}`.
- If the push **fails** (permission denied / 403):
  1. Fork the repository:
     ```bash
     gh repo fork {owner}/{repo} --clone=false
     ```
  2. Detect your GitHub username:
     ```bash
     gh api user --jq '.login'
     ```
  3. Add fork as a remote:
     ```bash
     git remote add fork https://github.com/{your_username}/{repo}.git
     ```
  4. Push to the fork:
     ```bash
     git push fork fix/issue-{number}
     ```
  5. Continue to Step 3 with `--head {your_username}:fix/issue-{number}`.

### Step 3: Create Pull Request

```bash
gh pr create \
  --repo {owner}/{repo} \
  --title "fix: {short description}" \
  --body "## Summary

Fixes #{number}.

### Problem
{Brief problem description}

### Solution
{Brief solution description}

### Changes
- {change 1}
- {change 2}

### Testing
- [x] Existing tests pass
- [x] {Any additional verification performed}" \
  --base {default_branch} \
  --head {head_ref}
```

> `{head_ref}` is `fix/issue-{number}` for direct push or `{your_username}:fix/issue-{number}` for fork push.

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

---

## External Endpoints

This skill interacts with the following external services:

| Endpoint | Purpose | Data Sent |
|---|---|---|
| `github.com` | Clone repositories, fetch issue details, push branches, create PRs | Git operations, branch names, PR metadata |
| GitHub API (via `gh` CLI) | Read issues/comments, create PRs, fork repos, check auth | Issue number, repo owner/name, PR title/body |

No other external services are contacted. All code analysis and modification happens locally.

---

## Security and Privacy

- **Local operations**: All code reading, analysis, and modification happens on your local machine.
- **Data sent externally**: Only standard Git and GitHub API operations (clone, push, PR creation) send data to GitHub. No code is sent to third-party services.
- **Authentication**: Uses your existing `gh` CLI authentication. No additional credentials are stored or transmitted.
- **No telemetry**: This skill does not collect or transmit any usage data.

---

## Model Invocation

This skill is designed for autonomous execution within an AI coding assistant. When triggered, the agent will:

1. Parse the GitHub issue URL from user input
2. Fetch issue details via `gh` CLI or web scraping
3. Clone or locate the repository locally
4. Analyze the codebase to identify the root cause
5. Implement a minimal fix
6. Run tests and verification
7. Present changes for user review
8. Submit a PR only after explicit user approval

Steps 7 and 8 require explicit user confirmation before proceeding. The agent will not push code or create PRs without user consent.

---

## Trust Statement

By using this skill, you authorize the agent to:
- Read GitHub issue content from public or authenticated-accessible repositories
- Clone repositories to your local machine
- Make code modifications in a dedicated branch
- Push changes and create pull requests **only with your explicit approval**

All Git operations use your existing `gh` CLI credentials. Only install this skill if you trust the repositories you intend to use it with.
