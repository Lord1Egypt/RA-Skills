# identity-aiops setup & security guide

> Verification status: mock-validated; no recorded live IdP run yet. Both **Keycloak**
> and **authentik** are free/self-hostable (each runs from a single container), so a lab is
> the easiest live check. The modelled REST paths are the largest verification
> debt.

## 1. Install

```bash
uv tool install identity-aiops       # or: pipx install identity-aiops
```

## 2. What you need per IdP

- **Keycloak** — a **confidential client** with *Client authentication* ON and
  *Service accounts roles* enabled (Clients → Create client). Grant its service
  account the `realm-management` roles the agent should have:
  - reads/analyses only: `view-users`, `view-events`, `view-clients`,
    `view-realm`, `view-identity-providers`
  - governed writes too: add `manage-users` and/or `manage-clients`
  identity-aiops exchanges the client's **client_id + secret** at
  `/realms/{realm}/protocol/openid-connect/token` (client-credentials grant)
  and refreshes the short-lived token automatically on a 401.
- **authentik** — an **API token** (Directory → Tokens & App passwords) for a
  least-privileged admin user. The token is sent as `Authorization: Bearer` on
  every call.

## 3. Onboard with the wizard

```bash
identity-aiops init
```

The wizard asks, per target, for the **platform** (`keycloak` / `authentik`),
the **base URL** (e.g. `https://sso.example.com`), TLS verification (default
**ON**; answer No only for self-signed lab certs), and — Keycloak only — the
**realm** (default `master`) and the **client_id** (saved as `username`). The
secret (client secret / API token) goes **encrypted** into
`~/.identity-aiops/secrets.enc`; non-secret details go to
`~/.identity-aiops/config.yaml`.

Example `config.yaml`:

```yaml
targets:
  - name: sso1
    platform: keycloak
    base_url: https://sso.example.com
    realm: master
    username: identity-aiops-agent
    verify_ssl: true
  - name: ak1
    platform: authentik
    base_url: https://auth.example.com
    verify_ssl: true
```

## 4. Verify

```bash
identity-aiops doctor
```

Doctor checks the config, the encrypted store (and its permissions), then per
target runs the full auth path (Keycloak token acquisition / authentik bearer)
plus a cheap realm probe — the user count. Exit code 0 = healthy.

## 5. MCP client configuration

```json
{
  "mcpServers": {
    "identity-aiops": {
      "command": "uvx",
      "args": ["--from", "identity-aiops", "identity-aiops-mcp"],
      "env": {
        "IDENTITY_AIOPS_MASTER_PASSWORD": "<master password>",
        "IDENTITY_AUDIT_APPROVED_BY": "<optional: attributed on audit rows>"
      }
    }
  }
}
```

MCP clients start the server with a minimal environment — shell-profile
variables are NOT inherited; put everything the server needs in the `env`
block.

## 6. Security notes

- Secrets: Fernet-encrypted (scrypt-derived key), chmod 600, never plaintext;
  legacy `IDENTITY_<TARGET>_SECRET` env fallback warns and should be migrated
  (`identity-aiops secret migrate`).
- Least privilege: scope the Keycloak service account / authentik token to the
  roles you actually want the agent to exercise — the reads/analyses work with
  view-only roles.
- High-risk writes (`enable_user`, `update_client_redirect_uris`,
  `rotate_client_secret`) are tagged risk=high on the audit row; whether they
  run is the connecting account's permissions or your agent's judgement, not a
  tool-side gate. `IDENTITY_AUDIT_APPROVED_BY` / `IDENTITY_AUDIT_RATIONALE` are
  optional annotations recorded when set.
- `rotate_client_secret` never shows a secret — fetch the new value from the
  admin console over a trusted channel.
- Audit/undo live in `~/.identity-aiops/` (`audit.db`, `undo.db`), relocatable
  via `IDENTITY_AIOPS_HOME`.
