---
name: gitcode-pr-comment-workflow
description: >
  GitCode PR review comment response workflow. Accepts a PR link, fetches review comments from the PR,
  checks out the PR's source branch locally, proposes modification plans based on review feedback,
  applies changes after user confirmation, and commits/pushes back to the source branch.
  Triggers on phrases like "根据 review 修改 PR", "处理 PR 审查意见", "fix PR review comments",
  "PR review workflow", "按检视意见修改", "review comment workflow".
  Requires gitcode CLI and git. NOT for creating new PRs (use gitcode-issue-workflow) or
  initiating code reviews (use code-review skill).
---

# GitCode PR Comment Workflow

Workflow: **PR Link → Fetch Review Comments → Understand User Approach → Design Document → Checkout Source Branch → Propose Changes → User Confirm → Apply & Push → Reply Unaddressed Comments**

## Prerequisites

- **gitcode CLI**: GitCode CLI. Source: https://github.com/codeasier/gitcode-cli
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
After confirming the CLI is installed, try a lightweight command to verify authentication (e.g., `gitcode pr view <number> --repo <owner>/<repo>`). If it returns a token-related error, the CLI is not authenticated.

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
gitcode pr view <number> --repo <owner>/<repo>
```

Do not proceed with the workflow until authentication is successful.

**Windows note:** On PowerShell, `gc` is an alias for `Get-Content`. Always use `gitcode` on Windows.

## 9-Step Workflow

### Step 1: Parse PR Link & Fetch Info

Accept a PR URL from the user. The URL format is:

```
https://gitcode.com/<owner>/<repo>/pulls/<number>
```

**Parse from the URL:**
- `owner`: Repository owner
- `repo`: Repository name
- `number`: PR number

Fetch PR details:

```bash
gitcode pr view <number> --repo <owner>/<repo>
```

**Key info to extract:**
- PR title and description
- **Source branch** (`head`): the branch being merged from
- **Target branch** (`base`): the branch being merged into
- **Source repo/fork**: which repo the source branch is from (may be a fork)
- PR state (open/closed/merged)

**⚠️ If the PR is closed or already merged, warn the user and stop.**

### Step 2: Fetch Review Comments

Fetch comments on the PR to identify review feedback:

```bash
gitcode pr view <number> --repo <owner>/<repo> --comments
```

Or use the GitCode API:

```bash
curl.exe -s "https://api.gitcode.com/api/v5/repos/<owner>/<repo>/pulls/<number>/comments?access_token=<token>"
```

**Parse and categorize comments:**

- **Review comments**: Comments that contain critique, suggestions, or requested changes (look for keywords like "建议", "建议修改", "需要", "请修改", "review", "nit", "concern", "TODO", "FIXME", or inline file-level comments)
- **General comments**: Conversational comments, approvals ("LGTM"), or status updates

**Present to user:**
1. Extract all review comments (the ones requesting changes)
2. For each review comment, show:
   - Author and timestamp
   - File path and line reference (if inline comment)
   - Comment content
3. Summarize: total review comments found, how many require code changes

Save review comments to `temp/pr_review_comments.json` for reference:

```json
{
  "pr": {
    "owner": "<owner>",
    "repo": "<repo>",
    "number": <number>,
    "source_branch": "<head_branch>",
    "target_branch": "<base_branch>",
    "source_repo": "<fork_owner>/<repo>"
  },
  "review_comments": [
    {
      "id": <comment_id>,
      "author": "<username>",
      "created_at": "<timestamp>",
      "path": "<file_path_or_null>",
      "line": <line_number_or_null>,
      "body": "<comment_text>",
      "requires_code_change": true
    }
  ]
}
```

### Step 3: Understand & Challenge User's Modification Approach

If no review comments require code changes, summarize the comments and ask whether the user wants any non-code response; do not enter the modification workflow.

If one or more review comments require code changes, **must stop here before checkout, file editing, or concrete implementation planning.** Ask the user for their intended modification approach, then apply the essence of the `understand-me` workflow until the user explicitly confirms the approach.

Required conversation flow:

1. Restate the PR context and review comments in your own words.
2. Identify which comments require code changes and which are informational/nits.
3. Ask the user for their modification approach if they have not provided one.
4. Convert the PR comments + user's approach into a **design decision tree**:
   - upstream decisions first: review intent, desired behavior, scope, compatibility, success criteria
   - downstream decisions later: target modules/files, implementation strategy, tests, commit/push scope
   - mark dependencies explicitly, e.g. `depends on: D1`
5. Ruthlessly but constructively interrogate the approach one branch at a time:
   - ask exactly **one question per turn**
   - for every question, provide **your recommended answer** and a short reason
   - do not bundle multiple questions
   - do not proceed while a dependency blocker is unresolved
6. If an answer can be found in the PR description, review comments, linked docs, or repository files already fetched/read, search/read those materials first instead of asking the user.
7. After each user answer, update the decision tree delta and ask the next highest-leverage single question.
8. Continue until the user explicitly confirms the modification approach (e.g. “确认”, “yes”, “按这个思路改”).

Suggested response shape during this step:

```markdown
## 我的理解
<PR context + review comment summary + user's approach>

