# Monday.com scopes

The OAuth scopes Monday.com connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/monday#permissions.

```bash
maton connection create monday --scopes account:read
```

| Scope | Requested |
| --- | --- |
| `account:read` | By default |
| `assets:read` | By default |
| `boards:read` | By default |
| `boards:write` | By default |
| `departments:read` | By default |
| `departments:write` | By default |
| `docs:read` | By default |
| `docs:write` | By default |
| `notifications:write` | By default |
| `tags:read` | By default |
| `teams:read` | By default |
| `teams:write` | By default |
| `updates:read` | By default |
| `updates:write` | By default |
| `users:read` | By default |
| `users:write` | By default |
| `webhooks:read` | By default |
| `webhooks:write` | By default |
| `workspaces:read` | By default |
| `workspaces:write` | By default |
| `me:read` | Always |
