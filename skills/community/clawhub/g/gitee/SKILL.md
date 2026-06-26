---
name: gitee
description: "Gitee operations via OpenAPI and git: repositories, pull requests, issues, comments, and file contents. Use when: (1) inspecting or creating Gitee pull requests, (2) listing or creating repository issues, (3) reading repository files from the Gitee API, (4) working with gitee.com remotes from the terminal. NOT for: GitHub-only workflows, local-only git tasks with no Gitee interaction, or browser-only account setup and SSO flows."
metadata:
  {
    "openclaw":
      {
        "emoji": "🧰",
        "requires": { "bins": ["curl", "git", "jq"], "env": ["GITEE_ACCESS_TOKEN"] },
        "primaryEnv": "GITEE_ACCESS_TOKEN",
      },
  }
---

# Gitee Skill

Use `git` for clone, fetch, branch, and push operations. Use `curl` + `jq` for structured Gitee API calls.

## When to Use

✅ **USE this skill when:**

- Checking Gitee pull requests, branches, or repository metadata
- Listing or creating issues on a Gitee repository
- Reading repository files through the Gitee API
- Automating Gitee workflows from the terminal when no dedicated CLI is available

## When NOT to Use

❌ **DON'T use this skill when:**

- Working with GitHub repositories → use the `github` skill
- Doing local-only git work with no Gitee interaction → use `git` directly
- Handling browser-only flows such as login, captcha, or SSO approval

## Setup

1. Create a Gitee personal access token with the repository permissions you need.
2. Export the API base URL and token:

```bash
export GITEE_API="https://gitee.com/api/v5"
export GITEE_ACCESS_TOKEN="..."
```

3. Never print, commit, or paste the token into chat. Keep it in environment/config only.

## Remote Patterns

Common Gitee remotes:

```text
https://gitee.com/owner/repo.git
git@gitee.com:owner/repo.git
```

Inspect the current repo:

```bash
git remote -v
git remote get-url origin
```

## API Conventions

- Gitee OpenAPI examples commonly pass OAuth2 credentials as `access_token`.
- Prefer `curl -fsS` so HTTP failures surface clearly.
- Prefer `jq -nc` to build JSON request bodies instead of hand-escaped strings.
- Repository issue APIs differ from GitHub: many issue routes use `/repos/{owner}/issues` and pass the repo name as a `repo` field.

## Common Commands

### Pull Requests

List open pull requests:

```bash
OWNER=owner
REPO=repo

curl -fsS --get "$GITEE_API/repos/$OWNER/$REPO/pulls" \
  --data-urlencode "access_token=$GITEE_ACCESS_TOKEN" \
  --data-urlencode "state=open" |
  jq '.[] | {number, title, state, author: .user.login}'
```

View one pull request:

```bash
PR_NUMBER=12

curl -fsS --get "$GITEE_API/repos/$OWNER/$REPO/pulls/$PR_NUMBER" \
  --data-urlencode "access_token=$GITEE_ACCESS_TOKEN"
```

Create a pull request:

```bash
HEAD_BRANCH="feature-branch"
BASE_BRANCH="main"
TITLE="feat: add gitee support"
BODY="Summary of the change"

curl -fsS -X POST "$GITEE_API/repos/$OWNER/$REPO/pulls" \
  -H "Content-Type: application/json" \
  -d "$(jq -nc \
    --arg access_token "$GITEE_ACCESS_TOKEN" \
    --arg title "$TITLE" \
    --arg head "$HEAD_BRANCH" \
    --arg base "$BASE_BRANCH" \
    --arg body "$BODY" \
    '{access_token: $access_token, title: $title, head: $head, base: $base, body: $body}')" |
  jq '{number, title, html_url, state}'
```

### Issues

List issues for a repository:

```bash
curl -fsS --get "$GITEE_API/repos/$OWNER/issues" \
  --data-urlencode "access_token=$GITEE_ACCESS_TOKEN" \
  --data-urlencode "repo=$REPO" \
  --data-urlencode "state=open" |
  jq '.[] | {number, title, state}'
```

Create an issue:

```bash
TITLE="Bug: unexpected failure"
BODY="Steps to reproduce..."

curl -fsS -X POST "$GITEE_API/repos/$OWNER/issues" \
  -H "Content-Type: application/json" \
  -d "$(jq -nc \
    --arg access_token "$GITEE_ACCESS_TOKEN" \
    --arg repo "$REPO" \
    --arg title "$TITLE" \
    --arg body "$BODY" \
    '{access_token: $access_token, repo: $repo, title: $title, body: $body}')" |
  jq '{number, title, state, html_url}'
```

### Repository Contents

Read a file:

```bash
FILE_PATH="README.md"

curl -fsS --get "$GITEE_API/repos/$OWNER/$REPO/contents/$FILE_PATH" \
  --data-urlencode "access_token=$GITEE_ACCESS_TOKEN"
```

Create or update file contents use the same path with `POST` or `PUT`. Build the JSON body with `jq -nc` and include the commit message plus content fields required by the endpoint.

### Git Transport

Clone from Gitee:

```bash
git clone "https://gitee.com/$OWNER/$REPO.git"
```

Push the current branch:

```bash
git push origin HEAD
```

Add a dedicated Gitee remote:

```bash
git remote add gitee "git@gitee.com:$OWNER/$REPO.git"
git push gitee HEAD
```

## Useful `jq` Filters

Open PR titles:

```bash
jq -r '.[] | "#\(.number) \(.title)"'
```

Issue numbers and links:

```bash
jq -r '.[] | "#\(.number) \(.html_url)"'
```

## Notes

- Prefer API calls when you need structured metadata, filtering, or automation.
- Prefer `git` when you need branch, commit, clone, fetch, or push behavior.
- Gitee OpenAPI docs: https://gitee.com/api/v5/swagger
- If an operation is missing here, look it up in the OpenAPI docs and keep the same `access_token` + `curl` pattern.
