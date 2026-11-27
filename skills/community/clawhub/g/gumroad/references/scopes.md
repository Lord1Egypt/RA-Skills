# Gumroad scopes

The OAuth scopes Gumroad connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/gumroad#permissions.

```bash
maton connection create gumroad --scopes edit_products
```

| Scope | Requested |
| --- | --- |
| `edit_products` | By default |
| `view_sales` | By default |
| `view_payouts` | By default |
| `mark_sales_as_shipped` | By default |
| `edit_sales` | By default |
| `view_profile` | Always |
