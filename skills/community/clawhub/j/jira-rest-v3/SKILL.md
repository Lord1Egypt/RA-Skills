# File: skills/jira-rest-v3/SKILL.md

# openClaw Skill — Jira Daily Work via ATREST (Jira Cloud REST API v3 + Jira Software Agile API)

## What this skill is for
Use this skill to perform everyday Jira work from openClaw:
- find and triage issues (JQL search)
- read and update issues (fields, assignee, workflow transition)
- create issues
- manage comments (list, add, update, delete)
- log time (worklogs)
- work with boards, backlog, and sprints (Jira Software Agile API)

This skill assumes Jira Cloud.

---

## Most important rule for openClaw
When a user explicitly asks for Jira work, or when a task clearly requires Jira data, **do not merely describe the REST API**.

You MUST do all of the following:
1. map the user request to a concrete Jira REST endpoint
2. build the final HTTP method + URL + query + headers + body
3. execute a **real CLI HTTP call** from the current OS environment
4. parse the JSON response
5. report the result back to the user in a concise human-readable format

If the environment is Linux, prefer `curl`.
If the environment is Windows, prefer **either** `curl.exe` **or** PowerShell `Invoke-RestMethod`.

Never stop at “the API endpoint would be …”. The skill is only considered applied when the actual CLI request is made.

---

## Required environment variables (openclaw.json -> "env")
All variables MUST use the `ATREST_` prefix.

### Jira site + authentication
- `ATREST_JIRA_BASE_URL`
  - Example: `https://your-domain.atlassian.net`
  - Do NOT include a trailing slash.
- `ATREST_JIRA_AUTH_MODE`
  - `basic` (recommended for scripts) or `bearer`
- `ATREST_JIRA_EMAIL`
  - Required when `ATREST_JIRA_AUTH_MODE=basic`
- `ATREST_JIRA_API_TOKEN`
  - Required when `ATREST_JIRA_AUTH_MODE=basic`
- `ATREST_JIRA_BEARER_TOKEN`
  - Required when `ATREST_JIRA_AUTH_MODE=bearer`
- `ATREST_JIRA_USER_AGENT`
  - Example: `openClaw-jira-atrest/1.0`

### Defaults (optional but practical)
- `ATREST_JIRA_DEFAULT_PROJECT_KEY`
- `ATREST_JIRA_DEFAULT_ISSUE_TYPE`
  - Example: `Task`, `Bug`, `Story`
- `ATREST_JIRA_DEFAULT_BOARD_ID`
- `ATREST_JIRA_DEFAULT_MAX_RESULTS`
  - Example: `50`
- `ATREST_JIRA_DEFAULT_FIELDS`
  - Comma-separated list for search/read, e.g. `summary,status,assignee,priority,updated`

### Resilience (optional)
- `ATREST_HTTP_TIMEOUT_MS` (e.g. `30000`)
- `ATREST_HTTP_RETRY_MAX` (e.g. `3`)
- `ATREST_HTTP_RETRY_BACKOFF_MS` (e.g. `1000`)

See also: `refs/openclaw_env_example.json`.

---

## API base paths (two families)
1) Jira Cloud *Platform* REST API v3 (issues, comments, projects, users, worklogs, …)
- Base: `${ATREST_JIRA_BASE_URL}/rest/api/3`

2) Jira Software *Agile* REST API (boards, sprints, backlog, ranking, …)
- Base: `${ATREST_JIRA_BASE_URL}/rest/agile/1.0`

When selecting an endpoint, always choose the correct base family first.
- issue, comment, worklog, project, user => Platform v3
- board, backlog, sprint => Agile API

---

## Authentication rules (must follow)
### If AUTH_MODE = basic
- Use HTTP Basic Auth with **email + API token**.
- Either:
  - set `Authorization: Basic <base64(email:apiToken)>`, or
  - use the HTTP client’s built-in basic auth feature.

