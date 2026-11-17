# GitHub Integration Skill — SKILL.md

## Metadata

- **name:** github-integration
- **version:** 1.0.0
- **description:** Operate GitHub repositories, issues, pull requests, files, and code search using the GitHub REST API via curl. Requires a GitHub Personal Access Token (PAT).
- **trigger phrases:** []
- **trigger phrases (natural English, ≥10):**
  - "create a GitHub issue"
  - "open an issue on"
  - "comment on the PR"
  - "close the issue"
  - "list all issues in"
  - "show me the pull requests"
  - "get the contents of a file in"
  - "search for code in"
  - "create a new branch on"
  - "add a label to"
  - "find repositories matching"
  - "get repo info for"
  - "create a pull request"
  - "update a file in"
  - "delete a label from"

---

## 1. Overview

This skill wraps the **GitHub REST API** (v3) using `curl` commands executed in a shell. It handles:

- Issues (create, list, update, comment, label)
- Pull Requests (create, list, comment, merge, close)
- Repository contents (get file, create/update file, delete file)
- Code and repository search
- Repository metadata
- Labels management

All requests use **Bearer token authentication** with a GitHub Personal Access Token (PAT). The base URL is `https://api.github.com`.

---

## 2. Prerequisites

### 2.1 GitHub Personal Access Token (PAT)

1. Go to **GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens** (or classic tokens).
2. Click **Generate new token** (fine-grained recommended).
3. Set an expiration date.
4. Under **Permissions**, grant at minimum:
   - `issues: Read and write`
   - `pull_requests: Read and write`
   - `contents: Read and write`
   - `search: Read and write`
   - `metadata: Read-only` (always included)
5. Copy the generated token.

### 2.2 Store the Token

Store the PAT in your OpenClaw environment so it is never hard-coded:

```bash
# Option A — export in your shell profile (~/.bashrc, ~/.zshrc)
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"

# Option B — write to a secure file with restricted permissions
echo "ghp_xxxxxxxxxxxxxxxxxxxx" > ~/.config/openclaw/github_token
chmod 600 ~/.config/openclaw/github_token
```

Reference it in every curl call:

```bash
GH_TOKEN="$(cat ~/.config/openclaw/github_token)"
```

### 2.3 jq Installation

Many examples use `jq` to parse JSON responses. Install it if not present:

```bash
sudo apt install jq   # Debian/Ubuntu
brew install jq       # macOS
```

---

## 3. Capabilities

### 3.1 Create an Issue

Create a new issue in a repository.

```
POST /repos/{owner}/{repo}/issues
```

**Trigger phrases:**
- "create a GitHub issue"
- "open an issue on"
- "file a new bug report"

### 3.2 List Issues

List issues (open, closed, or all) in a repository.

```
GET /repos/{owner}/{repo}/issues
```

**Trigger phrases:**
- "list all issues in"
- "show me the open issues"

### 3.3 Get a Single Issue

Fetch a specific issue by number.

```
GET /repos/{owner}/{repo}/issues/{issue_number}
```

### 3.4 Update / Close an Issue

Update issue fields (state, title, body, labels, assignee).

```
PATCH /repos/{owner}/{repo}/issues/{issue_number}
```

**Trigger phrases:**
- "close the issue"
- "update the issue"

### 3.5 Comment on an Issue or PR

Add a comment to an issue or pull request.

```
POST /repos/{owner}/{repo}/issues/{issue_number}/comments
```

**Trigger phrases:**
- "comment on the issue"
- "reply to the PR"

### 3.6 List Comments on an Issue

```
GET /repos/{owner}/{repo}/issues/{issue_number}/comments
```

### 3.7 Create a Pull Request

Create a new pull request between two branches.

```
POST /repos/{owner}/{repo}/pulls
```

**Trigger phrases:**
- "create a pull request"
- "open a PR"

### 3.8 List Pull Requests

```
GET /repos/{owner}/{repo}/pulls
```

**Trigger phrases:**
- "list pull requests"
- "show me the PRs"

### 3.9 Get Pull Request Details

