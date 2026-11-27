# Klaviyo scopes

The OAuth scopes Klaviyo connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/klaviyo#permissions.

```bash
maton connection create klaviyo --scopes campaigns:read
```

| Scope | Requested |
| --- | --- |
| `accounts:write` | By default |
| `campaigns:read` | By default |
| `campaigns:write` | By default |
| `catalogs:read` | By default |
| `catalogs:write` | By default |
| `conversations:read` | By default |
| `conversations:write` | By default |
| `coupon-codes:read` | By default |
| `coupon-codes:write` | By default |
| `coupons:read` | By default |
| `coupons:write` | By default |
| `events:read` | By default |
| `events:write` | By default |
| `flows:read` | By default |
| `flows:write` | By default |
| `forms:read` | By default |
| `forms:write` | By default |
| `images:read` | By default |
| `images:write` | By default |
| `lists:read` | By default |
| `lists:write` | By default |
| `metrics:read` | By default |
| `metrics:write` | By default |
| `profiles:read` | By default |
| `profiles:write` | By default |
| `reviews:read` | By default |
| `reviews:write` | By default |
| `segments:read` | By default |
| `segments:write` | By default |
| `subscriptions:read` | By default |
| `subscriptions:write` | By default |
| `tags:read` | By default |
| `tags:write` | By default |
| `templates:read` | By default |
| `templates:write` | By default |
| `webhooks:read` | By default |
| `webhooks:write` | By default |
| `accounts:read` | Always |
