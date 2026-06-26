---
name: propel-code-review
description: Run async diff-based code reviews using the Propel Review API, poll for completion, retrieve structured findings, and send comment feedback. Use when reviewing the current branch diff or any Git diff with Propel.
metadata: {"clawdbot":{"requires":{"env":["PROPEL_API_KEY"],"bins":["curl","git","jq"]},"primaryEnv":"PROPEL_API_KEY","homepage":"https://www.propelcode.ai/"}}
---

# Propel Review API Skill

Use this guide to interact with the Propel Review API from an AI agent.
Always target the production API unless told otherwise.

## Purpose

Run async, diff-based code reviews via the production API and retrieve comments.

## Quick Permission Check

Before rollout to a new workspace/repo, run this from the target repository root:

```bash
plugins/propel-code-review/skills/propel-code-review/scripts/smoke_test_permissions.sh
```

It validates:
- good token + connected repo
- good token + unconnected repo
- invalid token + connected repo

## Pre-flight: Verify API Key

**Before making any API call**, check whether `PROPEL_API_KEY` is set:

```bash
if [ -n "$PROPEL_API_KEY" ]; then echo "PROPEL_API_KEY is set"; else echo "PROPEL_API_KEY is not set"; fi
```

If the variable is empty, unset, or you just received a `401/403` from the Review
API, **do not attempt any API calls** with the current value. Follow these steps
to capture a fresh token — each step is a separate action:

**Step 1** — Tell the user and open the browser. Send this message and run the
Bash command in the same response (in parallel):

Message to user:
> `PROPEL_API_KEY` is not set. Opening the token creation page:
> https://app.propelcode.ai/administration/settings?tab=review-api-tokens&token_name=Claude+Code&scopes=reviews:read,reviews:write
> The name and scopes are pre-filled. Click **Create token**, copy it, and paste it here.

Bash command:
```bash
URL="https://app.propelcode.ai/administration/settings?tab=review-api-tokens&token_name=Claude+Code&scopes=reviews:read,reviews:write"
if command -v xdg-open >/dev/null; then xdg-open "$URL"; else open "$URL"; fi
```

**Step 2** — Wait for the user to paste the token. Do not proceed until the user
pastes a value starting with `rev_`. If the value doesn't start with `rev_`, tell
them it doesn't look valid and ask them to try again.

**Step 3** — Once you have a valid token, persist it and load it into the session.
Run this in a **single Bash call** (replace `<TOKEN>` with the actual token):

```bash
case "$SHELL" in */zsh) SHELL_RC="$HOME/.zshrc" ;; */bash) SHELL_RC="$HOME/.bashrc" ;; *) SHELL_RC="" ;; esac; if [ -z "$SHELL_RC" ] && [ -f "$HOME/.zshrc" ]; then SHELL_RC="$HOME/.zshrc"; fi; if [ -z "$SHELL_RC" ] && [ -f "$HOME/.bashrc" ]; then SHELL_RC="$HOME/.bashrc"; fi; if [ -n "$SHELL_RC" ]; then printf '\n# Propel Review API token\nexport PROPEL_API_KEY="%s"\n' "<TOKEN>" >> "$SHELL_RC" && echo "Saved to $SHELL_RC"; else echo "No shell profile found"; fi; export PROPEL_API_KEY="<TOKEN>"
```

Tell the user where the key was saved (e.g. "Saved to ~/.zshrc").

**Step 4** — Continue with the review workflow.

## Setup (Manual)

If you prefer to set the token yourself ahead of time:

```bash
export PROPEL_API_KEY="rev_..."
```

The token must be a Review API token (scoped to both `reviews:write` and `reviews:read`).

## Base URL

```
https://api.propelcode.ai
```

## Authentication

Use a bearer token in the `Authorization` header:

```
Authorization: Bearer $PROPEL_API_KEY
```

## Endpoints (Only These)

Do not assume any other Review APIs exist. Only use the async endpoints below.

