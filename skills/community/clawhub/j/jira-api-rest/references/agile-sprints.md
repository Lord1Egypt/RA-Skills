# Agile (boards/sprints) — Jira Cloud REST

Uses Jira Agile REST API (separate from core /rest/api/3):

Base: `/rest/agile/1.0`

## Boards
- List boards: `GET /board?maxResults=...&projectKeyOrId=DES`
- Board details: `GET /board/{boardId}`
- Board sprints: `GET /board/{boardId}/sprint?state=active|future|closed&maxResults=...`

## Sprints
- Sprint details: `GET /sprint/{sprintId}`
- Sprint issues: `GET /sprint/{sprintId}/issue?fields=...&jql=...&maxResults=...`
- Create sprint: `POST /sprint` body: `{ "name": "...", "originBoardId": 184, "startDate": "...", "endDate": "..." }`
- Update sprint: `PUT /sprint/{sprintId}` body: `{ "name": "...", "state": "active|closed|future", ... }`

## Practical notes
- Jira may require `startDate/endDate` as ISO timestamps.
- Moving sprint states (future→active→closed) is done via `PUT /sprint/{id}` with `state`.
