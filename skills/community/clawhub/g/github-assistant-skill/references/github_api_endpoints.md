# GitHub REST API Endpoints Reference

## Authentication
- Header: `Authorization: token <TOKEN>`
- Token scopes needed: `repo`, `public_repo`, `notifications`
- Fine-grained PAT: 需要配置具体的仓库权限

## Trending (No official API)
- Browser URL: `https://github.com/trending[/{language}]?since={daily|weekly|monthly}`
- Fallback: Search API `GET /search/repositories?q=created:>2024-01-01&sort=stars`

## Search
- `GET /search/repositories?q={query}&sort=stars&order=desc&per_page=25`
- `GET /search/users?q={query}`
- `GET /search/issues?q={query}`
- Query syntax: `language:python stars:>1000 topic:ai`

## Repository Info
- `GET /repos/{owner}/{repo}`
- `GET /repos/{owner}/{repo}/languages`
- `GET /repos/{owner}/{repo}/contributors`

## Star Operations
- Star: `PUT /user/starred/{owner}/{repo}` (no body)
- Unstar: `DELETE /user/starred/{owner}/{repo}`
- List starred: `GET /user/starred`
- Check if starred: `GET /user/starred/{owner}/{repo}` (204 = starred, 404 = not starred)

## Fork
- Fork: `POST /repos/{owner}/{repo}/forks`
- List forks: `GET /repos/{owner}/{repo}/forks`

## Watch (Subscription)
- Watch: `PUT /repos/{owner}/{repo}/subscription` body: `{"subscribed": true}`
- Unwatch: `DELETE /repos/{owner}/{repo}/subscription`
- Check: `GET /repos/{owner}/{repo}/subscription`

## Issues
- List issues: `GET /repos/{owner}/{repo}/issues?state=open&per_page=100`
- Get issue: `GET /repos/{owner}/{repo}/issues/{issue_number}`
- Create issue: `POST /repos/{owner}/{repo}/issues` body: `{"title": "...", "body": "...", "labels": [...]}`
- Update issue: `PATCH /repos/{owner}/{repo}/issues/{issue_number}` body: `{"title": "...", "body": "...", "state": "open|closed"}`
- Close issue: `PATCH /repos/{owner}/{repo}/issues/{issue_number}` body: `{"state": "closed"}`
- Reopen issue: `PATCH /repos/{owner}/{repo}/issues/{issue_number}` body: `{"state": "open"}`
- Lock issue: `PUT /repos/{owner}/{repo}/issues/{issue_number}/lock` body: `{"lock_reason": "off-topic|too heated|resolved|spam"}`
- Unlock issue: `DELETE /repos/{owner}/{repo}/issues/{issue_number}/lock`

## Issue Labels
- List labels: `GET /repos/{owner}/{repo}/labels`
- Add labels: `POST /repos/{owner}/{repo}/issues/{issue_number}/labels` body: `{"labels": ["bug", "help wanted"]}`
- Remove label: `DELETE /repos/{owner}/{repo}/issues/{issue_number}/labels/{name}`
- Set labels (replace all): `PUT /repos/{owner}/{repo}/issues/{issue_number}/labels` body: `{"labels": ["bug"]}`

## Issue Comments
- List comments: `GET /repos/{owner}/{repo}/issues/{issue_number}/comments`
- Create comment: `POST /repos/{owner}/{repo}/issues/{issue_number}/comments` body: `{"body": "..."}`
- Update comment: `PATCH /repos/{owner}/{repo}/issues/comments/{comment_id}` body: `{"body": "..."}`
- Delete comment: `DELETE /repos/{owner}/{repo}/issues/comments/{comment_id}`

## Pull Requests
- List PRs: `GET /repos/{owner}/{repo}/pulls?state=open&per_page=100`
- Get PR: `GET /repos/{owner}/{repo}/pulls/{pull_number}`
- Create PR: `POST /repos/{owner}/{repo}/pulls` body: `{"title": "...", "head": "branch", "base": "main", "body": "..."}`
- Update PR: `PATCH /repos/{owner}/{repo}/pulls/{pull_number}` body: `{"title": "...", "body": "...", "state": "open|closed"}`
- Close PR: `PATCH /repos/{owner}/{repo}/pulls/{pull_number}` body: `{"state": "closed"}`
- Merge PR: `PUT /repos/{owner}/{repo}/pulls/{pull_number}/merge` body: `{"commit_title": "...", "merge_method": "merge|squash|rebase"}`
- Check mergeability: `GET /repos/{owner}/{repo}/pulls/{pull_number}` → check `mergeable` field

## PR Reviews
- List reviews: `GET /repos/{owner}/{repo}/pulls/{pull_number}/reviews`
- Create review: `POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews` body: `{"body": "...", "event": "APPROVE|REQUEST_CHANGES|COMMENT"}`
- Submit review: `POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/events` body: `{"body": "...", "event": "APPROVE|REQUEST_CHANGES|COMMENT"}`
- Request reviewers: `POST /repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers` body: `{"reviewers": ["username"]}`

