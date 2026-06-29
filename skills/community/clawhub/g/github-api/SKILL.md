---
name: github
description: |
  GitHub API integration with managed OAuth. Access repositories, issues, pull requests, commits, branches, and users.
  Use this skill when users want to interact with GitHub repositories, manage issues and PRs, search code, or automate workflows.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# GitHub

Access the GitHub REST API with managed OAuth authentication. Manage repositories, issues, pull requests, commits, branches, users, and more.

## Quick Start

**CLI:**

```bash
maton github repo list --sort updated
```

```bash
maton api '/github/user/repos?sort=updated&per_page=10'
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/github/user/repos?sort=updated&per_page=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/github/{native-api-path}
```

Maton proxies requests to `api.github.com` and automatically injects your OAuth token.

## Installation

**NPM:**
```bash
npm install -g @maton/cli
```

**Homebrew:**
```bash
brew install maton-ai/cli/maton
```

## Authentication

**CLI:**

```bash
maton login                          # Opens browser for API key
maton login --interactive            # Skip browser, paste API key directly
maton whoami                         # Show current auth state
```

**Manual:**

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key
4. Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

## Connection Management

Manage your GitHub OAuth connections at `https://api.maton.ai`.

### List Connections

**CLI:**

```bash
maton connection list github --status ACTIVE
```

