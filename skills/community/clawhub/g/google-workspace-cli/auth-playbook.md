# Auth Playbook - Google Workspace CLI

## Recommended Auth Paths

- Local desktop: `gws auth setup` then `gws auth login`
- Existing project control: manual OAuth client + `gws auth login`
- CI/headless: inject a dedicated credentials file from a secure secret manager at runtime
- Server-to-server: service account credentials file and optional impersonation

## Multi-Account Operations

```bash
gws auth login --account work@corp.com
gws auth login --account personal@gmail.com
gws auth list
gws auth default work@corp.com
```

One-off override pattern:

```bash
gws --account personal@gmail.com drive files list --params '{"pageSize":5}'
```

## Precedence Rules

1. explicit access-token override
2. explicit credentials-file override
3. encrypted account credentials (`gws auth login --account`)

## Scope Strategy

- Start with minimum scopes for first-run reliability.
- Expand with explicit `--scopes` only when a method requires it.
- Avoid broad scope bundles when only one service is needed.

## Non-Negotiables

- Never request secrets in chat text.
- Never mix unrelated tenants under one default account.
- Never run mutation commands when account ownership is unclear.
- Never store unencrypted credentials in shared workspaces.