```
GET /repos/{owner}/{repo}/pulls/{pull_number}
```

### 3.10 Merge a Pull Request

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/merge
```

### 3.11 Get File Contents

Retrieve the content of a file (returns base64-encoded `content` + `sha`).

```
GET /repos/{owner}/{repo}/contents/{path}
```

**Trigger phrases:**
- "get the contents of a file in"
- "show me the README"

### 3.12 Create or Update a File

Create a new file or update an existing one. Requires the file's current `sha` for updates.

```
PUT /repos/{owner}/{repo}/contents/{path}
```

**Trigger phrases:**
- "create a file in"
- "update a file in"
- "write to the repo"

### 3.13 Delete a File

Delete a file. Requires the file's current `sha` and a commit message.

```
DELETE /repos/{owner}/{repo}/contents/{path}
```

### 3.14 Search Code

Search across repositories using GitHub's search API.

```
GET /search/code?q={query}&repo={owner}/{repo}
```

**Trigger phrases:**
- "search for code in"
- "find code matching"

### 3.15 Search Repositories

```
GET /search/repositories?q={query}
```

**Trigger phrases:**
- "find repositories matching"
- "search for repos"

### 3.16 Get Repository Information

```
GET /repos/{owner}/{repo}
```

**Trigger phrases:**
- "get repo info for"
- "show repository details"

### 3.17 List Repository Labels

```
GET /repos/{owner}/{repo}/labels
```

### 3.18 Create a Label

```
POST /repos/{owner}/{repo}/labels
```

### 3.19 Add Label to an Issue

```
POST /repos/{owner}/{repo}/issues/{issue_number}/labels
```

**Trigger phrases:**
- "add a label to"
- "tag the issue with"

### 3.20 Remove Label from an Issue

```
DELETE /repos/{owner}/{repo}/issues/{issue_number}/labels/{name}
```

---

## 4. Detailed API Steps

### Common Variables

```bash
# Set once per session or per command block
GH_TOKEN="$(cat ~/.config/openclaw/github_token)"
BASE_URL="https://api.github.com"
HEADERS="-H 'Authorization: Bearer ${GH_TOKEN}' -H 'Accept: application/vnd.github+json'"
# Example usage:
# curl -s ${HEADERS} ${BASE_URL}/repos/owner/repo
```

---

### 4.1 Create an Issue

```bash
OWNER="octocat"
REPO="hello-world"
URL="${BASE_URL}/repos/${OWNER}/${REPO}/issues"

curl -s -X POST ${URL} \
  -H "Authorization: Bearer ${GH_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -d '{
    "title": "Bug: login fails with special characters",
    "body": "Steps to reproduce:\n1. Enter password with @ symbol\n2. Click login\nExpected: success; Actual: 500 error",
    "labels": ["bug", "priority-high"],
    "assignees": ["octocat"]
  }' | jq '{ number, title, state, html_url }'
```

**Response fields used:** `number`, `title`, `state`, `html_url`, `labels`

---

### 4.2 List Issues

```bash
OWNER="torvalds"
REPO="linux"
STATE="open"          # open | closed | all
PER_PAGE="10"

URL="${BASE_URL}/repos/${OWNER}/${REPO}/issues?state=${STATE}&per_page=${PER_PAGE}"

curl -s ${URL} \
  -H "Authorization: Bearer ${GH_TOKEN}" \
  -H "Accept: application/vnd.github+json" | \
  jq '.[] | { number, title, state, labels: [.labels[].name], created_at }'
```

---

### 4.3 Get a Single Issue

```bash
OWNER="facebook"
REPO="react"
ISSUE_NUM="25000"

URL="${BASE_URL}/repos/${OWNER}/${REPO}/issues/${ISSUE_NUM}"

curl -s ${URL} \
  -H "Authorization: Bearer ${GH_TOKEN}" | \
  jq '{ number, title, state, body, labels: [.labels[].name], assignee, comments, html_url }'
```

---

### 4.4 Close an Issue

```bash
OWNER="octocat"
REPO="hello-world"
ISSUE_NUM="42"

