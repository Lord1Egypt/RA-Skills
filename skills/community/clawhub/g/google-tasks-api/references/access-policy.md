# Google Tasks access policy

An access policy limits which endpoints Google Tasks connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/google-tasks#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Google Tasks: its 4 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create google-tasks --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "tasks/v1/users/@me/lists"},
    {"method": "GET", "path": "tasks/v1/users/@me/lists/{id}"},
    {"method": "GET", "path": "tasks/v1/lists/{id}/tasks"},
    {"method": "GET", "path": "tasks/v1/lists/{id}/tasks/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Google Tasks endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | tasks/v1/users/@me/lists | read | tasklists | Returns all the authenticated user's task lists. |
| POST | tasks/v1/users/@me/lists | write | tasklists | Creates a new task list and adds it to the authenticated user's task lists. |
| GET | tasks/v1/users/@me/lists/{id} | read | tasklists | Returns the authenticated user's specified task list. |
| PUT | tasks/v1/users/@me/lists/{id} | write | tasklists | Updates the authenticated user's specified task list. |
| PATCH | tasks/v1/users/@me/lists/{id} | write | tasklists | Updates the authenticated user's specified task list. |
| DELETE | tasks/v1/users/@me/lists/{id} | write | tasklists | Deletes the authenticated user's specified task list. |
| POST | tasks/v1/lists/{id}/clear | write | tasks | Clears all completed tasks from the specified task list. |
| GET | tasks/v1/lists/{id}/tasks | read | tasks | Returns all tasks in the specified task list. |
| POST | tasks/v1/lists/{id}/tasks | write | tasks | Creates a new task on the specified task list. |
| GET | tasks/v1/lists/{id}/tasks/{id} | read | tasks | Returns the specified task. |
| PUT | tasks/v1/lists/{id}/tasks/{id} | write | tasks | Updates the specified task. |
| PATCH | tasks/v1/lists/{id}/tasks/{id} | write | tasks | Updates the specified task. |
| DELETE | tasks/v1/lists/{id}/tasks/{id} | write | tasks | Deletes the specified task from the task list. |
| POST | tasks/v1/lists/{id}/tasks/{id}/move | write | tasks | Moves the specified task to another position in the destination task list. |
