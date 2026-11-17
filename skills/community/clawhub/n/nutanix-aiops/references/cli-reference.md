# nutanix-aiops CLI reference

> Talks to Nutanix **Prism Central v4** on HTTPS `:9440`
> with HTTP Basic auth. The CLI is a convenience subset; the full **51-tool**
> surface is via the MCP server (`nutanix-aiops mcp`).

## Setup & diagnostics

```bash
nutanix-aiops init                      # interactive onboarding wizard
nutanix-aiops doctor [--skip-auth]      # config + secret store + connectivity + REST-RBAC preflight
nutanix-aiops mcp                       # start the MCP server (stdio transport)
```

`doctor` checks the config file, the encrypted secret store and its permissions,
that a password is present per target, and (unless `--skip-auth`) connectivity
plus a **REST-RBAC preflight** against Prism Central — confirming the account can
actually call the v4 APIs, not just log in to the Web UI.

## Estate & clusters (read)

```bash
nutanix-aiops overview [--target <t>]              # one-shot estate summary
nutanix-aiops cluster list                         # registered clusters (extId, AOS, hypervisors, nodes)
nutanix-aiops cluster health <cluster_ext_id>      # services, resiliency, upgrade state
nutanix-aiops cluster hosts                         # hosts across all clusters
nutanix-aiops cluster util <cluster_ext_id>        # CPU / memory / storage / IOPS utilization
```

## Diagnostics / RCA (read-only)

```bash
nutanix-aiops diagnose cluster-health              # resiliency, storage >80%/>90%, nodes down — worst first
nutanix-aiops diagnose alert-triage                # active alerts by severity + oldest unresolved
```

Both print a worst-first findings table (severity · resource · signal · detail ·
action) or a green all-clear line when every measured value is under threshold.

## VMs

```bash
nutanix-aiops vm list [--esxi | --no-esxi]         # AHV + ESXi VMs (ESXi included by default)
nutanix-aiops vm get <vm_ext_id>                   # one VM detail (shows its ETag)
nutanix-aiops vm power <vm_ext_id> <on|off|shutdown|reboot> [--dry-run]
nutanix-aiops vm delete <vm_ext_id> [--dry-run]    # (HIGH) dry-run + double confirm
nutanix-aiops vm migrate <vm_ext_id> <target_host_ext_id> [--dry-run]   # (HIGH) dry-run + double confirm
```

## Secrets (encrypted store `~/.nutanix-aiops/secrets.enc`)

```bash
nutanix-aiops secret set <target> [--value <pw>]   # store PC password (hidden prompt if no --value)
nutanix-aiops secret list                           # names only — values never shown
nutanix-aiops secret rm <target>
nutanix-aiops secret migrate                        # import legacy plaintext env (NUTANIX_<T>_PASSWORD)
nutanix-aiops secret rotate-password                # re-encrypt the store under a new master password
```

## Common options

- `--target, -t <name>` — target name from `config.yaml` (omit to use the default / first target)
- `--dry-run` — print the API call that would be made, change nothing
- `--esxi / --no-esxi` — include or exclude ESXi-managed VMs in `vm list` (default: include)
- Destructive commands (`vm delete`, `vm migrate`) require a `--dry-run` preview and **two confirmations**

## Full surface via MCP

The 51 governed tools (clusters, VMs, storage, network, catalog, data
protection / DR, alerts + `analyze_alert` RCA, LCM upgrades, capacity runway,
and the `cluster_health_rca` / `alert_triage_rca` diagnostics)
are exposed by `nutanix-aiops mcp`. Set `NUTANIX_AIOPS_MASTER_PASSWORD` so the
encrypted store unlocks non-interactively. See `capabilities.md` for the full
tool → API-path → returns map.
</content>