URL="${BASE_URL}/repos/${OWNER}/${REPO}/issues/${ISSUE_NUM}"

curl -s -X PATCH ${URL} \
  -H "Authorization: Bearer ${GH_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -d '{ "state": "closed", "state_reason": "completed" }' | \
  jq '{ number, state, state_reason }'
```

---

### 4.5 Comment on an Issue

```bash
OWNER="microsoft"
REPO="vscode"
ISSUE_NUM="12345"
COMMENT_BODY="Thanks for reporting this! I can reproduce it. Labeling as bug."

curl -s -X POST \
  "${BASE_URL}/repos/${OWNER}/${REPO}/issues/${ISSUE_NUM}/comments" \
  -H "Authorization: Bearer ${GH_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -d "$(jq -n --arg body "$COMMENT_BODY" '{ body: $body }')" | \
  jq '{ id, body, created_at, html_url }'
```

---

### 4.6 List Comments on an Issue

```bash
OWNER="microsoft"
REPO="vscode"
ISSUE_NUM="12345"

curl -s "${BASE_URL}/repos/${OWNER}/${REPO}/issues/${ISSUE_NUM}/comments" \
  -H "Authorization: Bearer ${GH_TOKEN}" | \
  jq '.[] | { id, user: .user.login, body, created_at }'
```

---

### 4.7 Create a Pull Request

```bash
OWNER="myorg"
REPO="myrepo"
URL="${BASE_URL}/repos/${OWNER}/${REPO}/pulls"

curl -s -X POST ${URL} \
  -H "Authorization: Bearer ${GH_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -d '{
    "title": "feat: add dark mode support",
    "head": "feature/dark-mode",
    "base": "main",
    "body": "## Summary\nAdds a dark mode toggle to the settings page.\n\n## Test plan\n- [ ] Toggle works on all pages\n- [ ] Preference persists across sessions",
    "draft": false
  }' | jq '{ number, title, state, html_url, draft }'
```

---

### 4.8 List Pull Requests

```bash
OWNER="torvalds"
REPO="linux"
STATE="open"    # open | closed | all | merged

curl -s "${BASE_URL}/repos/${OWNER}/${REPO}/pulls?state=${STATE}&per_page=20" \
  -H "Authorization: Bearer ${GH_TOKEN}" | \
  jq '.[] | { number, title, state, user: .user.login, head: .head.ref, base: .base.ref }'
```

---

### 4.9 Merge a Pull Request

```bash
OWNER="myorg"
REPO="myrepo"
PR_NUM="42"
METHOD="squash"    # merge | squash | rebase

curl -s -X PUT \
  "${BASE_URL}/repos/${OWNER}/${REPO}/pulls/${PR_NUM}/merge" \
  -H "Authorization: Bearer ${GH_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -d '{
    "merge_method": "'"${METHOD}"'",
    "commit_title": "feat: add dark mode (squashed)",
    "commit_message": "See PR description"
  }' | jq '{ merged, message }'
```

---

### 4.10 Get File Contents (and SHA)

```bash
OWNER="torvalds"
REPO="linux"
FILE_PATH="README"

curl -s "${BASE_URL}/repos/${OWNER}/${REPO}/contents/${FILE_PATH}" \
  -H "Authorization: Bearer ${GH_TOKEN}" | \
  jq '{ name, path, sha, size, html_url, content: (.content | gsub("\n"; "")) }'
```

> **Note:** The `content` field is base64-encoded. To decode:
> ```bash
> CONTENT=$(curl -s "${BASE_URL}/repos/${OWNER}/${REPO}/contents/${FILE_PATH}" \
>   -H "Authorization: Bearer ${GH_TOKEN}" | jq -r '.content')
> echo "$CONTENT" | base64 -d
> ```

---

### 4.11 Create a New File

```bash
OWNER="myorg"
REPO="myrepo"
FILE_PATH="docs/new-feature.md"
COMMIT_MSG="docs: add new feature documentation"
CONTENT=$(echo -n "# New Feature\n\nThis feature does X." | base64 -w0)