### If AUTH_MODE = bearer
- Set `Authorization: Bearer ${ATREST_JIRA_BEARER_TOKEN}`

Never print secrets, never echo tokens into logs, never store tokens in repo.

---

## Rich-text fields (ADF)
Jira Cloud v3 uses Atlassian Document Format (ADF) for:
- issue `description`, `environment`, and textarea custom fields
- comment `body`
- worklog `comment`

When the user provides plain text, wrap it into minimal ADF.
See `refs/jira-json-quickref.md#adf-minimal`.

---

## CLI execution contract (this is the part openClaw must follow)
For every Jira command, execute the request through the OS shell.

### Mandatory workflow
1. Verify required environment variables exist.
2. Decide whether the endpoint belongs to Platform v3 or Agile API.
3. Build the final path.
4. Add query parameters.
5. Build headers:
   - `Accept: application/json`
   - `Content-Type: application/json` for requests with JSON body
   - `User-Agent: ${ATREST_JIRA_USER_AGENT}` if set
   - `Authorization: ...` according to auth mode
6. For `POST` and `PUT`, write the JSON body into a temporary file whenever the payload is non-trivial.
7. Execute the request via CLI.
8. Parse the response JSON.
9. If needed, paginate.
10. Present the result to the user.

### Never do this
- do not only describe the endpoint without calling it
- do not invent Jira data without an HTTP request
- do not inline large JSON payloads into shell commands if quoting is likely to break
- do not expose token values in terminal output

---

## Canonical transport on Linux
Use Bash + `curl`.

### Linux preflight
```bash
: "${ATREST_JIRA_BASE_URL:?Missing ATREST_JIRA_BASE_URL}"
: "${ATREST_JIRA_AUTH_MODE:?Missing ATREST_JIRA_AUTH_MODE}"
```

### Linux auth handling
```bash
JIRA_BASE="${ATREST_JIRA_BASE_URL}"
JIRA_UA="${ATREST_JIRA_USER_AGENT:-openClaw-jira-atrest/1.0}"

if [ "${ATREST_JIRA_AUTH_MODE}" = "basic" ]; then
  : "${ATREST_JIRA_EMAIL:?Missing ATREST_JIRA_EMAIL}"
  : "${ATREST_JIRA_API_TOKEN:?Missing ATREST_JIRA_API_TOKEN}"
  AUTH_HEADER="Authorization: Basic $(printf '%s' "${ATREST_JIRA_EMAIL}:${ATREST_JIRA_API_TOKEN}" | base64 | tr -d '\n')"
elif [ "${ATREST_JIRA_AUTH_MODE}" = "bearer" ]; then
  : "${ATREST_JIRA_BEARER_TOKEN:?Missing ATREST_JIRA_BEARER_TOKEN}"
  AUTH_HEADER="Authorization: Bearer ${ATREST_JIRA_BEARER_TOKEN}"
else
  echo "Unsupported ATREST_JIRA_AUTH_MODE=${ATREST_JIRA_AUTH_MODE}" >&2
  exit 1
fi
```

### Linux generic GET template
```bash
curl --silent --show-error --fail \
  --request GET \
  --url "${JIRA_BASE}/rest/api/3/issue/PROJ-123?fields=summary,status,assignee,updated" \
  --header "Accept: application/json" \
  --header "$AUTH_HEADER" \
  --header "User-Agent: ${JIRA_UA}"
```

### Linux generic POST/PUT template with temp file
```bash
cat > /tmp/jira-body.json <<'JSON'
{
  "fields": {
    "project": { "key": "PROJ" },
    "issuetype": { "name": "Task" },
    "summary": "Created from openClaw"
  }
}
JSON

curl --silent --show-error --fail \
  --request POST \
  --url "${JIRA_BASE}/rest/api/3/issue" \
  --header "Accept: application/json" \
  --header "Content-Type: application/json" \
  --header "$AUTH_HEADER" \
  --header "User-Agent: ${JIRA_UA}" \
  --data-binary @/tmp/jira-body.json
```

