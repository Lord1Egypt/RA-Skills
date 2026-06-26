---
name: jira-atlassian
description: |
  Full-featured Atlassian Jira Cloud REST API v3 skill. Manage issues, sprints, boards, epics, projects, users, and more via direct Jira API calls.
  Use when managing Jira issues, running JQL queries, creating tickets, managing sprints/boards, or interacting with Jira via API.
  Requires Atlassian email and API token for authentication.
metadata:
  author: jeffersonling1217-png
  version: "1.0.0"
  clawdbot:
    emoji: ✅
    homepage: https://clawhub.ai/jeffersonling1217-png/jira-atlassian
    requires:
      env:
        - JIRA_EMAIL
        - JIRA_API_TOKEN
        - JIRA_DOMAIN
---

# Jira Integration

Interact with Atlassian Jira Cloud via REST API v3.

## Authentication

Use **Basic Auth** with email and API token:

**Required Environment Variables:**
```bash
JIRA_EMAIL=your_email@example.com
JIRA_API_TOKEN=your_api_token
JIRA_DOMAIN=your_domain  # e.g. "yourcompany" for yourcompany.atlassian.net
```

**Credentials:**
- Email: `$JIRA_EMAIL`
- API Token: `$JIRA_API_TOKEN`
- Domain: `https://$JIRA_DOMAIN.atlassian.net`

**Base URL:**
```
https://$JIRA_DOMAIN.atlassian.net/rest/api/3
```

**Jira Software (Agile) Base URL:**
```
https://$JIRA_DOMAIN.atlassian.net/rest/agile/1.0
```

**Generate API Token:**
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Label it (e.g., "nanobot")
4. Copy the token

## Common Headers

```
Content-Type: application/json
Accept: application/json
Authorization: Basic base64(email:token)
```

---

# Complete API Reference

## Total API Summary

| Category | Count |
|----------|-------|
| **Total Endpoints** | 122 |
| **Total Schemas** | 64 |
| **Jira Software (Agile)** | 51 endpoints |
| **Builds API** | 9 endpoints |
| **Deployments API** | 7 endpoints |
| **DevInfo API** | 7 endpoints |
| **DevOps Components** | 7 endpoints |
| **Feature Flags** | 6 endpoints |
| **Operations** | 11 endpoints |
| **Remote Links** | 5 endpoints |
| **Security** | 13 endpoints |

---

## Jira Software (Agile) API

### Boards

#### Get All Boards
```
GET /rest/agile/1.0/board
```
Returns all boards visible to the user.

#### Create Board
```
POST /rest/agile/1.0/board
```
Body:
```json
{
  "name": "Sprint Board",
  "type": "scrum",
  "filterId": 12345,
  "location": {
    "type": "project",
    "projectKeyOrId": "PROJ"
  }
}
```

#### Get Board by ID
```
GET /rest/agile/1.0/board/{boardId}
```

#### Delete Board
```
DELETE /rest/agile/1.0/board/{boardId}
```

#### Get Board Configuration
```
GET /rest/agile/1.0/board/{boardId}/configuration
```
Returns board configuration including column config, estimation type, and ranking info.

#### Get Issues for Board
```
GET /rest/agile/1.0/board/{boardId}/issue
```
Query params: `startAt`, `maxResults`, `jql`, `validateQuery`, `fields`, `expand`

#### Move Issues to Board
```
POST /rest/agile/1.0/board/{boardId}/issue
```
Body:
```json
{
  "issues": ["PROJ-1", "PROJ-2"],
  "rankBeforeIssue": "PROJ-3",
  "rankAfterIssue": "PROJ-4",
  "rankCustomFieldId": 10001
}
```

#### Get Backlog Issues
```
GET /rest/agile/1.0/board/{boardId}/backlog
```

#### Move Issues to Backlog
```
POST /rest/agile/1.0/backlog/{boardId}/issue
```
Body:
```json
{
  "issues": ["PROJ-1", "PROJ-2"]
}
```

---

### Sprints

#### Get All Sprints
```
GET /rest/agile/1.0/board/{boardId}/sprint
```

#### Create Sprint
```
POST /rest/agile/1.0/sprint
```
Body:
```json
{
  "name": "Sprint 1",
  "originBoardId": 1,
  "startDate": "2024-01-15T00:00:00.000Z",
  "endDate": "2024-01-29T00:00:00.000Z",
  "goal": "Sprint 1 goal"
}
```

#### Get Sprint
```
GET /rest/agile/1.0/sprint/{sprintId}
```

#### Update Sprint (Full)
```
PUT /rest/agile/1.0/sprint/{sprintId}
```
Body:
```json
{
  "name": "Updated Sprint Name",
  "startDate": "2024-01-15T00:00:00.000Z",
  "endDate": "2024-01-29T00:00:00.000Z",
  "goal": "Updated goal",
  "state": "active"
}
```

