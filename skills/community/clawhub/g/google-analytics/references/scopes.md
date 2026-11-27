# Google Analytics Admin scopes

The OAuth scopes Google Analytics Admin connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/google-analytics#permissions.

```bash
maton connection create google-analytics-admin --scopes https://www.googleapis.com/auth/analytics.readonly
```

| Scope | Requested |
| --- | --- |
| `https://www.googleapis.com/auth/analytics.edit` | By default |
| `https://www.googleapis.com/auth/analytics` | By default |
| `https://www.googleapis.com/auth/analytics.readonly` | Optional |
| `https://www.googleapis.com/auth/userinfo.email` | Always |

# Google Analytics Data scopes

The OAuth scopes Google Analytics Data connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/google-analytics#permissions.

```bash
maton connection create google-analytics-data --scopes https://www.googleapis.com/auth/analytics.readonly
```

| Scope | Requested |
| --- | --- |
| `https://www.googleapis.com/auth/analytics.edit` | By default |
| `https://www.googleapis.com/auth/analytics` | By default |
| `https://www.googleapis.com/auth/analytics.readonly` | Optional |
| `https://www.googleapis.com/auth/userinfo.email` | Always |
