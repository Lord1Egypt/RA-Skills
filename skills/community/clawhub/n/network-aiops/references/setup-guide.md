# network-aiops Setup Guide

## Install

```bash
uv tool install network-aiops
network-aiops init      # interactive onboarding wizard (recommended)
network-aiops doctor
```

`network-aiops` requires Python ≥ 3.11. If `uv` picked an older interpreter:

```bash
uv python install 3.12
uv tool install --python 3.12 --force network-aiops
```

## Configure devices

Create `~/.network-aiops/config.yaml`:

```yaml
devices:
  - name: core-sw1            # used as -t core-sw1
    driver: eos               # ios | nxos | nxos_ssh | iosxr | eos | junos
    host: 10.0.0.1
    username: admin
    optional_args:            # passed verbatim to NAPALM (optional)
      secret: enable-pw       # enable/secret
      port: 443
  - name: edge-rtr
    driver: ios
    host: 10.0.0.254
    username: netops
# Optional source-of-truth:
netbox:
  url: https://netbox.example.com
```

### Secrets — encrypted store (never in config.yaml)

Secrets are stored **encrypted** in `~/.network-aiops/secrets.enc` (Fernet/AES +
scrypt-derived key; chmod 600) — never in config.yaml or a plaintext `.env`.
Device login passwords are keyed by the device name; the NetBox API token uses
the reserved name `netbox-token`. The fastest path is `network-aiops init`, or
set them individually:

```bash
network-aiops secret set core-sw1       # hidden prompt for the device password
network-aiops secret set edge-rtr
network-aiops secret set netbox-token   # the NetBox API token
network-aiops secret list               # names only — values are never printed
```

Unlock the store non-interactively by exporting the master password (used by the
MCP server, cron, CI):

```bash
export NETWORK_AIOPS_MASTER_PASSWORD='your-master-password'
chmod 700 ~/.network-aiops
```

**Migrating from a legacy plaintext `.env`** (`NETWORK_<TARGET_UPPER>_PASSWORD`,
`NETWORK_NETBOX_TOKEN`): run `network-aiops secret migrate` to import them into
the encrypted store (the old file is renamed to `.env.migrated`; delete it once
verified). Those env vars still work as a deprecated fallback with a warning. An
empty device password is allowed for key-based SSH auth.

### Supported drivers

`ios` (Cisco IOS/IOS-XE), `nxos` / `nxos_ssh` (Cisco Nexus NX-OS), `iosxr`
(Cisco IOS-XR), `eos` (Arista EOS), `junos` (Juniper Junos). Other platforms
(Nokia SR OS / SR Linux, Huawei VRP, …) are reachable via NAPALM community
drivers but are untested here — request official support via a GitHub issue/PR.

## Security

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by Cisco, Arista, Juniper, NetBox Labs, or any network vendor.** Vendor and product names are trademarks of their respective owners. Source is auditable at [github.com/AIops-tools/Network-AIops](https://github.com/AIops-tools/Network-AIops) under the MIT license.

1. **Source code** — [github.com/AIops-tools/Network-AIops](https://github.com/AIops-tools/Network-AIops), MIT.
2. **Config file contents** — `config.yaml` holds only device names, drivers,
   hosts, usernames, and NAPALM `optional_args`. No credentials.
3. **Credentials** — device passwords and the NetBox token live in the encrypted
   store `~/.network-aiops/secrets.enc` (Fernet/AES, scrypt-derived key, chmod
   600), unlocked by `NETWORK_AIOPS_MASTER_PASSWORD`; never read back, logged, or
   echoed. Legacy plaintext env vars remain a deprecated fallback. Keep the dir
   chmod 700.
4. **TLS verification** — NAPALM transports (eAPI/NX-API HTTPS, NETCONF/SSH)
   follow each device's own certificate / SSH host-key configuration; the skill
   does not weaken it.
5. **Prompt-injection protection** — all device-returned text (facts, configs,
   diffs, neighbor data) is run through `sanitize()` (truncation + control-char
   stripping).
6. **Least privilege** — use a device account with only the privilege you need:
   a read-only login for facts/backup, and a config-capable login only for the
   merge/replace/rollback tools.

## Governance harness

Bundled under `network_aiops.governance` — no external dependency. State lives
under `~/.network-aiops/` (override with `NETWORK_AIOPS_HOME`):

- `audit.db` — every tool call (skill, tool, params, status, duration, agent).
- `rules.yaml` — policy deny rules, maintenance windows, risk tiers.
- Token/runaway budget guard (`NETWORK_MAX_TOOL_CALLS`, `NETWORK_MAX_TOOL_SECONDS`,
  `NETWORK_RUNAWAY_MAX`, `NETWORK_RUNAWAY_WINDOW_SEC`).
- Undo store — inverse descriptors for reversible writes (config merge/replace).
- Encrypted secret store (`secrets.enc`) — device passwords + NetBox token,
  unlocked by `NETWORK_AIOPS_MASTER_PASSWORD`.
- Accountability: set `NETWORK_AUDIT_APPROVED_BY` / `NETWORK_AUDIT_RATIONALE` to
  record who authorized a high-tier operation and why.

## MCP client config

```jsonc
{
  "command": "network-aiops",
  "args": ["mcp"],
  "env": {
    "NETWORK_AIOPS_CONFIG": "~/.network-aiops/config.yaml",
    "NETWORK_AIOPS_MASTER_PASSWORD": "…"
  }
}
```

Fallback (no `uv tool install`): `uvx --from network-aiops network-aiops-mcp`.
Prefer the installed entry point — it does not re-resolve PyPI at launch.

## Static analysis

```bash
uvx bandit -r network_aiops/ mcp_server/
```
