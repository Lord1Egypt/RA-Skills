---
name: gitcode-issue-workflow
description: >
  End-to-end GitCode issue workflow covering issue pickup, analysis, code modification, and PR submission.
  Use when user asks to handle/fix/resolve a GitCode issue, or when working on issue-driven development
  for GitCode repositories. Triggers on phrases like "接取 issue", "处理 issue", "修复 issue", "fix issue",
  "handle issue", "resolve issue", "提交 PR", "create PR for issue". Requires gitcode CLI (GitCode CLI) and git.
  NOT for code review (use code-review skill), issue triage without code changes, or non-GitCode platforms.
---

# GitCode Issue Workflow

End-to-end workflow: Issue → Analysis → Code Fix → PR Submission.

## Prerequisites

- **gitcode CLI**: GitCode CLI (similar to GitHub's `gh`). Source: https://github.com/codeasier/gitcode-cli
- **git**: Standard git CLI
- **GitCode Token**: Stored in MEMORY.md or provided by user
- **Local repo**: User must confirm the local repository path

**CLI command name:**
- `gitcode` — full command name, works on all platforms (recommended on Windows)
- `gc` — short alias, works on macOS/Linux (conflicts with PowerShell `Get-Content` on Windows)

**gitcode CLI detection (follow this order):**
1. Try `gitcode --version` first (recommended, works everywhere)
2. If not found, try `gc --version` (macOS/Linux fallback)
3. If neither found, ask user for the full path to the executable
4. If not installed, prompt to install from https://github.com/codeasier/gitcode-cli

**gitcode CLI authentication check:**
After confirming the CLI is installed, try a lightweight command to verify authentication (e.g., `gitcode issue view 1 --repo <owner>/<repo>`). If it returns a token-related error like `Invalid header parameter: private-token, required`, the CLI is not authenticated.

**Stop and prompt the user to authenticate first**:
```bash
gitcode auth login
```
Or if they have a token, use `--with-token` (not `--token`):
```bash
echo <your_token> | gitcode auth login --with-token
```

**Windows note:** If the CLI outputs emoji characters and throws `UnicodeEncodeError: 'gbk' codec can't encode character`, set the Python IO encoding before running CLI commands:
```powershell
$env:PYTHONIOENCODING="utf-8"
gitcode issue view <number> --repo <owner>/<repo>
```

Do not proceed with the workflow until authentication is successful.

**Windows note:** On PowerShell, `gc` is an alias for `Get-Content`. Always use `gitcode` on Windows.

## 8-Step Workflow

### Step 1: Fetch & Read Issue

Fetch the issue using gitcode CLI:

```bash
gitcode issue view <number> --repo <owner>/<repo>
gitcode issue view <number> --repo <owner>/<repo> --comments
```

(`gc` can be used as shorthand on macOS/Linux, e.g., `gc issue view ...`)

**If the CLI returns an authentication error** (e.g., `Invalid header parameter: private-token, required`):
1. Check `gitcode auth status`
2. If not authenticated, **prompt the user to run `gitcode auth login`** and stop the workflow
3. If the user prefers not to use the CLI for authentication, fall back to the GitCode API with an explicit token:
   ```bash
   curl -s "https://api.gitcode.com/api/v5/repos/<owner>/<repo>/issues/<number>?access_token=<token>"
   curl -s "https://api.gitcode.com/api/v5/repos/<owner>/<repo>/issues/<number>/comments?access_token=<token>"
   ```

Parse and present to user:
- Issue title, state, author, assignees, labels
- Problem description (each numbered point)
- Comments from maintainers (especially assignment decisions and clarifications)

### Step 2: Understand & Challenge User's Modification Approach

**Must stop here before touching the local repository or planning concrete code edits.**

After reading and explaining the issue, ask the user for their intended modification approach. Then apply the essence of the `understand-me` workflow until the user explicitly confirms the approach.

Required conversation flow:

1. Restate the issue in your own words and identify the real problem to solve.
2. Ask the user for their modification approach if they have not provided one.
3. Convert the issue + user's approach into a **design decision tree**:
   - upstream decisions first: goal, scope, constraints, success criteria
   - downstream decisions later: target modules/files, implementation strategy, tests, rollout/PR scope
   - mark dependencies explicitly, e.g. `depends on: D1`
4. Ruthlessly but constructively interrogate the approach one branch at a time:
   - ask exactly **one question per turn**
   - for every question, provide **your recommended answer** and a short reason
   - do not bundle multiple questions
   - do not proceed while a dependency blocker is unresolved
5. If an answer can be found in the issue body, issue comments, linked docs, or repository files already fetched/read, search/read those materials first instead of asking the user.
6. After each user answer, update the decision tree delta and ask the next highest-leverage single question.
7. Continue until the user explicitly confirms the modification approach (e.g. “确认”, “yes”, “按这个思路改”).

Suggested response shape during this step:

```markdown
## 我的理解
<issue + approach summary>

## 设计决策树（当前版本）
- D1: <goal/scope>
  - A: ...
  - B: ...
- D2: <implementation direction>
  - depends on: D1
  - A: ...
  - B: ...

## 当前要拷问的问题
<one question only>

**我的推荐答案：** <recommended answer>
**推荐理由：** <brief reason>
```

**Do not move to Step 3 until the approach is confirmed.**

### Step 3: Generate Design Document

**Must generate a design document after the user confirms the modification approach and before any code modification.**

Create a Markdown design document under `temp/` first, for example:

```text
temp/issue-<number>-design.md
```

The design document must include:

1. **Issue summary**: title, link, key requirements, maintainer comments.
2. **Confirmed modification approach**: the final user-confirmed direction from Step 2.
3. **Design decision tree**: resolved decisions, rejected branches, and remaining assumptions.
4. **Affected scope**: expected modules/files/components to inspect or modify.
5. **Implementation plan**: ordered, minimal change steps.
6. **Compatibility and risk analysis**: behavior changes, edge cases, migration concerns.
7. **Validation plan**: tests, commands, manual checks, screenshots if needed.
8. **Non-goals**: explicitly list what will not be changed in this PR.

After writing the document:

1. Show the design document path and a concise summary to the user.
2. Ask the user to confirm the design document.
3. If the user requests changes, revise the document and ask again.
4. Do not inspect/modify target code for implementation beyond what is necessary to draft the design unless the user confirms.

**Do not move to Step 4 until the design document is confirmed.**

### Step 4: Confirm Local Repository

**Must confirm with user before proceeding:**

1. Ask user for the local repository path (or confirm if already known)
2. Verify the repo exists and is on the correct branch:

```bash
cd <repo_path>
git status
git log --oneline -3
```

3. Pull latest code from the target branch (usually `master`):

```bash
git pull <remote> <branch>
```

**⚠️ Constraints:**
- Never assume the local repo path — always confirm with user
- Verify working tree is clean before starting work
- Identify which remote is `upstream` (the target org repo) vs personal fork

### Step 5: Read & Analyze Target Files

Read the files that need modification based on the issue description:

```bash
# Use read tool to examine the file contents
read <file_path>
```

**Analysis requirements:**
- Understand the current structure and content of files to be modified
- Cross-reference with issue requirements and maintainer comments
- Identify the minimal change set needed

### Step 6: Propose Changes

**⚠️ Must get user approval before modifying any files.**

Present to the user:
1. **Modification target**: Which file(s) will be changed
2. **Modification approach**: What will be changed and why
3. **Expected diff**: Show the before/after comparison in diff format

```diff
- old content
+ new content
```

4. **Rationale**: How this addresses the issue requirements

**Wait for user confirmation before proceeding to Step 7.**

If user requests adjustments, revise the proposal and re-present.

### Step 7: Apply Changes

After user approval, apply the changes:

```bash
# Edit the file using edit tool
edit <file_path> oldText -> newText
```

Verify the changes:

```bash
cd <repo_path>
git diff <file>
```

Show the diff output to user for final confirmation.

### Step 8: Create Branch, Commit & Submit PR

This step involves multiple sub-steps. Follow them in strict order.

#### 8.1 Create Branch

Branch naming format: `[type]_[YYYYMMDD]_[brief_description]`

- **type**: `doc`, `fix`, `feat`, `refactor`, `test`, `chore`, etc.
- **date**: Current date in YYYYMMDD format
- **description**: 1-2 English words separated by underscores

```bash
cd <repo_path>
git checkout -b <branch_name>
```

Examples:
- `doc_20260424_contributing_guide`
- `fix_20260424_null_check`
- `feat_20260424_export_csv`

#### 8.2 Commit

Commit message format: `[type]([module]): [detailed description]`

```bash
git add <changed_files>
git commit -m "<type>(<module>): <description>"
```

Examples:
- `docs(readme): elevate contributing guide to standalone section`
- `fix(parser): add null check for empty input`
- `feat(export): add CSV export support`

#### 8.3 Push to Personal Fork

**⚠️ Critical constraints:**
- **Must ask user which remote to push to** — never assume
- **Never push directly to the upstream/organization repository**
- List available remotes for user to choose:

```bash
git remote -v
```

Then push:

```bash
git push <personal_remote> <branch_name>
```

#### 8.4 Create PR (Merge Request)

**Method 1: gitcode CLI (preferred)**

```bash
gitcode pr create -R <upstream_owner>/<repo> \
  --fork <personal_owner>/<repo> \
  --head <branch_name> \
  --base <target_branch> \
  --title "<commit_message>" \
  --body "<pr_description>"
```

On macOS/Linux, `gc` is a valid shorthand: `gc pr create ...`

**⚠️ Must ask user for the target branch** (e.g., `master`, `main`, `develop`) if not already known. Do not assume.

PR body template:

```markdown
## PR描述 (What this PR does / why we need it?)

<!--
- 请明确说明您提交PR的变更内容。本部分旨在概述所做的变更，以及此PR是如何解决该问题的。请尽可能地提供有助于评审人员更高效、更快速完成检视审查的实用说明。
- 请说明为何需要这些更改，例如具体的使用场景或bug描述。
- 关联issue号(如果有)

- Please clarify what changes you are proposing. The purpose of this section is to outline the changes and how this PR fixes the issue.
If possible, please consider writing useful notes for better and faster reviews in your PR.
- Please clarify why the changes are needed. For instance, the use case and bug description.
- Fixes [#<issue-number>](https://gitcode.com/<upstream_owner>/<repo>/issues/<issue-number>)
-->

## 面向用户的变更 (Does this PR introduce _any_ user-facing change)?
<!--
请注意，这里指的是**任何**面向用户的变更，包括但不限于API、用户界面或其他使用方式上的变更。
Note that it means *any* user-facing change including all aspects such as API, interface or other behavior changes.
-->

## 功能验证 (How was this patch tested?)
<!--
请确认CI已通过增量及存量的单元测试用例。
如果本次测试方式与常规单元测试不同，请详细说明您的测试步骤(最好提供完整的可复现的操作路径及关键截图)，以便Committer能够快速复现验证，也便于后续的维护。
如果未添加测试，请说明未添加的原因，以及为何难添加测试。

- [_] 功能自验
- [_] 本地自验截图(涉及个人标识符等敏感信息请注意脱敏)
- [_] 新增/变更内容是否已新增/适配UT测试用例看护

CI passed with new added/existing test.
If it was tested in a way different from regular unit tests, please clarify how you tested step by step, ideally copy and paste-able, so that other reviewers can test and check, and descendants can verify in the future.
If tests were not added, please describe why they were not added and/or why it was difficult to add.

- [_] Self-verification of the feature.
- [_] Screenshot of local self-verification (please anonymize any sensitive information such as personal identifiers)
- [_] Have new or modified unit test (UT) cases been added or adapted to cover the newly added or changed content?
-->
```

**Method 2: GitCode API (fallback if gc CLI fails)**

See [references/gitcode-api.md](references/gitcode-api.md) for the API endpoint and parameters.

```bash
curl -s -X POST "https://api.gitcode.com/api/v5/repos/<owner>/<repo>/pulls?access_token=<token>" \
  -H "Content-Type: application/json" \
  -d @<payload_file>
```

Payload structure:

```json
{
  "title": "<PR title>",
  "body": "<PR description>",
  "head": "<fork_owner>:<branch_name>",
  "base": "<target_branch>",
  "fork_path": "<fork_owner>/<repo>"
}
```

**Method 3: Manual (last resort)**

If both gc CLI and API fail, provide the user with the manual creation URL:

```
https://gitcode.com/<fork_owner>/<repo>/merge_requests/new?source_branch=<branch_name>
```

And the PR description text for them to paste.

#### 8.5 Confirm & Report

After PR creation, present a summary:

| Item | Value |
|:---|:---|
| PR URL | `<link>` |
| PR Number | `#<number>` |
| Source | `<fork_owner>/<repo>:<branch>` |
| Target | `<upstream_owner>/<repo>:<base_branch>` |
| Linked Issue | `#<issue_number>` |
| Status | Opened |

## Key Constraints

### Safety Rules

1. **Never push to upstream/organization repos directly** — always use personal fork
2. **Never modify files without user approval** — always show proposed changes first
3. **Never assume repository paths** — always confirm with user
4. **Never assume target branch** — always ask if unknown
5. **Never assume push remote** — always list remotes and ask user to choose
6. **All external write operations require explicit user confirmation**

### Git Workflow Rules

1. Working tree must be clean before creating a new branch
2. Branch must be created from the latest target branch code
3. Commit messages must follow the format: `[type]([module]): [description]`
4. Branch names must follow the format: `[type]_[YYYYMMDD]_[brief_description]`
5. Always verify changes with `git diff` before committing

### Asking vs Doing

| Action | Ask First? |
|:---|:---|
| Read files, check git status | ❌ Just do it |
| Fetch issue details | ❌ Just do it |
| Propose changes | ❌ Present proposal |
| Modify files | ✅ Wait for approval |
| Push to remote | ✅ Ask which remote |
| Create PR | ✅ Ask target branch if unknown |
| Post issue comments | ✅ Always confirm |

## Temp File Management

All temporary files generated during the workflow must be stored in `temp/` directory under the workspace:

```
workspace/temp/
├── *.md          # Downloaded files for review
├── *.json        # API payloads
└── *             # Other temp files
```

**⚠️ Clean up `temp/` directory after workflow completion:**

```bash
Remove-Item -Recurse -Force temp/  # Windows
rm -rf temp/                        # Linux/macOS
```
