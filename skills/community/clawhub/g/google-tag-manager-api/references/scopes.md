# Google Tag Manager scopes

The OAuth scopes Google Tag Manager connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/google-tag-manager#permissions.

```bash
maton connection create google-tag-manager --scopes https://www.googleapis.com/auth/tagmanager.readonly
```

| Scope | Requested |
| --- | --- |
| `https://www.googleapis.com/auth/tagmanager.edit.containers` | By default |
| `https://www.googleapis.com/auth/tagmanager.delete.containers` | By default |
| `https://www.googleapis.com/auth/tagmanager.edit.containerversions` | By default |
| `https://www.googleapis.com/auth/tagmanager.publish` | By default |
| `https://www.googleapis.com/auth/tagmanager.manage.users` | By default |
| `https://www.googleapis.com/auth/tagmanager.manage.accounts` | By default |
| `https://www.googleapis.com/auth/tagmanager.readonly` | Optional |
| `https://www.googleapis.com/auth/userinfo.email` | Always |