### Create Review (Async)

`POST /v1/reviews`

Request body:

```json
{
  "diff": "string (required)",
  "repository": "string (required)",
  "base_commit": "string (required)",
  "head_commit_sha": "string (optional)",
  "branch": "string (optional)"
}
```

Constraints:
- `diff` max size: 1,000,000 bytes
- `repository` max length: 255
- `base_commit` max length: 255
- `head_commit_sha` max length: 255
- `branch` max length: 255

Notes:
- `base_commit` should be a commit that exists in the remote repo history
  (typically the base commit of the branch you are reviewing).
- `repository` should be the canonical repo slug (for example, `owner/repo`)
  derived from the git remote URL.

Response (202):

```json
{
  "review_id": "uuid",
  "status": "queued",
  "repository": "owner/repo",
  "base_commit": "sha",
  "created_at": "...",
  "updated_at": "..."
}
```

### Get Review Status/Results

`GET /v1/reviews/:review_id`

Response (200):

```json
{
  "review_id": "uuid",
  "status": "queued|running|completed|failed",
  "poll_after_ms": 3000,
  "comments": [
    {
      "comment_id": "string",
      "file_path": "path",
      "line": 123,
      "message": "...",
      "severity": "error|warning|info"
    }
  ],
  "error": {
    "code": "generation_failed",
    "message": "..."
  }
}
```

### Post Comment Feedback

`POST /v1/reviews/:review_id/comments/feedback`

Request body:

```json
{
  "comment_id": "string (required)",
  "incorporated": true,
  "notes": "string (optional)"
}
```

Response (200):

```json
{
  "review_id": "uuid",
  "comment_id": "string",
  "incorporated": true
}
```

## Scripts Used by This Skill

Use the helper scripts in `scripts/` instead of ad-hoc inline curl loops.
Paths below are relative to this skill directory:

- `scripts/create_review.sh` wraps `POST /v1/reviews`.
- `scripts/poll_review.sh` wraps polling `GET /v1/reviews/:review_id` until
  terminal status (`completed` or `failed`) or timeout.
- `scripts/post_comment_feedback.sh` wraps
  `POST /v1/reviews/:review_id/comments/feedback`.

## Approval-Friendly Prefixes (One-Time)

If your client supports prefix-based trust/approval, approve these once before
running this skill:

- `scripts/create_review.sh`
- `scripts/poll_review.sh`
- `scripts/post_comment_feedback.sh`
- `git diff`
- `git rev-parse`
- `git remote get-url`
- `gh pr view`
- `jq`

## Workflow (Recommended)

1. Resolve the base branch (PR base when available; otherwise remote default branch):
   - `BASE_BRANCH=$(gh pr view --json baseRefName -q '.baseRefName' 2>/dev/null || git remote show origin | sed -n '/HEAD branch/s/.*: //p')`
2. Compute the base commit (must exist in the remote repo history):
   - `git rev-parse "$BASE_BRANCH"`
3. Compute the current head commit and branch (for local review dedup context):
   - `git rev-parse HEAD`
   - `git rev-parse --abbrev-ref HEAD`
4. Compute the repository slug:
   - `git remote get-url origin | sed -E 's#(git@github.com:|https://github.com/)##; s/\\.git$//'`
5. Generate the diff:
   - `git diff "$BASE_BRANCH" > /tmp/review_api.diff`
6. Call `scripts/create_review.sh` with diff, base commit, repository slug, head commit, and branch.
7. Handle create-review failures before polling (script exits non-zero and
   prints the API response body):
   - `401/403`: token invalid/expired/missing scope. Stop and ask user to refresh token.
   - `404`: repository is not connected to the Propel workspace (or slug is wrong). Stop and ask user to connect/fix repo slug.
   - `400/413`: invalid request or diff too large. Stop and show actionable fix.
   - `5xx`: transient API error. Retry with bounded backoff, then stop and report if still failing.