### Linux parsing guidance
- If `jq` is available, use it for formatting and extraction.
- Otherwise return raw JSON or parse minimally with the shell.

Example:
```bash
curl --silent --show-error --fail ... | jq -r '.key, .fields.summary'
```

---

## Canonical transport on Windows
Use **either** PowerShell `Invoke-RestMethod` **or** `curl.exe`.

Important:
- In Windows PowerShell / PowerShell, `curl` can be an alias.
- To force the native curl client, call **`curl.exe`** explicitly.

### Windows PowerShell preflight
```powershell
if (-not $env:ATREST_JIRA_BASE_URL) { throw "Missing ATREST_JIRA_BASE_URL" }
if (-not $env:ATREST_JIRA_AUTH_MODE) { throw "Missing ATREST_JIRA_AUTH_MODE" }
```

### Windows PowerShell auth handling
```powershell
$JiraBase = $env:ATREST_JIRA_BASE_URL.TrimEnd('/')
$JiraUa   = if ($env:ATREST_JIRA_USER_AGENT) { $env:ATREST_JIRA_USER_AGENT } else { 'openClaw-jira-atrest/1.0' }

if ($env:ATREST_JIRA_AUTH_MODE -eq 'basic') {
    if (-not $env:ATREST_JIRA_EMAIL) { throw 'Missing ATREST_JIRA_EMAIL' }
    if (-not $env:ATREST_JIRA_API_TOKEN) { throw 'Missing ATREST_JIRA_API_TOKEN' }
    $pair = "{0}:{1}" -f $env:ATREST_JIRA_EMAIL, $env:ATREST_JIRA_API_TOKEN
    $basic = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($pair))
    $AuthHeader = "Basic $basic"
}
elseif ($env:ATREST_JIRA_AUTH_MODE -eq 'bearer') {
    if (-not $env:ATREST_JIRA_BEARER_TOKEN) { throw 'Missing ATREST_JIRA_BEARER_TOKEN' }
    $AuthHeader = "Bearer $($env:ATREST_JIRA_BEARER_TOKEN)"
}
else {
    throw "Unsupported ATREST_JIRA_AUTH_MODE=$($env:ATREST_JIRA_AUTH_MODE)"
}

$Headers = @{
    Accept        = 'application/json'
    Authorization = $AuthHeader
    'User-Agent'  = $JiraUa
}
```

### Windows PowerShell generic GET template
```powershell
$response = Invoke-RestMethod `
  -Method Get `
  -Uri "$JiraBase/rest/api/3/issue/PROJ-123?fields=summary,status,assignee,updated" `
  -Headers $Headers

$response.key
$response.fields.summary
```

### Windows PowerShell generic POST/PUT template with temp file
```powershell
$payload = @{
    fields = @{
        project   = @{ key = 'PROJ' }
        issuetype = @{ name = 'Task' }
        summary   = 'Created from openClaw'
    }
} | ConvertTo-Json -Depth 20

$tmp = Join-Path $env:TEMP 'jira-body.json'
Set-Content -Path $tmp -Value $payload -Encoding UTF8

$Headers['Content-Type'] = 'application/json'
$response = Invoke-RestMethod `
  -Method Post `
  -Uri "$JiraBase/rest/api/3/issue" `
  -Headers $Headers `
  -Body (Get-Content -Path $tmp -Raw)
```

### Windows native curl template
```powershell
curl.exe --silent --show-error --fail `
  --request GET `
  --url "$JiraBase/rest/api/3/issue/PROJ-123?fields=summary,status,assignee,updated" `
  --header "Accept: application/json" `
  --header "Authorization: $AuthHeader" `
  --header "User-Agent: $JiraUa"
```

---

