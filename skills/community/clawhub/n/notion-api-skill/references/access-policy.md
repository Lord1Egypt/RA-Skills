# Notion access policy

An access policy limits which endpoints Notion connections may call through Maton. Notion doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/notion#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Notion: its 34 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create notion --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v1/ai/plugins"},
    {"method": "GET", "path": "v1/ai/plugins/{id}"},
    {"method": "GET", "path": "v1/ai/skills/{id}"},
    {"method": "POST", "path": "v1/agents/query"},
    {"method": "GET", "path": "v1/agents/{id}"},
    {"method": "GET", "path": "v1/agents/{id}/insights"},
    {"method": "GET", "path": "v1/blocks/{id}"},
    {"method": "GET", "path": "v1/blocks/{id}/children"},
    {"method": "GET", "path": "v1/comments"},
    {"method": "GET", "path": "v1/comments/{id}"},
    {"method": "GET", "path": "v1/custom_emojis"},
    {"method": "GET", "path": "v1/data_sources/{id}"},
    {"method": "POST", "path": "v1/data_sources/{id}/query"},
    {"method": "GET", "path": "v1/data_sources/{id}/templates"},
    {"method": "GET", "path": "v1/databases"},
    {"method": "GET", "path": "v1/databases/{id}"},
    {"method": "POST", "path": "v1/databases/{id}/query"},
    {"method": "GET", "path": "v1/file_uploads"},
    {"method": "GET", "path": "v1/file_uploads/{id}"},
    {"method": "POST", "path": "v1/blocks/meeting_notes/query"},
    {"method": "GET", "path": "v1/pages/{id}"},
    {"method": "GET", "path": "v1/pages/{id}/markdown"},
    {"method": "GET", "path": "v1/pages/{id}/properties/{id}"},
    {"method": "POST", "path": "v1/search"},
    {"method": "POST", "path": "v1/sessions/query"},
    {"method": "GET", "path": "v1/sessions/{id}"},
    {"method": "POST", "path": "v1/sessions/{id}/events/query"},
    {"method": "GET", "path": "v1/users"},
    {"method": "GET", "path": "v1/users/me"},
    {"method": "GET", "path": "v1/users/{id}"},
    {"method": "GET", "path": "v1/views"},
    {"method": "GET", "path": "v1/views/{id}"},
    {"method": "POST", "path": "v1/views/{id}/queries"},
    {"method": "GET", "path": "v1/views/{id}/queries/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Notion endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v1/ai/plugins | read | agent_skills | List the plugins available to your connection. |
| GET | v1/ai/plugins/{id} | read | agent_skills | Download a plugin directory containing skills and supporting files. |
| GET | v1/ai/skills/{id} | read | agent_skills | Download a skill directory containing its instructions and supporting files. |
| POST | v1/ai/skills/{id}/upload | write | agent_skills | Upload a skill directory archive to a skill page in one request. |
| POST | v1/agents/batch | write | agents | Asynchronously apply multiple agent management operations. |
| POST | v1/agents/query | read | agents | Find the Custom Agents and personal agent that an integration can access. |
| GET | v1/agents/{id} | read | agents | Retrieve metadata for one accessible Custom Agent or the personal agent. |
| PATCH | v1/agents/{id} | write | agents | Change a Custom Agent's or the personal agent's name, model, status, and other settings in one request. |
| DELETE | v1/agents/{id} | write | agents | Soft-delete a Custom Agent with a personal access token. |
| PATCH | v1/agents/{id}/credit_limit | write | agents | Set or clear the credit limit for a Custom Agent. |
| GET | v1/agents/{id}/insights | read | agents | Retrieve configuration and usage insights for a Custom Agent or the authenticated user's personal agent. |
| PATCH | v1/agents/{id}/status | write | agents | Enable or disable a Custom Agent (deprecated). |
| GET | v1/blocks/{id} | read | blocks | Retrieves a Block object using the ID specified. |
| PATCH | v1/blocks/{id} | write | blocks | Update a block. |
| DELETE | v1/blocks/{id} | write | blocks | Delete a block. |
| GET | v1/blocks/{id}/children | read | blocks | Returns a paginated array of child block objects contained in the block using the ID specified. |
| PATCH | v1/blocks/{id}/children | write | blocks | Creates and appends new children blocks to the parent block_id specified. |
| GET | v1/comments | read | comments | Retrieves a list of un-resolved Comment objects from a page or block. |
| POST | v1/comments | write | comments | Creates a comment on a page, block, or existing discussion thread. |
| GET | v1/comments/{id} | read | comments | Retrieves a Comment object from its comment_id. |
| PATCH | v1/comments/{id} | write | comments | Updates a comment by its comment_id. |
| DELETE | v1/comments/{id} | write | comments | Deletes a comment by its comment_id. |
| GET | v1/custom_emojis | read | custom_emojis | Retrieves a list of custom emojis in the workspace. |
| POST | v1/data_sources | write | data_sources | Create a data source. |
| GET | v1/data_sources/{id} | read | data_sources | Retrieve a data source. |
| PATCH | v1/data_sources/{id} | write | data_sources | Update a data source. |
| POST | v1/data_sources/{id}/query | read | data_sources | Query a data source. |
| GET | v1/data_sources/{id}/templates | read | data_sources | List the page templates your connection can read in a data source. |
| GET | v1/databases | read | databases | Legacy list of databases shared with the connection, only on API versions up to 2021-08-16. |
| POST | v1/databases | write | databases | Create a database. |
| GET | v1/databases/{id} | read | databases | Retrieve a database. |
| PATCH | v1/databases/{id} | write | databases | Update a database. |
| POST | v1/databases/{id}/query | read | databases | Legacy database query, deprecated as of version 2025-09-03; use data source query. |
| GET | v1/file_uploads | read | file_uploads | Use this API to retrieve file uploads for the current bot connection, sorted by most recent first. |
| POST | v1/file_uploads | write | file_uploads | Use this API to initiate the process of uploading a file to your Notion workspace. |
| GET | v1/file_uploads/{id} | read | file_uploads | Use this API to get the details of a File Upload object. |
| POST | v1/file_uploads/{id}/complete | write | file_uploads | Use this API to finalize a mode=multi_part file upload after all of the parts have been sent successfully. |
| POST | v1/file_uploads/{id}/send | write | file_uploads | Use this API to transmit file contents to Notion for a file upload. |
| POST | v1/blocks/meeting_notes | write | meeting_notes | Creates AI meeting notes from an uploaded audio or video file. |
| POST | v1/blocks/meeting_notes/query | read | meeting_notes | Query meeting notes for the workspace with optional filters, sorts, and a result limit. |
| POST | v1/meeting_notes | write | meeting_notes | Creates a full-page meeting note, or gets or creates the meeting note for a calendar event. |
| PATCH | v1/meeting_notes/{id} | write | meeting_notes | Links an existing full-page meeting note to a calendar event. |
| POST | v1/pages | write | pages | Use this API to create a new page as a child of an existing page or data source. |
| GET | v1/pages/{id} | read | pages | Retrieve a page. |
| PATCH | v1/pages/{id} | write | pages | Use this API to modify attributes of a Notion page, such as its properties, icon, or cover. |
| GET | v1/pages/{id}/markdown | read | pages | Retrieve the content of a page rendered as markdown. |
| PATCH | v1/pages/{id}/markdown | write | pages | Insert or replace content in a page using markdown. |
| POST | v1/pages/{id}/move | write | pages | Use this API to move an existing Notion page to a new parent. |
| GET | v1/pages/{id}/properties/{id} | read | pages | Retrieve a page property item. |
| POST | v1/search | read | search | Find pages and data sources by title. |
| POST | v1/sessions | write | sessions | Start a session, send a message, submit an action, or stream a session turn. |
| POST | v1/sessions/query | read | sessions | Find agent sessions that an integration can access. |
| GET | v1/sessions/{id} | read | sessions | Retrieve the status, metadata, and required actions for a session. |
| POST | v1/sessions/{id}/cancel | write | sessions | Cancel an in-progress session. |
| POST | v1/sessions/{id}/events/query | read | sessions | Retrieve a page of events from an accessible session. |
| GET | v1/users | read | users | Returns a paginated list of Users for the workspace. |
| GET | v1/users/me | read | users | Retrieves the User associated with the token provided in the authorization header. |
| GET | v1/users/{id} | read | users | Retrieves a User using the ID specified. |
| GET | v1/views | read | views | List all views in a database. |
| POST | v1/views | write | views | Create a new view on a database or add a widget view to a dashboard. |
| GET | v1/views/{id} | read | views | Retrieve a view by its ID. |
| PATCH | v1/views/{id} | write | views | Update a view's name, filter, sorts, or configuration. |
| DELETE | v1/views/{id} | write | views | Delete a view from a database. |
| POST | v1/views/{id}/queries | read | views | Execute a view's query and return the first page of results. |
| GET | v1/views/{id}/queries/{id} | read | views | Paginate through cached view query results. |
| DELETE | v1/views/{id}/queries/{id} | write | views | Delete a cached view query. |
