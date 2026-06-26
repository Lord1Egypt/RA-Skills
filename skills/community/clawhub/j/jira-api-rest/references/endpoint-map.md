# Endpoint map (Jira Cloud REST v3)

This is a pragmatic mapping from common `jira-cli` operations to REST endpoints.

## Identity
- me: `GET /rest/api/3/myself`

## Projects
- list/search projects: `GET /rest/api/3/project/search`

## Issues
- get issue: `GET /rest/api/3/issue/{key}?fields=...&expand=...`
- create issue: `POST /rest/api/3/issue`
- edit issue fields: `PUT /rest/api/3/issue/{key}`
- add comment: `POST /rest/api/3/issue/{key}/comment`
- transitions list: `GET /rest/api/3/issue/{key}/transitions`
- transition: `POST /rest/api/3/issue/{key}/transitions`
- assign: `PUT /rest/api/3/issue/{key}/assignee`
- user search (resolve accountId): `GET /rest/api/3/user/search?query=...`
- link issues: `POST /rest/api/3/issueLink`

## Search (JQL)
- JQL search (new): `GET /rest/api/3/search/jql?jql=...`
  - Atlassian migration from `/rest/api/3/search` (deprecated/410).

## Worklogs
- list: `GET /rest/api/3/issue/{key}/worklog`
- add: `POST /rest/api/3/issue/{key}/worklog`
- update: `PUT /rest/api/3/issue/{key}/worklog/{id}`
- delete: `DELETE /rest/api/3/issue/{key}/worklog/{id}`

Query params for update/delete:
- `adjustEstimate=auto|new|leave`
- `newEstimate=...` (when `adjustEstimate=new`)