curl -s -X PUT \
  "${BASE_URL}/repos/${OWNER}/${REPO}/contents/${FILE_PATH}" \
  -H "Authorization: Bearer ${GH_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -d "{
    \"message\": \"${COMMIT_MSG}\",
    \"content\": \"${CONTENT}\"
  }" | jq '{ commit: { sha, message, html_url } }'
```

---

### 4.12 Update an Existing File

To update a file, you must first fetch its current SHA.

```bash
OWNER="myorg"
REPO="myrepo"
FILE_PATH="README.md"
COMMIT_MSG="docs: update README with new screenshot"

# Step 1 — get current SHA
SHA=$(curl -s "${BASE_URL}/repos/${OWNER}/${REPO}/contents/${FILE_PATH}" \
  -H "Authorization: Bearer ${GH_TOKEN}" | jq -r '.sha')

# Step 2 — PUT with the SHA
NEW_CONTENT=$(echo -n "Updated README content here" | base64 -w0)

curl -s -X PUT \
  "${BASE_URL}/repos/${OWNER}/${REPO}/contents/${FILE_PATH}" \
  -H "Authorization: Bearer ${GH_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -d "{
    \"message\": \"${COMMIT_MSG}\",
    \"content\": \"${NEW_CONTENT}\",
    \"sha\": \"${SHA}\"
  }" | jq '{ commit: { sha, message } }'
```

---

### 4.13 Delete a File

```bash
OWNER="myorg"
REPO="myrepo"
FILE_PATH="old/deprecated-file.txt"
COMMIT_MSG="chore: remove deprecated file"

# Get SHA first
SHA=$(curl -s "${BASE_URL}/repos/${OWNER}/${REPO}/contents/${FILE_PATH}" \
  -H "Authorization: Bearer ${GH_TOKEN}" | jq -r '.sha')

curl -s -X DELETE \
  "${BASE_URL}/repos/${OWNER}/${REPO}/contents/${FILE_PATH}" \
  -H "Authorization: Bearer ${GH_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -d "{
    \"message\": \"${COMMIT_MSG}\",
    \"sha\": \"${SHA}\"
  }" | jq '{ commit: { sha, message } }'
```

---

### 4.14 Search Code

```bash
QUERY="csrf token"
OWNER="myorg"
REPO="myrepo"
PER_PAGE="30"

# URL-encode the query string
ENCODED_QUERY=$(echo -n "${QUERY}" | jq -sRr @uri)

curl -s "https://api.github.com/search/code?q=${ENCODED_QUERY}+repo:${OWNER}/${REPO}&per_page=${PER_PAGE}" \
  -H "Authorization: Bearer ${GH_TOKEN}" \
  -H "Accept: application/vnd.github+json" | \
  jq '{ total_count, items: [.items[] | { name, path, html_url }] }'
```

---

### 4.15 Search Repositories

```bash
QUERY="machine learning python"
SORT="stars"      # stars | forks | updated
ORDER="desc"
PER_PAGE="10"

ENCODED_QUERY=$(echo -n "${QUERY}" | jq -sRr @uri)

curl -s "https://api.github.com/search/repositories?q=${ENCODED_QUERY}&sort=${SORT}&order=${ORDER}&per_page=${PER_PAGE}" \
  -H "Authorization: Bearer ${GH_TOKEN}" | \
  jq '.items[] | { full_name, description, stargazers_count, forks_count, language, html_url }'
```

---

### 4.16 Get Repository Information

```bash
OWNER="torvalds"
REPO="linux"

curl -s "${BASE_URL}/repos/${OWNER}/${REPO}" \
  -H "Authorization: Bearer ${GH_TOKEN}" | \
  jq '{
    full_name, description, homepage,
    stargazers_count, forks_count, open_issues_count,
    language, default_branch, visibility,
    created_at, updated_at, pushed_at,
    topics: [.topics[0:10]],
    license: .license.spdx_id
  }'