#### Partially Update Sprint
```
POST /rest/agile/1.0/sprint/{sprintId}
```
Body:
```json
{
  "name": "Updated Name",
  "goal": "Updated goal",
  "state": "closed"
}
```

#### Delete Sprint
```
DELETE /rest/agile/1.0/sprint/{sprintId}
```

#### Get Issues for Sprint
```
GET /rest/agile/1.0/sprint/{sprintId}/issue
```

#### Move Issues to Sprint
```
POST /rest/agile/1.0/sprint/{sprintId}/issue
```
Body:
```json
{
  "issues": ["PROJ-1", "PROJ-2"]
}
```

#### Swap Sprint
```
POST /rest/agile/1.0/sprint/{sprintId}/swap
```
Body:
```json
{
  "sprintToSwapWith": 5
}
```

---

### Epics

#### Get Epics for Board
```
GET /rest/agile/1.0/board/{boardId}/epic
```

#### Get Epic
```
GET /rest/agile/1.0/epic/{epicIdOrKey}
```

#### Partially Update Epic
```
POST /rest/agile/1.0/epic/{epicIdOrKey}
```
Body:
```json
{
  "name": "Epic Name",
  "summary": "Epic summary",
  "color": "color_1",
  "done": false
}
```

#### Get Issues for Epic
```
GET /rest/agile/1.0/epic/{epicIdOrKey}/issue
```

#### Move Issues to Epic
```
POST /rest/agile/1.0/epic/{epicIdOrKey}/issue
```
Body:
```json
{
  "issues": ["PROJ-1", "PROJ-2"]
}
```

#### Rank Epics
```
PUT /rest/agile/1.0/epic/{epicIdOrKey}/rank
```
Body:
```json
{
  "rankBeforeEpic": "EPIC-2",
  "rankAfterEpic": "EPIC-3",
  "rankCustomFieldId": 10001
}
```

#### Get Issues Without Epic
```
GET /rest/agile/1.0/epic/none/issue
```

#### Remove Issues from Epic
```
POST /rest/agile/1.0/epic/none/issue
```
Body:
```json
{
  "issues": ["PROJ-1", "PROJ-2"]
}
```

---

### Issue Ranking

#### Rank Issues
```
PUT /rest/agile/1.0/issue/rank
```
Body:
```json
{
  "issues": ["PROJ-1", "PROJ-2"],
  "rankAfterIssue": "PROJ-3",
  "rankBeforeIssue": "PROJ-4",
  "rankCustomFieldId": 10001
}
```

#### Get Agile Issue
```
GET /rest/agile/1.0/issue/{issueIdOrKey}
```
Returns issue with Agile fields (sprint, closedSprints, flagged, epic).

#### Get Issue Estimation
```
GET /rest/agile/1.0/issue/{issueIdOrKey}/estimation?boardId={boardId}
```

#### Estimate Issue
```
PUT /rest/agile/1.0/issue/{issueIdOrKey}/estimation
```
Body:
```json
{
  "boardId": 1,
  "value": "3h"
}
```
Accepts formats: "1w", "2d", "3h", "20m" or number (minutes).

---

## Jira Platform API

### Issues (CRUD Operations)

#### Get Issue
```
GET /rest/api/3/issue/{issueIdOrKey}
```
Query params: `fields`, `expand`, `properties`, `updateHistory`
Examples:
- `GET /rest/api/3/issue/PROJ-123`
- `GET /rest/api/3/issue/PROJ-123?fields=summary,status,assignee`
- `GET /rest/api/3/issue/PROJ-123?expand=changelog`

#### Create Issue
```
POST /rest/api/3/issue
```
Body:
```json
{
  "fields": {
    "project": { "key": "PROJECT_KEY" },
    "summary": "Issue title",
    "description": {
      "type": "doc",
      "version": 1,
      "content": [
        { "type": "paragraph", "content": [{ "type": "text", "text": "Description" }] }
      ]
    },
    "issuetype": { "name": "Task" },
    "priority": { "id": "3" },
    "assignee": { "accountId": "USER_ACCOUNT_ID" }
  }
}
```

#### Edit Issue
```
PUT /rest/api/3/issue/{issueIdOrKey}
```
Body:
```json
{
  "fields": {
    "summary": "Updated summary",
    "description": { ... }
  },
  "update": {
    "labels": [
      { "add": "bugfix" },
      { "remove": "blocker" }
    ]
  }
}
```

#### Delete Issue
```
DELETE /rest/api/3/issue/{issueIdOrKey}?deleteSubtasks=true
```

#### Assign Issue
```
PUT /rest/api/3/issue/{issueIdOrKey}/assignee
```
Body:
```json
{
  "accountId": "USER_ACCOUNT_ID"
}
```
Use `"accountId": "-1"` for default assignee, `null` for unassigned.

---

### Search (JQL)