## Reusable helper pattern (recommended for openClaw)
Whenever possible, define one reusable request helper in the active shell session and use it for all Jira calls.

A ready-to-copy reference is provided in:
- `refs/cli-rest-quickref.md`

This dramatically increases the chance that openClaw actually performs the HTTP call instead of drifting into abstract API discussion.

---

## Request building rules by command type
### GET requests
- Build final URL with encoded query parameters.
- Prefer querystring parameters over JSON body.
- Safe for: reads, searches, list operations.

### POST requests
- Prefer JSON temp file for non-trivial body.
- Use for: issue create, comment add, transitions apply, sprint create, sprint add issues, worklog add.

### PUT requests
- Prefer JSON temp file for non-trivial body.
- Use for: issue edit, assign, comment update, sprint update.

### DELETE requests
- Only execute when user intent is explicit.
- Require confirmation unless the user already clearly asked to delete.

---

## Response handling rules
### Success
- `200` / `201`: parse and summarize JSON response
- `204`: report success, then optionally follow up with a GET if the user expects the updated resource

### Error handling
- `400`: invalid payload, invalid JQL, missing required fields, or bad field ids
- `401`: missing or invalid authentication
- `403`: authenticated but missing permission or blocked by project/board rules
- `404`: resource not found, wrong key/id, or inaccessible resource
- `409`: conflict (workflow/state/business rule)
- `429`: rate limit; respect `Retry-After` if present, then retry with backoff

Always explain the Jira-specific cause as clearly as possible.

---

## Pagination rules
### Platform v3 issue search
For `jira.issues.searchJql`:
- use `nextPageToken` until `isLast=true`
- if the user only asked for a quick answer, stop after a reasonable page size and summarize

### StartAt-based endpoints
For endpoints that use `startAt` and `maxResults`:
- loop until all required items are collected or the user-requested limit is reached

---

## Command-to-HTTP execution mapping
The following mappings are normative. They are not examples only; they define how openClaw should actually perform the CLI call.

# Command Catalog

## 1) Projects & Users (Platform v3)

### jira.projects.search
- GET `/rest/api/3/project/search`
- Query: `startAt`, `maxResults`, optional filters supported by Jira
- Use for: selecting a project id/key, listing available projects
- Output: id, key, name, projectTypeKey/style if available
- CLI rule: perform a GET request against the Platform v3 base path

### jira.users.search
- GET `/rest/api/3/user/search`
- Query: `query` (string), optional pagination params supported by Jira
- Use for: resolving a person name or email fragment into `accountId`
- CLI rule: perform a GET request against the Platform v3 base path

---

## 2) Issue search & read (Platform v3)

### jira.issues.searchJql (Enhanced search)
- GET `/rest/api/3/search/jql` (or POST for very long JQL)
- Query: `jql`, `nextPageToken`, `maxResults`, `fields[]`, `expand`, `properties[]`, `fieldsByKeys`, `failFast`, `reconcileIssues[]`
- Pagination: use `nextPageToken` until `isLast=true`
- Default: use `ATREST_JIRA_DEFAULT_MAX_RESULTS` and `ATREST_JIRA_DEFAULT_FIELDS` if provided
- Output: list of issues with key fields
- CLI rule: encode JQL correctly; for Linux prefer `--get --data-urlencode` or a fully encoded URL; for PowerShell prefer a URI string with encoded query parameters

### jira.issues.get
- GET `/rest/api/3/issue/{issueIdOrKey}`
- Query: `fields` (comma-separated or array, depending on client), `expand`
- Output: key, summary, status, assignee, description (ADF), priority, labels, updated
- CLI rule: perform a GET request and summarize requested fields only

### jira.issues.changelog
- GET `/rest/api/3/issue/{issueIdOrKey}/changelog`
- Query: `startAt`, `maxResults`
- Output: recent changes (field, from, to, author, created)
- CLI rule: paginate if the user asks for full history

---