```

---

### 4.17 List Repository Labels

```bash
OWNER="microsoft"
REPO="vscode"

curl -s "${BASE_URL}/repos/${OWNER}/${REPO}/labels?per_page=100" \
  -H "Authorization: Bearer ${GH_TOKEN}" | \
  jq '.[] | { name, color, description }'
```

---

### 4.18 Create a Label

```bash
OWNER="myorg"
REPO="myrepo"

curl -s -X POST \
  "${BASE_URL}/repos/${OWNER}/${REPO}/labels" \
  -H "Authorization: Bearer ${GH_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -d '{
    "name": "priority-critical",
    "color": "d73a4a",
    "description": "Critical priority, resolve immediately"
  }' | jq '{ name, color, description }'
```

---

### 4.19 Add Label to an Issue

```bash
OWNER="myorg"
REPO="myrepo"
ISSUE_NUM="42"

curl -s -X POST \
  "${BASE_URL}/repos/${OWNER}/${REPO}/issues/${ISSUE_NUM}/labels" \
  -H "Authorization: Bearer ${GH_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -d "$(jq -n --arg name "bug" '{ labels: [$name] }')" | \
  jq '.[] | { name, color }'
```

To add multiple labels at once:

```bash
curl -s -X POST \
  "${BASE_URL}/repos/${OWNER}/${REPO}/issues/${ISSUE_NUM}/labels" \
  -H "Authorization: Bearer ${GH_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -d '{
    "labels": ["bug", "priority-high", "needs-triage"]
  }' | jq '.'
```

---

### 4.20 Remove Label from an Issue

```bash
OWNER="myorg"
REPO="myrepo"
ISSUE_NUM="42"
LABEL_NAME="needs-triage"

# URL-encode the label name (e.g., spaces become %20)
ENCODED_LABEL=$(echo -n "${LABEL_NAME}" | jq -sRr @uri)

curl -s -X DELETE \
  "${BASE_URL}/repos/${OWNER}/${REPO}/issues/${ISSUE_NUM}/labels/${ENCODED_LABEL}" \
  -H "Authorization: Bearer ${GH_TOKEN}" | \
  jq -e '.name' || echo "Label removed (or already absent)"
```

---

## 5. Output Format

### Success

```json
{
  "ok": true,
  "action": "create_issue",
  "data": {
    "number": 42,
    "title": "Bug: login fails",
    "state": "open",
    "html_url": "https://github.com/owner/repo/issues/42"
  }
}
```

### Error — Rate Limited

```json
{
  "ok": false,
  "action": "api_request",
  "error": "rate_limited",
  "message": "GitHub API rate limit exceeded. Retry after 3600 seconds.",
  "retry_after": 3600
}
```

### Error — Not Found

```json
{
  "ok": false,
  "action": "get_file",
  "error": "not_found",
  "message": "File not found: path/to/file.md in owner/repo"
}
```

### Error — Missing Token

```json
{
  "ok": false,
  "error": "missing_token",
  "message": "GITHUB_TOKEN is not set. Provide a GitHub PAT and store it in ~/.config/openclaw/github_token"
}
```

---

## 6. Example Conversations

### Example 1: File a Bug Issue

**User:** "Can you open a GitHub issue on octocat/hello-world? Title: 'Login breaks with @ in password'. Body: 'Steps: 1. Enter @ in password. 2. Click login. Expected: success. Actual: 500 error.' Add labels: bug, priority-high."

**Assistant (executes):**

```bash
GH_TOKEN="$(cat ~/.config/openclaw/github_token)"
curl -s -X POST "https://api.github.com/repos/octocat/hello-world/issues" \
  -H "Authorization: Bearer ${GH_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -d '{
    "title": "Login breaks with @ in password",
    "body": "Steps: 1. Enter @ in password. 2. Click login.\nExpected: success. Actual: 500 error.",
    "labels": ["bug", "priority-high"]
  }' | jq '{ number, title, state, html_url, labels: [.labels[].name] }'