## 设计决策树（当前版本）
- D1: <review intent/scope>
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

**Do not move to Step 4 until the approach is confirmed.**

### Step 4: Generate Design Document

**Must generate a design document after the user confirms the modification approach and before any code modification.**

Create a Markdown design document under `temp/` first, for example:

```text
temp/pr-<number>-review-comment-design.md
```

The design document must include:

1. **PR summary**: title, link, source/target branches, current intent.
2. **Review comment summary**: comments requiring code changes, comments not requiring code changes, file/line references.
3. **Confirmed modification approach**: the final user-confirmed direction from Step 3.
4. **Design decision tree**: resolved decisions, rejected branches, and remaining assumptions.
5. **Affected scope**: expected modules/files/components to inspect or modify.
6. **Implementation plan**: ordered, minimal change steps.
7. **Compatibility and risk analysis**: behavior changes, edge cases, regression risk.
8. **Validation plan**: tests, commands, manual checks, screenshots if needed.
9. **Non-goals**: explicitly list what will not be changed in this PR update.

After writing the document:

1. Show the design document path and a concise summary to the user.
2. Ask the user to confirm the design document.
3. If the user requests changes, revise the document and ask again.
4. Do not inspect/modify target code for implementation beyond what is necessary to draft the design unless the user confirms.

**Do not move to Step 5 until the design document is confirmed.**

### Step 5: Confirm Local Repository & Checkout Source Branch

**Must confirm with user before proceeding:**

1. Ask user for the local repository path (or confirm if already known)
2. Verify the repo exists:

```bash
cd <repo_path>
git status
git log --oneline -3
```

