# GitLab REST API v4 Reference Manual

> Source: https://gitlab.fullnine.com.cn/help/api/index.md
> API Version: v4
> Base URL: `https://gitlab.fullnine.com.cn/api/v4`

## Authentication

All API requests require authentication via one of:

| Method | Header/Param | Example |
|--------|-------------|---------|
| Private Token | `PRIVATE-TOKEN` header | `curl -H "PRIVATE-TOKEN: <token>" URL` |
| Private Token | `private_token` query param | `curl "URL?private_token=<token>"` |
| OAuth2 Token | `Authorization: Bearer` header | `curl -H "Authorization: Bearer <token>" URL` |

Create a Personal Access Token at: `https://gitlab.fullnine.com.cn/-/profile/personal_access_tokens`

Required scopes: `api` (full access) or `read_api` (read-only).

---

## Pagination

| Parameter | Description | Default |
|-----------|-------------|---------|
| `page` | Page number | 1 |
| `per_page` | Items per page | 20 (max: 100) |

Response headers: `x-total`, `x-total-pages`, `x-page`, `x-per-page`, `x-next-page`, `x-prev-page`

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - GET/PUT/DELETE succeeded |
| 201 | Created - POST succeeded |
| 204 | No Content - DELETE succeeded |
| 304 | Not Modified |
| 400 | Bad Request - missing/invalid params |
| 401 | Unauthorized - invalid/missing token |
| 403 | Forbidden - insufficient permissions |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Unprocessable Entity |
| 429 | Too Many Requests (rate limited) |
| 500 | Server Error |

---

## Project Resources

### Projects API

| Action | Method | Endpoint | Key Params |
|--------|--------|----------|------------|
| List all projects | GET | `/projects` | `search`, `owned`, `membership`, `visibility`, `archived`, `order_by`, `sort`, `simple` |
| List user projects | GET | `/users/:user_id/projects` | `search`, `visibility` |
| Get single project | GET | `/projects/:id` | `statistics`, `license` |
| Create project | POST | `/projects` | `name`(req), `path`, `description`, `visibility`, `namespace_id`, `initialize_with_readme`, `default_branch` |
| Edit project | PUT | `/projects/:id` | `name`, `description`, `visibility`, `default_branch` |
| Delete project | DELETE | `/projects/:id` | |
| Fork project | POST | `/projects/:id/fork` | `namespace`, `name`, `path` |
| Get project users | GET | `/projects/:id/users` | `search` |
| List project groups | GET | `/projects/:id/groups` | `search` |

### Branches API

| Action | Method | Endpoint | Key Params |
|--------|--------|----------|------------|
| List branches | GET | `/projects/:id/repository/branches` | `search` |
| Get branch | GET | `/projects/:id/repository/branches/:branch` | |
| Create branch | POST | `/projects/:id/repository/branches` | `branch`(req), `ref`(req) |
| Delete branch | DELETE | `/projects/:id/repository/branches/:branch` | |
| Delete merged branches | DELETE | `/projects/:id/repository/merged_branches` | |

### Commits API

| Action | Method | Endpoint | Key Params |
|--------|--------|----------|------------|
| List commits | GET | `/projects/:id/repository/commits` | `ref_name`, `since`, `until`, `path`, `all` |
| Get single commit | GET | `/projects/:id/repository/commits/:sha` | |
| Get commit diff | GET | `/projects/:id/repository/commits/:sha/diff` | |
| List commit comments | GET | `/projects/:id/repository/commits/:sha/comments` | |
| Post commit comment | POST | `/projects/:id/repository/commits/:sha/comments` | `note`(req), `path`, `line`, `line_type` |

### Repository API

| Action | Method | Endpoint | Key Params |
|--------|--------|----------|------------|
| List repository tree | GET | `/projects/:id/repository/tree` | `path`, `ref`, `recursive`, `per_page` |
| Get file metadata | GET | `/projects/:id/repository/files/:file_path` | `ref`(req) |
| Get raw file content | GET | `/projects/:id/repository/files/:file_path/raw` | `ref` |
| Create new file | POST | `/projects/:id/repository/files/:file_path` | `branch`(req), `content`(req), `commit_message`(req), `encoding` |
| Update file | PUT | `/projects/:id/repository/files/:file_path` | `branch`(req), `content`(req), `commit_message`(req) |
| Delete file | DELETE | `/projects/:id/repository/files/:file_path` | `branch`(req), `commit_message`(req) |
| Compare branches/tags | GET | `/projects/:id/repository/compare` | `from`(req), `to`(req) |