```

**Output:**

```
{
  "number": 42,
  "title": "Login breaks with @ in password",
  "state": "open",
  "html_url": "https://github.com/octocat/hello-world/issues/42",
  "labels": ["bug", "priority-high"]
}
```

**Assistant:** Done! Issue #42 created: https://github.com/octocat/hello-world/issues/42  
Labels: bug, priority-high.

---

### Example 2: Get a File and Update It

**User:** "Get the current README.md from myorg/myrepo, then update it to add a '## Changelog' section."

**Assistant (step 1 — get current contents + sha):**

```bash
GH_TOKEN="$(cat ~/.config/openclaw/github_token)"
curl -s "https://api.github.com/repos/myorg/myrepo/contents/README.md" \
  -H "Authorization: Bearer ${GH_TOKEN}" | \
  jq '{ sha, content: (.content | gsub("\n"; "")), encoding }'
```

**Output:**

```
{
  "sha": "a1b2c3d4e5f6789012345678901234567890abcd",
  "content": "IyBNeVJlcG8KClRoaXMgaXMgdGhlIFJFQURNRSB...",
  "encoding": "base64"
}
```

**Assistant (step 2 — decode, append changelog, encode, PUT):**

```bash
GH_TOKEN="$(cat ~/.config/openclaw/github_token)"
SHA="a1b2c3d4e5f6789012345678901234567890abcd"
OLD_CONTENT=$(curl -s "https://api.github.com/repos/myorg/myrepo/contents/README.md" \
  -H "Authorization: Bearer ${GH_TOKEN}" | jq -r '.content' | base64 -d)

NEW_CONTENT="${OLD_CONTENT}

## Changelog

- 2026-07-04: Added changelog section"

ENCODED=$(echo -n "${NEW_CONTENT}" | base64 -w0)

curl -s -X PUT "https://api.github.com/repos/myorg/myrepo/contents/README.md" \
  -H "Authorization: Bearer ${GH_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -d "{
    \"message\": \"docs: add changelog section\",
    \"content\": \"${ENCODED}\",
    \"sha\": \"${SHA}\"
  }" | jq '{ commit: { sha, message } }'
```

**Output:**

```
{ "commit": { "sha": "newcommitsha1234567890", "message": "docs: add changelog section" } }
```

---

### Example 3: Search Code and File a PR

**User:** "Search for 'csrf' in the myorg/frontend repo, then open a PR to fix it on a branch called fix/csrf-vulnerability from main."

**Assistant (search):**

```bash
GH_TOKEN="$(cat ~/.config/openclaw/github_token)"
QUERY="csrf"
curl -s "https://api.github.com/search/code?q=csrf+repo:myorg/frontend&per_page=10" \
  -H "Authorization: Bearer ${GH_TOKEN}" | \
  jq '{ total_count, files: [.items[] | { path, html_url }] }'
```

**Output:**

```
{ "total_count": 3, "files": [...] }
```

**Assistant (create PR):**

```bash
GH_TOKEN="$(cat ~/.config/openclaw/github_token)"
curl -s -X POST "https://api.github.com/repos/myorg/frontend/pulls" \
  -H "Authorization: Bearer ${GH_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -d '{
    "title": "fix: address CSRF vulnerability in auth flow",
    "head": "fix/csrf-vulnerability",
    "base": "main",
    "body": "## Summary\nFixes CSRF vulnerability found in search. Adds token validation.\n\n## Changes\n- Added CSRF token check in POST handlers\n- Added unit tests for auth flow\n\n## References\nCloses #42"
  }' | jq '{ number, title, state, html_url, draft }'
```

**Output:**

```
{ "number": 99, "title": "fix: address CSRF vulnerability in auth flow", "state": "open", "html_url": "https://github.com/myorg/frontend/pull/99", "draft": false }
```

**Assistant:** Found 3 files with "csrf". PR #99 opened: https://github.com/myorg/frontend/pull/99 — ready for review.

---

## 7. Installation Guide

### Step 1 — Create a GitHub PAT

1. Navigate to: https://github.com/settings/tokens
2. Click **Generate new token (classic)** or **Generate new token (fine-grained)**.
3. Name: `openclaw-github-skill`
4. Expiration: 30 days (or your preference)
5. For **fine-grained**:
   - Repository access: select specific repos, or All repositories
   - Permissions: Issues (Read and write), Pull requests (Read and write), Contents (Read and write), Search (Read and write), Metadata (Read-only)
6. Click **Generate token** and copy the token immediately (it is shown only once).

### Step 2 — Store the Token on the OpenClaw Host

```bash
# Create the config directory
mkdir -p ~/.config/openclaw

