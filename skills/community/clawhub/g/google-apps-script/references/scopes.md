# Google Apps Script scopes

The OAuth scopes Google Apps Script connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/google-apps-script#permissions.

```bash
maton connection create google-apps-script --scopes https://www.googleapis.com/auth/script.projects.readonly
```

| Scope | Requested |
| --- | --- |
| `https://www.googleapis.com/auth/script.deployments` | By default |
| `https://www.googleapis.com/auth/script.metrics` | By default |
| `https://www.googleapis.com/auth/script.processes` | By default |
| `https://www.googleapis.com/auth/script.projects` | By default |
| `https://www.googleapis.com/auth/script.storage` | By default |
| `https://www.googleapis.com/auth/script.projects.readonly` | Optional |
| `https://www.googleapis.com/auth/script.deployments.readonly` | Optional |
| `https://www.googleapis.com/auth/drive.readonly` | Optional |
| `https://www.googleapis.com/auth/userinfo.email` | Always |
