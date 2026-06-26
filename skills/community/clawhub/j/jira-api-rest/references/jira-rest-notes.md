# Jira REST notes (focused)

This skill uses Jira Cloud REST API v3.

## Auth

- Prefer **Basic auth** with Atlassian API token.
- In this workspace, credentials are typically stored in `~/.netrc`:
  - machine: `<your-domain>.atlassian.net`
  - login: `<email>`
  - password: `<api_token>`

Never print or paste tokens in chat.

## Endpoints used by the scripts

### Search by JQL (new)

Atlassian is migrating from `/rest/api/3/search` → `/rest/api/3/search/jql`.

- `GET /rest/api/3/search/jql?jql=...&maxResults=50&fields=key,summary,status`

### Worklogs

- List: `GET /rest/api/3/issue/{issueKey}/worklog`
- Delete: `DELETE /rest/api/3/issue/{issueKey}/worklog/{worklogId}?adjustEstimate=auto`
- Update: `PUT /rest/api/3/issue/{issueKey}/worklog/{worklogId}`
  - Body supports fields like `timeSpent`, `started`, and `comment` (ADF).

Estimate adjustment params (query string):
- `adjustEstimate=auto|new|leave`
- `newEstimate=...` (when `adjustEstimate=new`)

## ADF comment format (minimal)

```json
{
  "comment": {
    "type": "doc",
    "version": 1,
    "content": [
      {"type": "paragraph", "content": [{"type": "text", "text": "your text"}]}
    ]
  }
}
```