# Write the token (replace with your actual token)
echo "ghp_xxxxxxxxxxxxxxxxxxxx" > ~/.config/openclaw/github_token

# Lock down the file
chmod 600 ~/.config/openclaw/github_token

# Verify it works
cat ~/.config/openclaw/github_token
```

### Step 3 — Verify Authentication

```bash
GH_TOKEN="$(cat ~/.config/openclaw/github_token)"
curl -s -H "Authorization: Bearer ${GH_TOKEN}" \
  "https://api.github.com/user" | \
  jq '{ login, name, email }'
```

Expected output shows your GitHub username and email. If you get `401 Unauthorized`, the token is invalid or lacks the correct scopes.

### Step 4 — Install jq (if missing)

```bash
sudo apt update && sudo apt install -y jq
```

### Step 5 — Test the Skill

```bash
# Test listing issues (public repo)
GH_TOKEN="$(cat ~/.config/openclaw/github_token)"
curl -s "https://api.github.com/repos/octocat/hello-world/issues?per_page=5" \
  -H "Authorization: Bearer ${GH_TOKEN}" | \
  jq '.[] | { number, title }'
```

### Step 6 — Integrate with OpenClaw (Optional)

If your OpenClaw instance uses environment variables, add this to `~/.bashrc` or the OpenClaw service environment:

```bash
export GITHUB_TOKEN="$(cat ~/.config/openclaw/github_token)"
```

Restart the OpenClaw gateway after adding the variable.

---

## 8. Caveats, Rate Limits, and Best Practices

### 8.1 Rate Limits

| Endpoint type | Authenticated limit | Notes |
|---|---|---|
| Most API endpoints | 5,000 requests/hour | Per token, per API instance |
| Search (code/repos) | 30 requests/minute | Subject to secondary limit |
| GraphQL API | 5,000 points/hour | Different from REST limits |

**Handle rate limits in scripts:**

```bash
# Check remaining requests
REMAINING=$(curl -s -I "https://api.github.com/rate_limit" \
  -H "Authorization: Bearer ${GH_TOKEN}" | \
  grep -i "x-ratelimit-remaining" | awk '{print $2}')

if [ "$REMAINING" -lt 10 ]; then
  echo "Warning: only ${REMAINING} requests remaining. Waiting..."
  sleep 60
fi
```

**When rate limited (HTTP 429):**

```bash
# Parse Retry-After header (seconds)
RETRY_AFTER=$(curl -s -I "https://api.github.com/repos/owner/repo" \
  -H "Authorization: Bearer ${GH_TOKEN}" | \
  grep -i "retry-after" | awk '{print $2}')