#### Search Issues
```
GET /rest/api/3/search?jql={jql}&startAt={offset}&maxResults={limit}&fields={fields}
```
Query params: `jql`, `startAt`, `maxResults`, `fields`, `expand`, `properties`
Examples:
- `GET /rest/api/3/search?jql=project=PMG ORDER BY created DESC`
- `GET /rest/api/3/search?jql=assignee=currentUser()&maxResults=50`

---

### Issue Operations

#### Get Transitions
```
GET /rest/api/3/issue/{issueIdOrKey}/transitions
```

#### Transition Issue
```
POST /rest/api/3/issue/{issueIdOrKey}/transitions
```
Body:
```json
{
  "transition": { "id": "21" }
}
```

#### Add Comment
```
POST /rest/api/3/issue/{issueIdOrKey}/comment
```
Body:
```json
{
  "body": {
    "type": "doc",
    "version": 1,
    "content": [
      { "type": "paragraph", "content": [{ "type": "text", "text": "Comment text" }] }
    ]
  }
}
```

#### Send Notification
```
POST /rest/api/3/issue/{issueIdOrKey}/notify
```
Body:
```json
{
  "subject": "Subject",
  "textBody": "Body text",
  "to": { "reporter": true },
  "restrict": { "group": { "name": "jira-software-users" } }
}
```

---

### Issue Metadata

#### Get Create Issue Metadata
```
GET /rest/api/3/issue/createmeta?projectKeys={project}&issuetypeNames={type}
```

#### Get Edit Metadata
```
GET /rest/api/3/issue/{issueIdOrKey}/editmeta
```

#### Get Create Metadata for Project
```
GET /rest/api/3/issue/createmeta/{projectIdOrKey}/issuetypes
```

#### Get Create Metadata for Project & Issue Type
```
GET /rest/api/3/issue/createmeta/{projectIdOrKey}/issuetypes/{issueTypeId}
```

---

### Bulk Operations

#### Bulk Create Issues (up to 50)
```
POST /rest/api/3/issue/bulk
```
Body:
```json
{
  "issueUpdates": [
    { "fields": { "project": { "key": "PROJ" }, "summary": "...", "issuetype": { "name": "Task" } } },
    { "fields": { "project": { "key": "PROJ" }, "summary": "...", "issuetype": { "name": "Bug" } } }
  ]
}
```

#### Bulk Fetch Issues (up to 100)
```
POST /rest/api/3/issue/bulkfetch
```
Body:
```json
{
  "issueIdsOrKeys": ["PROJ-1", "PROJ-2", "10005"],
  "fields": ["summary", "project", "status", "assignee"],
  "properties": []
}
```

#### Bulk Fetch Changelogs
```
POST /rest/api/3/changelog/bulkfetch
```
Body:
```json
{
  "issueIdsOrKeys": ["PROJ-1", "PROJ-2"],
  "fieldIds": ["status", "assignee"],
  "maxResults": 100
}
```

#### Get Changelogs
```
GET /rest/api/3/issue/{issueIdOrKey}/changelog?startAt=0&maxResults=50
```

#### Get Changelogs by IDs
```
POST /rest/api/3/issue/{issueIdOrKey}/changelog/list
```
Body:
```json
{
  "changelogIds": [10001, 10002]
}
```

---

### Projects

#### Get Projects
```
GET /rest/api/3/project
```

#### Get Project
```
GET /rest/api/3/project/{projectIdOrKey}
```

---

### Users

#### Get User
```
GET /rest/api/3/user?accountId={accountId}
```

#### Get Current User (Myself)
```
GET /rest/api/3/myself
```

#### Search Users
```
GET /rest/api/3/user/search?query={query}&maxResults={limit}
```

---

### Issue Events

#### Get Events (Admin)
```
GET /rest/api/3/events
```

---

## DevOps Integration APIs

### Build Information API

#### Submit Build Data
```
POST /rest/builds/0.1/bulk
```
**Note:** Requires Connect JWT token or OAuth token for on-premise integration.

#### Get Build by Key
```
GET /rest/builds/0.1/pipelines/{pipelineId}/builds/{buildNumber}
```

---

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Bad request or malformed data |
| 401 | Invalid credentials or expired token |
| 403 | Permission denied |
| 404 | Resource not found |
| 409 | Conflict |
| 429 | Rate limited - wait and retry |
| 500 | Internal server error |

---

## Notes

- **JQL (Jira Query Language)**: Use JQL for powerful issue search and filtering
- **Issue IDs vs Keys**: Use `PROJ-123` format for keys, numeric ID for direct lookups
- **Transition IDs**: Get available transitions first via `GET /rest/api/3/issue/{key}/transitions`
- **Account IDs**: Jira Cloud uses account IDs for users - get them via the users API
- **Bulk Operations**: Use bulk endpoints for efficiency when creating/fetching multiple issues
- **Expand**: Use `?expand=changelog` on issue GET to retrieve full change history
