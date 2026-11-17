# identity-aiops CLI reference

All read commands print normalized JSON. All write commands take `--dry-run`
(preview, no call, no audit) and otherwise require **double confirmation**;
confirmed writes execute through the governed MCP twins, so they land in
`~/.identity-aiops/audit.db` with undo where applicable. `--target/-t` selects
a target from config (default: the first one).

## Setup / health

```bash
identity-aiops init                 # onboarding wizard (platform, base URL, realm, secret)
identity-aiops doctor               # config + secrets + token acquisition + user-count probe
identity-aiops doctor --skip-auth   # config/secrets checks only (no network)
identity-aiops overview             # one-shot estate summary
identity-aiops mcp                  # start the MCP server (stdio)
```

## Secrets (encrypted store)

```bash
identity-aiops secret set <target>    # store/replace a secret (hidden prompt)
identity-aiops secret list            # target names only — never values
identity-aiops secret remove <target>
identity-aiops secret migrate         # legacy .env / env vars → secrets.enc
```

Master password: `IDENTITY_AIOPS_MASTER_PASSWORD` (non-interactive/MCP) or an
interactive prompt on a TTY.

## Events

```bash
identity-aiops events                          # recent auth events
identity-aiops events --type LOGIN_ERROR -n 50 # Keycloak failed logins
identity-aiops events --type login_failed      # authentik failed logins
identity-aiops events --user alice
```

## Users

```bash
identity-aiops users list [--search alice] [--limit 200]
identity-aiops users show <user-id>
identity-aiops users sessions <user-id>
identity-aiops users credentials <user-id>          # MFA surface

# governed writes
identity-aiops users disable <user-id> [--dry-run]          # med, undo: enable
identity-aiops users enable <user-id> [--dry-run]           # HIGH
identity-aiops users revoke-sessions <user-id> [--dry-run]  # med, irreversible
identity-aiops users require-reset <user-id> [--clear] [--dry-run]
```

## Clients

```bash
identity-aiops clients list [--limit 200]
identity-aiops clients show <client-id>

# governed writes
identity-aiops clients set-redirect-uris <client-id> -u https://a/cb -u https://b/cb [--dry-run]  # HIGH
identity-aiops clients rotate-secret <client-id> [--dry-run]                                       # HIGH, masked
```

## Environment variables

| Variable | Purpose |
|----------|---------|
| `IDENTITY_AIOPS_HOME` | relocate all state (config, secrets, audit, undo) |
| `IDENTITY_AIOPS_CONFIG` | alternate config.yaml path (MCP server) |
| `IDENTITY_AIOPS_MASTER_PASSWORD` | unlock secrets.enc non-interactively |
| `IDENTITY_AUDIT_APPROVED_BY` / `IDENTITY_AUDIT_RATIONALE` | optional audit annotations (who/why), recorded when set |
| `IDENTITY_MAX_TOOL_CALLS` / `IDENTITY_MAX_TOOL_SECONDS` | session budget ceilings |
| `IDENTITY_<TARGET>_SECRET` | legacy plaintext secret fallback (deprecated) |
