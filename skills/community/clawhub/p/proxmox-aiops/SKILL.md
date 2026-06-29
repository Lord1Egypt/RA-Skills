---
name: proxmox-aiops
description: >
  Use this skill whenever the user needs to manage VMs and containers on Proxmox VE — list/inspect/configure VMs, power and lifecycle (start/stop/shutdown/reboot/reconfigure/clone/delete/migrate), snapshots (create/delete/list/rollback), disk grow/move, vzdump backups (create/list/restore), LXC containers (list/start/stop), cluster/node status, cluster resource inventory, async task polling + logs, free-VMID lookup, HA status, resource pools, firewall inspection, guest-agent ping, and storage listing.
  Always use this skill for "list proxmox vms", "start proxmox vm", "stop proxmox vm", "proxmox snapshot", "proxmox backup", "restore proxmox vm", "resize proxmox disk", "proxmox vm status", "migrate proxmox vm", "proxmox container", "proxmox ha", "proxmox pool", "proxmox firewall", or "list proxmox storage" when the context is explicitly Proxmox / Proxmox VE / PVE.
  Do NOT use for non-Proxmox hypervisors, Kubernetes, or cloud providers.
  Preview — broad coverage of common Proxmox operations, with a built-in governance harness (audit, policy, token budget, undo, risk-tiers).
installer:
  kind: uv
  package: proxmox-aiops
argument-hint: "[vmid or describe your Proxmox task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"env":["PROXMOX_AIOPS_CONFIG"],"bins":["proxmox-aiops"],"config":["~/.proxmox-aiops/config.yaml","~/.proxmox-aiops/.env"]},"optional":{"env":["PROXMOX_TARGET_SECRET"]},"primaryEnv":"PROXMOX_AIOPS_CONFIG","homepage":"https://github.com/AIops-tools/Proxmox-AIops","emoji":"🧱","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed Proxmox VE operations (preview). The governance harness (audit, policy, token/runaway budget, undo, risk-tiers) is bundled in the package — no external skill-family dependency.
  All write operations are audited to a local SQLite DB under ~/.proxmox-aiops/ (relocatable via PROXMOX_AIOPS_HOME).
  Credentials: Each Proxmox target requires a per-target secret env var in ~/.proxmox-aiops/.env following the pattern PROXMOX_<TARGET_NAME_UPPER>_SECRET (API token UUID for token auth, or login password). Secrets are never logged or echoed; .env should be chmod 600.
  Destructive operations (vm stop/delete/snapshot-delete/snapshot-rollback, ct stop) require double confirmation at the CLI layer and support --dry-run. All write tools pass through the @governed_tool decorator (pre-check + budget guard + audit + risk-tier gate). Reversible writes record an inverse undo descriptor to the undo store.
  Webhooks: none — no outbound network calls beyond the configured Proxmox API endpoint.
  SSL: verify_ssl defaults to true; disable only for self-signed lab certificates.
  Transitive dependencies: proxmoxer (Proxmox API client) and the MCP SDK. No post-install scripts or background services.
---