3. **Add the source repo as a remote** (if it's a fork and not already added):

```bash
# Check if remote already exists
git remote -v

# Add remote for the source fork if needed
git remote add <source_remote_name> <source_repo_url>
# or if it already exists, just fetch
git fetch <source_remote_name>
```

4. **Checkout the PR's source branch:**

```bash
# Create/check out the local tracking branch
git checkout -b <local_branch_name> <source_remote_name>/<source_branch>
# Or if already exists locally:
git checkout <local_branch_name>
git pull <source_remote_name> <source_branch>
```

**⚠️ Important:**
- If the working tree is dirty, **stash first** (`git stash`) and warn the user
- Pull latest from the source branch to ensure we're on the current code
- Verify the branch is correct: `git log --oneline -3` should show PR-related commits

5. Pull latest code to ensure we're up to date:

```bash
git pull <source_remote_name> <source_branch>
```

### Step 6: Read Files & Propose Changes

For each review comment that requires code changes:

1. **Read the relevant file(s)** using the `read` tool
2. **Locate the problematic code** referenced by the comment
3. **Propose a modification plan**

**Present the modification plan to the user:**

For each review comment:

```
## 检视意见 #N

**Reviewer**: <author>
**文件**: <file_path>
**行号**: L<line>
**意见**: <original comment text>

### 修改方案

**修改文件**: <file_path>
**修改位置**: L<start>-L<end>
**修改方式**: <description of the change>

```diff
- <old code>
+ <new code>
```

**理由**: <explanation of how this addresses the review comment>
```

**Group related changes** if multiple comments affect the same file.

**Wait for user confirmation before proceeding.** If the user requests adjustments, revise the plan and re-present.

**⚠️ External write constraint:** All file modifications require explicit user approval. Show the complete plan first, then ask: "是否确认按以上方案进行修改？(yes/no)"
```

### Step 7: Apply Changes

After user approval:

1. Apply each change using the `edit` tool:

```bash
# Use edit tool for precise replacements
edit <file_path> oldText -> newText
```

2. **Verify changes:**

```bash
cd <repo_path>
git diff
```

3. Show the complete diff to the user for final confirmation before committing.

### Step 8: Commit & Push to Source Branch

#### 8.1 Commit

Commit message format: `[type]([module]): address review comments`

Use a descriptive type:
- `fix`: Bug fixes from review
- `refactor`: Code structure improvements
- `style`: Formatting/style changes
- `docs`: Documentation updates

```bash
git add <changed_files>
git commit -m "<type>(<module>): address review comments on PR #<number>"
```

For multiple distinct changes, consider separate commits per logical change.

#### 8.2 Push

**⚠️ Must confirm the push remote with the user.**

```bash
# Show available remotes
git remote -v

# Push to the source branch
git push <source_remote_name> HEAD:<source_branch>
```

**Important:**
- Push to the **same branch** that the PR is based on
- If the user's fork is the source, push to their fork remote
- If the user has write access to the upstream repo, they may push directly

#### 8.3 Confirm & Report

After push, present a summary:

| Item | Value |
|:---|:---|
| PR URL | `https://gitcode.com/<owner>/<repo>/pulls/<number>` |
| PR Number | `#<number>` |
| Source Branch | `<source_branch>` |
| Target Branch | `<target_branch>` |
| Files Changed | `<count>` |
| Review Comments Addressed | `<count>` |
| Status | Changes pushed |

Optionally, post a comment on the PR acknowledging the review and confirming changes:

```markdown
感谢审查！已根据检视意见修改并推送到源分支。

修改内容：
- <summary of change 1>
- <summary of change 2>
```

**⚠️ Posting PR comments requires user confirmation before executing.**

### Step 9: Reply to Unaddressed Review Comments

After pushing code changes, identify review comments that were **not addressed** in this round (skipped, deferred, or out of scope) and reply to them on the PR to close the loop.

#### 9.1 Identify Unaddressed Comments

From the review comments collected in Step 2, identify comments that:
- Were **not modified** in the code changes (Steps 6-7)
- Were **not already resolved/closed** by the reviewer
- Were **not already replied to** by the PR author

Cross-reference with the design document's "Non-goals" section and the user's confirmed modification scope.

#### 9.2 Ask User for Confirmation

Present the list of unaddressed comments to the user:

```
## 未修改的检视意见

| # | 严重度 | 文件 | 意见摘要 | 建议回复 |
|---|--------|------|----------|----------|
| 8 | 建议 | interface.ts | status 移除 \| string | 暂不修改，后续单独处理 |
| 14 | 建议 | KernelE2ETimeTable.tsx | rowClassName 性能优化 | 暂不修改，建议级优化后续单独处理 |
| ... | ... | ... | ... | ... |

是否需要回复这些检视意见？
```

**Ask the user:**
1. Whether to reply to unaddressed comments
2. If yes, whether to use the suggested replies or customize them
3. For each comment, the user may provide a different reply text

**⚠️ Must get user confirmation before posting any replies.**

#### 9.3 Reply via GitCode API

Use the Reply to PR Comment API to post replies within each comment's discussion thread.

**Get the access token** from gitcode CLI config:

```bash
TOKEN=$(python -c "from gitcode_cli.config import get_token; print(get_token())")
```

**Reply to a comment** using its `discussion_id` (obtained from Step 2's API response):

```bash
# Write body to file to avoid encoding issues on Windows
echo '{"body": "<reply text>"}' > /tmp/reply_body.json

curl -s -X POST \
  "https://api.gitcode.com/api/v5/repos/<owner>/<repo>/pulls/<number>/discussions/<discussion_id>/comments?access_token=${TOKEN}" \
  -H "Content-Type: application/json" \
  -d @/tmp/reply_body.json
```

**Batch reply example** (same reply for multiple comments):

```bash
TOKEN=$(python -c "from gitcode_cli.config import get_token; print(get_token())")
echo '{"body": "暂不修改，建议级优化后续单独处理。"}' > /tmp/reply_body.json

for did in "<discussion_id_1>" "<discussion_id_2>" "<discussion_id_3>"; do
  curl -s -X POST \
    "https://api.gitcode.com/api/v5/repos/<owner>/<repo>/pulls/<number>/discussions/${did}/comments?access_token=${TOKEN}" \
    -H "Content-Type: application/json" \
    -d @/tmp/reply_body.json
done
```

**⚠️ Notes:**
- The `discussion_id` comes from the `GET /repos/{owner}/{repo}/pulls/{number}/comments` API response's `discussion_id` field
- On Windows, always write JSON body to a file first and use `-d @file.json` to avoid encoding issues with non-ASCII characters
- Each reply is posted within the existing discussion thread, keeping the conversation context
- Clean up temp files after replying: `rm -f /tmp/reply_body.json`

#### 9.4 Confirm & Report

After replying, present a summary:

| # | 检视意见 | discussion_id | 回复内容 | note_id |
|---|----------|---------------|----------|---------|
| 8 | status \| string | `92909e71...` | 暂不修改，后续单独处理 | 173582636 |
| ... | ... | ... | ... | ... |

Total: **N** unaddressed comments replied.

## Key Constraints

### Safety Rules

1. **Never push to the wrong branch** — always verify the source branch before pushing
2. **Never modify files without user approval** — always show proposed changes first
3. **Never assume repository paths** — always confirm with user
4. **Never assume push remote** — always list remotes and ask user to choose
5. **All external write operations require explicit user confirmation**

### Git Workflow Rules

1. Always pull latest from source branch before making changes
2. Stash dirty working trees before checking out
3. Commit messages must be descriptive and reference the PR number
4. Always verify changes with `git diff` before committing

### Asking vs Doing

| Action | Ask First? |
|:---|:---|
| Parse PR URL, fetch PR info | ❌ Just do it |
| Fetch review comments | ❌ Just do it |
| Confirm local repo path | ✅ Must confirm |
| Checkout source branch | ✅ Confirm branch name |
| Ask/challenge modification approach | ✅ Required if comments need code changes |
| Generate design document | ✅ Required before code modification |
| Confirm design document | ✅ Required before code modification |
| Read files, analyze code | ❌ Just do it after design confirmation |
| Propose changes | ❌ Present plan |
| Modify files | ✅ Wait for approval |
| Commit changes | ✅ Show commit message |
| Push to remote | ✅ Confirm remote and branch |
| Post PR comment | ✅ Always confirm |
| Reply to unaddressed review comments | ✅ Always confirm |

## Temp File Management

All temporary files generated during the workflow must be stored in `temp/` directory under the workspace:

```
workspace/temp/
├── pr_review_comments.json              # Downloaded review comments
├── pr-<number>-review-comment-design.md # Confirmed design document
├── *.md                                 # Review notes
└── *                                    # Other temp files
```

**⚠️ Clean up `temp/` directory after workflow completion:**

```bash
Remove-Item -Recurse -Force temp/  # Windows
rm -rf temp/                        # Linux/macOS
```

## GitCode API Reference (PR Comments)

See [references/gitcode-api.md](references/gitcode-api.md) for full API reference.

### Get PR Comments

```
GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/comments?access_token=<token>
```

### Post PR Comment

```
POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/comments?access_token=<token>
```

Body:

```json
{
  "body": "<comment text (markdown)>",
  "commit_id": "<commit_sha>",
  "path": "<file_path>",
  "position": <line_number>
}
```

### Get PR Diff

```
GET https://gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/diff
```

Headers:

```
Authorization: Bearer <token>
```

Note: Diff endpoint uses `gitcode.com` not `api.gitcode.com`.

### Reply to PR Comment

Reply to an existing PR review comment within its discussion thread.

```
POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/discussions/{discussion_id}/comments?access_token=<token>
```

Body:

```json
{
  "body": "<reply text (markdown)>"
}
```

The `discussion_id` is obtained from the `GET /repos/{owner}/{repo}/pulls/{number}/comments` response's `discussion_id` field.

## PowerShell Notes

- Use `;` to chain commands (not `&&`)
- Use `curl.exe` (not `curl` which aliases to `Invoke-WebRequest`)
- For JSON payloads, write to file first then use `-d @file.json` to avoid escaping issues
- Remove temp files: `Remove-Item -Recurse -Force temp/`