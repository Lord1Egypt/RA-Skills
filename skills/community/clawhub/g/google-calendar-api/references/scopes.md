# Google Calendar scopes

The OAuth scopes Google Calendar connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/google-calendar#permissions.

```bash
maton connection create google-calendar --scopes https://www.googleapis.com/auth/calendar.readonly
```

| Scope | Requested |
| --- | --- |
| `https://www.googleapis.com/auth/calendar` | By default |
| `https://www.googleapis.com/auth/calendar.readonly` | Optional |
| `https://www.googleapis.com/auth/userinfo.email` | Always |
