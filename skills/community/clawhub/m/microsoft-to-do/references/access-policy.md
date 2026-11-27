# Microsoft To Do access policy

An access policy limits which endpoints Microsoft To Do connections may call through Maton. Microsoft To Do doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/microsoft-to-do#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Microsoft To Do: its 44 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create microsoft-to-do --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v1.0/me/todo/lists/**"},
    {"method": "GET", "path": "v1.0/me/todo"},
    {"method": "GET", "path": "v1.0/me/todo/lists"},
    {"method": "GET", "path": "v1.0/me/todo/lists/delta"},
    {"method": "GET", "path": "v1.0/me/todo/lists/{id}"},
    {"method": "GET", "path": "v1.0/me/todo/lists/{id}/extensions"},
    {"method": "GET", "path": "v1.0/me/todo/lists/{id}/extensions/{id}"},
    {"method": "GET", "path": "v1.0/users/{id}/todo/lists/**"},
    {"method": "GET", "path": "v1.0/users/{id}/todo"},
    {"method": "GET", "path": "v1.0/users/{id}/todo/lists"},
    {"method": "GET", "path": "v1.0/users/{id}/todo/lists/delta"},
    {"method": "GET", "path": "v1.0/users/{id}/todo/lists/{id}"},
    {"method": "GET", "path": "v1.0/users/{id}/todo/lists/{id}/extensions"},
    {"method": "GET", "path": "v1.0/users/{id}/todo/lists/{id}/extensions/{id}"},
    {"method": "GET", "path": "v1.0/me/todo/lists/{id}/tasks"},
    {"method": "GET", "path": "v1.0/me/todo/lists/{id}/tasks/delta"},
    {"method": "GET", "path": "v1.0/me/todo/lists/{id}/tasks/{id}"},
    {"method": "GET", "path": "v1.0/me/todo/lists/{id}/tasks/{id}/extensions"},
    {"method": "GET", "path": "v1.0/me/todo/lists/{id}/tasks/{id}/extensions/{id}"},
    {"method": "GET", "path": "v1.0/users/{id}/todo/lists/{id}/tasks"},
    {"method": "GET", "path": "v1.0/users/{id}/todo/lists/{id}/tasks/delta"},
    {"method": "GET", "path": "v1.0/users/{id}/todo/lists/{id}/tasks/{id}"},
    {"method": "GET", "path": "v1.0/users/{id}/todo/lists/{id}/tasks/{id}/extensions"},
    {"method": "GET", "path": "v1.0/users/{id}/todo/lists/{id}/tasks/{id}/extensions/{id}"},
    {"method": "GET", "path": "v1.0/me/todo/lists/{id}/tasks/{id}/checklistItems"},
    {"method": "GET", "path": "v1.0/me/todo/lists/{id}/tasks/{id}/checklistItems/{id}"},
    {"method": "GET", "path": "v1.0/users/{id}/todo/lists/{id}/tasks/{id}/checklistItems"},
    {"method": "GET", "path": "v1.0/users/{id}/todo/lists/{id}/tasks/{id}/checklistItems/{id}"},
    {"method": "GET", "path": "v1.0/me/todo/lists/{id}/tasks/{id}/linkedResources"},
    {"method": "GET", "path": "v1.0/me/todo/lists/{id}/tasks/{id}/linkedResources/{id}"},
    {"method": "GET", "path": "v1.0/users/{id}/todo/lists/{id}/tasks/{id}/linkedResources"},
    {"method": "GET", "path": "v1.0/users/{id}/todo/lists/{id}/tasks/{id}/linkedResources/{id}"},
    {"method": "GET", "path": "v1.0/me/todo/lists/{id}/tasks/{id}/attachments"},
    {"method": "GET", "path": "v1.0/me/todo/lists/{id}/tasks/{id}/attachments/{id}"},
    {"method": "GET", "path": "v1.0/me/todo/lists/{id}/tasks/{id}/attachments/{id}/$value"},
    {"method": "GET", "path": "v1.0/me/todo/lists/{id}/tasks/{id}/attachmentSessions"},
    {"method": "GET", "path": "v1.0/me/todo/lists/{id}/tasks/{id}/attachmentSessions/{id}"},
    {"method": "GET", "path": "v1.0/users/{id}/todo/lists/{id}/tasks/{id}/attachments"},
    {"method": "GET", "path": "v1.0/users/{id}/todo/lists/{id}/tasks/{id}/attachments/{id}"},
    {"method": "GET", "path": "v1.0/users/{id}/todo/lists/{id}/tasks/{id}/attachments/{id}/$value"},
    {"method": "GET", "path": "v1.0/users/{id}/todo/lists/{id}/tasks/{id}/attachmentSessions"},
    {"method": "GET", "path": "v1.0/users/{id}/todo/lists/{id}/tasks/{id}/attachmentSessions/{id}"},
    {"method": "GET", "path": "v1.0/subscriptions"},
    {"method": "GET", "path": "v1.0/subscriptions/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Microsoft To Do endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | `v1.0/me/todo/lists/**` | read | lists | Read anything under the To Do lists of the signed-in user: lists, tasks, checklist items, linked resources, attachments, delta. |
| GET | v1.0/me/todo | read | lists | Get the To Do container of the signed-in user. |
| GET | v1.0/me/todo/lists | read | lists | List the task lists of the signed-in user. |
| GET | v1.0/me/todo/lists/delta | read | lists | Track task list changes of the signed-in user (delta query). |
| GET | v1.0/me/todo/lists/{id} | read | lists | Get a task list of the signed-in user. |
| POST | v1.0/me/todo/lists | write | lists | Create a task list for the signed-in user. |
| PATCH | v1.0/me/todo/lists/{id} | write | lists | Update a task list of the signed-in user. |
| DELETE | v1.0/me/todo/lists/{id} | write | lists | Delete a task list of the signed-in user. |
| GET | v1.0/me/todo/lists/{id}/extensions | read | lists | List open extensions of a task list of the signed-in user. |
| GET | v1.0/me/todo/lists/{id}/extensions/{id} | read | lists | Get an open extension of a task list of the signed-in user. |
| POST | v1.0/me/todo/lists/{id}/extensions | write | lists | Create an open extension on a task list of the signed-in user. |
| PATCH | v1.0/me/todo/lists/{id}/extensions/{id} | write | lists | Update an open extension of a task list of the signed-in user. |
| DELETE | v1.0/me/todo/lists/{id}/extensions/{id} | write | lists | Delete an open extension of a task list of the signed-in user. |
| GET | `v1.0/users/{id}/todo/lists/**` | read | lists | Read anything under the To Do lists of a specified user: lists, tasks, checklist items, linked resources, attachments, delta. |
| GET | v1.0/users/{id}/todo | read | lists | Get the To Do container of a specified user. |
| GET | v1.0/users/{id}/todo/lists | read | lists | List the task lists of a specified user. |
| GET | v1.0/users/{id}/todo/lists/delta | read | lists | Track task list changes of a specified user (delta query). |
| GET | v1.0/users/{id}/todo/lists/{id} | read | lists | Get a task list of a specified user. |
| POST | v1.0/users/{id}/todo/lists | write | lists | Create a task list for a specified user. |
| PATCH | v1.0/users/{id}/todo/lists/{id} | write | lists | Update a task list of a specified user. |
| DELETE | v1.0/users/{id}/todo/lists/{id} | write | lists | Delete a task list of a specified user. |
| GET | v1.0/users/{id}/todo/lists/{id}/extensions | read | lists | List open extensions of a task list of a specified user. |
| GET | v1.0/users/{id}/todo/lists/{id}/extensions/{id} | read | lists | Get an open extension of a task list of a specified user. |
| POST | v1.0/users/{id}/todo/lists/{id}/extensions | write | lists | Create an open extension on a task list of a specified user. |
| PATCH | v1.0/users/{id}/todo/lists/{id}/extensions/{id} | write | lists | Update an open extension of a task list of a specified user. |
| DELETE | v1.0/users/{id}/todo/lists/{id}/extensions/{id} | write | lists | Delete an open extension of a task list of a specified user. |
| GET | v1.0/me/todo/lists/{id}/tasks | read | tasks | List tasks in a task list of the signed-in user. |
| GET | v1.0/me/todo/lists/{id}/tasks/delta | read | tasks | Track task changes in a task list of the signed-in user (delta query). |
| GET | v1.0/me/todo/lists/{id}/tasks/{id} | read | tasks | Get a task of the signed-in user. |
| POST | v1.0/me/todo/lists/{id}/tasks | write | tasks | Create a task in a task list of the signed-in user. |
| PATCH | v1.0/me/todo/lists/{id}/tasks/{id} | write | tasks | Update a task of the signed-in user (including completing it). |
| DELETE | v1.0/me/todo/lists/{id}/tasks/{id} | write | tasks | Delete a task of the signed-in user. |
| GET | v1.0/me/todo/lists/{id}/tasks/{id}/extensions | read | tasks | List open extensions of a task of the signed-in user. |
| GET | v1.0/me/todo/lists/{id}/tasks/{id}/extensions/{id} | read | tasks | Get an open extension of a task of the signed-in user. |
| POST | v1.0/me/todo/lists/{id}/tasks/{id}/extensions | write | tasks | Create an open extension on a task of the signed-in user. |
| PATCH | v1.0/me/todo/lists/{id}/tasks/{id}/extensions/{id} | write | tasks | Update an open extension of a task of the signed-in user. |
| DELETE | v1.0/me/todo/lists/{id}/tasks/{id}/extensions/{id} | write | tasks | Delete an open extension of a task of the signed-in user. |
| GET | v1.0/users/{id}/todo/lists/{id}/tasks | read | tasks | List tasks in a task list of a specified user. |
| GET | v1.0/users/{id}/todo/lists/{id}/tasks/delta | read | tasks | Track task changes in a task list of a specified user (delta query). |
| GET | v1.0/users/{id}/todo/lists/{id}/tasks/{id} | read | tasks | Get a task of a specified user. |
| POST | v1.0/users/{id}/todo/lists/{id}/tasks | write | tasks | Create a task in a task list of a specified user. |
| PATCH | v1.0/users/{id}/todo/lists/{id}/tasks/{id} | write | tasks | Update a task of a specified user (including completing it). |
| DELETE | v1.0/users/{id}/todo/lists/{id}/tasks/{id} | write | tasks | Delete a task of a specified user. |
| GET | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/extensions | read | tasks | List open extensions of a task of a specified user. |
| GET | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/extensions/{id} | read | tasks | Get an open extension of a task of a specified user. |
| POST | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/extensions | write | tasks | Create an open extension on a task of a specified user. |
| PATCH | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/extensions/{id} | write | tasks | Update an open extension of a task of a specified user. |
| DELETE | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/extensions/{id} | write | tasks | Delete an open extension of a task of a specified user. |
| GET | v1.0/me/todo/lists/{id}/tasks/{id}/checklistItems | read | checklist items | List checklist items of a task of the signed-in user. |
| GET | v1.0/me/todo/lists/{id}/tasks/{id}/checklistItems/{id} | read | checklist items | Get a checklist item of a task of the signed-in user. |
| POST | v1.0/me/todo/lists/{id}/tasks/{id}/checklistItems | write | checklist items | Create a checklist item on a task of the signed-in user. |
| PATCH | v1.0/me/todo/lists/{id}/tasks/{id}/checklistItems/{id} | write | checklist items | Update a checklist item of a task of the signed-in user. |
| DELETE | v1.0/me/todo/lists/{id}/tasks/{id}/checklistItems/{id} | write | checklist items | Delete a checklist item of a task of the signed-in user. |
| GET | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/checklistItems | read | checklist items | List checklist items of a task of a specified user. |
| GET | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/checklistItems/{id} | read | checklist items | Get a checklist item of a task of a specified user. |
| POST | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/checklistItems | write | checklist items | Create a checklist item on a task of a specified user. |
| PATCH | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/checklistItems/{id} | write | checklist items | Update a checklist item of a task of a specified user. |
| DELETE | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/checklistItems/{id} | write | checklist items | Delete a checklist item of a task of a specified user. |
| GET | v1.0/me/todo/lists/{id}/tasks/{id}/linkedResources | read | linked resources | List linked resources of a task of the signed-in user. |
| GET | v1.0/me/todo/lists/{id}/tasks/{id}/linkedResources/{id} | read | linked resources | Get a linked resource of a task of the signed-in user. |
| POST | v1.0/me/todo/lists/{id}/tasks/{id}/linkedResources | write | linked resources | Create a linked resource on a task of the signed-in user. |
| PATCH | v1.0/me/todo/lists/{id}/tasks/{id}/linkedResources/{id} | write | linked resources | Update a linked resource of a task of the signed-in user. |
| DELETE | v1.0/me/todo/lists/{id}/tasks/{id}/linkedResources/{id} | write | linked resources | Delete a linked resource of a task of the signed-in user. |
| GET | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/linkedResources | read | linked resources | List linked resources of a task of a specified user. |
| GET | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/linkedResources/{id} | read | linked resources | Get a linked resource of a task of a specified user. |
| POST | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/linkedResources | write | linked resources | Create a linked resource on a task of a specified user. |
| PATCH | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/linkedResources/{id} | write | linked resources | Update a linked resource of a task of a specified user. |
| DELETE | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/linkedResources/{id} | write | linked resources | Delete a linked resource of a task of a specified user. |
| GET | v1.0/me/todo/lists/{id}/tasks/{id}/attachments | read | attachments | List file attachments of a task of the signed-in user. |
| GET | v1.0/me/todo/lists/{id}/tasks/{id}/attachments/{id} | read | attachments | Get a file attachment of a task of the signed-in user. |
| GET | v1.0/me/todo/lists/{id}/tasks/{id}/attachments/{id}/$value | read | attachments | Download the raw content of a task attachment of the signed-in user. |
| POST | v1.0/me/todo/lists/{id}/tasks/{id}/attachments | write | attachments | Attach a file to a task of the signed-in user. |
| POST | v1.0/me/todo/lists/{id}/tasks/{id}/attachments/createUploadSession | write | attachments | Create an upload session to attach a large file to a task of the signed-in user. |
| DELETE | v1.0/me/todo/lists/{id}/tasks/{id}/attachments/{id} | write | attachments | Delete a file attachment of a task of the signed-in user. |
| GET | v1.0/me/todo/lists/{id}/tasks/{id}/attachmentSessions | read | attachments | List attachment upload sessions of a task of the signed-in user. |
| GET | v1.0/me/todo/lists/{id}/tasks/{id}/attachmentSessions/{id} | read | attachments | Get the status of an attachment upload session of a task of the signed-in user. |
| PUT | v1.0/me/todo/lists/{id}/tasks/{id}/attachmentSessions/{id}/content | write | attachments | Upload bytes to an attachment upload session of a task of the signed-in user. |
| DELETE | v1.0/me/todo/lists/{id}/tasks/{id}/attachmentSessions/{id} | write | attachments | Cancel an attachment upload session of a task of the signed-in user. |
| GET | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/attachments | read | attachments | List file attachments of a task of a specified user. |
| GET | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/attachments/{id} | read | attachments | Get a file attachment of a task of a specified user. |
| GET | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/attachments/{id}/$value | read | attachments | Download the raw content of a task attachment of a specified user. |
| POST | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/attachments | write | attachments | Attach a file to a task of a specified user. |
| POST | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/attachments/createUploadSession | write | attachments | Create an upload session to attach a large file to a task of a specified user. |
| DELETE | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/attachments/{id} | write | attachments | Delete a file attachment of a task of a specified user. |
| GET | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/attachmentSessions | read | attachments | List attachment upload sessions of a task of a specified user. |
| GET | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/attachmentSessions/{id} | read | attachments | Get the status of an attachment upload session of a task of a specified user. |
| PUT | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/attachmentSessions/{id}/content | write | attachments | Upload bytes to an attachment upload session of a task of a specified user. |
| DELETE | v1.0/users/{id}/todo/lists/{id}/tasks/{id}/attachmentSessions/{id} | write | attachments | Cancel an attachment upload session of a task of a specified user. |
| POST | v1.0/$batch | write | batch | JSON batch of up to 20 Graph requests; can carry writes, so it is not part of read access. |
| GET | v1.0/subscriptions | read | subscriptions | List change-notification (webhook) subscriptions; clientState is not returned. |
| GET | v1.0/subscriptions/{id} | read | subscriptions | Get a change-notification subscription. |
| POST | v1.0/subscriptions | write | subscriptions | Create a webhook subscription that pushes task changes to an external URL. |
| PATCH | v1.0/subscriptions/{id} | write | subscriptions | Renew or update a webhook subscription. |
| DELETE | v1.0/subscriptions/{id} | write | subscriptions | Delete a webhook subscription. |
| POST | v1.0/subscriptions/{id}/reauthorize | write | subscriptions | Reauthorize a webhook subscription after a lifecycle notification. |