### Tags API

| Action | Method | Endpoint | Key Params |
|--------|--------|----------|------------|
| List tags | GET | `/projects/:id/repository/tags` | `search`, `order_by`, `sort` |
| Create tag | POST | `/projects/:id/repository/tags` | `tag_name`(req), `ref`(req), `message`, `release_description` |
| Delete tag | DELETE | `/projects/:id/repository/tags/:tag_name` | |

### Issues API

| Action | Method | Endpoint | Key Params |
|--------|--------|----------|------------|
| List all issues | GET | `/issues` | `scope`, `state`, `labels`, `milestone`, `search`, `assignee_id`, `author_id` |
| List project issues | GET | `/projects/:id/issues` | `state`, `labels`, `milestone`, `assignee_id`, `search`, `order_by`, `sort`, `created_after`, `created_before` |
| List group issues | GET | `/groups/:id/issues` | `state`, `labels`, `milestone`, `search` |
| Get single issue | GET | `/projects/:id/issues/:issue_iid` | |
| Create issue | POST | `/projects/:id/issues` | `title`(req), `description`, `labels`, `assignee_ids`, `milestone_id`, `due_date`, `confidential` |
| Edit issue | PUT | `/projects/:id/issues/:issue_iid` | `title`, `description`, `state_event`, `labels`, `assignee_ids`, `add_labels`, `remove_labels` |
| Delete issue | DELETE | `/projects/:id/issues/:issue_iid` | |
| List issue notes | GET | `/projects/:id/issues/:issue_iid/notes` | `sort`, `order_by` |
| Create issue note | POST | `/projects/:id/issues/:issue_iid/notes` | `body`(req) |
| List issue links | GET | `/projects/:id/issues/:issue_iid/links` | |

### Merge Requests API

| Action | Method | Endpoint | Key Params |
|--------|--------|----------|------------|
| List all MRs | GET | `/merge_requests` | `scope`, `state`, `labels`, `milestone`, `search`, `source_branch`, `target_branch` |
| List project MRs | GET | `/projects/:id/merge_requests` | `state`, `labels`, `milestone`, `source_branch`, `target_branch`, `search`, `order_by`, `sort` |
| List group MRs | GET | `/groups/:id/merge_requests` | `state`, `labels`, `milestone`, `search` |
| Get single MR | GET | `/projects/:id/merge_requests/:mr_iid` | `include_diverged_commits_count`, `include_rebase_in_progress` |
| Create MR | POST | `/projects/:id/merge_requests` | `source_branch`(req), `target_branch`(req), `title`(req), `description`, `assignee_id`, `reviewer_ids`, `labels`, `milestone_id`, `remove_source_branch`, `squash` |
| Update MR | PUT | `/projects/:id/merge_requests/:mr_iid` | `title`, `description`, `state_event`, `labels`, `assignee_id`, `reviewer_ids` |
| Merge MR | PUT | `/projects/:id/merge_requests/:mr_iid/merge` | `merge_commit_message`, `squash`, `should_remove_source_branch`, `merge_when_pipeline_succeeds` |
| Get MR changes | GET | `/projects/:id/merge_requests/:mr_iid/changes` | `access_raw_diffs` |
| Get MR commits | GET | `/projects/:id/merge_requests/:mr_iid/commits` | |
| Get MR participants | GET | `/projects/:id/merge_requests/:mr_iid/participants` | |
| List MR notes | GET | `/projects/:id/merge_requests/:mr_iid/notes` | `sort`, `order_by` |
| Create MR note | POST | `/projects/:id/merge_requests/:mr_iid/notes` | `body`(req) |
| Approve MR | POST | `/projects/:id/merge_requests/:mr_iid/approve` | |
| Unapprove MR | POST | `/projects/:id/merge_requests/:mr_iid/unapprove` | |
| List MR pipelines | GET | `/projects/:id/merge_requests/:mr_iid/pipelines` | |