```bash
maton api -X GET /connections -f app=github -f status=ACTIVE
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=github&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

**CLI:**

```bash
maton connection create github
```

```bash
maton api /connections -f app=github
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'github'}).encode()
req = urllib.request.Request('https://api.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

**CLI:**

```bash
maton connection view {connection_id}
```

```bash
maton api /connections/{connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

**CLI:**

```bash
maton connection delete {connection_id}
```

```bash
maton api -X DELETE /connections/{connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple GitHub connections, specify which one to use:

**CLI:**

```bash
maton github user --connection {connection_id}
```

```bash
maton api /github/user --connection {connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/github/user')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always specify the connection to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to repositories, issues, pull requests, commits, branches, and users within the connected GitHub account.
- **All write operations require explicit user approval.** Before executing any create, update, or delete call:
  1. Confirm the exact target (owner/repo, issue number, branch name) with the user.
  2. Verify the correct connection ID when multiple connections exist.
  3. State whether the action is reversible or destructive.
- **Irreversible / high-risk operations** (require extra caution):
  - Deleting repositories, branches, or releases
  - Force-pushing or rewriting history
  - Merging pull requests (cannot be unmerged)
  - Removing collaborators or transferring ownership
- **Scope boundaries:**
  - Only operate on repositories the user explicitly names. Never enumerate or modify repositories outside the current task context.
  - Organization-level actions (creating repos, managing members) require the user to confirm the target organization.
  - Do not request or use OAuth scopes beyond what the current task requires.

## API Reference

### Users

#### Get Authenticated User

```bash
GET /github/user
```

Example:

```bash
maton github whoami
```

#### Get User by Username

```bash
GET /github/users/{username}
```

#### List Users

```bash
GET /github/users?since={user_id}&per_page=30
```

### Repositories

#### List User Repositories

```bash
GET /github/user/repos?per_page=30&sort=updated
```

Query parameters: `type` (all, owner, public, private, member), `sort` (created, updated, pushed, full_name), `direction` (asc, desc), `per_page`, `page`

Example:

```bash
maton github repo list --sort updated
```

#### List Organization Repositories

```bash
GET /github/orgs/{org}/repos?per_page=30
```

Example:

```bash
maton github repo list {org}
```

#### Get Repository

```bash
GET /github/repos/{owner}/{repo}
```

Example:

```bash
maton github repo view --repo {owner}/{repo}
```

#### Create Repository (User)

```bash
POST /github/user/repos
Content-Type: application/json

{
  "name": "my-new-repo",
  "description": "A new repository",
  "private": true,
  "auto_init": true
}
```

Example:

```bash
maton github repo create my-new-repo --description "A new repository" --visibility private
```

#### Create Repository (Organization)

```bash
POST /github/orgs/{org}/repos
Content-Type: application/json

{
  "name": "my-new-repo",
  "description": "A new repository",
  "private": true
}
```

Example:

```bash
maton github repo create {org}/my-new-repo --visibility private
```

#### Update Repository

```bash
PATCH /github/repos/{owner}/{repo}
Content-Type: application/json

{
  "description": "Updated description",
  "has_issues": true,
  "has_wiki": false
}
```

Example:

```bash
maton github repo edit --repo {owner}/{repo} --description "Updated description" --enable-issues --enable-wiki=false
```

### Repository Contents

#### List Contents

```bash
GET /github/repos/{owner}/{repo}/contents/{path}
```

#### Get File Contents

```bash
GET /github/repos/{owner}/{repo}/contents/{path}?ref={branch}
```

#### Create or Update File

```bash
PUT /github/repos/{owner}/{repo}/contents/{path}
Content-Type: application/json

{
  "message": "Create new file",
  "content": "SGVsbG8gV29ybGQh",
  "branch": "main"
}
```

Note: `content` must be Base64 encoded.

#### Delete File

```bash
DELETE /github/repos/{owner}/{repo}/contents/{path}
Content-Type: application/json

{
  "message": "Delete file",
  "sha": "{file_sha}",
  "branch": "main"
}
```

### Branches

#### List Branches

```bash
GET /github/repos/{owner}/{repo}/branches?per_page=30
```

#### Get Branch

```bash
GET /github/repos/{owner}/{repo}/branches/{branch}
```

#### Rename Branch

```bash
POST /github/repos/{owner}/{repo}/branches/{branch}/rename
Content-Type: application/json

{
  "new_name": "new-branch-name"
}
```

#### Merge Branches

```bash
POST /github/repos/{owner}/{repo}/merges
Content-Type: application/json

{
  "base": "main",
  "head": "feature-branch",
  "commit_message": "Merge feature branch"
}
```

### Commits

#### List Commits

```bash
GET /github/repos/{owner}/{repo}/commits?per_page=30
```

Query parameters: `sha` (branch name or commit SHA), `path` (file path), `author`, `committer`, `since`, `until`, `per_page`, `page`

#### Get Commit

```bash
GET /github/repos/{owner}/{repo}/commits/{ref}
```

#### Compare Two Commits

```bash
GET /github/repos/{owner}/{repo}/compare/{base}...{head}
```

### Issues

#### List Repository Issues

```bash
GET /github/repos/{owner}/{repo}/issues?state=open&per_page=30
```

Query parameters: `state` (open, closed, all), `labels`, `assignee`, `creator`, `mentioned`, `sort`, `direction`, `since`, `per_page`, `page`

Example:

```bash
maton github issue list --repo {owner}/{repo} --state open
```

#### Get Issue

```bash
GET /github/repos/{owner}/{repo}/issues/{issue_number}
```

Example:

```bash
maton github issue view {issue_number} --repo {owner}/{repo}
```

#### Create Issue

```bash
POST /github/repos/{owner}/{repo}/issues
Content-Type: application/json

{
  "title": "Found a bug",
  "body": "Bug description here",
  "labels": ["bug"],
  "assignees": ["username"]
}
```

Example:

```bash
maton github issue create --repo {owner}/{repo} --title "Found a bug" --body "Bug description here" --label bug --assignee username
```

#### Update Issue

```bash
PATCH /github/repos/{owner}/{repo}/issues/{issue_number}
Content-Type: application/json

{
  "state": "closed",
  "state_reason": "completed"
}
```

Example:

```bash
maton github issue close {issue_number} --repo {owner}/{repo} --reason completed
```

#### Lock Issue

```bash
PUT /github/repos/{owner}/{repo}/issues/{issue_number}/lock
Content-Type: application/json

{
  "lock_reason": "resolved"
}
```

Example:

```bash
maton github issue lock {issue_number} --repo {owner}/{repo} --reason resolved
```

#### Unlock Issue

```bash
DELETE /github/repos/{owner}/{repo}/issues/{issue_number}/lock
```

Example:

```bash
maton github issue unlock {issue_number} --repo {owner}/{repo}
```

### Issue Comments

#### List Issue Comments

```bash
GET /github/repos/{owner}/{repo}/issues/{issue_number}/comments?per_page=30
```

Example:

```bash
maton github issue view {issue_number} --repo {owner}/{repo} --comments
```

#### Create Issue Comment

```bash
POST /github/repos/{owner}/{repo}/issues/{issue_number}/comments
Content-Type: application/json

{
  "body": "This is a comment"
}
```

Example:

```bash
maton github issue comment {issue_number} --repo {owner}/{repo} --body "This is a comment"
```

#### Update Issue Comment

```bash
PATCH /github/repos/{owner}/{repo}/issues/comments/{comment_id}
Content-Type: application/json

{
  "body": "Updated comment"
}
```

#### Delete Issue Comment

```bash
DELETE /github/repos/{owner}/{repo}/issues/comments/{comment_id}
```

### Labels

#### List Labels

```bash
GET /github/repos/{owner}/{repo}/labels?per_page=30
```

Example:

```bash
maton github label list --repo {owner}/{repo}
```

#### Create Label

```bash
POST /github/repos/{owner}/{repo}/labels
Content-Type: application/json

{
  "name": "priority:high",
  "color": "ff0000",
  "description": "High priority issues"
}
```

Example:

```bash
maton github label create "priority:high" --repo {owner}/{repo} --color ff0000 --description "High priority issues"
```

### Milestones

#### List Milestones

```bash
GET /github/repos/{owner}/{repo}/milestones?state=open&per_page=30
```

#### Create Milestone

```bash
POST /github/repos/{owner}/{repo}/milestones
Content-Type: application/json

{
  "title": "v1.0",
  "state": "open",
  "description": "First release",
  "due_on": "2026-03-01T00:00:00Z"
}
```

### Pull Requests

#### List Pull Requests

```bash
GET /github/repos/{owner}/{repo}/pulls?state=open&per_page=30
```

Query parameters: `state` (open, closed, all), `head`, `base`, `sort`, `direction`, `per_page`, `page`

Example:

```bash
maton github pr list --repo {owner}/{repo} --state open
```

#### Get Pull Request

```bash
GET /github/repos/{owner}/{repo}/pulls/{pull_number}
```

Example:

```bash
maton github pr view {pull_number} --repo {owner}/{repo}
```

#### Create Pull Request

```bash
POST /github/repos/{owner}/{repo}/pulls
Content-Type: application/json

{
  "title": "New feature",
  "body": "Description of changes",
  "head": "feature-branch",
  "base": "main",
  "draft": false
}
```

Example:

```bash
maton github pr create --repo {owner}/{repo} --base main --head feature-branch --title "New feature" --body "Description of changes"
```

#### Update Pull Request

```bash
PATCH /github/repos/{owner}/{repo}/pulls/{pull_number}
Content-Type: application/json

{
  "title": "Updated title",
  "state": "closed"
}
```

Example:

```bash
maton github pr edit {pull_number} --repo {owner}/{repo} --title "Updated title"
```

#### List Pull Request Commits

```bash
GET /github/repos/{owner}/{repo}/pulls/{pull_number}/commits?per_page=30
```

#### List Pull Request Files

```bash
GET /github/repos/{owner}/{repo}/pulls/{pull_number}/files?per_page=30
```

Example:

```bash
maton github pr diff {pull_number} --repo {owner}/{repo}
```

#### Check If Merged

```bash
GET /github/repos/{owner}/{repo}/pulls/{pull_number}/merge
```

#### Merge Pull Request

```bash
PUT /github/repos/{owner}/{repo}/pulls/{pull_number}/merge
Content-Type: application/json

{
  "commit_title": "Merge pull request",
  "merge_method": "squash"
}
```

Merge methods: `merge`, `squash`, `rebase`

Example:

```bash
maton github pr merge {pull_number} --repo {owner}/{repo} --squash --delete-branch
```

### Pull Request Reviews

#### List Reviews

```bash
GET /github/repos/{owner}/{repo}/pulls/{pull_number}/reviews?per_page=30
```

#### Create Review

```bash
POST /github/repos/{owner}/{repo}/pulls/{pull_number}/reviews
Content-Type: application/json

{
  "body": "Looks good!",
  "event": "APPROVE"
}
```

Events: `APPROVE`, `REQUEST_CHANGES`, `COMMENT`

Example:

```bash
maton github pr review {pull_number} --repo {owner}/{repo} --approve --body "Looks good!"
```

Note: GitHub does not allow approving your own pull requests; `--approve` returns `422 Can not approve your own pull request` in that case. Use `--comment` or `--request-changes` instead.

### Search

#### Search Repositories

```bash
GET /github/search/repositories?q={query}&per_page=30
```

Example queries:
- `tetris+language:python` - Repositories with "tetris" in Python
- `react+stars:>10000` - Repositories with "react" and 10k+ stars

Example:

```bash
maton github repo search tetris --language python
```

#### Search Issues

```bash
GET /github/search/issues?q={query}&per_page=30
```

Example queries:
- `bug+is:open+is:issue` - Open issues containing "bug"
- `author:username+is:pr` - Pull requests by author

Example:

```bash
maton github issue search "bug" --state open
```

#### Search Code

```bash
GET /github/search/code?q={query}&per_page=30
```

Example queries:
- `addClass+repo:facebook/react` - Search for "addClass" in a specific repo
- `function+extension:js` - JavaScript functions

Note: Code search may timeout on broad queries.

#### Search Users

```bash
GET /github/search/users?q={query}&per_page=30
```

### Organizations

#### List User Organizations

```bash
GET /github/user/orgs?per_page=30
```

Note: Requires `read:org` scope.

#### Get Organization

```bash
GET /github/orgs/{org}
```

#### List Organization Members

```bash
GET /github/orgs/{org}/members?per_page=30
```

### Rate Limit

#### Get Rate Limit

```bash
GET /github/rate_limit
```

## Pagination

GitHub uses page-based pagination. The CLI automatically paginates with '--paginate'.

Example:

```bash
maton github repo list --paginate
```

## Code Examples

### CLI

```bash
# Get repos as JSON (full objects)
maton github repo list --json

# Project specific fields with jq
maton github repo list --json --jq '.[] | {name, full_name, private}'

# Filter — e.g., only public repos
maton github repo list --json --jq '.[] | select(.private == false) | .name'

# Extract a single field
maton github issue list --repo owner/repo --json --jq '.[].title'
```

### JavaScript

```javascript
const response = await fetch(
  'https://api.maton.ai/github/repos/owner/repo/issues?state=open&per_page=10',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const issues = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://api.maton.ai/github/repos/owner/repo/issues',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'state': 'open', 'per_page': 10}
)
issues = response.json()
```

## Notes

- Repository names are case-insensitive but the API preserves case
- Issue numbers and PR numbers share the same sequence per repository
- Content must be Base64 encoded when creating/updating files
- Rate limits: 5000 requests/hour for authenticated users, 30 searches/minute
- Search queries may timeout on very broad patterns
- Some endpoints require specific OAuth scopes (e.g., `read:org` for organization operations). If you receive a scope error, contact Maton support at support@maton.ai with the specific operations/APIs you need and your use-case
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing GitHub connection |
| 401 | Invalid or missing Maton API key |
| 403 | Forbidden - insufficient permissions or scope |
| 404 | Resource not found |
| 408 | Request timeout (common for complex searches) |
| 422 | Validation failed |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from GitHub API |

### Troubleshooting: API Key Issues

**CLI:**

1. Check your auth state:

```bash
maton whoami
```

2. Verify the API key is valid by listing connections:

```bash
maton connection list
```

**Manual:**

1. Check that the `MATON_API_KEY` environment variable is set:

```bash
echo $MATON_API_KEY
```

2. Verify the API key is valid by listing connections:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Troubleshooting: Invalid App Name

1. Ensure your URL path starts with `github`. For example:

- Correct: `https://api.maton.ai/github/user`
- Incorrect: `https://api.maton.ai/api.github.com/user`

## Resources

- [GitHub REST API Documentation](https://docs.github.com/en/rest)
- [Repositories API](https://docs.github.com/en/rest/repos/repos)
- [Issues API](https://docs.github.com/en/rest/issues/issues)
- [Pull Requests API](https://docs.github.com/en/rest/pulls/pulls)
- [Search API](https://docs.github.com/en/rest/search/search)
- [Rate Limits](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)
- [Maton CLI Manual](https://cli.maton.ai/manual)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
