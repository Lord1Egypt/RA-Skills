# LinkedIn scopes

The OAuth scopes LinkedIn connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/linkedin#permissions.

```bash
maton connection create linkedin --scopes w_member_social
```

| Scope | Requested |
| --- | --- |
| `w_member_social` | By default |
| `r_ads_reporting` | By default |
| `r_organization_social` | By default |
| `rw_organization_admin` | By default |
| `w_organization_social` | By default |
| `rw_ads` | By default |
| `r_organization_admin` | By default |
| `r_1st_connections_size` | By default |
| `r_basicprofile` | Always |