### Pipelines API

| Action | Method | Endpoint | Key Params |
|--------|--------|----------|------------|
| List pipelines | GET | `/projects/:id/pipelines` | `scope`, `status`, `ref`, `sha`, `yaml_errors`, `order_by`, `sort` |
| Get pipeline | GET | `/projects/:id/pipelines/:pipeline_id` | |
| Create pipeline | POST | `/projects/:id/pipeline` | `ref`(req), `variables` (array of key/value) |
| Retry pipeline | POST | `/projects/:id/pipelines/:pipeline_id/retry` | |
| Cancel pipeline | POST | `/projects/:id/pipelines/:pipeline_id/cancel` | |
| Delete pipeline | DELETE | `/projects/:id/pipelines/:pipeline_id` | |
| List pipeline jobs | GET | `/projects/:id/pipelines/:pipeline_id/jobs` | `scope` |
| Get job log/trace | GET | `/projects/:id/jobs/:job_id/trace` | _(returns plain text)_ |

### Labels API

| Action | Method | Endpoint | Key Params |
|--------|--------|----------|------------|
| List labels | GET | `/projects/:id/labels` | `with_counts` |
| Create label | POST | `/projects/:id/labels` | `name`(req), `color`(req), `description`, `priority` |
| Update label | PUT | `/projects/:id/labels/:label_id` | `new_name`, `color`, `description`, `priority` |
| Delete label | DELETE | `/projects/:id/labels/:label_id` | |

### Milestones API

| Action | Method | Endpoint | Key Params |
|--------|--------|----------|------------|
| List milestones | GET | `/projects/:id/milestones` | `iids`, `state`, `search` |
| Get milestone | GET | `/projects/:id/milestones/:milestone_id` | |
| Create milestone | POST | `/projects/:id/milestones` | `title`(req), `description`, `due_date`, `start_date` |
| Update milestone | PUT | `/projects/:id/milestones/:milestone_id` | `title`, `description`, `due_date`, `start_date`, `state_event` |
| Delete milestone | DELETE | `/projects/:id/milestones/:milestone_id` | |

### Releases API

| Action | Method | Endpoint | Key Params |
|--------|--------|----------|------------|
| List releases | GET | `/projects/:id/releases` | `order_by`, `sort` |
| Get release | GET | `/projects/:id/releases/:tag_name` | |
| Create release | POST | `/projects/:id/releases` | `tag_name`(req), `name`, `description`, `ref`, `milestones` |
| Update release | PUT | `/projects/:id/releases/:tag_name` | `name`, `description`, `milestones`, `released_at` |
| Delete release | DELETE | `/projects/:id/releases/:tag_name` | |

### Snippets API

| Action | Method | Endpoint | Key Params |
|--------|--------|----------|------------|
| List project snippets | GET | `/projects/:id/snippets` | |
| Get snippet | GET | `/projects/:id/snippets/:snippet_id` | |
| Create snippet | POST | `/projects/:id/snippets` | `title`(req), `file_name`(req), `content`, `visibility` |
| Update snippet | PUT | `/projects/:id/snippets/:snippet_id` | `title`, `file_name`, `content`, `visibility` |
| Delete snippet | DELETE | `/projects/:id/snippets/:snippet_id` | |

### Members API

| Action | Method | Endpoint | Key Params |
|--------|--------|----------|------------|
| List project members | GET | `/projects/:id/members` | `query`, `user_ids` |
| List group members | GET | `/groups/:id/members` | `query`, `user_ids` |
| Get member | GET | `/projects/:id/members/:user_id` | |
| Add member | POST | `/projects/:id/members` | `user_id`(req), `access_level`(req) |
| Edit member | PUT | `/projects/:id/members/:user_id` | `access_level`(req) |
| Remove member | DELETE | `/projects/:id/members/:user_id` | |

### Webhooks (Hooks) API

