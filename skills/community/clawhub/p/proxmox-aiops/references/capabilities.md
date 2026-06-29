# proxmox-aiops capabilities

39 MCP tools (22 read / 17 write). Every tool is wrapped with the bundled
`@governed_tool` harness (audit + budget + risk-tier + undo). Typical response
sizes are small high-signal summaries, not full API blobs.

## VM lifecycle (11)

| Tool | R/W | Inverse (undo) | Typical response |
|------|:---:|----------------|------------------|
| `vm_list` | R | — | ~50–500 tok (one row per VM) |
| `vm_get` | R | — | ~120 tok |
| `vm_config` | R | — | ~120 tok |
| `vm_start` | W | `vm_stop` | task UPID |
| `vm_stop` | W | `vm_start` | task UPID |
| `vm_shutdown` | W | `vm_start` | task UPID |
| `vm_reboot` | W | — (no inverse) | task UPID |
| `vm_reconfigure` | W | `vm_reconfigure` (prior cores/memory) | applied + previous |
| `vm_clone` | W | `vm_delete(newid)` | task UPID |
| `vm_delete` | W | — (irreversible, risk=high) | task UPID |
| `vm_migrate` | W | `vm_migrate` (back to source node) | task UPID |

## Snapshots (4)

| Tool | R/W | Inverse | Notes |
|------|:---:|---------|-------|
| `vm_list_snapshots` | R | — | name + description |
| `vm_snapshot_create` | W | `vm_snapshot_delete` | |
| `vm_snapshot_delete` | W | — | |
| `vm_snapshot_rollback` | W | — (irreversible, risk=high) | discards newer state |

## Disk (2)

| Tool | R/W | Inverse | Notes |
|------|:---:|---------|-------|
| `vm_resize_disk` | W | — (grow-only; shrink refused) | `+<N>G` or larger absolute |
| `vm_move_disk` | W | `vm_move_disk` (back to source storage) | task UPID |

## Backups — vzdump (3)

| Tool | R/W | Inverse | Notes |
|------|:---:|---------|-------|
| `backup_list` | R | — | archives on a storage, filterable by vmid |
| `vm_backup` | W | — | task UPID; mode snapshot/suspend/stop |
| `backup_restore` | W | `vm_delete` only when restored into a free vmid; none on forced overwrite (risk=high) | task UPID |

## LXC containers (3)

| Tool | R/W | Inverse |
|------|:---:|---------|
| `ct_list` | R | — |
| `ct_start` | W | `ct_stop` |
| `ct_stop` | W | `ct_start` |

## Cluster / tasks (7)

| Tool | R/W | Notes |
|------|:---:|-------|
| `node_list` | R | status, cpu load, memory |
| `cluster_status` | R | membership + quorum |
| `task_status` | R | poll an async UPID (clone/migrate/backup) |
| `cluster_resources` | R | `/cluster/resources` inventory (vm/node/storage filter) |
| `node_status` | R | one node: cpu, load average, memory, uptime |
| `task_log` | R | log lines of an async task by UPID |
| `next_vmid` | R | a free VMID for a new guest |

## HA (2)

| Tool | R/W | Notes |
|------|:---:|-------|
| `ha_status` | R | `{configured, entries}`; clear signal when HA absent |
| `ha_resource_list` | R | HA-managed resources; empty when HA absent |

## Pools (2)

| Tool | R/W | Notes |
|------|:---:|-------|
| `pool_list` | R | poolid + comment |
| `pool_members` | R | members (VMs/CTs/storage) of a pool |

## Firewall — read-only (2)

| Tool | R/W | Notes |
|------|:---:|-------|
| `vm_firewall_rules_list` | R | per-VM firewall rules |
| `cluster_firewall_status` | R | cluster firewall enable + default policies |

## Guest agent (1)

| Tool | R/W | Notes |
|------|:---:|-------|
| `vm_agent_ping` | R | `responsive` bool; absence reported, not crashed |

## Storage (2)

| Tool | R/W | Notes |
|------|:---:|-------|
| `storage_list` | R | pools: type, total/used/avail |
| `storage_content` | R | volumes: ISOs, disk images, backups, templates |

## Not yet covered (preview scope)

VM create-from-scratch / template instantiation, guest agent **exec**
(intentionally omitted as too risky), container create/clone/destroy, firewall
**rule mutation** (read-only for now), and ACL management. These are the natural
next additions — each gets a matching `@governed_tool` wrapper and an `undo=`
declaration where a clean inverse exists. Missing something? Open an issue/PR.