# Proxmox AIops (preview)

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by Proxmox Server Solutions GmbH.** "Proxmox" is a trademark of its owner. Source code is publicly auditable at [github.com/AIops-tools/Proxmox-AIops](https://github.com/AIops-tools/Proxmox-AIops) under the MIT license.

Governed VM and container lifecycle operations for Proxmox VE — **39 MCP tools**, every one wrapped with the bundled `@governed_tool` harness: a local unified audit log under `~/.proxmox-aiops/`, policy engine, token/runaway budget guard, undo-token recording, and graduated-autonomy risk tiers.

> **Standalone**: the governance harness is bundled in the package (`proxmox_aiops.governance`) — proxmox-aiops has no external skill-family dependency. Preview: broad coverage of common Proxmox operations, not yet exhaustive.

## What This Skill Does

| Category | Tools | Count | Read or Write |
|----------|-------|:-----:|:-------------:|
| **VM Lifecycle** | list, get, config, start, stop, shutdown, reboot, reconfigure, clone, delete, migrate | 11 | 3 read / 8 write |
| **Snapshots** | create, delete, list, rollback | 4 | 1 read / 3 write |
| **Disk** | resize (grow-only), move | 2 | 0 read / 2 write |
| **Backups (vzdump)** | create, list, restore | 3 | 1 read / 2 write |
| **LXC Containers** | list, start, stop | 3 | 1 read / 2 write |
| **Cluster / Tasks** | node list, cluster status, task poll, cluster resources, node status, task log, next vmid | 7 | 7 read |
| **HA** | status, resource list | 2 | 2 read |
| **Pools** | list, members | 2 | 2 read |
| **Firewall** | vm rules, cluster status | 2 | 2 read |
| **Guest Agent** | ping | 1 | 1 read |
| **Storage** | list pools, list content | 2 | 2 read |

## Quick Install

```bash
uv tool install proxmox-aiops
proxmox-aiops doctor
```

## When to Use This Skill

- List/inspect Proxmox QEMU VMs and their config
- Power ops: start, hard-stop, graceful shutdown, reboot
- Reconfigure (cores/memory), clone, delete, or migrate a VM between nodes
- Grow a VM disk (grow-only — shrink is refused) or move it to another storage
- Create, list, and restore vzdump backups
- Create / delete / list / roll back VM snapshots
- Manage LXC containers (list, start, stop)
- Inspect cluster nodes, quorum, the `/cluster/resources` inventory, node load/mem, and poll async tasks + fetch their logs by UPID; get a free VMID
- Check HA status / HA-managed resources (handles "HA not configured" gracefully)
- List resource pools and their members
- Inspect VM firewall rules and the cluster firewall enable state (read-only)
- Ping a VM's QEMU guest agent
- List storage pools and their content (ISOs, disk images, backups)

**Do NOT use when** the target is not Proxmox VE (other hypervisors, Kubernetes, or cloud providers are out of scope for this skill).

## Common Workflows

### Snapshot, then reconfigure a VM

1. `proxmox-aiops vm list` → find the vmid and confirm it is the right VM/node
2. `proxmox-aiops vm snapshot-create <vmid> --name pre-change` → baseline before any risky change
3. Make the change (outside this skeleton's scope for now)
4. **Failure branch**: if the change goes wrong, the `vm_snapshot_create` MCP call recorded an `_undo_id` (look it up with `proxmox-aiops` audit tooling), then run the inverse — e.g. `proxmox-aiops vm snapshot-rollback <vmid> --name pre-change`, or `vm snapshot-delete` to clean up after a manual recovery.

### Stop a VM safely

1. `proxmox-aiops vm get <vmid>` → confirm current status is `running`
2. `proxmox-aiops vm stop <vmid> --dry-run` → preview the exact API call
3. `proxmox-aiops vm stop <vmid>` → double confirmation required; `vm_stop` records an inverse `vm_start` undo descriptor
4. **Failure branch**: if `doctor` shows the node unreachable or the secret env var is missing, fix `~/.proxmox-aiops/.env` (chmod 600) before retrying — the stop is never issued against an unauthenticated session.

## Usage Mode

| Scenario | Recommended | Why |
|----------|:-----------:|-----|
| Local/small models (Ollama, Qwen) | **CLI** | fewer tokens than MCP |
| Cloud models (Claude, GPT) | Either | MCP gives structured JSON I/O |
| Automated pipelines | **MCP** | type-safe parameters, audited |

## MCP Tools (39 — 22 read, 17 write)

| Category | Tools | R/W |
|----------|-------|:---:|
| VM Lifecycle | `vm_list`, `vm_get`, `vm_config` | Read |
| | `vm_start`, `vm_stop`, `vm_shutdown`, `vm_reboot`, `vm_reconfigure`, `vm_clone`, `vm_delete`, `vm_migrate` | Write |
| Snapshots | `vm_list_snapshots` | Read |
| | `vm_snapshot_create`, `vm_snapshot_delete`, `vm_snapshot_rollback` | Write |
| Disk | `vm_resize_disk` (grow-only), `vm_move_disk` | Write |
| Backups | `backup_list` | Read |
| | `vm_backup`, `backup_restore` (high) | Write |
| LXC Containers | `ct_list` | Read |
| | `ct_start`, `ct_stop` | Write |
| Cluster / Tasks | `node_list`, `cluster_status`, `task_status`, `cluster_resources`, `node_status`, `task_log`, `next_vmid` | Read |
| HA | `ha_status`, `ha_resource_list` | Read |
| Pools | `pool_list`, `pool_members` | Read |
| Firewall | `vm_firewall_rules_list`, `cluster_firewall_status` | Read |
| Guest Agent | `vm_agent_ping` | Read |
| Storage | `storage_list`, `storage_content` | Read |

**Harness features that light up**: write tools with a clean inverse (`vm_start`/`vm_stop`/`vm_shutdown`/`vm_reconfigure`/`vm_clone`/`vm_migrate`/`vm_snapshot_create`/`vm_move_disk`/`ct_start`/`ct_stop`) pass an `undo=` lambda so the harness records an inverse descriptor (with `_undo_id`) to the undo store — `vm_reconfigure` captures the prior cores/memory, `vm_clone`'s inverse is `vm_delete(newid)`, `vm_migrate`'s is migrate-back, `vm_move_disk`'s is move-back to the captured source storage. `backup_restore` records a `vm_delete` inverse **only** when it restored into a free VMID (a forced overwrite is destructive and declares none). Irreversible writes (`vm_delete`, `vm_snapshot_rollback`, `backup_restore` with `force`) declare no undo and are tagged `risk_level=high`; `vm_resize_disk` is grow-only and refuses shrink before any API call. All 39 tools are audit-logged under `~/.proxmox-aiops/` and pass through the policy pre-check + budget/runaway guard + graduated risk-tier gate. Proxmox writes are async (return a task UPID) — poll with `task_status` (and read lines with `task_log`) instead of re-issuing (the runaway breaker backs this up).

## CLI Quick Reference

```bash
proxmox-aiops vm list [--target <t>] [--node <n>]
proxmox-aiops vm get <vmid> [--node <n>]
proxmox-aiops vm start <vmid> [--node <n>]
proxmox-aiops vm stop <vmid> [--dry-run]              # double confirm
proxmox-aiops vm resize-disk <vmid> --disk scsi0 --size +10G   # grow-only
proxmox-aiops vm move-disk <vmid> --disk scsi0 --storage ceph [--delete]
proxmox-aiops vm agent-ping <vmid>
proxmox-aiops vm snapshot-create <vmid> --name <snap>
proxmox-aiops vm snapshot-delete <vmid> --name <snap> [--dry-run]   # double confirm
proxmox-aiops vm snapshot-list <vmid>
proxmox-aiops backup create <vmid> --storage <s> [--mode snapshot]
proxmox-aiops backup list <storage> [--vmid <id>]
proxmox-aiops backup restore <vmid> --archive <volid> --storage <s> [--force] [--dry-run]  # double confirm
proxmox-aiops cluster resources [--type vm|node|storage]
proxmox-aiops cluster node-status <node>
proxmox-aiops cluster task-log <upid>
proxmox-aiops cluster next-vmid
proxmox-aiops ha status
proxmox-aiops pool list
proxmox-aiops firewall vm-rules <vmid>
proxmox-aiops storage list [--node <n>]
proxmox-aiops init                                    # onboarding wizard (encrypted creds)
proxmox-aiops secret set <target>                     # manage encrypted secret store
proxmox-aiops doctor
proxmox-aiops mcp                                      # start MCP server (stdio)
```

> Credentials are managed by the `proxmox-aiops init` onboarding wizard and the
> `proxmox-aiops secret` commands, which back an encrypted secret store (no
> plaintext passwords in `config.yaml`).

## Troubleshooting

### "Config file not found"
Create `~/.proxmox-aiops/config.yaml` with a `targets:` list (see README), and put secrets in `~/.proxmox-aiops/.env` (chmod 600).

### "Secret not found. Set environment variable: PROXMOX_<NAME>_SECRET"
Each target needs a per-target secret env var. For target `pve-lab`, set `PROXMOX_PVE_LAB_SECRET=<token-uuid>` in `.env`.

### "Token auth requires user in the form 'user@realm!tokenid'"
For API-token auth (recommended, least privilege), `user` must include the token id after `!`, e.g. `root@pam!claude`. For password auth set `auth_kind: password` and use `user@realm`.

### "No node specified and no default node configured"
Either pass `--node <name>` / `node=<name>`, or set `node:` on the target in `config.yaml`. VM operations can auto-locate a vmid across nodes, but storage listing needs an explicit node.

## Audit & Safety

All operations are automatically audited via the bundled `@governed_tool` decorator (`proxmox_aiops.governance`):
- Every tool call logged to `~/.proxmox-aiops/audit.db` (local SQLite audit DB; relocate with `PROXMOX_AIOPS_HOME`)
- Policy rules enforced via `~/.proxmox-aiops/rules.yaml` (deny rules, maintenance windows, risk tiers)
- Budget / runaway guard caps cumulative tool calls and wall-time, and trips on tight poll/retry loops
- Undo store records inverse descriptors for reversible writes (start/stop/shutdown/reconfigure/clone/migrate/snapshot-create, container start/stop)
- Graduated-autonomy risk tiers gate write operations (require a recorded approver for the highest tiers)

The harness is bundled in the package — no external dependency, no manual setup.

## Contributing & feature requests

This is a preview — coverage is intentionally focused. **Missing a device, action, or feature you need?** Open an issue or pull request at [github.com/AIops-tools/Proxmox-AIops](https://github.com/AIops-tools/Proxmox-AIops/issues) — feature requests, contributions, and comments are all welcome.

## License

MIT — [github.com/AIops-tools/Proxmox-AIops](https://github.com/AIops-tools/Proxmox-AIops)