## 3) Create & update issues (Platform v3)

### jira.issues.create
- POST `/rest/api/3/issue`
- Body: see `refs/jira-json-quickref.md#issue-create`
- Required fields: `project`, `issuetype`, `summary`
- Common optional: `description` (ADF), `priority`, `labels`, `assignee` (accountId)
- Output: created issue key + self link
- CLI rule: always write non-trivial JSON to a temp file before POSTing

### jira.issues.edit
- PUT `/rest/api/3/issue/{issueIdOrKey}`
- Query: `notifyUsers`, `returnIssue`, `overrideScreenSecurity`, `overrideEditableFlag`, `expand`
- Body: `fields` and/or `update` (operations)
- Rule: transitions are NOT done here; use the transitions endpoint instead
- Body reference: `refs/jira-json-quickref.md#issue-edit`
- Output: `204` unless `returnIssue=true`
- CLI rule: always use a JSON body file for operation-based updates

### jira.issues.assign
- PUT `/rest/api/3/issue/{issueIdOrKey}/assignee`
- Body: `{ "accountId": "..." }` (or `null` for unassigned where allowed)
- Use for: assigning to a user by accountId
- Output: `204`
- CLI rule: resolve accountId first if needed, then execute the PUT request

### jira.issues.transitions.list
- GET `/rest/api/3/issue/{issueIdOrKey}/transitions`
- Query: `expand`, optional filters supported by Jira
- Use for: retrieving available workflow transitions and ids
- Output: list transitions: id, name, to.status
- CLI rule: do this first if the user names a status but not a transition id

### jira.issues.transitions.apply
- POST `/rest/api/3/issue/{issueIdOrKey}/transitions`
- Body: `{ "transition": { "id": "X" }, ... }` optionally plus `update.comment.add` etc.
- Body reference: `refs/jira-json-quickref.md#issue-transition`
- Output: `204`
- CLI rule: if the user said “move to Done”, first list transitions, map the human name to the transition id, then apply the POST request

### jira.issues.delete  (destructive)
- DELETE `/rest/api/3/issue/{issueIdOrKey}`
- Query: `deleteSubtasks` (optional)
- Require explicit user intent before calling
- Output: `204`
- CLI rule: never execute unless the user explicitly asked to delete

---

## 4) Comments (Platform v3)

### jira.comments.list
- GET `/rest/api/3/issue/{issueIdOrKey}/comment`
- Query: `startAt`, `maxResults`, `orderBy`, `expand`
- Output: comment id, author, created/updated, body (ADF), visibility
- CLI rule: parse and present comment text in readable form when possible

### jira.comments.add
- POST `/rest/api/3/issue/{issueIdOrKey}/comment`
- Body: `{ "body": <ADF>, "visibility": <optional>, "properties": <optional> }`
- Body reference: `refs/jira-json-quickref.md#comment-add`
- Output: created comment (id, timestamps, body)
- CLI rule: if the user provides plain text, convert it to minimal ADF before POSTing

### jira.comments.update
- PUT `/rest/api/3/issue/{issueIdOrKey}/comment/{id}`
- Body: same shape as add (`body` / `visibility` / `properties`)
- Output: updated comment
- CLI rule: use a temp JSON file for the body

### jira.comments.delete  (destructive)
- DELETE `/rest/api/3/issue/{issueIdOrKey}/comment/{id}`
- Require explicit user intent before calling
- Output: `204`
- CLI rule: same destructive-action safeguards as issue delete

---

## 5) Worklogs (Platform v3)

### jira.worklogs.list
- GET `/rest/api/3/issue/{issueIdOrKey}/worklog`
- Output: worklog entries (id, author, started, timeSpentSeconds, comment ADF)
- CLI rule: if the user wants totals, sum `timeSpentSeconds`