echo "Rate limited. Retry after ${RETRY_AFTER} seconds."
# Consider sleeping + retrying
```

### 8.2 Token Permissions

- **Minimum viable PAT:** For issues + PRs only — no `contents:write` needed.
- **No `repo` scope needed for public repos:** Public repo operations work with limited-scope fine-grained tokens.
- **Avoid the `repo` (classic) scope** unless you need full repo access — it grants access to all your private repos.
- **Fine-grained tokens are preferred** over classic tokens for least-privilege access.

### 8.3 Working with Branches

- Creating files requires the **target branch** to already exist.
- Branch names must be URL-safe (lowercase, hyphens, no spaces).
- Create a branch via the Git Data API or via the web interface, then commit to it.

### 8.4 File Content Encoding

- All file content sent to GitHub must be **base64-encoded** with standard alphabet (no line breaks, use `-w0` flag with `base64`).
- GitHub returns base64 content with line breaks every ~80 characters — **strip them before decoding:**
  ```bash
  CONTENT=$(echo "$CONTENT" | tr -d '\n')
  echo "$CONTENT" | base64 -d
  ```

### 8.5 SHA is Required for Updates/Deletions

- Every PUT or DELETE on a file path requires the current `sha` of that file.
- Always fetch the SHA first in a separate request. If the SHA has changed (conflict), the PUT will fail with `409 Conflict`.

### 8.6 Draft Pull Requests

- Set `"draft": true` when creating a PR to open it as a draft.
- Draft PRs cannot be merged via the merge API until promoted.

### 8.7 Commas in JSON

- Bash `curl -d` with single-quoted JSON works fine for simple strings.
- For user-supplied dynamic content, use `jq -n --arg key "$value"` to safely embed variables without JSON-escaping issues.

### 8.8 Pagination

For large result sets, GitHub paginates at 30 (default) or 30/60/100 (max per page). Use:

```bash
# Page through issues
PAGE=1
PER_PAGE=100
while true; do
  RESULT=$(curl -s "${BASE_URL}/repos/${OWNER}/${REPO}/issues?page=${PAGE}&per_page=${PER_PAGE}" \
    -H "Authorization: Bearer ${GH_TOKEN}")
  COUNT=$(echo "$RESULT" | jq length)
  [ "$COUNT" -eq 0 ] && break
  echo "$RESULT" | jq '.[] | { number, title }'
  PAGE=$((PAGE + 1))
done
```

### 8.9 HTTPS Only

- GitHub API only accepts HTTPS. Plain HTTP requests are redirected (and may expose tokens in clear text during the redirect).
- Always use `https://api.github.com`.

### 8.10 Token Security

- **Never** hard-code a PAT in a script, skill file, or chat message.
- Use file-based storage with `chmod 600` as shown in §2.
- Rotate tokens regularly — especially if they may have been exposed.
- Revoke a token immediately if you suspect it is compromised: https://github.com/settings/tokens

---

## 9. Quick Reference Cheat Sheet

```bash
# Variables
GH_TOKEN="$(cat ~/.config/openclaw/github_token)"
BASE="https://api.github.com"
H="-H 'Authorization: Bearer ${GH_TOKEN}' -H 'Accept: application/vnd.github+json'"

# Create issue
curl -s -X POST $BASE/repos/OWNER/REPO/issues -H "$H" -d '{"title":"Bug"}'

# List issues
curl -s "$BASE/repos/OWNER/REPO/issues?state=open&per_page=30" -H "$H"

# Close issue
curl -s -X PATCH $BASE/repos/OWNER/REPO/issues/N -H "$H" -d '{"state":"closed"}'

# Comment
curl -s -X POST $BASE/repos/OWNER/REPO/issues/N/comments -H "$H" -d "$(jq -n --arg b 'Comment text' '{body:$b}')"

# Create PR
curl -s -X POST $BASE/repos/OWNER/REPO/pulls -H "$H" -d '{"title":"PR","head":"branch","base":"main"}'

# Get file
curl -s $BASE/repos/OWNER/REPO/contents/PATH -H "$H"

# Update file (needs sha)
SHA=$(curl -s $BASE/repos/OWNER/REPO/contents/PATH -H "$H" | jq -r '.sha')
ENCODED=$(echo "new content" | base64 -w0)
curl -s -X PUT $BASE/repos/OWNER/REPO/contents/PATH -H "$H" -d "{\"message\":\"update\",\"content\":\"$ENCODED\",\"sha\":\"$SHA\"}"

# Search code
curl -s "https://api.github.com/search/code?q=QUERY+repo:OWNER/REPO" -H "$H"

# Get repo info
curl -s $BASE/repos/OWNER/REPO -H "$H"

# Add label
curl -s -X POST $BASE/repos/OWNER/REPO/issues/N/labels -H "$H" -d '{"labels":["bug"]}'

# Check rate limit
curl -s $BASE/rate_limit -H "$H"
```