| Action | Method | Endpoint | Key Params |
|--------|--------|----------|------------|
| List project hooks | GET | `/projects/:id/hooks` | |
| Get hook | GET | `/projects/:id/hooks/:hook_id` | |
| Add hook | POST | `/projects/:id/hooks` | `url`(req), `push_events`, `merge_requests_events`, `issues_events`, `token`, `enable_ssl_verification` |
| Edit hook | PUT | `/projects/:id/hooks/:hook_id` | `url`, `push_events`, `merge_requests_events`, `issues_events` |
| Delete hook | DELETE | `/projects/:id/hooks/:hook_id` | |

---

## Group Resources

### Groups API

| Action | Method | Endpoint | Key Params |
|--------|--------|----------|------------|
| List groups | GET | `/groups` | `search`, `owned`, `min_access_level`, `order_by`, `sort` |
| Get group | GET | `/groups/:id` | `with_projects` |
| List subgroups | GET | `/groups/:id/subgroups` | `search`, `owned`, `order_by`, `sort` |
| List group projects | GET | `/groups/:id/projects` | `search`, `visibility`, `order_by`, `sort` |
| Create group | POST | `/groups` | `name`(req), `path`(req), `description`, `visibility`, `parent_id` |
| Update group | PUT | `/groups/:id` | `name`, `path`, `description`, `visibility` |
| Delete group | DELETE | `/groups/:id` | |

---

## Standalone Resources

### Users API

| Action | Method | Endpoint | Key Params |
|--------|--------|----------|------------|
| List users | GET | `/users` | `search`, `username`, `active`, `blocked`, `external` |
| Get current user | GET | `/user` | |
| Get single user | GET | `/users/:id` | |
| Get user projects | GET | `/users/:id/projects` | `order_by`, `sort` |
| List SSH keys | GET | `/user/keys` | |

### Search API

| Action | Method | Endpoint | Key Params |
|--------|--------|----------|------------|
| Global search | GET | `/search` | `scope`(req), `search`(req) |
| Group search | GET | `/groups/:id/search` | `scope`(req), `search`(req) |
| Project search | GET | `/projects/:id/search` | `scope`(req), `search`(req) |

**Search scopes:**
- Global: `projects`, `issues`, `merge_requests`, `milestones`, `snippet_titles`, `users`
- Group: `projects`, `issues`, `merge_requests`, `milestones`
- Project: `issues`, `merge_requests`, `milestones`, `notes`, `wiki_blobs`, `commits`, `blobs`

### Runners API

| Action | Method | Endpoint | Key Params |
|--------|--------|----------|------------|
| List owned runners | GET | `/runners` | `scope`, `type`, `status` |
| List all runners (admin) | GET | `/runners/all` | `scope`, `type`, `status` |
| Get runner details | GET | `/runners/:id` | |
| List project runners | GET | `/projects/:id/runners` | `scope`, `type`, `status` |

### Version API

| Action | Method | Endpoint |
|--------|--------|----------|
| Get version | GET | `/version` |

### Namespaces API

| Action | Method | Endpoint | Key Params |
|--------|--------|----------|------------|
| List namespaces | GET | `/namespaces` | `search` |
| Get namespace | GET | `/namespaces/:id` | |

---

## Access Levels

| Value | Role |
|-------|------|
| 10 | Guest |
| 20 | Reporter |
| 30 | Developer |
| 40 | Maintainer |
| 50 | Owner |

## Project Visibility

| Value | Description |
|-------|-------------|
| `private` | Access must be granted explicitly |
| `internal` | Any signed-in user can clone (except external users) |
| `public` | No authentication required |

## Merge Methods

| Value | Description |
|-------|-------------|
| `merge` | Merge commit created for every merge |
| `rebase_merge` | Merge commit + fast-forward required |
| `ff` | Fast-forward only, no merge commits |

## Issue/MR State Events

Use `state_event` parameter to change state:
- Issues: `close`, `reopen`
- Merge Requests: `close`, `reopen`

## Date Format

All dates use ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`

Examples:
- `2024-01-15T08:00:00Z`
- `2024-12-31` (for due dates)

## URL Encoding

- Namespaced paths: encode `/` as `%2F` (e.g., `my-group%2Fmy-project`)
- File paths in repository: URL-encode the full path (e.g., `src%2FREADME.md`)
- Branch names with `/`: URL-encode (e.g., `feature%2Fmy-branch`)
