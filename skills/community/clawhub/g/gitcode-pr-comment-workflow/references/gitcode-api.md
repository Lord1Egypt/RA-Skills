# GitCode API Reference

## Base URL

```
https://api.gitcode.com/api/v5
```

## Authentication

All requests require `access_token` as a query parameter:

```
?access_token=<token>
```

Token stored in MEMORY.md or provided by user at runtime.

## Issue APIs

### Get Issue

```
GET /repos/{owner}/{repo}/issues/{number}
```

### Get Issue Comments

```
GET /repos/{owner}/{repo}/issues/{number}/comments
```

### Create Issue Comment

```
POST /repos/{owner}/{repo}/issues/{number}/comments
```

Body:

```json
{
  "body": "<comment text>"
}
```

## Pull Request APIs

### Create Pull Request

```
POST /repos/{owner}/{repo}/pulls?access_token=<token>
```

**Required parameters:**

| Parameter | Type | Description |
|:---|:---|:---|
| `title` | string | PR title |
| `head` | string | Source branch. Cross-repo format: `username:branch` |
| `base` | string | Target branch (e.g., `master`) |

**Optional parameters:**

| Parameter | Type | Description |
|:---|:---|:---|
| `body` | string | PR description (markdown) |
| `fork_path` | string | Fork repo path `owner/repo`. **Required for cross-repo PRs** |
| `labels` | string | Comma-separated label names |
| `issue` | string | Issue ID to auto-fill title/body |
| `assignees` | string | Comma-separated reviewer usernames |
| `testers` | string | Comma-separated tester usernames |
| `prune_source_branch` | boolean | Delete source branch after merge (default: false) |
| `draft` | boolean | Create as draft (default: false) |
| `squash` | boolean | Squash merge (default: false) |
| `close_related_issue` | boolean | Close linked issues on merge |

**Cross-repo PR example (fork → upstream):**

```bash
curl -s -X POST "https://api.gitcode.com/api/v5/repos/Ascend/msinsight/pulls?access_token=<token>" \
  -H "Content-Type: application/json" \
  -d @payload.json
```

payload.json:

```json
{
  "title": "docs(readme): elevate contributing guide to standalone section",
  "body": "## 修改内容\n\n...\n\n### 关联 Issue\n\nfix #209",
  "head": "hummel_mao:doc_20260424_contributing_guide",
  "base": "master",
  "fork_path": "hummel_mao/msinsight"
}
```

**⚠️ Important notes:**
- For cross-repo PRs, `head` format must be `<fork_owner>:<branch_name>`
- `fork_path` is **required** for cross-repo PRs (fork → upstream)
- API endpoint uses `pulls` not `pull_requests`
- API base domain is `api.gitcode.com` not `gitcode.com`

### Get Pull Request

```
GET /repos/{owner}/{repo}/pulls/{number}
```

### List Pull Request Files

```
GET /repos/{owner}/{repo}/pulls/{number}/files
```

### Get Pull Request Diff

```
GET /repos/{owner}/{repo}/pulls/{number}/diff
```

Headers:

```
Authorization: Bearer <token>
```

Note: Diff endpoint uses `gitcode.com` not `api.gitcode.com`:

```
GET https://gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/diff
```

### Post PR Comment

```
POST /repos/{owner}/{repo}/pulls/{number}/comments
```

Body:

```json
{
  "body": "<comment text>",
  "commit_id": "<sha>",
  "path": "<file_path>",
  "position": <line_number>
}
```

### Get PR Comments (with discussion_id and resolved status)

```
GET /repos/{owner}/{repo}/pulls/{number}/comments?access_token=<token>
```

Response fields of interest:

| Field | Type | Description |
|:---|:---|:---|
| `id` | integer | Comment ID |
| `discussion_id` | string | Discussion thread ID (used for replying) |
| `body` | string | Comment content |
| `resolved` | boolean | Whether the comment is resolved |
| `user.login` | string | Comment author |
| `diff_position.start_new_line` | integer | Target line number |
| `reply` | array | Existing replies in the discussion |

### Reply to PR Comment

Reply to an existing PR review comment within its discussion thread.

```
POST /repos/{owner}/{repo}/pulls/{number}/discussions/{discussion_id}/comments?access_token=<token>
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|:---|:---|:---|:---|
| `owner` | string | yes | Repository owner (organization or user path) |
| `repo` | string | yes | Repository path |
| `number` | integer | yes | PR sequential number |
| `discussion_id` | string | yes | Discussion ID (obtained from GET comments response) |

**Query Parameters:**

| Parameter | Type | Required | Description |
|:---|:---|:---|:---|
| `access_token` | string | yes | User access token |

**Request Body (application/json):**

| Parameter | Type | Required | Description |
|:---|:---|:---|:---|
| `body` | string | yes | Reply content (supports markdown) |

**Response (200):**

```json
{
  "id": "<discussion_id>",
  "note_id": <note_id>,
  "body": "<reply text>"
}
```

**Example:**

```bash
# Write body to file to avoid encoding issues on Windows
echo '{"body": "暂不修改，后续单独处理。"}' > /tmp/reply_body.json

curl -s -X POST \
  "https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/discussions/{discussion_id}/comments?access_token=<token>" \
  -H "Content-Type: application/json" \
  -d @/tmp/reply_body.json
```

**⚠️ Notes:**
- The `discussion_id` can be obtained from the `GET /repos/{owner}/{repo}/pulls/{number}/comments` response's `discussion_id` field
- On Windows, write the JSON body to a file first and use `-d @file.json` to avoid encoding issues with Chinese characters
- This API replies within an existing discussion thread, keeping the conversation context

## gitcode CLI Quick Reference

**Source**: https://github.com/codeasier/gitcode-cli

**Command names:**
- `gitcode` — full name, works on all platforms (use on Windows)
- `gc` — short alias, works on macOS/Linux only

**Windows note:** On PowerShell, `gc` conflicts with `Get-Content`. Always use `gitcode` on Windows.

**Installation**: If `gitcode` command not found, install from https://github.com/codeasier/gitcode-cli

**PATH issue**: If `gitcode` not in PATH, ask user for the full executable path and use it directly. Use this full path for all gitcode commands in the session.

### Issue Commands

```bash
gc issue view <number> --repo <owner>/<repo>
gc issue view <number> --repo <owner>/<repo> --comments
gc issue list --repo <owner>/<repo> --state open
```

### PR Commands

```bash
# Create PR (current branch as head)
gitcode pr create -R <owner>/<repo> --title "..." --body "..."

# Create cross-repo PR (fork → upstream)
gitcode pr create -R <upstream_owner>/<repo> \
  --fork <fork_owner>/<repo> \
  --head <branch_name> \
  --base <target_branch> \
  --title "..." --body "..."

# Auto-fill from last commit
gitcode pr create -R <owner>/<repo> --fill

# Open in browser after creation
gitcode pr create -R <owner>/<repo> --title "..." --web
```

On macOS/Linux, `gc` can be used as a shorthand for `gitcode`.

### Repo Commands

```bash
gitcode repo view <owner>/<repo>
```

## PowerShell Notes

- Use `;` to chain commands (not `&&`)
- Use `curl.exe` (not `curl` which aliases to `Invoke-WebRequest`)
- For JSON payloads, write to file first then use `-d @file.json` to avoid escaping issues
- Remove temp files: `Remove-Item -Recurse -Force temp/`
