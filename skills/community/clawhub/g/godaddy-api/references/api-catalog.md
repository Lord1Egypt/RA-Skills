# Dynamic API catalog

The official `gddy` CLI ships an embedded, searchable catalog of GoDaddy REST and GraphQL operations. Prefer it over a static list because GoDaddy's available API domains and schemas evolve.

## Inventory and search

```bash
gddy api domain list --json
gddy api search "certificate renew" --json
gddy api operation list --domain <domain> --json
gddy api operation get <operation-id-or-path> --json
```

`api operation get` shows the operation's API domain, base URL, full path, method, parameters, request schema, responses, and scopes. If a path fragment matches multiple operations, add `--method` or use the exact operation ID.

Inspect nested contracts when needed:

```bash
gddy api parameter list --operation <operation-id>
gddy api parameter get <parameter> --operation <operation-id>
gddy api response list --operation <operation-id>
gddy api response get <status> --operation <operation-id>
gddy api schema get <schema>
```

Use each command's `--help` because identifiers and options are discoverable from the installed release.

## REST calls

`gddy api call` accepts an operation ID or documented relative path:

```bash
gddy api call <operation-id> --param name=value
gddy api call <operation-id> --file request.json
gddy api call /documented/path --method GET --param name=value
```

- `--param` routes known values to path, query, header, or body using the operation schema.
- `--file` loads JSON and takes precedence over `--body`.
- `--field` merges a body field.
- `--header` adds a documented header; never put credentials on the command line.
- `--include` returns response headers, useful for request IDs and rate limits.
- `--dry-run` previews mutations without executing.

Use operation IDs when possible so the CLI can validate and route parameters. Do not invent a method, base URL, scope, or request body when discovery returns no contract.

## GraphQL calls

```bash
gddy api graphql get <operation-id>
gddy api graphql type get <type> --domain <domain>
gddy api graphql sdl get <wrapper-operation-id>
gddy api graphql call <operation-id> --arg name=value --select id,name
```

The CLI builds the query and variables. Always inspect the operation first. Select only the fields needed, and dry-run mutations before seeking approval.

## Domains API fallback

For application code where `gddy` is not the runtime, use the machine-readable specs rather than copying a CLI call:

- <https://developer.godaddy.com/openapi/domains-v3.json> — current discovery, quote/registration, domain reads, nameservers, DNS, and operations
- <https://developer.godaddy.com/openapi/domains-v2.json> — customer-scoped lifecycle, transfers, forwarding, notifications, and actions
- <https://developer.godaddy.com/openapi/domains-v1.json> — maintained account list/detail, renewals, contacts, transfers, and record-set DNS

Use PAT Bearer authentication for new integrations; v3 requires it. The public MCP at `https://api.godaddy.com/v1/domains/mcp` is unauthenticated and read-only for public domain discovery. Never treat it as an account-management or mutation surface.
