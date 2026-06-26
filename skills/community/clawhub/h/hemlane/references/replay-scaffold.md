# Hemlane replay scaffold

Use `scripts/replay_hemlane_graphql.py` to replay a Hemlane GraphQL request with auth provided at runtime.

## Required env vars
- `HEMLANE_COOKIE` - browser session cookies if required
- `HEMLANE_CSRF_TOKEN` - CSRF token if required

Optional:
- `HEMLANE_AUTHORIZATION`
- `HEMLANE_GRAPHQL_ENDPOINT` (defaults to `https://api.hemlane.com/graphql`)
- `HEMLANE_REFERER`
- `HEMLANE_ORIGIN`
- `HEMLANE_APOLLO_CLIENT_NAME`
- `HEMLANE_APOLLO_CLIENT_VERSION`
- `HEMLANE_USER_AGENT`

## Dry run
```bash
python scripts/replay_hemlane_graphql.py   --query references/example-hubspot-submit.graphql   --variables references/example-hubspot-submit.variables.json   --operation-name HubspotFormSubmit   --dry-run
```

## Live replay
```bash
python scripts/replay_hemlane_graphql.py   --query references/example-hubspot-submit.graphql   --variables references/example-hubspot-submit.variables.json   --operation-name HubspotFormSubmit   --pretty
```

## Safety rules
- Keep live cookies and CSRF values out of committed files.
- Prefer `--dry-run` first to inspect the reconstructed payload.
- Replay only from a currently valid authenticated session.
- If a mutation changes state, confirm the target IDs and variables before sending.
