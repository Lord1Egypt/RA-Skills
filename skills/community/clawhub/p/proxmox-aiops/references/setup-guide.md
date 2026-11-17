# proxmox-aiops setup guide

## Install

```bash
uv tool install proxmox-aiops
# or: pipx install proxmox-aiops
```

## Configure

```bash
mkdir -p ~/.proxmox-aiops && chmod 700 ~/.proxmox-aiops
```

`~/.proxmox-aiops/config.yaml` (no secrets here):

```yaml
targets:
  - name: pve-lab
    host: 10.0.0.10
    user: "root@pam!claude"   # API token form: user@realm!tokenid
    node: pve1                 # default node for this target
    auth_kind: token           # 'token' or 'password'
    verify_ssl: false          # self-signed lab certs only; true in prod
```

`~/.proxmox-aiops/.env` (chmod 600 — secrets only):

```bash
PROXMOX_PVE_LAB_SECRET=<api-token-uuid-or-password>
```

The secret variable is `PROXMOX_<TARGET_NAME_UPPER>_SECRET` (hyphens → underscores).

```bash
chmod 600 ~/.proxmox-aiops/.env
proxmox-aiops doctor          # verifies connectivity + credentials
```

## Use as an MCP server

```jsonc
{
  "command": "proxmox-aiops",
  "args": ["mcp"],
  "env": { "PROXMOX_AIOPS_CONFIG": "~/.proxmox-aiops/config.yaml" }
}
```

Using the `proxmox-aiops mcp` subcommand (rather than `uvx --from`) means the
MCP client launches the already-installed entry point and does not re-resolve
the package over the network at startup.

## Security

> **Disclaimer**: Community-maintained project, **not affiliated with Proxmox
> Server Solutions GmbH**. MIT licensed. See `SECURITY.md`.

- **Credentials**: `.env` only, chmod 600, per-target `PROXMOX_<TARGET>_SECRET`.
- **Audit**: every operation logged to a local SQLite DB under
  `~/.proxmox-aiops/` (relocate with `PROXMOX_AIOPS_HOME`).
- **Budget guard**: cap calls/wall-time with `PROXMOX_MAX_TOOL_CALLS` /
  `PROXMOX_MAX_TOOL_SECONDS`; a runaway poll/retry loop trips automatically.
- **Risk tiers**: each tool's `risk_level` is recorded on the audit row as a
  descriptive tier (none/confirm/review) — a label, not a gate.
  `PROXMOX_AUDIT_APPROVED_BY` / `PROXMOX_AUDIT_RATIONALE` are optional audit
  annotations, never required.
- **Destructive ops**: double confirmation + `--dry-run` at the CLI.
- **TLS**: `verify_ssl` defaults true; disable only for self-signed labs.
- **No webhooks / telemetry / background services.**

## Least privilege

Create a dedicated Proxmox API token with only the roles your workflows need
(e.g. `PVEVMAdmin` on the relevant pool) rather than `root@pam`.