### jira.worklogs.add
- POST `/rest/api/3/issue/{issueIdOrKey}/worklog`
- Body reference: `refs/jira-json-quickref.md#worklog-add`
- Output: created worklog
- CLI rule: create ADF comment only when the user supplied text

---

## 6) Boards & Sprints (Agile API)

### jira.boards.list
- GET `/rest/agile/1.0/board`
- Query: `startAt`, `maxResults`, filters like `type`, `name`, `projectKeyOrId`, etc.
- Output: board id, name, type
- CLI rule: use Agile API base path, not Platform v3

### jira.boards.get
- GET `/rest/agile/1.0/board/{boardId}`
- Output: board details (location, type)
- CLI rule: use Agile API base path

### jira.boards.backlog
- GET `/rest/agile/1.0/board/{boardId}/backlog`
- Query: `startAt`, `maxResults`, `jql`, `fields`, `expand`
- Output: backlog issues
- CLI rule: use Agile API base path and paginate if required

### jira.boards.issues
- GET `/rest/agile/1.0/board/{boardId}/issue`
- Query: `startAt`, `maxResults`, `jql`, `fields`, `expand`
- Output: issues currently on the board (by board column mapping)
- CLI rule: use Agile API base path

### jira.boards.sprints
- GET `/rest/agile/1.0/board/{boardId}/sprint`
- Query: `startAt`, `maxResults`, `state`
- Output: sprints (id, name, state, dates)
- CLI rule: use Agile API base path

### jira.boards.sprint.issues
- GET `/rest/agile/1.0/board/{boardId}/sprint/{sprintId}/issue`
- Query: `startAt`, `maxResults`, optional filters
- Output: issues in that sprint (board view)
- CLI rule: use Agile API base path

---

## 7) Sprint lifecycle (Agile API)

### jira.sprints.create
- POST `/rest/agile/1.0/sprint`
- Body reference: `refs/jira-json-quickref.md#sprint-create`
- Output: created sprint
- CLI rule: always post JSON via temp file or serialized body string

### jira.sprints.get
- GET `/rest/agile/1.0/sprint/{sprintId}`
- Output: sprint details
- CLI rule: use Agile API base path

### jira.sprints.update
- PUT `/rest/agile/1.0/sprint/{sprintId}`
- Body: full sprint object fields
- Important: missing fields may be nulled depending on request shape and endpoint semantics
- Use for: rename, goal, start, close by state changes when allowed
- CLI rule: read sprint first when there is any risk of overwriting fields unintentionally

### jira.sprints.issues
- GET `/rest/agile/1.0/sprint/{sprintId}/issue`
- Output: sprint issues
- CLI rule: use Agile API base path

### jira.sprints.addIssues
- POST `/rest/agile/1.0/sprint/{sprintId}/issue`
- Body: `{ "issues": ["PROJ-1", "PROJ-2", ...] }`
- Output: `204` on success
- CLI rule: send exact issue keys in the JSON body

---

## Practical command examples that openClaw can imitate exactly
These are concrete examples to reduce ambiguity.

### Search issues by JQL on Linux
```bash
JQL='project = PROJ AND statusCategory != Done ORDER BY updated DESC'
curl --silent --show-error --fail --get \
  --url "${JIRA_BASE}/rest/api/3/search/jql" \
  --data-urlencode "jql=${JQL}" \
  --data-urlencode "maxResults=${ATREST_JIRA_DEFAULT_MAX_RESULTS:-50}" \
  --data-urlencode "fields=${ATREST_JIRA_DEFAULT_FIELDS:-summary,status,assignee,priority,updated}" \
  --header "Accept: application/json" \
  --header "$AUTH_HEADER" \
  --header "User-Agent: ${JIRA_UA}"
```

