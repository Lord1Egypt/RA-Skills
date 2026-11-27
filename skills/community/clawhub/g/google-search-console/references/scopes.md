# Google Search Console scopes

The OAuth scopes Google Search Console connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/google-search-console#permissions.

```bash
maton connection create google-search-console --scopes https://www.googleapis.com/auth/webmasters.readonly
```

| Scope | Requested |
| --- | --- |
| `https://www.googleapis.com/auth/webmasters` | By default |
| `https://www.googleapis.com/auth/webmasters.readonly` | Optional |
| `https://www.googleapis.com/auth/userinfo.email` | Always |
