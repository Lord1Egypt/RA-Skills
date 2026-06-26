# Git Integration for PingCode TimeLogger

## Supported Providers

### GitHub

**Fetch commits for a date range:**
```
GET https://api.github.com/repos/{owner}/{repo}/commits?author={username}&since={ISO8601}&until={ISO8601}
Authorization: Bearer <token>
```

Response: Array of commit objects. Key fields:
- `commit.message` — commit message (use first line as task title)
- `commit.author.date` — commit timestamp (for day grouping)
- `sha` — commit hash (for dedup)

**Pagination**: Follow `Link` header for next page. Default 30 per page, max 100 with `?per_page=100`.

### GitLab

**Fetch commits for a date range:**
```
GET {gitlab_url}/api/v4/projects/{project_id}/repository/commits?author={username}&since={ISO8601}&until={ISO8601}
PRIVATE-TOKEN: <token>
```

For project ID, use URL-encoded path: `GET /api/v4/projects/{url_encoded_path}/repository/commits`

Response: Array of commit objects. Key fields:
- `title` — commit message first line
- `committed_date` — timestamp
- `id` — commit hash

**Pagination**: Use `page` and `per_page` query params.

## Commit-to-Task Conversion

### Grouping Strategy
1. Fetch all commits in the date range across configured repos
2. Group by date (using commit timestamp, converted to CST)
3. Within each day, merge related commits:
   - Same prefix (e.g., `fix:`, `feat:`, `chore:`) → group together
   - Same ticket reference (e.g., `#123`, `JIRA-456`) → group together
4. Generate task title from grouped commits:
   - Single commit: Use first line of commit message
   - Multiple related: Summarize (e.g., "Bug fixes: auth timeout, null check, retry logic")

### Hour Distribution
- User provides total hours for the period
- Distribute proportionally by commit count per day
- Minimum 0.5h per day that has commits
- Round to nearest 0.5h
- Adjust last day to make total exact

### Example

User: "根据本周Git提交填8小时工时"

Commits found:
- Monday: 5 commits (auth module fixes)
- Tuesday: 3 commits (API endpoints)
- Wednesday: 0 commits
- Thursday: 2 commits (deploy config)
- Friday: 0 commits

Distribution (total 8h, 10 commits):
- Monday: 5/10 × 8 = 4.0h → "Auth模块问题修复"
- Tuesday: 3/10 × 8 = 2.5h → "API接口开发"
- Thursday: 2/10 × 8 = 1.5h → "部署配置调整"
- Total: 8.0h ✓