## PR Comments (Review Comments)
- List comments: `GET /repos/{owner}/{repo}/pulls/{pull_number}/comments`
- Create comment: `POST /repos/{owner}/{repo}/pulls/{pull_number}/comments` body: `{"body": "...", "path": "file.py", "line": 10, "side": "RIGHT"}`
- Reply to comment: `POST /repos/{owner}/{repo}/pulls/{pull_number}/comments` body: `{"body": "...", "in_reply_to": comment_id}`

## Repository Contents (Files)
- Get file: `GET /repos/{owner}/{repo}/contents/{path}?ref={branch}`
- Create file: `PUT /repos/{owner}/{repo}/contents/{path}` body: `{"message": "commit msg", "content": base64_content, "branch": "main"}`
- Update file: `PUT /repos/{owner}/{repo}/contents/{path}` body: `{"message": "...", "content": base64_content, "sha": file_sha, "branch": "..."}`
- Delete file: `DELETE /repos/{owner}/{repo}/contents/{path}` body: `{"message": "...", "sha": file_sha, "branch": "..."}`
- Get README: `GET /repos/{owner}/{repo}/readme`

## Branches
- List branches: `GET /repos/{owner}/{repo}/branches`
- Get branch: `GET /repos/{owner}/{repo}/branches/{branch}`
- Create branch: `POST /repos/{owner}/{repo}/git/refs` body: `{"ref": "refs/heads/new-branch", "sha": "commit_sha"}`
- Delete branch: `DELETE /repos/{owner}/{repo}/git/refs/heads/{branch}`
- Branch protection: `PUT /repos/{owner}/{repo}/branches/{branch}/protection`

## Releases
- List releases: `GET /repos/{owner}/{repo}/releases`
- Get release: `GET /repos/{owner}/{repo}/releases/{release_id}`
- Create release: `POST /repos/{owner}/{repo}/releases` body: `{"tag_name": "v1.0", "name": "Release 1.0", "body": "..."}`
- Update release: `PATCH /repos/{owner}/{repo}/releases/{release_id}` body: `{"name": "...", "body": "..."}`
- Delete release: `DELETE /repos/{owner}/{repo}/releases/{release_id}`
- Upload asset: `POST https://uploads.github.com/repos/{owner}/{repo}/releases/{release_id}/assets?name={filename}`

## Actions (Workflows)
- List workflows: `GET /repos/{owner}/{repo}/actions/workflows`
- List runs: `GET /repos/{owner}/{repo}/actions/runs?status=success|failure|in_progress`
- Get run: `GET /repos/{owner}/{repo}/actions/runs/{run_id}`
- Trigger workflow: `POST /repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches` body: `{"ref": "main", "inputs": {...}}`
- Cancel run: `POST /repos/{owner}/{repo}/actions/runs/{run_id}/cancel`
- Re-run: `POST /repos/{owner}/{repo}/actions/runs/{run_id}/rerun`
- Get logs: `GET /repos/{owner}/{repo}/actions/runs/{run_id}/logs`
- List jobs: `GET /repos/{owner}/{repo}/actions/runs/{run_id}/jobs`

## Create Repository
- Create for authenticated user: `POST /user/repos` body: `{"name": "...", "description": "...", "private": false}`
- Create in org: `POST /orgs/{org}/repos` body: `{"name": "...", "private": false}`

## User
- Current user: `GET /user`
- User profile: `GET /users/{username}`
- Update profile: `PATCH /user` body: `{"name": "...", "bio": "..."}`
- Follow user: `PUT /user/following/{username}`
- Unfollow user: `DELETE /user/following/{username}`
- Check following: `GET /user/following/{username}` (204 = following, 404 = not following)

## Notifications
- List notifications: `GET /notifications?all=false&participating=false`
- Mark as read: `PUT /notifications` body: `{"last_read_at": "2024-01-01T00:00:00Z"}`
- Get thread: `GET /notifications/threads/{thread_id}`
- Mark thread read: `PATCH /notifications/threads/{thread_id}` body: `{"read": true}`

## Organizations
- List orgs: `GET /user/orgs`
- Get org: `GET /orgs/{org}`
- List org repos: `GET /orgs/{org}/repos`

## Rate Limits
- Check: `GET /rate_limit`
- Unauthenticated: 60 requests/hour
- Authenticated: 5,000 requests/hour
- Search API: 30 requests/minute (authenticated)

## Common Error Codes
- 200: Success
- 201: Created
- 204: Success (no content)
- 304: Not modified
- 400: Bad request
- 401: Unauthorized (bad credentials)
- 403: Forbidden (rate limit or permission denied)
- 404: Not found
- 409: Conflict
- 422: Validation error

## Best Practices
1. Always use authentication for higher rate limits
2. Handle 403 errors with exponential backoff
3. Use conditional requests with `If-None-Match` header (ETag)
4. Paginate with `Link` header or `?page=N&per_page=100`
5. Cache responses when possible
6. Use `Accept: application/vnd.github.v3+json` header