### Search issues by JQL on Windows PowerShell
```powershell
$jql = 'project = PROJ AND statusCategory != Done ORDER BY updated DESC'
$maxResults = if ($env:ATREST_JIRA_DEFAULT_MAX_RESULTS) { $env:ATREST_JIRA_DEFAULT_MAX_RESULTS } else { '50' }
$uri = "$JiraBase/rest/api/3/search/jql?maxResults=$maxResults&fields=summary,status,assignee,priority,updated&jql=$([uri]::EscapeDataString($jql))"
Invoke-RestMethod -Method Get -Uri $uri -Headers $Headers
```

### Add a comment from plain text on Linux
```bash
cat > /tmp/comment.json <<'JSON'
{
  "body": {
    "type": "doc",
    "version": 1,
    "content": [
      {
        "type": "paragraph",
        "content": [
          { "type": "text", "text": "Work completed and verified." }
        ]
      }
    ]
  }
}
JSON

curl --silent --show-error --fail \
  --request POST \
  --url "${JIRA_BASE}/rest/api/3/issue/PROJ-123/comment" \
  --header "Accept: application/json" \
  --header "Content-Type: application/json" \
  --header "$AUTH_HEADER" \
  --header "User-Agent: ${JIRA_UA}" \
  --data-binary @/tmp/comment.json
```

### Transition an issue on Windows PowerShell
```powershell
$transitionPayload = @{
    transition = @{ id = '31' }
} | ConvertTo-Json -Depth 10

$Headers['Content-Type'] = 'application/json'
Invoke-RestMethod `
  -Method Post `
  -Uri "$JiraBase/rest/api/3/issue/PROJ-123/transitions" `
  -Headers $Headers `
  -Body $transitionPayload
```

---

## Output conventions (recommended)
When replying to the user after an API call:
- For issue lists: show `KEY — Summary (Status) [Assignee] updated <date>`
- For single issue: show key fields + the user-requested detail (description/comments/etc.)
- For updates/transitions: confirm what changed + resulting status/assignee
- For failures: report the HTTP status and the Jira-relevant reason in plain English

---

## Recommendations that improve openClaw reliability
These are strongly recommended additions to prompts and agent behavior.

### 1) Force execution language
Add wording like:
- “For every `jira.*` action, execute a real CLI HTTP request. Do not stop at endpoint explanation.”
- “On Linux use `curl`; on Windows use `curl.exe` or `Invoke-RestMethod`.”

### 2) Force JSON temp files for write operations
Add wording like:
- “For POST/PUT bodies larger than one line, always write JSON to a temp file first.”

This prevents the most common quoting failures.

### 3) Force an execution transcript shape
Require the agent to think in this order:
1. selected command
2. selected endpoint
3. constructed URL
4. constructed body file if any
5. executed CLI request
6. summarized response

### 4) Add a minimal Jira connectivity self-test
Before complex Jira work, allow the agent to verify connectivity with a harmless call such as:
- `GET /rest/api/3/myself`
- or `GET /rest/api/3/project/search?maxResults=1`

### 5) Keep one canonical transport per OS
Do not let the agent improvise between many different HTTP clients.
- Linux: `curl`
- Windows: `Invoke-RestMethod` or `curl.exe`

### 6) Resolve names before mutating data
For assignees, transitions, board ids, and sprint ids, first resolve the exact Jira identifier, then perform the write operation.

---

## Quickref — embedding app data into Jira issue text
For patterns and ready-to-copy ADF payload snippets, including an example for “ContentCraft: Mermaid Diagrams for Jira”, see:
- `refs/app-embedding-quickref.md`

---

## JSON and CLI references
- `refs/jira-json-quickref.md` (payload shapes, short parameter notes, ADF helper)
- `refs/jql-cheatsheet.md` (ready-to-use JQL patterns)
- `refs/openclaw_env_example.json` (env snippet)
- `refs/app-embedding-quickref.md` (how to embed app data into Jira text bodies; includes ContentCraft Mermaid example)
- `refs/cli-rest-quickref.md` (Linux Bash + Windows PowerShell reusable request helpers and concrete REST execution examples)
