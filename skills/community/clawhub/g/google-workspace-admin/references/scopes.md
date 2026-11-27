# Google Workspace Admin scopes

The OAuth scopes Google Workspace Admin connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/google-workspace-admin#permissions.

```bash
maton connection create google-workspace-admin --scopes https://www.googleapis.com/auth/admin.directory.user.readonly
```

| Scope | Requested |
| --- | --- |
| `https://www.googleapis.com/auth/admin.directory.user` | By default |
| `https://www.googleapis.com/auth/admin.directory.group` | By default |
| `https://www.googleapis.com/auth/admin.directory.orgunit` | By default |
| `https://www.googleapis.com/auth/admin.directory.domain` | By default |
| `https://www.googleapis.com/auth/admin.directory.rolemanagement` | By default |
| `https://www.googleapis.com/auth/admin.directory.user.readonly` | Optional |
| `https://www.googleapis.com/auth/admin.directory.group.readonly` | Optional |
| `https://www.googleapis.com/auth/admin.directory.orgunit.readonly` | Optional |
| `https://www.googleapis.com/auth/admin.directory.domain.readonly` | Optional |
| `https://www.googleapis.com/auth/admin.directory.rolemanagement.readonly` | Optional |
| `https://www.googleapis.com/auth/userinfo.email` | Always |