8. Poll with `scripts/poll_review.sh` until status is `completed` or `failed`.
   The script keeps the existing 15 minute timeout budget, and honors
   `poll_after_ms` from the API when present.
9. Present comments to the user with file/line context.
10. For each comment, determine whether it is valid and applicable to the code.
11. If valid, incorporate the change in the codebase. If invalid, do not change
   the codebase.
12. Immediately call `scripts/post_comment_feedback.sh` for each comment with
    `comment_id`, `incorporated` true/false, and brief `notes` explaining the
    decision. Do not wait for user confirmation.

## Example (Production)

```bash
BASE_BRANCH=$(gh pr view --json baseRefName -q '.baseRefName' 2>/dev/null || git remote show origin | sed -n '/HEAD branch/s/.*: //p')
BASE_COMMIT=$(git rev-parse "$BASE_BRANCH")
HEAD_COMMIT=$(git rev-parse HEAD)
BRANCH=$(git rev-parse --abbrev-ref HEAD)
REPO_SLUG=$(git remote get-url origin | sed -E 's#(git@github.com:|https://github.com/)##; s/\\.git$//')
git diff "$BASE_BRANCH" > /tmp/review_api.diff

CREATE_RESPONSE=$(
  scripts/create_review.sh \
    --diff-file /tmp/review_api.diff \
    --repo "$REPO_SLUG" \
    --base-commit "$BASE_COMMIT" \
    --head-commit-sha "$HEAD_COMMIT" \
    --branch "$BRANCH"
)

REVIEW_ID=$(echo "$CREATE_RESPONSE" | jq -r '.review_id // empty')
if [ -z "$REVIEW_ID" ]; then
  echo "$CREATE_RESPONSE"
  exit 1
fi

scripts/poll_review.sh \
  --review-id "$REVIEW_ID" \
  --max-attempts 30 \
  --sleep-seconds 30 \
  --output-file /tmp/review_api.result.json

# The poller uses the 30x30s budget above, but will follow API-provided
# poll_after_ms hints when the server returns them.

cat /tmp/review_api.result.json

# Example feedback posts after deciding incorporate true/false per comment.
jq -c '.comments[]?' /tmp/review_api.result.json | while read -r comment; do
  COMMENT_ID=$(echo "$comment" | jq -r '.comment_id // empty')
  if [ -z "$COMMENT_ID" ]; then
    continue
  fi
  scripts/post_comment_feedback.sh \
    --review-id "$REVIEW_ID" \
    --comment-id "$COMMENT_ID" \
    --incorporated true \
    --notes "Applied in this branch."
done
```

## Troubleshooting

- `401/403` — re-run the pre-flight check above. The token may be missing,
  expired, or missing scopes. Guide the user to generate a new one at:
  https://app.propelcode.ai/administration/settings?tab=review-api-tokens&token_name=Claude+Code&scopes=reviews:read,reviews:write
- `404 {"error":"Repository not found"}` — the repository string does not match
  a repo connected to the account. Treat this as an access/config problem, not a retryable failure.
- `413` — the diff exceeded the 1,000,000 byte limit.

## Permission Handling Contract

If review creation returns `401`, `403`, or `404`, do all of the following:

1. Stop the review flow immediately (do not poll and do not retry in a loop).
2. Report the exact repository slug used.
3. Report an actionable next step:
   - `401/403`: "refresh token and confirm `reviews:read` + `reviews:write` scopes".
   - `404`: "connect this repository in Propel workspace, or correct owner/repo slug".
4. Mark the run as blocked until user intervention.

## Notes for Agents

- Do not log or expose tokens in output.
- Always use `https://api.propelcode.ai` until told otherwise.
- Use `scripts/create_review.sh`, `scripts/poll_review.sh`, and
  `scripts/post_comment_feedback.sh` instead of inline curl commands.
- The agent must decide whether each comment is valid, incorporate fixes when
  valid, and report feedback automatically via the feedback endpoint using the
  `comment_id` from the review response (no user confirmation required).
